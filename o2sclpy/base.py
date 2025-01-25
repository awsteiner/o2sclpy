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
import numpy

from o2sclpy.string import *

itp_linear=1
itp_cspline=2
itp_cspline_peri=3
itp_akima=4
itp_akima_peri=5
itp_monotonic=6
itp_steffen=7
itp_nearest_neigh=8

def force_bytes_string(obj):
    """
    This function returns the bytes object corresponding to ``obj``
    in case it is a string using UTF-8. 
    """
    if (isinstance(obj,numpy.bytes_)==True or
        isinstance(obj,bytes)==True):
        return obj
    if isinstance(obj,o2sclpy.base.std_string):
        return obj.to_bytes()
    return bytes(obj,'utf-8')

class std_vector:
    """
    Python interface for C++ class ``std::vector<double>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class std_vector

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_vector_double_
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
        Delete function for class std_vector
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector
        
        Returns: std_vector object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class std_vector
        
        Returns: new copy of the std_vector object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_std_vector_double_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_double__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_double__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: ``double``
        """
        func=self._link.o2scl.o2scl_std_vector_double__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,i,value)
        return

    def push_back(self,x):
        """
        | Parameters:
        | *x*: ``double``
        """
        func=self._link.o2scl.o2scl_std_vector_double__push_back
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,x)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()
    
    def to_numpy(self):
        """
        Copy the vector to a numpy array
    
        Returns: a one-dimensional ``numpy`` array
        """
        ret=numpy.zeros((self.size()))
        for i in range(0,self.size()):
            ret[i]=self.__getitem__(i)
        return ret
    
    def append(self,value):
        """
        Add an element to the end of the vector
        """
        self.push_back(value)
        return
    
    def from_list(self,lst):
        """
        Set the vector with a python list
        """
        self.resize(len(lst))
        for i in range(0,len(lst)):
            self[i]=lst[i]
        return
                 
    def erase(self,index):
        """
        Erase item at specified index
        """
        n=self.size()
        v2=self.deepcopy()
        self.resize(n-1)
        for i in range(0,n-1):
            if i<index:
                self[i]=v2[i]
            else:
                self[i]=v2[i+1]
        return

class std_vector_int:
    """
    Python interface for C++ class ``std::vector<int>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class std_vector_int

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_vector_int_
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
        Delete function for class std_vector_int
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_int_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_int
        
        Returns: std_vector_int object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class std_vector_int
        
        Returns: new copy of the std_vector_int object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_std_vector_int_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_int__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_int__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_int__getitem
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: ``int``
        """
        func=self._link.o2scl.o2scl_std_vector_int__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_int]
        func(self._ptr,i,value)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()
    
    def to_numpy(self):
        """
        Copy the vector to a numpy array
    
        Returns: a one-dimensional ``numpy`` array with dtype ``int32``
        """
        ret=numpy.zeros((self.size()),dtype=numpy.int32)
        for i in range(0,self.size()):
            ret[i]=self.__getitem__(i)
        return ret

class std_vector_size_t:
    """
    Python interface for C++ class ``std::vector<size_t>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class std_vector_size_t

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_vector_size_t_
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
        Delete function for class std_vector_size_t
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_size_t_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_size_t
        
        Returns: std_vector_size_t object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class std_vector_size_t
        
        Returns: new copy of the std_vector_size_t object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_std_vector_size_t_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_size_t__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_size_t__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_size_t__getitem
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_size_t__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,i,value)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()
    
    def to_numpy(self):
        """
        Copy the vector to a numpy array
    
        Returns: a one-dimensional ``numpy`` array with dtype ``uint64``
        """
        ret=numpy.zeros((self.size()),dtype=numpy.uint64)
        for i in range(0,self.size()):
            ret[i]=self.__getitem__(i)
        return ret
     
    def init_py(self,v):
        """
        Initialize the vector from a python array
        """
        self.resize(len(v))
        for i in range(0,len(v)):
            self.__setitem__(i,v[i])
        return
    def __str__(self):
        """
        Desc
        """
        s='('
        for i in range(0,len(self)):
            if i!=len(self)-1:
                s=s+str(self[i])+','
            else:
                s=s+str(self[i])
        s=s+')'
        return s
        

class std_vector_string:
    """
    Python interface for C++ class ``std::vector<std::string>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class std_vector_string

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_vector_std_string_
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
        Delete function for class std_vector_string
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_std_string_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_string
        
        Returns: std_vector_string object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class std_vector_string
        
        Returns: new copy of the std_vector_string object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_std_vector_std_string_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_std_string__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_std_string__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def push_back(self,x):
        """
        | Parameters:
        | *x*: byte array
        """
        s_x=o2sclpy.std_string()
        s_x.init_bytes(force_bytes_string(x))
        # tag 7
        func=self._link.o2scl.o2scl_std_vector_std_string__push_back
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_x._ptr)
        return

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_std_vector_std_string__getitem
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: Python bytes object
        """
        func=self._link.o2scl.o2scl_std_vector_std_string__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        s=std_string()
        s.init_bytes(value)
        func(self._ptr,i,s._ptr)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()
    
    def append(self,value):
        """
        Add an element to the end of the vector
        """
        self.push_back(value)
        return
    
    def set_list(self,ls):
        """
        Set the object from a python list
        """
        self.resize(len(ls))
        for i in range(0,len(ls)):
            self[i]=force_bytes(ls[i])
        return
    
    def to_list(self):
        """
        Set the object from a python list
        """
        ret=[]
        for i in range(0,self.size()):
            ret.append(self[i])
        return ret

class ublas_vector:
    """
    Python interface for C++ class ``boost::numeric::ublas::vector<double>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class ublas_vector

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_boost_numeric_ublas_vector_double_
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
        Delete function for class ublas_vector
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_boost_numeric_ublas_vector_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ublas_vector
        
        Returns: ublas_vector object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class ublas_vector
        
        Returns: new copy of the ublas_vector object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_boost_numeric_ublas_vector_double_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_double__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_double__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def __getitem__(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: ``double``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_double__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,i,value)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()
    
    def to_numpy(self):
        """
        Copy the vector to a numpy array
    
        Returns: a one-dimensional ``numpy`` array
        """
        ret=numpy.zeros((self.size()))
        for i in range(0,self.size()):
            ret[i]=self.__getitem__(i)
        return ret

class ublas_vector_int:
    """
    Python interface for C++ class ``boost::numeric::ublas::vector<int>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class ublas_vector_int

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_boost_numeric_ublas_vector_int_
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
        Delete function for class ublas_vector_int
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_boost_numeric_ublas_vector_int_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ublas_vector_int
        
        Returns: ublas_vector_int object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class ublas_vector_int
        
        Returns: new copy of the ublas_vector_int object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_boost_numeric_ublas_vector_int_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_int__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_int__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def __getitem__(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_int__getitem
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: ``int``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_vector_int__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_int]
        func(self._ptr,i,value)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()
    
    def to_numpy(self):
        """
        Copy the vector to a numpy array
    
        Returns: a one-dimensional ``numpy`` array
        """
        ret=numpy.zeros((self.size()),dtype=numpy.intc)
        for i in range(0,self.size()):
            ret[i]=self.__getitem__(i)
        return ret

class ublas_matrix:
    """
    Python interface for C++ class ``boost::numeric::ublas::matrix<double>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class ublas_matrix

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_boost_numeric_ublas_matrix_double_
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
        Delete function for class ublas_matrix
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_boost_numeric_ublas_matrix_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ublas_matrix
        
        Returns: ublas_matrix object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class ublas_matrix
        
        Returns: new copy of the ublas_matrix object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_boost_numeric_ublas_matrix_double_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def size1(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_double__size1
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def size2(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_double__size2
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def resize(self,m,n):
        """
        | Parameters:
        | *m*: ``size_t``
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_double__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,m,n)
        return

    def __getitem__(self,matrix_tuple):
        """
        | Parameters:
        | *m*: ``size_t``
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        m,n=matrix_tuple
        ret=func(self._ptr,m,n)
        return ret

    def __setitem__(self,matrix_tuple,value):
        m,n=matrix_tuple
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_double__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,m,n,value)
        return

    def to_numpy(self):
        """
        Copy the vector to a numpy matrix
    
        Returns: a two-dimensional ``numpy`` array, with dimension
        ``size1(),size2()``.
        """
        ret=numpy.zeros((self.size1(),self.size2()))
        for i in range(0,self.size1()):
            for j in range(0,self.size2()):
                ret[i,j]=self.__getitem__((i,j))
        return ret

class ublas_matrix_int:
    """
    Python interface for C++ class ``boost::numeric::ublas::matrix<int>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class ublas_matrix_int

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_boost_numeric_ublas_matrix_int_
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
        Delete function for class ublas_matrix_int
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_boost_numeric_ublas_matrix_int_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ublas_matrix_int
        
        Returns: ublas_matrix_int object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class ublas_matrix_int
        
        Returns: new copy of the ublas_matrix_int object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_boost_numeric_ublas_matrix_int_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def size1(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_int__size1
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def size2(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_int__size2
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def resize(self,m,n):
        """
        | Parameters:
        | *m*: ``size_t``
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_int__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,m,n)
        return

    def __getitem__(self,matrix_tuple):
        """
        | Parameters:
        | *m*: ``size_t``
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_int__getitem
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        m,n=matrix_tuple
        ret=func(self._ptr,m,n)
        return ret

    def __setitem__(self,matrix_tuple,value):
        m,n=matrix_tuple
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_int__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_int]
        func(self._ptr,m,n,value)
        return

    def to_numpy(self):
        """
        Copy the ublas matrix to a numpy matrix
    
        Returns: a two-dimensional ``numpy`` array, with dimension
        ``size1(),size2()``.
        """
        ret=numpy.zeros(self.size1(),self.size2(),dtype=numpy.intc)
        for i in range(0,self.size1()):
            for j in range(0,self.size2()):
                ret[i,j]=self.__getitem__((i,j))
        return ret

class std_vector_vector:
    """
    Python interface for C++ class ``std::vector<std::vector<double>>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class std_vector_vector

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_vector_std_vector_double_
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
        Delete function for class std_vector_vector
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_std_vector_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_vector
        
        Returns: std_vector_vector object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class std_vector_vector
        
        Returns: new copy of the std_vector_vector object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_std_vector_std_vector_double_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_double__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_double__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        | Returns: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_double__getitem
        n_=ctypes.c_int(0)
        ptr_=ctypes.POINTER(ctypes.c_double)()
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),ctypes.POINTER(ctypes.c_int)]
        func(self._ptr,n,ctypes.byref(ptr_),ctypes.byref(n_))
        ret=numpy.ctypeslib.as_array(ptr_,shape=(n_.value,))
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: Python array
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_double__setitem
        sv=std_vector()
        sv.resize(len(value))
        for j in range(0,len(value)):
            sv[j]=value[j]
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,i,sv._ptr)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()

class vec_vec_string:
    """
    Python interface for C++ class ``std::vector<std::vector<std::string>>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class vec_vec_string

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_vector_std_vector_std_string_
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
        Delete function for class vec_vec_string
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_std_vector_std_string_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class vec_vec_string
        
        Returns: vec_vec_string object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class vec_vec_string
        
        Returns: new copy of the vec_vec_string object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_std_vector_std_vector_std_string_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_std_string__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_std_string__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        | Returns: std_vector_string object
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_std_string__getitem
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        vstrt=std_vector_string(ret)
        return vstrt

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: std_vector_string object
        """
        func=self._link.o2scl.o2scl_std_vector_std_vector_std_string__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,i,value._ptr)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()

class std_complex:
    """
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
        
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class std_complex

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_std_complex_double_
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
        Delete function for class std_complex
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_complex_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_complex
        
        Returns: std_complex object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def real(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_std_complex_double__real
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def real_set(self,value):
        """
        | Parameters:
        | *value*: ``double``
        """
        func=self._link.o2scl.o2scl_std_complex_double__real_set
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def imag(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_std_complex_double__imag
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def imag_set(self,value):
        """
        | Parameters:
        | *value*: ``double``
        """
        func=self._link.o2scl.o2scl_std_complex_double__imag_set
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @classmethod
    def init(cls,re,im):
        """
        Constructor-like class method for std::complex<double> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_std_complex_double__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double]
        return cls(f(re,im))

    def to_python(self):
        """
        Convert to a python complex number
    
        Returns: a python complex number
        """
        ret=self.real()+self.imag()*1j
        return ret

class lib_settings_class:
    """
    Python interface for O₂scl class ``lib_settings_class``,
    see
    https://awsteiner.org/code/o2scl/html/class/lib_settings_class.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class lib_settings_class

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_lib_settings_class
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
        Delete function for class lib_settings_class
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_lib_settings_class
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class lib_settings_class
        
        Returns: lib_settings_class object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def get_data_dir(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_data_dir
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def set_data_dir(self,dir):
        """
        | Parameters:
        | *dir*: byte array
        | Returns: a Python int
        """
        s_dir=o2sclpy.std_string()
        s_dir.init_bytes(force_bytes_string(dir))
        # tag 7
        func=self._link.o2scl.o2scl_lib_settings_class_set_data_dir
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_dir._ptr)
        return ret

    def get_doc_dir(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_doc_dir
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def set_doc_dir(self,dir):
        """
        | Parameters:
        | *dir*: byte array
        | Returns: a Python int
        """
        s_dir=o2sclpy.std_string()
        s_dir.init_bytes(force_bytes_string(dir))
        # tag 7
        func=self._link.o2scl.o2scl_lib_settings_class_set_doc_dir
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_dir._ptr)
        return ret

    def openmp_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_openmp_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def readline_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_readline_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def ncurses_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_ncurses_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def armadillo_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_armadillo_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def eigen_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_eigen_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def fftw_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_fftw_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def hdf5_compression_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_hdf5_compression_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def system_type(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_system_type
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def range_check(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_range_check
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def time_compiled(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_time_compiled
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def date_compiled(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_date_compiled
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def o2scl_version(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_o2scl_version
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def config_h_report(self):
        """
        """
        func=self._link.o2scl.o2scl_lib_settings_class_config_h_report
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def get_convert_units(self):
        """
        | Returns: :class:`convert_units` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_convert_units
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        ret2=convert_units(ret)
        return ret2


class table:
    """
    Python interface for O2scl class ``table``,
    see
    https://awsteiner.org/code/o2scl/html/class/table.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class table

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_table_
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
        Delete function for class table
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_table_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class table
        
        Returns: table object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class table
        
        Returns: new copy of the table object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_table_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def __getitem__(self,col):
        """
        | Parameters:
        | *col*: byte array
        | Returns: :class:`std_vector` object
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        func=self._link.o2scl.o2scl_table__getitem
        n_=ctypes.c_int(0)
        ptr_=ctypes.POINTER(ctypes.c_double)()
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),ctypes.POINTER(ctypes.c_int)]
        func(self._ptr,s_col._ptr,ctypes.byref(ptr_),ctypes.byref(n_))
        ret=numpy.ctypeslib.as_array(ptr_,shape=(n_.value,))
        return ret

    def set(self,col,row,val):
        """
        | Parameters:
        | *col*: byte array
        | *row*: ``size_t``
        | *val*: ``double``
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        func=self._link.o2scl.o2scl_table__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,s_col._ptr,row,val)
        return

    def get(self,col,row):
        """
        | Parameters:
        | *col*: byte array
        | *row*: ``size_t``
        | Returns: a Python float
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        func=self._link.o2scl.o2scl_table__get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,s_col._ptr,row)
        return ret

    def get_ncolumns(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table__get_ncolumns
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_nlines(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table__get_nlines
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_nlines(self,lines):
        """
        | Parameters:
        | *lines*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__set_nlines
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,lines)
        return

    def get_maxlines(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table__get_maxlines
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_maxlines(self,llines):
        """
        | Parameters:
        | *llines*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__set_maxlines
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,llines)
        return

    def set_nlines_auto(self,il):
        """
        | Parameters:
        | *il*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__set_nlines_auto
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,il)
        return

    def inc_maxlines(self,llines):
        """
        | Parameters:
        | *llines*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__inc_maxlines
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,llines)
        return

    def new_column(self,col):
        """
        | Parameters:
        | *col*: byte array
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        func=self._link.o2scl.o2scl_table__new_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_col._ptr)
        return

    def get_column_name(self,icol):
        """
        | Parameters:
        | *icol*: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_table__get_column_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,icol)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def rename_column(self,src,dest):
        """
        | Parameters:
        | *src*: byte array
        | *dest*: byte array
        """
        s_src=o2sclpy.std_string()
        s_src.init_bytes(force_bytes_string(src))
        # tag 7
        s_dest=o2sclpy.std_string()
        s_dest.init_bytes(force_bytes_string(dest))
        # tag 7
        func=self._link.o2scl.o2scl_table__rename_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_src._ptr,s_dest._ptr)
        return

    def delete_column(self,col):
        """
        | Parameters:
        | *col*: byte array
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        func=self._link.o2scl.o2scl_table__delete_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_col._ptr)
        return

    def get_sorted_name(self,icol):
        """
        | Parameters:
        | *icol*: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_table__get_sorted_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,icol)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def init_column(self,scol,val):
        """
        | Parameters:
        | *scol*: byte array
        | *val*: ``double``
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__init_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,s_scol._ptr,val)
        return

    def is_column(self,scol):
        """
        | Parameters:
        | *scol*: byte array
        | Returns: a Python boolean
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__is_column
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_scol._ptr)
        return ret

    def lookup_column(self,scol):
        """
        | Parameters:
        | *scol*: byte array
        | Returns: a Python int
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__lookup_column
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_scol._ptr)
        return ret

    def copy_column(self,src,dest):
        """
        | Parameters:
        | *src*: byte array
        | *dest*: byte array
        """
        s_src=o2sclpy.std_string()
        s_src.init_bytes(force_bytes_string(src))
        # tag 7
        s_dest=o2sclpy.std_string()
        s_dest.init_bytes(force_bytes_string(dest))
        # tag 7
        func=self._link.o2scl.o2scl_table__copy_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_src._ptr,s_dest._ptr)
        return

    def add_col_from_table(self,source,src_index,src_col,dest_index,dest_col):
        """
        | Parameters:
        | *source*: :class:`table<>` object
        | *src_index*: byte array
        | *src_col*: byte array
        | *dest_index*: byte array
        | *dest_col*: byte array
        """
        s_src_index=o2sclpy.std_string()
        s_src_index.init_bytes(force_bytes_string(src_index))
        # tag 7
        s_src_col=o2sclpy.std_string()
        s_src_col.init_bytes(force_bytes_string(src_col))
        # tag 7
        s_dest_index=o2sclpy.std_string()
        s_dest_index.init_bytes(force_bytes_string(dest_index))
        # tag 7
        s_dest_col=o2sclpy.std_string()
        s_dest_col.init_bytes(force_bytes_string(dest_col))
        # tag 7
        func=self._link.o2scl.o2scl_table__add_col_from_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,source._ptr,s_src_index._ptr,s_src_col._ptr,s_dest_index._ptr,s_dest_col._ptr)
        return

    def insert_table(self,source,src_index,allow_extrap,dest_index):
        """
        | Parameters:
        | *source*: :class:`table<>` object
        | *src_index*: byte array
        | *allow_extrap*: ``bool``
        | *dest_index*: byte array
        """
        s_src_index=o2sclpy.std_string()
        s_src_index.init_bytes(force_bytes_string(src_index))
        # tag 7
        s_dest_index=o2sclpy.std_string()
        s_dest_index.init_bytes(force_bytes_string(dest_index))
        # tag 7
        func=self._link.o2scl.o2scl_table__insert_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool,ctypes.c_void_p]
        func(self._ptr,source._ptr,s_src_index._ptr,allow_extrap,s_dest_index._ptr)
        return

    def add_table(self,source):
        """
        | Parameters:
        | *source*: :class:`table<>` object
        """
        func=self._link.o2scl.o2scl_table__add_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,source._ptr)
        return

    def new_row(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__new_row
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def copy_row(self,src,dest):
        """
        | Parameters:
        | *src*: ``size_t``
        | *dest*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__copy_row
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,src,dest)
        return

    def delete_row(self,scol,val):
        """
        | Parameters:
        | *scol*: byte array
        | *val*: ``double``
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__delete_row
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,s_scol._ptr,val)
        return

    def delete_rows_func(self,func):
        """
        | Parameters:
        | *func*: byte array
        """
        s_func=o2sclpy.std_string()
        s_func.init_bytes(force_bytes_string(func))
        # tag 7
        func=self._link.o2scl.o2scl_table__delete_rows_func
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_func._ptr)
        return

    def delete_rows_ends(self,row_start,row_end):
        """
        | Parameters:
        | *row_start*: ``size_t``
        | *row_end*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__delete_rows_ends
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,row_start,row_end)
        return

    def line_of_names(self,names):
        """
        | Parameters:
        | *names*: byte array
        """
        s_names=o2sclpy.std_string()
        s_names.init_bytes(force_bytes_string(names))
        # tag 7
        func=self._link.o2scl.o2scl_table__line_of_names
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_names._ptr)
        return

    def line_of_data_vector(self,data):
        """
        | Parameters:
        | *data*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_table__line_of_data
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,data._ptr)
        return

    def insert_row(self,nv,data,row):
        """
        | Parameters:
        | *nv*: ``size_t``
        | *data*: :class:`std_vector` object
        | *row*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__insert_row
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,nv,data._ptr,row)
        return

    def ordered_lookup(self,scol,val):
        """
        | Parameters:
        | *scol*: byte array
        | *val*: ``double``
        | Returns: a Python int
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__ordered_lookup
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,s_scol._ptr,val)
        return ret

    def lookup(self,scol,val):
        """
        | Parameters:
        | *scol*: byte array
        | *val*: ``double``
        | Returns: a Python int
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__lookup
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,s_scol._ptr,val)
        return ret

    def lookup_val(self,scol,val,scol2):
        """
        | Parameters:
        | *scol*: byte array
        | *val*: ``double``
        | *scol2*: byte array
        | Returns: a Python int
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        s_scol2=o2sclpy.std_string()
        s_scol2.init_bytes(force_bytes_string(scol2))
        # tag 7
        func=self._link.o2scl.o2scl_table__lookup_val
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,s_scol._ptr,val,s_scol2._ptr)
        return ret

    def set_interp_type(self,interp_type):
        """
        | Parameters:
        | *interp_type*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table__set_interp_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,interp_type)
        return

    def get_interp_type(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table__get_interp_type
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def interp(self,sx,x0,sy):
        """
        | Parameters:
        | *sx*: byte array
        | *x0*: ``double``
        | *sy*: byte array
        | Returns: a Python float
        """
        s_sx=o2sclpy.std_string()
        s_sx.init_bytes(force_bytes_string(sx))
        # tag 7
        s_sy=o2sclpy.std_string()
        s_sy.init_bytes(force_bytes_string(sy))
        # tag 7
        func=self._link.o2scl.o2scl_table__interp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,s_sx._ptr,x0,s_sy._ptr)
        return ret

    def interp_index(self,ix,x0,iy):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *x0*: ``double``
        | *iy*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_table__interp_index
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double,ctypes.c_size_t]
        ret=func(self._ptr,ix,x0,iy)
        return ret

    def deriv_col(self,x,y,yp):
        """
        | Parameters:
        | *x*: byte array
        | *y*: byte array
        | *yp*: byte array
        """
        s_x=o2sclpy.std_string()
        s_x.init_bytes(force_bytes_string(x))
        # tag 7
        s_y=o2sclpy.std_string()
        s_y.init_bytes(force_bytes_string(y))
        # tag 7
        s_yp=o2sclpy.std_string()
        s_yp.init_bytes(force_bytes_string(yp))
        # tag 7
        func=self._link.o2scl.o2scl_table__deriv_col
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_x._ptr,s_y._ptr,s_yp._ptr)
        return

    def deriv(self,sx,x0,sy):
        """
        | Parameters:
        | *sx*: byte array
        | *x0*: ``double``
        | *sy*: byte array
        | Returns: a Python float
        """
        s_sx=o2sclpy.std_string()
        s_sx.init_bytes(force_bytes_string(sx))
        # tag 7
        s_sy=o2sclpy.std_string()
        s_sy.init_bytes(force_bytes_string(sy))
        # tag 7
        func=self._link.o2scl.o2scl_table__deriv
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,s_sx._ptr,x0,s_sy._ptr)
        return ret

    def deriv_index(self,ix,x0,iy):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *x0*: ``double``
        | *iy*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_table__deriv_index
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double,ctypes.c_size_t]
        ret=func(self._ptr,ix,x0,iy)
        return ret

    def deriv2_col(self,x,y,yp):
        """
        | Parameters:
        | *x*: byte array
        | *y*: byte array
        | *yp*: byte array
        """
        s_x=o2sclpy.std_string()
        s_x.init_bytes(force_bytes_string(x))
        # tag 7
        s_y=o2sclpy.std_string()
        s_y.init_bytes(force_bytes_string(y))
        # tag 7
        s_yp=o2sclpy.std_string()
        s_yp.init_bytes(force_bytes_string(yp))
        # tag 7
        func=self._link.o2scl.o2scl_table__deriv2_col
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_x._ptr,s_y._ptr,s_yp._ptr)
        return

    def deriv2(self,sx,x0,sy):
        """
        | Parameters:
        | *sx*: byte array
        | *x0*: ``double``
        | *sy*: byte array
        | Returns: a Python float
        """
        s_sx=o2sclpy.std_string()
        s_sx.init_bytes(force_bytes_string(sx))
        # tag 7
        s_sy=o2sclpy.std_string()
        s_sy.init_bytes(force_bytes_string(sy))
        # tag 7
        func=self._link.o2scl.o2scl_table__deriv2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,s_sx._ptr,x0,s_sy._ptr)
        return ret

    def deriv2_index(self,ix,x0,iy):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *x0*: ``double``
        | *iy*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_table__deriv2_index
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double,ctypes.c_size_t]
        ret=func(self._ptr,ix,x0,iy)
        return ret

    def integ(self,sx,x1,x2,sy):
        """
        | Parameters:
        | *sx*: byte array
        | *x1*: ``double``
        | *x2*: ``double``
        | *sy*: byte array
        | Returns: a Python float
        """
        s_sx=o2sclpy.std_string()
        s_sx.init_bytes(force_bytes_string(sx))
        # tag 7
        s_sy=o2sclpy.std_string()
        s_sy.init_bytes(force_bytes_string(sy))
        # tag 7
        func=self._link.o2scl.o2scl_table__integ
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,s_sx._ptr,x1,x2,s_sy._ptr)
        return ret

    def integ_index(self,ix,x1,x2,iy):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *x1*: ``double``
        | *x2*: ``double``
        | *iy*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_table__integ_index
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        ret=func(self._ptr,ix,x1,x2,iy)
        return ret

    def integ_col(self,x,y,yi):
        """
        | Parameters:
        | *x*: byte array
        | *y*: byte array
        | *yi*: byte array
        """
        s_x=o2sclpy.std_string()
        s_x.init_bytes(force_bytes_string(x))
        # tag 7
        s_y=o2sclpy.std_string()
        s_y.init_bytes(force_bytes_string(y))
        # tag 7
        s_yi=o2sclpy.std_string()
        s_yi.init_bytes(force_bytes_string(yi))
        # tag 7
        func=self._link.o2scl.o2scl_table__integ_col
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_x._ptr,s_y._ptr,s_yi._ptr)
        return

    def max(self,max):
        """
        | Parameters:
        | *max*: byte array
        | Returns: a Python float
        """
        s_max=o2sclpy.std_string()
        s_max.init_bytes(force_bytes_string(max))
        # tag 7
        func=self._link.o2scl.o2scl_table__max
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_max._ptr)
        return ret

    def min(self,min):
        """
        | Parameters:
        | *min*: byte array
        | Returns: a Python float
        """
        s_min=o2sclpy.std_string()
        s_min.init_bytes(force_bytes_string(min))
        # tag 7
        func=self._link.o2scl.o2scl_table__min
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_min._ptr)
        return ret

    def zero_table(self):
        """
        """
        func=self._link.o2scl.o2scl_table__zero_table
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_table__clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear_data(self):
        """
        """
        func=self._link.o2scl.o2scl_table__clear_data
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear_table(self):
        """
        """
        func=self._link.o2scl.o2scl_table__clear_table
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear_constants(self):
        """
        """
        func=self._link.o2scl.o2scl_table__clear_constants
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def sort_table(self,scol):
        """
        | Parameters:
        | *scol*: byte array
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__sort_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_scol._ptr)
        return

    def sort_column(self,scol):
        """
        | Parameters:
        | *scol*: byte array
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__sort_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_scol._ptr)
        return

    def average_col_roll(self,col_name,window):
        """
        | Parameters:
        | *col_name*: byte array
        | *window*: ``size_t``
        """
        s_col_name=o2sclpy.std_string()
        s_col_name.init_bytes(force_bytes_string(col_name))
        # tag 7
        func=self._link.o2scl.o2scl_table__average_col_roll
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,s_col_name._ptr,window)
        return

    def average_rows(self,window,rolling):
        """
        | Parameters:
        | *window*: ``size_t``
        | *rolling*: ``bool``
        """
        func=self._link.o2scl.o2scl_table__average_rows
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_bool]
        func(self._ptr,window,rolling)
        return

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_table__is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def functions_columns(self,list):
        """
        | Parameters:
        | *list*: byte array
        """
        s_list=o2sclpy.std_string()
        s_list.init_bytes(force_bytes_string(list))
        # tag 7
        func=self._link.o2scl.o2scl_table__functions_columns
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_list._ptr)
        return

    def function_column(self,function,scol):
        """
        | Parameters:
        | *function*: byte array
        | *scol*: byte array
        """
        s_function=o2sclpy.std_string()
        s_function.init_bytes(force_bytes_string(function))
        # tag 7
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__function_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_function._ptr,s_scol._ptr)
        return

    def row_function(self,scol,row):
        """
        | Parameters:
        | *scol*: byte array
        | *row*: ``size_t``
        | Returns: a Python float
        """
        s_scol=o2sclpy.std_string()
        s_scol.init_bytes(force_bytes_string(scol))
        # tag 7
        func=self._link.o2scl.o2scl_table__row_function
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,s_scol._ptr,row)
        return ret

    def function_find_row(self,function):
        """
        | Parameters:
        | *function*: byte array
        | Returns: a Python int
        """
        s_function=o2sclpy.std_string()
        s_function.init_bytes(force_bytes_string(function))
        # tag 7
        func=self._link.o2scl.o2scl_table__function_find_row
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_function._ptr)
        return ret

    def summary(self):
        """
        """
        func=self._link.o2scl.o2scl_table__summary
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def line_of_data(self,v):
        """
        Copy ``v`` to an :class:`std_vector` object and add the line of
        data to the table
        """
        # Create a std_vector object and copy the data over
        vec=std_vector()
        vec.resize(len(v))
        for i in range(0,len(v)):
            vec[i]=v[i]
        self.line_of_data_vector(vec)
        return
                                 
    def row_to_dict(self,row):
        """
        Convert the specified row to a python dictionary
        """
        dct={}
        for i in range(0,self.get_ncolumns()):
            dct[self.get_column_name(i)]=self.get(self.get_column_name(i),
                                                  row)
        return dct

