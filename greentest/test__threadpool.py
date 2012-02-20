from time import time
import random
import greentest
from gevent.threadpool import ThreadPool
from gevent import six
import gevent


class TestCase(greentest.TestCase):

    def cleanup(self):
        if self.pool is not None:
            self.pool.kill()


class PoolBasicTests(TestCase):

    def test_execute_async(self):
        self.pool = pool = ThreadPool(2)
        r = []
        first = pool.spawn(r.append, 1)
        first.get()
        self.assertEqual(r, [1])
        gevent.sleep(0)

        pool.apply_async(r.append, (2, ))
        self.assertEqual(r, [1])

        pool.apply_async(r.append, (3, ))
        self.assertEqual(r, [1])

        pool.apply_async(r.append, (4, ))
        self.assertEqual(r, [1])
        gevent.sleep(0.01)
        self.assertEqual(sorted(r), [1, 2, 3, 4])

    def test_apply(self):
        self.pool = pool = ThreadPool(1)
        result = pool.apply(lambda a: ('foo', a), (1, ))
        self.assertEqual(result, ('foo', 1))

    def test_init_valuerror(self):
        self.switch_expected = False
        self.assertRaises(ValueError, ThreadPool, -1)
        self.pool = None

#
# tests from standard library test/test_multiprocessing.py


class TimingWrapper(object):

    def __init__(self, func):
        self.func = func
        self.elapsed = None

    def __call__(self, *args, **kwds):
        t = time()
        try:
            return self.func(*args, **kwds)
        finally:
            self.elapsed = time() - t


def sqr(x, wait=0.0):
    gevent.sleep(wait)
    return x * x


def sqr_random_sleep(x):
    gevent.sleep(random.random() * 0.1)
    return x * x


TIMEOUT1, TIMEOUT2, TIMEOUT3 = 0.082, 0.035, 0.14


class TestPool(TestCase):
    __timeout__ = 5
    size = 1

    def setUp(self):
        greentest.TestCase.setUp(self)
        self.pool = ThreadPool(self.size)

    def test_apply(self):
        papply = self.pool.apply
        self.assertEqual(papply(sqr, (5,)), sqr(5))
        self.assertEqual(papply(sqr, (), {'x': 3}), sqr(x=3))

    def test_map(self):
        pmap = self.pool.map
        self.assertEqual(pmap(sqr, range(10)), list(map(sqr, range(10))))
        self.assertEqual(pmap(sqr, range(100)), list(map(sqr, range(100))))

    def test_async(self):
        res = self.pool.apply_async(sqr, (7, TIMEOUT1,))
        get = TimingWrapper(res.get)
        self.assertEqual(get(), 49)
        self.assertAlmostEqual(get.elapsed, TIMEOUT1, 1)

    def test_async_callback(self):
        result = []
        res = self.pool.apply_async(sqr, (7, TIMEOUT1,), callback=lambda x: result.append(x))
        get = TimingWrapper(res.get)
        self.assertEqual(get(), 49)
        self.assertAlmostEqual(get.elapsed, TIMEOUT1, 1)
        gevent.sleep(0)  # let's the callback run
        assert result == [49], result

    def test_async_timeout(self):
        res = self.pool.apply_async(sqr, (6, TIMEOUT2 + 0.2))
        get = TimingWrapper(res.get)
        self.assertRaises(gevent.Timeout, get, timeout=TIMEOUT2)
        self.assertAlmostEqual(get.elapsed, TIMEOUT2, 1)
        self.pool.join()

    def test_imap(self):
        it = self.pool.imap(sqr, range(10))
        self.assertEqual(list(it), list(map(sqr, range(10))))

        it = self.pool.imap(sqr, range(10))
        for i in range(10):
            self.assertEqual(six.advance_iterator(it), i * i)
        self.assertRaises(StopIteration, lambda: six.advance_iterator(it))

        it = self.pool.imap(sqr, range(1000))
        for i in range(1000):
            self.assertEqual(six.advance_iterator(it), i * i)
        self.assertRaises(StopIteration, lambda: six.advance_iterator(it))

    def test_imap_random(self):
        it = self.pool.imap(sqr_random_sleep, range(10))
        self.assertEqual(list(it), list(map(sqr, range(10))))

    def test_imap_unordered(self):
        it = self.pool.imap_unordered(sqr, range(1000))
        self.assertEqual(sorted(it), list(map(sqr, range(1000))))

        it = self.pool.imap_unordered(sqr, range(1000))
        self.assertEqual(sorted(it), list(map(sqr, range(1000))))

    def test_imap_unordered_random(self):
        it = self.pool.imap_unordered(sqr_random_sleep, range(10))
        self.assertEqual(sorted(it), list(map(sqr, range(10))))

    def test_terminate(self):
        result = self.pool.map_async(gevent.sleep, [0.1] * ((self.size or 10) * 2))
        gevent.sleep(0.1)
        kill = TimingWrapper(self.pool.kill)
        kill()
        assert kill.elapsed < 0.5, kill.elapsed
        result.join()

    def sleep(self, x):
        gevent.sleep(float(x) / 10.)
        return str(x)

    def test_imap_unordered_sleep(self):
        # testing that imap_unordered returns items in competion order
        result = list(self.pool.imap_unordered(self.sleep, [10, 1, 2]))
        if self.pool.size == 1:
            expected = ['10', '1', '2']
        else:
            expected = ['1', '2', '10']
        self.assertEqual(result, expected)


