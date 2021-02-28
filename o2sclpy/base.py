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
    Python interface for O\ :sub:`2`\ scl class ``std::string``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/std::string.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std::string .

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
        Delete function for class std::string .
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
        Shallow copy function for class std::string .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def length(self):
        """
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: :class:`char` object
        """
        func=self._link.o2scl.o2scl_std__string_getitem
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        ret2=char(self._link,ret)
        return ret2

    def __setitem__(self,n,value):
        func=self._link.o2scl.o2scl_std__string_setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char]
        func(self._ptr,n,val)
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

    def c_str(self):
        """
        | Returns: ``ctypes.c_char`` object
        """
        func=self._link.o2scl.o2scl_std__string_c_str
        func.restype=ctypes.c_char
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __len__(self):
        return length()
     
    def init_bytes(self,s):
        # Initialize the string from a Python bytes object
        resize(len(s))
        for i in range(0,len(s)):
            self.__setitem__(i,s[i])
        return
    
    def to_bytes(self):
        ret=b''
        for i in range(0,self.length()):
            ret=ret+self.__getitem__(i)
        return ret

class std_vector:
    """
    Python interface for O\ :sub:`2`\ scl class ``std::vector<double>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/std::vector<double>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std::vector<double> .

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
        Delete function for class std::vector<double> .
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
        Shallow copy function for class std::vector<double> .
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
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: :class:`double` object
        """
        func=self._link.o2scl.o2scl_std__vector_double__getitem
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        ret2=double(self._link,ret)
        return ret2

    def __setitem__(self,n,value):
        func=self._link.o2scl.o2scl_std__vector_double__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,n,val)
        return

    def __len__(self):
        return size()
    
    def to_numpy(self):
        ret=numpy.zeros((self.size()))
        for i in range(0,self.length()):
            ret[i]=self.__getitem__(i)
        return ret

class std_vector_int:
    """
    Python interface for O\ :sub:`2`\ scl class ``vector<int>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/vector<int>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class vector<int> .

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_vector_int_
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
        Delete function for class vector<int> .
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_vector_int_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class vector<int> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_vector_int__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: ``ctypes.c_size_t`` object
        """
        func=self._link.o2scl.o2scl_vector_int__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        | Returns: :class:`int` object
        """
        func=self._link.o2scl.o2scl_vector_int__getitem
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        ret2=int(self._link,ret)
        return ret2

    def __setitem__(self,n,value):
        func=self._link.o2scl.o2scl_vector_int__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_int]
        func(self._ptr,n,val)
        return

    def __len__(self):
        return size()
    
    def to_numpy(self):
        ret=numpy.zeros((self.size()),dtype=numpy.int32_t)
        for i in range(0,self.length()):
            ret[i]=self.__getitem__(i)
        return ret

class std_vector_size_t:
    """
    Python interface for O\ :sub:`2`\ scl class ``vector<size_t>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/vector<size_t>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class vector<size_t> .

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_vector_size_t_
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
        Delete function for class vector<size_t> .
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_vector_size_t_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class vector<size_t> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_vector_size_t__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: ``ctypes.c_size_t`` object
        """
        func=self._link.o2scl.o2scl_vector_size_t__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        | Returns: :class:`size_t` object
        """
        func=self._link.o2scl.o2scl_vector_size_t__getitem
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        ret2=size_t(self._link,ret)
        return ret2

    def __setitem__(self,n,value):
        func=self._link.o2scl.o2scl_vector_size_t__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        func(self._ptr,n,val)
        return

    def __len__(self):
        return size()
    
    def to_numpy(self):
        ret=numpy.zeros((self.size()),dtype=numpy.uint64_t)
        for i in range(0,self.length()):
            ret[i]=self.__getitem__(i)
        return ret

