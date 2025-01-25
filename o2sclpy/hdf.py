"""
  ───────────────────────────────────────────────────────────────────

  Copyright (C) 2020-2025, Andrew W. Steiner

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

  ───────────────────────────────────────────────────────────────────
"""

import ctypes
from abc import abstractmethod
from o2sclpy.utils import force_bytes
import o2sclpy.doc_data

from o2sclpy.base import *
from o2sclpy.other import *

class hdf_file:
    """
    Python interface for O2scl class ``hdf_file``,
    See
    https://awsteiner.org/code/o2scl/html/class/hdf_file.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class hdf_file

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_create_hdf_file
            f.restype=ctypes.c_void_p
            f.argtypes=[]
            self._ptr=f()
        else:
            self._ptr=pointer
            self._owner=False
        self._link=o2sclpy.doc_data.top_linker
        return

    def __del__(self):
        """
        Delete function for class hdf_file
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_hdf_free_hdf_file
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class hdf_file
        
        Returns: hdf_file object
        """

        new_obj=type(self)(self._ptr)
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
        | *fname*: byte array
        | *write_access* =false: ``bool``
        | *err_on_fail* =true: ``bool``
        """
        s_fname=o2sclpy.std_string()
        s_fname.init_bytes(force_bytes_string(fname))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_open
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool,ctypes.c_bool]
        func(self._ptr,s_fname._ptr,write_access,err_on_fail)
        return

    def open_or_create(self,fname):
        """
        | Parameters:
        | *fname*: byte array
        """
        s_fname=o2sclpy.std_string()
        s_fname.init_bytes(force_bytes_string(fname))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_open_or_create
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_fname._ptr)
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
        | *name*: byte array
        | Returns: a Python int, a Python obj
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_getc
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_char)]
        c_conv=ctypes.c_char(0)
        ret=func(self._ptr,s_name._ptr,ctypes.byref(c_conv))
        return ret,c_conv.value

    def getd(self,name):
        """
        | Parameters:
        | *name*: byte array
        | Returns: a Python int, a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_double)]
        d_conv=ctypes.c_double(0)
        ret=func(self._ptr,s_name._ptr,ctypes.byref(d_conv))
        return ret,d_conv.value

    def geti(self,name):
        """
        | Parameters:
        | *name*: byte array
        | Returns: a Python int, a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
        i_conv=ctypes.c_int(0)
        ret=func(self._ptr,s_name._ptr,ctypes.byref(i_conv))
        return ret,i_conv.value

    def get_szt(self,name):
        """
        | Parameters:
        | *name*: byte array
        | Returns: a Python int, a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_szt
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t)]
        u_conv=ctypes.c_size_t(0)
        ret=func(self._ptr,s_name._ptr,ctypes.byref(u_conv))
        return ret,u_conv.value

    def gets(self,name,s):
        """
        | Parameters:
        | *name*: byte array
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,s._ptr)
        return ret

    def gets_var(self,name,s):
        """
        | Parameters:
        | *name*: byte array
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_var
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,s._ptr)
        return ret

    def gets_fixed(self,name,s):
        """
        | Parameters:
        | *name*: byte array
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_fixed
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,s._ptr)
        return ret

    def gets_def_fixed(self,name,deft,s):
        """
        | Parameters:
        | *name*: byte array
        | *deft*: byte array
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        s_deft=o2sclpy.std_string()
        s_deft.init_bytes(force_bytes_string(deft))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_def_fixed
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,s_deft._ptr,s._ptr)
        return ret

    def setc(self,name,c):
        """
        | Parameters:
        | *name*: byte array
        | *c*: ``char``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_setc
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char]
        func(self._ptr,s_name._ptr,c)
        return

    def setd(self,name,d):
        """
        | Parameters:
        | *name*: byte array
        | *d*: ``double``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_setd
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,s_name._ptr,d)
        return

    def seti(self,name,i):
        """
        | Parameters:
        | *name*: byte array
        | *i*: ``int``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_seti
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,s_name._ptr,i)
        return

    def set_szt(self,name,u):
        """
        | Parameters:
        | *name*: byte array
        | *u*: ``size_t``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_szt
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,s_name._ptr,u)
        return

    def sets(self,name,s):
        """
        | Parameters:
        | *name*: byte array
        | *s*: byte array
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        s_s=o2sclpy.std_string()
        s_s.init_bytes(force_bytes_string(s))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_sets
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_name._ptr,s_s._ptr)
        return

    def sets_fixed(self,name,s):
        """
        | Parameters:
        | *name*: byte array
        | *s*: byte array
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        s_s=o2sclpy.std_string()
        s_s.init_bytes(force_bytes_string(s))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_sets_fixed
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_name._ptr,s_s._ptr)
        return

    def getd_vec(self,name,v):
        """
        | Parameters:
        | *name*: byte array
        | *v*: :class:`std_vector` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,v._ptr)
        return ret

    def geti_vec(self,name,v):
        """
        | Parameters:
        | *name*: byte array
        | *v*: :class:`std_vector_int` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,v._ptr)
        return ret

    def get_szt_vec(self,name,v):
        """
        | Parameters:
        | *name*: byte array
        | *v*: :class:`std_vector_size_t` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_szt_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,v._ptr)
        return ret

    def gets_vec_copy(self,name,s):
        """
        | Parameters:
        | *name*: byte array
        | *s*: :class:`std_vector_string` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_vec_copy
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,s._ptr)
        return ret

    def setd_vec(self,name,v):
        """
        | Parameters:
        | *name*: byte array
        | *v*: :class:`std_vector` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_setd_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,v._ptr)
        return ret

    def seti_vec(self,name,v):
        """
        | Parameters:
        | *name*: byte array
        | *v*: :class:`std_vector_int` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_seti_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,v._ptr)
        return ret

    def set_szt_vec(self,name,v):
        """
        | Parameters:
        | *name*: byte array
        | *v*: :class:`std_vector_size_t` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_szt_vec
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,v._ptr)
        return ret

    def sets_vec_copy(self,name,s):
        """
        | Parameters:
        | *name*: byte array
        | *s*: :class:`std_vector_string` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_sets_vec_copy
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,s._ptr)
        return ret

    def getd_mat_copy(self,name,m):
        """
        | Parameters:
        | *name*: byte array
        | *m*: :class:`ublas_matrix` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd_mat_copy
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,m._ptr)
        return ret

    def geti_mat_copy(self,name,m):
        """
        | Parameters:
        | *name*: byte array
        | *m*: :class:`ublas_matrix_int` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti_mat_copy
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,m._ptr)
        return ret

    def setd_mat_copy(self,name,m):
        """
        | Parameters:
        | *name*: byte array
        | *m*: :class:`ublas_matrix` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_setd_mat_copy
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,m._ptr)
        return ret

    def seti_mat_copy(self,name,m):
        """
        | Parameters:
        | *name*: byte array
        | *m*: :class:`ublas_matrix_int` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_seti_mat_copy
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,m._ptr)
        return ret

    def getd_ten(self,name,t):
        """
        | Parameters:
        | *name*: byte array
        | *t*: :class:`tensor` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,t._ptr)
        return ret

    def geti_ten(self,name,t):
        """
        | Parameters:
        | *name*: byte array
        | *t*: :class:`tensor_int` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,t._ptr)
        return ret

    def get_szt_ten(self,name,t):
        """
        | Parameters:
        | *name*: byte array
        | *t*: :class:`tensor_size_t` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_szt_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,t._ptr)
        return ret

    def setd_ten(self,name,t):
        """
        | Parameters:
        | *name*: byte array
        | *t*: :class:`tensor` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_setd_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,t._ptr)
        return ret

    def seti_ten(self,name,t):
        """
        | Parameters:
        | *name*: byte array
        | *t*: :class:`tensor_int` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_seti_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,t._ptr)
        return ret

    def set_szt_ten(self,name,t):
        """
        | Parameters:
        | *name*: byte array
        | *t*: :class:`tensor_size_t` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_set_szt_ten
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,t._ptr)
        return ret

    def getc_def(self,name,deft):
        """
        | Parameters:
        | *name*: byte array
        | *deft*: ``char``
        | Returns: a Python int, a Python obj
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_getc_def
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char,ctypes.POINTER(ctypes.c_char)]
        c_conv=ctypes.c_char(0)
        ret=func(self._ptr,s_name._ptr,deft,ctypes.byref(c_conv))
        return ret,c_conv.value

    def getd_def(self,name,deft):
        """
        | Parameters:
        | *name*: byte array
        | *deft*: ``double``
        | Returns: a Python int, a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_getd_def
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
        d_conv=ctypes.c_double(0)
        ret=func(self._ptr,s_name._ptr,deft,ctypes.byref(d_conv))
        return ret,d_conv.value

    def geti_def(self,name,deft):
        """
        | Parameters:
        | *name*: byte array
        | *deft*: ``int``
        | Returns: a Python int, a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_geti_def
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.POINTER(ctypes.c_int)]
        i_conv=ctypes.c_int(0)
        ret=func(self._ptr,s_name._ptr,deft,ctypes.byref(i_conv))
        return ret,i_conv.value

    def get_szt_def(self,name,deft):
        """
        | Parameters:
        | *name*: byte array
        | *deft*: ``size_t``
        | Returns: a Python int, a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_hdf_file_get_szt_def
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
        u_conv=ctypes.c_size_t(0)
        ret=func(self._ptr,s_name._ptr,deft,ctypes.byref(u_conv))
        return ret,u_conv.value

    def gets_def(self,name,deft,s):
        """
        | Parameters:
        | *name*: byte array
        | *deft*: byte array
        | *s*: :class:`std_string` object
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        s_deft=o2sclpy.std_string()
        s_deft.init_bytes(force_bytes_string(deft))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_gets_def
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr,s_deft._ptr,s._ptr)
        return ret

    def find_object_by_type(self,otype,name,use_regex=False,verbose=0):
        """
        | Parameters:
        | *otype*: byte array
        | *name*: :class:`std_string` object
        | *use_regex* =false: ``bool``
        | *verbose* =0: ``int``
        | Returns: a Python int
        """
        s_otype=o2sclpy.std_string()
        s_otype.init_bytes(force_bytes_string(otype))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_find_object_by_type
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool,ctypes.c_int]
        ret=func(self._ptr,s_otype._ptr,name._ptr,use_regex,verbose)
        return ret

    def find_object_by_name(self,name,otype,use_regex=False,verbose=0):
        """
        | Parameters:
        | *name*: byte array
        | *otype*: :class:`std_string` object
        | *use_regex* =false: ``bool``
        | *verbose* =0: ``int``
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_find_object_by_name
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool,ctypes.c_int]
        ret=func(self._ptr,s_name._ptr,otype._ptr,use_regex,verbose)
        return ret

    def find_object_by_pattern(self,pattern,otype,use_regex=False,verbose=0):
        """
        | Parameters:
        | *pattern*: byte array
        | *otype*: :class:`std_string` object
        | *use_regex* =false: ``bool``
        | *verbose* =0: ``int``
        | Returns: a Python int
        """
        s_pattern=o2sclpy.std_string()
        s_pattern.init_bytes(force_bytes_string(pattern))
        # tag 7
        # tag 6
        func=self._link.o2scl.o2scl_hdf_hdf_file_find_object_by_pattern
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool,ctypes.c_int]
        ret=func(self._ptr,s_pattern._ptr,otype._ptr,use_regex,verbose)
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
    Python interface for O2scl class ``acol_manager``,
    See
    https://awsteiner.org/code/o2scl/html/class/acol_manager.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class acol_manager

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_create_acol_manager
            f.restype=ctypes.c_void_p
            f.argtypes=[]
            self._ptr=f()
        else:
            self._ptr=pointer
            self._owner=False
        self._link=o2sclpy.doc_data.top_linker
        return

    def __del__(self):
        """
        Delete function for class acol_manager
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_hdf_free_acol_manager
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class acol_manager
        
        Returns: acol_manager object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def get_env_var_name(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_env_var_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_env_var_name(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_env_var_name
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_cl(self):
        """
        Get object of type :class:`cli`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_cl
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=cli(ptr)
        return obj

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

    def get_def_args(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_def_args
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_def_args(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_def_args
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_type(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_type
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_type(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_table_obj(self):
        """
        Get object of type :class:`table_units<>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_table_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=table_units(ptr)
        return obj

    def set_table_obj(self,value):
        """
        Set object of type :class:`table_units<>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_table_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_table3d_obj(self):
        """
        Get object of type :class:`table3d`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_table3d_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=table3d(ptr)
        return obj

    def set_table3d_obj(self,value):
        """
        Set object of type :class:`table3d`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_table3d_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_hist_obj(self):
        """
        Get object of type :class:`hist`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_hist_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=hist(ptr)
        return obj

    def set_hist_obj(self,value):
        """
        Set object of type :class:`hist`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_hist_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_hist_2d_obj(self):
        """
        Get object of type :class:`hist_2d`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_hist_2d_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=hist_2d(ptr)
        return obj

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

    def get_string_obj(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_string_obj
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_string_obj(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_string_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_cont_obj(self):
        """
        Get object of type :class:`std::vector<contour_line>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_cont_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=vector_contour_line(ptr)
        return obj

    def set_cont_obj(self,value):
        """
        Set object of type :class:`std::vector<contour_line>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_cont_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_ug_obj(self):
        """
        Get object of type :class:`uniform_grid<double>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_ug_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=uniform_grid<double>(ptr)
        return obj

    def set_ug_obj(self,value):
        """
        Set object of type :class:`uniform_grid<double>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_ug_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_intv_obj(self):
        """
        Get object of type :class:`std::vector<int>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_intv_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector_int(ptr)
        return obj

    def set_intv_obj(self,value):
        """
        Set object of type :class:`std::vector<int>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_intv_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_doublev_obj(self):
        """
        Get object of type :class:`std::vector<double>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_doublev_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector(ptr)
        return obj

    def set_doublev_obj(self,value):
        """
        Set object of type :class:`std::vector<double>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_doublev_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_size_tv_obj(self):
        """
        Get object of type :class:`std::vector<size_t>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_size_tv_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector_size_t(ptr)
        return obj

    def set_size_tv_obj(self,value):
        """
        Set object of type :class:`std::vector<size_t>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_size_tv_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_stringv_obj(self):
        """
        Get object of type :class:`std::vector<std::string>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_stringv_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector_string(ptr)
        return obj

    def set_stringv_obj(self,value):
        """
        Set object of type :class:`std::vector<std::string>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_stringv_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_vvstring_obj(self):
        """
        Get object of type :class:`std::vector<std::vector<std::string>>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_vvstring_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=vec_vec_string(ptr)
        return obj

    def set_vvstring_obj(self,value):
        """
        Set object of type :class:`std::vector<std::vector<std::string>>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_vvstring_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_vvdouble_obj(self):
        """
        Get object of type :class:`std::vector<std::vector<double>>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_vvdouble_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector_vector(ptr)
        return obj

    def set_vvdouble_obj(self,value):
        """
        Set object of type :class:`std::vector<std::vector<double>>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_vvdouble_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_tensor_obj(self):
        """
        Get object of type :class:`tensor<>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_tensor_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=tensor(ptr)
        return obj

    def set_tensor_obj(self,value):
        """
        Set object of type :class:`tensor<>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_tensor_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_tensor_int_obj(self):
        """
        Get object of type :class:`tensor<int>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_tensor_int_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=tensor_int(ptr)
        return obj

    def set_tensor_int_obj(self,value):
        """
        Set object of type :class:`tensor<int>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_tensor_int_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_tensor_size_t_obj(self):
        """
        Get object of type :class:`tensor<size_t>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_tensor_size_t_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=tensor_size_t(ptr)
        return obj

    def set_tensor_size_t_obj(self,value):
        """
        Set object of type :class:`tensor<size_t>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_tensor_size_t_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_tensor_grid_obj(self):
        """
        Get object of type :class:`tensor_grid<>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_tensor_grid_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=tensor_grid(ptr)
        return obj

    def set_tensor_grid_obj(self,value):
        """
        Set object of type :class:`tensor_grid<>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_tensor_grid_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_pdma_obj(self):
        """
        Get object of type :class:`prob_dens_mdim_amr<>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_pdma_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=prob_dens_mdim_amr(ptr)
        return obj

    def set_pdma_obj(self,value):
        """
        Set object of type :class:`prob_dens_mdim_amr<>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_pdma_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_pdmg_obj(self):
        """
        Get object of type :class:`prob_dens_mdim_gaussian<>`
        """
        func1=self._link.o2scl.o2scl_hdf_acol_manager_get_pdmg_obj
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=prob_dens_mdim_gaussian(ptr)
        return obj

    def set_pdmg_obj(self,value):
        """
        Set object of type :class:`prob_dens_mdim_gaussian<>`
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_pdmg_obj
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_command_color(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_command_color
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_command_color(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_command_color
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_type_color(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_type_color
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_type_color(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_type_color
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_param_color(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_param_color
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_param_color(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_param_color
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_help_color(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_help_color
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_help_color(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_help_color
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_exec_color(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_exec_color
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_exec_color(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_exec_color
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_url_color(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_url_color
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_url_color(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_url_color
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_default_color(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_default_color
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_default_color(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_default_color
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_color_spec(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_get_color_spec
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_color_spec(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_set_color_spec
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def help_found(self,arg1,arg2):
        """
        | Parameters:
        | *arg1*: byte array
        | *arg2*: byte array
        | Returns: a Python boolean
        """
        s_arg1=o2sclpy.std_string()
        s_arg1.init_bytes(force_bytes_string(arg1))
        # tag 7
        s_arg2=o2sclpy.std_string()
        s_arg2.init_bytes(force_bytes_string(arg2))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_acol_manager_help_found
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_arg1._ptr,s_arg2._ptr)
        return ret

    def run_empty(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_run_empty
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def validate_interp_type(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_validate_interp_type
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def parse_vec_string(self,args):
        """
        | Parameters:
        | *args*: :class:`std_vector_string` object
        """
        func=self._link.o2scl.o2scl_hdf_acol_manager_parse_vec_string
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,args._ptr)
        return

    def command_add(self,new_type):
        """
        | Parameters:
        | *new_type*: byte array
        """
        s_new_type=o2sclpy.std_string()
        s_new_type.init_bytes(force_bytes_string(new_type))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_acol_manager_command_add
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_new_type._ptr)
        return

    def command_del(self,ltype):
        """
        | Parameters:
        | *ltype*: byte array
        """
        s_ltype=o2sclpy.std_string()
        s_ltype.init_bytes(force_bytes_string(ltype))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_acol_manager_command_del
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_ltype._ptr)
        return


class cloud_file:
    """
    Python interface for O2scl class ``cloud_file``,
    See
    https://awsteiner.org/code/o2scl/html/class/cloud_file.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class cloud_file

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_create_cloud_file
            f.restype=ctypes.c_void_p
            f.argtypes=[]
            self._ptr=f()
        else:
            self._ptr=pointer
            self._owner=False
        self._link=o2sclpy.doc_data.top_linker
        return

    def __del__(self):
        """
        Delete function for class cloud_file
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_hdf_free_cloud_file
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class cloud_file
        
        Returns: cloud_file object
        """

        new_obj=type(self)(self._ptr)
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
        | *file*: byte array
        | *url*: byte array
        | *dir* ="": byte array
        | Returns: a Python int
        """
        s_file=o2sclpy.std_string()
        s_file.init_bytes(force_bytes_string(file))
        # tag 7
        s_url=o2sclpy.std_string()
        s_url.init_bytes(force_bytes_string(url))
        # tag 7
        s_dir=o2sclpy.std_string()
        s_dir.init_bytes(force_bytes_string(dir))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_file
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_file._ptr,s_url._ptr,s_dir._ptr)
        return ret

    def get_file_hash(self,file,url,hash="",dir=""):
        """
        | Parameters:
        | *file*: byte array
        | *url*: byte array
        | *hash* ="": byte array
        | *dir* ="": byte array
        | Returns: a Python int
        """
        s_file=o2sclpy.std_string()
        s_file.init_bytes(force_bytes_string(file))
        # tag 7
        s_url=o2sclpy.std_string()
        s_url.init_bytes(force_bytes_string(url))
        # tag 7
        s_hash=o2sclpy.std_string()
        s_hash.init_bytes(force_bytes_string(hash))
        # tag 7
        s_dir=o2sclpy.std_string()
        s_dir.init_bytes(force_bytes_string(dir))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_cloud_file_get_file_hash
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_file._ptr,s_url._ptr,s_hash._ptr,s_dir._ptr)
        return ret

    def hdf5_open(self,hf,file,url,dir=""):
        """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *file*: byte array
        | *url*: byte array
        | *dir* ="": byte array
        | Returns: a Python int
        """
        s_file=o2sclpy.std_string()
        s_file.init_bytes(force_bytes_string(file))
        # tag 7
        s_url=o2sclpy.std_string()
        s_url.init_bytes(force_bytes_string(url))
        # tag 7
        s_dir=o2sclpy.std_string()
        s_dir.init_bytes(force_bytes_string(dir))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_cloud_file_hdf5_open
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,hf._ptr,s_file._ptr,s_url._ptr,s_dir._ptr)
        return ret

    def hdf5_open_hash(self,hf,file,url,hash="",dir=""):
        """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *file*: byte array
        | *url*: byte array
        | *hash* ="": byte array
        | *dir* ="": byte array
        | Returns: a Python int
        """
        s_file=o2sclpy.std_string()
        s_file.init_bytes(force_bytes_string(file))
        # tag 7
        s_url=o2sclpy.std_string()
        s_url.init_bytes(force_bytes_string(url))
        # tag 7
        s_hash=o2sclpy.std_string()
        s_hash.init_bytes(force_bytes_string(hash))
        # tag 7
        s_dir=o2sclpy.std_string()
        s_dir.init_bytes(force_bytes_string(dir))
        # tag 7
        func=self._link.o2scl.o2scl_hdf_cloud_file_hdf5_open_hash
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,hf._ptr,s_file._ptr,s_url._ptr,s_hash._ptr,s_dir._ptr)
        return ret


def hdf_input_table(hf,t,name=""):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_table_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_n_table(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table<>` object
        | *name*: :class:`std::string` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_n_table_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,name._ptr)
    name._owner=True
    return

def hdf_output_table(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_output_table_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_table_units(hf,t,name=""):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table_units<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_table_units_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_n_table_units(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table_units<>` object
        | *name*: :class:`std::string` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_n_table_units_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,name._ptr)
    name._owner=True
    return

def hdf_output_table_units(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table_units<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_output_table_units_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_table3d(hf,t,name=""):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table3d` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_table3d_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_n_table3d(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table3d` object
        | *name*: :class:`std::string` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_n_table3d_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,name._ptr)
    name._owner=True
    return

def hdf_output_table3d(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`table3d` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_output_table3d_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_uniform_grid(hf,t,name=""):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`uniform_grid<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_uniform_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_n_uniform_grid(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`uniform_grid<>` object
        | *name*: :class:`std::string` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_n_uniform_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,name._ptr)
    name._owner=True
    return

def hdf_output_uniform_grid(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`uniform_grid<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_output_uniform_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_tensor_grid(hf,t,name=""):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`tensor_grid<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_tensor_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_n_tensor_grid(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`tensor_grid<>` object
        | *name*: :class:`std::string` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_n_tensor_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,name._ptr)
    name._owner=True
    return

def hdf_output_tensor_grid(hf,t,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *t*: :class:`tensor_grid<>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_output_tensor_grid_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,t._ptr,s_name._ptr)
    return

def hdf_input_vector_contour_line(hf,v,name=""):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *v*: :class:`std::vector<contour_line>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_vector_contour_line_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,v._ptr,s_name._ptr)
    return

def hdf_input_n_vector_contour_line(hf,v,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *v*: :class:`std::vector<contour_line>` object
        | *name*: :class:`std::string` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_input_n_vector_contour_line_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,v._ptr,name._ptr)
    name._owner=True
    return

def hdf_output_vector_contour_line(hf,v,name):
    """
        | Parameters:
        | *hf*: :class:`hdf_file` object
        | *v*: :class:`std::vector<contour_line>` object
        | *name*: string
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_hdf_output_vector_contour_line_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(hf._ptr,v._ptr,s_name._ptr)
    return

def value_spec(spec,d,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *spec*: string
        | *d*: ``double``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_value_spec_wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(s_spec._ptr,d._ptr,verbose,err_on_fail)
    return ret

def vector_spec(spec,v,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *spec*: string
        | *v*: :class:`std::vector<double>` object
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_vector_spec_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(s_spec._ptr,v._ptr,verbose,err_on_fail)
    return ret

def strings_spec(spec,v,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *spec*: string
        | *v*: :class:`std::vector<std::string>` object
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_strings_spec_std_vector_std_string__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(s_spec._ptr,v._ptr,verbose,err_on_fail)
    return ret

def vector_spec_v(spec):
    """
        | Parameters:
        | *spec*: string
        | Returns: ``std_vector`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_vector_spec_wrapper
    func.restype=std_vector
    func.argtypes=[ctypes.c_void_p]
    ret=func(s_spec._ptr)
    return ret

def mult_vector_spec(spec,v,use_regex=False,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *spec*: string
        | *v*: :class:`std::vector<std::vector<double>>` object
        | *use_regex*: ``bool``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_hdf_mult_vector_spec_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool,ctypes.c_int,ctypes.c_bool]
    ret=func(s_spec._ptr,v._ptr,use_regex,verbose,err_on_fail)
    return ret