class table_units(table):
    """
    Python interface for O2scl class ``table_units``,
    see
    https://awsteiner.org/code/o2scl/html/class/table_units.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class table_units

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_table_units_
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
        Delete function for class table_units
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_table_units_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class table_units
        
        Returns: table_units object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class table_units
        
        Returns: new copy of the table_units object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_table_units_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def set_unit(self,col,unit):
        """
        | Parameters:
        | *col*: byte array
        | *unit*: byte array
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        s_unit=o2sclpy.std_string()
        s_unit.init_bytes(force_bytes_string(unit))
        # tag 7
        func=self._link.o2scl.o2scl_table_units__set_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_col._ptr,s_unit._ptr)
        return

    def get_unit(self,col):
        """
        | Parameters:
        | *col*: byte array
        | Returns: Python bytes object
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        func=self._link.o2scl.o2scl_table_units__get_unit
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_col._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def line_of_units(self,unit_line):
        """
        | Parameters:
        | *unit_line*: byte array
        """
        s_unit_line=o2sclpy.std_string()
        s_unit_line.init_bytes(force_bytes_string(unit_line))
        # tag 7
        func=self._link.o2scl.o2scl_table_units__line_of_units
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_unit_line._ptr)
        return

    def remove_unit(self,col):
        """
        | Parameters:
        | *col*: byte array
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        func=self._link.o2scl.o2scl_table_units__remove_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_col._ptr)
        return

    def convert_to_unit(self,col,unit,err_on_fail=True):
        """
        | Parameters:
        | *col*: byte array
        | *unit*: byte array
        | *err_on_fail* =True: ``bool``
        | Returns: a Python int
        """
        s_col=o2sclpy.std_string()
        s_col.init_bytes(force_bytes_string(col))
        # tag 7
        s_unit=o2sclpy.std_string()
        s_unit.init_bytes(force_bytes_string(unit))
        # tag 7
        func=self._link.o2scl.o2scl_table_units__convert_to_unit
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]
        ret=func(self._ptr,s_col._ptr,s_unit._ptr,err_on_fail)
        return ret


class uniform_grid:
    """
    Python interface for O2scl class ``uniform_grid``,
    see
    https://awsteiner.org/code/o2scl/html/class/uniform_grid.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class uniform_grid

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_uniform_grid_
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
        Delete function for class uniform_grid
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid
        
        Returns: uniform_grid object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def get_nbins(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_uniform_grid__get_nbins
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_npoints(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_uniform_grid__get_npoints
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def is_log(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_uniform_grid__is_log
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_start(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_uniform_grid__get_start
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_end(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_uniform_grid__get_end
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_width(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_uniform_grid__get_width
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_uniform_grid__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def vector(self,v):
        """
        | Parameters:
        | *v*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_uniform_grid__vector
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,v._ptr)
        return

    def to_numpy(self):
        """
        Copy the ``uniform_grid`` object to a numpy array
    
        Returns: a one-dimensional ``numpy`` array
        """
        v=std_vector()
        self.vector(v)
        ret=numpy.zeros((self.get_npoints()))
        for i in range(0,self.get_npoints()):
            ret[i]=v[i]
        return ret

class uniform_grid_end(uniform_grid):
    """
    Python interface for O2scl class ``uniform_grid_end``,
    see
    https://awsteiner.org/code/o2scl/html/class/uniform_grid_end.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class uniform_grid_end

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_uniform_grid_end_
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
        Delete function for class uniform_grid_end
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_end_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_end
        
        Returns: uniform_grid_end object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,start,end,n_bins):
        """
        Constructor-like class method for uniform_grid_end<> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_uniform_grid_end__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(f(start,end,n_bins))


class uniform_grid_width(uniform_grid):
    """
    Python interface for O2scl class ``uniform_grid_width``,
    see
    https://awsteiner.org/code/o2scl/html/class/uniform_grid_width.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class uniform_grid_width

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_uniform_grid_width_
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
        Delete function for class uniform_grid_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_width_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_width
        
        Returns: uniform_grid_width object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,start,width,n_bins):
        """
        Constructor-like class method for uniform_grid_width<> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_uniform_grid_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(f(start,width,n_bins))


class uniform_grid_end_width(uniform_grid):
    """
    Python interface for O2scl class ``uniform_grid_end_width``,
    see
    https://awsteiner.org/code/o2scl/html/class/uniform_grid_end_width.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class uniform_grid_end_width

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_uniform_grid_end_width_
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
        Delete function for class uniform_grid_end_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_end_width_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_end_width
        
        Returns: uniform_grid_end_width object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,start,end,width):
        """
        Constructor-like class method for uniform_grid_end_width<> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_uniform_grid_end_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double]
        return cls(f(start,end,width))


class uniform_grid_log_end(uniform_grid):
    """
    Python interface for O2scl class ``uniform_grid_log_end``,
    see
    https://awsteiner.org/code/o2scl/html/class/uniform_grid_log_end.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class uniform_grid_log_end

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_uniform_grid_log_end_
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
        Delete function for class uniform_grid_log_end
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_log_end_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_log_end
        
        Returns: uniform_grid_log_end object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,start,end,n_bins):
        """
        Constructor-like class method for uniform_grid_log_end<> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_uniform_grid_log_end__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(f(start,end,n_bins))


class uniform_grid_log_width(uniform_grid):
    """
    Python interface for O2scl class ``uniform_grid_log_width``,
    see
    https://awsteiner.org/code/o2scl/html/class/uniform_grid_log_width.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class uniform_grid_log_width

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_uniform_grid_log_width_
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
        Delete function for class uniform_grid_log_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_log_width_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_log_width
        
        Returns: uniform_grid_log_width object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,start,width,n_bins):
        """
        Constructor-like class method for uniform_grid_log_width<> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_uniform_grid_log_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(f(start,width,n_bins))


class uniform_grid_log_end_width(uniform_grid):
    """
    Python interface for O2scl class ``uniform_grid_log_end_width``,
    see
    https://awsteiner.org/code/o2scl/html/class/uniform_grid_log_end_width.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class uniform_grid_log_end_width

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_uniform_grid_log_end_width_
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
        Delete function for class uniform_grid_log_end_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_log_end_width_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_log_end_width
        
        Returns: uniform_grid_log_end_width object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,start,end,width):
        """
        Constructor-like class method for uniform_grid_log_end_width<> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_uniform_grid_log_end_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double]
        return cls(f(start,end,width))


