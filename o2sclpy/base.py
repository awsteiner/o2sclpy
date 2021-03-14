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
import numpy


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
            f=link.o2scl.o2scl_create_std__string
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
            f=self._link.o2scl.o2scl_free_std__string
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
        func=self._link.o2scl.o2scl_std__string_length
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std__string_getitem
        func.restype=ctypes.c_char
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        func=self._link.o2scl.o2scl_std__string_setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char]
        func(self._ptr,i,value)
        return

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std__string_resize
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
            f=link.o2scl.o2scl_create_std__vector_double_
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
            f=self._link.o2scl.o2scl_free_std__vector_double_
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
        func=self._link.o2scl.o2scl_std__vector_double__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std__vector_double__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std__vector_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        func=self._link.o2scl.o2scl_std__vector_double__setitem
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
            f=link.o2scl.o2scl_create_std__vector_int_
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
            f=self._link.o2scl.o2scl_free_std__vector_int_
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
        func=self._link.o2scl.o2scl_std__vector_int__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std__vector_int__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std__vector_int__getitem
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        func=self._link.o2scl.o2scl_std__vector_int__setitem
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
            f=link.o2scl.o2scl_create_std__vector_size_t_
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
            f=self._link.o2scl.o2scl_free_std__vector_size_t_
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
        func=self._link.o2scl.o2scl_std__vector_size_t__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std__vector_size_t__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std__vector_size_t__getitem
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        func=self._link.o2scl.o2scl_std__vector_size_t__setitem
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
            f=link.o2scl.o2scl_create_std__vector_std__string_
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
            f=self._link.o2scl.o2scl_free_std__vector_std__string_
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
        func=self._link.o2scl.o2scl_std__vector_std__string__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std__vector_std__string__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

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
            f=link.o2scl.o2scl_create_boost__numeric__ublas__vector_double_
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
            f=self._link.o2scl.o2scl_free_boost__numeric__ublas__vector_double_
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
        func=self._link.o2scl.o2scl_boost__numeric__ublas__vector_double__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost__numeric__ublas__vector_double__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def __getitem__(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost__numeric__ublas__vector_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def __setitem__(self,i,value):
        func=self._link.o2scl.o2scl_boost__numeric__ublas__vector_double__setitem
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
            f=link.o2scl.o2scl_create_boost__numeric__ublas__matrix_double_
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
            f=self._link.o2scl.o2scl_free_boost__numeric__ublas__matrix_double_
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
        func=self._link.o2scl.o2scl_boost__numeric__ublas__matrix_double__size1
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def size2(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_boost__numeric__ublas__matrix_double__size2
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
        func=self._link.o2scl.o2scl_boost__numeric__ublas__matrix_double__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,m,n)
        return

    def __getitem__(self,tup):
        """
        | Parameters:
        | *m*: ``size_t``
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_boost__numeric__ublas__matrix_double__getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        m,n=tup
        ret=func(self._ptr,m,n)
        return ret

    def __setitem__(self,tup,value):
        m,n=tup
        func=self._link.o2scl.o2scl_boost__numeric__ublas__matrix_double__setitem
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

class lib_settings_class:
    """
    Python interface for O\ :sub:`2`\ scl class ``lib_settings_class``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/lib_settings_class.html .
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
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_data_dir
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

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
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_doc_dir
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

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
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_eos_installed
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def part_installed(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_part_installed
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def hdf_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_hdf_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def openmp_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_openmp_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def readline_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_readline_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def ncurses_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_ncurses_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def gsl2_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_gsl2_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def armadillo_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_armadillo_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def eigen_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_eigen_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def fftw_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_fftw_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def python_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_python_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def hdf5_compression_support(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_hdf5_compression_support
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def system_type(self):
        """
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_system_type
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

    def range_check(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_range_check
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def time_compiled(self):
        """
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_time_compiled
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

    def date_compiled(self):
        """
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_date_compiled
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

    def o2scl_version(self):
        """
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_o2scl_version
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

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
            f=link.o2scl.o2scl_create_table__
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
            f=self._link.o2scl.o2scl_free_table__
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
        f2=self._link.o2scl.o2scl_copy_table__
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def __getitem__(self,col):
        """
        | Parameters:
        | *col*: string
        | Returns: :class:`std::vector<double>` object
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table___getitem
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
        func=self._link.o2scl.o2scl_table___set
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
        func=self._link.o2scl.o2scl_table___get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        ret=func(self._ptr,col_,row)
        return ret

    def get_ncolumns(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table___get_ncolumns
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_nlines(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table___get_nlines
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_nlines(self,lines):
        """
        | Parameters:
        | *lines*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table___set_nlines
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,lines)
        return

    def get_maxlines(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table___get_maxlines
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_maxlines(self,llines):
        """
        | Parameters:
        | *llines*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table___set_maxlines
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,llines)
        return

    def set_nlines_auto(self,il):
        """
        | Parameters:
        | *il*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table___set_nlines_auto
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,il)
        return

    def inc_maxlines(self,llines):
        """
        | Parameters:
        | *llines*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table___inc_maxlines
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,llines)
        return

    def new_column(self,col):
        """
        | Parameters:
        | *col*: string
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table___new_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,col_)
        return

    def get_column(self,col):
        """
        | Parameters:
        | *col*: string
        | Returns: ``numpy`` array
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table___get_column
        n_=ctypes.c_int(0)
        ptr_=ctypes.POINTER(ctypes.c_double)()
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),ctypes.POINTER(ctypes.c_int)]
        func(self._ptr,col_,ctypes.byref(ptr_),ctypes.byref(n_))
        ret=numpy.ctypeslib.as_array(ptr_,shape=(n_.value,))
        return ret

    def get_column_name(self,icol):
        """
        | Parameters:
        | *icol*: ``size_t``
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_table___get_column_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,icol)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

    def rename_column(self,src,dest):
        """
        | Parameters:
        | *src*: string
        | *dest*: string
        """
        src_=ctypes.c_char_p(force_bytes(src))
        dest_=ctypes.c_char_p(force_bytes(dest))
        func=self._link.o2scl.o2scl_table___rename_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,src_,dest_)
        return

    def delete_column(self,col):
        """
        | Parameters:
        | *col*: string
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table___delete_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,col_)
        return

    def get_sorted_name(self,icol):
        """
        | Parameters:
        | *icol*: ``size_t``
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_table___get_sorted_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,icol)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

    def init_column(self,scol,val):
        """
        | Parameters:
        | *scol*: string
        | *val*: ``double``
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table___init_column
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,scol_,val)
        return

    def is_column(self,scol):
        """
        | Parameters:
        | *scol*: string
        | Returns: ``ctypes.c_bool`` object
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table___is_column
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
        func=self._link.o2scl.o2scl_table___lookup_column
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
        func=self._link.o2scl.o2scl_table___copy_column
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
        func=self._link.o2scl.o2scl_table___add_col_from_table
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
        func=self._link.o2scl.o2scl_table___insert_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool,ctypes.c_char_p]
        func(self._ptr,source._ptr,src_index_,allow_extrap,dest_index_)
        return

    def add_table(self,source):
        """
        | Parameters:
        | *source*: :class:`table<>` object
        """
        func=self._link.o2scl.o2scl_table___add_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,source._ptr)
        return

    def new_row(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table___new_row
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def copy_row(self,src,dest):
        """
        | Parameters:
        | *src*: ``size_t``
        | *dest*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table___copy_row
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
        func=self._link.o2scl.o2scl_table___delete_row
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
        func(self._ptr,scol_,val)
        return

    def delete_rows_func(self,func):
        """
        | Parameters:
        | *func*: string
        """
        func_=ctypes.c_char_p(force_bytes(func))
        func=self._link.o2scl.o2scl_table___delete_rows_func
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,func_)
        return

    def line_of_names(self,names):
        """
        | Parameters:
        | *names*: string
        """
        names_=ctypes.c_char_p(force_bytes(names))
        func=self._link.o2scl.o2scl_table___line_of_names
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,names_)
        return

    def line_of_data_vector(self,data):
        """
        | Parameters:
        | *data*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_table___line_of_data
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
        func=self._link.o2scl.o2scl_table___ordered_lookup
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
        func=self._link.o2scl.o2scl_table___lookup
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
        func=self._link.o2scl.o2scl_table___lookup_val
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_char_p]
        ret=func(self._ptr,scol_,val,scol2_)
        return ret

    def set_interp_type(self,interp_type):
        """
        | Parameters:
        | *interp_type*: ``size_t``
        """
        func=self._link.o2scl.o2scl_table___set_interp_type
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,interp_type)
        return

    def get_interp_type(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_table___get_interp_type
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
        func=self._link.o2scl.o2scl_table___interp
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
        func=self._link.o2scl.o2scl_table___interp_index
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
        func=self._link.o2scl.o2scl_table___deriv_col
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
        func=self._link.o2scl.o2scl_table___deriv
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
        func=self._link.o2scl.o2scl_table___deriv_index
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
        func=self._link.o2scl.o2scl_table___deriv2_col
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
        func=self._link.o2scl.o2scl_table___deriv2
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
        func=self._link.o2scl.o2scl_table___deriv2_index
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
        func=self._link.o2scl.o2scl_table___integ
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
        func=self._link.o2scl.o2scl_table___integ_index
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
        func=self._link.o2scl.o2scl_table___integ_col
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
        func=self._link.o2scl.o2scl_table___max
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
        func=self._link.o2scl.o2scl_table___min
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,min_)
        return ret

    def zero_table(self):
        """
        """
        func=self._link.o2scl.o2scl_table___zero_table
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_table___clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear_data(self):
        """
        """
        func=self._link.o2scl.o2scl_table___clear_data
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear_table(self):
        """
        """
        func=self._link.o2scl.o2scl_table___clear_table
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear_constants(self):
        """
        """
        func=self._link.o2scl.o2scl_table___clear_constants
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def sort_table(self,scol):
        """
        | Parameters:
        | *scol*: string
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table___sort_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,scol_)
        return

    def sort_column(self,scol):
        """
        | Parameters:
        | *scol*: string
        """
        scol_=ctypes.c_char_p(force_bytes(scol))
        func=self._link.o2scl.o2scl_table___sort_column
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
        func=self._link.o2scl.o2scl_table___average_col_roll
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        func(self._ptr,col_name_,window)
        return

    def average_rows(self,window,rolling):
        """
        | Parameters:
        | *window*: ``size_t``
        | *rolling*: ``bool``
        """
        func=self._link.o2scl.o2scl_table___average_rows
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_bool]
        func(self._ptr,window,rolling)
        return

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_table___is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def functions_columns(self,list):
        """
        | Parameters:
        | *list*: string
        """
        list_=ctypes.c_char_p(force_bytes(list))
        func=self._link.o2scl.o2scl_table___functions_columns
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
        func=self._link.o2scl.o2scl_table___function_column
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
        func=self._link.o2scl.o2scl_table___row_function
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
        func=self._link.o2scl.o2scl_table___function_find_row
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,function_)
        return ret

    def summary(self):
        """
        """
        func=self._link.o2scl.o2scl_table___summary
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
            f=link.o2scl.o2scl_create_table_units__
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
            f=self._link.o2scl.o2scl_free_table_units__
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
        f2=self._link.o2scl.o2scl_copy_table_units__
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
        func=self._link.o2scl.o2scl_table_units___set_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,col_,unit_)
        return

    def get_unit(self,col):
        """
        | Parameters:
        | *col*: string
        | Returns: std_string object
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table_units___get_unit
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,col_)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

    def line_of_units(self,unit_line):
        """
        | Parameters:
        | *unit_line*: string
        """
        unit_line_=ctypes.c_char_p(force_bytes(unit_line))
        func=self._link.o2scl.o2scl_table_units___line_of_units
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,unit_line_)
        return

    def remove_unit(self,col):
        """
        | Parameters:
        | *col*: string
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table_units___remove_unit
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        func(self._ptr,col_)
        return

    def convert_to_unit(self,col,unit,err_on_fail):
        """
        | Parameters:
        | *col*: string
        | *unit*: string
        | *err_on_fail*: ``bool``
        | Returns: a Python int
        """
        col_=ctypes.c_char_p(force_bytes(col))
        unit_=ctypes.c_char_p(force_bytes(unit))
        func=self._link.o2scl.o2scl_table_units___convert_to_unit
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
            f=link.o2scl.o2scl_create_uniform_grid__
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
            f=self._link.o2scl.o2scl_free_uniform_grid__
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
        func=self._link.o2scl.o2scl_uniform_grid___get_nbins
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_npoints(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_uniform_grid___get_npoints
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def is_log(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_uniform_grid___is_log
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_start(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_uniform_grid___get_start
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_end(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_uniform_grid___get_end
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_width(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_uniform_grid___get_width
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_uniform_grid___getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def vector(self,v):
        """
        | Parameters:
        | *v*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_uniform_grid___vector
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
            f=link.o2scl.o2scl_create_uniform_grid_end__
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
            f=self._link.o2scl.o2scl_free_uniform_grid_end__
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

        f=link.o2scl.o2scl_uniform_grid_end___init
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
            f=link.o2scl.o2scl_create_uniform_grid_width__
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
            f=self._link.o2scl.o2scl_free_uniform_grid_width__
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

        f=link.o2scl.o2scl_uniform_grid_width___init
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
            f=link.o2scl.o2scl_create_uniform_grid_end_width__
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
            f=self._link.o2scl.o2scl_free_uniform_grid_end_width__
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

        f=link.o2scl.o2scl_uniform_grid_end_width___init
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
            f=link.o2scl.o2scl_create_uniform_grid_log_end__
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
            f=self._link.o2scl.o2scl_free_uniform_grid_log_end__
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

        f=link.o2scl.o2scl_uniform_grid_log_end___init
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
            f=link.o2scl.o2scl_create_uniform_grid_log_width__
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
            f=self._link.o2scl.o2scl_free_uniform_grid_log_width__
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

        f=link.o2scl.o2scl_uniform_grid_log_width___init
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
            f=link.o2scl.o2scl_create_uniform_grid_log_end_width__
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
            f=self._link.o2scl.o2scl_free_uniform_grid_log_end_width__
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

        f=link.o2scl.o2scl_uniform_grid_log_end_width___init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double]
        return cls(link,f(start,end,width))


class table3d:
    """
    Python interface for O\ :sub:`2`\ scl class ``table3d``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/table3d.html .
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

    def get_size(self,nx,ny):
        """
        | Parameters:
        | *nx*: ``ctypes.c_size_t``
        | *ny*: ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_table3d_get_size
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
        nx_conv=ctypes.c_size_t(nx)
        ny_conv=ctypes.c_size_t(ny)
        func(self._ptr,ctypes.byref(nx_conv),ctypes.byref(ny_conv))
        nx=nx_conv.value()
        ny=ny_conv.value()
        return

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
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_table3d_is_size_set
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def is_xy_set(self):
        """
        | Returns: ``ctypes.c_bool`` object
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
        | Returns: std_string object
        """
        func=self._link.o2scl.o2scl_table3d_get_slice_name
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt

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

    def is_slice(self,name,ix):
        """
        | Parameters:
        | *name*: string
        | *ix*: ``ctypes.c_size_t``
        | Returns: ``ctypes.c_bool`` object
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_is_slice
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_size_t)]
        ix_conv=ctypes.c_size_t(ix)
        ret=func(self._ptr,name_,ctypes.byref(ix_conv))
        ix=ix_conv.value()
        return ret

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
        | Returns: :class:`boost::numeric::ublas::matrix<double>` object
        """
        slice_=ctypes.c_char_p(force_bytes(slice))
        func=self._link.o2scl.o2scl_table3d_get_slice
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,slice_)
        ret2=boost__numeric__ublas__matrix_double_(self._link,ret)
        return ret2

    def get_slice_i(self,slice):
        """
        | Parameters:
        | *slice*: string
        | Returns: :class:`boost::numeric::ublas::matrix<double>` object
        """
        slice_=ctypes.c_char_p(force_bytes(slice))
        func=self._link.o2scl.o2scl_table3d_get_slice_i
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,slice_)
        ret2=boost__numeric__ublas__matrix_double_(self._link,ret)
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
            f=link.o2scl.o2scl_create_tensor__
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
            f=self._link.o2scl.o2scl_free_tensor__
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
        f2=self._link.o2scl.o2scl_copy_tensor__
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor___is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor___clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_vector(self,index,val):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_tensor___set
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,index._ptr,val)
        return

    def set_all(self,x):
        """
        | Parameters:
        | *x*: ``double``
        """
        func=self._link.o2scl.o2scl_tensor___set_all
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,x)
        return

    def get_vector(self,index):
        """
        | Parameters:
        | *index*: :class:`vector<size_t>` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor___get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,index._ptr)
        return ret

    def get_rank(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor___get_rank
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
        func=self._link.o2scl.o2scl_tensor___get_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def total_size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_tensor___total_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def min_value(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor___min_value
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def max_value(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor___max_value
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def total_sum(self):
        """
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor___total_sum
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set(self,index,val):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and add the 
        data to the table
        """
        svst=o2sclpy.std_vector_size_t(self._link)
        syst.init_py(index)
        self.set_vector(syst,val)
        return
     
    def get(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object and get the 
        data from the table
        """
        svst=o2sclpy.std_vector_size_t(self._link)
        syst.init_py(index)
        return self.get_vector(syst)
    
    def resize(self,index):
        """
        Copy ``index`` to an :class:`std_vector_size_t` object 
        and resize
        """
        svst=o2sclpy.std_vector_size_t(self._link)
        syst.init_py(index)
        self.resize_vector(syst)
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
            f=link.o2scl.o2scl_create_tensor_grid__
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
            f=self._link.o2scl.o2scl_free_tensor_grid__
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
        f2=self._link.o2scl.o2scl_copy_tensor_grid__
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    def is_valid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_grid___is_valid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_val_vector(self,grid_point,val):
        """
        | Parameters:
        | *grid_point*: :class:`vector<double>` object
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_tensor_grid___set_val
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,grid_point._ptr,val)
        return

    def get_val_vector(self,grid_point):
        """
        | Parameters:
        | *grid_point*: :class:`vector<double>` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_tensor_grid___get_val
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,grid_point._ptr)
        return ret

    def is_grid_set(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl.o2scl_tensor_grid___is_grid_set
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_grid_packed(self,grid):
        """
        | Parameters:
        | *grid*: :class:`vector<double>` object
        """
        func=self._link.o2scl.o2scl_tensor_grid___set_grid_packed
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,grid._ptr)
        return

    def default_grid(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor_grid___default_grid
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def set_grid_i_vec(self,i,grid):
        """
        | Parameters:
        | *i*: ``size_t``
        | *grid*: :class:`vector<double>` object
        """
        func=self._link.o2scl.o2scl_tensor_grid___set_grid_i_vec
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
        func=self._link.o2scl.o2scl_tensor_grid___get_grid
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
        func=self._link.o2scl.o2scl_tensor_grid___set_grid
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,i,j,val)
        return


