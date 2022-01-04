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
import numpy

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
    Python interface for C++ class ``std::string``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std_string

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_string
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
        
        Returns: a std_string object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        | *value*: char
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
        | *s* a Python bytes string
        """
        self.resize(len(s))
        for i in range(0,len(s)):
            self.__setitem__(i,s[i])
        return
    
    def to_bytes(self):
        """
        Copy the string to a Python bytes object
    
        Returns: a Python bytes string
        """
        ret=b''
        for i in range(0,self.length()):
            ret=ret+self.__getitem__(i)
        return ret

class std_vector:
    """
    Python interface for C++ class ``std::vector<double>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std_vector

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_vector_double_
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
        Delete function for class std_vector
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector
        
        Returns: a std_vector object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        | *value*: double
        """
        func=self._link.o2scl.o2scl_std_vector_double__setitem
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

class std_vector_int:
    """
    Python interface for C++ class ``std::vector<int>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std_vector_int

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_vector_int_
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
        Delete function for class std_vector_int
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_int_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_int
        
        Returns: a std_vector_int object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        | *value*: int
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

    def __init__(self,link,pointer=0):
        """
        Init function for class std_vector_size_t

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_vector_size_t_
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
        Delete function for class std_vector_size_t
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_size_t_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_size_t
        
        Returns: a std_vector_size_t object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        | *value*: size_t
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

class std_vector_string:
    """
    Python interface for C++ class ``std::vector<std::string>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std_vector_string

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_vector_std_string_
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
        Delete function for class std_vector_string
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_std_string_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_string
        
        Returns: a std_vector_string object
        """

        new_obj=type(self)(self._link,self._ptr)
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

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_std_vector_std_string__getitem
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: Python bytes string
        """
        func=self._link.o2scl.o2scl_std_vector_std_string__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char_p]
        func(self._ptr,i,value)
        return

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: a Python int
        """
        return self.size()

class ublas_vector:
    """
    Python interface for C++ class ``boost::numeric::ublas::vector<double>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class ublas_vector

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_boost_numeric_ublas_vector_double_
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
        Delete function for class ublas_vector
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_boost_numeric_ublas_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ublas_vector
        
        Returns: a ublas_vector object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        | *value*: double
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

