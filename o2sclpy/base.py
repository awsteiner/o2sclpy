"""
  -------------------------------------------------------------------

  Copyright (C) 2020-2021, Andrew W. Steiner

  This file is part of O2scl.

  O2scl is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  O2scl is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with O2scl. If not, see <http://www.gnu.org/licenses/>.
  -------------------------------------------------------------------
"""

import ctypes
from abc import abstractmethod
from o2sclpy.utils import force_bytes


class table:
    """
    Python interface for class :ref:`table<> <o2scl:table<>>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class table<> .
        """

        f=dll.o2scl_create_table__
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class table<> .
        """

        f=self._dll.o2scl_free_table__
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def set(self,col,row,val):
        """
        Wrapper for table<>::set() .
        wrapper for :ref:`o2sclp:table<>::set()`.
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._dll.o2scl_table___set
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,col_,row,val)
        return

    def get(self,col,row):
        """
        Wrapper for table<>::get() .
        wrapper for :ref:`o2sclp:table<>::get()`.
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._dll.o2scl_table___get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        ret=func(self._ptr,col_,row)
        return ret

    def get_ncolumns(self):
        """
        Wrapper for table<>::get_ncolumns() .
        wrapper for :ref:`o2sclp:table<>::get_ncolumns()`.
        """
        func=self._dll.o2scl_table___get_ncolumns
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,]
        ret=func(self._ptr,)
        return ret

    def get_nlines(self):
        """
        Wrapper for table<>::get_nlines() .
        wrapper for :ref:`o2sclp:table<>::get_nlines()`.
        """
        func=self._dll.o2scl_table___get_nlines
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,]
        ret=func(self._ptr,)
        return ret

    def set_nlines(self,lines):
        """
        Wrapper for table<>::set_nlines() .
        wrapper for :ref:`o2sclp:table<>::set_nlines()`.
        """
        func=self._dll.o2scl_table___set_nlines
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,lines)
        return

    def new_column(self,col):
        """
        Wrapper for table<>::new_column() .
        wrapper for :ref:`o2sclp:table<>::new_column()`.
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._dll.o2scl_table___new_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,col_)
        return

    def get_column_name(self,icol):
        """
        Wrapper for table<>::get_column_name() .
        wrapper for :ref:`o2sclp:table<>::get_column_name()`.
        """
        func=self._dll.o2scl_table___get_column_name
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,icol)
        return ret

class find_constants:
    """
    Python interface for class :ref:`find_constants <o2scl:find_constants>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class find_constants .
        """

        f=dll.o2scl_create_find_constants
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class find_constants .
        """

        f=self._dll.o2scl_free_find_constants
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def find_print(self,name,unit,prec,verbose):
        """
        Wrapper for find_constants::find_print() .
        wrapper for :ref:`o2sclp:find_constants::find_print()`.
        """
        name_=ctypes.c_char_p(force_bytes(name))
        unit_=ctypes.c_char_p(force_bytes(unit))
        func=self._dll.o2scl_find_constants_find_print
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_int]
        func(self._ptr,name_,unit_,prec,verbose)
        return

    def find_unique(self,name,unit):
        """
        Wrapper for find_constants::find_unique() .
        wrapper for :ref:`o2sclp:find_constants::find_unique()`.
        """
        name_=ctypes.c_char_p(force_bytes(name))
        unit_=ctypes.c_char_p(force_bytes(unit))
        func=self._dll.o2scl_find_constants_find_unique
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,name_,unit_)
        return ret

class convert_units:
    """
    Python interface for class :ref:`convert_units<> <o2scl:convert_units<>>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class convert_units<> .
        """

        f=dll.o2scl_create_convert_units__
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class convert_units<> .
        """

        f=self._dll.o2scl_free_convert_units__
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def verbose(self):
        """
        Getter function for convert_units<>::verbose .
        """
        func=self._dll.o2scl_convert_units___get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for convert_units<>::verbose .
        """
        func=self._dll.o2scl_convert_units___set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def use_gnu_units(self):
        """
        Getter function for convert_units<>::use_gnu_units .
        """
        func=self._dll.o2scl_convert_units___get_use_gnu_units
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @use_gnu_units.setter
    def use_gnu_units(self,value):
        """
        Setter function for convert_units<>::use_gnu_units .
        """
        func=self._dll.o2scl_convert_units___set_use_gnu_units
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def err_on_fail(self):
        """
        Getter function for convert_units<>::err_on_fail .
        """
        func=self._dll.o2scl_convert_units___get_err_on_fail
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_on_fail.setter
    def err_on_fail(self,value):
        """
        Setter function for convert_units<>::err_on_fail .
        """
        func=self._dll.o2scl_convert_units___set_err_on_fail
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def combine_two_conv(self):
        """
        Getter function for convert_units<>::combine_two_conv .
        """
        func=self._dll.o2scl_convert_units___get_combine_two_conv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @combine_two_conv.setter
    def combine_two_conv(self,value):
        """
        Setter function for convert_units<>::combine_two_conv .
        """
        func=self._dll.o2scl_convert_units___set_combine_two_conv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_units_cmd_string(self,units_cmd_string):
        """
        Getter function for convert_units<>::units_cmd_string .
        """
        func=self._dll.o2scl_convert_units___get_units_cmd_string
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,units_cmd_string._ptr)
        return

    def set_units_cmd_string(self,value):
        """
        Setter function for convert_units<>::units_cmd_string .
        """
        func=self._dll.o2scl_convert_units___set_units_cmd_string
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def convert(self,frm,to,val):
        """
        Wrapper for convert_units<>::convert() .
        wrapper for :ref:`o2sclp:convert_units<>::convert()`.
        """
        frm_=ctypes.c_char_p(force_bytes(frm))
        to_=ctypes.c_char_p(force_bytes(to))
        func=self._dll.o2scl_convert_units___convert
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double]
        ret=func(self._ptr,frm_,to_,val)
        return ret

    def convert_ret(self,frm,to,val,converted):
        """
        Wrapper for convert_units<>::convert_ret() .
        wrapper for :ref:`o2sclp:convert_units<>::convert_ret()`.
        """
        frm_=ctypes.c_char_p(force_bytes(frm))
        to_=ctypes.c_char_p(force_bytes(to))
        func=self._dll.o2scl_convert_units___convert_ret
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,frm_,to_,val,converted)
        return ret

    def print_cache(self):
        """
        Wrapper for convert_units<>::print_cache() .
        wrapper for :ref:`o2sclp:convert_units<>::print_cache()`.
        """
        func=self._dll.o2scl_convert_units___print_cache
        func.argtypes=[ctypes.c_void_p,]
        func(self._ptr,)
        return

