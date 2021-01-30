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


class eos_base:
    """
    Python interface for class :ref:`eos_base <o2scle:eos_base>`.
    """

    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class eos_base .
        """

        f=dll.o2scl_create_eos_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_base .
        """

        f=self._dll.o2scl_free_eos_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def get_def_thermo(self,def_thermo):
        """
        Getter function for eos_base::def_thermo .
        """
        func=self._dll.o2scl_eos_base_get_def_thermo
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,def_thermo._ptr)
        return

    def set_def_thermo(self,value):
        """
        Setter function for eos_base::def_thermo .
        """
        func=self._dll.o2scl_eos_base_set_def_thermo
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

class eos_had_base(eos_base):
    """
    Python interface for class :ref:`eos_had_base <o2scle:eos_had_base>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class eos_had_base .
        """

        f=dll.o2scl_create_eos_had_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_base .
        """

        f=self._dll.o2scl_free_eos_had_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def eoa(self):
        """
        Getter function for eos_had_base::eoa .
        """
        func=self._dll.o2scl_eos_had_base_get_eoa
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @eoa.setter
    def eoa(self,value):
        """
        Setter function for eos_had_base::eoa .
        """
        func=self._dll.o2scl_eos_had_base_set_eoa
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def msom(self):
        """
        Getter function for eos_had_base::msom .
        """
        func=self._dll.o2scl_eos_had_base_get_msom
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @msom.setter
    def msom(self,value):
        """
        Setter function for eos_had_base::msom .
        """
        func=self._dll.o2scl_eos_had_base_set_msom
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def comp(self):
        """
        Getter function for eos_had_base::comp .
        """
        func=self._dll.o2scl_eos_had_base_get_comp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @comp.setter
    def comp(self,value):
        """
        Setter function for eos_had_base::comp .
        """
        func=self._dll.o2scl_eos_had_base_set_comp
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def n0(self):
        """
        Getter function for eos_had_base::n0 .
        """
        func=self._dll.o2scl_eos_had_base_get_n0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @n0.setter
    def n0(self,value):
        """
        Setter function for eos_had_base::n0 .
        """
        func=self._dll.o2scl_eos_had_base_set_n0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def esym(self):
        """
        Getter function for eos_had_base::esym .
        """
        func=self._dll.o2scl_eos_had_base_get_esym
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @esym.setter
    def esym(self,value):
        """
        Setter function for eos_had_base::esym .
        """
        func=self._dll.o2scl_eos_had_base_set_esym
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def kprime(self):
        """
        Getter function for eos_had_base::kprime .
        """
        func=self._dll.o2scl_eos_had_base_get_kprime
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @kprime.setter
    def kprime(self,value):
        """
        Setter function for eos_had_base::kprime .
        """
        func=self._dll.o2scl_eos_had_base_set_kprime
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Getter function for eos_had_base::err_nonconv .
        """
        func=self._dll.o2scl_eos_had_base_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for eos_had_base::err_nonconv .
        """
        func=self._dll.o2scl_eos_had_base_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_def_neutron(self,def_neutron):
        """
        Getter function for eos_had_base::def_neutron .
        """
        func=self._dll.o2scl_eos_had_base_get_def_neutron
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,def_neutron._ptr)
        return

    def set_def_neutron(self,value):
        """
        Setter function for eos_had_base::def_neutron .
        """
        func=self._dll.o2scl_eos_had_base_set_def_neutron
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_def_proton(self,def_proton):
        """
        Getter function for eos_had_base::def_proton .
        """
        func=self._dll.o2scl_eos_had_base_get_def_proton
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,def_proton._ptr)
        return

    def set_def_proton(self,value):
        """
        Setter function for eos_had_base::def_proton .
        """
        func=self._dll.o2scl_eos_had_base_set_def_proton
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def calc_e(self,n,p,th):
        """
        Wrapper for eos_had_base::calc_e() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_e()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_e
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,n._ptr,p._ptr,th._ptr)
        return ret

    def calc_p(self,n,p,th):
        """
        Wrapper for eos_had_base::calc_p() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_p()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_p
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,n._ptr,p._ptr,th._ptr)
        return ret

    def fcomp(self,nb,delta):
        """
        Wrapper for eos_had_base::fcomp() .
        wrapper for :ref:`o2sclp:eos_had_base::fcomp()`.
        """
        func=self._dll.o2scl_eos_had_base_fcomp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fcomp_err(self,nb,delta,unc):
        """
        Wrapper for eos_had_base::fcomp_err() .
        wrapper for :ref:`o2sclp:eos_had_base::fcomp_err()`.
        """
        func=self._dll.o2scl_eos_had_base_fcomp_err
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,nb,delta,unc._ptr)
        return ret

    def feoa(self,nb,delta):
        """
        Wrapper for eos_had_base::feoa() .
        wrapper for :ref:`o2sclp:eos_had_base::feoa()`.
        """
        func=self._dll.o2scl_eos_had_base_feoa
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym(self,nb,delta):
        """
        Wrapper for eos_had_base::fesym() .
        wrapper for :ref:`o2sclp:eos_had_base::fesym()`.
        """
        func=self._dll.o2scl_eos_had_base_fesym
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_err(self,nb,delta,unc):
        """
        Wrapper for eos_had_base::fesym_err() .
        wrapper for :ref:`o2sclp:eos_had_base::fesym_err()`.
        """
        func=self._dll.o2scl_eos_had_base_fesym_err
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,nb,delta,unc._ptr)
        return ret

    def fesym_slope(self,nb,delta):
        """
        Wrapper for eos_had_base::fesym_slope() .
        wrapper for :ref:`o2sclp:eos_had_base::fesym_slope()`.
        """
        func=self._dll.o2scl_eos_had_base_fesym_slope
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_curve(self,nb,delta):
        """
        Wrapper for eos_had_base::fesym_curve() .
        wrapper for :ref:`o2sclp:eos_had_base::fesym_curve()`.
        """
        func=self._dll.o2scl_eos_had_base_fesym_curve
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_skew(self,nb,delta):
        """
        Wrapper for eos_had_base::fesym_skew() .
        wrapper for :ref:`o2sclp:eos_had_base::fesym_skew()`.
        """
        func=self._dll.o2scl_eos_had_base_fesym_skew
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_diff(self,nb):
        """
        Wrapper for eos_had_base::fesym_diff() .
        wrapper for :ref:`o2sclp:eos_had_base::fesym_diff()`.
        """
        func=self._dll.o2scl_eos_had_base_fesym_diff
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,nb)
        return ret

    def feta(self,nb):
        """
        Wrapper for eos_had_base::feta() .
        wrapper for :ref:`o2sclp:eos_had_base::feta()`.
        """
        func=self._dll.o2scl_eos_had_base_feta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,nb)
        return ret

    def feta_prime(self,nb):
        """
        Wrapper for eos_had_base::feta_prime() .
        wrapper for :ref:`o2sclp:eos_had_base::feta_prime()`.
        """
        func=self._dll.o2scl_eos_had_base_feta_prime
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,nb)
        return ret

    def fkprime(self,nb,delta):
        """
        Wrapper for eos_had_base::fkprime() .
        wrapper for :ref:`o2sclp:eos_had_base::fkprime()`.
        """
        func=self._dll.o2scl_eos_had_base_fkprime
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fmsom(self,nb,delta):
        """
        Wrapper for eos_had_base::fmsom() .
        wrapper for :ref:`o2sclp:eos_had_base::fmsom()`.
        """
        func=self._dll.o2scl_eos_had_base_fmsom
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_neut(self,nb,delta):
        """
        Wrapper for eos_had_base::f_effm_neut() .
        wrapper for :ref:`o2sclp:eos_had_base::f_effm_neut()`.
        """
        func=self._dll.o2scl_eos_had_base_f_effm_neut
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_prot(self,nb,delta):
        """
        Wrapper for eos_had_base::f_effm_prot() .
        wrapper for :ref:`o2sclp:eos_had_base::f_effm_prot()`.
        """
        func=self._dll.o2scl_eos_had_base_f_effm_prot
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_scalar(self,nb,delta):
        """
        Wrapper for eos_had_base::f_effm_scalar() .
        wrapper for :ref:`o2sclp:eos_had_base::f_effm_scalar()`.
        """
        func=self._dll.o2scl_eos_had_base_f_effm_scalar
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_vector(self,nb,delta):
        """
        Wrapper for eos_had_base::f_effm_vector() .
        wrapper for :ref:`o2sclp:eos_had_base::f_effm_vector()`.
        """
        func=self._dll.o2scl_eos_had_base_f_effm_vector
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fn0(self,delta,leoa):
        """
        Wrapper for eos_had_base::fn0() .
        wrapper for :ref:`o2sclp:eos_had_base::fn0()`.
        """
        func=self._dll.o2scl_eos_had_base_fn0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,delta,leoa._ptr)
        return ret

    def f_number_suscept(self,mun,mup,dPdnn,dPdnp,dPdpp):
        """
        Wrapper for eos_had_base::f_number_suscept() .
        wrapper for :ref:`o2sclp:eos_had_base::f_number_suscept()`.
        """
        func=self._dll.o2scl_eos_had_base_f_number_suscept
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,mun,mup,dPdnn._ptr,dPdnp._ptr,dPdpp._ptr)
        return

    def f_inv_number_suscept(self,mun,mup,dednn,dednp,dedpp):
        """
        Wrapper for eos_had_base::f_inv_number_suscept() .
        wrapper for :ref:`o2sclp:eos_had_base::f_inv_number_suscept()`.
        """
        func=self._dll.o2scl_eos_had_base_f_inv_number_suscept
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,mun,mup,dednn._ptr,dednp._ptr,dedpp._ptr)
        return

    def saturation(self):
        """
        Wrapper for eos_had_base::saturation() .
        wrapper for :ref:`o2sclp:eos_had_base::saturation()`.
        """
        func=self._dll.o2scl_eos_had_base_saturation
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,]
        ret=func(self._ptr,)
        return ret

    def calc_mun_e(self,nn,np):
        """
        Wrapper for eos_had_base::calc_mun_e() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_mun_e()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_mun_e
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_mup_e(self,nn,np):
        """
        Wrapper for eos_had_base::calc_mup_e() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_mup_e()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_mup_e
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_ed(self,nn,np):
        """
        Wrapper for eos_had_base::calc_ed() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_ed()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_ed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_pr(self,nn,np):
        """
        Wrapper for eos_had_base::calc_pr() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_pr()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_pr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_nn_p(self,mun,mup):
        """
        Wrapper for eos_had_base::calc_nn_p() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_nn_p()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_nn_p
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,mun,mup)
        return ret

    def calc_np_p(self,nn,mup):
        """
        Wrapper for eos_had_base::calc_np_p() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_np_p()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_np_p
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,mup)
        return ret

    def calc_dmu_delta(self,nb,delta):
        """
        Wrapper for eos_had_base::calc_dmu_delta() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_dmu_delta()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_dmu_delta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def calc_musum_delta(self,nb,delta):
        """
        Wrapper for eos_had_base::calc_musum_delta() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_musum_delta()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_musum_delta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def calc_pressure_nb(self,nb,delta):
        """
        Wrapper for eos_had_base::calc_pressure_nb() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_pressure_nb()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_pressure_nb
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def calc_edensity_nb(self,nb,delta):
        """
        Wrapper for eos_had_base::calc_edensity_nb() .
        wrapper for :ref:`o2sclp:eos_had_base::calc_edensity_nb()`.
        """
        func=self._dll.o2scl_eos_had_base_calc_edensity_nb
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

