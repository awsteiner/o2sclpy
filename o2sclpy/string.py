"""
  ───────────────────────────────────────────────────────────────────

  Copyright (C) 2020-2024, Andrew W. Steiner

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

itp_linear=1
itp_cspline=2
itp_cspline_peri=3
itp_akima=4
itp_akima_peri=5
itp_monotonic=6
itp_steffen=7
itp_nearest_neigh=8

class std_string:
    """
    Note that std_string objects are not "immutable" like Python
    strings.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class std_string

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_string
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
        Delete function for class std_string
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_string
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_string
        
        Returns: std_string object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class std_string
        
        Returns: new copy of the std_string object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_std_string
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def length(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_string_length
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_string_getitem
        func.restype=ctypes.c_char
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: ``char``
        """
        func=self._link.o2scl.o2scl_std_string_setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char]
        func(self._ptr,i,value)
        return

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_string_resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: an int
        """
        return self.length()
     
    def init_bytes(self,s):
        """
        Initialize the string from a Python bytes object
    
        | Parameters:
        | *s*: a Python bytes string
        """
    
        f=self._link.o2scl.o2scl_char_p_to_string
        # AWS, 11/23/24: Note that, in ctypes, POINTER(char) is not 
        # the same as char_p, which is a bit confusing. 
        f.argtypes=[ctypes.c_int,ctypes.POINTER(ctypes.c_char),
                    ctypes.c_void_p]
        f(ctypes.c_int(len(s)),ctypes.c_char_p(s),self._ptr)
     
        return
    
    def to_bytes(self):
        """
        Copy the string to a Python bytes object
    
        Returns: a Python bytes string
        """
    
        n=ctypes.c_int(self.length())
                             
        # AWS, 11/23/24: The function create_string_buffer()
        # is the special ctypes function to create a POINTER(char) 
        # object for use in ctypes. Note that, in ctypes,
        # POINTER(char) is not the same as char_p, which is a bit
        # confusing.
     
        b=ctypes.create_string_buffer(self.length())
        f=self._link.o2scl.o2scl_string_to_char_p
        f.argtypes=[ctypes.c_void_p,
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_char)]
        f(self._ptr,ctypes.byref(n),b)
     
        return str(b.value)

