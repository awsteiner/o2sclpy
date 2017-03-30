O2sclpy
=======

.. toctree::
   :maxdepth: 2
   :caption: Contents:

O\ :sub:`2`\ sclpy: A set of python classes for use with the
O\ :sub:`2`\ scl C++ library (separately documented
at <https://web.utk.edu/~asteine1/o2scl>)

The main objects of interest are the :ref:`O2graph script`, and the
classes :py:class:`o2sclpy.cloud_file`,
:py:class:`o2sclpy.hdf5_reader`, and :py:class:`o2sclpy.plotter` .

--------------------------------------------------------------
	     
O2graph script
==============

The O\ :sub:`2`\ sclpy package includes a script called ``o2graph``
which can be used to plot O\ :sub:`2`\ scl data. The O\ :sub:`2`\ graph
script assumes that the O\ :sub:`2`\ scl library has been installed
separately (with HDF5 support enabled).

Usage requirements
------------------

The script attempts to dynamically load the O\ :sub:`2`\ scl libraries
``libo2scl`` and ``libo2scl_hdf`` using python's ctypes module. If it
cannot find them, you may need to use the argument ``-o2scl-libdir``
to specify the proper directory. On OSX, the script must load
the C++ library first, and if necessary you can specify its location
with the argument ``-o2scl-cpplib``.

Basic usage
-----------

.. include:: static/o2graph.help.txt
   :literal:

Intergration with o2scl
-----------------------

The O\ :sub:`2`\ graph script implements almost all of the
commands from the ``acol`` executable in O\ :sub:`2`\ scl
documented at
<https://web.utk.edu/~asteine1/o2scl/html/acol_section.html>
	     
--------------------------------------------------------------
	     
O2sclpy classes
===============

.. module:: o2sclpy

Class cloud_file
----------------
	    
.. autoclass:: cloud_file
	:members:
	:undoc-members:

Class hdf5_reader
-----------------
	    
.. autoclass:: hdf5_reader
	:members:
	:undoc-members:

Class plotter
-------------
	    
.. autoclass:: plotter
	:members:
	:undoc-members:

--------------------------------------------------------------
	     
Other O2sclpy objects
=====================

.. autofunction:: default_plot
.. autofunction:: get_str_array
.. autofunction:: parse_arguments
.. autofunction:: string_to_dict
.. autodata:: version		  

--------------------------------------------------------------

Todo list
=========

.. todolist::
	   
--------------------------------------------------------------

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
