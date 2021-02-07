.. _cpp:

The C++ interface
=================

O\ :sub:`2`\ sclpy includes several classes and functions which are
wrappers around the original O\ :sub:`2`\ scl classes and functions.
The full documentation of these classes and functions is not
reproduced here, but a link to the O\ :sub:`2`\ scl documentation is
provided. Note also that not all O\ :sub:`2`\ scl functions are
wrapped. In those O\ :sub:`2`\ scl classes which are wrapped in O\
:sub:`2`\ sclpy, not all of their methods or data members are
accessible in O\ :sub:`2`\ sclpy. If there is O\ :sub:`2`\ scl which
is missing and you would like me to include, let me know.

One :class:`o2sclpy.linker` object should be created and then that object
should be used to link the O\ :sub:`2`\ scl libraries with
the :meth:`o2sclpy.linker.link_o2scl_o2graph()` function. Then, all
O\ :sub:`2`\ scl-based classes can be instantiated with
the :class:`o2sclpy.linker` object. The ``pointer`` argument is optional
and only needed if one is performing a shallow copy of an
O\ :sub:`2`\ scl-based class.

Throwing C++ exceptions across DLL boundaries is difficult, so O\
:sub:`2`\ sclpy ensures that O\ :sub:`2`\ scl uses an alternate error
handler which calls ``exit()`` when an error occurs. As a result, O\
:sub:`2`\ sclpy does not support any interaction between Python and
C++ exceptions.

