from _libev import *
import ctypes

WATCHER_TYPES = ['io', 'timer', 'periodic', 'signal', 'child', 'stat', 'idle', 'prepare', 'check', 'embed', 'fork', 'cleanup', 'async']

def ev_is_default_loop(loop):
    return ctypes.addressof(loop.contents) == ctypes.addressof(EV_DEFAULT.contents)

def ev_init(ev, cb):
    ev.active = 0
    ev.pending = 0
    ev.priority = 0
    ev.cb = cb

def ev_io_set(ev, fd, events):
    ev.fd = fd
    ev.events = events | EV__IOFDSET

def ev_timer_set(ev, after, repeat):
    ev.at = after
    ev.repeat = repeat

def ev_periodic_set(ev, ofs, ival, rcb):
    ev.offset = ofs
    ev.interval = ival
    ev.reschedule_cb = rcb

def ev_signal_set(ev, signum):
    ev.signum = signum

def ev_child_set(ev, pid, trace):
    ev.pid = pid
    if trace:
        ev.flags = 1
    else:
        ev.flags = 0

def ev_stat_set(ev, path, interval):
    ev.path = path
    ev.interval = interval
    ev.wd = -2

def ev_idle_set(ev):
    pass

def ev_prepare_set(ev):
    pass

def ev_check_set(ev):
    pass

def ev_embed_set(ev, other):
    ev.other = other

def ev_fork_set(ev):
    pass

def ev_cleanup_set(ev):
    pass

def ev_async_set(ev):
    pass

def ev_io_init(ev, cb, fd, events):
    ev_init(ev, cb)
    ev_io_set(ev, fd, events)

def ev_timer_init(ev, cb, after, repeat):
    ev_init(ev, cb)
    ev_timer_set(ev, after, repeat)

def ev_periodic_init(ev, cb, ofs, ival, rcb):
    ev_init(ev, cb)
    ev_periodic_set(ev, ofs, ival, rcb)

def ev_signal_init(ev, cb, signum):
    ev_init(ev, cb)
    ev_signal_set(ev, signum)

def ev_child_init(ev, cb, pid, trace):
    ev_init(ev, cb)
    ev_child_set(ev, pid, trace)

def ev_stat_init(ev, cb, path, interval):
    ev_init(ev, cb)
    ev_stat_set(ev, path, interval)

def ev_idle_init(ev, cb):
    ev_init(ev, cb)
    ev_idle_set(ev)

def ev_prepare_init(ev, cb):
    ev_init(ev, cb)
    ev_prepare_set(ev)

def ev_check_init(ev, cb):
    ev_init(ev, cb)
    ev_check_set(ev)

def ev_embed_init(ev, cb, other):
    ev_init(ev, cb)
    ev_embed_set(ev, other)

def ev_fork_init(ev, cb):
    ev_init(ev, cb)
    ev_fork_set(ev)

def ev_cleanup_init(ev, cb):
    ev_init(ev, cb)
    ev_cleanup_set(ev)

def ev_async_init(ev, cb):
    ev_init(ev, cb)
    ev_async_set(ev)

# redefine from _libev because the automatic translation did not quite work
def ev_is_pending(ev):
    return ev.contents.pending

def ev_is_active(ev):
    return ev.contents.active

def wrap_callback(watcher_type, function):
    watcher_struct_type = globals()["ev_" + watcher_type]
    return ctypes.CFUNCTYPE(None, ctypes.POINTER(ev_loop), ctypes.POINTER(watcher_struct_type), ctypes.c_int)(function)