class table3d:
    """
    Python interface for O₂scl class ``table3d``,
    see
    https://awsteiner.org/code/o2scl/html/class/table3d.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class table3d

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_table3d
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
        Delete function for class table3d
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_table3d
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class table3d
        
        Returns: table3d object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class table3d
        
        Returns: new copy of the table3d object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_table3d
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def set_size(self,nx,ny):
        """
        | Parameters:
        | *nx*: ``size_t``
        | *ny*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table3d_set_size
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,nx,ny)
        return

    def set_xy(self,x_name,nx,x,y_name,ny,y):
        """
        | Parameters:
        | *x_name*: byte array
        | *nx*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y_name*: byte array
        | *ny*: ``size_t``
        | *y*: :class:`std_vector` object
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_set_xy
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,s_x_name._ptr,nx,x._ptr,s_y_name._ptr,ny,y._ptr)
        return

    def set_xy_grid(self,x_name,x_grid,y_name,y_grid):
        """
        | Parameters:
        | *x_name*: byte array
        | *x_grid*: :class:`uniform_grid<double>` object
        | *y_name*: byte array
        | *y_grid*: :class:`uniform_grid<double>` object
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_set_xy_grid
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_x_name._ptr,x_grid._ptr,s_y_name._ptr,y_grid._ptr)
        return

    def set(self,ix,iy,name,val):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *iy*: ``size_t``
        | *name*: byte array
        | *val*: ``double``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_set
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,ix,iy,s_name._ptr,val)
        return

    def get(self,ix,iy,name):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *iy*: ``size_t``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p]
        ret=func(self._ptr,ix,iy,s_name._ptr)
        return ret

    def get_i(self,ix,iy,iz):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *iy*: ``size_t``
        | *iz*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_table3d_get_i
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t]
        ret=func(self._ptr,ix,iy,iz)
        return ret

    def set_i(self,ix,iy,iz,val):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *iy*: ``size_t``
        | *iz*: ``size_t``
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_table3d_set_i
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,ix,iy,iz,val)
        return

    def set_val(self,x,y,name,val):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: byte array
        | *val*: ``double``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_set_val
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,x,y,s_name._ptr,val)
        return

    def get_val(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_get_val
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,x,y,s_name._ptr)
        return ret

    def set_grid_x(self,ix,val):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_table3d_set_grid_x
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,ix,val)
        return

    def set_grid_y(self,iy,val):
        """
        | Parameters:
        | *iy*: ``size_t``
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_table3d_set_grid_y
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,iy,val)
        return

    def get_grid_x(self,ix):
        """
        | Parameters:
        | *ix*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_table3d_get_grid_x
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,ix)
        return ret

    def get_grid_y(self,iy):
        """
        | Parameters:
        | *iy*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_table3d_get_grid_y
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,iy)
        return ret

    def get_x_name(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_table3d_get_x_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def get_y_name(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_table3d_get_y_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def set_x_name(self,name):
        """
        | Parameters:
        | *name*: byte array
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_set_x_name
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_name._ptr)
        return

    def set_y_name(self,name):
        """
        | Parameters:
        | *name*: byte array
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_set_y_name
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_name._ptr)
        return

    def get_size(self):
        """
        | Parameters:
        | Returns: , a Python int, a Python int
        """
        func=self._link.o2scl.o2scl_table3d_get_size
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
        nx_conv=ctypes.c_size_t(0)
        ny_conv=ctypes.c_size_t(0)
        func(self._ptr,ctypes.byref(nx_conv),ctypes.byref(ny_conv))
        return nx_conv.value,ny_conv.value

    def get_nx(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table3d_get_nx
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_ny(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table3d_get_ny
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_nslices(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table3d_get_nslices
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def is_size_set(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_table3d_is_size_set
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def is_xy_set(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_table3d_is_xy_set
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_slice_name(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_table3d_get_slice_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def new_slice(self,slice):
        """
        | Parameters:
        | *slice*: byte array
        """
        s_slice=o2sclpy.std_string()
        s_slice.init_bytes(force_bytes_string(slice))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_new_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_slice._ptr)
        return

    def set_slice_all(self,name,val):
        """
        | Parameters:
        | *name*: byte array
        | *val*: ``double``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_set_slice_all
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,s_name._ptr,val)
        return

    def lookup_slice(self,name):
        """
        | Parameters:
        | *name*: byte array
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_lookup_slice
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr)
        return ret

    def is_slice(self,name):
        """
        | Parameters:
        | *name*: byte array
        | Returns: a Python boolean, a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_is_slice
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t)]
        ix_conv=ctypes.c_size_t(0)
        ret=func(self._ptr,s_name._ptr,ctypes.byref(ix_conv))
        return ret,ix_conv.value

    def rename_slice(self,name1,name2):
        """
        | Parameters:
        | *name1*: byte array
        | *name2*: byte array
        """
        s_name1=o2sclpy.std_string()
        s_name1.init_bytes(force_bytes_string(name1))
        # tag 7
        s_name2=o2sclpy.std_string()
        s_name2.init_bytes(force_bytes_string(name2))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_rename_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_name1._ptr,s_name2._ptr)
        return

    def copy_slice(self,name1,name2):
        """
        | Parameters:
        | *name1*: byte array
        | *name2*: byte array
        """
        s_name1=o2sclpy.std_string()
        s_name1.init_bytes(force_bytes_string(name1))
        # tag 7
        s_name2=o2sclpy.std_string()
        s_name2.init_bytes(force_bytes_string(name2))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_copy_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_name1._ptr,s_name2._ptr)
        return

    def get_slice(self,slice):
        """
        | Parameters:
        | *slice*: byte array
        | Returns: :class:`ublas_matrix` object
        """
        s_slice=o2sclpy.std_string()
        s_slice.init_bytes(force_bytes_string(slice))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_get_slice
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_slice._ptr)
        ret2=ublas_matrix(ret)
        return ret2

    def get_slice_i(self,slice):
        """
        | Parameters:
        | *slice*: byte array
        | Returns: :class:`ublas_matrix` object
        """
        s_slice=o2sclpy.std_string()
        s_slice.init_bytes(force_bytes_string(slice))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_get_slice_i
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_slice._ptr)
        ret2=ublas_matrix(ret)
        return ret2

    def lookup_x(self,val,ix):
        """
        | Parameters:
        | *val*: ``double``
        | *ix*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table3d_lookup_x
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t]
        func(self._ptr,val,ix)
        return

    def lookup_y(self,val,iy):
        """
        | Parameters:
        | *val*: ``double``
        | *iy*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table3d_lookup_y
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t]
        func(self._ptr,val,iy)
        return

    def interp(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_interp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,x,y,s_name._ptr)
        return ret

    def deriv_x(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_deriv_x
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,x,y,s_name._ptr)
        return ret

    def deriv_y(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_deriv_y
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,x,y,s_name._ptr)
        return ret

    def deriv_xy(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_deriv_xy
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,x,y,s_name._ptr)
        return ret

    def integ_x(self,x1,x2,y,name):
        """
        | Parameters:
        | *x1*: ``double``
        | *x2*: ``double``
        | *y*: ``double``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_integ_x
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,x1,x2,y,s_name._ptr)
        return ret

    def integ_y(self,x,y1,y2,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y1*: ``double``
        | *y2*: ``double``
        | *name*: byte array
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_integ_y
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,x,y1,y2,s_name._ptr)
        return ret

    def zero_table(self):
        """
        """
        func=self._link.o2scl.o2scl_table3d_zero_table
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_table3d_clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def function_matrix(self,function,mat,throw_on_err):
        """
        | Parameters:
        | *function*: byte array
        | *mat*: :class:`ublas_matrix` object
        | *throw_on_err*: ``bool``
        | Returns: a Python int
        """
        s_function=o2sclpy.std_string()
        s_function.init_bytes(force_bytes_string(function))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_function_matrix
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]
        ret=func(self._ptr,s_function._ptr,mat._ptr,throw_on_err)
        return ret

    def function_slice(self,function,slice):
        """
        | Parameters:
        | *function*: byte array
        | *slice*: byte array
        """
        s_function=o2sclpy.std_string()
        s_function.init_bytes(force_bytes_string(function))
        # tag 7
        s_slice=o2sclpy.std_string()
        s_slice.init_bytes(force_bytes_string(slice))
        # tag 7
        func=self._link.o2scl.o2scl_table3d_function_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_function._ptr,s_slice._ptr)
        return

    def summary(self):
        """
        """
        func=self._link.o2scl.o2scl_table3d_summary
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return


class index_spec:
    """
    Python interface for O₂scl class ``index_spec``,
    see
    https://awsteiner.org/code/o2scl/html/class/index_spec.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class index_spec

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_index_spec
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
        Delete function for class index_spec
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_index_spec
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class index_spec
        
        Returns: index_spec object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @property
    def type(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_index_spec_get_type
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @type.setter
    def type(self,value):
        """
        Setter function for index_spec::type .
        """
        func=self._link.o2scl.o2scl_index_spec_set_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def ix1(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_index_spec_get_ix1
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ix1.setter
    def ix1(self,value):
        """
        Setter function for index_spec::ix1 .
        """
        func=self._link.o2scl.o2scl_index_spec_set_ix1
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def ix2(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_index_spec_get_ix2
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ix2.setter
    def ix2(self,value):
        """
        Setter function for index_spec::ix2 .
        """
        func=self._link.o2scl.o2scl_index_spec_set_ix2
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def ix3(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_index_spec_get_ix3
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ix3.setter
    def ix3(self,value):
        """
        Setter function for index_spec::ix3 .
        """
        func=self._link.o2scl.o2scl_index_spec_set_ix3
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def val1(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_index_spec_get_val1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @val1.setter
    def val1(self,value):
        """
        Setter function for index_spec::val1 .
        """
        func=self._link.o2scl.o2scl_index_spec_set_val1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def val2(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_index_spec_get_val2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @val2.setter
    def val2(self,value):
        """
        Setter function for index_spec::val2 .
        """
        func=self._link.o2scl.o2scl_index_spec_set_val2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def val3(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_index_spec_get_val3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @val3.setter
    def val3(self,value):
        """
        Setter function for index_spec::val3 .
        """
        func=self._link.o2scl.o2scl_index_spec_set_val3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return


class ix_index:
    """
    Python interface for O₂scl class ``ix_index``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_index.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_index

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_index
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
        Delete function for class ix_index
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_index
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_index
        
        Returns: ix_index object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix):
        """
        Constructor-like class method for ix_index .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_index_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t]
        return cls(f(ix))


class ix_fixed:
    """
    Python interface for O₂scl class ``ix_fixed``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_fixed.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_fixed

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_fixed
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
        Delete function for class ix_fixed
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_fixed
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_fixed
        
        Returns: ix_fixed object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix,ix2):
        """
        Constructor-like class method for ix_fixed .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_fixed_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_size_t]
        return cls(f(ix,ix2))


class ix_sum:
    """
    Python interface for O₂scl class ``ix_sum``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_sum.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_sum

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_sum
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
        Delete function for class ix_sum
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_sum
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_sum
        
        Returns: ix_sum object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix):
        """
        Constructor-like class method for ix_sum .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_sum_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t]
        return cls(f(ix))


class ix_trace:
    """
    Python interface for O₂scl class ``ix_trace``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_trace.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_trace

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_trace
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
        Delete function for class ix_trace
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_trace
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_trace
        
        Returns: ix_trace object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix,ix2):
        """
        Constructor-like class method for ix_trace .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_trace_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_size_t]
        return cls(f(ix,ix2))


class ix_reverse:
    """
    Python interface for O₂scl class ``ix_reverse``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_reverse.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_reverse

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_reverse
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
        Delete function for class ix_reverse
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_reverse
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_reverse
        
        Returns: ix_reverse object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix):
        """
        Constructor-like class method for ix_reverse .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_reverse_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t]
        return cls(f(ix))


class ix_range:
    """
    Python interface for O₂scl class ``ix_range``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_range.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_range

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_range
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
        Delete function for class ix_range
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_range
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_range
        
        Returns: ix_range object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix,start,end):
        """
        Constructor-like class method for ix_range .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_range_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t]
        return cls(f(ix,start,end))


class ix_interp:
    """
    Python interface for O₂scl class ``ix_interp``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_interp.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_interp

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_interp
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
        Delete function for class ix_interp
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_interp
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_interp
        
        Returns: ix_interp object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix,v):
        """
        Constructor-like class method for ix_interp .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_interp_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_double]
        return cls(f(ix,v))


class ix_grid:
    """
    Python interface for O₂scl class ``ix_grid``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_grid.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_grid

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_grid
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
        Delete function for class ix_grid
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_grid
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_grid
        
        Returns: ix_grid object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix,start,end,n_bins,log):
        """
        Constructor-like class method for ix_grid .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_grid_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_size_t,ctypes.c_bool]
        return cls(f(ix,start,end,n_bins,log))


class ix_gridw:
    """
    Python interface for O₂scl class ``ix_gridw``,
    see
    https://awsteiner.org/code/o2scl/html/class/ix_gridw.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class ix_gridw

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_ix_gridw
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
        Delete function for class ix_gridw
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_ix_gridw
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ix_gridw
        
        Returns: ix_gridw object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @classmethod
    def init(cls,ix,start,end,width,log):
        """
        Constructor-like class method for ix_gridw .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_ix_gridw_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_bool]
        return cls(f(ix,start,end,width,log))


