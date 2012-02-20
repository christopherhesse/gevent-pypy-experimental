import ctypes
from ctypes import pointer
import sys
import os
from signal import NSIG

import libev
from lookupable import Lookupable

__all__ = ['get_version',
           'get_header_version',
           'supported_backends',
           'recommended_backends',
           'embeddable_backends',
           'time',
           'loop']

UNDEF = libev.EV_UNDEF
NONE = libev.EV_NONE
READ = libev.EV_READ
WRITE = libev.EV_WRITE
TIMER = libev.EV_TIMER
PERIODIC = libev.EV_PERIODIC
SIGNAL = libev.EV_SIGNAL
CHILD = libev.EV_CHILD
STAT = libev.EV_STAT
IDLE = libev.EV_IDLE
PREPARE = libev.EV_PREPARE
CHECK = libev.EV_CHECK
EMBED = libev.EV_EMBED
FORK = libev.EV_FORK
CLEANUP = libev.EV_CLEANUP
ASYNC = libev.EV_ASYNC
CUSTOM = libev.EV_CUSTOM
ERROR = libev.EV_ERROR

READWRITE = libev.EV_READ | libev.EV_WRITE

MINPRI = libev.EV_MINPRI
MAXPRI = libev.EV_MAXPRI

BACKEND_PORT = libev.EVBACKEND_PORT
BACKEND_KQUEUE = libev.EVBACKEND_KQUEUE
BACKEND_EPOLL = libev.EVBACKEND_EPOLL
BACKEND_POLL = libev.EVBACKEND_POLL
BACKEND_SELECT = libev.EVBACKEND_SELECT
NOENV = libev.EVFLAG_NOENV
FORKCHECK = libev.EVFLAG_FORKCHECK
NOINOTIFY = libev.EVFLAG_NOINOTIFY
SIGNALFD = libev.EVFLAG_SIGNALFD
NOSIGMASK = libev.EVFLAG_NOSIGMASK

class _EVENTSType(object):
    def __repr__(self):
        return 'gevent.core.EVENTS'
GEVENT_CORE_EVENTS = _EVENTSType()
EVENTS = GEVENT_CORE_EVENTS

def get_version():
    return 'libev-%d.%02d' % (libev.ev_version_major(), libev.ev_version_minor())


def get_header_version():
    return 'libev-%d.%02d' % (libev.EV_VERSION_MAJOR, libev.EV_VERSION_MINOR)


# This list backends in the order they are actually tried by libev
_flags = [(libev.EVBACKEND_PORT, 'port'),
          (libev.EVBACKEND_KQUEUE, 'kqueue'),
          (libev.EVBACKEND_EPOLL, 'epoll'),
          (libev.EVBACKEND_POLL, 'poll'),
          (libev.EVBACKEND_SELECT, 'select'),
          (libev.EVFLAG_NOENV, 'noenv'),
          (libev.EVFLAG_FORKCHECK, 'forkcheck'),
          (libev.EVFLAG_SIGNALFD, 'signalfd'),
          (libev.EVFLAG_NOSIGMASK, 'nosigmask')]


_flags_str2int = dict((string, flag) for (flag, string) in _flags)


_events = [(libev.EV_READ,     'READ'),
           (libev.EV_WRITE,    'WRITE'),
           (libev.EV__IOFDSET, '_IOFDSET'),
           (libev.EV_PERIODIC, 'PERIODIC'),
           (libev.EV_SIGNAL,   'SIGNAL'),
           (libev.EV_CHILD,    'CHILD'),
           (libev.EV_STAT,     'STAT'),
           (libev.EV_IDLE,     'IDLE'),
           (libev.EV_PREPARE,  'PREPARE'),
           (libev.EV_CHECK,    'CHECK'),
           (libev.EV_EMBED,    'EMBED'),
           (libev.EV_FORK,     'FORK'),
           (libev.EV_CLEANUP,  'CLEANUP'),
           (libev.EV_ASYNC,    'ASYNC'),
           (libev.EV_CUSTOM,   'CUSTOM'),
           (libev.EV_ERROR,    'ERROR')]


def _flags_to_list(flags):
    result = []
    for code, value in _flags:
        if flags & code:
            result.append(value)
        flags &= ~code
        if not flags:
            break
    if flags:
        result.append(flags)
    return result


if sys.version_info[0] >= 3:
    basestring = (bytes, str)
