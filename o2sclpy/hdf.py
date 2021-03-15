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

    def open(self,fname,write_access,err_on_fail):
        """
        | Parameters:
        | *fname*: string
        | *write_access*: ``bool``
        | *err_on_fail*: ``bool``
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