class eos_had_eden_base(eos_had_base):
    """
    Python interface for class :ref:`eos_had_eden_base <o2scle:eos_had_eden_base>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class eos_had_eden_base .
        """

        f=dll.o2scl_create_eos_had_eden_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_eden_base .
        """

        f=self._dll.o2scl_free_eos_had_eden_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class eos_had_pres_base(eos_had_base):
    """
    Python interface for class :ref:`eos_had_pres_base <o2scle:eos_had_pres_base>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class eos_had_pres_base .
        """

        f=dll.o2scl_create_eos_had_pres_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_pres_base .
        """

        f=self._dll.o2scl_free_eos_had_pres_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class eos_had_temp_base(eos_had_base):
    """
    Python interface for class :ref:`eos_had_temp_base <o2scle:eos_had_temp_base>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class eos_had_temp_base .
        """

        f=dll.o2scl_create_eos_had_temp_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_temp_base .
        """

        f=self._dll.o2scl_free_eos_had_temp_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class eos_had_temp_eden_base(eos_had_temp_base):
    """
    Python interface for class :ref:`eos_had_temp_eden_base <o2scle:eos_had_temp_eden_base>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class eos_had_temp_eden_base .
        """

        f=dll.o2scl_create_eos_had_temp_eden_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_temp_eden_base .
        """

        f=self._dll.o2scl_free_eos_had_temp_eden_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class eos_had_temp_pres_base(eos_had_temp_base):
    """
    Python interface for class :ref:`eos_had_temp_pres_base <o2scle:eos_had_temp_pres_base>`.
    """

    @abstractmethod
    def __init__(self,dll):
        """
        Init function for class eos_had_temp_pres_base .
        """

        f=dll.o2scl_create_eos_had_temp_pres_base
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_temp_pres_base .
        """

        f=self._dll.o2scl_free_eos_had_temp_pres_base
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class eos_had_skyrme(eos_had_temp_eden_base):
    """
    Python interface for class :ref:`eos_had_skyrme <o2scle:eos_had_skyrme>`.
    """

    def __init__(self,dll):
        """
        Init function for class eos_had_skyrme .
        """

        f=dll.o2scl_create_eos_had_skyrme
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_skyrme .
        """

        f=self._dll.o2scl_free_eos_had_skyrme
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def t0(self):
        """
        Getter function for eos_had_skyrme::t0 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_t0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t0.setter
    def t0(self,value):
        """
        Setter function for eos_had_skyrme::t0 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_t0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def t1(self):
        """
        Getter function for eos_had_skyrme::t1 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_t1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t1.setter
    def t1(self,value):
        """
        Setter function for eos_had_skyrme::t1 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_t1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def t2(self):
        """
        Getter function for eos_had_skyrme::t2 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_t2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t2.setter
    def t2(self,value):
        """
        Setter function for eos_had_skyrme::t2 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_t2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def t3(self):
        """
        Getter function for eos_had_skyrme::t3 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_t3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t3.setter
    def t3(self,value):
        """
        Setter function for eos_had_skyrme::t3 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_t3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x0(self):
        """
        Getter function for eos_had_skyrme::x0 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_x0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x0.setter
    def x0(self,value):
        """
        Setter function for eos_had_skyrme::x0 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_x0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x1(self):
        """
        Getter function for eos_had_skyrme::x1 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_x1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x1.setter
    def x1(self,value):
        """
        Setter function for eos_had_skyrme::x1 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_x1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x2(self):
        """
        Getter function for eos_had_skyrme::x2 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_x2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x2.setter
    def x2(self,value):
        """
        Setter function for eos_had_skyrme::x2 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_x2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x3(self):
        """
        Getter function for eos_had_skyrme::x3 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_x3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x3.setter
    def x3(self,value):
        """
        Setter function for eos_had_skyrme::x3 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_x3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def alpha(self):
        """
        Getter function for eos_had_skyrme::alpha .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_alpha
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @alpha.setter
    def alpha(self,value):
        """
        Setter function for eos_had_skyrme::alpha .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_alpha
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a(self):
        """
        Getter function for eos_had_skyrme::a .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_a
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a.setter
    def a(self,value):
        """
        Setter function for eos_had_skyrme::a .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_a
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b(self):
        """
        Getter function for eos_had_skyrme::b .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_b
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b.setter
    def b(self,value):
        """
        Setter function for eos_had_skyrme::b .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_b
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def W0(self):
        """
        Getter function for eos_had_skyrme::W0 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_W0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @W0.setter
    def W0(self,value):
        """
        Setter function for eos_had_skyrme::W0 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_W0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b4(self):
        """
        Getter function for eos_had_skyrme::b4 .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_b4
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b4.setter
    def b4(self,value):
        """
        Setter function for eos_had_skyrme::b4 .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_b4
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b4p(self):
        """
        Getter function for eos_had_skyrme::b4p .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_b4p
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b4p.setter
    def b4p(self,value):
        """
        Setter function for eos_had_skyrme::b4p .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_b4p
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def parent_method(self):
        """
        Getter function for eos_had_skyrme::parent_method .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_parent_method
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @parent_method.setter
    def parent_method(self,value):
        """
        Setter function for eos_had_skyrme::parent_method .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_parent_method
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_reference(self,reference):
        """
        Getter function for eos_had_skyrme::reference .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_reference
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,reference._ptr)
        return

    def set_reference(self,value):
        """
        Setter function for eos_had_skyrme::reference .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_reference
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_nrfd(self,nrfd):
        """
        Getter function for eos_had_skyrme::nrfd .
        """
        func=self._dll.o2scl_eos_had_skyrme_get_nrfd
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,nrfd._ptr)
        return

    def set_nrfd(self,value):
        """
        Setter function for eos_had_skyrme::nrfd .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_nrfd
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

