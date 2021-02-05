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

Throwing C++ exceptions across DLL boundaries is difficult, so
O\ :sub:`2`\ sclpy ensures that uses an alternate error handler
which calls ``exit()`` when an error occurs. As a result,
O\ :sub:`2`\ sclpy does not support any interaction between
Python and C++ exceptions.

