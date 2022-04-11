"""
  -------------------------------------------------------------------

  Copyright (C) 2020-2022, Andrew W. Steiner

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
            f=link.o2scl.o2scl_hdf_create_hdf_file
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
            f=self._link.o2scl.o2scl_hdf_free_hdf_file
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_compr_type
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @compr_type.setter
    def compr_type(self,value):
        """
        Setter function for hdf_file::compr_type .
        """
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_compr_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def min_compr_size(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_min_compr_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @min_compr_size.setter
    def min_compr_size(self,value):
        """
        Setter function for hdf_file::min_compr_size .
        """
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_min_compr_size
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    def has_write_access(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_hdf_hdf_file_has_write_access
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_open
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool,ctypes.c_bool]
        func(self._ptr,fname_,write_access,err_on_fail)
        return

    def open_or_create(self,fname):
        """
        | Parameters:
        | *fname*: string
        """
        fname_=ctypes.c_char_p(force_bytes(fname))
        func=self._link.o2scl.o2scl_hdf_hdf_file_open_or_create
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,fname_)
        return

    def close(self):
        """
        """
        func=self._link.o2scl.o2scl_hdf_hdf_file_close
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_getc
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_szt
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_var
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_fixed
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_setc
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_setd
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_seti
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_szt
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_sets
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_sets_fixed
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd_vec
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti_vec
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_szt_vec
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_vec
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_setd_vec
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_seti_vec
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_szt_vec
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_sets_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,s._ptr)
        return ret

    def getd_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd_ten
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti_ten
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_szt_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        ret=func(self._ptr,name_,t._ptr)
        return ret

    def setd_ten(self,name,t):
        """
        | Parameters:
        | *name*: string
        | *t*: :class:`tensor` object
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_hdf_hdf_file_setd_ten
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_seti_ten
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_szt_ten
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_find_object_by_type
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_find_object_by_name
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
        func=self._link.o2scl.o2scl_hdf_hdf_file_find_object_by_pattern
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int]
        ret=func(self._ptr,pattern_,type._ptr,verbose)
        return ret

    def file_list(self,verbose):
        """
        | Parameters:
        | *verbose*: ``int``
        """
        func=self._link.o2scl.o2scl_hdf_hdf_file_file_list
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,verbose)
        return

    def copy(self,verbose,hf2):
        """
        | Parameters:
        | *verbose*: ``int``
        | *hf2*: :class:`hdf_file` object
        """
        func=self._link.o2scl.o2scl_hdf_hdf_file_copy
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p]
        func(self._ptr,verbose,hf2._ptr)
        return


