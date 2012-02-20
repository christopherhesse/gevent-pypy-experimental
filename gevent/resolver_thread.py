# Copyright (c) 2012 Denis Bilenko. See LICENSE for details.
import _socket
from gevent.hub import get_hub


__all__ = ['Resolver']


class Resolver(object):

    def __init__(self, hub=None):
        if hub is None:
            hub = get_hub()
        self.pool = hub.threadpool

    def close(self):
        pass

    # from briefly reading socketmodule.c, it seems that all of the functions
    # below are thread-safe in Python, even if they are not thread-safe in C.

    def gethostbyname(self, *args):
        return self.pool.apply(_socket.gethostbyname, args)

    def gethostbyname_ex(self, *args):
        return self.pool.apply(_socket.gethostbyname_ex, args)

    def getaddrinfo(self, *args, **kwargs):
        return self.pool.apply(_socket.getaddrinfo, args, kwargs)

    def gethostbyaddr(self, *args, **kwargs):
        return self.pool.apply(_socket.gethostbyaddr, args, kwargs)

    def getnameinfo(self, *args, **kwargs):
        return self.pool.apply(_socket.getnameinfo, args, kwargs)
