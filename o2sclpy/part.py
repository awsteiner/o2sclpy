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

class thermo:
    """
    Python interface for class :ref:`thermo <o2sclp:thermo_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class thermo .
        """

        f=dll.o2scl_create_thermo
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class thermo .
        """

        f=self._dll.o2scl_free_thermo
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def ed(self):
        """
        Getter function for thermo::ed .
        """
        func=self._dll.o2scl_thermo_get_ed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ed.setter
    def ed(self,value):
        """
        Setter function for thermo::ed .
        """
        func=self._dll.o2scl_thermo_set_ed
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def pr(self):
        """
        Getter function for thermo::pr .
        """
        func=self._dll.o2scl_thermo_get_pr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @pr.setter
    def pr(self,value):
        """
        Setter function for thermo::pr .
        """
        func=self._dll.o2scl_thermo_set_pr
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def en(self):
        """
        Getter function for thermo::en .
        """
        func=self._dll.o2scl_thermo_get_en
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @en.setter
    def en(self,value):
        """
        Setter function for thermo::en .
        """
        func=self._dll.o2scl_thermo_set_en
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class part:
    """
    Python interface for class :ref:`part <o2sclp:part_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class part .
        """

        f=dll.o2scl_create_part
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class part .
        """

        f=self._dll.o2scl_free_part
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def g(self):
        """
        Getter function for part::g .
        """
        func=self._dll.o2scl_part_get_g
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @g.setter
    def g(self,value):
        """
        Setter function for part::g .
        """
        func=self._dll.o2scl_part_set_g
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def m(self):
        """
        Getter function for part::m .
        """
        func=self._dll.o2scl_part_get_m
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @m.setter
    def m(self,value):
        """
        Setter function for part::m .
        """
        func=self._dll.o2scl_part_set_m
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ms(self):
        """
        Getter function for part::ms .
        """
        func=self._dll.o2scl_part_get_ms
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ms.setter
    def ms(self,value):
        """
        Setter function for part::ms .
        """
        func=self._dll.o2scl_part_set_ms
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def mu(self):
        """
        Getter function for part::mu .
        """
        func=self._dll.o2scl_part_get_mu
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mu.setter
    def mu(self,value):
        """
        Setter function for part::mu .
        """
        func=self._dll.o2scl_part_set_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def nu(self):
        """
        Getter function for part::nu .
        """
        func=self._dll.o2scl_part_get_nu
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nu.setter
    def nu(self,value):
        """
        Setter function for part::nu .
        """
        func=self._dll.o2scl_part_set_nu
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def n(self):
        """
        Getter function for part::n .
        """
        func=self._dll.o2scl_part_get_n
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @n.setter
    def n(self,value):
        """
        Setter function for part::n .
        """
        func=self._dll.o2scl_part_set_n
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ed(self):
        """
        Getter function for part::ed .
        """
        func=self._dll.o2scl_part_get_ed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ed.setter
    def ed(self,value):
        """
        Setter function for part::ed .
        """
        func=self._dll.o2scl_part_set_ed
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def pr(self):
        """
        Getter function for part::pr .
        """
        func=self._dll.o2scl_part_get_pr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @pr.setter
    def pr(self,value):
        """
        Setter function for part::pr .
        """
        func=self._dll.o2scl_part_set_pr
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def en(self):
        """
        Getter function for part::en .
        """
        func=self._dll.o2scl_part_get_en
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @en.setter
    def en(self,value):
        """
        Setter function for part::en .
        """
        func=self._dll.o2scl_part_set_en
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def inc_rest_mass(self):
        """
        Getter function for part::inc_rest_mass .
        """
        func=self._dll.o2scl_part_get_inc_rest_mass
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @inc_rest_mass.setter
    def inc_rest_mass(self,value):
        """
        Setter function for part::inc_rest_mass .
        """
        func=self._dll.o2scl_part_set_inc_rest_mass
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def non_interacting(self):
        """
        Getter function for part::non_interacting .
        """
        func=self._dll.o2scl_part_get_non_interacting
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @non_interacting.setter
    def non_interacting(self,value):
        """
        Setter function for part::non_interacting .
        """
        func=self._dll.o2scl_part_set_non_interacting
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def init(self,mass,dof):
        """
        Wrapper for part::init() .
        wrapper for :ref:`o2sclp:part::init()`.
        """
        func=self._dll.o2scl_part_init
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        func(self._ptr,mass,dof)
        return

    def anti(self,ax):
        """
        Wrapper for part::anti() .
        wrapper for :ref:`o2sclp:part::anti()`.
        """
        func=self._dll.o2scl_part_anti
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ax._ptr)
        return

class fermion(part):
    """
    Python interface for class :ref:`fermion <o2sclp:fermion_tl>`.
    """

    def __init__(self,dll):
        """
        Init function for class fermion .
        """

        f=dll.o2scl_create_fermion
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion .
        """

        f=self._dll.o2scl_free_fermion
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def kf(self):
        """
        Getter function for fermion::kf .
        """
        func=self._dll.o2scl_fermion_get_kf
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @kf.setter
    def kf(self,value):
        """
        Setter function for fermion::kf .
        """
        func=self._dll.o2scl_fermion_set_kf
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def delta(self):
        """
        Getter function for fermion::delta .
        """
        func=self._dll.o2scl_fermion_get_delta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @delta.setter
    def delta(self,value):
        """
        Setter function for fermion::delta .
        """
        func=self._dll.o2scl_fermion_set_delta
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class quark(fermion):
    """
    Python interface for class :ref:`quark <o2sclp:quark>`.
    """

    def __init__(self,dll):
        """
        Init function for class quark .
        """

        f=dll.o2scl_create_quark
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class quark .
        """

        f=self._dll.o2scl_free_quark
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def B(self):
        """
        Getter function for quark::B .
        """
        func=self._dll.o2scl_quark_get_B
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @B.setter
    def B(self,value):
        """
        Setter function for quark::B .
        """
        func=self._dll.o2scl_quark_set_B
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def qq(self):
        """
        Getter function for quark::qq .
        """
        func=self._dll.o2scl_quark_get_qq
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @qq.setter
    def qq(self,value):
        """
        Setter function for quark::qq .
        """
        func=self._dll.o2scl_quark_set_qq
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class fermion_zerot:
    """
    Python interface for class :ref:`fermion_zerot <o2sclp:fermion_zerot_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class fermion_zerot .
        """

        f=dll.o2scl_create_fermion_zerot
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_zerot .
        """

        f=self._dll.o2scl_free_fermion_zerot
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def kf_from_density(self,f):
        """
        Wrapper for fermion_zerot::kf_from_density() .
        wrapper for :ref:`o2sclp:fermion_zerot::kf_from_density()`.
        """
        func=self._dll.o2scl_fermion_zerot_kf_from_density
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,f._ptr)
        return

    def energy_density_zerot(self,f):
        """
        Wrapper for fermion_zerot::energy_density_zerot() .
        wrapper for :ref:`o2sclp:fermion_zerot::energy_density_zerot()`.
        """
        func=self._dll.o2scl_fermion_zerot_energy_density_zerot
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,f._ptr)
        return

    def pressure_zerot(self,f):
        """
        Wrapper for fermion_zerot::pressure_zerot() .
        wrapper for :ref:`o2sclp:fermion_zerot::pressure_zerot()`.
        """
        func=self._dll.o2scl_fermion_zerot_pressure_zerot
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,f._ptr)
        return

    def calc_mu_zerot(self,f):
        """
        Wrapper for fermion_zerot::calc_mu_zerot() .
        wrapper for :ref:`o2sclp:fermion_zerot::calc_mu_zerot()`.
        """
        func=self._dll.o2scl_fermion_zerot_calc_mu_zerot
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,f._ptr)
        return

    def calc_density_zerot(self,f):
        """
        Wrapper for fermion_zerot::calc_density_zerot() .
        wrapper for :ref:`o2sclp:fermion_zerot::calc_density_zerot()`.
        """
        func=self._dll.o2scl_fermion_zerot_calc_density_zerot
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,f._ptr)
        return

