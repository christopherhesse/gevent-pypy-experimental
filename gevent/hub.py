# Copyright (c) 2009-2011 Denis Bilenko. See LICENSE for details.

import sys
import os
import traceback
from gevent import core


__all__ = ['getcurrent',
           'GreenletExit',
           'spawn_raw',
           'sleep',
           'kill',
           'signal',
           'fork',
           'get_hub',
           'Hub',
           'Waiter']


def __import_py_magic_greenlet():
    try:
        from py.magic import greenlet
        return greenlet
    except ImportError:
        pass

try:
    greenlet = __import__('greenlet').greenlet
except ImportError:
    greenlet = __import_py_magic_greenlet()
    if greenlet is None:
        raise

getcurrent = greenlet.getcurrent
GreenletExit = greenlet.GreenletExit


# In greenlet >= 0.3.2, GreenletExit is a subclass of BaseException
# In greenlet <= 0.3.1, GreenletExit is a subclass of Exception
# Since, GreenletExit is a part of gevent's public interface, we want
# it to be consistent, so if we got older greenlet, we monkey patch
# GreenletExit's __bases__
if GreenletExit.__bases__[0] is Exception:
    GreenletExit.__bases__ = (BaseException, )

if sys.version_info[0] <= 2:
    thread = __import__('thread')
else:
    thread = __import__('_thread')
threadlocal = thread._local
_threadlocal = threadlocal()
_threadlocal.Hub = None
try:
    _original_fork = os.fork
except AttributeError:
    _original_fork = None
    __all__.remove('fork')
get_ident = thread.get_ident
MAIN_THREAD = get_ident()


def _switch_helper(function, args, kwargs):
    # work around the fact that greenlet.switch does not support keyword args
    return function(*args, **kwargs)


def spawn_raw(function, *args, **kwargs):
    hub = get_hub()
    if kwargs:
        g = greenlet(_switch_helper, hub)
        hub.loop.run_callback(g.switch, function, args, kwargs)
    else:
        g = greenlet(function, hub)
        hub.loop.run_callback(g.switch, *args)
    return g


def sleep(seconds=0):
    """Put the current greenlet to sleep for at least *seconds*.

    *seconds* may be specified as an integer, or a float if fractional seconds
    are desired.

    If *seconds* is equal to or less than zero, yield control the other coroutines
    without actually putting the process to sleep. The :class:`core.idle` watcher
    with the highest priority is used to achieve that.
    """
    hub = get_hub()
    loop = hub.loop
    if seconds <= 0:
        watcher = loop.idle()
        watcher.priority = loop.MAXPRI
    else:
        watcher = loop.timer(seconds)
    hub.wait(watcher)


def idle(priority=0):
    hub = get_hub()
    watcher = hub.loop.idle()
    if priority:
        watcher.priority = priority
    hub.wait(watcher)


def kill(greenlet, exception=GreenletExit):
    """Kill greenlet asynchronously. The current greenlet is not unscheduled.

    Note, that :meth:`gevent.Greenlet.kill` method does the same and more. However,
    MAIN greenlet - the one that exists initially - does not have ``kill()`` method
    so you have to use this function.
    """
    if not greenlet.dead:
        get_hub().loop.run_callback(greenlet.throw, exception)


class signal(object):

    greenlet_class = None

    def __init__(self, signalnum, handler, *args, **kwargs):
        self.hub = get_hub()
        self.watcher = self.hub.loop.signal(signalnum, ref=False)
        self.watcher.start(self._start)
        self.handler = handler
        self.args = args
        self.kwargs = kwargs
        if self.greenlet_class is None:
            from gevent import Greenlet
            self.greenlet_class = Greenlet

    def _get_ref(self):
        return self.watcher.ref

    def _set_ref(self, value):
        self.watcher.ref = value

    ref = property(_get_ref, _set_ref)
    del _get_ref, _set_ref

    def cancel(self):
        self.watcher.stop()

    def _start(self):
        try:
            greenlet = self.greenlet_class(self.handle)
            greenlet.switch()
        except:
            self.hub.handle_error(None, *sys._exc_info())

    def handle(self):
        try:
            self.handler(*self.args, **self.kwargs)
        except:
            self.hub.handle_error(None, *sys.exc_info())


if _original_fork is not None:

    def fork():
        result = _original_fork()
        if not result:
            get_hub().loop.reinit()
        return result