class lib_settings_class:
    """
    Python interface for O\ :sub:`2`\ scl class ``lib_settings_class``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/lib_settings_class.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class lib_settings_class .

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
        Delete function for class lib_settings_class .
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
        Shallow copy function for class lib_settings_class .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def get_data_dir(self):
        """
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_data_dir
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_data_dir(self,dir):
        """
        | Parameters:
        | *dir*: string
        | Returns: ``ctypes.c_int`` object
        """
        dir_=ctypes.c_char_p(force_bytes(dir))
        func=self._link.o2scl.o2scl_lib_settings_class_set_data_dir
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,dir_)
        return ret

    def get_doc_dir(self):
        """
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_get_doc_dir
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_doc_dir(self,dir):
        """
        | Parameters:
        | *dir*: string
        | Returns: ``ctypes.c_int`` object
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
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_system_type
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

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
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_time_compiled
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def date_compiled(self):
        """
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_date_compiled
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def o2scl_version(self):
        """
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_lib_settings_class_o2scl_version
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

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
    Python interface for O\ :sub:`2`\ scl class ``table<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/table<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class table<> .

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
        Delete function for class table<> .
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
        Shallow copy function for class table<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self):
        """
        Deep copy function for class table<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        f=self._link.o2scl.o2scl_copy_table__
        f.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f(src._ptr,new_obj._ptr)
        return new_obj

    def __getitem__(self,col):
        """
        | Parameters:
        | *col*: string
        | Returns: ``numpy`` array
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table___getitem
        n_=ctypes.c_int(0)
        ptr_=ctypes.POINTER(ctypes.c_double)()
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
        | Returns: ``ctypes.c_double`` object
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table___get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        ret=func(self._ptr,col_,row)
        return ret

    def get_ncolumns(self):
        """
        | Returns: ``ctypes.c_size_t`` object
        """
        func=self._link.o2scl.o2scl_table___get_ncolumns
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_nlines(self):
        """
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_table___get_column_name
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,icol)
        return ret

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
        | Returns: python bytes object
        """
        func=self._link.o2scl.o2scl_table___get_sorted_name
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,icol)
        return ret

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
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_size_t`` object
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
        # Create a std_vector object and copy the data over
        vec=o2sclpy.std_vector(self._link)
        vec.resize(len(v))
        for i in range(0,len(v)):
            vec[i]=v[i]
        line_of_data_vector(vec)
        return

class table_units(table):
    """
    Python interface for O\ :sub:`2`\ scl class ``table_units<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/table_units<>.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class table_units<> .

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
        Delete function for class table_units<> .
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
        Shallow copy function for class table_units<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self):
        """
        Deep copy function for class table_units<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        f=self._link.o2scl.o2scl_copy_table_units__
        f.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f(src._ptr,new_obj._ptr)
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
        | Returns: python bytes object
        """
        col_=ctypes.c_char_p(force_bytes(col))
        func=self._link.o2scl.o2scl_table_units___get_unit
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,col_)
        return ret

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
        | Returns: ``ctypes.c_int`` object
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
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/uniform_grid<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid<> .

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
        Delete function for class uniform_grid<> .
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
        Shallow copy function for class uniform_grid<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def get_nbins(self):
        """
        | Returns: ``ctypes.c_size_t`` object
        """
        func=self._link.o2scl.o2scl_uniform_grid___get_nbins
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_npoints(self):
        """
        | Returns: ``ctypes.c_size_t`` object
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
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl.o2scl_uniform_grid___get_start
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_end(self):
        """
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl.o2scl_uniform_grid___get_end
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_width(self):
        """
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl.o2scl_uniform_grid___getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret


class uniform_grid_end(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_end<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/uniform_grid_end<>.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_end<> .

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
        Delete function for class uniform_grid_end<> .
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
        Shallow copy function for class uniform_grid_end<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,n_bins):
        """
        Constructor-like class method for uniform_grid_end<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_create_uniform_grid_end___init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        cls._ptr=f(start,end,n_bins)
        cls._link=link
        return


class uniform_grid_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_width<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/uniform_grid_width<>.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_width<> .

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
        Delete function for class uniform_grid_width<> .
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
        Shallow copy function for class uniform_grid_width<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,width,n_bins):
        """
        Constructor-like class method for uniform_grid_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_create_uniform_grid_width___init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        cls._ptr=f(start,width,n_bins)
        cls._link=link
        return


class uniform_grid_end_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_end_width<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/uniform_grid_end_width<>.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_end_width<> .

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
        Delete function for class uniform_grid_end_width<> .
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
        Shallow copy function for class uniform_grid_end_width<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,width):
        """
        Constructor-like class method for uniform_grid_end_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_create_uniform_grid_end_width___init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double]
        cls._ptr=f(start,end,width)
        cls._link=link
        return


class uniform_grid_log_end(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_log_end<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/uniform_grid_log_end<>.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_log_end<> .

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
        Delete function for class uniform_grid_log_end<> .
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
        Shallow copy function for class uniform_grid_log_end<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,n_bins):
        """
        Constructor-like class method for uniform_grid_log_end<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_create_uniform_grid_log_end___init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        cls._ptr=f(start,end,n_bins)
        cls._link=link
        return


