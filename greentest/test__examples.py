import sys
import os
import glob
from os.path import join, abspath, dirname, normpath, basename
import unittest
try:
    import urllib2
except ImportError:
    from urllib import request as urllib2
import time
import signal
import re
import gevent
from gevent import socket
import mysubprocess as subprocess
from gevent.server import DatagramServer, StreamServer

# Ignore tracebacks: KeyboardInterrupt

examples_directory = normpath(join(dirname(abspath(__file__)), '..', 'examples'))
examples = [basename(x) for x in glob.glob(examples_directory + '/*.py')]
simple_examples = []


for example in examples:
    if 'serve_forever' not in open(join(examples_directory, example)).read():
        simple_examples.append(example)


def make_test(path):

    if sys.platform == 'win32' and os.path.basename(path) in ('geventsendfile.py', 'processes.py'):
        print 'Ignoring', path
        return

    if ' ' in path:
        path = '"%s"' % path

    class Test(unittest.TestCase):

        def test(self):
            run_script(self.path)

    Test.__name__ = 'Test_' + basename(path).split('.')[0]
    assert Test.__name__ not in globals(), Test.__name__
    Test.path = path

    return Test


def run_script(path, *args):
    cmd = [sys.executable, join(examples_directory, path)] + list(args)
    popen = subprocess.Popen(cmd)
    result = popen.gevent_wait()
    if result != 0:
        raise AssertionError('%r failed with code %s' % (cmd, result))


class BaseTestServer(unittest.TestCase):
    args = []

    def setUp(self):
        self.process = subprocess.Popen([sys.executable, join(examples_directory, self.path)] + self.args, cwd=examples_directory)
        time.sleep(1)

    def tearDown(self):
        self.assertEqual(self.process.poll(), None)
        self.process.interrupt()
        time.sleep(0.05)


class Test_httpserver(BaseTestServer):
    URL = 'http://localhost:8088'
    not_found_message = '<h1>Not Found</h1>'

    def read(self, path='/'):
        url = self.URL + path
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError:
            response = sys.exc_info()[1]
        return '%s %s' % (response.code, response.msg), response.read()

    def _test_hello(self):
        status, data = self.read('/')
        self.assertEqual(status, '200 OK')
        self.assertEqual(data, "<b>hello world</b>")

    def _test_not_found(self):
        status, data = self.read('/xxx')
        self.assertEqual(status, '404 Not Found')
        self.assertEqual(data, self.not_found_message)

    def test(self):
        # running all the test methods now so that we don't set up a server more than once
        for method in dir(self):
            if method.startswith('_test'):
                function = getattr(self, method)
                if callable(function):
                    function()


class Test_wsgiserver(Test_httpserver):
    path = 'wsgiserver.py'


if hasattr(socket, 'ssl'):

    class Test_wsgiserver_ssl(Test_httpserver):
        path = 'wsgiserver_ssl.py'
        URL = 'https://localhost:8443'

else:

    class Test_wsgiserver_ssl(unittest.TestCase):
        path = 'wsgiserver_ssl.py'

        def setUp(self):
            self.process = subprocess.Popen([sys.executable, join(examples_directory, self.path)],
                                            cwd=examples_directory, stderr=subprocess.PIPE)
            time.sleep(1)

        def test(self):
            self.assertEqual(self.process.poll(), 1)
            stderr = self.process.stderr.read().strip()
            m = re.match('Traceback \(most recent call last\):.*?ImportError: .*?ssl.*', stderr, re.DOTALL)
            assert m is not None, repr(stderr)

        def tearDown(self):
            if self.process.poll() is None:
                try:
                    SIGINT = getattr(signal, 'SIGINT', None)
                    if SIGINT is not None:
                        os.kill(self.process.pid, SIGINT)
                        time.sleep(0.1)
                    self.assertEqual(self.process.poll(), 1)
                finally:
                    if self.process.poll() is None:
                        self.process.kill()


class Test_webpy(Test_httpserver):
    path = 'webpy.py'
    not_found_message = 'not found'

    def _test_hello(self):
        status, data = self.read('/')
        self.assertEqual(status, '200 OK')
        assert "Hello, world" in data, repr(data)

    def _test_long(self):
        start = time.time()
        status, data = self.read('/long')
        delay = time.time() - start
        assert 10 - 0.1 < delay < 10 + 0.1, delay
        self.assertEqual(status, '200 OK')
        self.assertEqual(data, 'Hello, 10 seconds later')


class Test_webproxy(Test_httpserver):
    path = 'webproxy.py'

    def test(self):
        status, data = self.read('/')
        self.assertEqual(status, '200 OK')
        assert "gevent example" in data, repr(data)
        status, data = self.read('/http://www.google.com')
        self.assertEqual(status, '200 OK')
        assert 'google' in data.lower(), repr(data)


class Test_echoserver(BaseTestServer):
    path = 'echoserver.py'

    def test(self):
        def test_client(message):
            conn = socket.create_connection(('127.0.0.1', 6000)).makefile(bufsize=1)
            welcome = conn.readline()
            assert 'Welcome' in welcome, repr(welcome)
            conn.write(message)
            received = conn.read(len(message))
            self.assertEqual(received, message)
            conn._sock.settimeout(0.1)
            self.assertRaises(socket.timeout, conn.read, 1)
        client1 = gevent.spawn(test_client, 'hello\r\n')
        client2 = gevent.spawn(test_client, 'world\r\n')
        gevent.joinall([client1, client2], raise_error=True)


class Test_udp_client(unittest.TestCase):

    path = 'udp_client.py'

    def test(self):
        log = []
        def handle(message, address):
            log.append(message)
            server.sendto('reply-from-server', address)
        server = DatagramServer('127.0.0.1:9000', handle)
        server.start()
        try:
            run_script(self.path, 'Test_udp_client')
        finally:
            server.close()
        self.assertEqual(log, ['Test_udp_client'])


class Test_udp_server(BaseTestServer):
    path = 'udp_server.py'

    def test(self):
        address = ('localhost', 9000)
        sock = socket.socket(type=socket.SOCK_DGRAM)
        sock.connect(address)
        sock.send('Test_udp_server')
        data, address = sock.recvfrom(8192)
        self.assertEqual(data, 'Received 15 bytes')


class Test_portforwarder(BaseTestServer):
    path = 'portforwarder.py'
    args = ['127.0.0.5:9999', '127.0.0.6:9999']

    def test(self):
        log = []

        def handle(socket, address):
            while True:
                data = socket.recv(1024)
                log.append(data)
                if not data:
                    break

        server = StreamServer('127.0.0.6:9999', handle)
        server.start()
        try:
            conn = socket.create_connection(('127.0.0.5', 9999))
            conn.sendall('msg1')
            gevent.sleep(0.01)
            self.assertEqual(log, ['msg1'])
            conn.sendall('msg2')
            conn.close()
        finally:
            server.close()
        gevent.sleep(0.01)


tests = set()
for klass in globals().keys():
    if klass.startswith('Test'):
        path = getattr(globals()[klass], 'path', None)
        if path is not None:
            tests.add(path)


for example in simple_examples:
    if example in tests:
        continue
    test = make_test(example)
    if test is not None:
        globals()[test.__name__] = test
        print ('Added %s' % test.__name__)
    del test


class TestAllTested(unittest.TestCase):

    def test(self):
        untested = set(examples) - set(simple_examples)
        untested = set(basename(path) for path in untested) - tests
        if untested:
            raise AssertionError('The following examples have not been tested: %s\n - %s' % (len(untested), '\n - '.join(untested)))


del Test_httpserver


if __name__ == '__main__':
    unittest.main()