else:
    pass #basestring = __builtins__.basestring


def _flags_to_int(flags):
    # Note, that order does not matter, libev has its own predefined order
    if flags is None:
        return 0
    if isinstance(flags, (int, long)):
        return flags
    result = 0
    try:
        if isinstance(flags, basestring):
            return _flags_str2int[flags.lower()]
        for value in flags:
            result |= _flags_str2int[value.lower()]
    except KeyError, ex:
        raise ValueError('Invalid backend or flag: %s\nPossible values: %s' % (ex, ', '.join(sorted(_flags_str2int.keys()))))
    return result


def _str_hex(flag):
    if isinstance(flag, (int, long)):
        return hex(flag)
    return str(flag)


def _check_flags(flags):
    as_list = []
    flags &= libev.EVBACKEND_MASK
    if not flags:
        return
    if not (flags & libev.EVBACKEND_ALL):
        raise ValueError('Invalid value for backend: 0x%x' % flags)
    if not (flags & libev.ev_supported_backends()):
        as_list = [_str_hex(x) for x in _flags_to_list(flags)]
        raise ValueError('Unsupported backend: %s' % '|'.join(as_list))


def _events_to_str(events):
    result = []
    c_flag = 0
    for (flag, string) in _events:
        c_flag = flag
        if events & c_flag:
            result.append(string)
            events = events & (~c_flag)
        if not events:
            break
    if events:
        result.append(hex(events))
    return '|'.join(result)


def supported_backends():
    return _flags_to_list(libev.ev_supported_backends())


def recommended_backends():
    return _flags_to_list(libev.ev_recommended_backends())


def embeddable_backends():
    return _flags_to_list(libev.ev_embeddable_backends())


def time():
    return libev.ev_time()


class Loop(Lookupable):
    _ptr = None
    error_handler = None
    _signal_checker = libev.ev_prepare()
# #ifdef _WIN32
#     _periodic_signal_checker = libev.ev_timer()
# #endif

    def __init__(self, flags=None, default=True, ptr=None):
        libev.ev_prepare_init(self._signal_checker, gevent_signal_check)
# #ifdef _WIN32
#         libev.ev_timer_init(self._periodic_signal_checker, gevent_periodic_signal_check, 0.3, 0.3)
# #endif
        if ptr:
            self._ptr = ptr
        else:
            c_flags = _flags_to_int(flags)
            _check_flags(c_flags)
            if default:
                self._ptr = libev.ev_default_loop(c_flags)
                if not self._ptr:
                    raise SystemError("ev_default_loop(%s) failed" % (c_flags, ))
                libev.ev_prepare_start(self._ptr, pointer(self._signal_checker))
# #ifdef _WIN32
#                 libev.ev_timer_start(self._ptr, pointer(self._periodic_signal_checker))
#                 libev.ev_unref(self._ptr)
# #endif
            else:
                self._ptr = libev.ev_loop_new(c_flags)
                if not self._ptr:
                    raise SystemError("ev_loop_new(%s) failed" % (c_flags, ))
            if default or __SYSERR_CALLBACK is None:
                set_syserr_cb(self._handle_syserr)
        self._register_instance()

    def _get_key(self):
        return ctypes.addressof(self._ptr.contents)

    @classmethod
    def lookup_instance(cls, loop_struct):
        return super(Loop, cls).lookup_instance(ctypes.addressof(loop_struct.contents))

    def _stop_signal_checker(self):
        if libev.ev_is_active(pointer(self._signal_checker)):
            libev.ev_ref(self._ptr)
            libev.ev_prepare_stop(self._ptr, pointer(self._signal_checker))
#ifdef _WIN32
        if libev.ev_is_active(pointer(self._periodic_signal_checker)):
            libev.ev_ref(self._ptr)
            libev.ev_timer_stop(self._ptr, pointer(self._periodic_signal_checker))