class find_constants:
    """
    Python interface for O\ :sub:`2`\ scl class ``find_constants``,
    see
    https://neutronstars.utk.edu/code/o2scl/html/class/find_constants.html .
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
            f=link.o2scl.o2scl_create_convert_units__
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
            f=self._link.o2scl.o2scl_free_convert_units__
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
        func=self._link.o2scl.o2scl_convert_units___get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for convert_units<>::verbose .
        """
        func=self._link.o2scl.o2scl_convert_units___set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def use_gnu_units(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_convert_units___get_use_gnu_units
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @use_gnu_units.setter
    def use_gnu_units(self,value):
        """
        Setter function for convert_units<>::use_gnu_units .
        """
        func=self._link.o2scl.o2scl_convert_units___set_use_gnu_units
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def err_on_fail(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_convert_units___get_err_on_fail
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_on_fail.setter
    def err_on_fail(self,value):
        """
        Setter function for convert_units<>::err_on_fail .
        """
        func=self._link.o2scl.o2scl_convert_units___set_err_on_fail
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def combine_two_conv(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_convert_units___get_combine_two_conv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @combine_two_conv.setter
    def combine_two_conv(self,value):
        """
        Setter function for convert_units<>::combine_two_conv .
        """
        func=self._link.o2scl.o2scl_convert_units___set_combine_two_conv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_units_cmd_string(self,units_cmd_string):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_convert_units___get_units_cmd_string
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,units_cmd_string._ptr)
        return

    def set_units_cmd_string(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_convert_units___set_units_cmd_string
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
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
        func=self._link.o2scl.o2scl_convert_units___convert
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
        func=self._link.o2scl.o2scl_convert_units___convert_ret
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,frm_,to_,val,converted)
        return ret

    def print_cache(self):
        """
        """
        func=self._link.o2scl.o2scl_convert_units___print_cache
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return


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
            f2=self._link.o2scl.o2scl_create_shared_ptr_table_units__
            f2.restype=ctypes.c_void_p
            self._s_ptr=f2()
        else:
            self._s_ptr=shared_ptr

        f=self._link.o2scl.o2scl_shared_ptr_table_units___ptr
        f.argtypes=[ctypes.c_void_p]
        f.restype=ctypes.c_void_p
        self._ptr=f(self._s_ptr)
        return

    def __del__(self):
        """
        Delete function for shared_ptr_table_units .
        """

        f=self._link.o2scl.o2scl_free_shared_ptr_table_units__
        f.argtypes=[ctypes.c_void_p]
        f(self._s_ptr)
        return

