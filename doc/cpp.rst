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

One :class:`o2sclpy.linker` object should be created and then that
object should be used to link the O\ :sub:`2`\ scl libraries with the
:meth:`o2sclpy.linker.link_o2scl()` function. Then, all O\
:sub:`2`\ scl-based classes can be instantiated with the
:class:`o2sclpy.linker` object. In the ``__init__`` methods of python
wrappers of O\ :sub:`2`\ scl classes, the ``pointer`` argument is
optional and only needed if one is performing a shallow copy of an O\
:sub:`2`\ scl-based class.

Generally, O\ :sub:`2`\ sclpy should take care of the memory
management for you. If they have ownership over their pointer,
then their ``_owner`` data is ``True``, and their ``__del__``
method will call the C++ function necessary to free the memory
associated with the underlying
object. O\ :sub:`2`\ sclpy contains wrappers to some
``std::shared_ptr`` objects, and these objects may not be
destructed until the Python garbage collector deletes the last
O\ :sub:`2`\ sclpy class which owns a copy of the ``shared_ptr``.

Throwing C++ exceptions across DLL boundaries is not supported in
O\ :sub:`2`\ scl, so O\ :sub:`2`\ sclpy ensures that O\ :sub:`2`\ scl
uses an alternate error handler which calls ``exit()`` (i.e. from
``libc``) when an error occurs. O\ :sub:`2`\ sclpy does
not support any interaction between Python and C++ exceptions.

Finally, some O\ :sub:`2`\ scl classes output information to
``std::cout``, and in a Jupyter notebook this normally goes to the
Jupyter console. If you want this output to go to the Jupyter notebook
instead, you will need to use the :class:`o2sclpy.cap_cout` class.