#endif

    def destroy(self):
        if self._ptr:
            self._stop_signal_checker()
            libev.ev_loop_destroy(self._ptr)
            self._unregister_instance()
            self._ptr = None

    def __dealloc__(self):
        if self._ptr:
            self._stop_signal_checker()
            if not libev.ev_is_default_loop(self._ptr):
                libev.ev_loop_destroy(self._ptr)
            self._unregister_instance()
            self._ptr = None

    @property
    def ptr(self):
        return self._ptr

    @property
    def WatcherType(self):
        return BaseWatcher

    @property
    def MAXPRI(self):
       return libev.EV_MAXPRI

    @property
    def MINPRI(self):
        return libev.EV_MINPRI

    def _handle_syserr(self, message, errno):
        self.handle_error(None, SystemError, SystemError(message + ': ' + os.strerror(errno)), None)

    def handle_error(self, context, type, value, tb):
        error_handler = self.error_handler
        if error_handler is not None:
            # we do want to do getattr every time so that setting Hub.handle_error property just works
            handle_error = getattr(error_handler, 'handle_error', error_handler)
            handle_error(context, type, value, tb)
        else:
            self._default_handle_error(context, type, value, tb)

    def _default_handle_error(self, context, type, value, tb):
        # note: Hub sets its own error handler so this is not used by gevent
        # this is here to make core.loop usable without the rest of gevent
        import traceback
        traceback.print_exception(type, value, tb)
        libev.ev_break(self._ptr, libev.EVBREAK_ONE)

    def run(self, nowait=False, once=False):
        flags = 0
        if nowait:
            flags |= libev.EVRUN_NOWAIT
        if once:
            flags |= libev.EVRUN_ONCE
        libev.ev_run(self._ptr, flags)

    def reinit(self):
        libev.ev_loop_fork(self._ptr)

    def ref(self):
        libev.ev_ref(self._ptr)

    def unref(self):
        libev.ev_unref(self._ptr)

    def break_(self, how=libev.EVBREAK_ONE):
        libev.ev_break(self._ptr, how)

    def verify(self):
        libev.ev_verify(self._ptr)

    def now(self):
        return libev.ev_now(self._ptr)

    def update(self):
        libev.ev_now_update(self._ptr)

    def __repr__(self):
        return '<%s at 0x%x %s>' % (self.__class__.__name__, id(self), self._format())

    @property
    def default(self):
        return True if libev.ev_is_default_loop(self._ptr) else False

    @property
    def iteration(self):
        return libev.ev_iteration(self._ptr)

    @property
    def depth(self):
        return libev.ev_depth(self._ptr)

    @property
    def backend_int(self):
        return libev.ev_backend(self._ptr)

    @property
    def backend(self):
        backend = libev.ev_backend(self._ptr)
        for key, value in _flags:
            if key == backend:
                return value
        return backend

    def io(self, fd, events, ref=True):
        return IOWatcher(self, fd, events, ref)

    def timer(self, after, repeat=0.0, ref=True):
        return TimerWatcher(self, after, repeat, ref)

    def signal(self, signum, ref=True):
        return SignalWatcher(self, signum, ref)

    def idle(self, ref=True):
        return IdleWatcher(self, ref)

    def prepare(self, ref=True):
        return PrepareWatcher(self, ref)

    def fork(self, ref=True):
        return ForkWatcher(self, ref)

    def async(self, ref=True):
        return AsyncWatcher(self, ref)

    #def child(self, int pid, bint trace=0):
    #    return child(self, pid, trace)

    def callback(self):
        return CallbackWatcher(self)

    def run_callback(self, func, *args):
        result = CallbackWatcher(self)
        result.start(func, *args)
        return result

    def _format(self):
        msg = self.backend
        if self.default:
            msg += ' default'
#ifdef LIBEV_EMBED
        # if self.fileno() is not None:
        #     msg += ' fileno=%s' % self.fileno()
        # args = (self.activecnt, self.fdchangecnt, self.timercnt, self.asynccnt)
        # msg += ' ref/io/timer/async=%r/%r/%r/%r' % args
#endif
        return msg

#ifdef LIBEV_EMBED
    #
    # def fileno(self):
    #     raise Exception("Unsupported method in experimental port")
    #     fd = self._ptr.backend_fd
    #     if fd >= 0:
    #         return fd
    #
    # @property
    # def activecnt(self):
    #     raise Exception("Unsupported method in experimental port")
    #     return self._ptr.activecnt
    #
    # @property
    # def fdchangecnt(self):
    #     raise Exception("Unsupported method in experimental port")
    #     return self._ptr.fdchangecnt
    #
    # @property
    # def timercnt(self):
    #     raise Exception("Unsupported method in experimental port")
    #     return self._ptr.timercnt
    #
    # @property
    # def asynccnt(self):
    #     raise Exception("Unsupported method in experimental port")
    #     return self._ptr.asynccnt