class ublas_matrix:
    """
    Python interface for C++ class ``boost::numeric::ublas::matrix<double>``.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class ublas_matrix

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_boost_numeric_ublas_matrix_double_
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
        Delete function for class ublas_matrix
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_boost_numeric_ublas_matrix_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ublas_matrix
        
        Returns: a ublas_matrix object
        """

        new_obj=type(self)(self._link,self._ptr)
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

    def __getitem__(self,tup):
        """
        | Parameters:
        | *m*: ``size_t``
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        m,n=tup
        ret=func(self._ptr,m,n)
        return ret

    def __setitem__(self,tup,value):
        m,n=tup
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

    def __init__(self,link,pointer=0):
        """
        Init function for class ublas_matrix_int

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_boost_numeric_ublas_matrix_int_
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
        Delete function for class ublas_matrix_int
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_boost_numeric_ublas_matrix_int_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class ublas_matrix_int
        
        Returns: a ublas_matrix_int object
        """

        new_obj=type(self)(self._link,self._ptr)
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

    def __getitem__(self,tup):
        """
        | Parameters:
        | *m*: ``size_t``
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost_numeric_ublas_matrix_int__getitem
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        m,n=tup
        ret=func(self._ptr,m,n)
        return ret

    def __setitem__(self,tup,value):
        m,n=tup
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

    def __init__(self,link,pointer=0):
        """
        Init function for class std_vector_vector

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_vector_std_vector_double_
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
        Delete function for class std_vector_vector
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_std_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_vector
        
        Returns: a std_vector_vector object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        sv=std_vector(self._link)
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

class std_complex:
    """
    Python interface for O\ :sub:`2`\ scl class ``std::complex<double>``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/std::complex<double>.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std_complex

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_complex_double_
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
        Delete function for class std_complex
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_complex_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_complex
        
        Returns: a std_complex object
        """

        new_obj=type(self)(self._link,self._ptr)
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
    def init(cls,link,re,im):
        """
        Constructor-like class method for std::complex<double> .

        | Parameters:

        """

        f=link.o2scl.o2scl_std_complex_double__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double]
        return cls(link,f(re,im))

    def to_python(self):
        """
        Convert to a python complex number
    
        Returns: a python complex number
        """
        ret=self.real()+self.imag()*1j
        return ret

class lib_settings_class:
    """
    Python interface for O\ :sub:`2`\ scl class ``lib_settings_class``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/lib_settings_class.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class lib_settings_class

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_lib_settings_class
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
        Delete function for class lib_settings_class
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_lib_settings_class
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class lib_settings_class
        
        Returns: a lib_settings_class object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def get_data_dir(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_data_dir
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def set_data_dir(self,dir):
        """
        | Parameters:
        | *dir*: string
        | Returns: a Python int
        """
        dir_=ctypes.c_char_p(force_bytes(dir))
        func=self._link.o2scl.o2scl_lib_settings_class_set_data_dir
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,dir_)
        return ret

    def get_doc_dir(self):
        """
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_doc_dir
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def set_doc_dir(self,dir):
        """
        | Parameters:
        | *dir*: string
        | Returns: a Python int
        """
        dir_=ctypes.c_char_p(force_bytes(dir))
        func=self._link.o2scl.o2scl_lib_settings_class_set_doc_dir
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,dir_)
        return ret

    def eos_installed(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_eos_installed
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def part_installed(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_part_installed
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def hdf_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_hdf_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
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

    def gsl2_support(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_lib_settings_class_gsl2_support
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
        strt=std_string(self._link,ret)
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
        strt=std_string(self._link,ret)
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
        strt=std_string(self._link,ret)
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
        strt=std_string(self._link,ret)
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
        ret2=convert_units(self._link,ret)
        return ret2


class table:
    """
    Python interface for O\ :sub:`2`\ scl class ``table``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/table.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class table

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_table_
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
        Delete function for class table
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_table_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class table
        
        Returns: a table object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class table
        
        Returns: a new copy of the table object
        """

        new_obj=type(self)(self._link)
        f2=self._link.o2scl.o2scl_copy_table_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def __getitem__(self,col):
        """
        | Parameters:
        | *col*: string
        | Returns: :class:`std_vector` object
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table__getitem
        n_=ctypes.c_int(0)
        ptr_=ctypes.POINTER(ctypes.c_double)()
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),ctypes.POINTER(ctypes.c_int)]
        func(self._ptr,col_,ctypes.byref(ptr_),ctypes.byref(n_))
        ret=numpy.ctypeslib.as_array(ptr_,shape=(n_.value,))
        return ret

    def set(self,col,row,val):
        """
        | Parameters:
        | *col*: string
        | *row*: ``size_t``
        | *val*: ``double``
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,col_,row,val)
        return

    def get(self,col,row):
        """
        | Parameters:
        | *col*: string
        | *row*: ``size_t``
        | Returns: a Python float
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table__get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        ret=func(self._ptr,col_,row)
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
        | *col*: string
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table__new_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,col_)
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
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def rename_column(self,src,dest):
        """
        | Parameters:
        | *src*: string
        | *dest*: string
        """
        src_=ctypes.c_char_p(force_bytes(src))
        dest_=ctypes.c_char_p(force_bytes(dest))
        func=self._link.o2scl.o2scl_table__rename_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,src_,dest_)
        return

    def delete_column(self,col):
        """
        | Parameters:
        | *col*: string
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table__delete_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,col_)
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
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def init_column(self,scol,val):
        """
        | Parameters:
        | *scol*: string
        | *val*: ``double``
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__init_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,scol_,val)
        return

    def is_column(self,scol):
        """
        | Parameters:
        | *scol*: string
        | Returns: a Python boolean
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__is_column
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,scol_)
        return ret

    def lookup_column(self,scol):
        """
        | Parameters:
        | *scol*: string
        | Returns: a Python int
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__lookup_column
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,scol_)
        return ret

    def copy_column(self,src,dest):
        """
        | Parameters:
        | *src*: string
        | *dest*: string
        """
        src_=ctypes.c_char_p(force_bytes(src))
        dest_=ctypes.c_char_p(force_bytes(dest))
        func=self._link.o2scl.o2scl_table__copy_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,src_,dest_)
        return

    def add_col_from_table(self,source,src_index,src_col,dest_index,dest_col):
        """
        | Parameters:
        | *source*: :class:`table<>` object
        | *src_index*: string
        | *src_col*: string
        | *dest_index*: string
        | *dest_col*: string
        """
        src_index_=ctypes.c_char_p(force_bytes(src_index))
        src_col_=ctypes.c_char_p(force_bytes(src_col))
        dest_index_=ctypes.c_char_p(force_bytes(dest_index))
        dest_col_=ctypes.c_char_p(force_bytes(dest_col))
        func=self._link.o2scl.o2scl_table__add_col_from_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,source._ptr,src_index_,src_col_,dest_index_,dest_col_)
        return

    def insert_table(self,source,src_index,allow_extrap,dest_index):
        """
        | Parameters:
        | *source*: :class:`table<>` object
        | *src_index*: string
        | *allow_extrap*: ``bool``
        | *dest_index*: string
        """
        src_index_=ctypes.c_char_p(force_bytes(src_index))
        dest_index_=ctypes.c_char_p(force_bytes(dest_index))
        func=self._link.o2scl.o2scl_table__insert_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool,ctypes.c_char_p]
        func(self._ptr,source._ptr,src_index_,allow_extrap,dest_index_)
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
        | *scol*: string
        | *val*: ``double``
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__delete_row
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,scol_,val)
        return

    def delete_rows_func(self,func):
        """
        | Parameters:
        | *func*: string
        """
        func_=ctypes.c_char_p(force_bytes(func))
        func=self._link.o2scl.o2scl_table__delete_rows_func
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,func_)
        return

    def line_of_names(self,names):
        """
        | Parameters:
        | *names*: string
        """
        names_=ctypes.c_char_p(force_bytes(names))
        func=self._link.o2scl.o2scl_table__line_of_names
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,names_)
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

    def ordered_lookup(self,scol,val):
        """
        | Parameters:
        | *scol*: string
        | *val*: ``double``
        | Returns: a Python int
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__ordered_lookup
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        ret=func(self._ptr,scol_,val)
        return ret

    def lookup(self,scol,val):
        """
        | Parameters:
        | *scol*: string
        | *val*: ``double``
        | Returns: a Python int
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__lookup
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        ret=func(self._ptr,scol_,val)
        return ret

    def lookup_val(self,scol,val,scol2):
        """
        | Parameters:
        | *scol*: string
        | *val*: ``double``
        | *scol2*: string
        | Returns: a Python int
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        scol2_=ctypes.c_char_p(force_bytes(scol2))
        func=self._link.o2scl.o2scl_table__lookup_val
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,scol_,val,scol2_)
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
        | *sx*: string
        | *x0*: ``double``
        | *sy*: string
        | Returns: a Python float
        """
        sx_=ctypes.c_char_p(force_bytes(sx))
        sy_=ctypes.c_char_p(force_bytes(sy))
        func=self._link.o2scl.o2scl_table__interp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,sx_,x0,sy_)
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
        | *x*: string
        | *y*: string
        | *yp*: string
        """
        x_=ctypes.c_char_p(force_bytes(x))
        y_=ctypes.c_char_p(force_bytes(y))
        yp_=ctypes.c_char_p(force_bytes(yp))
        func=self._link.o2scl.o2scl_table__deriv_col
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,x_,y_,yp_)
        return

    def deriv(self,sx,x0,sy):
        """
        | Parameters:
        | *sx*: string
        | *x0*: ``double``
        | *sy*: string
        | Returns: a Python float
        """
        sx_=ctypes.c_char_p(force_bytes(sx))
        sy_=ctypes.c_char_p(force_bytes(sy))
        func=self._link.o2scl.o2scl_table__deriv
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,sx_,x0,sy_)
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
        | *x*: string
        | *y*: string
        | *yp*: string
        """
        x_=ctypes.c_char_p(force_bytes(x))
        y_=ctypes.c_char_p(force_bytes(y))
        yp_=ctypes.c_char_p(force_bytes(yp))
        func=self._link.o2scl.o2scl_table__deriv2_col
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,x_,y_,yp_)
        return

    def deriv2(self,sx,x0,sy):
        """
        | Parameters:
        | *sx*: string
        | *x0*: ``double``
        | *sy*: string
        | Returns: a Python float
        """
        sx_=ctypes.c_char_p(force_bytes(sx))
        sy_=ctypes.c_char_p(force_bytes(sy))
        func=self._link.o2scl.o2scl_table__deriv2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,sx_,x0,sy_)
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
        | *sx*: string
        | *x1*: ``double``
        | *x2*: ``double``
        | *sy*: string
        | Returns: a Python float
        """
        sx_=ctypes.c_char_p(force_bytes(sx))
        sy_=ctypes.c_char_p(force_bytes(sy))
        func=self._link.o2scl.o2scl_table__integ
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,sx_,x1,x2,sy_)
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
        | *x*: string
        | *y*: string
        | *yi*: string
        """
        x_=ctypes.c_char_p(force_bytes(x))
        y_=ctypes.c_char_p(force_bytes(y))
        yi_=ctypes.c_char_p(force_bytes(yi))
        func=self._link.o2scl.o2scl_table__integ_col
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,x_,y_,yi_)
        return

    def max(self,max):
        """
        | Parameters:
        | *max*: string
        | Returns: a Python float
        """
        max_=ctypes.c_char_p(force_bytes(max))
        func=self._link.o2scl.o2scl_table__max
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,max_)
        return ret

    def min(self,min):
        """
        | Parameters:
        | *min*: string
        | Returns: a Python float
        """
        min_=ctypes.c_char_p(force_bytes(min))
        func=self._link.o2scl.o2scl_table__min
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,min_)
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
        | *scol*: string
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__sort_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,scol_)
        return

    def sort_column(self,scol):
        """
        | Parameters:
        | *scol*: string
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__sort_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,scol_)
        return

    def average_col_roll(self,col_name,window):
        """
        | Parameters:
        | *col_name*: string
        | *window*: ``size_t``
        """
        col_name_=ctypes.c_char_p(force_bytes(col_name))
        func=self._link.o2scl.o2scl_table__average_col_roll
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        func(self._ptr,col_name_,window)
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
        | *list*: string
        """
        list_=ctypes.c_char_p(force_bytes(list))
        func=self._link.o2scl.o2scl_table__functions_columns
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,list_)
        return

    def function_column(self,function,scol):
        """
        | Parameters:
        | *function*: string
        | *scol*: string
        """
        function_=ctypes.c_char_p(force_bytes(function))
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__function_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,function_,scol_)
        return

    def row_function(self,scol,row):
        """
        | Parameters:
        | *scol*: string
        | *row*: ``size_t``
        | Returns: a Python float
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table__row_function
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        ret=func(self._ptr,scol_,row)
        return ret

    def function_find_row(self,function):
        """
        | Parameters:
        | *function*: string
        | Returns: a Python int
        """
        function_=ctypes.c_char_p(force_bytes(function))
        func=self._link.o2scl.o2scl_table__function_find_row
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,function_)
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
        vec=std_vector(self._link)
        vec.resize(len(v))
        for i in range(0,len(v)):
            vec[i]=v[i]
        self.line_of_data_vector(vec)
        return

class table_units(table):
    """
    Python interface for O\ :sub:`2`\ scl class ``table_units``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/table_units.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class table_units

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_table_units_
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
        Delete function for class table_units
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_table_units_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class table_units
        
        Returns: a table_units object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class table_units
        
        Returns: a new copy of the table_units object
        """

        new_obj=type(self)(self._link)
        f2=self._link.o2scl.o2scl_copy_table_units_
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def set_unit(self,col,unit):
        """
        | Parameters:
        | *col*: string
        | *unit*: string
        """
        col_=ctypes.c_char_p(force_bytes(col))
        unit_=ctypes.c_char_p(force_bytes(unit))
        func=self._link.o2scl.o2scl_table_units__set_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,col_,unit_)
        return

    def get_unit(self,col):
        """
        | Parameters:
        | *col*: string
        | Returns: Python bytes object
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table_units__get_unit
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,col_)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def line_of_units(self,unit_line):
        """
        | Parameters:
        | *unit_line*: string
        """
        unit_line_=ctypes.c_char_p(force_bytes(unit_line))
        func=self._link.o2scl.o2scl_table_units__line_of_units
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,unit_line_)
        return

    def remove_unit(self,col):
        """
        | Parameters:
        | *col*: string
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table_units__remove_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,col_)
        return

    def convert_to_unit(self,col,unit,err_on_fail=True):
        """
        | Parameters:
        | *col*: string
        | *unit*: string
        | *err_on_fail* =True: ``bool``
        | Returns: a Python int
        """
        col_=ctypes.c_char_p(force_bytes(col))
        unit_=ctypes.c_char_p(force_bytes(unit))
        func=self._link.o2scl.o2scl_table_units__convert_to_unit
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_bool]
        ret=func(self._ptr,col_,unit_,err_on_fail)
        return ret


class uniform_grid:
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/uniform_grid.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_uniform_grid_
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
        Delete function for class uniform_grid
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid
        
        Returns: a uniform_grid object
        """

        new_obj=type(self)(self._link,self._ptr)
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


