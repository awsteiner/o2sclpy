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

from o2sclpy.part import *

class nucleus(part):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucleus``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucleus.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucleus

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucleus
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
        Delete function for class nucleus
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucleus
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucleus
        
        Returns: a nucleus object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def Z(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_nucleus_get_Z
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Z.setter
    def Z(self,value):
        """
        Setter function for nucleus::Z .
        """
        func=self._link.o2scl.o2scl_nucleus_set_Z
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def N(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_nucleus_get_N
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @N.setter
    def N(self,value):
        """
        Setter function for nucleus::N .
        """
        func=self._link.o2scl.o2scl_nucleus_set_N
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def A(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_nucleus_get_A
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @A.setter
    def A(self,value):
        """
        Setter function for nucleus::A .
        """
        func=self._link.o2scl.o2scl_nucleus_set_A
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def mex(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucleus_get_mex
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mex.setter
    def mex(self,value):
        """
        Setter function for nucleus::mex .
        """
        func=self._link.o2scl.o2scl_nucleus_set_mex
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def be(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucleus_get_be
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @be.setter
    def be(self,value):
        """
        Setter function for nucleus::be .
        """
        func=self._link.o2scl.o2scl_nucleus_set_be
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return


class nucmass_info:
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_info``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_info.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_info

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_info
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
        Delete function for class nucmass_info
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_info
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_info
        
        Returns: a nucmass_info object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def parse_elstring(self,ela):
        """
        | Parameters:
        | *ela*: string
        | Returns: a Python int, a Python int, a Python int, a Python int
        """
        ela_=ctypes.c_char_p(force_bytes(ela))
        func=self._link.o2scl.o2scl_nucmass_info_parse_elstring
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)]
        Z_conv=ctypes.c_int(0)
        N_conv=ctypes.c_int(0)
        A_conv=ctypes.c_int(0)
        ret=func(self._ptr,ela_,ctypes.byref(Z_conv),ctypes.byref(N_conv),ctypes.byref(A_conv))
        return ret,Z_conv.value,N_conv.value,A_conv.value

    def eltoZ(self,el):
        """
        | Parameters:
        | *el*: string
        | Returns: a Python int
        """
        el_=ctypes.c_char_p(force_bytes(el))
        func=self._link.o2scl.o2scl_nucmass_info_eltoZ
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,el_)
        return ret

    def Ztoel(self,Z):
        """
        | Parameters:
        | *Z*: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_nucmass_info_Ztoel
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,Z)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def Ztoname(self,Z):
        """
        | Parameters:
        | *Z*: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_nucmass_info_Ztoname
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,Z)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def tostring(self,Z,N):
        """
        | Parameters:
        | *Z*: ``size_t``
        | *N*: ``size_t``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_nucmass_info_tostring
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        ret=func(self._ptr,Z,N)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def int_to_spinp(self,g):
        """
        | Parameters:
        | *g*: ``int``
        | Returns: Python bytes object
        """
        func=self._link.o2scl.o2scl_nucmass_info_int_to_spinp
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        ret=func(self._ptr,g)
        strt=std_string(self._link,ret)
        strt._owner=True
        return strt.to_bytes()

    def spinp_to_int(self,s):
        """
        | Parameters:
        | *s*: string
        | Returns: a Python int
        """
        s_=ctypes.c_char_p(force_bytes(s))
        func=self._link.o2scl.o2scl_nucmass_info_spinp_to_int
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,s_)
        return ret


class nucmass:
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass.html .
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass
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
        Delete function for class nucmass
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass
        
        Returns: a nucmass object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def m_prot(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_get_m_prot
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_prot.setter
    def m_prot(self,value):
        """
        Setter function for nucmass::m_prot .
        """
        func=self._link.o2scl.o2scl_nucmass_set_m_prot
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def m_neut(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_get_m_neut
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_neut.setter
    def m_neut(self,value):
        """
        Setter function for nucmass::m_neut .
        """
        func=self._link.o2scl.o2scl_nucmass_set_m_neut
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def m_elec(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_get_m_elec
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_elec.setter
    def m_elec(self,value):
        """
        Setter function for nucmass::m_elec .
        """
        func=self._link.o2scl.o2scl_nucmass_set_m_elec
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def m_amu(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_get_m_amu
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_amu.setter
    def m_amu(self,value):
        """
        Setter function for nucmass::m_amu .
        """
        func=self._link.o2scl.o2scl_nucmass_set_m_amu
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def is_included(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_nucmass_is_included
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def get_nucleus(self,Z,N,n):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | *n*: :class:`nucleus` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_nucmass_get_nucleus
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p]
        ret=func(self._ptr,Z,N,n._ptr)
        return ret

    def mass_excess(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_mass_excess
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def mass_excess_d(self,Z,N):
        """
        | Parameters:
        | *Z*: ``double``
        | *N*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_mass_excess_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

    def electron_binding(self,Z):
        """
        | Parameters:
        | *Z*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_electron_binding
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,Z)
        return ret

    def binding_energy(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_binding_energy
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def binding_energy_d(self,Z,N):
        """
        | Parameters:
        | *Z*: ``double``
        | *N*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_binding_energy_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

    def total_mass(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_total_mass
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def total_mass_d(self,Z,N):
        """
        | Parameters:
        | *Z*: ``double``
        | *N*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_total_mass_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

    def neutron_sep(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_neutron_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def two_neutron_sep(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_two_neutron_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def proton_sep(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_proton_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def two_proton_sep(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_two_proton_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def atomic_mass(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_atomic_mass
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def atomic_mass_d(self,Z,N):
        """
        | Parameters:
        | *Z*: ``double``
        | *N*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_atomic_mass_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret


class nucmass_table(nucmass):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_table``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_table.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_table

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_table
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
        Delete function for class nucmass_table
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_table
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_table
        
        Returns: a nucmass_table object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def n(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_nucmass_table_get_n
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @n.setter
    def n(self,value):
        """
        Setter function for nucmass_table::n .
        """
        func=self._link.o2scl.o2scl_nucmass_table_set_n
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    def get_reference(self):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_nucmass_table_get_reference
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string(self._link)
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_reference(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_nucmass_table_set_reference
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def is_loaded(self):
        """
        | Returns: a Python boolean
        """
        func=self._link.o2scl.o2scl_nucmass_table_is_loaded
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_nentries(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_nucmass_table_get_nentries
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret


class nucmass_fit_base(nucmass):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_fit_base``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_fit_base.html .
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_fit_base

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_fit_base
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
        Delete function for class nucmass_fit_base
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_fit_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_fit_base
        
        Returns: a nucmass_fit_base object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def nfit(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_nucmass_fit_base_get_nfit
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nfit.setter
    def nfit(self,value):
        """
        Setter function for nucmass_fit_base::nfit .
        """
        func=self._link.o2scl.o2scl_nucmass_fit_base_set_nfit
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return


class nucmass_semi_empirical(nucmass_fit_base):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_semi_empirical``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_semi_empirical.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_semi_empirical

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_semi_empirical
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
        Delete function for class nucmass_semi_empirical
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_semi_empirical
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_semi_empirical
        
        Returns: a nucmass_semi_empirical object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def B(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_get_B
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @B.setter
    def B(self,value):
        """
        Setter function for nucmass_semi_empirical::B .
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_set_B
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Sv(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_get_Sv
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Sv.setter
    def Sv(self,value):
        """
        Setter function for nucmass_semi_empirical::Sv .
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_set_Sv
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Ss(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_get_Ss
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Ss.setter
    def Ss(self,value):
        """
        Setter function for nucmass_semi_empirical::Ss .
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_set_Ss
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Ec(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_get_Ec
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Ec.setter
    def Ec(self,value):
        """
        Setter function for nucmass_semi_empirical::Ec .
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_set_Ec
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Epair(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_get_Epair
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Epair.setter
    def Epair(self,value):
        """
        Setter function for nucmass_semi_empirical::Epair .
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_set_Epair
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def mass_excess(self,Z,N):
        """
        | Parameters:
        | *Z*: ``int``
        | *N*: ``int``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_mass_excess
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def mass_excess_d(self,Z,N):
        """
        | Parameters:
        | *Z*: ``double``
        | *N*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_nucmass_semi_empirical_mass_excess_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret


class nucmass_ame(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_ame``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_ame.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_ame

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_ame
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
        Delete function for class nucmass_ame
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_ame
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_ame
        
        Returns: a nucmass_ame object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_dz_table(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_dz_table``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_dz_table.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_dz_table

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_dz_table
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
        Delete function for class nucmass_dz_table
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_dz_table
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_dz_table
        
        Returns: a nucmass_dz_table object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_dz_fit(nucmass_fit_base):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_dz_fit``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_dz_fit.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_dz_fit

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_dz_fit
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
        Delete function for class nucmass_dz_fit
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_dz_fit
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_dz_fit
        
        Returns: a nucmass_dz_fit object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_dz_fit_33(nucmass_fit_base):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_dz_fit_33``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_dz_fit_33.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_dz_fit_33

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_dz_fit_33
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
        Delete function for class nucmass_dz_fit_33
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_dz_fit_33
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_dz_fit_33
        
        Returns: a nucmass_dz_fit_33 object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_frdm(nucmass_fit_base):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_frdm``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_frdm.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_frdm

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_frdm
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
        Delete function for class nucmass_frdm
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_frdm
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_frdm
        
        Returns: a nucmass_frdm object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def a1(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_a1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a1.setter
    def a1(self,value):
        """
        Setter function for nucmass_frdm::a1 .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_a1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def J(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_J
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @J.setter
    def J(self,value):
        """
        Setter function for nucmass_frdm::J .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_J
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def K(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_K
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @K.setter
    def K(self,value):
        """
        Setter function for nucmass_frdm::K .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_K
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a2(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_a2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a2.setter
    def a2(self,value):
        """
        Setter function for nucmass_frdm::a2 .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_a2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Q(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_Q
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Q.setter
    def Q(self,value):
        """
        Setter function for nucmass_frdm::Q .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_Q
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a3(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_a3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a3.setter
    def a3(self,value):
        """
        Setter function for nucmass_frdm::a3 .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_a3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ca(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_ca
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ca.setter
    def ca(self,value):
        """
        Setter function for nucmass_frdm::ca .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_ca
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def W(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_W
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @W.setter
    def W(self,value):
        """
        Setter function for nucmass_frdm::W .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_W
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ael(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_ael
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ael.setter
    def ael(self,value):
        """
        Setter function for nucmass_frdm::ael .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_ael
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def rp(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_rp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @rp.setter
    def rp(self,value):
        """
        Setter function for nucmass_frdm::rp .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_rp
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def r0(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_r0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @r0.setter
    def r0(self,value):
        """
        Setter function for nucmass_frdm::r0 .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_r0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def MH(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_MH
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @MH.setter
    def MH(self,value):
        """
        Setter function for nucmass_frdm::MH .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_MH
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Mn(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_Mn
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Mn.setter
    def Mn(self,value):
        """
        Setter function for nucmass_frdm::Mn .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_Mn
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def e2(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_e2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @e2.setter
    def e2(self,value):
        """
        Setter function for nucmass_frdm::e2 .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_e2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_a
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a.setter
    def a(self,value):
        """
        Setter function for nucmass_frdm::a .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_a
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def aden(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_aden
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @aden.setter
    def aden(self,value):
        """
        Setter function for nucmass_frdm::aden .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_aden
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def rmac(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_rmac
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @rmac.setter
    def rmac(self,value):
        """
        Setter function for nucmass_frdm::rmac .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_rmac
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def h(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_h
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @h.setter
    def h(self,value):
        """
        Setter function for nucmass_frdm::h .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_h
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def L(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_L
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @L.setter
    def L(self,value):
        """
        Setter function for nucmass_frdm::L .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_L
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def C(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_C
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @C.setter
    def C(self,value):
        """
        Setter function for nucmass_frdm::C .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_C
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def gamma(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_gamma
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @gamma.setter
    def gamma(self,value):
        """
        Setter function for nucmass_frdm::gamma .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_gamma
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def amu(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_amu
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @amu.setter
    def amu(self,value):
        """
        Setter function for nucmass_frdm::amu .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_amu
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def nn(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_nn
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nn.setter
    def nn(self,value):
        """
        Setter function for nucmass_frdm::nn .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_nn
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def np(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_np
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @np.setter
    def np(self,value):
        """
        Setter function for nucmass_frdm::np .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_np
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Rn(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_Rn
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Rn.setter
    def Rn(self,value):
        """
        Setter function for nucmass_frdm::Rn .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_Rn
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Rp(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_get_Rp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Rp.setter
    def Rp(self,value):
        """
        Setter function for nucmass_frdm::Rp .
        """
        func=self._link.o2scl.o2scl_nucmass_frdm_set_Rp
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return


class nucmass_mnmsk(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_mnmsk``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_mnmsk.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_mnmsk

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_mnmsk
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
        Delete function for class nucmass_mnmsk
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_mnmsk
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_mnmsk
        
        Returns: a nucmass_mnmsk object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_mnmsk_exp(nucmass_mnmsk):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_mnmsk_exp``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_mnmsk_exp.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_mnmsk_exp

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_mnmsk_exp
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
        Delete function for class nucmass_mnmsk_exp
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_mnmsk_exp
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_mnmsk_exp
        
        Returns: a nucmass_mnmsk_exp object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_gen(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_gen``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_gen.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_gen

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_gen
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
        Delete function for class nucmass_gen
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_gen
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_gen
        
        Returns: a nucmass_gen object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_dglg(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_dglg``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_dglg.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_dglg

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_dglg
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
        Delete function for class nucmass_dglg
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_dglg
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_dglg
        
        Returns: a nucmass_dglg object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_hfb(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_hfb``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_hfb.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_hfb

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_hfb
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
        Delete function for class nucmass_hfb
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_hfb
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_hfb
        
        Returns: a nucmass_hfb object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_hfb_sp(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_hfb_sp``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_hfb_sp.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_hfb_sp

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_hfb_sp
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
        Delete function for class nucmass_hfb_sp
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_hfb_sp
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_hfb_sp
        
        Returns: a nucmass_hfb_sp object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_ktuy(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_ktuy``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_ktuy.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_ktuy

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_ktuy
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
        Delete function for class nucmass_ktuy
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_ktuy
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_ktuy
        
        Returns: a nucmass_ktuy object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_sdnp(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_sdnp``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_sdnp.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_sdnp

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_sdnp
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
        Delete function for class nucmass_sdnp
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_sdnp
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_sdnp
        
        Returns: a nucmass_sdnp object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class nucmass_wlw(nucmass_table):
    """
    Python interface for O\ :sub:`2`\ scl class ``nucmass_wlw``,
    See
    https://neutronstars.utk.edu/code/o2scl/part/html/class/nucmass_wlw.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class nucmass_wlw

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_nucmass_wlw
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
        Delete function for class nucmass_wlw
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_nucmass_wlw
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class nucmass_wlw
        
        Returns: a nucmass_wlw object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


def ame_load(link,ame,name,exp_only):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ame*: :class:`nucmass_ame` object
        | *name*: string
        | *exp_only*: ``bool``
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=link.o2scl.o2scl_ame_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool]
    func(ame._ptr,name_,exp_only)
    return

def ame_load_ext(link,ame,file_name,table_name,exp_only):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *ame*: :class:`nucmass_ame` object
        | *file_name*: string
        | *table_name*: string
        | *exp_only*: ``bool``
    """
    file_name_=ctypes.c_char_p(force_bytes(file_name))
    table_name_=ctypes.c_char_p(force_bytes(table_name))
    func=link.o2scl.o2scl_ame_load_ext_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_bool]
    func(ame._ptr,file_name_,table_name_,exp_only)
    return

def mnmsk_load(link,mnmsk,model,filename):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *mnmsk*: :class:`nucmass_mnmsk` object
        | *model*: string
        | *filename*: string
    """
    model_=ctypes.c_char_p(force_bytes(model))
    filename_=ctypes.c_char_p(force_bytes(filename))
    func=link.o2scl.o2scl_mnmsk_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    func(mnmsk._ptr,model_,filename_)
    return

def hfb_load(link,hfb,model,filename):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hfb*: :class:`nucmass_hfb` object
        | *model*: ``size_t``
        | *filename*: string
    """
    filename_=ctypes.c_char_p(force_bytes(filename))
    func=link.o2scl.o2scl_hfb_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char_p]
    func(hfb._ptr,model,filename_)
    return

def hfb_sp_load(link,hfb,model,filename):
    """
        | Parameters:
        | *link* :class:`linker` object
        | *hfb*: :class:`nucmass_hfb_sp` object
        | *model*: ``size_t``
        | *filename*: string
    """
    filename_=ctypes.c_char_p(force_bytes(filename))
    func=link.o2scl.o2scl_hfb_sp_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char_p]
    func(hfb._ptr,model,filename_)
    return

