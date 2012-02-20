'''Wrapper for ev.h

Generated with:
ctypesgen/ctypesgen.py -lev libev/ev.h -o gevent/_libev.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["ev"] = load_library("ev")

# 1 libraries
# End libraries

# No modules

ev_tstamp = c_double # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 143

__int32_t = c_int # /usr/include/i386/_types.h: 44

__int64_t = c_longlong # /usr/include/i386/_types.h: 46

__darwin_time_t = c_long # /usr/include/i386/_types.h: 118

__darwin_blkcnt_t = __int64_t # /usr/include/sys/_types.h: 94

__darwin_blksize_t = __int32_t # /usr/include/sys/_types.h: 95

__darwin_dev_t = __int32_t # /usr/include/sys/_types.h: 96

__darwin_gid_t = c_uint32 # /usr/include/sys/_types.h: 99

__darwin_ino64_t = c_uint64 # /usr/include/sys/_types.h: 101

__darwin_mode_t = c_uint16 # /usr/include/sys/_types.h: 109

__darwin_off_t = __int64_t # /usr/include/sys/_types.h: 110

__darwin_uid_t = c_uint32 # /usr/include/sys/_types.h: 133

sig_atomic_t = c_int # /usr/include/i386/signal.h: 39

uid_t = __darwin_uid_t # /usr/include/sys/signal.h: 172

# /usr/include/sys/_structs.h: 88
class struct_timespec(Structure):
    pass

struct_timespec.__slots__ = [
    'tv_sec',
    'tv_nsec',
]
struct_timespec._fields_ = [
    ('tv_sec', __darwin_time_t),
    ('tv_nsec', c_long),
]

blkcnt_t = __darwin_blkcnt_t # /usr/include/sys/stat.h: 87

blksize_t = __darwin_blksize_t # /usr/include/sys/stat.h: 92

dev_t = __darwin_dev_t # /usr/include/sys/stat.h: 97

mode_t = __darwin_mode_t # /usr/include/sys/stat.h: 114

nlink_t = c_uint16 # /usr/include/sys/stat.h: 119

gid_t = __darwin_gid_t # /usr/include/sys/stat.h: 129

off_t = __darwin_off_t # /usr/include/sys/stat.h: 134

# /usr/include/sys/stat.h: 225
class struct_stat(Structure):
    pass

struct_stat.__slots__ = [
    'st_dev',
    'st_mode',
    'st_nlink',
    'st_ino',
    'st_uid',
    'st_gid',
    'st_rdev',
    'st_atimespec',
    'st_mtimespec',
    'st_ctimespec',
    'st_birthtimespec',
    'st_size',
    'st_blocks',
    'st_blksize',
    'st_flags',
    'st_gen',
    'st_lspare',
    'st_qspare',
]
struct_stat._fields_ = [
    ('st_dev', dev_t),
    ('st_mode', mode_t),
    ('st_nlink', nlink_t),
    ('st_ino', __darwin_ino64_t),
    ('st_uid', uid_t),
    ('st_gid', gid_t),
    ('st_rdev', dev_t),
    ('st_atimespec', struct_timespec),
    ('st_mtimespec', struct_timespec),
    ('st_ctimespec', struct_timespec),
    ('st_birthtimespec', struct_timespec),
    ('st_size', off_t),
    ('st_blocks', blkcnt_t),
    ('st_blksize', blksize_t),
    ('st_flags', c_uint32),
    ('st_gen', c_uint32),
    ('st_lspare', __int32_t),
    ('st_qspare', __int64_t * 2),
]

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 160
class struct_ev_loop(Structure):
    pass

enum_anon_2 = c_int # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_UNDEF = 4294967295 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_NONE = 0 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_READ = 1 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_WRITE = 2 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV__IOFDSET = 128 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_IO = EV_READ # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_TIMER = 256 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_TIMEOUT = EV_TIMER # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_PERIODIC = 512 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_SIGNAL = 1024 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_CHILD = 2048 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_STAT = 4096 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_IDLE = 8192 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_PREPARE = 16384 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_CHECK = 32768 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_EMBED = 65536 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_FORK = 131072 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_CLEANUP = 262144 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_ASYNC = 524288 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_CUSTOM = 16777216 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

EV_ERROR = 2147483648 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 199

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 280
class struct_ev_watcher(Structure):
    pass

struct_ev_watcher.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
]
struct_ev_watcher._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_watcher), c_int)),
]

ev_watcher = struct_ev_watcher # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 283

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 286
class struct_ev_watcher_list(Structure):
    pass

struct_ev_watcher_list.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'next',
]
struct_ev_watcher_list._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_watcher_list), c_int)),
    ('next', POINTER(struct_ev_watcher_list)),
]

ev_watcher_list = struct_ev_watcher_list # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 289

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 292
class struct_ev_watcher_time(Structure):
    pass

struct_ev_watcher_time.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'at',
]
struct_ev_watcher_time._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_watcher_time), c_int)),
    ('at', ev_tstamp),
]

ev_watcher_time = struct_ev_watcher_time # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 295

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 299
class struct_ev_io(Structure):
    pass

struct_ev_io.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'next',
    'fd',
    'events',
]
struct_ev_io._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_io), c_int)),
    ('next', POINTER(struct_ev_watcher_list)),
    ('fd', c_int),
    ('events', c_int),
]

ev_io = struct_ev_io # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 305

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 309
class struct_ev_timer(Structure):
    pass

struct_ev_timer.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'at',
    'repeat',
]
struct_ev_timer._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_timer), c_int)),
    ('at', ev_tstamp),
    ('repeat', ev_tstamp),
]

ev_timer = struct_ev_timer # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 314

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 318
class struct_ev_periodic(Structure):
    pass

struct_ev_periodic.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'at',
    'offset',
    'interval',
    'reschedule_cb',
]
struct_ev_periodic._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_periodic), c_int)),
    ('at', ev_tstamp),
    ('offset', ev_tstamp),
    ('interval', ev_tstamp),
    ('reschedule_cb', CFUNCTYPE(UNCHECKED(ev_tstamp), POINTER(struct_ev_periodic), ev_tstamp)),
]

ev_periodic = struct_ev_periodic # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 325

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 329
class struct_ev_signal(Structure):
    pass

struct_ev_signal.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'next',
    'signum',
]
struct_ev_signal._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_signal), c_int)),
    ('next', POINTER(struct_ev_watcher_list)),
    ('signum', c_int),
]

ev_signal = struct_ev_signal # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 334

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 339
class struct_ev_child(Structure):
    pass

struct_ev_child.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'next',
    'flags',
    'pid',
    'rpid',
    'rstatus',
]
struct_ev_child._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_child), c_int)),
    ('next', POINTER(struct_ev_watcher_list)),
    ('flags', c_int),
    ('pid', c_int),
    ('rpid', c_int),
    ('rstatus', c_int),
]

ev_child = struct_ev_child # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 347

ev_statdata = struct_stat # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 354

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 359
class struct_ev_stat(Structure):
    pass

struct_ev_stat.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'next',
    'timer',
    'interval',
    'path',
    'prev',
    'attr',
    'wd',
]
struct_ev_stat._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_stat), c_int)),
    ('next', POINTER(struct_ev_watcher_list)),
    ('timer', ev_timer),
    ('interval', ev_tstamp),
    ('path', String),
    ('prev', ev_statdata),
    ('attr', ev_statdata),
    ('wd', c_int),
]

ev_stat = struct_ev_stat # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 370

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 376
class struct_ev_idle(Structure):
    pass

struct_ev_idle.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
]
struct_ev_idle._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_idle), c_int)),
]

ev_idle = struct_ev_idle # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 379

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 385
class struct_ev_prepare(Structure):
    pass

struct_ev_prepare.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
]
struct_ev_prepare._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_prepare), c_int)),
]

ev_prepare = struct_ev_prepare # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 388

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 392
class struct_ev_check(Structure):
    pass

struct_ev_check.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
]
struct_ev_check._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_check), c_int)),
]

ev_check = struct_ev_check # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 395

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 400
class struct_ev_fork(Structure):
    pass

struct_ev_fork.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
]
struct_ev_fork._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_fork), c_int)),
]

ev_fork = struct_ev_fork # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 403

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 409
class struct_ev_cleanup(Structure):
    pass

struct_ev_cleanup.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
]
struct_ev_cleanup._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_cleanup), c_int)),
]

ev_cleanup = struct_ev_cleanup # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 412

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 418
class struct_ev_embed(Structure):
    pass

struct_ev_embed.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'other',
    'io',
    'prepare',
    'check',
    'timer',
    'periodic',
    'idle',
    'fork',
    'cleanup',
]
struct_ev_embed._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_embed), c_int)),
    ('other', POINTER(struct_ev_loop)),
    ('io', ev_io),
    ('prepare', ev_prepare),
    ('check', ev_check),
    ('timer', ev_timer),
    ('periodic', ev_periodic),
    ('idle', ev_idle),
    ('fork', ev_fork),
    ('cleanup', ev_cleanup),
]

ev_embed = struct_ev_embed # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 433

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 439
class struct_ev_async(Structure):
    pass

struct_ev_async.__slots__ = [
    'active',
    'pending',
    'priority',
    'data',
    'cb',
    'sent',
]
struct_ev_async._fields_ = [
    ('active', c_int),
    ('pending', c_int),
    ('priority', c_int),
    ('data', POINTER(None)),
    ('cb', CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop), POINTER(struct_ev_async), c_int)),
    ('sent', sig_atomic_t),
]

ev_async = struct_ev_async # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 444

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 450
class union_ev_any_watcher(Union):
    pass

union_ev_any_watcher.__slots__ = [
    'w',
    'wl',
    'io',
    'timer',
    'periodic',
    'signal',
    'child',
    'stat',
    'idle',
    'prepare',
    'check',
    'fork',
    'cleanup',
    'embed',
    'async',
]
union_ev_any_watcher._fields_ = [
    ('w', struct_ev_watcher),
    ('wl', struct_ev_watcher_list),
    ('io', struct_ev_io),
    ('timer', struct_ev_timer),
    ('periodic', struct_ev_periodic),
    ('signal', struct_ev_signal),
    ('child', struct_ev_child),
    ('stat', struct_ev_stat),
    ('idle', struct_ev_idle),
    ('prepare', struct_ev_prepare),
    ('check', struct_ev_check),
    ('fork', struct_ev_fork),
    ('cleanup', struct_ev_cleanup),
    ('embed', struct_ev_embed),
    ('async', struct_ev_async),
]

enum_anon_3 = c_int # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

EVFLAG_AUTO = 0 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

EVFLAG_NOENV = 16777216 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

EVFLAG_FORKCHECK = 33554432 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

EVFLAG_NOINOTIFY = 1048576 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

EVFLAG_NOSIGFD = 0 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

EVFLAG_SIGNALFD = 2097152 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

EVFLAG_NOSIGMASK = 4194304 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 483

enum_anon_4 = c_int # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_SELECT = 1 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_POLL = 2 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_EPOLL = 4 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_KQUEUE = 8 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_DEVPOLL = 16 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_PORT = 32 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_ALL = 63 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

EVBACKEND_MASK = 65535 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 499

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 511
if hasattr(_libs['ev'], 'ev_version_major'):
    ev_version_major = _libs['ev'].ev_version_major
    ev_version_major.argtypes = []
    ev_version_major.restype = c_int

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 512
if hasattr(_libs['ev'], 'ev_version_minor'):
    ev_version_minor = _libs['ev'].ev_version_minor
    ev_version_minor.argtypes = []
    ev_version_minor.restype = c_int

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 514
if hasattr(_libs['ev'], 'ev_supported_backends'):
    ev_supported_backends = _libs['ev'].ev_supported_backends
    ev_supported_backends.argtypes = []
    ev_supported_backends.restype = c_uint

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 515
if hasattr(_libs['ev'], 'ev_recommended_backends'):
    ev_recommended_backends = _libs['ev'].ev_recommended_backends
    ev_recommended_backends.argtypes = []
    ev_recommended_backends.restype = c_uint

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 516
if hasattr(_libs['ev'], 'ev_embeddable_backends'):
    ev_embeddable_backends = _libs['ev'].ev_embeddable_backends
    ev_embeddable_backends.argtypes = []
    ev_embeddable_backends.restype = c_uint

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 518
if hasattr(_libs['ev'], 'ev_time'):
    ev_time = _libs['ev'].ev_time
    ev_time.argtypes = []
    ev_time.restype = ev_tstamp

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 519
if hasattr(_libs['ev'], 'ev_sleep'):
    ev_sleep = _libs['ev'].ev_sleep
    ev_sleep.argtypes = [ev_tstamp]
    ev_sleep.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 527
if hasattr(_libs['ev'], 'ev_set_allocator'):
    ev_set_allocator = _libs['ev'].ev_set_allocator
    ev_set_allocator.argtypes = [CFUNCTYPE(UNCHECKED(POINTER(None)), POINTER(None), c_long)]
    ev_set_allocator.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 533
if hasattr(_libs['ev'], 'ev_set_syserr_cb'):
    ev_set_syserr_cb = _libs['ev'].ev_set_syserr_cb
    ev_set_syserr_cb.argtypes = [CFUNCTYPE(UNCHECKED(None), String)]
    ev_set_syserr_cb.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 539
if hasattr(_libs['ev'], 'ev_default_loop'):
    ev_default_loop = _libs['ev'].ev_default_loop
    ev_default_loop.argtypes = [c_uint]
    ev_default_loop.restype = POINTER(struct_ev_loop)

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 544
try:
    ev_default_loop_ptr = (POINTER(struct_ev_loop)).in_dll(_libs['ev'], 'ev_default_loop_ptr')
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 556
if hasattr(_libs['ev'], 'ev_loop_new'):
    ev_loop_new = _libs['ev'].ev_loop_new
    ev_loop_new.argtypes = [c_uint]
    ev_loop_new.restype = POINTER(struct_ev_loop)

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 558
if hasattr(_libs['ev'], 'ev_now'):
    ev_now = _libs['ev'].ev_now
    ev_now.argtypes = [POINTER(struct_ev_loop)]
    ev_now.restype = ev_tstamp

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 582
if hasattr(_libs['ev'], 'ev_loop_destroy'):
    ev_loop_destroy = _libs['ev'].ev_loop_destroy
    ev_loop_destroy.argtypes = [POINTER(struct_ev_loop)]
    ev_loop_destroy.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 588
if hasattr(_libs['ev'], 'ev_loop_fork'):
    ev_loop_fork = _libs['ev'].ev_loop_fork
    ev_loop_fork.argtypes = [POINTER(struct_ev_loop)]
    ev_loop_fork.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 590
if hasattr(_libs['ev'], 'ev_backend'):
    ev_backend = _libs['ev'].ev_backend
    ev_backend.argtypes = [POINTER(struct_ev_loop)]
    ev_backend.restype = c_uint

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 592
if hasattr(_libs['ev'], 'ev_now_update'):
    ev_now_update = _libs['ev'].ev_now_update
    ev_now_update.argtypes = [POINTER(struct_ev_loop)]
    ev_now_update.restype = None

enum_anon_5 = c_int # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 604

EVRUN_NOWAIT = 1 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 604

EVRUN_ONCE = 2 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 604

enum_anon_6 = c_int # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 610

EVBREAK_CANCEL = 0 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 610

EVBREAK_ONE = 1 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 610

EVBREAK_ALL = 2 # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 610

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 617
if hasattr(_libs['ev'], 'ev_run'):
    ev_run = _libs['ev'].ev_run
    ev_run.argtypes = [POINTER(struct_ev_loop), c_int]
    ev_run.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 618
if hasattr(_libs['ev'], 'ev_break'):
    ev_break = _libs['ev'].ev_break
    ev_break.argtypes = [POINTER(struct_ev_loop), c_int]
    ev_break.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 625
if hasattr(_libs['ev'], 'ev_ref'):
    ev_ref = _libs['ev'].ev_ref
    ev_ref.argtypes = [POINTER(struct_ev_loop)]
    ev_ref.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 626
if hasattr(_libs['ev'], 'ev_unref'):
    ev_unref = _libs['ev'].ev_unref
    ev_unref.argtypes = [POINTER(struct_ev_loop)]
    ev_unref.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 632
if hasattr(_libs['ev'], 'ev_once'):
    ev_once = _libs['ev'].ev_once
    ev_once.argtypes = [POINTER(struct_ev_loop), c_int, c_int, ev_tstamp, CFUNCTYPE(UNCHECKED(None), c_int, POINTER(None)), POINTER(None)]
    ev_once.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 635
if hasattr(_libs['ev'], 'ev_iteration'):
    ev_iteration = _libs['ev'].ev_iteration
    ev_iteration.argtypes = [POINTER(struct_ev_loop)]
    ev_iteration.restype = c_uint

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 636
if hasattr(_libs['ev'], 'ev_depth'):
    ev_depth = _libs['ev'].ev_depth
    ev_depth.argtypes = [POINTER(struct_ev_loop)]
    ev_depth.restype = c_uint

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 637
if hasattr(_libs['ev'], 'ev_verify'):
    ev_verify = _libs['ev'].ev_verify
    ev_verify.argtypes = [POINTER(struct_ev_loop)]
    ev_verify.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 639
if hasattr(_libs['ev'], 'ev_set_io_collect_interval'):
    ev_set_io_collect_interval = _libs['ev'].ev_set_io_collect_interval
    ev_set_io_collect_interval.argtypes = [POINTER(struct_ev_loop), ev_tstamp]
    ev_set_io_collect_interval.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 640
if hasattr(_libs['ev'], 'ev_set_timeout_collect_interval'):
    ev_set_timeout_collect_interval = _libs['ev'].ev_set_timeout_collect_interval
    ev_set_timeout_collect_interval.argtypes = [POINTER(struct_ev_loop), ev_tstamp]
    ev_set_timeout_collect_interval.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 643
if hasattr(_libs['ev'], 'ev_set_userdata'):
    ev_set_userdata = _libs['ev'].ev_set_userdata
    ev_set_userdata.argtypes = [POINTER(struct_ev_loop), POINTER(None)]
    ev_set_userdata.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 644
if hasattr(_libs['ev'], 'ev_userdata'):
    ev_userdata = _libs['ev'].ev_userdata
    ev_userdata.argtypes = [POINTER(struct_ev_loop)]
    ev_userdata.restype = POINTER(None)

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 645
if hasattr(_libs['ev'], 'ev_set_invoke_pending_cb'):
    ev_set_invoke_pending_cb = _libs['ev'].ev_set_invoke_pending_cb
    ev_set_invoke_pending_cb.argtypes = [POINTER(struct_ev_loop), CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop))]
    ev_set_invoke_pending_cb.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 646
if hasattr(_libs['ev'], 'ev_set_loop_release_cb'):
    ev_set_loop_release_cb = _libs['ev'].ev_set_loop_release_cb
    ev_set_loop_release_cb.argtypes = [POINTER(struct_ev_loop), CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop)), CFUNCTYPE(UNCHECKED(None), POINTER(struct_ev_loop))]
    ev_set_loop_release_cb.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 648
if hasattr(_libs['ev'], 'ev_pending_count'):
    ev_pending_count = _libs['ev'].ev_pending_count
    ev_pending_count.argtypes = [POINTER(struct_ev_loop)]
    ev_pending_count.restype = c_uint

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 649
if hasattr(_libs['ev'], 'ev_invoke_pending'):
    ev_invoke_pending = _libs['ev'].ev_invoke_pending
    ev_invoke_pending.argtypes = [POINTER(struct_ev_loop)]
    ev_invoke_pending.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 654
if hasattr(_libs['ev'], 'ev_suspend'):
    ev_suspend = _libs['ev'].ev_suspend
    ev_suspend.argtypes = [POINTER(struct_ev_loop)]
    ev_suspend.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 655
if hasattr(_libs['ev'], 'ev_resume'):
    ev_resume = _libs['ev'].ev_resume
    ev_resume.argtypes = [POINTER(struct_ev_loop)]
    ev_resume.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 722
if hasattr(_libs['ev'], 'ev_feed_event'):
    ev_feed_event = _libs['ev'].ev_feed_event
    ev_feed_event.argtypes = [POINTER(struct_ev_loop), POINTER(None), c_int]
    ev_feed_event.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 723
if hasattr(_libs['ev'], 'ev_feed_fd_event'):
    ev_feed_fd_event = _libs['ev'].ev_feed_fd_event
    ev_feed_fd_event.argtypes = [POINTER(struct_ev_loop), c_int, c_int]
    ev_feed_fd_event.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 725
if hasattr(_libs['ev'], 'ev_feed_signal'):
    ev_feed_signal = _libs['ev'].ev_feed_signal
    ev_feed_signal.argtypes = [c_int]
    ev_feed_signal.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 726
if hasattr(_libs['ev'], 'ev_feed_signal_event'):
    ev_feed_signal_event = _libs['ev'].ev_feed_signal_event
    ev_feed_signal_event.argtypes = [POINTER(struct_ev_loop), c_int]
    ev_feed_signal_event.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 728
if hasattr(_libs['ev'], 'ev_invoke'):
    ev_invoke = _libs['ev'].ev_invoke
    ev_invoke.argtypes = [POINTER(struct_ev_loop), POINTER(None), c_int]
    ev_invoke.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 729
if hasattr(_libs['ev'], 'ev_clear_pending'):
    ev_clear_pending = _libs['ev'].ev_clear_pending
    ev_clear_pending.argtypes = [POINTER(struct_ev_loop), POINTER(None)]
    ev_clear_pending.restype = c_int

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 731
if hasattr(_libs['ev'], 'ev_io_start'):
    ev_io_start = _libs['ev'].ev_io_start
    ev_io_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_io)]
    ev_io_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 732
if hasattr(_libs['ev'], 'ev_io_stop'):
    ev_io_stop = _libs['ev'].ev_io_stop
    ev_io_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_io)]
    ev_io_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 734
if hasattr(_libs['ev'], 'ev_timer_start'):
    ev_timer_start = _libs['ev'].ev_timer_start
    ev_timer_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_timer)]
    ev_timer_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 735
if hasattr(_libs['ev'], 'ev_timer_stop'):
    ev_timer_stop = _libs['ev'].ev_timer_stop
    ev_timer_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_timer)]
    ev_timer_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 737
if hasattr(_libs['ev'], 'ev_timer_again'):
    ev_timer_again = _libs['ev'].ev_timer_again
    ev_timer_again.argtypes = [POINTER(struct_ev_loop), POINTER(ev_timer)]
    ev_timer_again.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 739
if hasattr(_libs['ev'], 'ev_timer_remaining'):
    ev_timer_remaining = _libs['ev'].ev_timer_remaining
    ev_timer_remaining.argtypes = [POINTER(struct_ev_loop), POINTER(ev_timer)]
    ev_timer_remaining.restype = ev_tstamp

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 742
if hasattr(_libs['ev'], 'ev_periodic_start'):
    ev_periodic_start = _libs['ev'].ev_periodic_start
    ev_periodic_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_periodic)]
    ev_periodic_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 743
if hasattr(_libs['ev'], 'ev_periodic_stop'):
    ev_periodic_stop = _libs['ev'].ev_periodic_stop
    ev_periodic_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_periodic)]
    ev_periodic_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 744
if hasattr(_libs['ev'], 'ev_periodic_again'):
    ev_periodic_again = _libs['ev'].ev_periodic_again
    ev_periodic_again.argtypes = [POINTER(struct_ev_loop), POINTER(ev_periodic)]
    ev_periodic_again.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 749
if hasattr(_libs['ev'], 'ev_signal_start'):
    ev_signal_start = _libs['ev'].ev_signal_start
    ev_signal_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_signal)]
    ev_signal_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 750
if hasattr(_libs['ev'], 'ev_signal_stop'):
    ev_signal_stop = _libs['ev'].ev_signal_stop
    ev_signal_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_signal)]
    ev_signal_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 755
if hasattr(_libs['ev'], 'ev_child_start'):
    ev_child_start = _libs['ev'].ev_child_start
    ev_child_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_child)]
    ev_child_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 756
if hasattr(_libs['ev'], 'ev_child_stop'):
    ev_child_stop = _libs['ev'].ev_child_stop
    ev_child_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_child)]
    ev_child_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 760
if hasattr(_libs['ev'], 'ev_stat_start'):
    ev_stat_start = _libs['ev'].ev_stat_start
    ev_stat_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_stat)]
    ev_stat_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 761
if hasattr(_libs['ev'], 'ev_stat_stop'):
    ev_stat_stop = _libs['ev'].ev_stat_stop
    ev_stat_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_stat)]
    ev_stat_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 762
if hasattr(_libs['ev'], 'ev_stat_stat'):
    ev_stat_stat = _libs['ev'].ev_stat_stat
    ev_stat_stat.argtypes = [POINTER(struct_ev_loop), POINTER(ev_stat)]
    ev_stat_stat.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 766
if hasattr(_libs['ev'], 'ev_idle_start'):
    ev_idle_start = _libs['ev'].ev_idle_start
    ev_idle_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_idle)]
    ev_idle_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 767
if hasattr(_libs['ev'], 'ev_idle_stop'):
    ev_idle_stop = _libs['ev'].ev_idle_stop
    ev_idle_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_idle)]
    ev_idle_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 771
if hasattr(_libs['ev'], 'ev_prepare_start'):
    ev_prepare_start = _libs['ev'].ev_prepare_start
    ev_prepare_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_prepare)]
    ev_prepare_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 772
if hasattr(_libs['ev'], 'ev_prepare_stop'):
    ev_prepare_stop = _libs['ev'].ev_prepare_stop
    ev_prepare_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_prepare)]
    ev_prepare_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 776
if hasattr(_libs['ev'], 'ev_check_start'):
    ev_check_start = _libs['ev'].ev_check_start
    ev_check_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_check)]
    ev_check_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 777
if hasattr(_libs['ev'], 'ev_check_stop'):
    ev_check_stop = _libs['ev'].ev_check_stop
    ev_check_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_check)]
    ev_check_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 781
if hasattr(_libs['ev'], 'ev_fork_start'):
    ev_fork_start = _libs['ev'].ev_fork_start
    ev_fork_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_fork)]
    ev_fork_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 782
if hasattr(_libs['ev'], 'ev_fork_stop'):
    ev_fork_stop = _libs['ev'].ev_fork_stop
    ev_fork_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_fork)]
    ev_fork_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 786
if hasattr(_libs['ev'], 'ev_cleanup_start'):
    ev_cleanup_start = _libs['ev'].ev_cleanup_start
    ev_cleanup_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_cleanup)]
    ev_cleanup_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 787
if hasattr(_libs['ev'], 'ev_cleanup_stop'):
    ev_cleanup_stop = _libs['ev'].ev_cleanup_stop
    ev_cleanup_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_cleanup)]
    ev_cleanup_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 792
if hasattr(_libs['ev'], 'ev_embed_start'):
    ev_embed_start = _libs['ev'].ev_embed_start
    ev_embed_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_embed)]
    ev_embed_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 793
if hasattr(_libs['ev'], 'ev_embed_stop'):
    ev_embed_stop = _libs['ev'].ev_embed_stop
    ev_embed_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_embed)]
    ev_embed_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 794
if hasattr(_libs['ev'], 'ev_embed_sweep'):
    ev_embed_sweep = _libs['ev'].ev_embed_sweep
    ev_embed_sweep.argtypes = [POINTER(struct_ev_loop), POINTER(ev_embed)]
    ev_embed_sweep.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 798
if hasattr(_libs['ev'], 'ev_async_start'):
    ev_async_start = _libs['ev'].ev_async_start
    ev_async_start.argtypes = [POINTER(struct_ev_loop), POINTER(ev_async)]
    ev_async_start.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 799
if hasattr(_libs['ev'], 'ev_async_stop'):
    ev_async_stop = _libs['ev'].ev_async_stop
    ev_async_stop.argtypes = [POINTER(struct_ev_loop), POINTER(ev_async)]
    ev_async_stop.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 800
if hasattr(_libs['ev'], 'ev_async_send'):
    ev_async_send = _libs['ev'].ev_async_send
    ev_async_send.argtypes = [POINTER(struct_ev_loop), POINTER(ev_async)]
    ev_async_send.restype = None

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 55
try:
    EV_COMPAT3 = 1
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 59
try:
    EV_FEATURES = 127
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 62
try:
    EV_FEATURE_CODE = (EV_FEATURES & 1)
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 63
try:
    EV_FEATURE_DATA = (EV_FEATURES & 2)
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 64
try:
    EV_FEATURE_CONFIG = (EV_FEATURES & 4)
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 65
try:
    EV_FEATURE_API = (EV_FEATURES & 8)
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 66
try:
    EV_FEATURE_WATCHERS = (EV_FEATURES & 16)
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 67
try:
    EV_FEATURE_BACKENDS = (EV_FEATURES & 32)
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 68
try:
    EV_FEATURE_OS = (EV_FEATURES & 64)
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 72
try:
    EV_MINPRI = EV_FEATURE_CONFIG and (-2) or 0
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 75
try:
    EV_MAXPRI = EV_FEATURE_CONFIG and 2 or 0
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 79
try:
    EV_MULTIPLICITY = EV_FEATURE_CONFIG
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 83
try:
    EV_PERIODIC_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 87
try:
    EV_STAT_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 91
try:
    EV_PREPARE_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 95
try:
    EV_CHECK_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 99
try:
    EV_IDLE_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 103
try:
    EV_FORK_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 107
try:
    EV_CLEANUP_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 111
try:
    EV_SIGNAL_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 118
try:
    EV_CHILD_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 123
try:
    EV_ASYNC_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 127
try:
    EV_EMBED_ENABLE = EV_FEATURE_WATCHERS
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 131
try:
    EV_WALK_ENABLE = 0
except:
    pass

EV_ATOMIC_T = sig_atomic_t # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 147

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 167
try:
    EV_DEFAULT = (ev_default_loop (0))
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 190
try:
    EV_PROTOTYPES = 1
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 195
try:
    EV_VERSION_MAJOR = 4
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 196
try:
    EV_VERSION_MINOR = 4
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 446
def ev_async_pending(w):
    return (w.contents.sent)

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 697
def ev_is_pending(ev):
    return (0 + ((ev.contents.pending).value))

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 698
def ev_is_active(ev):
    return (0 + ((ev.contents.active).value))

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 700
def ev_cb(ev):
    return (ev.contents.cb)

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 706
def ev_priority(ev):
    return (ev.contents.priority)

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 710
def ev_periodic_at(ev):
    return (ev.contents.at)

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 804
try:
    EVLOOP_NONBLOCK = EVRUN_NOWAIT
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 805
try:
    EVLOOP_ONESHOT = EVRUN_ONCE
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 806
try:
    EVUNLOOP_CANCEL = EVBREAK_CANCEL
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 807
try:
    EVUNLOOP_ONE = EVBREAK_ONE
except:
    pass

# /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 808
try:
    EVUNLOOP_ALL = EVBREAK_ALL
except:
    pass

ev_loop = struct_ev_loop # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 160

ev_watcher = struct_ev_watcher # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 280

ev_watcher_list = struct_ev_watcher_list # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 286

ev_watcher_time = struct_ev_watcher_time # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 292

ev_io = struct_ev_io # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 299

ev_timer = struct_ev_timer # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 309

ev_periodic = struct_ev_periodic # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 318

ev_signal = struct_ev_signal # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 329

ev_child = struct_ev_child # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 339

ev_stat = struct_ev_stat # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 359

ev_idle = struct_ev_idle # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 376

ev_prepare = struct_ev_prepare # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 385

ev_check = struct_ev_check # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 392

ev_fork = struct_ev_fork # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 400

ev_cleanup = struct_ev_cleanup # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 409

ev_embed = struct_ev_embed # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 418

ev_async = struct_ev_async # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 439

ev_any_watcher = union_ev_any_watcher # /Users/christopherhesse/Documents/Projects/gevent/gevent-pypy-experimental/libev/ev.h: 450

# No inserted files