class uniform_grid_end(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_end``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/uniform_grid_end.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_end

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_uniform_grid_end_
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
        Delete function for class uniform_grid_end
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_end_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_end
        
        Returns: a uniform_grid_end object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,n_bins):
        """
        Constructor-like class method for uniform_grid_end<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_uniform_grid_end__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(link,f(start,end,n_bins))


class uniform_grid_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_width``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/uniform_grid_width.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_width

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_uniform_grid_width_
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
        Delete function for class uniform_grid_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_width_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_width
        
        Returns: a uniform_grid_width object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,width,n_bins):
        """
        Constructor-like class method for uniform_grid_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_uniform_grid_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(link,f(start,width,n_bins))


class uniform_grid_end_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_end_width``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/uniform_grid_end_width.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_end_width

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_uniform_grid_end_width_
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
        Delete function for class uniform_grid_end_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_end_width_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_end_width
        
        Returns: a uniform_grid_end_width object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,width):
        """
        Constructor-like class method for uniform_grid_end_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_uniform_grid_end_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double]
        return cls(link,f(start,end,width))


class uniform_grid_log_end(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_log_end``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/uniform_grid_log_end.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_log_end

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_uniform_grid_log_end_
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
        Delete function for class uniform_grid_log_end
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_log_end_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_log_end
        
        Returns: a uniform_grid_log_end object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,n_bins):
        """
        Constructor-like class method for uniform_grid_log_end<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_uniform_grid_log_end__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(link,f(start,end,n_bins))


class uniform_grid_log_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_log_width``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/uniform_grid_log_width.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_log_width

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_uniform_grid_log_width_
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
        Delete function for class uniform_grid_log_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_log_width_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_log_width
        
        Returns: a uniform_grid_log_width object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,width,n_bins):
        """
        Constructor-like class method for uniform_grid_log_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_uniform_grid_log_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        return cls(link,f(start,width,n_bins))


class uniform_grid_log_end_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_log_end_width``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/uniform_grid_log_end_width.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_log_end_width

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_uniform_grid_log_end_width_
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
        Delete function for class uniform_grid_log_end_width
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_uniform_grid_log_end_width_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class uniform_grid_log_end_width
        
        Returns: a uniform_grid_log_end_width object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,width):
        """
        Constructor-like class method for uniform_grid_log_end_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_uniform_grid_log_end_width__init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double]
        return cls(link,f(start,end,width))