class eos_had_apr(eos_had_temp_eden_base):
    """
    Python interface for class :ref:`eos_had_apr <o2scle:eos_had_apr>`.
    """

    def __init__(self,dll):
        """
        Init function for class eos_had_apr .
        """

        f=dll.o2scl_create_eos_had_apr
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_apr .
        """

        f=self._dll.o2scl_free_eos_had_apr
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def pion(self):
        """
        Getter function for eos_had_apr::pion .
        """
        func=self._dll.o2scl_eos_had_apr_get_pion
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @pion.setter
    def pion(self,value):
        """
        Setter function for eos_had_apr::pion .
        """
        func=self._dll.o2scl_eos_had_apr_set_pion
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def parent_method(self):
        """
        Getter function for eos_had_apr::parent_method .
        """
        func=self._dll.o2scl_eos_had_apr_get_parent_method
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @parent_method.setter
    def parent_method(self,value):
        """
        Setter function for eos_had_apr::parent_method .
        """
        func=self._dll.o2scl_eos_had_apr_set_parent_method
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

class eos_had_rmf(eos_had_temp_pres_base):
    """
    Python interface for class :ref:`eos_had_rmf <o2scle:eos_had_rmf>`.
    """

    def __init__(self,dll):
        """
        Init function for class eos_had_rmf .
        """

        f=dll.o2scl_create_eos_had_rmf
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_had_rmf .
        """

        f=self._dll.o2scl_free_eos_had_rmf
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def calc_e_steps(self):
        """
        Getter function for eos_had_rmf::calc_e_steps .
        """
        func=self._dll.o2scl_eos_had_rmf_get_calc_e_steps
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @calc_e_steps.setter
    def calc_e_steps(self,value):
        """
        Setter function for eos_had_rmf::calc_e_steps .
        """
        func=self._dll.o2scl_eos_had_rmf_set_calc_e_steps
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def calc_e_relative(self):
        """
        Getter function for eos_had_rmf::calc_e_relative .
        """
        func=self._dll.o2scl_eos_had_rmf_get_calc_e_relative
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @calc_e_relative.setter
    def calc_e_relative(self,value):
        """
        Setter function for eos_had_rmf::calc_e_relative .
        """
        func=self._dll.o2scl_eos_had_rmf_set_calc_e_relative
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def zm_mode(self):
        """
        Getter function for eos_had_rmf::zm_mode .
        """
        func=self._dll.o2scl_eos_had_rmf_get_zm_mode
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @zm_mode.setter
    def zm_mode(self,value):
        """
        Setter function for eos_had_rmf::zm_mode .
        """
        func=self._dll.o2scl_eos_had_rmf_set_zm_mode
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def verbose(self):
        """
        Getter function for eos_had_rmf::verbose .
        """
        func=self._dll.o2scl_eos_had_rmf_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for eos_had_rmf::verbose .
        """
        func=self._dll.o2scl_eos_had_rmf_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Getter function for eos_had_rmf::err_nonconv .
        """
        func=self._dll.o2scl_eos_had_rmf_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for eos_had_rmf::err_nonconv .
        """
        func=self._dll.o2scl_eos_had_rmf_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def mnuc(self):
        """
        Getter function for eos_had_rmf::mnuc .
        """
        func=self._dll.o2scl_eos_had_rmf_get_mnuc
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mnuc.setter
    def mnuc(self,value):
        """
        Setter function for eos_had_rmf::mnuc .
        """
        func=self._dll.o2scl_eos_had_rmf_set_mnuc
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ms(self):
        """
        Getter function for eos_had_rmf::ms .
        """
        func=self._dll.o2scl_eos_had_rmf_get_ms
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ms.setter
    def ms(self,value):
        """
        Setter function for eos_had_rmf::ms .
        """
        func=self._dll.o2scl_eos_had_rmf_set_ms
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def mw(self):
        """
        Getter function for eos_had_rmf::mw .
        """
        func=self._dll.o2scl_eos_had_rmf_get_mw
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mw.setter
    def mw(self,value):
        """
        Setter function for eos_had_rmf::mw .
        """
        func=self._dll.o2scl_eos_had_rmf_set_mw
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def mr(self):
        """
        Getter function for eos_had_rmf::mr .
        """
        func=self._dll.o2scl_eos_had_rmf_get_mr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mr.setter
    def mr(self,value):
        """
        Setter function for eos_had_rmf::mr .
        """
        func=self._dll.o2scl_eos_had_rmf_set_mr
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def cs(self):
        """
        Getter function for eos_had_rmf::cs .
        """
        func=self._dll.o2scl_eos_had_rmf_get_cs
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cs.setter
    def cs(self,value):
        """
        Setter function for eos_had_rmf::cs .
        """
        func=self._dll.o2scl_eos_had_rmf_set_cs
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def cw(self):
        """
        Getter function for eos_had_rmf::cw .
        """
        func=self._dll.o2scl_eos_had_rmf_get_cw
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cw.setter
    def cw(self,value):
        """
        Setter function for eos_had_rmf::cw .
        """
        func=self._dll.o2scl_eos_had_rmf_set_cw
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def cr(self):
        """
        Getter function for eos_had_rmf::cr .
        """
        func=self._dll.o2scl_eos_had_rmf_get_cr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cr.setter
    def cr(self,value):
        """
        Setter function for eos_had_rmf::cr .
        """
        func=self._dll.o2scl_eos_had_rmf_set_cr
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b(self):
        """
        Getter function for eos_had_rmf::b .
        """
        func=self._dll.o2scl_eos_had_rmf_get_b
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b.setter
    def b(self,value):
        """
        Setter function for eos_had_rmf::b .
        """
        func=self._dll.o2scl_eos_had_rmf_set_b
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def c(self):
        """
        Getter function for eos_had_rmf::c .
        """
        func=self._dll.o2scl_eos_had_rmf_get_c
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @c.setter
    def c(self,value):
        """
        Setter function for eos_had_rmf::c .
        """
        func=self._dll.o2scl_eos_had_rmf_set_c
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def zeta(self):
        """
        Getter function for eos_had_rmf::zeta .
        """
        func=self._dll.o2scl_eos_had_rmf_get_zeta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @zeta.setter
    def zeta(self,value):
        """
        Setter function for eos_had_rmf::zeta .
        """
        func=self._dll.o2scl_eos_had_rmf_set_zeta
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def xi(self):
        """
        Getter function for eos_had_rmf::xi .
        """
        func=self._dll.o2scl_eos_had_rmf_get_xi
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @xi.setter
    def xi(self,value):
        """
        Setter function for eos_had_rmf::xi .
        """
        func=self._dll.o2scl_eos_had_rmf_set_xi
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a1(self):
        """
        Getter function for eos_had_rmf::a1 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_a1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a1.setter
    def a1(self,value):
        """
        Setter function for eos_had_rmf::a1 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_a1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a2(self):
        """
        Getter function for eos_had_rmf::a2 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_a2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a2.setter
    def a2(self,value):
        """
        Setter function for eos_had_rmf::a2 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_a2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a3(self):
        """
        Getter function for eos_had_rmf::a3 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_a3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a3.setter
    def a3(self,value):
        """
        Setter function for eos_had_rmf::a3 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_a3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a4(self):
        """
        Getter function for eos_had_rmf::a4 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_a4
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a4.setter
    def a4(self,value):
        """
        Setter function for eos_had_rmf::a4 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_a4
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a5(self):
        """
        Getter function for eos_had_rmf::a5 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_a5
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a5.setter
    def a5(self,value):
        """
        Setter function for eos_had_rmf::a5 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_a5
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a6(self):
        """
        Getter function for eos_had_rmf::a6 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_a6
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a6.setter
    def a6(self,value):
        """
        Setter function for eos_had_rmf::a6 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_a6
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b1(self):
        """
        Getter function for eos_had_rmf::b1 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_b1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b1.setter
    def b1(self,value):
        """
        Setter function for eos_had_rmf::b1 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_b1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b2(self):
        """
        Getter function for eos_had_rmf::b2 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_b2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b2.setter
    def b2(self,value):
        """
        Setter function for eos_had_rmf::b2 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_b2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b3(self):
        """
        Getter function for eos_had_rmf::b3 .
        """
        func=self._dll.o2scl_eos_had_rmf_get_b3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b3.setter
    def b3(self,value):
        """
        Setter function for eos_had_rmf::b3 .
        """
        func=self._dll.o2scl_eos_had_rmf_set_b3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class eos_quark(eos_base):
    """
    Python interface for class :ref:`eos_quark <o2scle:eos_quark>`.
    """

    def __init__(self,dll):
        """
        Init function for class eos_quark .
        """

        f=dll.o2scl_create_eos_quark
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_quark .
        """

        f=self._dll.o2scl_free_eos_quark
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

