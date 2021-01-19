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

from o2sclpy.part import *

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
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,ela,Z._ptr,N._ptr,A._ptr)
        return ret

    def eltoZ(self,el):
        """
        Wrapper for nucmass_info::eltoZ() .
        wrapper for :ref:`o2sclp:nucmass_info::eltoZ()`.
        """
        func=self._dll.o2scl_nucmass_info_eltoZ
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,el)
        return ret

    def Ztoel(self,Z):
        """
        Wrapper for nucmass_info::Ztoel() .
        wrapper for :ref:`o2sclp:nucmass_info::Ztoel()`.
        """
        func=self._dll.o2scl_nucmass_info_Ztoel
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,Z)
        return ret

    def Ztoname(self,Z):
        """
        Wrapper for nucmass_info::Ztoname() .
        wrapper for :ref:`o2sclp:nucmass_info::Ztoname()`.
        """
        func=self._dll.o2scl_nucmass_info_Ztoname
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,Z)
        return ret

    def tostring(self,Z,N):
        """
        Wrapper for nucmass_info::tostring() .
        wrapper for :ref:`o2sclp:nucmass_info::tostring()`.
        """
        func=self._dll.o2scl_nucmass_info_tostring
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t]
        ret=func(self._ptr,Z,N)
        return ret

    def int_to_spinp(self,g):
        """
        Wrapper for nucmass_info::int_to_spinp() .
        wrapper for :ref:`o2sclp:nucmass_info::int_to_spinp()`.
        """
        func=self._dll.o2scl_nucmass_info_int_to_spinp
        func.restype=ctypes.c_char_p
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
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
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
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,reference._ptr)
        return

    def set_reference(self,value):
        """
        Setter function for nucmass_table::reference .
        """
        func=self._dll.o2scl_nucmass_table_set_reference
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def is_loaded(self):
        """
        Wrapper for nucmass_table::is_loaded() .
        wrapper for :ref:`o2sclp:nucmass_table::is_loaded()`.
        """
        func=self._dll.o2scl_nucmass_table_is_loaded
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,]
        ret=func(self._ptr,)
        return ret

    def get_nentries(self):
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

class nucmass_semi_empirical(nucmass_fit_base):
    """
    Python interface for class :ref:`nucmass_semi_empirical <o2sclp:nucmass_semi_empirical>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_semi_empirical .
        """

        f=dll.o2scl_create_nucmass_semi_empirical
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_semi_empirical .
        """

        f=self._dll.o2scl_free_nucmass_semi_empirical
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def B(self):
        """
        Getter function for nucmass_semi_empirical::B .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_get_B
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @B.setter
    def B(self,value):
        """
        Setter function for nucmass_semi_empirical::B .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_set_B
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Sv(self):
        """
        Getter function for nucmass_semi_empirical::Sv .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_get_Sv
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Sv.setter
    def Sv(self,value):
        """
        Setter function for nucmass_semi_empirical::Sv .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_set_Sv
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Ss(self):
        """
        Getter function for nucmass_semi_empirical::Ss .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_get_Ss
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Ss.setter
    def Ss(self,value):
        """
        Setter function for nucmass_semi_empirical::Ss .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_set_Ss
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Ec(self):
        """
        Getter function for nucmass_semi_empirical::Ec .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_get_Ec
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Ec.setter
    def Ec(self,value):
        """
        Setter function for nucmass_semi_empirical::Ec .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_set_Ec
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Epair(self):
        """
        Getter function for nucmass_semi_empirical::Epair .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_get_Epair
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Epair.setter
    def Epair(self,value):
        """
        Setter function for nucmass_semi_empirical::Epair .
        """
        func=self._dll.o2scl_nucmass_semi_empirical_set_Epair
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def mass_excess(self,Z,N):
        """
        Wrapper for nucmass_semi_empirical::mass_excess() .
        wrapper for :ref:`o2sclp:nucmass_semi_empirical::mass_excess()`.
        """
        func=self._dll.o2scl_nucmass_semi_empirical_mass_excess
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        ret=func(self._ptr,Z,N)
        return ret

    def mass_excess_d(self,Z,N):
        """
        Wrapper for nucmass_semi_empirical::mass_excess_d() .
        wrapper for :ref:`o2sclp:nucmass_semi_empirical::mass_excess_d()`.
        """
        func=self._dll.o2scl_nucmass_semi_empirical_mass_excess_d
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,Z,N)
        return ret