class tensor:
    """
    Python interface for O2scl class ``tensor``,
    see
    https://awsteiner.org/code/o2scl/html/class/tensor.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class tensor

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_tensor_
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
        Delete function for class tensor
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor
        
        Returns: tensor object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor
        
        Returns: new copy of the tensor object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_tensor_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor__is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor__clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_vector(self,index,val):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_tensor__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,index._ptr,val)
        return

    def set_all(self,x):
        """
        | Parameters:
        | *x*: ``double``
        """
        func=self._link.o2scl.o2scl_tensor__set_all
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,x)
        return

    def swap_data(self,data):
        """
        | Parameters:
        | *data*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_tensor__swap_data
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,data._ptr)
        return

    def get_vector(self,index):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor__get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,index._ptr)
        return ret

    def resize_vector(self,n,index):
        """
        | Parameters:
        | *n*: ``size_t``
        | *index*: :class:`vector<size_t>` object
        """
        func=self._link.o2scl.o2scl_tensor__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,n,index._ptr)
        return

    def get_rank(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor__get_rank
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_size(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor__get_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def get_size_arr(self):
        """
        | Returns: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor__get_size_arr
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        ret2=std_vector_size_t(ret)
        return ret2

    def get_data(self):
        """
        | Returns: ``numpy`` array
        """
        func=self._link.o2scl.o2scl_tensor__get_data
        n_=ctypes.c_int(0)
        ptr_=ctypes.POINTER(ctypes.c_double)()
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),ctypes.POINTER(ctypes.c_int)]
        func(self._ptr,ctypes.byref(ptr_),ctypes.byref(n_))
        ret=numpy.ctypeslib.as_array(ptr_,shape=(n_.value,))
        return ret

    def total_size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor__total_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def pack_indices(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor__pack_indices
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,index._ptr)
        return ret

    def unpack_index(self,ix,index):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor__unpack_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,ix,index._ptr)
        return

    def min_value(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor__min_value
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def min_index(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor__min_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index._ptr)
        return

    def min(self,ix):
        """
        | Parameters:
        | *ix*: :class:`std_vector_size_t` object
        | Returns: , a Python float
        """
        func=self._link.o2scl.o2scl_tensor__min
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_double)]
        value_conv=ctypes.c_double(0)
        func(self._ptr,ix._ptr,ctypes.byref(value_conv))
        return value_conv.value

    def max_value(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor__max_value
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def max_index(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor__max_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index._ptr)
        return

    def max(self,ix):
        """
        | Parameters:
        | *ix*: :class:`std_vector_size_t` object
        | Returns: , a Python float
        """
        func=self._link.o2scl.o2scl_tensor__max
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_double)]
        value_conv=ctypes.c_double(0)
        func(self._ptr,ix._ptr,ctypes.byref(value_conv))
        return value_conv.value

    def minmax_value(self):
        """
        | Parameters:
        | Returns: , a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_tensor__minmax_value
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
        min_conv=ctypes.c_double(0)
        max_conv=ctypes.c_double(0)
        func(self._ptr,ctypes.byref(min_conv),ctypes.byref(max_conv))
        return min_conv.value,max_conv.value

    def minmax_index(self,min,max):
        """
        | Parameters:
        | *min*: :class:`std_vector_size_t` object
        | *max*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor__minmax_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,min._ptr,max._ptr)
        return

    def minmax(self,min_ix,max_ix):
        """
        | Parameters:
        | *min_ix*: :class:`std_vector_size_t` object
        | *max_ix*: :class:`std_vector_size_t` object
        | Returns: , a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_tensor__minmax
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_double),ctypes.c_void_p,ctypes.POINTER(ctypes.c_double)]
        min_value_conv=ctypes.c_double(0)
        max_value_conv=ctypes.c_double(0)
        func(self._ptr,min_ix._ptr,ctypes.byref(min_value_conv),max_ix._ptr,ctypes.byref(max_value_conv))
        return min_value_conv.value,max_value_conv.value

    def total_sum(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor__total_sum
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def copy_table3d_sum(self,ix_x,ix_y,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *slice_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor__copy_table3d_sum
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_slice_name._ptr)
        return

    def copy_table3d(self,ix_x,ix_y,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *slice_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor__copy_table3d
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_slice_name._ptr)
        return

    @classmethod
    def create_size(cls,rank,sizes):
        """
        Constructor-like class method for tensor<> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_tensor__create_size
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_void_p]
        return cls(f(rank,sizes._ptr))

    def create_size(self,v):
        """
        Copy ``v`` to an :class:`std_vector_size_t` object and add the line of
        data to the table
        """
        # Create a std_vector object and copy the data over
        vec=std_vector_size_t()
        vec.resize(len(v))
        for i in range(0,len(v)):
            vec[i]=v[i]
        self.create_size_vector(vec)
        return
     
    def set(self,index,val):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and add the 
        data to the table
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        self.set_vector(svst,val)
        return
     
    def get(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and get the 
        data from the table
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        return self.get_vector(svst)
    
    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        self.resize_vector(len(svst),svst)
        return

class tensor_int:
    """
    Python interface for O2scl class ``tensor``,
    see
    https://awsteiner.org/code/o2scl/html/class/tensor.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class tensor_int

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_tensor_int_std_vector_int_
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
        Delete function for class tensor_int
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_int_std_vector_int_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor_int
        
        Returns: tensor_int object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor_int
        
        Returns: new copy of the tensor_int object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_tensor_int_std_vector_int_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_vector(self,index,val):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | *val*: ``int``
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,index._ptr,val)
        return

    def set_all(self,x):
        """
        | Parameters:
        | *x*: ``int``
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__set_all
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,x)
        return

    def get_vector(self,index):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__get
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,index._ptr)
        return ret

    def resize_vector(self,n,index):
        """
        | Parameters:
        | *n*: ``size_t``
        | *index*: :class:`vector<size_t>` object
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,n,index._ptr)
        return

    def get_rank(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__get_rank
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_size(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__get_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def get_data(self):
        """
        | Returns: :class:`std_vector_int` object
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__get_data
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        ret2=std_vector_int(ret)
        return ret2

    def total_size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__total_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def pack_indices(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__pack_indices
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,index._ptr)
        return ret

    def unpack_index(self,ix,index):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__unpack_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,ix,index._ptr)
        return

    def min_value(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__min_value
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def min_index(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__min_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index._ptr)
        return

    def min(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        | Returns: , a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__min
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
        val_conv=ctypes.c_int(0)
        func(self._ptr,index._ptr,ctypes.byref(val_conv))
        return val_conv.value

    def max_value(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__max_value
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def max_index(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__max_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index._ptr)
        return

    def max(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        | Returns: , a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__max
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
        val_conv=ctypes.c_int(0)
        func(self._ptr,index._ptr,ctypes.byref(val_conv))
        return val_conv.value

    def minmax_value(self):
        """
        | Parameters:
        | Returns: , a Python int, a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__minmax_value
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)]
        min_conv=ctypes.c_int(0)
        max_conv=ctypes.c_int(0)
        func(self._ptr,ctypes.byref(min_conv),ctypes.byref(max_conv))
        return min_conv.value,max_conv.value

    def minmax_index(self,index_min,index_max):
        """
        | Parameters:
        | *index_min*: :class:`std_vector_size_t` object
        | *index_max*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__minmax_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index_min._ptr,index_max._ptr)
        return

    def minmax(self,index_min,index_max):
        """
        | Parameters:
        | *index_min*: :class:`std_vector_size_t` object
        | *index_max*: :class:`std_vector_size_t` object
        | Returns: , a Python int, a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__minmax
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_int),ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
        min_conv=ctypes.c_int(0)
        max_conv=ctypes.c_int(0)
        func(self._ptr,index_min._ptr,ctypes.byref(min_conv),index_max._ptr,ctypes.byref(max_conv))
        return min_conv.value,max_conv.value

    def total_sum(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__total_sum
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def copy_table3d_sum(self,ix_x,ix_y,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *slice_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__copy_table3d_sum
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_slice_name._ptr)
        return

    def copy_table3d(self,ix_x,ix_y,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *slice_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__copy_table3d
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_slice_name._ptr)
        return

    @classmethod
    def create_size(cls,rank,sizes):
        """
        Constructor-like class method for tensor<int,std::vector<int>> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_tensor_int_std_vector_int__create_size
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_void_p]
        return cls(f(rank,sizes._ptr))

    def create_size(self,v):
        """
        Copy ``v`` to an :class:`std_vector_size_t` object and add the line of
        data to the table
        """
        # Create a std_vector object and copy the data over
        vec=std_vector_size_t()
        vec.resize(len(v))
        for i in range(0,len(v)):
            vec[i]=v[i]
        self.create_size_vector(vec)
        return
     
    def set(self,index,val):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and add the 
        data to the table
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        self.set_vector(svst,val)
        return
     
    def get(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and get the 
        data from the table
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        return self.get_vector(svst)
    
    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        self.resize_vector(svst)
        return

class tensor_size_t:
    """
    Python interface for O2scl class ``tensor``,
    see
    https://awsteiner.org/code/o2scl/html/class/tensor.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class tensor_size_t

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_tensor_size_t_std_vector_size_t_
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
        Delete function for class tensor_size_t
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_size_t_std_vector_size_t_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor_size_t
        
        Returns: tensor_size_t object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor_size_t
        
        Returns: new copy of the tensor_size_t object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_tensor_size_t_std_vector_size_t_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_vector(self,index,val):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | *val*: ``size_t``
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,index._ptr,val)
        return

    def set_all(self,x):
        """
        | Parameters:
        | *x*: ``size_t``
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__set_all
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,x)
        return

    def get_vector(self,index):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__get
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,index._ptr)
        return ret

    def resize_vector(self,n,index):
        """
        | Parameters:
        | *n*: ``size_t``
        | *index*: :class:`vector<size_t>` object
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,n,index._ptr)
        return

    def get_rank(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__get_rank
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_size(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__get_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def get_data(self):
        """
        | Returns: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__get_data
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        ret2=std_vector_size_t(ret)
        return ret2

    def total_size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__total_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def min_value(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__min_value
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def min_index(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__min_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index._ptr)
        return

    def min(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        | Returns: , a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__min
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t)]
        val_conv=ctypes.c_size_t(0)
        func(self._ptr,index._ptr,ctypes.byref(val_conv))
        return val_conv.value

    def max_value(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__max_value
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def max_index(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__max_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index._ptr)
        return

    def max(self,index):
        """
        | Parameters:
        | *index*: :class:`std_vector_size_t` object
        | Returns: , a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__max
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t)]
        val_conv=ctypes.c_size_t(0)
        func(self._ptr,index._ptr,ctypes.byref(val_conv))
        return val_conv.value

    def minmax_value(self):
        """
        | Parameters:
        | Returns: , a Python int, a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__minmax_value
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
        min_conv=ctypes.c_size_t(0)
        max_conv=ctypes.c_size_t(0)
        func(self._ptr,ctypes.byref(min_conv),ctypes.byref(max_conv))
        return min_conv.value,max_conv.value

    def minmax_index(self,index_min,index_max):
        """
        | Parameters:
        | *index_min*: :class:`std_vector_size_t` object
        | *index_max*: :class:`std_vector_size_t` object
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__minmax_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,index_min._ptr,index_max._ptr)
        return

    def minmax(self,index_min,index_max):
        """
        | Parameters:
        | *index_min*: :class:`std_vector_size_t` object
        | *index_max*: :class:`std_vector_size_t` object
        | Returns: , a Python int, a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__minmax
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t)]
        min_conv=ctypes.c_size_t(0)
        max_conv=ctypes.c_size_t(0)
        func(self._ptr,index_min._ptr,ctypes.byref(min_conv),index_max._ptr,ctypes.byref(max_conv))
        return min_conv.value,max_conv.value

    def total_sum(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__total_sum
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def copy_table3d_sum(self,ix_x,ix_y,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *slice_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__copy_table3d_sum
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_slice_name._ptr)
        return

    def copy_table3d(self,ix_x,ix_y,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *slice_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__copy_table3d
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_slice_name._ptr)
        return

    @classmethod
    def create_size(cls,rank,sizes):
        """
        Constructor-like class method for tensor<size_t,std::vector<size_t>> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_tensor_size_t_std_vector_size_t__create_size
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_void_p]
        return cls(f(rank,sizes._ptr))

    def create_size(self,v):
        """
        Copy ``v`` to an :class:`std_vector_size_t` object and add the line of
        data to the table
        """
        # Create a std_vector object and copy the data over
        vec=std_vector_size_t()
        vec.resize(len(v))
        for i in range(0,len(v)):
            vec[i]=v[i]
        self.create_size_vector(vec)
        return
      
    def set(self,index,val):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and add the 
        data to the table
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        self.set_vector(svst,val)
        return
     
    def get(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and get the 
        data from the table
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        return self.get_vector(svst)
    
    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        self.resize_vector(svst)
        return

class tensor_grid(tensor):
    """
    Python interface for O2scl class ``tensor_grid``,
    see
    https://awsteiner.org/code/o2scl/html/class/tensor_grid.html .
    """

    def __init__(self,pointer=0):
        """
        Init function for class tensor_grid

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_tensor_grid_
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
        Delete function for class tensor_grid
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_grid_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor_grid
        
        Returns: tensor_grid object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor_grid
        
        Returns: new copy of the tensor_grid object
        """

        new_obj=type(self)()
        f2=self._link.o2scl.o2scl_copy_tensor_grid_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_grid__is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_val_vector(self,grid_point,val):
        """
        | Parameters:
        | *grid_point*: :class:`vector<double>` object
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_tensor_grid__set_val
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,grid_point._ptr,val)
        return

    def get_val_vector(self,grid_point):
        """
        | Parameters:
        | *grid_point*: :class:`vector<double>` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor_grid__get_val
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,grid_point._ptr)
        return ret

    def resize_vector(self,rank,dim):
        """
        | Parameters:
        | *rank*: ``size_t``
        | *dim*: :class:`vector<size_t>` object
        """
        func=self._link.o2scl.o2scl_tensor_grid__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,rank,dim._ptr)
        return

    def is_grid_set(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_tensor_grid__is_grid_set
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_grid_packed(self,grid):
        """
        | Parameters:
        | *grid*: :class:`vector<double>` object
        """
        func=self._link.o2scl.o2scl_tensor_grid__set_grid_packed
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,grid._ptr)
        return

    def set_grid_vec_vec(self,grid_vecs):
        """
        | Parameters:
        | *grid_vecs*: :class:`vector<vector<double>>` object
        """
        func=self._link.o2scl.o2scl_tensor_grid__set_grid_vec_vec
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,grid_vecs._ptr)
        return

    def default_grid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_grid__default_grid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_grid_i_vec(self,i,grid):
        """
        | Parameters:
        | *i*: ``size_t``
        | *grid*: :class:`vector<double>` object
        """
        func=self._link.o2scl.o2scl_tensor_grid__set_grid_i_vec
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,i,grid._ptr)
        return

    def set_grid_i_func(self,ix,func):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *func*: byte array
        """
        s_func=o2sclpy.std_string()
        s_func.init_bytes(force_bytes_string(func))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_grid__set_grid_i_func
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,ix,s_func._ptr)
        return

    def get_grid(self,i,j):
        """
        | Parameters:
        | *i*: ``size_t``
        | *j*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor_grid__get_grid
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        ret=func(self._ptr,i,j)
        return ret

    def get_grid_packed(self):
        """
        | Returns: ``numpy`` array
        """
        func=self._link.o2scl.o2scl_tensor_grid__get_grid_packed
        n_=ctypes.c_int(0)
        ptr_=ctypes.POINTER(ctypes.c_double)()
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),ctypes.POINTER(ctypes.c_int)]
        func(self._ptr,ctypes.byref(ptr_),ctypes.byref(n_))
        ret=numpy.ctypeslib.as_array(ptr_,shape=(n_.value,))
        return ret

    def set_grid(self,i,j,val):
        """
        | Parameters:
        | *i*: ``size_t``
        | *j*: ``size_t``
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_tensor_grid__set_grid
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,i,j,val)
        return

    def lookup_grid(self,i,val):
        """
        | Parameters:
        | *i*: ``size_t``
        | *val*: ``double``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_grid__lookup_grid
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        ret=func(self._ptr,i,val)
        return ret

    def copy_slice_interp(self,ifix,vals):
        """
        | Parameters:
        | *ifix*: :class:`std_vector_size_t` object
        | *vals*: :class:`std_vector` object
        | Returns: :class:`tensor_grid` object
        """
        func=self._link.o2scl.o2scl_tensor_grid__copy_slice_interp
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret2=func(self._ptr,ifix._ptr,vals._ptr)
        ret=tensor_grid(ret2)
        ret.owner=True
        return ret

    def copy_table3d_align(self,ix_x,ix_y,index,tab,z_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *index*: :class:`vector<size_t>` object
        | *tab*: :class:`table3d` object
        | *z_name* ="z": byte array
        """
        s_z_name=o2sclpy.std_string()
        s_z_name.init_bytes(force_bytes_string(z_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_grid__copy_table3d_align
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,index._ptr,tab._ptr,s_z_name._ptr)
        return

    def copy_table3d_align_setxy(self,ix_x,ix_y,index,tab,x_name="x",y_name="y",z_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *index*: :class:`vector<size_t>` object
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *z_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_z_name=o2sclpy.std_string()
        s_z_name.init_bytes(force_bytes_string(z_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_grid__copy_table3d_align_setxy
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,index._ptr,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_z_name._ptr)
        return

    def copy_table3d_interp(self,ix_x,ix_y,index,tab,slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *index*: :class:`std_vector_size_t` object
        | *tab*: :class:`table3d` object
        | *slice_name* ="z": byte array
        """
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_grid__copy_table3d_interp
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,index._ptr,tab._ptr,s_slice_name._ptr)
        return

    def copy_table3d_interp_values(self,ix_x,ix_y,values,tab,slice_name="z",verbose=0):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *values*: :class:`std_vector` object
        | *tab*: :class:`table3d` object
        | *slice_name* ="z": byte array
        | *verbose* =0: ``int``
        """
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_grid__copy_table3d_interp_values
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,ix_x,ix_y,values._ptr,tab._ptr,s_slice_name._ptr,verbose)
        return

    def copy_table3d_interp_values_setxy(self,ix_x,ix_y,values,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *values*: :class:`std_vector` object
        | *tab*: :class:`table3d` object
        | *x_name* ="x": byte array
        | *y_name* ="y": byte array
        | *slice_name* ="z": byte array
        """
        s_x_name=o2sclpy.std_string()
        s_x_name.init_bytes(force_bytes_string(x_name))
        # tag 7
        s_y_name=o2sclpy.std_string()
        s_y_name.init_bytes(force_bytes_string(y_name))
        # tag 7
        s_slice_name=o2sclpy.std_string()
        s_slice_name.init_bytes(force_bytes_string(slice_name))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_grid__copy_table3d_interp_values_setxy
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ix_x,ix_y,values._ptr,tab._ptr,s_x_name._ptr,s_y_name._ptr,s_slice_name._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_grid__clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_interp_type(self,interp_type):
        """
        | Parameters:
        | *interp_type*: ``size_t``
        """
        func=self._link.o2scl.o2scl_tensor_grid__set_interp_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,interp_type)
        return

    def interp_linear_partial(self,ix_to_interp,ix,val):
        """
        | Parameters:
        | *ix_to_interp*: :class:`std_vector_size_t` object
        | *ix*: :class:`std_vector_size_t` object
        | *val*: :class:`std_vector` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor_grid__interp_linear_partial
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,ix_to_interp._ptr,ix._ptr,val._ptr)
        return ret

    def interp_linear(self,v):
        """
        | Parameters:
        | *v*: :class:`vector<double>` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor_grid__interp_linear
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,v._ptr)
        return ret

    def from_table3d_fermi(self,t3d,slice,n_points,low=0.0,high=0.0,width=0.0):
        """
        | Parameters:
        | *t3d*: :class:`table3d` object
        | *slice*: byte array
        | *n_points*: ``size_t``
        | *low* =0.0: ``double``
        | *high* =0.0: ``double``
        | *width* =0.0: ``double``
        """
        s_slice=o2sclpy.std_string()
        s_slice.init_bytes(force_bytes_string(slice))
        # tag 7
        func=self._link.o2scl.o2scl_tensor_grid__from_table3d_fermi
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_double]
        func(self._ptr,t3d._ptr,s_slice._ptr,n_points,low,high,width)
        return

    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=std_vector_size_t()
        svst.init_py(index)
        self.resize_vector(len(svst),svst)
        return

