.. _cpp:

Using the C++ interface
=======================

:ref:`O2sclpy <o2sclpy>`

C++ interface contents
----------------------

- :ref:`C++ interface introduction`
- :ref:`Linking with O2scl <link2>`
- :ref:`Linking with O2scl example <linkexample>`
- :ref:`Class linker`

C++ interface introduction
--------------------------
     
O₂sclpy includes several classes and functions which are wrappers
around the original O₂scl classes and functions. The full
documentation of these classes and functions is not reproduced here,
but a link to the O₂scl documentation is provided. Note also that not
all O₂scl functions are wrapped. In those O₂scl classes which are
wrapped in O₂sclpy, not all of their methods or data members are
accessible in O₂sclpy. If there is O₂scl which is missing and you
would like me to include, let me know.

One :class:`o2sclpy.linker` object should be created and then that
object should be used to link the O₂scl libraries with the
:meth:`o2sclpy.linker.link_o2scl()` function. Then, all O₂scl-based
classes can be instantiated with the :class:`o2sclpy.linker` object.
In the ``__init__`` methods of python wrappers of O₂scl classes, the
``pointer`` argument is optional and only needed if one is performing
a shallow copy of an O₂scl-based class.

Generally, O₂sclpy should take care of the memory management for you.
If they have ownership over their pointer, then their ``_owner`` data
is ``True``, and their ``__del__`` method will call the C++ function
necessary to free the memory associated with the underlying object.
O₂sclpy contains wrappers to some ``std::shared_ptr`` objects, and
these objects may not be destructed until the Python garbage collector
deletes the last O₂sclpy class which owns a copy of the
``shared_ptr``.

Throwing C++ exceptions across DLL boundaries is not supported in
O₂scl, so O₂sclpy ensures that O₂scl uses an alternate error handler
which calls ``exit()`` (i.e. from ``libc``) when an error occurs.
O₂sclpy does not support any interaction between Python and C++
exceptions.

Finally, some O₂scl classes output information to ``std::cout``, and
in a Jupyter notebook this normally goes to the Jupyter console. If
you want this output to go to the Jupyter notebook instead, you will
need to use the :class:`o2sclpy.cap_cout` class.

.. _link2:

Linking with O₂scl
------------------

The :class:`o2sclpy.linker` class (see below) controls the dynamical
loading of the O₂scl libraries. This class may require some additional
information about your system in order to perform the dynamic loading
properly.

The variable :data:`o2sclpy.linker.o2scl_cpp_lib` specifies the C++
library to be loaded, in case it is not loaded automatically. The
function :func:`o2sclpy.linker.get_library_settings()` will set this to be
the value of the environment variable ``O2SCL_CPP_LIB``. You can also
specify the C++ library on the command-line when using the
:ref:`o2graph_script` using the ``o2scl-cpp-lib`` command. On a MacOS
laptop, when using ``clang`` the C++ library is typically found
automatically, but when using ``gcc`` I have to set this value to
``/usr/local/lib/gcc/11/libstdc++.dylib``.

The variable :data:`o2sclpy.linker.o2scl_lib_dir` specifies the
directory where ``libo2scl.so`` is to be found, in case it cannot be
found automatically. The function
:func:`o2sclpy.linker.get_library_settings()` will set this to be the
value of the environment variable ``O2SCL_LIB_DIR``. You can also
specify the C++ library on the command-line when using the
:ref:`o2graph_script` using the ``o2scl-lib-dir`` command.

Finally, the variable :data:`o2sclpy.linker.o2scl_addl_libs` is a list
of additional libraries which are required and not automatically
included by the dynamic loading. The function
:func:`o2sclpy.linker.get_library_settings()` will set this to be the
comma-separated list in the environment variable ``O2SCL_ADDL_LIBS``.
You can also specify the C++ library on the command-line when using
the :ref:`o2graph_script` using the ``o2scl-addl-libs`` command. If
O₂scl is installed with OpenMP support, the OpenMP libraries are often
not automatically linked in, and so you may need to include something
similar to ``/usr/local/lib/gcc/11/libgomp.1.dylib``. Also, on my
MacOS laptop, the readline library is not automatically included, so I
typically use
``O2SCL_ADDL_LIBS=/usr/lib/libreadline.dylib,/usr/local/lib/gcc/11/libgomp.1.dylib``.

.. _linkexample:

Linking with O₂scl example
--------------------------

Use this `link
<https://nbviewer.org/urls/raw.githubusercontent.com/awsteiner/o2sclpy/main/examples/link_o2scl.ipynb>`_
to view this example as a jupyter notebook on nbviewer.org.

.. literalinclude:: ../examples/link_o2scl.py

Class linker
------------
                    
.. autoclass:: o2sclpy.linker
        :members:
        :undoc-members:
