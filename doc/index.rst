O2sclpy: v0.924.dev1
====================

O\ :sub:`2`\ sclpy: A set of python classes for use with the
O\ :sub:`2`\ scl C++ library (separately documented
at <https://neutronstars.utk.edu/code/o2scl>)

.. warning:: This python library is experimental and still under
	     development.

The main objects of interest are the :ref:`O2graph script`, and the
classes :py:class:`o2sclpy.cloud_file`,
:py:class:`o2sclpy.hdf5_reader`, and :py:class:`o2sclpy.plotter` .

Installation and Requirements
-----------------------------

O\ :sub:`2`\ sclpy can be installed with e.g. ``pip3 install
o2sclpy``. If you want to install the development version (v0.924.dev1),
you can clone the git repository, change directory to the O\ :sub:`2`\
sclpy directory, and then use e.g. ``pip3 install .`` if you want to
use the pip package manager or ``python3 setup.py install`` to do a
direct installation. O\ :sub:`2`\ sclpy requires python3 packages
``requests``, `h5py <https://www.h5py.org/>`_, `numpy
<https://www.numpy.org>`_, and `matplotlib <https://matplotlib.org>`_.
O\ :sub:`2`\ sclpy also assumes LaTeX is installed on your system.

The ``o2graph`` script requires an installation of O\ :sub:`2`\ scl.
The release version, O\ :sub:`2`\ sclpy 0.923, requires the O\
:sub:`2`\ scl v0.923 release from
<https://github.com/awsteiner/o2scl/releases/tag/v0.923> and the
development version, O\ :sub:`2`\ sclpy 0.924.dev1, requires that the
most recent version of O\ :sub:`2`\ scl from the master branch on
github is installed on your machine.

The ``o2graph`` script attempts to dynamically load the O\ :sub:`2`\
scl libraries ``libo2scl`` and ``libo2scl_hdf`` using python's ctypes
module. If it cannot find them, you may need to use the argument
``-o2scl-libdir`` to specify the proper directory. If you're on OSX
and using GCC, the script must load the C++ library first, and if
necessary you can specify its location with the argument
``-o2scl-cpplib`` (on my OSX laptop this is ``-o2scl-cpplib
/usr/local/lib/gcc/9/libstdc++.dylib``).

Contents
--------

.. toctree::
   :maxdepth: 2

   licensing
   o2graph
   other_class
   other
   internal
   todos

--------------------------------------------------------------

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