class TestPool2(TestPool):
    size = 2


class TestPool3(TestPool):
    size = 3


class TestPool10(TestPool):
    size = 10


# class TestJoinSleep(greentest.GenericGetTestCase):
# 
#     def wait(self, timeout):
#         pool = ThreadPool(1)
#         pool.spawn(gevent.sleep, 10)
#         pool.join(timeout=timeout)
# 
# 
# class TestJoinSleep_raise_error(greentest.GenericWaitTestCase):
# 
#     def wait(self, timeout):
#         pool = ThreadPool(1)
#         g = pool.spawn(gevent.sleep, 10)
#         pool.join(timeout=timeout, raise_error=True)


class TestJoinEmpty(TestCase):
    switch_expected = False

    def test(self):
        self.pool = ThreadPool(1)
        self.pool.join()


class TestSpawn(TestCase):
    switch_expected = True

    def test(self):
        self.pool = pool = ThreadPool(1)
        self.assertEqual(len(pool), 0)
        pool.spawn(gevent.sleep, 0.1)
        self.assertEqual(len(pool), 1)
        pool.spawn(gevent.sleep, 0.1)
        # even though the pool is of size 1, it can contain 2 items
        # since we allow +1 for better throughput
        self.assertEqual(len(pool), 2)
        gevent.sleep(0.11)
        self.assertEqual(len(pool), 1)
        gevent.sleep(0.11)
        self.assertEqual(len(pool), 0)


def error_iter():
    yield 1
    yield 2
    raise greentest.ExpectedException


class TestErrorInIterator(TestCase):
    error_fatal = False

    def test(self):
        self.pool = ThreadPool(3)
        self.assertRaises(greentest.ExpectedException, self.pool.map, lambda x: None, error_iter())
        gevent.sleep(0.001)

    def test_unordered(self):
        self.pool = ThreadPool(3)
        def unordered():
            return list(self.pool.imap_unordered(lambda x: None, error_iter()))
        self.assertRaises(greentest.ExpectedException, unordered)
        gevent.sleep(0.001)


class TestMaxsize(TestCase):

    def test_inc(self):
        self.pool = ThreadPool(0)
        done = []
        gevent.spawn(self.pool.spawn, done.append, 1)
        gevent.spawn(self.pool.spawn, done.append, 2)
        gevent.sleep(0.001)
        self.assertEqual(done, [])
        self.pool.maxsize = 1
        gevent.sleep(0.001)
        self.assertEqual(done, [2, 1])


if __name__ == '__main__':
    greentest.main()