class uniform_grid_log_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_log_width<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/uniform_grid_log_width<>.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_log_width<> .

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
        Delete function for class uniform_grid_log_width<> .
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
        Shallow copy function for class uniform_grid_log_width<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,width,n_bins):
        """
        Constructor-like class method for uniform_grid_log_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_create_uniform_grid_log_width___init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_size_t]
        cls._ptr=f(start,width,n_bins)
        cls._link=link
        return


class uniform_grid_log_end_width(uniform_grid):
    """
    Python interface for O\ :sub:`2`\ scl class ``uniform_grid_log_end_width<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/uniform_grid_log_end_width<>.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class uniform_grid_log_end_width<> .

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
        Delete function for class uniform_grid_log_end_width<> .
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
        Shallow copy function for class uniform_grid_log_end_width<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @classmethod
    def init(cls,link,start,end,width):
        """
        Constructor-like class method for uniform_grid_log_end_width<> .

        | Parameters:

        """

        f=link.o2scl.o2scl_create_uniform_grid_log_end_width___init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_double,ctypes.c_double,ctypes.c_double]
        cls._ptr=f(start,end,width)
        cls._link=link
        return


class table3d:
    """
    Python interface for O\ :sub:`2`\ scl class ``table3d``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/table3d.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class table3d .

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
        Delete function for class table3d .
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
        Shallow copy function for class table3d .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self):
        """
        Deep copy function for class table3d .
        """

        new_obj=type(self)(self._link,self._ptr)
        f=self._link.o2scl.o2scl_copy_table3d
        f.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f(src._ptr,new_obj._ptr)
        return new_obj

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
        | Returns: ``ctypes.c_double`` object
        """
        name_=ctypes.c_char_p(force_bytes(name))
        func=self._link.o2scl.o2scl_table3d_get
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t,ctypes.c_char_p]
        ret=func(self._ptr,ix,iy,name_)
        return ret

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

    def get_nx(self):
        """
        | Returns: ``ctypes.c_size_t`` object
        """
        func=self._link.o2scl.o2scl_table3d_get_nx
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_ny(self):
        """
        | Returns: ``ctypes.c_size_t`` object
        """
        func=self._link.o2scl.o2scl_table3d_get_ny
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_nslices(self):
        """
        | Returns: ``ctypes.c_size_t`` object
        """
        func=self._link.o2scl.o2scl_table3d_get_nslices
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret


class tensor:
    """
    Python interface for O\ :sub:`2`\ scl class ``tensor<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/tensor<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class tensor<> .

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
        Delete function for class tensor<> .
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
        Shallow copy function for class tensor<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self):
        """
        Deep copy function for class tensor<> .
        """

        new_obj=type(self)(self._link,self._ptr)
        f=self._link.o2scl.o2scl_copy_tensor__
        f.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f(src._ptr,new_obj._ptr)
        return new_obj

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_tensor___clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return


class find_constants:
    """
    Python interface for O\ :sub:`2`\ scl class ``find_constants``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/find_constants.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class find_constants .

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
        Delete function for class find_constants .
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
        Shallow copy function for class find_constants .
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
        | Returns: ``ctypes.c_double`` object
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
    Python interface for O\ :sub:`2`\ scl class ``convert_units<>``,
    See
    https://neutronstars.utk.edu/code/o2scl-dev/html/class/convert_units<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class convert_units<> .

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
        Delete function for class convert_units<> .
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
        Shallow copy function for class convert_units<> .
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
        | Returns: ``ctypes.c_double`` object
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
        | Returns: ``ctypes.c_int`` object
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

    _s_ptr=0
    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,shared_ptr=0):
        """
        Init function for shared_ptr_table_units<> .
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
        Delete function for shared_ptr_table_units<> .
        """

        f=self._link.o2scl.o2scl_free_shared_ptr_table_units__
        f.argtypes=[ctypes.c_void_p]
        f(self._s_ptr)
        return

