.. _base:

Base classes from O\ :sub:`2`\ scl
==================================

:ref:`O2sclpy <o2sclpy>`

Note that this python interface is not intended
to provide the full functionality of the corresponding C++ 
class.

* :ref:`Class std_string`
* :ref:`Class std_vector`
* :ref:`Class std_vector_int`
* :ref:`Class std_vector_size_t`
* :ref:`Class std_vector_string`
* :ref:`Class ublas_vector`
* :ref:`Class ublas_vector_int`
* :ref:`Class ublas_matrix`
* :ref:`Class ublas_matrix_int`
* :ref:`Class std_vector_vector`
* :ref:`Class vec_vec_string`
* :ref:`Class std_complex`
* :ref:`Class lib_settings_class`
* :ref:`Class table`
* :ref:`Class table_units`
* :ref:`Class uniform_grid`
* :ref:`Class uniform_grid_end`
* :ref:`Class uniform_grid_width`
* :ref:`Class uniform_grid_end_width`
* :ref:`Class uniform_grid_log_end`
* :ref:`Class uniform_grid_log_width`
* :ref:`Class uniform_grid_log_end_width`
* :ref:`Class table3d`
* :ref:`Class index_spec`
* :ref:`Class ix_index`
* :ref:`Class ix_fixed`
* :ref:`Class ix_sum`
* :ref:`Class ix_trace`
* :ref:`Class ix_reverse`
* :ref:`Class ix_range`
* :ref:`Class ix_interp`
* :ref:`Class ix_grid`
* :ref:`Class ix_gridw`
* :ref:`Class tensor`
* :ref:`Class tensor_int`
* :ref:`Class tensor_size_t`
* :ref:`Class tensor_grid`
* :ref:`Class find_constants_const_entry`
* :ref:`Class find_constants`
* :ref:`Class convert_units_der_unit`
* :ref:`Class convert_units`
* :ref:`Class columnify`
* :ref:`Class format_float`
* :ref:`Class interp_vec`
* :ref:`Class interp_krige_optim_rbf_noise`
* :ref:`Class terminal`
* :ref:`Class gen_test_number`
* :ref:`Class funct_string`
* :ref:`Class comm_option_s`
* :ref:`Class cmd_line_arg`
* :ref:`Class cli`
* :ref:`Class shared_ptr_table_units`
* :ref:`Function rearrange_and_copy`
* :ref:`Function rearrange_and_copy_int`
* :ref:`Function rearrange_and_copy_size_t`
* :ref:`Function grid_rearrange_and_copy`
* :ref:`Function fermi_function`
* :ref:`Function bose_function`
* :ref:`Function quadratic_extremum_x`
* :ref:`Function quadratic_extremum_y`
* :ref:`Function screenify`
* :ref:`Function file_exists`
* :ref:`Function RGBtoHSV`
* :ref:`Function HSVtoRGB`
* :ref:`Function wordexp_single_file`
* :ref:`Function wordexp_wrapper`
* :ref:`Function function_to_double`
* :ref:`Function function_to_double_nothrow`
* :ref:`Function find_constant`
* :ref:`Function string_to_uint_list`
* :ref:`Function rewrap_keep_endlines`
* :ref:`Function vector_level_count`
* :ref:`Function vector_deriv_interp`
* :ref:`Function vector_deriv2_interp`
* :ref:`Function vector_deriv_xy_interp`
* :ref:`Function vector_deriv2_xy_interp`
* :ref:`Function vector_integ_interp`
* :ref:`Function vector_integ_xy_interp`
* :ref:`Function vector_integ_ul_interp`
* :ref:`Function vector_integ_ul_xy_interp`
* :ref:`Function vector_find_level`
* :ref:`Function vector_invert_enclosed_sum`
* :ref:`Function vector_region_int`
* :ref:`Function vector_region_fracint`
* :ref:`Function vector_bound_fracint`
* :ref:`Function vector_bound_int`
* :ref:`Function rebin_xy`
* :ref:`Function linear_or_log_chi2`
* :ref:`Function linear_or_log_pair`
* :ref:`Function vector_refine`
* :ref:`Function linear_or_log`
* :ref:`Function get_screen_size_ioctl`

Class std_string
----------------

.. autoclass:: o2sclpy.std_string
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class std_vector
----------------

.. autoclass:: o2sclpy.std_vector
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class std_vector_int
--------------------

.. autoclass:: o2sclpy.std_vector_int
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class std_vector_size_t
-----------------------

.. autoclass:: o2sclpy.std_vector_size_t
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class std_vector_string
-----------------------

.. autoclass:: o2sclpy.std_vector_string
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class ublas_vector
------------------

.. autoclass:: o2sclpy.ublas_vector
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class ublas_vector_int
----------------------

.. autoclass:: o2sclpy.ublas_vector_int
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class ublas_matrix
------------------

.. autoclass:: o2sclpy.ublas_matrix
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class ublas_matrix_int
----------------------

.. autoclass:: o2sclpy.ublas_matrix_int
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class std_vector_vector
-----------------------