class table3d:
    """
    Python interface for O\ :sub:`2`\ scl class ``table3d``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/table3d.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class table3d

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_table3d
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
        Delete function for class table3d
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_table3d
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class table3d
        
        Returns: a table3d object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class table3d
        
        Returns: a new copy of the table3d object
        """

        new_obj=type(self)(self._link)
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
        | *x_name*: string
        | *nx*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y_name*: string
        | *ny*: ``size_t``
        | *y*: :class:`std_vector` object
        """
        x_name_=ctypes.c_char_p(force_bytes(x_name))
        y_name_=ctypes.c_char_p(force_bytes(y_name))
        func=self._link.o2scl.o2scl_table3d_set_xy
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,x_name_,nx,x._ptr,y_name_,ny,y._ptr)
        return

    def set_xy_grid(self,x_name,x_grid,y_name,y_grid):
        """
        | Parameters:
        | *x_name*: string
        | *x_grid*: :class:`uniform_grid<double>` object
        | *y_name*: string
        | *y_grid*: :class:`uniform_grid<double>` object
        """
        x_name_=ctypes.c_char_p(force_bytes(x_name))
        y_name_=ctypes.c_char_p(force_bytes(y_name))
        func=self._link.o2scl.o2scl_table3d_set_xy_grid
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p]
        func(self._ptr,x_name_,x_grid._ptr,y_name_,y_grid._ptr)
        return

    def set(self,ix,iy,name,val):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *iy*: ``size_t``
        | *name*: string
        | *val*: ``double``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_set
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,ix,iy,name_,val)
        return

    def get(self,ix,iy,name):
        """
        | Parameters:
        | *ix*: ``size_t``
        | *iy*: ``size_t``
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_char_p]
        ret=func(self._ptr,ix,iy,name_)
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
        | *name*: string
        | *val*: ``double``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_set_val
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,x,y,name_,val)
        return

    def get_val(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_get_val
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,x,y,name_)
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
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def new_slice(self,slice):
        """
        | Parameters:
        | *slice*: string
        """
        slice_=ctypes.c_char_p(force_bytes(slice))
        func=self._link.o2scl.o2scl_table3d_new_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,slice_)
        return

    def set_slice_all(self,name,val):
        """
        | Parameters:
        | *name*: string
        | *val*: ``double``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_set_slice_all
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,name_,val)
        return

    def lookup_slice(self,name):
        """
        | Parameters:
        | *name*: string
        | Returns: a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_lookup_slice
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,name_)
        return ret

    def is_slice(self,name):
        """
        | Parameters:
        | *name*: string
        | Returns: a Python boolean, a Python int
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_is_slice
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
        ix_conv=ctypes.c_size_t(0)
        ret=func(self._ptr,name_,ctypes.byref(ix_conv))
        return ret,ix_conv.value

    def rename_slice(self,name1,name2):
        """
        | Parameters:
        | *name1*: string
        | *name2*: string
        """
        name1_=ctypes.c_char_p(force_bytes(name1))
        name2_=ctypes.c_char_p(force_bytes(name2))
        func=self._link.o2scl.o2scl_table3d_rename_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,name1_,name2_)
        return

    def copy_slice(self,name1,name2):
        """
        | Parameters:
        | *name1*: string
        | *name2*: string
        """
        name1_=ctypes.c_char_p(force_bytes(name1))
        name2_=ctypes.c_char_p(force_bytes(name2))
        func=self._link.o2scl.o2scl_table3d_copy_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,name1_,name2_)
        return

    def get_slice(self,slice):
        """
        | Parameters:
        | *slice*: string
        | Returns: :class:`ublas_matrix` object
        """
        slice_=ctypes.c_char_p(force_bytes(slice))
        func=self._link.o2scl.o2scl_table3d_get_slice
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,slice_)
        ret2=ublas_matrix(self._link,ret)
        return ret2

    def get_slice_i(self,slice):
        """
        | Parameters:
        | *slice*: string
        | Returns: :class:`ublas_matrix` object
        """
        slice_=ctypes.c_char_p(force_bytes(slice))
        func=self._link.o2scl.o2scl_table3d_get_slice_i
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,slice_)
        ret2=ublas_matrix(self._link,ret)
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
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_interp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,x,y,name_)
        return ret

    def deriv_x(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_deriv_x
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,x,y,name_)
        return ret

    def deriv_y(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_deriv_y
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,x,y,name_)
        return ret

    def deriv_xy(self,x,y,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y*: ``double``
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_deriv_xy
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,x,y,name_)
        return ret

    def integ_x(self,x1,x2,y,name):
        """
        | Parameters:
        | *x1*: ``double``
        | *x2*: ``double``
        | *y*: ``double``
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_integ_x
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,x1,x2,y,name_)
        return ret

    def integ_y(self,x,y1,y2,name):
        """
        | Parameters:
        | *x*: ``double``
        | *y1*: ``double``
        | *y2*: ``double``
        | *name*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_integ_y
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,x,y1,y2,name_)
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
        | *function*: string
        | *mat*: :class:`ublas_matrix` object
        | *throw_on_err*: ``bool``
        | Returns: a Python int
        """
        function_=ctypes.c_char_p(force_bytes(function))
        func=self._link.o2scl.o2scl_table3d_function_matrix
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_bool]
        ret=func(self._ptr,function_,mat._ptr,throw_on_err)
        return ret

    def function_slice(self,function,slice):
        """
        | Parameters:
        | *function*: string
        | *slice*: string
        """
        function_=ctypes.c_char_p(force_bytes(function))
        slice_=ctypes.c_char_p(force_bytes(slice))
        func=self._link.o2scl.o2scl_table3d_function_slice
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,function_,slice_)
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
    Python interface for O\ :sub:`2`\ scl class ``index_spec``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/index_spec.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class index_spec

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_index_spec
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
        Delete function for class index_spec
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_index_spec
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class index_spec
        
        Returns: a index_spec object
        """

        new_obj=type(self)(self._link,self._ptr)
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


class tensor:
    """
    Python interface for O\ :sub:`2`\ scl class ``tensor``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/tensor.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class tensor

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_tensor_
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
        Delete function for class tensor
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor
        
        Returns: a tensor object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor
        
        Returns: a new copy of the tensor object
        """

        new_obj=type(self)(self._link)
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
        ret2=std_vector_size_t(self._link,ret)
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

    def convert_table3d_sum(self,ix_x,ix_y,tab,x_name="x",y_name="y",slice_name="z"):
        """
        | Parameters:
        | *ix_x*: ``size_t``
        | *ix_y*: ``size_t``
        | *tab*: :class:`table3d` object
        | *x_name* ="x": string
        | *y_name* ="y": string
        | *slice_name* ="z": string
        """
        x_name_=ctypes.c_char_p(force_bytes(x_name))
        y_name_=ctypes.c_char_p(force_bytes(y_name))
        slice_name_=ctypes.c_char_p(force_bytes(slice_name))
        func=self._link.o2scl.o2scl_tensor__convert_table3d_sum
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,ix_x,ix_y,tab._ptr,x_name_,y_name_,slice_name_)
        return

    @classmethod
    def create_size(cls,link,rank,sizes):
        """
        Constructor-like class method for tensor<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_tensor__create_size
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_void_p]
        return cls(link,f(rank,sizes._ptr))

    def create_size(self,v):
        """
        Copy ``v`` to an :class:`std_vector_size_t` object and add the line of
        data to the table
        """
        # Create a std_vector object and copy the data over
        vec=std_vector_size_t(self._link)
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
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        self.set_vector(svst,val)
        return
     
    def get(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and get the 
        data from the table
        """
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        return self.get_vector(svst)
    
    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        self.resize_vector(len(svst),svst)
        return

class tensor_grid:
    """
    Python interface for O\ :sub:`2`\ scl class ``tensor_grid``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/tensor_grid.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class tensor_grid

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_tensor_grid_
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
        Delete function for class tensor_grid
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_grid_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor_grid
        
        Returns: a tensor_grid object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor_grid
        
        Returns: a new copy of the tensor_grid object
        """

        new_obj=type(self)(self._link)
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


class tensor_int:
    """
    Python interface for O\ :sub:`2`\ scl class ``tensor``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/tensor.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class tensor_int

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_tensor_int_std_vector_int_
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
        Delete function for class tensor_int
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_int_std_vector_int_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor_int
        
        Returns: a tensor_int object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor_int
        
        Returns: a new copy of the tensor_int object
        """

        new_obj=type(self)(self._link)
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
        ret2=std_vector_int(self._link,ret)
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

    def min_value(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__min_value
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def max_value(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__max_value
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def total_sum(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_int_std_vector_int__total_sum
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    @classmethod
    def create_size(cls,link,rank,sizes):
        """
        Constructor-like class method for tensor<int,std::vector<int>> .

        | Parameters:

        """

        f=link.o2scl.o2scl_tensor_int_std_vector_int__create_size
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_void_p]
        return cls(link,f(rank,sizes._ptr))

    def create_size(self,v):
        """
        Copy ``v`` to an :class:`std_vector_size_t` object and add the line of
        data to the table
        """
        # Create a std_vector object and copy the data over
        vec=std_vector_size_t(self._link)
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
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        self.set_vector(svst,val)
        return
     
    def get(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and get the 
        data from the table
        """
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        return self.get_vector(svst)
    
    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        self.resize_vector(svst)
        return

class tensor_size_t:
    """
    Python interface for O\ :sub:`2`\ scl class ``tensor``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/tensor.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class tensor_size_t

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_tensor_size_t_std_vector_size_t_
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
        Delete function for class tensor_size_t
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_tensor_size_t_std_vector_size_t_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class tensor_size_t
        
        Returns: a tensor_size_t object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class tensor_size_t
        
        Returns: a new copy of the tensor_size_t object
        """

        new_obj=type(self)(self._link)
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
        ret2=std_vector_size_t(self._link,ret)
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

    def max_value(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__max_value
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def total_sum(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor_size_t_std_vector_size_t__total_sum
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    @classmethod
    def create_size(cls,link,rank,sizes):
        """
        Constructor-like class method for tensor<size_t,std::vector<size_t>> .

        | Parameters:

        """

        f=link.o2scl.o2scl_tensor_size_t_std_vector_size_t__create_size
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_size_t,ctypes.c_void_p]
        return cls(link,f(rank,sizes._ptr))

    def create_size(self,v):
        """
        Copy ``v`` to an :class:`std_vector_size_t` object and add the line of
        data to the table
        """
        # Create a std_vector object and copy the data over
        vec=std_vector_size_t(self._link)
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
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        self.set_vector(svst,val)
        return
     
    def get(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and get the 
        data from the table
        """
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        return self.get_vector(svst)
    
    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=std_vector_size_t(self._link)
        svst.init_py(index)
        self.resize_vector(svst)
        return

class find_constants_const_entry:
    """
    Python interface for O\ :sub:`2`\ scl class ``find_constants::const_entry``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/find_constants::const_entry.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class find_constants_const_entry

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_find_constants_const_entry
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
        Delete function for class find_constants_const_entry
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_find_constants_const_entry
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class find_constants_const_entry
        
        Returns: a find_constants_const_entry object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def get_names(self,names):
        """
        Get object of type :class:`std::vector<std::string>`
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_names
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,names._ptr)
        return

    def set_names(self,value):
        """
        Set object of type :class:`std::vector<std::string>`
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_names
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_unit(self,unit):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_unit
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,unit._ptr)
        return

    def set_unit(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
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
        Setter function for find_constants::const_entry::unit_flag .
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
        Setter function for find_constants::const_entry::val .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_val
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def get_source(self,source):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_get_source
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,source._ptr)
        return

    def set_source(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_source
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
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
        Setter function for find_constants::const_entry::m .
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
        Setter function for find_constants::const_entry::k .
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
        Setter function for find_constants::const_entry::s .
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
        Setter function for find_constants::const_entry::K .
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
        Setter function for find_constants::const_entry::A .
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
        Setter function for find_constants::const_entry::mol .
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
        Setter function for find_constants::const_entry::cd .
        """
        func=self._link.o2scl.o2scl_find_constants_const_entry_set_cd
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return


class find_constants:
    """
    Python interface for O\ :sub:`2`\ scl class ``find_constants``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/find_constants.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class find_constants

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_find_constants
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
        Delete function for class find_constants
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_find_constants
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class find_constants
        
        Returns: a find_constants object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def find_print(self,name,unit,prec,verbose):
        """
        | Parameters:
        | *name*: string
        | *unit*: string
        | *prec*: ``size_t``
        | *verbose*: ``int``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        unit_=ctypes.c_char_p(force_bytes(unit))
        func=self._link.o2scl.o2scl_find_constants_find_print
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_int]
        func(self._ptr,name_,unit_,prec,verbose)
        return

    def find_unique(self,name,unit):
        """
        | Parameters:
        | *name*: string
        | *unit*: string
        | Returns: a Python float
        """
        name_=ctypes.c_char_p(force_bytes(name))
        unit_=ctypes.c_char_p(force_bytes(unit))
        func=self._link.o2scl.o2scl_find_constants_find_unique
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,name_,unit_)
        return ret

    def output_list_cout(self):
        """
        """
        func=self._link.o2scl.o2scl_find_constants_output_list_cout
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def add_constant(self,f,verbose=0):
        """
        | Parameters:
        | *f*: :class:`find_constants::const_entry` object
        | *verbose* =0: ``int``
        """
        func=self._link.o2scl.o2scl_find_constants_add_constant
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,f._ptr,verbose)
        return

    def del_constant(self,name,verbose=0):
        """
        | Parameters:
        | *name*: :class:`std_string` object
        | *verbose* =0: ``int``
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_find_constants_del_constant
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,name._ptr,verbose)
        return


class convert_units_der_unit:
    """
    Python interface for O\ :sub:`2`\ scl class ``convert_units<>::der_unit``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/convert_units<>::der_unit.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class convert_units_der_unit

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_convert_units_der_unit
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
        Delete function for class convert_units_der_unit
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_convert_units_der_unit
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class convert_units_der_unit
        
        Returns: a convert_units_der_unit object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def get_label(self,label):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_label
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,label._ptr)
        return

    def set_label(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_label
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
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

    def get_name(self,name):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_get_name
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,name._ptr)
        return

    def set_name(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_convert_units_der_unit_set_name
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def set(self,label,val,name='',m=0,k=0,s=0,K=0,A=0,mol=0,cd=0):
        """
        Set the properties of a derived unit
        FIXME: beter docs here
        """
        label2=std_string(self._link)
        label2.init_bytes(force_bytes(label))
        self.set_label(label2)
        self.val=val
        name2=std_string(self._link)
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
    Python interface for O\ :sub:`2`\ scl class ``convert_units``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/convert_units.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class convert_units

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_convert_units_
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
        Delete function for class convert_units
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_convert_units_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class convert_units
        
        Returns: a convert_units object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        | *frm*: string
        | *to*: string
        | *val*: ``double``
        | Returns: a Python float
        """
        frm_=ctypes.c_char_p(force_bytes(frm))
        to_=ctypes.c_char_p(force_bytes(to))
        func=self._link.o2scl.o2scl_convert_units__convert
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double]
        ret=func(self._ptr,frm_,to_,val)
        return ret

    def convert_ret(self,frm,to,val,converted):
        """
        | Parameters:
        | *frm*: string
        | *to*: string
        | *val*: ``double``
        | *converted*: ``double``
        | Returns: a Python int
        """
        frm_=ctypes.c_char_p(force_bytes(frm))
        to_=ctypes.c_char_p(force_bytes(to))
        func=self._link.o2scl.o2scl_convert_units__convert_ret
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,frm_,to_,val,converted)
        return ret

    def del_unit(self,name):
        """
        | Parameters:
        | *name*: :class:`std_string` object
        """
        name_=ctypes.c_char_p(force_bytes(name))
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
        | *frm*: string
        | *to*: string
        | Returns: a Python int
        """
        frm_=ctypes.c_char_p(force_bytes(frm))
        to_=ctypes.c_char_p(force_bytes(to))
        func=self._link.o2scl.o2scl_convert_units__is_in_cache
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,frm_,to_)
        return ret

    def remove_cache(self,frm,to):
        """
        | Parameters:
        | *frm*: string
        | *to*: string
        | Returns: a Python int
        """
        frm_=ctypes.c_char_p(force_bytes(frm))
        to_=ctypes.c_char_p(force_bytes(to))
        func=self._link.o2scl.o2scl_convert_units__remove_cache
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        ret=func(self._ptr,frm_,to_)
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

    def add_unit(self,label,val,name='',m=0,k=0,s=0,K=0,A=0,mol=0,cd=0):
        """
        Add a unit
        """
        du=convert_units_der_unit(self._link)
        du.set(label,val,name,m,k,s,K,A,mol,cd)
        self.add_unit_internal(du)
        return

class columnify:
    """
    Python interface for O\ :sub:`2`\ scl class ``columnify``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/columnify.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class columnify

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_columnify
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
        Delete function for class columnify
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_columnify
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class columnify
        
        Returns: a columnify object
        """

        new_obj=type(self)(self._link,self._ptr)
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
    Python interface for O\ :sub:`2`\ scl class ``format_float``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/format_float.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class format_float

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_format_float
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
        Delete function for class format_float
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_format_float
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class format_float
        
        Returns: a format_float object
        """

        new_obj=type(self)(self._link,self._ptr)
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
        | *dec_point*: string
        """
        dec_point_=ctypes.c_char_p(force_bytes(dec_point))
        func=self._link.o2scl.o2scl_format_float_set_dec_point
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,dec_point_)
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
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()


class interp:
    """
    Python interface for O\ :sub:`2`\ scl class ``interp<std::vector<double>>``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/interp<std::vector<double>>.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class interp

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_interp_std_vector_double_
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
        Delete function for class interp
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_interp_std_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class interp
        
        Returns: a interp object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def eval(self,x0,n,x,y):
        """
        | Parameters:
        | *x0*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y*: :class:`std_vector` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_std_vector_double__eval
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,x0,n,x._ptr,y._ptr)
        return ret

    def deriv(self,x0,n,x,y):
        """
        | Parameters:
        | *x0*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y*: :class:`std_vector` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_std_vector_double__deriv
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,x0,n,x._ptr,y._ptr)
        return ret

    def deriv2(self,x0,n,x,y):
        """
        | Parameters:
        | *x0*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y*: :class:`std_vector` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_std_vector_double__deriv2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,x0,n,x._ptr,y._ptr)
        return ret

    def integ(self,x1,x2,n,x,y):
        """
        | Parameters:
        | *x1*: ``double``
        | *x2*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std_vector` object
        | *y*: :class:`std_vector` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_interp_std_vector_double__integ
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,x1,x2,n,x._ptr,y._ptr)
        return ret

    def set_type(self,interp_type):
        """
        | Parameters:
        | *interp_type*: ``int``
        """
        func=self._link.o2scl.o2scl_interp_std_vector_double__set_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,interp_type)
        return


class interp_vec:
    """
    Python interface for O\ :sub:`2`\ scl class ``interp_vec<std::vector<double>>``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/interp_vec<std::vector<double>>.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class interp_vec

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_interp_vec_std_vector_double_
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
        Delete function for class interp_vec
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_interp_vec_std_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class interp_vec
        
        Returns: a interp_vec object
        """

        new_obj=type(self)(self._link,self._ptr)
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


class interp_krige_optim:
    """
    Python interface for O\ :sub:`2`\ scl class ``interp_krige_optim<std::vector<double>>``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/interp_krige_optim<std::vector<double>>.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class interp_krige_optim

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_interp_krige_optim_std_vector_double_
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
        Delete function for class interp_krige_optim
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_interp_krige_optim_std_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class interp_krige_optim
        
        Returns: a interp_krige_optim object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def verbose(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for interp_krige_optim<std::vector<double>>::verbose .
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def mode(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__get_mode
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mode.setter
    def mode(self,value):
        """
        Setter function for interp_krige_optim<std::vector<double>>::mode .
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__set_mode
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def nlen(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__get_nlen
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nlen.setter
    def nlen(self,value):
        """
        Setter function for interp_krige_optim<std::vector<double>>::nlen .
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__set_nlen
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def full_min(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__get_full_min
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @full_min.setter
    def full_min(self,value):
        """
        Setter function for interp_krige_optim<std::vector<double>>::full_min .
        """
        func=self._link.o2scl.o2scl_interp_krige_optim_std_vector_double__set_full_min
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return


class gen_test_number:
    """
    Python interface for O\ :sub:`2`\ scl class ``gen_test_number<double>``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/gen_test_number<double>.html .
    
    Note that python complex numbers are immutable, but this class is
    not, so the real and imaginary parts can be changed with real_set()
    and imag_set(). 
                                 
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class gen_test_number

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_gen_test_number_double_
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
        Delete function for class gen_test_number
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_gen_test_number_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class gen_test_number
        
        Returns: a gen_test_number object
        """

        new_obj=type(self)(self._link,self._ptr)
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


class shared_ptr_table_units(table_units):
    """
    Python interface for a shared pointer to a class of type ``table_units<>``
    """

    _s_ptr=0
    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,shared_ptr=0):
        """
        Init function for shared_ptr_table_units .
        """

        self._link=link
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

def ix_index(link,ix):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_index_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t]
    ret=func(ix)
    return ret

def ix_fixed(link,ix,ix2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | *ix2*: ``size_t``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_fixed_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t,ctypes.c_size_t]
    ret=func(ix,ix2)
    return ret

def ix_sum(link,ix):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_sum_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t]
    ret=func(ix)
    return ret

def ix_trace(link,ix,ix2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | *ix2*: ``size_t``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_trace_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t,ctypes.c_size_t]
    ret=func(ix,ix2)
    return ret

def ix_reverse(link,ix):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_reverse_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t]
    ret=func(ix)
    return ret

def ix_range(link,ix,start,end):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | *start*: ``size_t``
        | *end*: ``size_t``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_range_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t,ctypes.c_size_t,ctypes.c_size_t]
    ret=func(ix,start,end)
    return ret

def ix_interp(link,ix,v):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | *v*: ``double``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_interp_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t,ctypes.c_double]
    ret=func(ix,v)
    return ret

def ix_grid(link,ix,start,end,n_bins,log=False):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | *start*: ``double``
        | *end*: ``double``
        | *n_bins*: ``size_t``
        | *log*: ``bool``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_grid_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_size_t,ctypes.c_bool]
    ret=func(ix,start,end,n_bins,log)
    return ret

def ix_gridw(link,ix,start,end,width,log=False):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ix*: ``size_t``
        | *start*: ``double``
        | *end*: ``double``
        | *width*: ``double``
        | *log*: ``bool``
        | Returns: ``ctypes.c_index_spec`` object
    """
    func=link.o2scl.o2scl_ix_gridw_wrapper
    func.restype=ctypes.c_index_spec
    func.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_bool]
    ret=func(ix,start,end,width,log)
    return ret

def fermi_function(link,E,mu,T,limit=40.0):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *E*: ``double``
        | *mu*: ``double``
        | *T*: ``double``
        | *limit*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_fermi_function_wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    ret=func(E,mu,T,limit)
    return ret

def bose_function(link,E,mu,T,limit=40.0):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *E*: ``double``
        | *mu*: ``double``
        | *T*: ``double``
        | *limit*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_bose_function_wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    ret=func(E,mu,T,limit)
    return ret

def quadratic_extremum_x(link,x1,x2,x3,y1,y2,y3):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *x1*: ``double``
        | *x2*: ``double``
        | *x3*: ``double``
        | *y1*: ``double``
        | *y2*: ``double``
        | *y3*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_quadratic_extremum_x_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    ret=func(x1,x2,x3,y1,y2,y3)
    return ret

def quadratic_extremum_y(link,x1,x2,x3,y1,y2,y3):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *x1*: ``double``
        | *x2*: ``double``
        | *x3*: ``double``
        | *y1*: ``double``
        | *y2*: ``double``
        | *y3*: ``double``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_quadratic_extremum_y_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
    ret=func(x1,x2,x3,y1,y2,y3)
    return ret

def screenify(link,nin,in_cols,out_cols,max_size=80):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *nin*: ``size_t``
        | *in_cols*: :class:`vector<std::string>` object
        | *out_cols*: :class:`vector<std::string>` object
        | *max_size*: ``size_t``
    """
    func=link.o2scl.o2scl_screenify_vector_std_string__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(nin,in_cols._ptr,out_cols._ptr,max_size)
    return

def file_exists(link,fname):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *fname*: string
        | Returns: ``ctypes.c_bool`` object
    """
    fname_=ctypes.c_char_p(force_bytes(fname))
    func=link.o2scl.o2scl_file_exists_wrapper
    func.restype=ctypes.c_bool
    func.argtypes=[ctypes.c_char_p]
    ret=func(fname_)
    return ret

def RGBtoHSV(link,r,g,b,h,s,v):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *r*: ``double``
        | *g*: ``double``
        | *b*: ``double``
        | *h*: ``double``
        | *s*: ``double``
        | *v*: ``double``
    """
    func=link.o2scl.o2scl_RGBtoHSV_wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(r,g,b,h._ptr,s._ptr,v._ptr)
    return

def HSVtoRGB(link,h,s,v,r,g,b):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *h*: ``double``
        | *s*: ``double``
        | *v*: ``double``
        | *r*: ``double``
        | *g*: ``double``
        | *b*: ``double``
    """
    func=link.o2scl.o2scl_HSVtoRGB_wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(h,s,v,r._ptr,g._ptr,b._ptr)
    return

def wordexp_single_file(link,fname):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *fname*: :class:`std::string` object
    """
    fname.__del__()
    fname._ptr=ctypes.c_void_p()
    func=link.o2scl.o2scl_wordexp_single_file_wrapper
    func.argtypes=[ctypes.POINTER(ctypes.c_void_p)]
    func(ctypes.byref(fname._ptr))
    fname._owner=True
    return

def wordexp_wrapper(link,word,matches):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *word*: string
        | *matches*: :class:`std::vector<std::string>` object
    """
    word_=ctypes.c_char_p(force_bytes(word))
    func=link.o2scl.o2scl_wordexp_wrapper_wrapper
    func.argtypes=[ctypes.c_char_p,ctypes.c_void_p]
    func(word_,matches._ptr)
    return

def function_to_double(link,s,verbose=0):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *s*: string
        | *verbose*: ``int``
        | Returns: ``ctypes.c_double`` object
    """
    s_=ctypes.c_char_p(force_bytes(s))
    func=link.o2scl.o2scl_function_to_double_wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_char_p,ctypes.c_int]
    ret=func(s_,verbose)
    return ret

def function_to_double_nothrow(link,s,result,verbose=0):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *s*: string
        | *result*: ``double``
        | *verbose*: ``int``
        | Returns: ``ctypes.c_int`` object
    """
    s_=ctypes.c_char_p(force_bytes(s))
    func=link.o2scl.o2scl_function_to_double_nothrow_wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_int]
    ret=func(s_,result._ptr,verbose)
    return ret

def string_to_uint_list(link,x,list):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *x*: :class:`std::string` object
        | *list*: :class:`vector<size_t>` object
        | Returns: ``ctypes.c_int`` object
    """
    x.__del__()
    x._ptr=ctypes.c_void_p()
    func=link.o2scl.o2scl_string_to_uint_list_vector_size_t__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.POINTER(ctypes.c_void_p),ctypes.c_void_p]
    ret=func(ctypes.byref(x._ptr),list._ptr)
    x._owner=True
    return ret

def vector_level_count(link,level,n,x,y):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *level*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | Returns: ``ctypes.c_size_t`` object
    """
    func=link.o2scl.o2scl_vector_level_count_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_size_t
    func.argtypes=[ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p]
    ret=func(level,n,x._ptr,y._ptr)
    return ret

def vector_deriv_interp(link,n,v,dv,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *v*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=link.o2scl.o2scl_vector_deriv_interp_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,v._ptr,dv._ptr,interp_type)
    return

def vector_deriv2_interp(link,n,v,dv,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *v*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=link.o2scl.o2scl_vector_deriv2_interp_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,v._ptr,dv._ptr,interp_type)
    return

def vector_deriv_xy_interp(link,n,vx,vy,dv,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=link.o2scl.o2scl_vector_deriv_xy_interp_std_vector_double_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,vx._ptr,vy._ptr,dv._ptr,interp_type)
    return

def vector_deriv2_xy_interp(link,n,vx,vy,dv,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *dv*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
    """
    func=link.o2scl.o2scl_vector_deriv2_xy_interp_std_vector_double_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    func(n,vx._ptr,vy._ptr,dv._ptr,interp_type)
    return

def vector_integ_interp(link,n,vx,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_vector_integ_interp_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,vx._ptr,interp_type)
    return ret

def vector_integ_xy_interp(link,n,vx,vy,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_vector_integ_xy_interp_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,vx._ptr,vy._ptr,interp_type)
    return ret

def vector_integ_ul_interp(link,n,x2,v,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *x2*: ``double``
        | *v*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_vector_integ_ul_interp_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,x2,v._ptr,interp_type)
    return ret

def vector_integ_ul_xy_interp(link,n,x2,vx,vy,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *x2*: ``double``
        | *vx*: :class:`std::vector<double>` object
        | *vy*: :class:`std::vector<double>` object
        | *interp_type*: ``size_t``
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_vector_integ_ul_xy_interp_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_size_t,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
    ret=func(n,x2,vx._ptr,vy._ptr,interp_type)
    return ret

def vector_find_level(link,level,n,x,y,locs):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *level*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *locs*: :class:`std::vector<double>` object
    """
    func=link.o2scl.o2scl_vector_find_level_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(level,n,x._ptr,y._ptr,locs._ptr)
    return

def vector_invert_enclosed_sum(link,sum,n,x,y,lev,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *sum*: ``double``
        | *n*: ``size_t``
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *lev*: ``double``
        | *boundaries*: ``int``
        | *verbose*: ``int``
        | *err_on_fail*: ``bool``
    """
    func=link.o2scl.o2scl_vector_invert_enclosed_sum_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_double,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    func(sum,n,x._ptr,y._ptr,lev._ptr,boundaries,verbose,err_on_fail)
    return

def vector_region_int(link,n,x,y,intl,locs,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
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
    func=link.o2scl.o2scl_vector_region_int_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,intl,locs._ptr,boundaries,verbose,err_on_fail)
    return ret

def vector_region_fracint(link,n,x,y,intl,locs,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
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
    func=link.o2scl.o2scl_vector_region_fracint_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,intl,locs._ptr,boundaries,verbose,err_on_fail)
    return ret

def vector_bound_fracint(link,n,x,y,frac,low,high,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
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
    func=link.o2scl.o2scl_vector_bound_fracint_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,frac,low._ptr,high._ptr,boundaries,verbose,err_on_fail)
    return ret

def vector_bound_int(link,n,x,y,frac,low,high,boundaries=0,verbose=0,err_on_fail=True):
    """
        | Parameters:
        | *link* :class:`linker` object
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
    func=link.o2scl.o2scl_vector_bound_int_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_int
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ret=func(n,x._ptr,y._ptr,frac,low._ptr,high._ptr,boundaries,verbose,err_on_fail)
    return ret

def rebin_xy(link,x,y,x_out,y_out,n_pts,interp_type):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *x_out*: :class:`std::vector<double>` object
        | *y_out*: :class:`std::vector<double>` object
        | *n_pts*: ``size_t``
        | *interp_type*: ``size_t``
    """
    func=link.o2scl.o2scl_rebin_xy_std_vector_double_std_vector_double_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
    func(x._ptr,y._ptr,x_out._ptr,y_out._ptr,n_pts,interp_type)
    return

def linear_or_log_chi2(link,x,y):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | Returns: ``ctypes.c_double`` object
    """
    func=link.o2scl.o2scl_linear_or_log_chi2_std_vector_double_std_vector_double__wrapper
    func.restype=ctypes.c_double
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    ret=func(x._ptr,y._ptr)
    return ret

def linear_or_log_pair(link,x,y,log_x,log_y):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *x*: :class:`std::vector<double>` object
        | *y*: :class:`std::vector<double>` object
        | *log_x*: ``bool``
        | *log_y*: ``bool``
    """
    func=link.o2scl.o2scl_linear_or_log_std_vector_double_std_vector_double__wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    func(x._ptr,y._ptr,log_x._ptr,log_y._ptr)
    return

def vector_refine(link,n,index,data,factor,interp_type=2):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *n*: ``size_t``
        | *index*: :class:`std::vector<double>` object
        | *data*: :class:`std::vector<double>` object
        | *factor*: ``size_t``
        | *interp_type*: ``size_t``
    """
    func=link.o2scl.o2scl_vector_refine_std_vector_double_std_vector_double_double__wrapper
    func.argtypes=[ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
    func(n,index._ptr,data._ptr,factor,interp_type)
    return

def linear_or_log(link,x,log_x):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *x*: :class:`std::vector<double>` object
        | *log_x*: ``bool``
    """
    func=link.o2scl.o2scl_linear_or_log_std_vector_double__wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
    func(x._ptr,log_x._ptr)
    return