class acol_manager:
    """
    Python interface for O\ :sub:`2`\ scl class ``acol_manager``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/acol_manager.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class acol_manager

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_hdf_create_acol_manager
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
        Delete function for class acol_manager
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_hdf_free_acol_manager
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class acol_manager
        
        Returns: a acol_manager object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def get_env_var_name(self,env_var_name):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_env_var_name
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,env_var_name._ptr)
        return

    def set_env_var_name(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_env_var_name
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_cl(self,cl):
        """
        Get object of type :class:`cli`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_cl
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        cl._ptr=func(self._ptr)
        cl._owner=False
        return

    def set_cl(self,value):
        """
        Set object of type :class:`cli`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_cl
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    @property
    def verbose(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for acol_manager::verbose .
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    def get_type(self,type):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_type
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,type._ptr)
        return

    def set_type(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_table_obj(self,table_obj):
        """
        Get object of type :class:`table_units<>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_table_obj
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        table_obj._ptr=func(self._ptr)
        table_obj._owner=False
        return

    def set_table_obj(self,value):
        """
        Set object of type :class:`table_units<>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_table_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_table3d_obj(self,table3d_obj):
        """
        Get object of type :class:`table3d`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_table3d_obj
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        table3d_obj._ptr=func(self._ptr)
        table3d_obj._owner=False
        return

    def set_table3d_obj(self,value):
        """
        Set object of type :class:`table3d`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_table3d_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_hist_obj(self,hist_obj):
        """
        Get object of type :class:`hist`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_hist_obj
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        hist_obj._ptr=func(self._ptr)
        hist_obj._owner=False
        return

    def set_hist_obj(self,value):
        """
        Set object of type :class:`hist`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_hist_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_hist_2d_obj(self,hist_2d_obj):
        """
        Get object of type :class:`hist_2d`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_hist_2d_obj
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        hist_2d_obj._ptr=func(self._ptr)
        hist_2d_obj._owner=False
        return

    def set_hist_2d_obj(self,value):
        """
        Set object of type :class:`hist_2d`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_hist_2d_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    @property
    def int_obj(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_int_obj
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @int_obj.setter
    def int_obj(self,value):
        """
        Setter function for acol_manager::int_obj .
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_int_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def char_obj(self):
        """
        Property of type ``ctypes.c_char``
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_char_obj
        func.restype=ctypes.c_char
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @char_obj.setter
    def char_obj(self,value):
        """
        Setter function for acol_manager::char_obj .
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_char_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_char]
        func(self._ptr,value)
        return

    @property
    def double_obj(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_double_obj
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @double_obj.setter
    def double_obj(self,value):
        """
        Setter function for acol_manager::double_obj .
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_double_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def size_t_obj(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_size_t_obj
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @size_t_obj.setter
    def size_t_obj(self,value):
        """
        Setter function for acol_manager::size_t_obj .
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_size_t_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    def get_string_obj(self,string_obj):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_string_obj
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,string_obj._ptr)
        return

    def set_string_obj(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_string_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return


class cloud_file:
    """
    Python interface for O\ :sub:`2`\ scl class ``cloud_file``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/cloud_file.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class cloud_file

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_hdf_create_cloud_file
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
        Delete function for class cloud_file
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_hdf_free_cloud_file
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class cloud_file
        
        Returns: a cloud_file object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def hash_type(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_hash_type
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @hash_type.setter
    def hash_type(self,value):
        """
        Setter function for cloud_file::hash_type .
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_set_hash_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def verbose(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for cloud_file::verbose .
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def throw_on_fail(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_throw_on_fail
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @throw_on_fail.setter
    def throw_on_fail(self,value):
        """
        Setter function for cloud_file::throw_on_fail .
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_set_throw_on_fail
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def allow_wget(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_allow_wget
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @allow_wget.setter
    def allow_wget(self,value):
        """
        Setter function for cloud_file::allow_wget .
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_set_allow_wget
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def allow_curl(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_allow_curl
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @allow_curl.setter
    def allow_curl(self,value):
        """
        Setter function for cloud_file::allow_curl .
        """
        func=self._link.o2scl.o2scl_hdf_cloud_file_set_allow_curl
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_file(self,file,url,dir=""):
        """
        | Parameters:
        | *file*: string
        | *url*: string
        | *dir* ="": string
        | Returns: a Python int
        """
        file_=ctypes.c_char_p(force_bytes(file))
        url_=ctypes.c_char_p(force_bytes(url))
        dir_=ctypes.c_char_p(force_bytes(dir))
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_file
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,file_,url_,dir_)
        return ret

    def get_file_hash(self,file,url,hash="",dir=""):
        """
        | Parameters:
        | *file*: string
        | *url*: string
        | *hash* ="": string
        | *dir* ="": string
        | Returns: a Python int
        """
        file_=ctypes.c_char_p(force_bytes(file))
        url_=ctypes.c_char_p(force_bytes(url))
        hash_=ctypes.c_char_p(force_bytes(hash))
        dir_=ctypes.c_char_p(force_bytes(dir))
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_file_hash
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,file_,url_,hash_,dir_)
        return ret

    def hdf5_open(self,hf,file,url,dir=""):
        """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *file*: string
        | *url*: string
        | *dir* ="": string
        | Returns: a Python int
        """
        file_=ctypes.c_char_p(force_bytes(file))
        url_=ctypes.c_char_p(force_bytes(url))
        dir_=ctypes.c_char_p(force_bytes(dir))
        func=self._link.o2scl.o2scl_hdf_cloud_file_hdf5_open
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,hf._ptr,file_,url_,dir_)
        return ret

    def hdf5_open_hash(self,hf,file,url,hash="",dir=""):
        """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *file*: string
        | *url*: string
        | *hash* ="": string
        | *dir* ="": string
        | Returns: a Python int
        """
        file_=ctypes.c_char_p(force_bytes(file))
        url_=ctypes.c_char_p(force_bytes(url))
        hash_=ctypes.c_char_p(force_bytes(hash))
        dir_=ctypes.c_char_p(force_bytes(dir))
        func=self._link.o2scl.o2scl_hdf_cloud_file_hdf5_open_hash
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,hf._ptr,file_,url_,hash_,dir_)
        return ret


def hdf_input_table(link,hf,t,name):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table<>` object
        | *name*: string
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl.o2scl_hdf_hdf_input_table_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_n_table_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_output_table_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_table_units_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_n_table_units_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_output_table_units_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_table3d_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_n_table3d_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_output_table3d_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_uniform_grid_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_n_uniform_grid_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_output_uniform_grid_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_tensor_grid_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_input_n_tensor_grid_wrapper
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
    func=link.o2scl.o2scl_hdf_hdf_output_tensor_grid_wrapper
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
    func=link.o2scl.o2scl_hdf_value_spec_wrapper
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
    func=link.o2scl.o2scl_hdf_vector_spec_std_vector_double__wrapper
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
    func=link.o2scl.o2scl_hdf_strings_spec_std_vector_std_string__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(spec_,v._ptr,verbose,err_on_fail)
    return ret

def vector_spec_v(link,spec):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *spec*: string
        | Returns: ``std_vector`` object
    """
    spec_=ctypes.c_char_p(force_bytes(spec))
    func=link.o2scl.o2scl_hdf_vector_spec_wrapper
    func.restype=std_vector
    func.argtypes=[ctypes.c_char_p]
    ret=func(spec_)
    return ret

def mult_vector_spec(link,spec,v,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *spec*: string
        | *v*: :class:`std::vector<std::vector<double>>` object
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    spec_=ctypes.c_char_p(force_bytes(spec))
    func=link.o2scl.o2scl_hdf_mult_vector_spec_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(spec_,v._ptr,verbose,err_on_fail)
    return ret