class fermion_thermo(fermion_zerot):
    """
    Python interface for class :ref:`fermion_thermo <o2sclp:fermion_thermo_tl>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class fermion_thermo .
        """

        f=dll.o2scl_create_fermion_thermo
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_thermo .
        """

        f=self._dll.o2scl_free_fermion_thermo
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def calc_mu_deg(self,f,T,prec):
        """
        Wrapper for fermion_thermo::calc_mu_deg() .
        wrapper for :ref:`o2sclp:fermion_thermo::calc_mu_deg()`.
        """
        func=self._dll.o2scl_fermion_thermo_calc_mu_deg
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T,prec)
        return ret

    def calc_mu_ndeg(self,f,T,prec,inc_antip):
        """
        Wrapper for fermion_thermo::calc_mu_ndeg() .
        wrapper for :ref:`o2sclp:fermion_thermo::calc_mu_ndeg()`.
        """
        func=self._dll.o2scl_fermion_thermo_calc_mu_ndeg
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_bool]
        ret=func(self._ptr,f._ptr,T,prec,inc_antip)
        return ret

    def massless_calc_mu(self,f,T):
        """
        Wrapper for fermion_thermo::massless_calc_mu() .
        wrapper for :ref:`o2sclp:fermion_thermo::massless_calc_mu()`.
        """
        func=self._dll.o2scl_fermion_thermo_massless_calc_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

    def massless_pair_mu(self,f,T):
        """
        Wrapper for fermion_thermo::massless_pair_mu() .
        wrapper for :ref:`o2sclp:fermion_thermo::massless_pair_mu()`.
        """
        func=self._dll.o2scl_fermion_thermo_massless_pair_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

    def massless_calc_density(self,f,T):
        """
        Wrapper for fermion_thermo::massless_calc_density() .
        wrapper for :ref:`o2sclp:fermion_thermo::massless_calc_density()`.
        """
        func=self._dll.o2scl_fermion_thermo_massless_calc_density
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

    def massless_pair_density(self,f,T):
        """
        Wrapper for fermion_thermo::massless_pair_density() .
        wrapper for :ref:`o2sclp:fermion_thermo::massless_pair_density()`.
        """
        func=self._dll.o2scl_fermion_thermo_massless_pair_density
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

class fermion_rel(fermion_thermo):
    """
    Python interface for class :ref:`fermion_rel <o2sclp:fermion_rel_tl>`.
    """

    def __init__(self,dll):
        """
        Init function for class fermion_rel .
        """

        f=dll.o2scl_create_fermion_rel
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_rel .
        """

        f=self._dll.o2scl_free_fermion_rel
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def err_nonconv(self):
        """
        Getter function for fermion_rel::err_nonconv .
        """
        func=self._dll.o2scl_fermion_rel_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for fermion_rel::err_nonconv .
        """
        func=self._dll.o2scl_fermion_rel_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def min_psi(self):
        """
        Getter function for fermion_rel::min_psi .
        """
        func=self._dll.o2scl_fermion_rel_get_min_psi
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @min_psi.setter
    def min_psi(self,value):
        """
        Setter function for fermion_rel::min_psi .
        """
        func=self._dll.o2scl_fermion_rel_set_min_psi
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def deg_limit(self):
        """
        Getter function for fermion_rel::deg_limit .
        """
        func=self._dll.o2scl_fermion_rel_get_deg_limit
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @deg_limit.setter
    def deg_limit(self,value):
        """
        Setter function for fermion_rel::deg_limit .
        """
        func=self._dll.o2scl_fermion_rel_set_deg_limit
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def exp_limit(self):
        """
        Getter function for fermion_rel::exp_limit .
        """
        func=self._dll.o2scl_fermion_rel_get_exp_limit
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @exp_limit.setter
    def exp_limit(self,value):
        """
        Setter function for fermion_rel::exp_limit .
        """
        func=self._dll.o2scl_fermion_rel_set_exp_limit
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def upper_limit_fac(self):
        """
        Getter function for fermion_rel::upper_limit_fac .
        """
        func=self._dll.o2scl_fermion_rel_get_upper_limit_fac
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @upper_limit_fac.setter
    def upper_limit_fac(self,value):
        """
        Setter function for fermion_rel::upper_limit_fac .
        """
        func=self._dll.o2scl_fermion_rel_set_upper_limit_fac
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def deg_entropy_fac(self):
        """
        Getter function for fermion_rel::deg_entropy_fac .
        """
        func=self._dll.o2scl_fermion_rel_get_deg_entropy_fac
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @deg_entropy_fac.setter
    def deg_entropy_fac(self,value):
        """
        Setter function for fermion_rel::deg_entropy_fac .
        """
        func=self._dll.o2scl_fermion_rel_set_deg_entropy_fac
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def verbose(self):
        """
        Getter function for fermion_rel::verbose .
        """
        func=self._dll.o2scl_fermion_rel_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for fermion_rel::verbose .
        """
        func=self._dll.o2scl_fermion_rel_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def use_expansions(self):
        """
        Getter function for fermion_rel::use_expansions .
        """
        func=self._dll.o2scl_fermion_rel_get_use_expansions
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @use_expansions.setter
    def use_expansions(self,value):
        """
        Setter function for fermion_rel::use_expansions .
        """
        func=self._dll.o2scl_fermion_rel_set_use_expansions
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def tol_expan(self):
        """
        Getter function for fermion_rel::tol_expan .
        """
        func=self._dll.o2scl_fermion_rel_get_tol_expan
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @tol_expan.setter
    def tol_expan(self,value):
        """
        Setter function for fermion_rel::tol_expan .
        """
        func=self._dll.o2scl_fermion_rel_set_tol_expan
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def verify_ti(self):
        """
        Getter function for fermion_rel::verify_ti .
        """
        func=self._dll.o2scl_fermion_rel_get_verify_ti
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verify_ti.setter
    def verify_ti(self,value):
        """
        Setter function for fermion_rel::verify_ti .
        """
        func=self._dll.o2scl_fermion_rel_set_verify_ti
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def therm_ident(self):
        """
        Getter function for fermion_rel::therm_ident .
        """
        func=self._dll.o2scl_fermion_rel_get_therm_ident
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @therm_ident.setter
    def therm_ident(self,value):
        """
        Setter function for fermion_rel::therm_ident .
        """
        func=self._dll.o2scl_fermion_rel_set_therm_ident
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def get_unc(self,unc):
        """
        Getter function for fermion_rel::unc .
        """
        func=self._dll.o2scl_fermion_rel_get_unc
        func.restype=ctypes.c_fermion
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,unc._ptr)

    def set_unc(self,value):
        """
        Setter function for fermion_rel::unc .
        """
        func=self._dll.o2scl_fermion_rel_set_unc
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def nu_from_n(self,f,T):
        """
        Wrapper for fermion_rel::nu_from_n() .
        wrapper for :ref:`o2sclp:fermion_rel::nu_from_n()`.
        """
        func=self._dll.o2scl_fermion_rel_nu_from_n
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def calc_density(self,f,T):
        """
        Wrapper for fermion_rel::calc_density() .
        wrapper for :ref:`o2sclp:fermion_rel::calc_density()`.
        """
        func=self._dll.o2scl_fermion_rel_calc_density
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def pair_density(self,f,T):
        """
        Wrapper for fermion_rel::pair_density() .
        wrapper for :ref:`o2sclp:fermion_rel::pair_density()`.
        """
        func=self._dll.o2scl_fermion_rel_pair_density
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def calc_mu(self,f,T):
        """
        Wrapper for fermion_rel::calc_mu() .
        wrapper for :ref:`o2sclp:fermion_rel::calc_mu()`.
        """
        func=self._dll.o2scl_fermion_rel_calc_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

    def pair_mu(self,f,T):
        """
        Wrapper for fermion_rel::pair_mu() .
        wrapper for :ref:`o2sclp:fermion_rel::pair_mu()`.
        """
        func=self._dll.o2scl_fermion_rel_pair_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

class fermion_nonrel(fermion_zerot):
    """
    Python interface for class :ref:`fermion_nonrel <o2sclp:fermion_nonrel_tl>`.
    """

    def __init__(self,dll):
        """
        Init function for class fermion_nonrel .
        """

        f=dll.o2scl_create_fermion_nonrel
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_nonrel .
        """

        f=self._dll.o2scl_free_fermion_nonrel
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def calc_density(self,f,T):
        """
        Wrapper for fermion_nonrel::calc_density() .
        wrapper for :ref:`o2sclp:fermion_nonrel::calc_density()`.
        """
        func=self._dll.o2scl_fermion_nonrel_calc_density
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def calc_mu(self,f,T):
        """
        Wrapper for fermion_nonrel::calc_mu() .
        wrapper for :ref:`o2sclp:fermion_nonrel::calc_mu()`.
        """
        func=self._dll.o2scl_fermion_nonrel_calc_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

    def nu_from_n(self,f,T):
        """
        Wrapper for fermion_nonrel::nu_from_n() .
        wrapper for :ref:`o2sclp:fermion_nonrel::nu_from_n()`.
        """
        func=self._dll.o2scl_fermion_nonrel_nu_from_n
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,f._ptr,T)
        return

class boson(part):
    """
    Python interface for class :ref:`boson <o2sclp:boson>`.
    """

    def __init__(self,dll):
        """
        Init function for class boson .
        """

        f=dll.o2scl_create_boson
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class boson .
        """

        f=self._dll.o2scl_free_boson
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def co(self):
        """
        Getter function for boson::co .
        """
        func=self._dll.o2scl_boson_get_co
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @co.setter
    def co(self,value):
        """
        Setter function for boson::co .
        """
        func=self._dll.o2scl_boson_set_co
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class boson_rel:
    """
    Python interface for class :ref:`boson_rel <o2sclp:boson_rel>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class boson_rel .
        """

        f=dll.o2scl_create_boson_rel
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class boson_rel .
        """

        f=self._dll.o2scl_free_boson_rel
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def calc_density(self,b,T):
        """
        Wrapper for boson_rel::calc_density() .
        wrapper for :ref:`o2sclp:boson_rel::calc_density()`.
        """
        func=self._dll.o2scl_boson_rel_calc_density
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,b._ptr,T)
        return

    def calc_mu(self,b,T):
        """
        Wrapper for boson_rel::calc_mu() .
        wrapper for :ref:`o2sclp:boson_rel::calc_mu()`.
        """
        func=self._dll.o2scl_boson_rel_calc_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,b._ptr,T)
        return

    def nu_from_n(self,b,T):
        """
        Wrapper for boson_rel::nu_from_n() .
        wrapper for :ref:`o2sclp:boson_rel::nu_from_n()`.
        """
        func=self._dll.o2scl_boson_rel_nu_from_n
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,b._ptr,T)
        return

    def pair_density(self,b,T):
        """
        Wrapper for boson_rel::pair_density() .
        wrapper for :ref:`o2sclp:boson_rel::pair_density()`.
        """
        func=self._dll.o2scl_boson_rel_pair_density
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,b._ptr,T)
        return

    def pair_mu(self,b,T):
        """
        Wrapper for boson_rel::pair_mu() .
        wrapper for :ref:`o2sclp:boson_rel::pair_mu()`.
        """
        func=self._dll.o2scl_boson_rel_pair_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,b._ptr,T)
        return

class classical_thermo:
    """
    Python interface for class :ref:`classical_thermo <o2sclp:classical_thermo_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class classical_thermo .
        """

        f=dll.o2scl_create_classical_thermo
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class classical_thermo .
        """

        f=self._dll.o2scl_free_classical_thermo
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def calc_density(self,p,T):
        """
        Wrapper for classical_thermo::calc_density() .
        wrapper for :ref:`o2sclp:classical_thermo::calc_density()`.
        """
        func=self._dll.o2scl_classical_thermo_calc_density
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,p._ptr,T)
        return

    def calc_mu(self,p,T):
        """
        Wrapper for classical_thermo::calc_mu() .
        wrapper for :ref:`o2sclp:classical_thermo::calc_mu()`.
        """
        func=self._dll.o2scl_classical_thermo_calc_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,p._ptr,T)
        return

class thermo_np_deriv_press:
    """
    Python interface for class :ref:`thermo_np_deriv_press <o2sclp:thermo_np_deriv_press_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class thermo_np_deriv_press .
        """

        f=dll.o2scl_create_thermo_np_deriv_press
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class thermo_np_deriv_press .
        """

        f=self._dll.o2scl_free_thermo_np_deriv_press
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def dsdT(self):
        """
        Getter function for thermo_np_deriv_press::dsdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_get_dsdT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dsdT.setter
    def dsdT(self,value):
        """
        Setter function for thermo_np_deriv_press::dsdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_set_dsdT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dnndT(self):
        """
        Getter function for thermo_np_deriv_press::dnndT .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_get_dnndT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dnndT.setter
    def dnndT(self,value):
        """
        Setter function for thermo_np_deriv_press::dnndT .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_set_dnndT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dnpdT(self):
        """
        Getter function for thermo_np_deriv_press::dnpdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_get_dnpdT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dnpdT.setter
    def dnpdT(self,value):
        """
        Setter function for thermo_np_deriv_press::dnpdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_set_dnpdT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dnndmun(self):
        """
        Getter function for thermo_np_deriv_press::dnndmun .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_get_dnndmun
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dnndmun.setter
    def dnndmun(self,value):
        """
        Setter function for thermo_np_deriv_press::dnndmun .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_set_dnndmun
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dndmu_mixed(self):
        """
        Getter function for thermo_np_deriv_press::dndmu_mixed .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_get_dndmu_mixed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dndmu_mixed.setter
    def dndmu_mixed(self,value):
        """
        Setter function for thermo_np_deriv_press::dndmu_mixed .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_set_dndmu_mixed
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dnpdmup(self):
        """
        Getter function for thermo_np_deriv_press::dnpdmup .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_get_dnpdmup
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dnpdmup.setter
    def dnpdmup(self,value):
        """
        Setter function for thermo_np_deriv_press::dnpdmup .
        """
        func=self._dll.o2scl_thermo_np_deriv_press_set_dnpdmup
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class thermo_np_deriv_helm:
    """
    Python interface for class :ref:`thermo_np_deriv_helm <o2sclp:thermo_np_deriv_helm_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class thermo_np_deriv_helm .
        """

        f=dll.o2scl_create_thermo_np_deriv_helm
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class thermo_np_deriv_helm .
        """

        f=self._dll.o2scl_free_thermo_np_deriv_helm
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def dsdT(self):
        """
        Getter function for thermo_np_deriv_helm::dsdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_get_dsdT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dsdT.setter
    def dsdT(self,value):
        """
        Setter function for thermo_np_deriv_helm::dsdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_set_dsdT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dmundT(self):
        """
        Getter function for thermo_np_deriv_helm::dmundT .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_get_dmundT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dmundT.setter
    def dmundT(self,value):
        """
        Setter function for thermo_np_deriv_helm::dmundT .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_set_dmundT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dmupdT(self):
        """
        Getter function for thermo_np_deriv_helm::dmupdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_get_dmupdT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dmupdT.setter
    def dmupdT(self,value):
        """
        Setter function for thermo_np_deriv_helm::dmupdT .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_set_dmupdT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dmundnn(self):
        """
        Getter function for thermo_np_deriv_helm::dmundnn .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_get_dmundnn
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dmundnn.setter
    def dmundnn(self,value):
        """
        Setter function for thermo_np_deriv_helm::dmundnn .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_set_dmundnn
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dmudn_mixed(self):
        """
        Getter function for thermo_np_deriv_helm::dmudn_mixed .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_get_dmudn_mixed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dmudn_mixed.setter
    def dmudn_mixed(self,value):
        """
        Setter function for thermo_np_deriv_helm::dmudn_mixed .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_set_dmudn_mixed
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dmupdnp(self):
        """
        Getter function for thermo_np_deriv_helm::dmupdnp .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_get_dmupdnp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dmupdnp.setter
    def dmupdnp(self,value):
        """
        Setter function for thermo_np_deriv_helm::dmupdnp .
        """
        func=self._dll.o2scl_thermo_np_deriv_helm_set_dmupdnp
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class part_deriv_press:
    """
    Python interface for class :ref:`part_deriv_press <o2sclp:part_deriv_press_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class part_deriv_press .
        """

        f=dll.o2scl_create_part_deriv_press
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class part_deriv_press .
        """

        f=self._dll.o2scl_free_part_deriv_press
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def dndmu(self):
        """
        Getter function for part_deriv_press::dndmu .
        """
        func=self._dll.o2scl_part_deriv_press_get_dndmu
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dndmu.setter
    def dndmu(self,value):
        """
        Setter function for part_deriv_press::dndmu .
        """
        func=self._dll.o2scl_part_deriv_press_set_dndmu
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dndT(self):
        """
        Getter function for part_deriv_press::dndT .
        """
        func=self._dll.o2scl_part_deriv_press_get_dndT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dndT.setter
    def dndT(self,value):
        """
        Setter function for part_deriv_press::dndT .
        """
        func=self._dll.o2scl_part_deriv_press_set_dndT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dsdT(self):
        """
        Getter function for part_deriv_press::dsdT .
        """
        func=self._dll.o2scl_part_deriv_press_get_dsdT
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dsdT.setter
    def dsdT(self,value):
        """
        Setter function for part_deriv_press::dsdT .
        """
        func=self._dll.o2scl_part_deriv_press_set_dsdT
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def deriv_f(self,dmudn,dmudT,dsdT_n):
        """
        Wrapper for part_deriv_press::deriv_f() .
        wrapper for :ref:`o2sclp:part_deriv_press::deriv_f()`.
        """
        func=self._dll.o2scl_part_deriv_press_deriv_f
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,dmudn._ptr,dmudT._ptr,dsdT_n._ptr)
        return

class part_deriv(part):
    """
    Python interface for class :ref:`part_deriv <o2sclp:part_deriv_tl>`.
    """

    def __init__(self,dll):
        """
        Init function for class part_deriv .
        """

        f=dll.o2scl_create_part_deriv
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class part_deriv .
        """

        f=self._dll.o2scl_free_part_deriv
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class fermion_deriv(fermion):
    """
    Python interface for class :ref:`fermion_deriv <o2sclp:fermion_deriv_tl>`.
    """

    def __init__(self,dll):
        """
        Init function for class fermion_deriv .
        """

        f=dll.o2scl_create_fermion_deriv
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_deriv .
        """

        f=self._dll.o2scl_free_fermion_deriv
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class deriv_thermo_base:
    """
    Python interface for class :ref:`deriv_thermo_base <o2sclp:deriv_thermo_base_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class deriv_thermo_base .
        """

        f=dll.o2scl_create_deriv_thermo_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class deriv_thermo_base .
        """

        f=self._dll.o2scl_free_deriv_thermo_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def heat_cap_ppart_const_vol(self,p,T):
        """
        Wrapper for deriv_thermo_base::heat_cap_ppart_const_vol() .
        wrapper for :ref:`o2sclp:deriv_thermo_base::heat_cap_ppart_const_vol()`.
        """
        func=self._dll.o2scl_deriv_thermo_base_heat_cap_ppart_const_vol
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,p._ptr,T)
        return ret

    def heat_cap_ppart_const_press(self,p,T):
        """
        Wrapper for deriv_thermo_base::heat_cap_ppart_const_press() .
        wrapper for :ref:`o2sclp:deriv_thermo_base::heat_cap_ppart_const_press()`.
        """
        func=self._dll.o2scl_deriv_thermo_base_heat_cap_ppart_const_press
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,p._ptr,T)
        return ret

    def compress_adiabatic(self,p,T):
        """
        Wrapper for deriv_thermo_base::compress_adiabatic() .
        wrapper for :ref:`o2sclp:deriv_thermo_base::compress_adiabatic()`.
        """
        func=self._dll.o2scl_deriv_thermo_base_compress_adiabatic
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,p._ptr,T)
        return ret

    def compress_const_tptr(self,p,T):
        """
        Wrapper for deriv_thermo_base::compress_const_tptr() .
        wrapper for :ref:`o2sclp:deriv_thermo_base::compress_const_tptr()`.
        """
        func=self._dll.o2scl_deriv_thermo_base_compress_const_tptr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,p._ptr,T)
        return ret

    def coeff_thermal_exp(self,p,T):
        """
        Wrapper for deriv_thermo_base::coeff_thermal_exp() .
        wrapper for :ref:`o2sclp:deriv_thermo_base::coeff_thermal_exp()`.
        """
        func=self._dll.o2scl_deriv_thermo_base_coeff_thermal_exp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,p._ptr,T)
        return ret

    def squared_sound_speed(self,p,T):
        """
        Wrapper for deriv_thermo_base::squared_sound_speed() .
        wrapper for :ref:`o2sclp:deriv_thermo_base::squared_sound_speed()`.
        """
        func=self._dll.o2scl_deriv_thermo_base_squared_sound_speed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,p._ptr,T)
        return ret

class fermion_deriv_rel:
    """
    Python interface for class :ref:`fermion_deriv_rel <o2sclp:fermion_deriv_rel_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class fermion_deriv_rel .
        """

        f=dll.o2scl_create_fermion_deriv_rel
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_deriv_rel .
        """

        f=self._dll.o2scl_free_fermion_deriv_rel
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def exp_limit(self):
        """
        Getter function for fermion_deriv_rel::exp_limit .
        """
        func=self._dll.o2scl_fermion_deriv_rel_get_exp_limit
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @exp_limit.setter
    def exp_limit(self,value):
        """
        Setter function for fermion_deriv_rel::exp_limit .
        """
        func=self._dll.o2scl_fermion_deriv_rel_set_exp_limit
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def deg_limit(self):
        """
        Getter function for fermion_deriv_rel::deg_limit .
        """
        func=self._dll.o2scl_fermion_deriv_rel_get_deg_limit
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @deg_limit.setter
    def deg_limit(self,value):
        """
        Setter function for fermion_deriv_rel::deg_limit .
        """
        func=self._dll.o2scl_fermion_deriv_rel_set_deg_limit
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def upper_limit_fac(self):
        """
        Getter function for fermion_deriv_rel::upper_limit_fac .
        """
        func=self._dll.o2scl_fermion_deriv_rel_get_upper_limit_fac
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @upper_limit_fac.setter
    def upper_limit_fac(self,value):
        """
        Setter function for fermion_deriv_rel::upper_limit_fac .
        """
        func=self._dll.o2scl_fermion_deriv_rel_set_upper_limit_fac
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def get_unc(self,unc):
        """
        Getter function for fermion_deriv_rel::unc .
        """
        func=self._dll.o2scl_fermion_deriv_rel_get_unc
        func.restype=ctypes.c_fermion_deriv
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,unc._ptr)

    def set_unc(self,value):
        """
        Setter function for fermion_deriv_rel::unc .
        """
        func=self._dll.o2scl_fermion_deriv_rel_set_unc
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    @property
    def method(self):
        """
        Getter function for fermion_deriv_rel::method .
        """
        func=self._dll.o2scl_fermion_deriv_rel_get_method
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @method.setter
    def method(self,value):
        """
        Setter function for fermion_deriv_rel::method .
        """
        func=self._dll.o2scl_fermion_deriv_rel_set_method
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def last_method(self):
        """
        Getter function for fermion_deriv_rel::last_method .
        """
        func=self._dll.o2scl_fermion_deriv_rel_get_last_method
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @last_method.setter
    def last_method(self,value):
        """
        Setter function for fermion_deriv_rel::last_method .
        """
        func=self._dll.o2scl_fermion_deriv_rel_set_last_method
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Getter function for fermion_deriv_rel::err_nonconv .
        """
        func=self._dll.o2scl_fermion_deriv_rel_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for fermion_deriv_rel::err_nonconv .
        """
        func=self._dll.o2scl_fermion_deriv_rel_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def nu_from_n(self,f,T):
        """
        Wrapper for fermion_deriv_rel::nu_from_n() .
        wrapper for :ref:`o2sclp:fermion_deriv_rel::nu_from_n()`.
        """
        func=self._dll.o2scl_fermion_deriv_rel_nu_from_n
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def calc_density(self,f,T):
        """
        Wrapper for fermion_deriv_rel::calc_density() .
        wrapper for :ref:`o2sclp:fermion_deriv_rel::calc_density()`.
        """
        func=self._dll.o2scl_fermion_deriv_rel_calc_density
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def pair_density(self,f,T):
        """
        Wrapper for fermion_deriv_rel::pair_density() .
        wrapper for :ref:`o2sclp:fermion_deriv_rel::pair_density()`.
        """
        func=self._dll.o2scl_fermion_deriv_rel_pair_density
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def calc_mu(self,f,T):
        """
        Wrapper for fermion_deriv_rel::calc_mu() .
        wrapper for :ref:`o2sclp:fermion_deriv_rel::calc_mu()`.
        """
        func=self._dll.o2scl_fermion_deriv_rel_calc_mu
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def pair_mu(self,f,T):
        """
        Wrapper for fermion_deriv_rel::pair_mu() .
        wrapper for :ref:`o2sclp:fermion_deriv_rel::pair_mu()`.
        """
        func=self._dll.o2scl_fermion_deriv_rel_pair_mu
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

class fermion_deriv_nr:
    """
    Python interface for class :ref:`fermion_deriv_nr <o2sclp:fermion_deriv_nr_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class fermion_deriv_nr .
        """

        f=dll.o2scl_create_fermion_deriv_nr
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_deriv_nr .
        """

        f=self._dll.o2scl_free_fermion_deriv_nr
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def flimit(self):
        """
        Getter function for fermion_deriv_nr::flimit .
        """
        func=self._dll.o2scl_fermion_deriv_nr_get_flimit
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @flimit.setter
    def flimit(self,value):
        """
        Setter function for fermion_deriv_nr::flimit .
        """
        func=self._dll.o2scl_fermion_deriv_nr_set_flimit
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def get_unc(self,unc):
        """
        Getter function for fermion_deriv_nr::unc .
        """
        func=self._dll.o2scl_fermion_deriv_nr_get_unc
        func.restype=ctypes.c_fermion_deriv
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,unc._ptr)

    def set_unc(self,value):
        """
        Setter function for fermion_deriv_nr::unc .
        """
        func=self._dll.o2scl_fermion_deriv_nr_set_unc
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def calc_density_zerot(self,f):
        """
        Wrapper for fermion_deriv_nr::calc_density_zerot() .
        wrapper for :ref:`o2sclp:fermion_deriv_nr::calc_density_zerot()`.
        """
        func=self._dll.o2scl_fermion_deriv_nr_calc_density_zerot
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,f._ptr)
        return

    def calc_mu_zerot(self,f):
        """
        Wrapper for fermion_deriv_nr::calc_mu_zerot() .
        wrapper for :ref:`o2sclp:fermion_deriv_nr::calc_mu_zerot()`.
        """
        func=self._dll.o2scl_fermion_deriv_nr_calc_mu_zerot
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,f._ptr)
        return

    def nu_from_n(self,f,T):
        """
        Wrapper for fermion_deriv_nr::nu_from_n() .
        wrapper for :ref:`o2sclp:fermion_deriv_nr::nu_from_n()`.
        """
        func=self._dll.o2scl_fermion_deriv_nr_nu_from_n
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def calc_density(self,f,T):
        """
        Wrapper for fermion_deriv_nr::calc_density() .
        wrapper for :ref:`o2sclp:fermion_deriv_nr::calc_density()`.
        """
        func=self._dll.o2scl_fermion_deriv_nr_calc_density
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

    def calc_mu(self,f,T):
        """
        Wrapper for fermion_deriv_nr::calc_mu() .
        wrapper for :ref:`o2sclp:fermion_deriv_nr::calc_mu()`.
        """
        func=self._dll.o2scl_fermion_deriv_nr_calc_mu
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,f._ptr,T)
        return ret

