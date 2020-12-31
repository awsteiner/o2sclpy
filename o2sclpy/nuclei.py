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

class nucleus(part):
    """
    Python interface for class :ref:`nucleus <o2sclp:nucleus>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucleus .
        """

        f=dll.o2scl_create_nucleus
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucleus .
        """

        f=self._dll.o2scl_free_nucleus
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def Z(self):
        """
        Getter function for nucleus::Z .
        """
        func=self._dll.o2scl_nucleus_get_Z
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Z.setter
    def Z(self,value):
        """
        Setter function for nucleus::Z .
        """
        func=self._dll.o2scl_nucleus_set_Z
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def N(self):
        """
        Getter function for nucleus::N .
        """
        func=self._dll.o2scl_nucleus_get_N
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @N.setter
    def N(self,value):
        """
        Setter function for nucleus::N .
        """
        func=self._dll.o2scl_nucleus_set_N
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def A(self):
        """
        Getter function for nucleus::A .
        """
        func=self._dll.o2scl_nucleus_get_A
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @A.setter
    def A(self,value):
        """
        Setter function for nucleus::A .
        """
        func=self._dll.o2scl_nucleus_set_A
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def mex(self):
        """
        Getter function for nucleus::mex .
        """
        func=self._dll.o2scl_nucleus_get_mex
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mex.setter
    def mex(self,value):
        """
        Setter function for nucleus::mex .
        """
        func=self._dll.o2scl_nucleus_set_mex
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def be(self):
        """
        Getter function for nucleus::be .
        """
        func=self._dll.o2scl_nucleus_get_be
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @be.setter
    def be(self,value):
        """
        Setter function for nucleus::be .
        """
        func=self._dll.o2scl_nucleus_set_be
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class nucmass_info:
    """
    Python interface for class :ref:`nucmass_info <o2sclp:nucmass_info>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class nucmass_info .
        """

        f=dll.o2scl_create_nucmass_info
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_info .
        """

        f=self._dll.o2scl_free_nucmass_info
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def parse_elstring(self,ela,Z,N,A):
        """
        Wrapper for nucmass_info::parse_elstring() .
        wrapper for :ref:`o2sclp:nucmass_info::parse_elstring()`.
        """
        func=self._dll.o2scl_nucmass_info_parse_elstring
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_std::string,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,ela,Z._ptr,N._ptr,A._ptr)
        return ret

    def eltoZ(self,el):
        """
        Wrapper for nucmass_info::eltoZ() .
        wrapper for :ref:`o2sclp:nucmass_info::eltoZ()`.
        """
        func=self._dll.o2scl_nucmass_info_eltoZ
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_std::string]
        ret=func(self._ptr,el)
        return ret

    def Ztoel(self,Z):
        """
        Wrapper for nucmass_info::Ztoel() .
        wrapper for :ref:`o2sclp:nucmass_info::Ztoel()`.
        """
        func=self._dll.o2scl_nucmass_info_Ztoel
        func.restype=ctypes.c_std::string
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,Z)
        return ret

    def Ztoname(self,Z):
        """
        Wrapper for nucmass_info::Ztoname() .
        wrapper for :ref:`o2sclp:nucmass_info::Ztoname()`.
        """
        func=self._dll.o2scl_nucmass_info_Ztoname
        func.restype=ctypes.c_std::string
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,Z)
        return ret

    def tostring(self,Z,N):
        """
        Wrapper for nucmass_info::tostring() .
        wrapper for :ref:`o2sclp:nucmass_info::tostring()`.
        """
        func=self._dll.o2scl_nucmass_info_tostring
        func.restype=ctypes.c_std::string
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        ret=func(self._ptr,Z,N)
        return ret

    def int_to_spinp(self,g):
        """
        Wrapper for nucmass_info::int_to_spinp() .
        wrapper for :ref:`o2sclp:nucmass_info::int_to_spinp()`.
        """
        func=self._dll.o2scl_nucmass_info_int_to_spinp
        func.restype=ctypes.c_std::string
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        ret=func(self._ptr,g)
        return ret

    def spinp_to_int(self,s):
        """
        Wrapper for nucmass_info::spinp_to_int() .
        wrapper for :ref:`o2sclp:nucmass_info::spinp_to_int()`.
        """
        func=self._dll.o2scl_nucmass_info_spinp_to_int
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_std::string]
        ret=func(self._ptr,s)
        return ret

class nucmass:
    """
    Python interface for class :ref:`nucmass <o2sclp:nucmass>`.
    """

    _ptr=0
    _dll=0

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class nucmass .
        """

        f=dll.o2scl_create_nucmass
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass .
        """

        f=self._dll.o2scl_free_nucmass
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def m_prot(self):
        """
        Getter function for nucmass::m_prot .
        """
        func=self._dll.o2scl_nucmass_get_m_prot
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_prot.setter
    def m_prot(self,value):
        """
        Setter function for nucmass::m_prot .
        """
        func=self._dll.o2scl_nucmass_set_m_prot
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def m_neut(self):
        """
        Getter function for nucmass::m_neut .
        """
        func=self._dll.o2scl_nucmass_get_m_neut
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_neut.setter
    def m_neut(self,value):
        """
        Setter function for nucmass::m_neut .
        """
        func=self._dll.o2scl_nucmass_set_m_neut
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def m_elec(self):
        """
        Getter function for nucmass::m_elec .
        """
        func=self._dll.o2scl_nucmass_get_m_elec
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_elec.setter
    def m_elec(self,value):
        """
        Setter function for nucmass::m_elec .
        """
        func=self._dll.o2scl_nucmass_set_m_elec
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def m_amu(self):
        """
        Getter function for nucmass::m_amu .
        """
        func=self._dll.o2scl_nucmass_get_m_amu
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m_amu.setter
    def m_amu(self,value):
        """
        Setter function for nucmass::m_amu .
        """
        func=self._dll.o2scl_nucmass_set_m_amu
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def is_included(self,Z,N):
        """
        Wrapper for nucmass::is_included() .
        wrapper for :ref:`o2sclp:nucmass::is_included()`.
        """
        func=self._dll.o2scl_nucmass_is_included
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def get_nucleus(self,Z,N,n):
        """
        Wrapper for nucmass::get_nucleus() .
        wrapper for :ref:`o2sclp:nucmass::get_nucleus()`.
        """
        func=self._dll.o2scl_nucmass_get_nucleus
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p]
        ret=func(self._ptr,Z,N,n._ptr)
        return ret

    def mass_excess(self,Z,N):
        """
        Wrapper for nucmass::mass_excess() .
        wrapper for :ref:`o2sclp:nucmass::mass_excess()`.
        """
        func=self._dll.o2scl_nucmass_mass_excess
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def mass_excess_d(self,Z,N):
        """
        Wrapper for nucmass::mass_excess_d() .
        wrapper for :ref:`o2sclp:nucmass::mass_excess_d()`.
        """
        func=self._dll.o2scl_nucmass_mass_excess_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

    def electron_binding(self,Z):
        """
        Wrapper for nucmass::electron_binding() .
        wrapper for :ref:`o2sclp:nucmass::electron_binding()`.
        """
        func=self._dll.o2scl_nucmass_electron_binding
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,Z)
        return ret

    def binding_energy(self,Z,N):
        """
        Wrapper for nucmass::binding_energy() .
        wrapper for :ref:`o2sclp:nucmass::binding_energy()`.
        """
        func=self._dll.o2scl_nucmass_binding_energy
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def binding_energy_d(self,Z,N):
        """
        Wrapper for nucmass::binding_energy_d() .
        wrapper for :ref:`o2sclp:nucmass::binding_energy_d()`.
        """
        func=self._dll.o2scl_nucmass_binding_energy_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

    def total_mass(self,Z,N):
        """
        Wrapper for nucmass::total_mass() .
        wrapper for :ref:`o2sclp:nucmass::total_mass()`.
        """
        func=self._dll.o2scl_nucmass_total_mass
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def total_mass_d(self,Z,N):
        """
        Wrapper for nucmass::total_mass_d() .
        wrapper for :ref:`o2sclp:nucmass::total_mass_d()`.
        """
        func=self._dll.o2scl_nucmass_total_mass_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

    def neutron_sep(self,Z,N):
        """
        Wrapper for nucmass::neutron_sep() .
        wrapper for :ref:`o2sclp:nucmass::neutron_sep()`.
        """
        func=self._dll.o2scl_nucmass_neutron_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def two_neutron_sep(self,Z,N):
        """
        Wrapper for nucmass::two_neutron_sep() .
        wrapper for :ref:`o2sclp:nucmass::two_neutron_sep()`.
        """
        func=self._dll.o2scl_nucmass_two_neutron_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def proton_sep(self,Z,N):
        """
        Wrapper for nucmass::proton_sep() .
        wrapper for :ref:`o2sclp:nucmass::proton_sep()`.
        """
        func=self._dll.o2scl_nucmass_proton_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def two_proton_sep(self,Z,N):
        """
        Wrapper for nucmass::two_proton_sep() .
        wrapper for :ref:`o2sclp:nucmass::two_proton_sep()`.
        """
        func=self._dll.o2scl_nucmass_two_proton_sep
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def atomic_mass(self,Z,N):
        """
        Wrapper for nucmass::atomic_mass() .
        wrapper for :ref:`o2sclp:nucmass::atomic_mass()`.
        """
        func=self._dll.o2scl_nucmass_atomic_mass
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def atomic_mass_d(self,Z,N):
        """
        Wrapper for nucmass::atomic_mass_d() .
        wrapper for :ref:`o2sclp:nucmass::atomic_mass_d()`.
        """
        func=self._dll.o2scl_nucmass_atomic_mass_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

class nucmass_table(nucmass):
    """
    Python interface for class :ref:`nucmass_table <o2sclp:nucmass_table>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class nucmass_table .
        """

        f=dll.o2scl_create_nucmass_table
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_table .
        """

        f=self._dll.o2scl_free_nucmass_table
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def n(self):
        """
        Getter function for nucmass_table::n .
        """
        func=self._dll.o2scl_nucmass_table_get_n
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @n.setter
    def n(self,value):
        """
        Setter function for nucmass_table::n .
        """
        func=self._dll.o2scl_nucmass_table_set_n
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    def get_reference(self,reference):
        """
        Getter function for nucmass_table::reference .
        """
        func=self._dll.o2scl_nucmass_table_get_reference
        func.restype=ctypes.c_std::string
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,reference._ptr)

    def set_reference(self,value):
        """
        Setter function for nucmass_table::reference .
        """
        func=self._dll.o2scl_nucmass_table_set_reference
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def is_loaded(self,):
        """
        Wrapper for nucmass_table::is_loaded() .
        wrapper for :ref:`o2sclp:nucmass_table::is_loaded()`.
        """
        func=self._dll.o2scl_nucmass_table_is_loaded
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,]
        ret=func(self._ptr,)
        return ret

    def get_nentries(self,):
        """
        Wrapper for nucmass_table::get_nentries() .
        wrapper for :ref:`o2sclp:nucmass_table::get_nentries()`.
        """
        func=self._dll.o2scl_nucmass_table_get_nentries
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,]
        ret=func(self._ptr,)
        return ret

class nucmass_fit_base(nucmass):
    """
    Python interface for class :ref:`nucmass_fit_base <o2sclp:nucmass_fit_base>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class nucmass_fit_base .
        """

        f=dll.o2scl_create_nucmass_fit_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_fit_base .
        """

        f=self._dll.o2scl_free_nucmass_fit_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def nfit(self):
        """
        Getter function for nucmass_fit_base::nfit .
        """
        func=self._dll.o2scl_nucmass_fit_base_get_nfit
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nfit.setter
    def nfit(self,value):
        """
        Setter function for nucmass_fit_base::nfit .
        """
        func=self._dll.o2scl_nucmass_fit_base_set_nfit
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