.. autoclass:: o2sclpy.std_vector_vector
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class vec_vec_string
--------------------

.. autoclass:: o2sclpy.vec_vec_string
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__
        .. automethod:: __setitem__

Class std_complex
-----------------

.. autoclass:: o2sclpy.std_complex
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class lib_settings_class
------------------------

.. autoclass:: o2sclpy.lib_settings_class
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class table
-----------

.. autoclass:: o2sclpy.table
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__
        .. automethod:: __getitem__

Class table_units
-----------------

.. autoclass:: o2sclpy.table_units
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__

Class uniform_grid
------------------

.. autoclass:: o2sclpy.uniform_grid
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __getitem__

Class uniform_grid_end
----------------------

.. autoclass:: o2sclpy.uniform_grid_end
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class uniform_grid_width
------------------------

.. autoclass:: o2sclpy.uniform_grid_width
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class uniform_grid_end_width
----------------------------

.. autoclass:: o2sclpy.uniform_grid_end_width
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class uniform_grid_log_end
--------------------------

.. autoclass:: o2sclpy.uniform_grid_log_end
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class uniform_grid_log_width
----------------------------

.. autoclass:: o2sclpy.uniform_grid_log_width
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class uniform_grid_log_end_width
--------------------------------

.. autoclass:: o2sclpy.uniform_grid_log_end_width
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class table3d
-------------

.. autoclass:: o2sclpy.table3d
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__

Class index_spec
----------------

.. autoclass:: o2sclpy.index_spec
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_index
--------------

.. autoclass:: o2sclpy.ix_index
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_fixed
--------------

.. autoclass:: o2sclpy.ix_fixed
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_sum
------------

.. autoclass:: o2sclpy.ix_sum
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_trace
--------------

.. autoclass:: o2sclpy.ix_trace
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_reverse
----------------

.. autoclass:: o2sclpy.ix_reverse
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_range
--------------

.. autoclass:: o2sclpy.ix_range
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_interp
---------------

.. autoclass:: o2sclpy.ix_interp
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_grid
-------------

.. autoclass:: o2sclpy.ix_grid
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class ix_gridw
--------------

.. autoclass:: o2sclpy.ix_gridw
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class tensor
------------

.. autoclass:: o2sclpy.tensor
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__

Class tensor_int
----------------

.. autoclass:: o2sclpy.tensor_int
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__

Class tensor_size_t
-------------------

.. autoclass:: o2sclpy.tensor_size_t
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__

Class tensor_grid
-----------------

.. autoclass:: o2sclpy.tensor_grid
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __deepcopy__

Class find_constants_const_entry
--------------------------------

.. autoclass:: o2sclpy.find_constants_const_entry
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class find_constants
--------------------

.. autoclass:: o2sclpy.find_constants
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class convert_units_der_unit
----------------------------

.. autoclass:: o2sclpy.convert_units_der_unit
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class convert_units
-------------------

.. autoclass:: o2sclpy.convert_units
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class columnify
---------------

.. autoclass:: o2sclpy.columnify
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class format_float
------------------

.. autoclass:: o2sclpy.format_float
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class interp_vec
----------------

.. autoclass:: o2sclpy.interp_vec
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class interp_krige_optim_rbf_noise
----------------------------------

.. autoclass:: o2sclpy.interp_krige_optim_rbf_noise
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class terminal
--------------

.. autoclass:: o2sclpy.terminal
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class gen_test_number
---------------------

.. autoclass:: o2sclpy.gen_test_number
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class funct_string
------------------

.. autoclass:: o2sclpy.funct_string
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__
        .. automethod:: __getitem__

Class comm_option_s
-------------------

.. autoclass:: o2sclpy.comm_option_s
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class cmd_line_arg
------------------

.. autoclass:: o2sclpy.cmd_line_arg
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class cli
---------

.. autoclass:: o2sclpy.cli
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__
        .. automethod:: __copy__

Class shared_ptr_table_units
----------------------------

.. autoclass:: o2sclpy.shared_ptr_table_units
        :members:
        :undoc-members:

        .. automethod:: __init__
        .. automethod:: __del__

Function rearrange_and_copy
---------------------------

.. autofunction:: o2sclpy.rearrange_and_copy(link,t,spec,verbose,err_on_fail)

Function rearrange_and_copy_int
-------------------------------

.. autofunction:: o2sclpy.rearrange_and_copy_int(link,t,spec,verbose,err_on_fail)

Function rearrange_and_copy_size_t
----------------------------------

.. autofunction:: o2sclpy.rearrange_and_copy_size_t(link,t,spec,verbose,err_on_fail)

Function grid_rearrange_and_copy
--------------------------------

.. autofunction:: o2sclpy.grid_rearrange_and_copy(link,t,spec,verbose,err_on_fail)

Function fermi_function
-----------------------

.. autofunction:: o2sclpy.fermi_function(link,E,mu,T,limit)

Function bose_function
----------------------

.. autofunction:: o2sclpy.bose_function(link,E,mu,T,limit)

