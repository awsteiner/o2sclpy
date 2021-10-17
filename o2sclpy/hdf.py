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

from o2sclpy.base import *

class hdf_file:
    """
    Python interface for O\ :sub:`2`\ scl class ``hdf_file``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/hdf_file.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class hdf_file

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl_hdf.o2scl_hdf_create_hdf_file
            f.restype=ctypes.c_void_p
            f.argtypes=[]
            self._ptr=f()
        else:
            self._ptr=pointer
            self._owner=False
        self._link=link
        return

    def __del__(self):
        """
        Delete function for class hdf_file
        """

        if self._owner==True:
            f=self._link.o2scl_hdf.o2scl_hdf_free_hdf_file
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class hdf_file
        
        Returns: a hdf_file object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def compr_type(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_get_compr_type
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @compr_type.setter
    def compr_type(self,value):
        """
        Setter function for hdf_file::compr_type .
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_set_compr_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def min_compr_size(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_get_min_compr_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @min_compr_size.setter
    def min_compr_size(self,value):
        """
        Setter function for hdf_file::min_compr_size .
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_set_min_compr_size
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    def has_write_access(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_has_write_access
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def open(self,fname,write_access=False,err_on_fail=True):
        """
        | Parameters:
        | *fname*: string
        | *write_access* =false: ``bool``
        | *err_on_fail* =true: ``bool``
        """
        fname_=ctypes.c_char_p(force_bytes(fname))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_open
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool,ctypes.c_bool]
        func(self._ptr,fname_,write_access,err_on_fail)
        return

    def open_or_create(self,fname):
        """
        | Parameters:
        | *fname*: string
        """
        fname_=ctypes.c_char_p(force_bytes(fname))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_open_or_create
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,fname_)
        return

    def close(self):
        """
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_close
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def getc(self,name):
        """
        | Parameters:
        | *name*: string
        | Returns: a Python int, a Python obj
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_getc
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_char)]
        c_conv=ctypes.c_char(0)
        ret=func(self._ptr,name_,ctypes.byref(c_conv))
        return ret,c_conv.value

    def getd(self,name):
        """
        | Parameters:
        | *name*: string
        | Returns: a Python int, a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_getd
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_double)]
        d_conv=ctypes.c_double(0)
        ret=func(self._ptr,name_,ctypes.byref(d_conv))
        return ret,d_conv.value

    def geti(self,name):
        """
        | Parameters:
        | *name*: string
        | Returns: a Python int, a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_geti
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_int)]
        i_conv=ctypes.c_int(0)
        ret=func(self._ptr,name_,ctypes.byref(i_conv))
        return ret,i_conv.value

    def get_szt(self,name):
        """
        | Parameters:
        | *name*: string
        | Returns: a Python int, a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_get_szt
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
        u_conv=ctypes.c_size_t(0)
        ret=func(self._ptr,name_,ctypes.byref(u_conv))
        return ret,u_conv.value

    def gets(self,name,s):
        """
        | Parameters:
        | *name*: string
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        s_=ctypes.c_char_p(force_bytes(s))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_gets
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,s._ptr)
        return ret

    def gets_var(self,name,s):
        """
        | Parameters:
        | *name*: string
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        s_=ctypes.c_char_p(force_bytes(s))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_gets_var
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,s._ptr)
        return ret

    def gets_fixed(self,name,s):
        """
        | Parameters:
        | *name*: string
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        s_=ctypes.c_char_p(force_bytes(s))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_gets_fixed
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,s._ptr)
        return ret

    def setc(self,name,c):
        """
        | Parameters:
        | *name*: string
        | *c*: ``char``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_setc
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char]
        func(self._ptr,name_,c)
        return

    def setd(self,name,d):
        """
        | Parameters:
        | *name*: string
        | *d*: ``double``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_setd
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,name_,d)
        return

    def seti(self,name,i):
        """
        | Parameters:
        | *name*: string
        | *i*: ``int``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_seti
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int]
        func(self._ptr,name_,i)
        return

    def set_szt(self,name,u):
        """
        | Parameters:
        | *name*: string
        | *u*: ``size_t``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_set_szt
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        func(self._ptr,name_,u)
        return

    def sets(self,name,s):
        """
        | Parameters:
        | *name*: string
        | *s*: string
        """
        name_=ctypes.c_char_p(force_bytes(name))
        s_=ctypes.c_char_p(force_bytes(s))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_sets
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,name_,s_)
        return

    def sets_fixed(self,name,s):
        """
        | Parameters:
        | *name*: string
        | *s*: string
        """
        name_=ctypes.c_char_p(force_bytes(name))
        s_=ctypes.c_char_p(force_bytes(s))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_sets_fixed
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,name_,s_)
        return

    def getd_vec(self,name,v):
        """
        | Parameters:
        | *name*: string
        | *v*: :class:`std_vector` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_getd_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,v._ptr)
        return ret

    def geti_vec(self,name,v):
        """
        | Parameters:
        | *name*: string
        | *v*: :class:`std_vector_int` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_geti_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,v._ptr)
        return ret

    def get_szt_vec(self,name,v):
        """
        | Parameters:
        | *name*: string
        | *v*: :class:`std_vector_size_t` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_get_szt_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,v._ptr)
        return ret

    def gets_vec(self,name,s):
        """
        | Parameters:
        | *name*: string
        | *s*: :class:`std_vector_string` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_gets_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,s._ptr)
        return ret

    def setd_vec(self,name,v):
        """
        | Parameters:
        | *name*: string
        | *v*: :class:`std_vector` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_setd_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,v._ptr)
        return ret

    def seti_vec(self,name,v):
        """
        | Parameters:
        | *name*: string
        | *v*: :class:`std_vector_int` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_seti_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,v._ptr)
        return ret

    def set_szt_vec(self,name,v):
        """
        | Parameters:
        | *name*: string
        | *v*: :class:`std_vector_size_t` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_set_szt_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,v._ptr)
        return ret

    def sets_vec(self,name,s):
        """
        | Parameters:
        | *name*: string
        | *s*: :class:`std_vector_string` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_sets_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,s._ptr)
        return ret

    def getd_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor<>` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_getd_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,t._ptr)
        return ret

    def geti_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor<int>` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_geti_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,t._ptr)
        return ret

    def get_szt_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor<size_t>` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_get_szt_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,t._ptr)
        return ret

    def setd_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor<>` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_setd_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,t._ptr)
        return ret

    def seti_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor<int>` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_seti_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,t._ptr)
        return ret

    def set_szt_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor<size_t>` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_set_szt_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,t._ptr)
        return ret

    def find_object_by_type(self,type,name,verbose=0):
        """
        | Parameters:
        | *type*: string
        | *name*: :class:`std_string` object
        | *verbose* =0: ``int``
        | Returns: a Python int
        """
        type_=ctypes.c_char_p(force_bytes(type))
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_find_object_by_type
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int]
        ret=func(self._ptr,type_,name._ptr,verbose)
        return ret

    def find_object_by_name(self,name,type,verbose=0):
        """
        | Parameters:
        | *name*: string
        | *type*: :class:`std_string` object
        | *verbose* =0: ``int``
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        type_=ctypes.c_char_p(force_bytes(type))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_find_object_by_name
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int]
        ret=func(self._ptr,name_,type._ptr,verbose)
        return ret

    def find_object_by_pattern(self,pattern,type,verbose=0):
        """
        | Parameters:
        | *pattern*: string
        | *type*: :class:`std_string` object
        | *verbose* =0: ``int``
        | Returns: a Python int
        """
        pattern_=ctypes.c_char_p(force_bytes(pattern))
        type_=ctypes.c_char_p(force_bytes(type))
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_find_object_by_pattern
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int]
        ret=func(self._ptr,pattern_,type._ptr,verbose)
        return ret

    def file_list(self,verbose):
        """
        | Parameters:
        | *verbose*: ``int``
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_file_list
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,verbose)
        return

    def copy(self,verbose,hf2):
        """
        | Parameters:
        | *verbose*: ``int``
        | *hf2*: :class:`hdf_file` object
        """
        func=self._link.o2scl_hdf.o2scl_hdf_hdf_file_copy
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p]
        func(self._ptr,verbose,hf2._ptr)
        return


def hdf_input_table(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_table_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_n_table(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table<>` object
        | *name*: :class:`std::string` object
    """
    name.__del__()
    name._ptr=ctypes.c_void_p()
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_n_table_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
    func(hf._ptr,t._ptr,ctypes.byref(name._ptr))
    name._owner=True
    return

