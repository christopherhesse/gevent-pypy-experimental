import sys
import greentest
import gevent
from gevent.hub import get_hub


def raise_(ex):
    raise ex


MSG = 'should be re-raised and caught'


class Test(greentest.TestCase):

    error_fatal = False

    def test_sys_exit(self):
        self.start(sys.exit, MSG)

        try:
            gevent.sleep(0.001)
        except SystemExit:
            ex = sys.exc_info()[1]
            assert str(ex) == MSG, repr(str(ex))

    def test_keyboard_interrupt(self):
        self.start(raise_, KeyboardInterrupt)

        try:
            gevent.sleep(0.001)
        except KeyboardInterrupt:
            pass

    def test_system_error(self):
        self.start(raise_, SystemError(MSG))

        try:
            gevent.sleep(0.001)
        except SystemError:
            ex = sys.exc_info()[1]
            assert str(ex) == MSG, repr(str(ex))

    def test_exception(self):
        self.start(raise_, Exception('regular exception must not kill the program'))
        gevent.sleep(0.001)


class TestCallback(Test):

    def setUp(self):
        super(TestCallback, self).setUp()
        self.x = get_hub().loop.callback()

    def tearDown(self):
        assert not self.x.pending, self.x

    def start(self, *args):
        self.x.start(*args)


class TestSpawn(Test):

    def tearDown(self):
        assert self.x.dead, self.x

    def start(self, *args):
        self.x = gevent.spawn(*args)


del Test

if __name__ == '__main__':
    greentest.main()