Function quadratic_extremum_x
-----------------------------

.. autofunction:: o2sclpy.quadratic_extremum_x(link,x1,x2,x3,y1,y2,y3)

Function quadratic_extremum_y
-----------------------------

.. autofunction:: o2sclpy.quadratic_extremum_y(link,x1,x2,x3,y1,y2,y3)

Function screenify
------------------

.. autofunction:: o2sclpy.screenify(link,nin,in_cols,out_cols,max_size)

Function file_exists
--------------------

.. autofunction:: o2sclpy.file_exists(link,fname)

Function RGBtoHSV
-----------------

.. autofunction:: o2sclpy.RGBtoHSV(link,r,g,b,h,s,v)

Function HSVtoRGB
-----------------

.. autofunction:: o2sclpy.HSVtoRGB(link,h,s,v,r,g,b)

Function wordexp_single_file
----------------------------

.. autofunction:: o2sclpy.wordexp_single_file(link,fname)

Function wordexp_wrapper
------------------------

.. autofunction:: o2sclpy.wordexp_wrapper(link,word,matches)

Function function_to_double
---------------------------

.. autofunction:: o2sclpy.function_to_double(link,s,verbose)

Function function_to_double_nothrow
-----------------------------------

.. autofunction:: o2sclpy.function_to_double_nothrow(link,s,result,verbose)

Function find_constant
----------------------

.. autofunction:: o2sclpy.find_constant(link,name,unit)

Function string_to_uint_list
----------------------------

.. autofunction:: o2sclpy.string_to_uint_list(link,x,list)

Function rewrap_keep_endlines
-----------------------------

.. autofunction:: o2sclpy.rewrap_keep_endlines(link,str,sv,ncol,verbose,ignore_vt100)

Function vector_level_count
---------------------------

.. autofunction:: o2sclpy.vector_level_count(link,level,n,x,y)

Function vector_deriv_interp
----------------------------

.. autofunction:: o2sclpy.vector_deriv_interp(link,n,v,dv,interp_type)

Function vector_deriv2_interp
-----------------------------

.. autofunction:: o2sclpy.vector_deriv2_interp(link,n,v,dv,interp_type)

Function vector_deriv_xy_interp
-------------------------------

.. autofunction:: o2sclpy.vector_deriv_xy_interp(link,n,vx,vy,dv,interp_type)

Function vector_deriv2_xy_interp
--------------------------------

.. autofunction:: o2sclpy.vector_deriv2_xy_interp(link,n,vx,vy,dv,interp_type)

Function vector_integ_interp
----------------------------

.. autofunction:: o2sclpy.vector_integ_interp(link,n,vx,interp_type)

Function vector_integ_xy_interp
-------------------------------

.. autofunction:: o2sclpy.vector_integ_xy_interp(link,n,vx,vy,interp_type)

Function vector_integ_ul_interp
-------------------------------

.. autofunction:: o2sclpy.vector_integ_ul_interp(link,n,x2,v,interp_type)

Function vector_integ_ul_xy_interp
----------------------------------

.. autofunction:: o2sclpy.vector_integ_ul_xy_interp(link,n,x2,vx,vy,interp_type)

Function vector_find_level
--------------------------

.. autofunction:: o2sclpy.vector_find_level(link,level,n,x,y,locs)

Function vector_invert_enclosed_sum
-----------------------------------

.. autofunction:: o2sclpy.vector_invert_enclosed_sum(link,sum,n,x,y,lev,boundaries,verbose,err_on_fail)

Function vector_region_int
--------------------------

.. autofunction:: o2sclpy.vector_region_int(link,n,x,y,intl,locs,boundaries,verbose,err_on_fail)

Function vector_region_fracint
------------------------------

.. autofunction:: o2sclpy.vector_region_fracint(link,n,x,y,intl,locs,boundaries,verbose,err_on_fail)

Function vector_bound_fracint
-----------------------------

.. autofunction:: o2sclpy.vector_bound_fracint(link,n,x,y,frac,low,high,boundaries,verbose,err_on_fail)

Function vector_bound_int
-------------------------

.. autofunction:: o2sclpy.vector_bound_int(link,n,x,y,frac,low,high,boundaries,verbose,err_on_fail)

Function rebin_xy
-----------------

.. autofunction:: o2sclpy.rebin_xy(link,x,y,x_out,y_out,n_pts,interp_type)

Function linear_or_log_chi2
---------------------------

.. autofunction:: o2sclpy.linear_or_log_chi2(link,x,y)

Function linear_or_log_pair
---------------------------

.. autofunction:: o2sclpy.linear_or_log_pair(link,x,y,log_x,log_y)

Function vector_refine
----------------------

.. autofunction:: o2sclpy.vector_refine(link,n,index,data,factor,interp_type)

Function linear_or_log
----------------------

.. autofunction:: o2sclpy.linear_or_log(link,x,log_x)

Function get_screen_size_ioctl
------------------------------

.. autofunction:: o2sclpy.get_screen_size_ioctl(link,row,col)