class find_constants_const_entry:
    """
    Python interface for O₂scl class ``find_constants<>::const_entry``,
    see
    https://awsteiner.org/code/o2scl/html/class/find_constants<>::const_entry.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class find_constants_const_entry

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_find_constants_const_entry
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
        Delete function for class find_constants_const_entry
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_find_constants_const_entry
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class find_constants_const_entry
        
        Returns: find_constants_const_entry object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def get_names(self):
        """
        Get object of type :class:`std::vector<std::string>`
        """
        func1=self._link.o2scl.o2scl_find_constants_const_entry_get_names
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector_string(ptr)
        return obj

    def set_names(self,value):
        """
        Set object of type :class:`std::vector<std::string>`
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_names
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_unit(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_unit
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_unit(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    @property
    def unit_flag(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_unit_flag
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @unit_flag.setter
    def unit_flag(self,value):
        """
        Setter function for find_constants<>::const_entry::unit_flag .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_unit_flag
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def val(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_val
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @val.setter
    def val(self,value):
        """
        Setter function for find_constants<>::const_entry::val .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_val
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def get_source(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_source
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_source(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_source
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    @property
    def m(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_m
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m.setter
    def m(self,value):
        """
        Setter function for find_constants<>::const_entry::m .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_m
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def k(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_k
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @k.setter
    def k(self,value):
        """
        Setter function for find_constants<>::const_entry::k .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_k
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def s(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_s
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @s.setter
    def s(self,value):
        """
        Setter function for find_constants<>::const_entry::s .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_s
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def K(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_K
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @K.setter
    def K(self,value):
        """
        Setter function for find_constants<>::const_entry::K .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_K
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def A(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_A
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @A.setter
    def A(self,value):
        """
        Setter function for find_constants<>::const_entry::A .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_A
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def mol(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_mol
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mol.setter
    def mol(self,value):
        """
        Setter function for find_constants<>::const_entry::mol .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_mol
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def cd(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_cd
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cd.setter
    def cd(self,value):
        """
        Setter function for find_constants<>::const_entry::cd .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_cd
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return


class find_constants:
    """
    Python interface for O₂scl class ``find_constants<>``,
    see
    https://awsteiner.org/code/o2scl/html/class/find_constants<>.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class find_constants

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_find_constants_
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
        Delete function for class find_constants
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_find_constants_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class find_constants
        
        Returns: find_constants object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def output_list_cout(self):
        """
        """
        func=self._link.o2scl.o2scl_find_constants__output_list_cout
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def add_constant(self,f,verbose=0):
        """
        | Parameters:
        | *f*: :class:`find_constants<>::const_entry` object
        | *verbose* =0: ``int``
        """
        func=self._link.o2scl.o2scl_find_constants__add_constant
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,f._ptr,verbose)
        return

    def del_constant(self,name,verbose=0):
        """
        | Parameters:
        | *name*: :class:`std_string` object
        | *verbose* =0: ``int``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_find_constants__del_constant
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,name._ptr,verbose)
        return


class convert_units_der_unit:
    """
    Python interface for O₂scl class ``convert_units<>::der_unit``,
    see
    https://awsteiner.org/code/o2scl/html/class/convert_units<>::der_unit.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class convert_units_der_unit

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_convert_units_der_unit
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
        Delete function for class convert_units_der_unit
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_convert_units_der_unit
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class convert_units_der_unit
        
        Returns: convert_units_der_unit object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def get_label(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_label
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_label(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_label
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    @property
    def m(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_m
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m.setter
    def m(self,value):
        """
        Setter function for convert_units<>::der_unit::m .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_m
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def k(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_k
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @k.setter
    def k(self,value):
        """
        Setter function for convert_units<>::der_unit::k .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_k
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def s(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_s
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @s.setter
    def s(self,value):
        """
        Setter function for convert_units<>::der_unit::s .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_s
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def K(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_K
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @K.setter
    def K(self,value):
        """
        Setter function for convert_units<>::der_unit::K .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_K
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def A(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_A
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @A.setter
    def A(self,value):
        """
        Setter function for convert_units<>::der_unit::A .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_A
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def mol(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_mol
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mol.setter
    def mol(self,value):
        """
        Setter function for convert_units<>::der_unit::mol .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_mol
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def cd(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_cd
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cd.setter
    def cd(self,value):
        """
        Setter function for convert_units<>::der_unit::cd .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_cd
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def val(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_val
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @val.setter
    def val(self,value):
        """
        Setter function for convert_units<>::der_unit::val .
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_val
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def get_name(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_name(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_name
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def set(self,label,val,name='',m=0,k=0,s=0,K=0,A=0,mol=0,cd=0):
        """
        Set the properties of a derived unit
        FIXME: better docs here
        """
        label2=std_string()
        label2.init_bytes(force_bytes(label))
        self.set_label(label2)
        self.val=val
        name2=std_string()
        name2.init_bytes(force_bytes(name))
        self.set_name(name2)
        self.m=m
        self.k=k
        self.s=s
        self.K=K
        self.A=A
        self.mol=mol
        self.cd=cd
        return

class convert_units:
    """
    Python interface for O2scl class ``convert_units``,
    see
    https://awsteiner.org/code/o2scl/html/class/convert_units.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class convert_units

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_convert_units_
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
        Delete function for class convert_units
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_convert_units_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class convert_units
        
        Returns: convert_units object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @property
    def verbose(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_convert_units__get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for convert_units<>::verbose .
        """
        func=self._link.o2scl.o2scl_convert_units__set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def err_on_fail(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_convert_units__get_err_on_fail
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_on_fail.setter
    def err_on_fail(self,value):
        """
        Setter function for convert_units<>::err_on_fail .
        """
        func=self._link.o2scl.o2scl_convert_units__set_err_on_fail
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def combine_two_conv(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_convert_units__get_combine_two_conv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @combine_two_conv.setter
    def combine_two_conv(self,value):
        """
        Setter function for convert_units<>::combine_two_conv .
        """
        func=self._link.o2scl.o2scl_convert_units__set_combine_two_conv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def convert(self,frm,to,val):
        """
        | Parameters:
        | *frm*: byte array
        | *to*: byte array
        | *val*: ``double``
        | Returns: a Python float
        """
        s_frm=o2sclpy.std_string()
        s_frm.init_bytes(force_bytes_string(frm))
        # tag 7
        s_to=o2sclpy.std_string()
        s_to.init_bytes(force_bytes_string(to))
        # tag 7
        func=self._link.o2scl.o2scl_convert_units__convert
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,s_frm._ptr,s_to._ptr,val)
        return ret

    def convert_ret(self,frm,to,val,converted):
        """
        | Parameters:
        | *frm*: byte array
        | *to*: byte array
        | *val*: ``double``
        | *converted*: ``double``
        | Returns: a Python int
        """
        s_frm=o2sclpy.std_string()
        s_frm.init_bytes(force_bytes_string(frm))
        # tag 7
        s_to=o2sclpy.std_string()
        s_to.init_bytes(force_bytes_string(to))
        # tag 7
        func=self._link.o2scl.o2scl_convert_units__convert_ret
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,s_frm._ptr,s_to._ptr,val,converted)
        return ret

    def del_unit(self,name):
        """
        | Parameters:
        | *name*: :class:`std_string` object
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_convert_units__del_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,name._ptr)
        return

    def add_unit_internal(self,d):
        """
        | Parameters:
        | *d*: :class:`convert_units<>::der_unit` object
        """
        func=self._link.o2scl.o2scl_convert_units__add_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,d._ptr)
        return

    def set_natural_units(self,c_is_one=True,hbar_is_one=True,kb_is_one=True):
        """
        | Parameters:
        | *c_is_one* =true: ``bool``
        | *hbar_is_one* =true: ``bool``
        | *kb_is_one* =true: ``bool``
        """
        func=self._link.o2scl.o2scl_convert_units__set_natural_units
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool,ctypes.c_bool,ctypes.c_bool]
        func(self._ptr,c_is_one,hbar_is_one,kb_is_one)
        return

    def is_in_cache(self,frm,to):
        """
        | Parameters:
        | *frm*: byte array
        | *to*: byte array
        | Returns: a Python int
        """
        s_frm=o2sclpy.std_string()
        s_frm.init_bytes(force_bytes_string(frm))
        # tag 7
        s_to=o2sclpy.std_string()
        s_to.init_bytes(force_bytes_string(to))
        # tag 7
        func=self._link.o2scl.o2scl_convert_units__is_in_cache
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_frm._ptr,s_to._ptr)
        return ret

    def remove_cache(self,frm,to):
        """
        | Parameters:
        | *frm*: byte array
        | *to*: byte array
        | Returns: a Python int
        """
        s_frm=o2sclpy.std_string()
        s_frm.init_bytes(force_bytes_string(frm))
        # tag 7
        s_to=o2sclpy.std_string()
        s_to.init_bytes(force_bytes_string(to))
        # tag 7
        func=self._link.o2scl.o2scl_convert_units__remove_cache
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_frm._ptr,s_to._ptr)
        return ret

    def clear_cache(self):
        """
        """
        func=self._link.o2scl.o2scl_convert_units__clear_cache
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def test_unique(self):
        """
        """
        func=self._link.o2scl.o2scl_convert_units__test_unique
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def print_cache(self):
        """
        """
        func=self._link.o2scl.o2scl_convert_units__print_cache
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def print_units_cout(self):
        """
        """
        func=self._link.o2scl.o2scl_convert_units__print_units_cout
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def find_print(self,name,unit,prec,use_regex):
        """
        | Parameters:
        | *name*: byte array
        | *unit*: byte array
        | *prec*: ``size_t``
        | *use_regex*: ``bool``
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        s_unit=o2sclpy.std_string()
        s_unit.init_bytes(force_bytes_string(unit))
        # tag 7
        func=self._link.o2scl.o2scl_convert_units__find_print
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_bool]
        func(self._ptr,s_name._ptr,s_unit._ptr,prec,use_regex)
        return

    def find_unique(self,name,unit,use_regex=False):
        """
        | Parameters:
        | *name*: byte array
        | *unit*: byte array
        | *use_regex* =false: ``bool``
        | Returns: a Python float
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        s_unit=o2sclpy.std_string()
        s_unit.init_bytes(force_bytes_string(unit))
        # tag 7
        func=self._link.o2scl.o2scl_convert_units__find_unique
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]
        ret=func(self._ptr,s_name._ptr,s_unit._ptr,use_regex)
        return ret

    def add_unit(self,label,val,name='',m=0,k=0,s=0,K=0,A=0,mol=0,cd=0):
        """
        Add a unit
        """
        du=convert_units_der_unit()
        du.set(label,val,name,m,k,s,K,A,mol,cd)
        self.add_unit_internal(du)
        return

class columnify:
    """
    Python interface for O₂scl class ``columnify``,
    see
    https://awsteiner.org/code/o2scl/html/class/columnify.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class columnify

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_columnify
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
        Delete function for class columnify
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_columnify
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class columnify
        
        Returns: columnify object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @property
    def align_left(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_columnify_get_align_left
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def align_right(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_columnify_get_align_right
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def align_lmid(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_columnify_get_align_lmid
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def align_rmid(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_columnify_get_align_rmid
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def align_dp(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_columnify_get_align_dp
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def align_lnum(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_columnify_get_align_lnum
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)


class format_float:
    """
    Python interface for O₂scl class ``format_float``,
    see
    https://awsteiner.org/code/o2scl/html/class/format_float.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class format_float

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_format_float
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
        Delete function for class format_float
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_format_float
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class format_float
        
        Returns: format_float object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def set_sig_figs(self,sig_figs):
        """
        | Parameters:
        | *sig_figs*: ``size_t``
        """
        func=self._link.o2scl.o2scl_format_float_set_sig_figs
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,sig_figs)
        return

    def set_exp_limits(self,min,max):
        """
        | Parameters:
        | *min*: ``int``
        | *max*: ``int``
        """
        func=self._link.o2scl.o2scl_format_float_set_exp_limits
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        func(self._ptr,min,max)
        return

    def set_pad_zeros(self,pad):
        """
        | Parameters:
        | *pad*: ``bool``
        """
        func=self._link.o2scl.o2scl_format_float_set_pad_zeros
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,pad)
        return

    def set_dec_point(self,dec_point):
        """
        | Parameters:
        | *dec_point*: byte array
        """
        s_dec_point=o2sclpy.std_string()
        s_dec_point.init_bytes(force_bytes_string(dec_point))
        # tag 7
        func=self._link.o2scl.o2scl_format_float_set_dec_point
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,s_dec_point._ptr)
        return

    def set_exp_digits(self,d):
        """
        | Parameters:
        | *d*: ``int``
        """
        func=self._link.o2scl.o2scl_format_float_set_exp_digits
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,d)
        return

    def html_mode(self):
        """
        """
        func=self._link.o2scl.o2scl_format_float_html_mode
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def latex_mode(self):
        """
        """
        func=self._link.o2scl.o2scl_format_float_latex_mode
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def c_mode(self):
        """
        """
        func=self._link.o2scl.o2scl_format_float_c_mode
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def convert(self,x,debug=False):
        """
        | Parameters:
        | *x*: ``double``
        | *debug* =false: ``bool``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_format_float_convert
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_bool]
        ret=func(self._ptr,x,debug)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()


class interp_vec:
    """
    Python interface for O₂scl class ``interp_vec<std::vector<double>>``,
    see
    https://awsteiner.org/code/o2scl/html/class/interp_vec<std::vector<double>>.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class interp_vec

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_interp_vec_std_vector_double_
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
        Delete function for class interp_vec
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_interp_vec_std_vector_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class interp_vec
        
        Returns: interp_vec object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def set(self,n,x,y,interp_type):
        """
        | Parameters:
        | *n*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y*: :class:`std_vector` object
        | *interp_type*: ``int``
        """
        func=self._link.o2scl.o2scl_interp_vec_std_vector_double__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,n,x._ptr,y._ptr,interp_type)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_interp_vec_std_vector_double__clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def eval(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_vec_std_vector_double__eval
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def deriv(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_vec_std_vector_double__deriv
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def deriv2(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_vec_std_vector_double__deriv2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def integ(self,x1,x2):
        """
        | Parameters:
        | *x1*: ``double``
        | *x2*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_vec_std_vector_double__integ
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,x1,x2)
        return ret


class interp_krige_optim_rbf_noise:
    """
    Python interface for O₂scl class ``interp_krige_optim<std::vector<double>,std::vector<double>,covar_funct_rbf_noise>``,
    see
    https://awsteiner.org/code/o2scl/html/class/interp_krige_optim<std::vector<double>,std::vector<double>,covar_funct_rbf_noise>.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class interp_krige_optim_rbf_noise

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise_
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
        Delete function for class interp_krige_optim_rbf_noise
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class interp_krige_optim_rbf_noise
        
        Returns: interp_krige_optim_rbf_noise object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @property
    def mode_loo_cv(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__get_mode_loo_cv
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def mode_loo_cv_bf(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__get_mode_loo_cv_bf
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def mode_max_lml(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__get_mode_max_lml
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @property
    def verbose(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for interp_krige_optim<std::vector<double>,std::vector<double>,covar_funct_rbf_noise>::verbose .
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def mode(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__get_mode
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mode.setter
    def mode(self,value):
        """
        Setter function for interp_krige_optim<std::vector<double>,std::vector<double>,covar_funct_rbf_noise>::mode .
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__set_mode
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    def set(self,size,x,y):
        """
        | Parameters:
        | *size*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,size,x._ptr,y._ptr)
        return

    def eval(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__eval
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def deriv(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__deriv
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def deriv2(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__deriv2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def sigma(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__sigma
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def sample(self,x0):
        """
        | Parameters:
        | *x0*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__sample
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x0)
        return ret

    def sample_vec(self,x,y):
        """
        | Parameters:
        | *x*: :class:`std_vector` object
        | *y*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double_std_vector_double_covar_funct_rbf_noise__sample_vec
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,x._ptr,y._ptr)
        return


class terminal:
    """
    Python interface for O₂scl class ``terminal``,
    see
    https://awsteiner.org/code/o2scl/html/class/terminal.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class terminal

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_terminal
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
        Delete function for class terminal
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_terminal
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class terminal
        
        Returns: terminal object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def is_redirected(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_terminal_is_redirected
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def str_len(self,str):
        """
        | Parameters:
        | *str*: byte array
        | Returns: a Python int
        """
        s_str=o2sclpy.std_string()
        s_str.init_bytes(force_bytes_string(str))
        # tag 7
        func=self._link.o2scl.o2scl_terminal_str_len
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_str._ptr)
        return ret

    def hrule(self,n=78):
        """
        | Parameters:
        | *n* =78: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_hrule
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def cyan_fg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_cyan_fg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def magenta_fg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_magenta_fg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def yellow_fg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_yellow_fg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def red_fg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_red_fg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def green_fg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_green_fg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def blue_fg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_blue_fg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def cyan_bg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_cyan_bg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def magenta_bg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_magenta_bg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def yellow_bg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_yellow_bg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def red_bg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_red_bg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def green_bg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_green_bg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def blue_bg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_blue_bg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def default_fgbg(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_default_fgbg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def bold(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_bold
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def eight_bit_fg(self,col):
        """
        | Parameters:
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_eight_bit_fg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_short]
        ret=func(self._ptr,col)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def eight_bit_bg(self,col):
        """
        | Parameters:
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_eight_bit_bg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_short]
        ret=func(self._ptr,col)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def lowint(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_lowint
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def underline(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_underline
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def reverse(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_reverse
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def alt_font(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_alt_font
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def normal_font(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_normal_font
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def eight_bit_summ(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_eight_bit_summ
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def three_byte_summ(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_three_byte_summ
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def three_byte_summ_long(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_terminal_three_byte_summ_long
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()


class gen_test_number:
    """
    Python interface for O₂scl class ``gen_test_number<double>``,
    see
    https://awsteiner.org/code/o2scl/html/class/gen_test_number<double>.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class gen_test_number

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_gen_test_number_double_
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
        Delete function for class gen_test_number
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_gen_test_number_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class gen_test_number
        
        Returns: gen_test_number object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def reset(self):
        """
        """
        func=self._link.o2scl.o2scl_gen_test_number_double__reset
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_radix(self,r):
        """
        | Parameters:
        | *r*: ``double``
        """
        func=self._link.o2scl.o2scl_gen_test_number_double__set_radix
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,r)
        return

    def gen(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_gen_test_number_double__gen
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret


class funct_string:
    """
    Python interface for O₂scl class ``funct_string<double>``,
    see
    https://awsteiner.org/code/o2scl/html/class/funct_string<double>.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,pointer=0):
        """
        Init function for class funct_string

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_funct_string_double_
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
        Delete function for class funct_string
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_funct_string_double_
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class funct_string
        
        Returns: funct_string object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def set_parm(self,name,val):
        """
        | Parameters:
        | *name*: byte array
        | *val*: ``double``
        | Returns: a Python int
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_funct_string_double__set_parm
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,s_name._ptr,val)
        return ret

    def __getitem__(self,x):
        """
        | Parameters:
        | *x*: ``double``
        """
        func=self._link.o2scl.o2scl_funct_string_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    @classmethod
    def init(cls,expr,var):
        """
        Constructor-like class method for funct_string<double> .

        | Parameters:

        """

        f=o2sclpy.doc_data.top_linker.o2scl.o2scl_funct_string_double__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_char_p,ctypes.c_char_p]
        return cls(f(expr_,var_))


class comm_option_s:
    """
    Python interface for O₂scl class ``comm_option_s``,
    see
    https://awsteiner.org/code/o2scl/html/class/comm_option_s.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class comm_option_s

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_comm_option_s
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
        Delete function for class comm_option_s
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_comm_option_s
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class comm_option_s
        
        Returns: comm_option_s object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @property
    def shrt(self):
        """
        Property of type ``ctypes.c_char``
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_shrt
        func.restype=ctypes.c_char
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @shrt.setter
    def shrt(self,value):
        """
        Setter function for comm_option_s::shrt .
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_shrt
        func.argtypes=[ctypes.c_void_p,ctypes.c_char]
        func(self._ptr,value)
        return

    def get_lng(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_lng
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_lng(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_lng
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_desc(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_desc
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_desc(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_desc
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    @property
    def min_parms(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_min_parms
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @min_parms.setter
    def min_parms(self,value):
        """
        Setter function for comm_option_s::min_parms .
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_min_parms
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def max_parms(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_max_parms
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @max_parms.setter
    def max_parms(self,value):
        """
        Setter function for comm_option_s::max_parms .
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_max_parms
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    def get_parm_desc(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_parm_desc
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_parm_desc(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_parm_desc
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_help(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_help
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_help(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_help
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    @property
    def type(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_comm_option_s_get_type
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @type.setter
    def type(self,value):
        """
        Setter function for comm_option_s::type .
        """
        func=self._link.o2scl.o2scl_comm_option_s_set_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return


class cmd_line_arg:
    """
    Python interface for O₂scl class ``cmd_line_arg``,
    see
    https://awsteiner.org/code/o2scl/html/class/cmd_line_arg.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class cmd_line_arg

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_cmd_line_arg
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
        Delete function for class cmd_line_arg
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_cmd_line_arg
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class cmd_line_arg
        
        Returns: cmd_line_arg object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    def get_arg(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_cmd_line_arg_get_arg
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_arg(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_cmd_line_arg_set_arg
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    @property
    def is_option(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_cmd_line_arg_get_is_option
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @is_option.setter
    def is_option(self,value):
        """
        Setter function for cmd_line_arg::is_option .
        """
        func=self._link.o2scl.o2scl_cmd_line_arg_set_is_option
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def is_valid(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_cmd_line_arg_get_is_valid
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @is_valid.setter
    def is_valid(self,value):
        """
        Setter function for cmd_line_arg::is_valid .
        """
        func=self._link.o2scl.o2scl_cmd_line_arg_set_is_valid
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_parms(self):
        """
        Get object of type :class:`std::vector<std::string>`
        """
        func1=self._link.o2scl.o2scl_cmd_line_arg_get_parms
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector_string(ptr)
        return obj

    def set_parms(self,value):
        """
        Set object of type :class:`std::vector<std::string>`
        """
        func=self._link.o2scl.o2scl_cmd_line_arg_set_parms
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return


class cli:
    """
    Python interface for O₂scl class ``cli``,
    see
    https://awsteiner.org/code/o2scl/html/class/cli.html .
    
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,pointer=0):
        """
        Init function for class cli

        | Parameters:
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=o2sclpy.doc_data.top_linker.o2scl.o2scl_create_cli
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
        Delete function for class cli
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_cli
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class cli
        
        Returns: cli object
        """

        new_obj=type(self)(self._ptr)
        return new_obj

    @property
    def sync_verbose(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_cli_get_sync_verbose
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @sync_verbose.setter
    def sync_verbose(self,value):
        """
        Setter function for cli::sync_verbose .
        """
        func=self._link.o2scl.o2scl_cli_set_sync_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def gnu_intro(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_cli_get_gnu_intro
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @gnu_intro.setter
    def gnu_intro(self,value):
        """
        Setter function for cli::gnu_intro .
        """
        func=self._link.o2scl.o2scl_cli_set_gnu_intro
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_desc(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_cli_get_desc
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_desc(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_cli_set_desc
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_cmd_name(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_cli_get_cmd_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_cmd_name(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_cli_set_cmd_name
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_addl_help_cmd(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_cli_get_addl_help_cmd
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_addl_help_cmd(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_cli_set_addl_help_cmd
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def get_addl_help_cli(self):
        """
        Get byte array object.
        """
        func=self._link.o2scl.o2scl_cli_get_addl_help_cli
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string()
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_addl_help_cli(self,value):
        """
        Set object from byte array
        """
        func=self._link.o2scl.o2scl_cli_set_addl_help_cli
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        s_=o2sclpy.std_string()
        s_.init_bytes(force_bytes_string(value))
        func(self._ptr,s_._ptr)
        return

    def set_verbose(self,v):
        """
        | Parameters:
        | *v*: ``int``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_cli_set_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        ret=func(self._ptr,v)
        return ret

    def parse_for_aliases(self,sv,allow_undashed,debug=False):
        """
        | Parameters:
        | *sv*: :class:`std_vector_string` object
        | *allow_undashed*: ``bool``
        | *debug* =false: ``bool``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_cli_parse_for_aliases
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool,ctypes.c_bool]
        ret=func(self._ptr,sv._ptr,allow_undashed,debug)
        return ret

    def apply_aliases(self,sv,istart,debug=False):
        """
        | Parameters:
        | *sv*: :class:`std_vector_string` object
        | *istart*: ``size_t``
        | *debug* =false: ``bool``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_cli_apply_aliases
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_bool]
        ret=func(self._ptr,sv._ptr,istart,debug)
        return ret

    def get_option_list(self):
        """
        | Returns: :class:`std_vector_string` object
        """
        func=self._link.o2scl.o2scl_cli_get_option_list
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        vstrt=std_vector_string(ret)
        return vstrt

    def parameter_desc(self,name):
        """
        | Parameters:
        | *name*: byte array
        | Returns: Python bytes object
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_cli_parameter_desc
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()

    def option_short_desc(self,name):
        """
        | Parameters:
        | *name*: byte array
        | Returns: Python bytes object
        """
        s_name=o2sclpy.std_string()
        s_name.init_bytes(force_bytes_string(name))
        # tag 7
        func=self._link.o2scl.o2scl_cli_option_short_desc
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,s_name._ptr)
        strt=std_string(ret) # tag 5
        strt._owner=True
        return strt.to_bytes()


class shared_ptr_table_units(table_units):
    """
    Python interface for a shared pointer to a class of type ``table_units<>``
    """

    _s_ptr=0
    _ptr=0
    _link=0
    _owner=True

    def __init__(self,shared_ptr=0):
        """
        Init function for shared_ptr_table_units .
        """

        self._link=o2sclpy.doc_data.top_linker
        if shared_ptr==0:
            f2=self._link.o2scl.o2scl_create_shared_ptr_table_units_
            f2.restype=ctypes.c_void_p
            self._s_ptr=f2()
        else:
            self._s_ptr=shared_ptr

        f=self._link.o2scl.o2scl_shared_ptr_table_units__ptr
        f.argtypes=[ctypes.c_void_p]
        f.restype=ctypes.c_void_p
        self._ptr=f(self._s_ptr)
        return

    def __del__(self):
        """
        Delete function for shared_ptr_table_units .
        """

        f=self._link.o2scl.o2scl_free_shared_ptr_table_units_
        f.argtypes=[ctypes.c_void_p]
        f(self._s_ptr)
        return

def rearrange_and_copy(t,spec,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *t*: :class:`tensor<>` object
        | *spec*: string
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``tensor`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_rearrange_and_copy_tensor_double__wrapper
    func.restype=ctypes.c_void_p
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(t._ptr,s_spec._ptr,verbose,err_on_fail)
    ten=tensor(ret)
    ten._owner=True
    return ten

def rearrange_and_copy_int(t,spec,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *t*: :class:`tensor<int>` object
        | *spec*: string
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``tensor_int`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_rearrange_and_copy_tensor_int_int__wrapper
    func.restype=ctypes.c_void_p
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(t._ptr,s_spec._ptr,verbose,err_on_fail)
    ten=tensor(ret)
    ten._owner=True
    return ten

def rearrange_and_copy_size_t(t,spec,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *t*: :class:`tensor<size_t>` object
        | *spec*: string
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``tensor_size_t`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_rearrange_and_copy_tensor_size_t_size_t__wrapper
    func.restype=ctypes.c_void_p
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(t._ptr,s_spec._ptr,verbose,err_on_fail)
    ten=tensor(ret)
    ten._owner=True
    return ten

def grid_rearrange_and_copy(t,spec,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *t*: :class:`tensor_grid<>` object
        | *spec*: string
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``tensor_grid`` object
    """
    s_spec=o2sclpy.std_string()
    s_spec.init_bytes(force_bytes_string(spec))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_grid_rearrange_and_copy_tensor_grid_double__wrapper
    func.restype=ctypes.c_void_p
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_bool]
    ret=func(t._ptr,s_spec._ptr,verbose,err_on_fail)
    ten=tensor_grid(ret)
    ten._owner=True
    return ten

def fermi_function(x):
    """
        | Parameters:
        | *x*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_fermi_function_wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double]
    ret=func(x)
    return ret

def bose_function(x):
    """
        | Parameters:
        | *x*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_bose_function_wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double]
    ret=func(x)
    return ret

def quadratic_extremum_x(x1,x2,x3,y1,y2,y3):
    """
        | Parameters:
        | *x1*: ``double``
        | *x2*: ``double``
        | *x3*: ``double``
        | *y1*: ``double``
        | *y2*: ``double``
        | *y3*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_quadratic_extremum_x_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    ret=func(x1,x2,x3,y1,y2,y3)
    return ret

def quadratic_extremum_y(x1,x2,x3,y1,y2,y3):
    """
        | Parameters:
        | *x1*: ``double``
        | *x2*: ``double``
        | *x3*: ``double``
        | *y1*: ``double``
        | *y2*: ``double``
        | *y3*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_quadratic_extremum_y_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    ret=func(x1,x2,x3,y1,y2,y3)
    return ret

def screenify(nin,in_cols,out_cols,max_size=80):
    """
        | Parameters:
        | *nin*: ``size_t``
        | *in_cols*: :class:`vector<std::string>` object
        | *out_cols*: :class:`vector<std::string>` object
        | *max_size*: ``size_t``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_screenify_vector_std_string__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(nin,in_cols._ptr,out_cols._ptr,max_size)
    return

def file_exists(fname):
    """
        | Parameters:
        | *fname*: string
        | Returns: ``ctypes.c_bool`` object
    """
    s_fname=o2sclpy.std_string()
    s_fname.init_bytes(force_bytes_string(fname))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_file_exists_wrapper
    func.restype=ctypes.c_bool
    func.argtypes=[ctypes.c_void_p]
    ret=func(s_fname._ptr)
    return ret

def RGBtoHSV(r,g,b,h,s,v):
    """
        | Parameters:
        | *r*: ``double``
        | *g*: ``double``
        | *b*: ``double``
        | *h*: ``double``
        | *s*: ``double``
        | *v*: ``double``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_RGBtoHSV_wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(r,g,b,h._ptr,s._ptr,v._ptr)
    return

def HSVtoRGB(h,s,v,r,g,b):
    """
        | Parameters:
        | *h*: ``double``
        | *s*: ``double``
        | *v*: ``double``
        | *r*: ``double``
        | *g*: ``double``
        | *b*: ``double``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_HSVtoRGB_wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(h,s,v,r._ptr,g._ptr,b._ptr)
    return

def wordexp_single_file(fname):
    """
        | Parameters:
        | *fname*: :class:`std::string` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_wordexp_single_file_wrapper
    func.argtypes=[ctypes.c_void_p]
    func(fname._ptr)
    fname._owner=True
    return

def wordexp_wrapper(word,matches):
    """
        | Parameters:
        | *word*: string
        | *matches*: :class:`std::vector<std::string>` object
    """
    s_word=o2sclpy.std_string()
    s_word.init_bytes(force_bytes_string(word))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_wordexp_wrapper_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    func(s_word._ptr,matches._ptr)
    return

def function_to_double(s,verbose=0):
    """
        | Parameters:
        | *s*: string
        | *verbose*: ``int``
        | Returns: ``ctypes.c_double`` object
    """
    s_s=o2sclpy.std_string()
    s_s.init_bytes(force_bytes_string(s))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_function_to_double_wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_void_p,ctypes.c_int]
    ret=func(s_s._ptr,verbose)
    return ret

def function_to_double_nothrow(s,result,verbose=0):
    """
        | Parameters:
        | *s*: string
        | *result*: ``double``
        | *verbose*: ``int``
        | Returns: ``ctypes.c_int`` object
    """
    s_s=o2sclpy.std_string()
    s_s.init_bytes(force_bytes_string(s))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_function_to_double_nothrow_wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
    ret=func(s_s._ptr,result._ptr,verbose)
    return ret

def find_constant(name,unit):
    """
        | Parameters:
        | *name*: string
        | *unit*: string
        | Returns: ``ctypes.c_double`` object
    """
    s_name=o2sclpy.std_string()
    s_name.init_bytes(force_bytes_string(name))
    s_unit=o2sclpy.std_string()
    s_unit.init_bytes(force_bytes_string(unit))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_find_constant_wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    ret=func(s_name._ptr,s_unit._ptr)
    return ret

def string_to_uint_list(x,list):
    """
        | Parameters:
        | *x*: :class:`std::string` object
        | *list*: :class:`vector<size_t>` object
        | Returns: ``ctypes.c_int`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_string_to_uint_list_vector_size_t__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    ret=func(x._ptr,list._ptr)
    x._owner=True
    return ret

def rewrap_keep_endlines(str,sv,ncol=79,verbose=0,ignore_vt100=True):
    """
        | Parameters:
        | *str*: string
        | *sv*: :class:`std::vector<std::string>` object
        | *ncol*: ``size_t``
        | *verbose*: ``int``
        | *ignore_vt100*: ``bool``
    """
    s_str=o2sclpy.std_string()
    s_str.init_bytes(force_bytes_string(str))
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_rewrap_keep_endlines_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_int,ctypes.c_bool]
    func(s_str._ptr,sv._ptr,ncol,verbose,ignore_vt100)
    return

def vector_level_count(level,n,x,y):
    """
        | Parameters:
        | *level*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | Returns: ``ctypes.c_size_t`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_level_count_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_size_t
    func.argtypes=[ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p]
    ret=func(level,n,x._ptr,y._ptr)
    return ret

def vector_deriv_interp(n,v,dv,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *v*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_deriv_interp_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,v._ptr,dv._ptr,interp_type)
    return

def vector_deriv2_interp(n,v,dv,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *v*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_deriv2_interp_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,v._ptr,dv._ptr,interp_type)
    return

def vector_deriv_xy_interp(n,vx,vy,dv,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_deriv_xy_interp_std_vector_double_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,vx._ptr,vy._ptr,dv._ptr,interp_type)
    return

def vector_deriv2_xy_interp(n,vx,vy,dv,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_deriv2_xy_interp_std_vector_double_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,vx._ptr,vy._ptr,dv._ptr,interp_type)
    return

def vector_integ_interp(n,vx,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_integ_interp_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,vx._ptr,interp_type)
    return ret

def vector_integ_xy_interp(n,vx,vy,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_integ_xy_interp_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,vx._ptr,vy._ptr,interp_type)
    return ret

def vector_integ_ul_interp(n,x2,v,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *x2*: ``double``
        | *v*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_integ_ul_interp_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,x2,v._ptr,interp_type)
    return ret

def vector_integ_ul_xy_interp(n,x2,vx,vy,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *x2*: ``double``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_integ_ul_xy_interp_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,x2,vx._ptr,vy._ptr,interp_type)
    return ret

def vector_find_level(level,n,x,y,locs):
    """
        | Parameters:
        | *level*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *locs*: :class:`std::vector<double>` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_find_level_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(level,n,x._ptr,y._ptr,locs._ptr)
    return

def vector_invert_enclosed_sum(sum,n,x,y,lev,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *sum*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *lev*: ``double``
        | *boundaries*: ``int``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_invert_enclosed_sum_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    func(sum,n,x._ptr,y._ptr,lev._ptr,boundaries,verbose,err_on_fail)
    return

def vector_region_int(n,x,y,intl,locs,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *intl*: ``double``
        | *locs*: :class:`std::vector<double>` object
        | *boundaries*: ``int``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_region_int_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,intl,locs._ptr,boundaries,verbose,err_on_fail)
    return ret

def vector_region_fracint(n,x,y,intl,locs,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *intl*: ``double``
        | *locs*: :class:`std::vector<double>` object
        | *boundaries*: ``int``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_region_fracint_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,intl,locs._ptr,boundaries,verbose,err_on_fail)
    return ret

def vector_bound_fracint(n,x,y,frac,low,high,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *frac*: ``double``
        | *low*: ``double``
        | *high*: ``double``
        | *boundaries*: ``int``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_bound_fracint_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,frac,low._ptr,high._ptr,boundaries,verbose,err_on_fail)
    return ret

def vector_bound_int(n,x,y,frac,low,high,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *frac*: ``double``
        | *low*: ``double``
        | *high*: ``double``
        | *boundaries*: ``int``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
        | Returns: ``ctypes.c_int`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_bound_int_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,frac,low._ptr,high._ptr,boundaries,verbose,err_on_fail)
    return ret

def rebin_xy(x,y,x_out,y_out,n_pts,interp_type):
    """
        | Parameters:
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *x_out*: :class:`std::vector<double>` object
        | *y_out*: :class:`std::vector<double>` object
        | *n_pts*: ``size_t``
        | *interp_type*: ``size_t``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_rebin_xy_std_vector_double_std_vector_double_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
    func(x._ptr,y._ptr,x_out._ptr,y_out._ptr,n_pts,interp_type)
    return

def linear_or_log_chi2(x,y):
    """
        | Parameters:
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | Returns: ``ctypes.c_double`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_linear_or_log_chi2_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    ret=func(x._ptr,y._ptr)
    return ret

def linear_or_log_pair(x,y,log_x,log_y):
    """
        | Parameters:
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *log_x*: ``bool``
        | *log_y*: ``bool``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_linear_or_log_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(x._ptr,y._ptr,log_x._ptr,log_y._ptr)
    return

def vector_refine(n,index,data,factor,interp_type=2):
    """
        | Parameters:
        | *n*: ``size_t``
        | *index*: :class:`std::vector<double>` object
        | *data*: :class:`std::vector<double>` object
        | *factor*: ``size_t``
        | *interp_type*: ``size_t``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_vector_refine_std_vector_double_std_vector_double_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
    func(n,index._ptr,data._ptr,factor,interp_type)
    return

def linear_or_log(x,log_x):
    """
        | Parameters:
        | *x*: :class:`std::vector<double>` object
        | *log_x*: ``bool``
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_linear_or_log_std_vector_double__wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    func(x._ptr,log_x._ptr)
    return

def get_screen_size_ioctl(row,col):
    """
        | Parameters:
        | *row*: ``int``
        | *col*: ``int``
        | Returns: ``ctypes.c_int`` object
    """
    func=o2sclpy.doc_data.top_linker.o2scl.o2scl_get_screen_size_ioctl_wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    ret=func(row._ptr,col._ptr)
    return ret

