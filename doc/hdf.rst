.. _hdf:

HDF5 classes from O\ :sub:`2`\ scl
==================================

:ref:`O2sclpy <o2sclpy>`

* :ref:`Class hdf_file`
* :ref:`Class acol_manager`
* :ref:`Class cloud_file`
* :ref:`Function hdf_input_table`
* :ref:`Function hdf_input_n_table`
* :ref:`Function hdf_output_table`
* :ref:`Function hdf_input_table_units`
* :ref:`Function hdf_input_n_table_units`
* :ref:`Function hdf_output_table_units`
* :ref:`Function hdf_input_table3d`
* :ref:`Function hdf_input_n_table3d`
* :ref:`Function hdf_output_table3d`
* :ref:`Function hdf_input_uniform_grid`
* :ref:`Function hdf_input_n_uniform_grid`
* :ref:`Function hdf_output_uniform_grid`
* :ref:`Function hdf_input_tensor_grid`
* :ref:`Function hdf_input_n_tensor_grid`
* :ref:`Function hdf_output_tensor_grid`
* :ref:`Function hdf_input_vector_contour_line`
* :ref:`Function hdf_input_n_vector_contour_line`
* :ref:`Function hdf_output_vector_contour_line`
* :ref:`Function value_spec`
* :ref:`Function vector_spec`
* :ref:`Function strings_spec`
* :ref:`Function vector_spec_v`
* :ref:`Function mult_vector_spec`

Class hdf_file
--------------

.. autoclass:: o2sclpy.hdf_file
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class acol_manager
------------------

.. autoclass:: o2sclpy.acol_manager
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class cloud_file
----------------

.. autoclass:: o2sclpy.cloud_file
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Function hdf_input_table
------------------------

.. autofunction:: o2sclpy.hdf_input_table(link,hf,t,name)

Function hdf_input_n_table
--------------------------

.. autofunction:: o2sclpy.hdf_input_n_table(link,hf,t,name)

Function hdf_output_table
-------------------------

.. autofunction:: o2sclpy.hdf_output_table(link,hf,t,name)

Function hdf_input_table_units
------------------------------

.. autofunction:: o2sclpy.hdf_input_table_units(link,hf,t,name)

Function hdf_input_n_table_units
--------------------------------

.. autofunction:: o2sclpy.hdf_input_n_table_units(link,hf,t,name)

Function hdf_output_table_units
-------------------------------

.. autofunction:: o2sclpy.hdf_output_table_units(link,hf,t,name)

Function hdf_input_table3d
--------------------------

.. autofunction:: o2sclpy.hdf_input_table3d(link,hf,t,name)

Function hdf_input_n_table3d
----------------------------

.. autofunction:: o2sclpy.hdf_input_n_table3d(link,hf,t,name)

Function hdf_output_table3d
---------------------------

.. autofunction:: o2sclpy.hdf_output_table3d(link,hf,t,name)

Function hdf_input_uniform_grid
-------------------------------

.. autofunction:: o2sclpy.hdf_input_uniform_grid(link,hf,t,name)

Function hdf_input_n_uniform_grid
---------------------------------

.. autofunction:: o2sclpy.hdf_input_n_uniform_grid(link,hf,t,name)

Function hdf_output_uniform_grid
--------------------------------

.. autofunction:: o2sclpy.hdf_output_uniform_grid(link,hf,t,name)

Function hdf_input_tensor_grid
------------------------------

.. autofunction:: o2sclpy.hdf_input_tensor_grid(link,hf,t,name)

Function hdf_input_n_tensor_grid
--------------------------------

.. autofunction:: o2sclpy.hdf_input_n_tensor_grid(link,hf,t,name)

Function hdf_output_tensor_grid
-------------------------------

.. autofunction:: o2sclpy.hdf_output_tensor_grid(link,hf,t,name)

Function hdf_input_vector_contour_line
--------------------------------------

.. autofunction:: o2sclpy.hdf_input_vector_contour_line(link,hf,v,name)

Function hdf_input_n_vector_contour_line
----------------------------------------

.. autofunction:: o2sclpy.hdf_input_n_vector_contour_line(link,hf,v,name)

Function hdf_output_vector_contour_line
---------------------------------------

.. autofunction:: o2sclpy.hdf_output_vector_contour_line(link,hf,v,name)

Function value_spec
-------------------

.. autofunction:: o2sclpy.value_spec(link,spec,d,verbose,err_on_fail)

Function vector_spec
--------------------

.. autofunction:: o2sclpy.vector_spec(link,spec,v,verbose,err_on_fail)

Function strings_spec
---------------------

.. autofunction:: o2sclpy.strings_spec(link,spec,v,verbose,err_on_fail)

Function vector_spec_v
----------------------

.. autofunction:: o2sclpy.vector_spec_v(link,spec)

Function mult_vector_spec
-------------------------

.. autofunction:: o2sclpy.mult_vector_spec(link,spec,v,use_regex,verbose,err_on_fail)