#endif
loop = Loop # confusing class name, used by gevent hub.py

class BaseWatcher(Lookupable):
    """Abstract base class for all the watchers"""
    type = None

    def __init__(self, loop, ref=True, *init_args):
        print "NEW WATCHER: ", self.__class__
        self.loop = None
        self._callback = None
        self.args = None

        # about readonly _flags attribute:
        # bit #1 set if object owns Python reference to itself (Py_INCREF was called and we must call Py_DECREF later)
        # bit #2 set if ev_unref() was called and we must call ev_ref() later
        # bit #3 set if user wants to call ev_unref() before start()
        self._flags = 0

        self._watcher_struct = getattr(libev, 'ev_' + self.type)()
        self._watcher_init = getattr(libev, 'ev_' + self.type + '_init')
        self._watcher_start = getattr(libev, 'ev_' + self.type + '_start')
        self._watcher_stop = getattr(libev, 'ev_' + self.type + '_stop')
        self._watcher_callback = create_watcher_callback(self)

        self._watcher_init(self._watcher_struct, self._watcher_callback, *init_args)

        self.loop = loop
        if ref:
            self._flags = 0
        else:
            self._flags = 4

        self._register_instance()

    def _get_key(self):
        return ctypes.addressof(self._watcher_struct)

    @classmethod
    def lookup_instance(cls, watcher_struct):
        return super(BaseWatcher, cls).lookup_instance(ctypes.addressof(watcher_struct))

    def get_ref(self):
        return False if self._flags & 4 else True

    def set_ref(self, value):
        if value:
            if not self._flags & 4:
                return  # ref is already True
            if self._flags & 2:  # ev_unref was called, undo
                libev.ev_ref(self.loop._ptr)
            self._flags &= ~6  # do not want unref, no outstanding unref
        else:
            if self._flags & 4:
                return  # ref is already False
            self._flags |= 4
            if not self._flags & 2 and libev.ev_is_active(pointer(self._watcher_struct)):
                libev.ev_unref(self.loop._ptr)
                self._flags |= 2

    ref = property(get_ref, set_ref)

    def get_callback(self):
        return self._callback

    def set_callback(self, callback):
        if not hasattr(callback, "__call__"):
            raise TypeError("Expected callable, not %r" % callback)
        self._callback = callback

    def delete_callback(self):
        self._callback = None

    callback = property(get_callback, set_callback, delete_callback)

    def stop(self):
        if self._flags & 2:
            libev.ev_ref(self.loop._ptr)
            self._flags &= ~2
        self._watcher_stop(self.loop._ptr, pointer(self._watcher_struct))
        self._callback = None
        self.args = None

    def get_priority(self):
        return libev.ev_priority(pointer(self._watcher_struct))

    def set_priority(self, priority):
        if libev.ev_is_active(pointer(self._watcher_struct)):
            raise AttributeError("Cannot set priority of an active watcher")
        libev.ev_set_priority(pointer(self._watcher_struct), priority)

    priority = property(get_priority, set_priority)

    def _python_incref(self):
        #Py_INCREF(<PyObjectPtr>self)
        self._flags |= 1

    def _libev_unref(self):
        libev.ev_unref(self.loop._ptr)
        self._flags |= 2

    def feed(self, revents, callback, *args):
        self.callback = callback
        self.args = args
        self._libev_unref()
        self._watcher_start(self.loop._ptr, pointer(self._watcher_struct))

    @property
    def pending(self):
        return True if libev.ev_is_pending(pointer(self._watcher_struct)) else False

    def start(self, callback, *args):
        self.callback = callback
        self.args = args
        self._libev_unref()
        self._watcher_start(self.loop._ptr, pointer(self._watcher_struct))
        #self._python_incref()

    def __repr__(self):
        # if Py_ReprEnter(<PyObjectPtr>self) != 0:
        #     return "<...>"
        try:
            format = self._format()
            result = "<%s at 0x%x%s" % (self.__class__.__name__, id(self), format)
            if self.active:
                result += " active"
            if self.pending:
                result += " pending"
            if self.callback is not None:
                result += " callback=%r" % (self.callback, )
            if self.args is not None:
                result += " args=%r" % (self.args, )
            return result + ">"
        finally:
            pass
            # Py_ReprLeave(<PyObjectPtr>self)

    def _format(self):
        return ''

    @property
    def active(self):
        return True if libev.ev_is_active(pointer(self._watcher_struct)) else False