def hdf_output_table(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_output_table_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_table_units(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table_units<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_table_units_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_n_table_units(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table_units<>` object
        | *name*: :class:`std::string` object
    """
    name.__del__()
    name._ptr=ctypes.c_void_p()
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_n_table_units_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
    func(hf._ptr,t._ptr,ctypes.byref(name._ptr))
    name._owner=True
    return

def hdf_output_table_units(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table_units<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_output_table_units_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_table3d(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table3d` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_table3d_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_n_table3d(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table3d` object
        | *name*: :class:`std::string` object
    """
    name.__del__()
    name._ptr=ctypes.c_void_p()
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_n_table3d_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
    func(hf._ptr,t._ptr,ctypes.byref(name._ptr))
    name._owner=True
    return

def hdf_output_table3d(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table3d` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_output_table3d_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_uniform_grid(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`uniform_grid<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_uniform_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_n_uniform_grid(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`uniform_grid<>` object
        | *name*: :class:`std::string` object
    """
    name.__del__()
    name._ptr=ctypes.c_void_p()
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_n_uniform_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
    func(hf._ptr,t._ptr,ctypes.byref(name._ptr))
    name._owner=True
    return

def hdf_output_uniform_grid(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`uniform_grid<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_output_uniform_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_tensor_grid(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`tensor_grid<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_tensor_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def hdf_input_n_tensor_grid(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`tensor_grid<>` object
        | *name*: :class:`std::string` object
    """
    name.__del__()
    name._ptr=ctypes.c_void_p()
    func=link.o2scl_hdf.o2scl_hdf_hdf_input_n_tensor_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
    func(hf._ptr,t._ptr,ctypes.byref(name._ptr))
    name._owner=True
    return

def hdf_output_tensor_grid(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`tensor_grid<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl_hdf.o2scl_hdf_hdf_output_tensor_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p]
    func(hf._ptr,t._ptr,name_)
    return

def value_spec(link,spec,d,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *spec*: string
        | *d*: ``double``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    spec_=ctypes.c_char_p(force_bytes(spec))
    func=link.o2scl_hdf.o2scl_hdf_value_spec_wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(spec_,d._ptr,verbose,err_on_fail)
    return ret

def vector_spec(link,spec,v,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *spec*: string
        | *v*: :class:`std::vector<double>` object
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    spec_=ctypes.c_char_p(force_bytes(spec))
    func=link.o2scl_hdf.o2scl_hdf_vector_spec_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(spec_,v._ptr,verbose,err_on_fail)
    return ret

def strings_spec(link,spec,v,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *spec*: string
        | *v*: :class:`std::vector<std::string>` object
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    spec_=ctypes.c_char_p(force_bytes(spec))
    func=link.o2scl_hdf.o2scl_hdf_strings_spec_std_vector_std_string__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(spec_,v._ptr,verbose,err_on_fail)
    return ret

