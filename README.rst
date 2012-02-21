gevent-pypy-experimental
=======

Experimental port of gevent_ 1.0b to run on PyPy_.  Don't use this for anything serious.

PyPy does not easily support C extension modules, so this is just gevent with all the C extension parts replaced with ctypes_ wrappers.

While basic functionality should be there, error handling in this port is untested and for sure broken.  Also, an installed copy of libev_ is required (normal gevent compiles libev itself).  Even with PyPy's JIT, the calls of the ctypes overhead will hurt performance vs gevent with the normal C extension module.

On my Mac system, I needed to specify the LD_LIBRARY_PATH to run this with PyPy (I have libev installed through macports_)::

    LD_LIBRARY_PATH="/opt/local/lib" pypy whatever.py

How to Install
--------------
PyPy can't use the default installer, so just copy the "gevent" folder to your PyPy site-packages.  Since it's all Python and uses your own libev installation, there is really no need to build anything.

Limitations
-----------
* Crashes sometimes unless you turn off the JIT (pypy --jit off), possibly a bug in the JIT.  Seems stable besides that.
* Way slower than normal python+normal gevent
* Exception/error handling incomplete
* Win32 is completely not supported
* gevent tests a long way from running successfully

.. _gevent: http://www.gevent.org
.. _libev: http://software.schmorp.de/pkg/libev.html
.. _ctypes: http://docs.python.org/library/ctypes.html
.. _PyPy: http://pypy.org/
.. _macports: http://www.macports.org/