#
# cdef public class io(watcher) [object PyGeventIOObject, type PyGeventIO_Type]:
#
#     WATCHER_BASE(io)
#
#     def start(self, object callback, *args, pass_events=False):
#         self.callback = callback
#         if pass_events:
#             self.args = (GEVENT_CORE_EVENTS, ) + args
#         else:
#             self.args = args
#         LIBEV_UNREF
#         libev.ev_io_start(self.loop._ptr, &self._watcher)
#         PYTHON_INCREF
#
#     ACTIVE
#
#     PENDING
#
# #ifdef _WIN32
#
#     def __init__(self, loop loop, long fd, int events, ref=True):
#         if events & ~(libev.EV__IOFDSET | libev.EV_READ | libev.EV_WRITE):
#             raise ValueError('illegal event mask: %r' % events)
#         cdef int vfd = libev.vfd_open(fd)
#         libev.vfd_free(self._watcher.fd)
#         libev.ev_io_init(&self._watcher, <void *>gevent_callback_io, vfd, events)
#         self.loop = loop
#         if ref:
#             self._flags = 0
#         else:
#             self._flags = 4
#
# #else
#
#     def __init__(self, loop loop, int fd, int events, ref=True):
#         if fd < 0:
#             raise ValueError('fd must be non-negative: %r' % fd)
#         if events & ~(libev.EV__IOFDSET | libev.EV_READ | libev.EV_WRITE):
#             raise ValueError('illegal event mask: %r' % events)
#         libev.ev_io_init(&self._watcher, <void *>gevent_callback_io, fd, events)
#         self.loop = loop
#         if ref:
#             self._flags = 0
#         else:
#             self._flags = 4
#
# #endif
#
#     property fd:
#
#         def __get__(self):
#             return libev.vfd_get(self._watcher.fd)
#
#         def __set__(self, long fd):
#             if libev.ev_is_active(&self._watcher):
#                 raise AttributeError("'io' watcher attribute 'fd' is read-only while watcher is active")
#             cdef int vfd = libev.vfd_open(fd)
#             libev.vfd_free(self._watcher.fd)
#             libev.ev_io_init(&self._watcher, <void *>gevent_callback_io, vfd, self._watcher.events)
#
#     property events:
#
#         def __get__(self):
#             return self._watcher.events
#
#         def __set__(self, int events):
#             if libev.ev_is_active(&self._watcher):
#                 raise AttributeError("'io' watcher attribute 'events' is read-only while watcher is active")
#             libev.ev_io_init(&self._watcher, <void *>gevent_callback_io, self._watcher.fd, events)
#
#     property events_str:
#
#         def __get__(self):
#             return _events_to_str(self._watcher.events)
#
#     def _format(self):
#         return ' fd=%s events=%s' % (self.fd, self.events_str)
#
# #ifdef _WIN32
#
#     def __cinit__(self):
#         self._watcher.fd = -1;
#
#     def __dealloc__(self):
#         libev.vfd_free(self._watcher.fd)
#
# #endif