class eos_quark_bag(eos_quark):
    """
    Python interface for class :ref:`eos_quark_bag <o2scle:eos_quark_bag>`.
    """

    def __init__(self,dll):
        """
        Init function for class eos_quark_bag .
        """

        f=dll.o2scl_create_eos_quark_bag
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_quark_bag .
        """

        f=self._dll.o2scl_free_eos_quark_bag
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def bag_constant(self):
        """
        Getter function for eos_quark_bag::bag_constant .
        """
        func=self._dll.o2scl_eos_quark_bag_get_bag_constant
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @bag_constant.setter
    def bag_constant(self,value):
        """
        Setter function for eos_quark_bag::bag_constant .
        """
        func=self._dll.o2scl_eos_quark_bag_set_bag_constant
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class eos_quark_njl(eos_quark):
    """
    Python interface for class :ref:`eos_quark_njl <o2scle:eos_quark_njl>`.
    """

    def __init__(self,dll):
        """
        Init function for class eos_quark_njl .
        """

        f=dll.o2scl_create_eos_quark_njl
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class eos_quark_njl .
        """

        f=self._dll.o2scl_free_eos_quark_njl
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    @property
    def B0(self):
        """
        Getter function for eos_quark_njl::B0 .
        """
        func=self._dll.o2scl_eos_quark_njl_get_B0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @B0.setter
    def B0(self,value):
        """
        Setter function for eos_quark_njl::B0 .
        """
        func=self._dll.o2scl_eos_quark_njl_set_B0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def L(self):
        """
        Getter function for eos_quark_njl::L .
        """
        func=self._dll.o2scl_eos_quark_njl_get_L
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @L.setter
    def L(self,value):
        """
        Setter function for eos_quark_njl::L .
        """
        func=self._dll.o2scl_eos_quark_njl_set_L
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def G(self):
        """
        Getter function for eos_quark_njl::G .
        """
        func=self._dll.o2scl_eos_quark_njl_get_G
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @G.setter
    def G(self,value):
        """
        Setter function for eos_quark_njl::G .
        """
        func=self._dll.o2scl_eos_quark_njl_set_G
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def K(self):
        """
        Getter function for eos_quark_njl::K .
        """
        func=self._dll.o2scl_eos_quark_njl_get_K
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @K.setter
    def K(self,value):
        """
        Setter function for eos_quark_njl::K .
        """
        func=self._dll.o2scl_eos_quark_njl_set_K
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def limit(self):
        """
        Getter function for eos_quark_njl::limit .
        """
        func=self._dll.o2scl_eos_quark_njl_get_limit
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @limit.setter
    def limit(self,value):
        """
        Setter function for eos_quark_njl::limit .
        """
        func=self._dll.o2scl_eos_quark_njl_set_limit
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def fromqq(self):
        """
        Getter function for eos_quark_njl::fromqq .
        """
        func=self._dll.o2scl_eos_quark_njl_get_fromqq
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @fromqq.setter
    def fromqq(self,value):
        """
        Setter function for eos_quark_njl::fromqq .
        """
        func=self._dll.o2scl_eos_quark_njl_set_fromqq
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

def skyrme_load(dll,sk,model,external,verbose):
    """
    Wrapper for skyrme_load() .
    """
    model_=ctypes.c_char_p(force_bytes(model))
    func=dll.o2scl_skyrme_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool,ctypes.c_int]
    func(sk._ptr,model_,external,verbose)
    return

def rmf_load(dll,rmf,model,external):
    """
    Wrapper for rmf_load() .
    """
    model_=ctypes.c_char_p(force_bytes(model))
    func=dll.o2scl_rmf_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool]
    func(rmf._ptr,model_,external)
    return