def get_hub_class():
    """Return the type of hub to use for the current thread.

    If there's no type of hub for the current thread yet, 'gevent.hub.Hub' is used.
    """
    global _threadlocal
    try:
        hubtype = _threadlocal.Hub
    except AttributeError:
        hubtype = None
    if hubtype is None:
        hubtype = _threadlocal.Hub = Hub
    return hubtype


def get_hub(*args, **kwargs):
    """Return the hub for the current thread.

    If hub does not exists in the current thread, the new one is created with call to :meth:`get_hub_class`.
    """
    global _threadlocal
    try:
        return _threadlocal.hub
    except AttributeError:
        hubtype = get_hub_class()
        hub = _threadlocal.hub = hubtype(*args, **kwargs)
        return hub


def _get_hub():
    """Return the hub for the current thread.

    Return ``None`` if no hub has been created yet.
    """
    global _threadlocal
    try:
        return _threadlocal.hub
    except AttributeError:
        pass


def set_hub(hub):
    _threadlocal.hub = hub


if sys.version_info[0] >= 3:
    basestring = (str, bytes)

    def exc_clear():
        pass
else:
    basestring = basestring
    exc_clear = sys.exc_clear


def _import(path):
    if isinstance(path, list):
        error = ImportError('Cannot import from empty list: %r' % (path, ))
        for item in path:
            try:
                return _import(item)
            except ImportError:
                error = sys.exc_info()[1]
        raise error
    if not isinstance(path, basestring):
        return path
    if '.' not in path:
        raise ImportError("Cannot import %r (required format: module.class)" % path)
    module, item = path.rsplit('.', 1)
    x = __import__(module)
    for attr in path.split('.')[1:]:
        x = getattr(x, attr, _NONE)
        if x is _NONE:
            raise ImportError('Cannot import name %r from %r' % (attr, x))
    return x


def config(default, envvar):
    result = os.environ.get(envvar) or default
    if isinstance(result, basestring):
        return result.split(',')
    return result


def resolver_config(default, envvar):
    result = config(default, envvar)
    return [_resolvers.get(x, x) for x in result]


_resolvers = {'ares': 'gevent.resolver_ares.Resolver',
              'thread': 'gevent.resolver_thread.Resolver',
              'block': 'gevent.socket.BlockingResolver'}