class TimerWatcher(BaseWatcher):
    type = "timer"

    def start(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self._libev_unref()
        if kwargs.get('update'):
            libev.ev_now_update(self.loop._ptr)
        libev.ev_timer_start(self.loop._ptr, pointer(self._watcher_struct))
        #self._python_incref()

    def __init__(self, loop, after=0.0, repeat=0.0, ref=True):
        if repeat < 0.0:
            raise ValueError("repeat must be positive or zero: %r" % repeat)
        super(TimerWatcher, self).__init__(loop, ref, after, repeat)

    @property
    def at(self):
        return self._watcher.at

    # QQQ: add 'after' and 'repeat' properties?

    def again(self, callback, update=True, *args):
        self.callback = callback
        self.args = args
        self._libev_unref()
        if update:
            libev.ev_now_update(self.loop._ptr)
        libev.ev_timer_again(self.loop._ptr, pointer(self._watcher_struct))
        #self._python_incref()


class SignalWatcher(BaseWatcher):
    type = "signal"

    def __init__(self, loop, signalnum, ref=True):
        if signalnum < 1 or signalnum >= NSIG:
            raise ValueError('illegal signal number: %r' % signalnum)
        # still possible to crash on one of libev's asserts:
        # 1) "libev: ev_signal_start called with illegal signal number"
        #    EV_NSIG might be different from signal.NSIG on some platforms
        # 2) "libev: a signal must not be attached to two different loops"
        #    we probably could check that in LIBEV_EMBED mode, but not in general
        super(SignalWatcher, self).__init__(loop, ref, signalnum)

class IdleWatcher(BaseWatcher):
    type = "idle"

class PrepareWatcher(BaseWatcher):
    type = "prepare"

class ForkWatcher(BaseWatcher):
    type = "fork"

class AsyncWatcher(BaseWatcher):
    type = "async"

    @property
    def pending(self):
        return True if libev.ev_async_pending(pointer(self._watcher_struct)) else False

    def send(self):
        libev.ev_async_send(self.loop._ptr, pointer(self._watcher_struct))

#cdef public class child(watcher) [object PyGeventChildObject, type PyGeventChild_Type]:
#
#    WATCHER(child)
#
#    INIT(child, ``, int pid, bint trace=0'', ``, pid, trace'')

class CallbackWatcher(BaseWatcher):
    type = "prepare"

    def start(self, callback, *args):
        self.callback = callback
        self.args = args
        libev.ev_feed_event(self.loop._ptr, pointer(self._watcher_struct), libev.EV_CUSTOM)
        #self._python_incref()

    @property
    def active(self):
        return self.callback is not None


__SYSERR_CALLBACK = None

standard_c_lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))
standard_c_lib.__error.restype = ctypes.POINTER(ctypes.c_int)

def _syserr_cb(msg):
    try:
        errno = standard_c_lib._error().contents.value
        __SYSERR_CALLBACK(msg, errno)
    except:
        set_syserr_cb(None)
        raise

def _empty_syserr_cb(msg):
    """Making a NULL pointer for the optional callback does not seem to be possible with ctypes"""
    pass

syserr_cb = ctypes.CFUNCTYPE(None, libev.String)(_syserr_cb)
empty_syserr_cb = ctypes.CFUNCTYPE(None, libev.String)(_empty_syserr_cb)

def set_syserr_cb(callback):
    global __SYSERR_CALLBACK
    if callback is None:
        libev.ev_set_syserr_cb(empty_syserr_cb)
        __SYSERR_CALLBACK = None
    elif hasattr(callback, '__call__'):
        libev.ev_set_syserr_cb(syserr_cb)
        __SYSERR_CALLBACK = callback
    else:
        raise TypeError('Expected callable or None, got %r' % (callback, ))


def set_exc_info(type, value):
    if type is not None or value is not None:
        print "set_exc_info: ", type, value

def gevent_handle_error(loop, context):
    raise Exception("unimplemented")

def gevent_check_signals(loop):
    if sys.exc_info()[0] is not None:
        gevent_handle_error(loop, None)

def gevent_callback(watcher, revents):
    gevent_check_signals(watcher.loop)
    if watcher.args is not None and len(watcher.args) > 0 and watcher.args[0] == GEVENT_CORE_EVENTS:
        watcher.args[0] = revents

    from hub import getcurrent
    print "gevent_callback current greenlet:", "%s" % getcurrent()
    print "gevent_callback calling watcher: ", watcher, " with args:", watcher.args
    watcher._callback(*watcher.args)
    print "watcher callback complete"

    if not libev.ev_is_active(pointer(watcher._watcher_struct)):
        watcher.stop()

def _gevent_signal_check(loop_struct_pointer, watcher_struct_pointer, revents):
    loop = Loop.lookup_instance(loop_struct_pointer)
    gevent_check_signals(loop)
gevent_signal_check = libev.wrap_callback("prepare", _gevent_signal_check)

def gevent_periodic_signal_check(loop, watcher, revents):
    raise Exception("unimplemented")

# TODO: circular ref to watcher? watcher has callback that points to watcher - use lookup function - use cls of watcher watcher.__class__
def create_watcher_callback(watcher):
    # get reference to the class so we can use it to look up this
    # specific watcher without using a reference to the watcher
    watcher_class = watcher.__class__
    def watcher_callback(loop_struct_pointer, watcher_struct_pointer, revents):
        print "watcher_callback"
        w = watcher_class.lookup_instance(watcher_struct_pointer.contents)
        gevent_callback(w, revents)
        print "end watcher_callback"

    return libev.wrap_callback(watcher.type, watcher_callback)