class nucmass_ame(nucmass_table):
    """
    Python interface for class :ref:`nucmass_ame <o2sclp:nucmass_ame>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_ame .
        """

        f=dll.o2scl_create_nucmass_ame
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_ame .
        """

        f=self._dll.o2scl_free_nucmass_ame
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_dz_table(nucmass_table):
    """
    Python interface for class :ref:`nucmass_dz_table <o2sclp:nucmass_dz_table>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_dz_table .
        """

        f=dll.o2scl_create_nucmass_dz_table
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_dz_table .
        """

        f=self._dll.o2scl_free_nucmass_dz_table
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_dz_fit(nucmass_fit_base):
    """
    Python interface for class :ref:`nucmass_dz_fit <o2sclp:nucmass_dz_fit>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_dz_fit .
        """

        f=dll.o2scl_create_nucmass_dz_fit
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_dz_fit .
        """

        f=self._dll.o2scl_free_nucmass_dz_fit
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_dz_fit_33(nucmass_fit_base):
    """
    Python interface for class :ref:`nucmass_dz_fit_33 <o2sclp:nucmass_dz_fit_33>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_dz_fit_33 .
        """

        f=dll.o2scl_create_nucmass_dz_fit_33
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_dz_fit_33 .
        """

        f=self._dll.o2scl_free_nucmass_dz_fit_33
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_frdm(nucmass_fit_base):
    """
    Python interface for class :ref:`nucmass_frdm <o2sclp:nucmass_frdm>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_frdm .
        """

        f=dll.o2scl_create_nucmass_frdm
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_frdm .
        """

        f=self._dll.o2scl_free_nucmass_frdm
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def a1(self):
        """
        Getter function for nucmass_frdm::a1 .
        """
        func=self._dll.o2scl_nucmass_frdm_get_a1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a1.setter
    def a1(self,value):
        """
        Setter function for nucmass_frdm::a1 .
        """
        func=self._dll.o2scl_nucmass_frdm_set_a1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def J(self):
        """
        Getter function for nucmass_frdm::J .
        """
        func=self._dll.o2scl_nucmass_frdm_get_J
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @J.setter
    def J(self,value):
        """
        Setter function for nucmass_frdm::J .
        """
        func=self._dll.o2scl_nucmass_frdm_set_J
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def K(self):
        """
        Getter function for nucmass_frdm::K .
        """
        func=self._dll.o2scl_nucmass_frdm_get_K
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @K.setter
    def K(self,value):
        """
        Setter function for nucmass_frdm::K .
        """
        func=self._dll.o2scl_nucmass_frdm_set_K
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a2(self):
        """
        Getter function for nucmass_frdm::a2 .
        """
        func=self._dll.o2scl_nucmass_frdm_get_a2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a2.setter
    def a2(self,value):
        """
        Setter function for nucmass_frdm::a2 .
        """
        func=self._dll.o2scl_nucmass_frdm_set_a2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Q(self):
        """
        Getter function for nucmass_frdm::Q .
        """
        func=self._dll.o2scl_nucmass_frdm_get_Q
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Q.setter
    def Q(self,value):
        """
        Setter function for nucmass_frdm::Q .
        """
        func=self._dll.o2scl_nucmass_frdm_set_Q
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a3(self):
        """
        Getter function for nucmass_frdm::a3 .
        """
        func=self._dll.o2scl_nucmass_frdm_get_a3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a3.setter
    def a3(self,value):
        """
        Setter function for nucmass_frdm::a3 .
        """
        func=self._dll.o2scl_nucmass_frdm_set_a3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ca(self):
        """
        Getter function for nucmass_frdm::ca .
        """
        func=self._dll.o2scl_nucmass_frdm_get_ca
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ca.setter
    def ca(self,value):
        """
        Setter function for nucmass_frdm::ca .
        """
        func=self._dll.o2scl_nucmass_frdm_set_ca
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def W(self):
        """
        Getter function for nucmass_frdm::W .
        """
        func=self._dll.o2scl_nucmass_frdm_get_W
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @W.setter
    def W(self,value):
        """
        Setter function for nucmass_frdm::W .
        """
        func=self._dll.o2scl_nucmass_frdm_set_W
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ael(self):
        """
        Getter function for nucmass_frdm::ael .
        """
        func=self._dll.o2scl_nucmass_frdm_get_ael
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ael.setter
    def ael(self,value):
        """
        Setter function for nucmass_frdm::ael .
        """
        func=self._dll.o2scl_nucmass_frdm_set_ael
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def rp(self):
        """
        Getter function for nucmass_frdm::rp .
        """
        func=self._dll.o2scl_nucmass_frdm_get_rp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @rp.setter
    def rp(self,value):
        """
        Setter function for nucmass_frdm::rp .
        """
        func=self._dll.o2scl_nucmass_frdm_set_rp
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def r0(self):
        """
        Getter function for nucmass_frdm::r0 .
        """
        func=self._dll.o2scl_nucmass_frdm_get_r0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @r0.setter
    def r0(self,value):
        """
        Setter function for nucmass_frdm::r0 .
        """
        func=self._dll.o2scl_nucmass_frdm_set_r0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def MH(self):
        """
        Getter function for nucmass_frdm::MH .
        """
        func=self._dll.o2scl_nucmass_frdm_get_MH
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @MH.setter
    def MH(self,value):
        """
        Setter function for nucmass_frdm::MH .
        """
        func=self._dll.o2scl_nucmass_frdm_set_MH
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Mn(self):
        """
        Getter function for nucmass_frdm::Mn .
        """
        func=self._dll.o2scl_nucmass_frdm_get_Mn
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Mn.setter
    def Mn(self,value):
        """
        Setter function for nucmass_frdm::Mn .
        """
        func=self._dll.o2scl_nucmass_frdm_set_Mn
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def e2(self):
        """
        Getter function for nucmass_frdm::e2 .
        """
        func=self._dll.o2scl_nucmass_frdm_get_e2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @e2.setter
    def e2(self,value):
        """
        Setter function for nucmass_frdm::e2 .
        """
        func=self._dll.o2scl_nucmass_frdm_set_e2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a(self):
        """
        Getter function for nucmass_frdm::a .
        """
        func=self._dll.o2scl_nucmass_frdm_get_a
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a.setter
    def a(self,value):
        """
        Setter function for nucmass_frdm::a .
        """
        func=self._dll.o2scl_nucmass_frdm_set_a
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def aden(self):
        """
        Getter function for nucmass_frdm::aden .
        """
        func=self._dll.o2scl_nucmass_frdm_get_aden
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @aden.setter
    def aden(self,value):
        """
        Setter function for nucmass_frdm::aden .
        """
        func=self._dll.o2scl_nucmass_frdm_set_aden
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def rmac(self):
        """
        Getter function for nucmass_frdm::rmac .
        """
        func=self._dll.o2scl_nucmass_frdm_get_rmac
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @rmac.setter
    def rmac(self,value):
        """
        Setter function for nucmass_frdm::rmac .
        """
        func=self._dll.o2scl_nucmass_frdm_set_rmac
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def h(self):
        """
        Getter function for nucmass_frdm::h .
        """
        func=self._dll.o2scl_nucmass_frdm_get_h
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @h.setter
    def h(self,value):
        """
        Setter function for nucmass_frdm::h .
        """
        func=self._dll.o2scl_nucmass_frdm_set_h
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def L(self):
        """
        Getter function for nucmass_frdm::L .
        """
        func=self._dll.o2scl_nucmass_frdm_get_L
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @L.setter
    def L(self,value):
        """
        Setter function for nucmass_frdm::L .
        """
        func=self._dll.o2scl_nucmass_frdm_set_L
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def C(self):
        """
        Getter function for nucmass_frdm::C .
        """
        func=self._dll.o2scl_nucmass_frdm_get_C
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @C.setter
    def C(self,value):
        """
        Setter function for nucmass_frdm::C .
        """
        func=self._dll.o2scl_nucmass_frdm_set_C
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def gamma(self):
        """
        Getter function for nucmass_frdm::gamma .
        """
        func=self._dll.o2scl_nucmass_frdm_get_gamma
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @gamma.setter
    def gamma(self,value):
        """
        Setter function for nucmass_frdm::gamma .
        """
        func=self._dll.o2scl_nucmass_frdm_set_gamma
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def amu(self):
        """
        Getter function for nucmass_frdm::amu .
        """
        func=self._dll.o2scl_nucmass_frdm_get_amu
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @amu.setter
    def amu(self,value):
        """
        Setter function for nucmass_frdm::amu .
        """
        func=self._dll.o2scl_nucmass_frdm_set_amu
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def nn(self):
        """
        Getter function for nucmass_frdm::nn .
        """
        func=self._dll.o2scl_nucmass_frdm_get_nn
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nn.setter
    def nn(self,value):
        """
        Setter function for nucmass_frdm::nn .
        """
        func=self._dll.o2scl_nucmass_frdm_set_nn
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def np(self):
        """
        Getter function for nucmass_frdm::np .
        """
        func=self._dll.o2scl_nucmass_frdm_get_np
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @np.setter
    def np(self,value):
        """
        Setter function for nucmass_frdm::np .
        """
        func=self._dll.o2scl_nucmass_frdm_set_np
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Rn(self):
        """
        Getter function for nucmass_frdm::Rn .
        """
        func=self._dll.o2scl_nucmass_frdm_get_Rn
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Rn.setter
    def Rn(self,value):
        """
        Setter function for nucmass_frdm::Rn .
        """
        func=self._dll.o2scl_nucmass_frdm_set_Rn
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def Rp(self):
        """
        Getter function for nucmass_frdm::Rp .
        """
        func=self._dll.o2scl_nucmass_frdm_get_Rp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Rp.setter
    def Rp(self,value):
        """
        Setter function for nucmass_frdm::Rp .
        """
        func=self._dll.o2scl_nucmass_frdm_set_Rp
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class nucmass_mnmsk(nucmass_table):
    """
    Python interface for class :ref:`nucmass_mnmsk <o2sclp:nucmass_mnmsk>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_mnmsk .
        """

        f=dll.o2scl_create_nucmass_mnmsk
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_mnmsk .
        """

        f=self._dll.o2scl_free_nucmass_mnmsk
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_mnmsk_exp(nucmass_mnmsk):
    """
    Python interface for class :ref:`nucmass_mnmsk_exp <o2sclp:nucmass_mnmsk_exp>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_mnmsk_exp .
        """

        f=dll.o2scl_create_nucmass_mnmsk_exp
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_mnmsk_exp .
        """

        f=self._dll.o2scl_free_nucmass_mnmsk_exp
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_gen(nucmass_table):
    """
    Python interface for class :ref:`nucmass_gen <o2sclp:nucmass_gen>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_gen .
        """

        f=dll.o2scl_create_nucmass_gen
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_gen .
        """

        f=self._dll.o2scl_free_nucmass_gen
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_dglg(nucmass_table):
    """
    Python interface for class :ref:`nucmass_dglg <o2sclp:nucmass_dglg>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_dglg .
        """

        f=dll.o2scl_create_nucmass_dglg
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_dglg .
        """

        f=self._dll.o2scl_free_nucmass_dglg
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_hfb(nucmass_table):
    """
    Python interface for class :ref:`nucmass_hfb <o2sclp:nucmass_hfb>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_hfb .
        """

        f=dll.o2scl_create_nucmass_hfb
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_hfb .
        """

        f=self._dll.o2scl_free_nucmass_hfb
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_hfb_sp(nucmass_table):
    """
    Python interface for class :ref:`nucmass_hfb_sp <o2sclp:nucmass_hfb_sp>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_hfb_sp .
        """

        f=dll.o2scl_create_nucmass_hfb_sp
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_hfb_sp .
        """

        f=self._dll.o2scl_free_nucmass_hfb_sp
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_ktuy(nucmass_table):
    """
    Python interface for class :ref:`nucmass_ktuy <o2sclp:nucmass_ktuy>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_ktuy .
        """

        f=dll.o2scl_create_nucmass_ktuy
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_ktuy .
        """

        f=self._dll.o2scl_free_nucmass_ktuy
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_sdnp(nucmass_table):
    """
    Python interface for class :ref:`nucmass_sdnp <o2sclp:nucmass_sdnp>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_sdnp .
        """

        f=dll.o2scl_create_nucmass_sdnp
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_sdnp .
        """

        f=self._dll.o2scl_free_nucmass_sdnp
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class nucmass_wlw(nucmass_table):
    """
    Python interface for class :ref:`nucmass_wlw <o2sclp:nucmass_wlw>`.
    """

    def __init__(self,dll):
        """
        Init function for class nucmass_wlw .
        """

        f=dll.o2scl_create_nucmass_wlw
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class nucmass_wlw .
        """

        f=self._dll.o2scl_free_nucmass_wlw
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