class Hub(greenlet):
    """A greenlet that runs the event loop.

    It is created automatically by :func:`get_hub`.
    """

    SYSTEM_ERROR = (KeyboardInterrupt, SystemExit, SystemError)
    NOT_ERROR = (GreenletExit, SystemExit)
    loop_class = config('gevent.core.loop', 'GEVENT_LOOP')
    resolver_class = ['gevent.resolver_ares.Resolver',
                      'gevent.resolver_thread.Resolver',
                      'gevent.socket.BlockingResolver']
    resolver_class = resolver_config(resolver_class, 'GEVENT_RESOLVER')
    threadpool_class = config('gevent.threadpool.ThreadPool', 'GEVENT_THREADPOOL')
    DEFAULT_BACKEND = config(None, 'GEVENT_BACKEND')
    format_context = 'pprint.pformat'
    threadpool_size = 10

    def __init__(self, loop=None, default=None):
        greenlet.__init__(self)
        if hasattr(loop, 'run'):
            if default is not None:
                raise TypeError("Unexpected argument: default")
            self.loop = loop
        else:
            if default is None:
                default = get_ident() == MAIN_THREAD
            loop_class = _import(self.loop_class)
            if loop is None:
                loop = self.DEFAULT_BACKEND
            self.loop = loop_class(flags=loop, default=default)
        self._resolver = None
        self._threadpool = None
        self.format_context = _import(self.format_context)

    def __repr__(self):
        result = '<%s at 0x%x %s' % (self.__class__.__name__, id(self), self.loop._format())
        if self._resolver is not None:
            result += ' resolver=%r' % self._resolver
        if self._threadpool is not None:
            result += ' threadpool=%r' % self._threadpool
        return result + '>'

    def handle_error(self, context, type, value, tb):
        self.print_exception(context, type, value, tb)
        if context is None or issubclass(type, self.SYSTEM_ERROR):
            self.handle_system_error(type, value)

    def handle_system_error(self, type, value):
        current = getcurrent()
        if current is self or current is self.parent:
            self.parent.throw(type, value)
        else:
            self.loop.run_callback(self.parent.throw, type, value)

    def print_exception(self, context, type, value, tb):
        if issubclass(type, self.NOT_ERROR):
            return
        traceback.print_exception(type, value, tb)
        del tb
        if context is not None:
            if not isinstance(context, str):
                try:
                    context = self.format_context(context)
                except:
                    traceback.print_exc()
                    context = repr(context)
            sys.stderr.write('%s failed with %s\n\n' % (context, getattr(type, '__name__', 'exception'), ))

    def switch(self):
        exc_type, exc_value = sys.exc_info()[:2]
        try:
            switch_out = getattr(getcurrent(), 'switch_out', None)
            if switch_out is not None:
                switch_out()
            exc_clear()
            return greenlet.switch(self)
        finally:
            core.set_exc_info(exc_type, exc_value)

    def switch_out(self):
        raise AssertionError('Impossible to call blocking function in the event loop callback')

    def wait(self, watcher):
        unique = object()
        watcher.start(getcurrent().switch, unique)
        try:
            result = self.switch()
            assert result is unique, 'Invalid switch into %s: %r' % (getcurrent(), result)
        finally:
            watcher.stop()

    def cancel_wait(self, watcher, error):
        if watcher.callback is not None:
            self.loop.run_callback(self._cancel_wait, watcher, error)

    def _cancel_wait(self, watcher, error):
        if watcher.active:
            switch = watcher.callback
            if switch is not None:
                greenlet = getattr(switch, '__self__', None)
                if greenlet is not None:
                    greenlet.throw(error)

    def run(self):
        assert self is getcurrent(), 'Do not call Hub.run() directly'
        while True:
            loop = self.loop
            loop.error_handler = self
            try:
                loop.run()
            finally:
                loop.error_handler = None  # break the refcount cycle
            self.parent.throw(LoopExit('This operation would block forever'))
        # this function must never return, as it will cause switch() in the parent greenlet
        # to return an unexpected value
        # It is still possible to kill this greenlet with throw. However, in that case
        # switching to it is no longer safe, as switch will return immediatelly

    def join(self, timeout=None, event=None):
        """Wait for the event loop to finish. Exits only when there are
        no more spawned greenlets, started servers, active timeouts or watchers.

        If *timeout* is provided, wait no longer for the specified number of seconds.
        If *event* was provided, exit when it was signalled with :meth:`Event.set` method.

        Returns True if exited because the loop finished execution.
        Returns False if exited because of timeout expired or event was signalled.
        """
        assert getcurrent() is self.parent, "only possible from the MAIN greenlet"
        if self.dead:
            return True

        waiter = Waiter()

        if event is not None:
            switch = waiter.switch
            event.rawlink(switch)

        try:
            if timeout is not None:
                timeout = self.loop.timer(timeout, ref=False)
                timeout.start(waiter.switch)

            try:
                try:
                    waiter.get()
                except LoopExit:
                    return True
            finally:
                if timeout is not None:
                    timeout.stop()
        finally:
            if event is not None:
                event.unlink(switch)
        return False

    def destroy(self):
        # this function would be useful after fork / before exec
        global _threadlocal
        if self._resolver is not None:
            self._resolver.close()
            del self._resolver
        if self._threadpool is not None:
            self._threadpool.close()
            del self._threadpool
        self.loop.destroy()
        del self.loop
        if getattr(_threadlocal, 'hub', None) is self:
            del _threadlocal.hub

    def _get_resolver(self):
        if self._resolver is None:
            if self.resolver_class is not None:
                self.resolver_class = _import(self.resolver_class)
                self._resolver = self.resolver_class(hub=self)
        return self._resolver

    def _set_resolver(self, value):
        self._resolver = value

    def _del_resolver(self):
        del self._resolver

    resolver = property(_get_resolver, _set_resolver, _del_resolver)

    def _get_threadpool(self):
        if self._threadpool is None:
            if self.threadpool_class is not None:
                self.threadpool_class = _import(self.threadpool_class)
                self._threadpool = self.threadpool_class(self.threadpool_size, hub=self)
        return self._threadpool

    def _set_threadpool(self, value):
        self._threadpool = value

    def _del_threadpool(self):
        del self._threadpool

    threadpool = property(_get_threadpool, _set_threadpool, _del_threadpool)


class LoopExit(Exception):
    pass