class classical_deriv_thermo:
    """
    Python interface for class :ref:`classical_deriv_thermo <o2sclp:classical_deriv_thermo_tl>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class classical_deriv_thermo .
        """

        f=dll.o2scl_create_classical_deriv_thermo
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class classical_deriv_thermo .
        """

        f=self._dll.o2scl_free_classical_deriv_thermo
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def calc_density(self,p,T):
        """
        Wrapper for classical_deriv_thermo::calc_density() .
        wrapper for :ref:`o2sclp:classical_deriv_thermo::calc_density()`.
        """
        func=self._dll.o2scl_classical_deriv_thermo_calc_density
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,p._ptr,T)
        return

    def calc_mu(self,p,T):
        """
        Wrapper for classical_deriv_thermo::calc_mu() .
        wrapper for :ref:`o2sclp:classical_deriv_thermo::calc_mu()`.
        """
        func=self._dll.o2scl_classical_deriv_thermo_calc_mu
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,p._ptr,T)
        return

class fermion_mag_zerot:
    """
    Python interface for class :ref:`fermion_mag_zerot <o2sclp:fermion_mag_zerot>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class fermion_mag_zerot .
        """

        f=dll.o2scl_create_fermion_mag_zerot
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class fermion_mag_zerot .
        """

        f=self._dll.o2scl_free_fermion_mag_zerot
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def nmax_up(self):
        """
        Getter function for fermion_mag_zerot::nmax_up .
        """
        func=self._dll.o2scl_fermion_mag_zerot_get_nmax_up
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nmax_up.setter
    def nmax_up(self,value):
        """
        Setter function for fermion_mag_zerot::nmax_up .
        """
        func=self._dll.o2scl_fermion_mag_zerot_set_nmax_up
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def nmax_dn(self):
        """
        Getter function for fermion_mag_zerot::nmax_dn .
        """
        func=self._dll.o2scl_fermion_mag_zerot_get_nmax_dn
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nmax_dn.setter
    def nmax_dn(self,value):
        """
        Setter function for fermion_mag_zerot::nmax_dn .
        """
        func=self._dll.o2scl_fermion_mag_zerot_set_nmax_dn
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def sum_limit(self):
        """
        Getter function for fermion_mag_zerot::sum_limit .
        """
        func=self._dll.o2scl_fermion_mag_zerot_get_sum_limit
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @sum_limit.setter
    def sum_limit(self,value):
        """
        Setter function for fermion_mag_zerot::sum_limit .
        """
        func=self._dll.o2scl_fermion_mag_zerot_set_sum_limit
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    def calc_mu_zerot_mag(self,f,qB,kappa):
        """
        Wrapper for fermion_mag_zerot::calc_mu_zerot_mag() .
        wrapper for :ref:`o2sclp:fermion_mag_zerot::calc_mu_zerot_mag()`.
        """
        func=self._dll.o2scl_fermion_mag_zerot_calc_mu_zerot_mag
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        func(self._ptr,f._ptr,qB,kappa)
        return

    def calc_density_zerot_mag(self,f,qB,kappa):
        """
        Wrapper for fermion_mag_zerot::calc_density_zerot_mag() .
        wrapper for :ref:`o2sclp:fermion_mag_zerot::calc_density_zerot_mag()`.
        """
        func=self._dll.o2scl_fermion_mag_zerot_calc_density_zerot_mag
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        func(self._ptr,f._ptr,qB,kappa)
        return