def ame_load(dll,ame,name,exp_only):
    """
    Wrapper for ame_load() .
    """
    name_=ctypes.c_char_p(force_bytes(name))
    func=dll.o2scl_ame_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool]
    func(ame._ptr,name_,exp_only)
    return

def ame_load_ext(dll,ame,file_name,table_name,exp_only):
    """
    Wrapper for ame_load_ext() .
    """
    file_name_=ctypes.c_char_p(force_bytes(file_name))
    table_name_=ctypes.c_char_p(force_bytes(table_name))
    func=dll.o2scl_ame_load_ext_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_bool]
    func(ame._ptr,file_name_,table_name_,exp_only)
    return

def mnmsk_load(dll,mnmsk,model,filename):
    """
    Wrapper for mnmsk_load() .
    """
    model_=ctypes.c_char_p(force_bytes(model))
    filename_=ctypes.c_char_p(force_bytes(filename))
    func=dll.o2scl_mnmsk_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
    func(mnmsk._ptr,model_,filename_)
    return

def hfb_load(dll,hfb,model,filename):
    """
    Wrapper for hfb_load() .
    """
    filename_=ctypes.c_char_p(force_bytes(filename))
    func=dll.o2scl_hfb_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char_p]
    func(hfb._ptr,model,filename_)
    return

def hfb_sp_load(dll,hfb,model,filename):
    """
    Wrapper for hfb_sp_load() .
    """
    filename_=ctypes.c_char_p(force_bytes(filename))
    func=dll.o2scl_hfb_sp_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_char_p]
    func(hfb._ptr,model,filename_)
    return