class Waiter(object):
    """A low level communication utility for greenlets.

    Wrapper around greenlet's ``switch()`` and ``throw()`` calls that makes them somewhat safer:

    * switching will occur only if the waiting greenlet is executing :meth:`get` method currently;
    * any error raised in the greenlet is handled inside :meth:`switch` and :meth:`throw`
    * if :meth:`switch`/:meth:`throw` is called before the receiver calls :meth:`get`, then :class:`Waiter`
      will store the value/exception. The following :meth:`get` will return the value/raise the exception.

    The :meth:`switch` and :meth:`throw` methods must only be called from the :class:`Hub` greenlet.
    The :meth:`get` method must be called from a greenlet other than :class:`Hub`.

        >>> result = Waiter()
        >>> timer = get_hub().loop.timer(0.1)
        >>> timer.start(result.switch, 'hello from Waiter')
        >>> result.get() # blocks for 0.1 seconds
        'hello from Waiter'

    If switch is called before the greenlet gets a chance to call :meth:`get` then
    :class:`Waiter` stores the value.

        >>> result = Waiter()
        >>> timer = get_hub().loop.timer(0.1)
        >>> timer.start(result.switch, 'hi from Waiter')
        >>> sleep(0.2)
        >>> result.get() # returns immediatelly without blocking
        'hi from Waiter'

    .. warning::

        This a limited and dangerous way to communicate between greenlets. It can easily
        leave a greenlet unscheduled forever if used incorrectly. Consider using safer
        :class:`Event`/:class:`AsyncResult`/:class:`Queue` classes.
    """

    __slots__ = ['hub', 'greenlet', 'value', '_exception']

    def __init__(self, hub=None):
        if hub is None:
            self.hub = get_hub()
        else:
            self.hub = hub
        self.greenlet = None
        self.value = None
        self._exception = _NONE

    def clear(self):
        self.greenlet = None
        self.value = None
        self._exception = _NONE

    def __str__(self):
        if self._exception is _NONE:
            return '<%s greenlet=%s>' % (type(self).__name__, self.greenlet)
        elif self._exception is None:
            return '<%s greenlet=%s value=%r>' % (type(self).__name__, self.greenlet, self.value)
        else:
            return '<%s greenlet=%s exc_info=%r>' % (type(self).__name__, self.greenlet, self.exc_info)

    def ready(self):
        """Return true if and only if it holds a value or an exception"""
        return self._exception is not _NONE

    def successful(self):
        """Return true if and only if it is ready and holds a value"""
        return self._exception is None

    @property
    def exc_info(self):
        "Holds the exception info passed to :meth:`throw` if :meth:`throw` was called. Otherwise ``None``."
        if self._exception is not _NONE:
            return self._exception

    def switch(self, value=None):
        """Switch to the greenlet if one's available. Otherwise store the value."""
        if self.greenlet is None:
            self.value = value
            self._exception = None
        else:
            assert getcurrent() is self.hub, "Can only use Waiter.switch method from the Hub greenlet"
            try:
                self.greenlet.switch(value)
            except:
                self.hub.handle_error(self.greenlet.switch, *sys.exc_info())

    def switch_args(self, *args):
        return self.switch(args)

    def throw(self, *throw_args):
        """Switch to the greenlet with the exception. If there's no greenlet, store the exception."""
        if self.greenlet is None:
            self._exception = throw_args
        else:
            assert getcurrent() is self.hub, "Can only use Waiter.switch method from the Hub greenlet"
            try:
                self.greenlet.throw(*throw_args)
            except:
                self.hub.handle_error(self.greenlet.throw, *sys.exc_info())

    def get(self):
        """If a value/an exception is stored, return/raise it. Otherwise until switch() or throw() is called."""
        if self._exception is not _NONE:
            if self._exception is None:
                return self.value
            else:
                getcurrent().throw(*self._exception)
        else:
            assert self.greenlet is None, 'This Waiter is already used by %r' % (self.greenlet, )
            self.greenlet = getcurrent()
            try:
                return self.hub.switch()
            finally:
                self.greenlet = None

    def __call__(self, source):
        if source.exception is None:
            self.switch(source.value)
        else:
            self.throw(source.exception)

    # can also have a debugging version, that wraps the value in a tuple (self, value) in switch()
    # and unwraps it in wait() thus checking that switch() was indeed called


class _NONE(object):
    "A special thingy you must never pass to any of gevent API"
    __slots__ = []

    def __repr__(self):
        return '<_NONE>'

_NONE = _NONE()
