.. _link:

Linking with O\ :sub:`2`\ scl
=============================

The :class:`o2sclpy.linker` class (see below) controls the dynamical loading
of the O\ :sub:`2`\ scl libraries. This class may require some
additional information about your system in order to perform the
dynamic loading properly. 

The variable :data:`link_o2scl.o2scl_cpp_lib` specifies the C++ library
to be loaded, in case it is not loaded automatically. The function
:func:`link_o2scl.get_library_settings()` will set this to be the
value of the environment variable ``O2SCL_CPP_LIB``. You can also
specify the C++ library on the command-line when using the
:ref:`o2graph_script` using the ``o2scl-cpp-lib`` command. On a MacOS
laptop, when using ``clang`` the C++ library is typically found
automatically, but when using ``gcc`` I have to set this value to
``/usr/local/lib/gcc/10/libstdc++.dylib``.

The variable :data:`link_o2scl.o2scl_lib_dir` specifies the directory
where ``libo2scl.so`` is to be found, in case it cannot be found
automatically. The function :func:`link_o2scl.get_library_settings()`
will set this to be the value of the environment variable
``O2SCL_LIB_DIR``. You can also specify the C++ library on the
command-line when using the :ref:`o2graph_script` using the
``o2scl-lib-dir`` command.

Finally, the variable :data:`link_o2scl.o2scl_addl_libs` is a list of
additional libraries which are required and not automatically included
by the dynamic loading. The function
:func:`link_o2scl.get_library_settings()` will set this to be the
comma-separated list in the environment variable ``O2SCL_ADDL_LIBS``.
You can also specify the C++ library on the command-line when using
the :ref:`o2graph_script` using the ``o2scl-addl-libs`` command. If O\
:sub:`2`\ scl is installed with OpenMP support, the OpenMP libraries
are often not automatically linked in, and so you may need to include
something similar to ``/usr/local/lib/gcc/10/libgomp.1.dylib``. Also,
on my MacOS laptop, the readline library is not automatically
included, so I typically use
``O2SCL_ADDL_LIBS=/usr/lib/libreadline.dylib,/usr/local/lib/gcc/10/libgomp.1.dylib``. 

.. autoclass:: o2sclpy.linker
        :members:
        :undoc-members:
