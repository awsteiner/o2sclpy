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

from o2sclpy.base import *

class eos_base:
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_base <o2scle:eos_base>`.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_base .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_base
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
        Delete function for class eos_base .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    def get_def_thermo(self,def_thermo):
        """
        Object of type :class:`o2scl::thermo`
        """
        func=self._link.o2scl_eos.o2scl_eos_base_get_def_thermo
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,def_thermo._ptr)
        return

    def set_def_thermo(self,value):
        """
        Setter function for eos_base::def_thermo .
        """
        func=self._link.o2scl_eos.o2scl_eos_base_set_def_thermo
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

class eos_had_base(eos_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_base <o2scle:eos_had_base>`.
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_base .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_base
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
        Delete function for class eos_had_base .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def eoa(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_eoa
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @eoa.setter
    def eoa(self,value):
        """
        Setter function for eos_had_base::eoa .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_eoa
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def msom(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_msom
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @msom.setter
    def msom(self,value):
        """
        Setter function for eos_had_base::msom .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_msom
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def comp(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_comp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @comp.setter
    def comp(self,value):
        """
        Setter function for eos_had_base::comp .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_comp
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def n0(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_n0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @n0.setter
    def n0(self,value):
        """
        Setter function for eos_had_base::n0 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_n0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def esym(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_esym
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @esym.setter
    def esym(self,value):
        """
        Setter function for eos_had_base::esym .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_esym
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def kprime(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_kprime
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @kprime.setter
    def kprime(self,value):
        """
        Setter function for eos_had_base::kprime .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_kprime
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for eos_had_base::err_nonconv .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_def_neutron(self,def_neutron):
        """
        Object of type :class:`o2scl::fermion`
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_def_neutron
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,def_neutron._ptr)
        return

    def set_def_neutron(self,value):
        """
        Setter function for eos_had_base::def_neutron .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_def_neutron
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_def_proton(self,def_proton):
        """
        Object of type :class:`o2scl::fermion`
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_get_def_proton
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,def_proton._ptr)
        return

    def set_def_proton(self,value):
        """
        Setter function for eos_had_base::def_proton .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_set_def_proton
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def calc_e(self,n,p,th):
        """
        | Parameters:
        | *n*: :ref:`o2scl::fermion` object
        | *p*: :ref:`o2scl::fermion` object
        | *th*: :ref:`o2scl::thermo` object
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_e
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,n._ptr,p._ptr,th._ptr)
        return ret

    def calc_p(self,n,p,th):
        """
        | Parameters:
        | *n*: :ref:`o2scl::fermion` object
        | *p*: :ref:`o2scl::fermion` object
        | *th*: :ref:`o2scl::thermo` object
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_p
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,n._ptr,p._ptr,th._ptr)
        return ret

    def fcomp(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fcomp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fcomp_err(self,nb,delta,unc):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | *unc*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fcomp_err
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,nb,delta,unc._ptr)
        return ret

    def feoa(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_feoa
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fesym
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_err(self,nb,delta,unc):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | *unc*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fesym_err
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,nb,delta,unc._ptr)
        return ret

    def fesym_slope(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fesym_slope
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_curve(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fesym_curve
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_skew(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fesym_skew
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fesym_diff(self,nb):
        """
        | Parameters:
        | *nb*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fesym_diff
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,nb)
        return ret

    def feta(self,nb):
        """
        | Parameters:
        | *nb*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_feta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,nb)
        return ret

    def feta_prime(self,nb):
        """
        | Parameters:
        | *nb*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_feta_prime
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,nb)
        return ret

    def fkprime(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fkprime
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fmsom(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fmsom
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_neut(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_f_effm_neut
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_prot(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_f_effm_prot
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_scalar(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_f_effm_scalar
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def f_effm_vector(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_f_effm_vector
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def fn0(self,delta,leoa):
        """
        | Parameters:
        | *delta*: ``double``
        | *leoa*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_fn0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_void_p]
        ret=func(self._ptr,delta,leoa._ptr)
        return ret

    def f_number_suscept(self,mun,mup,dPdnn,dPdnp,dPdpp):
        """
        | Parameters:
        | *mun*: ``double``
        | *mup*: ``double``
        | *dPdnn*: ``double``
        | *dPdnp*: ``double``
        | *dPdpp*: ``double``
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_f_number_suscept
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,mun,mup,dPdnn._ptr,dPdnp._ptr,dPdpp._ptr)
        return

    def f_inv_number_suscept(self,mun,mup,dednn,dednp,dedpp):
        """
        | Parameters:
        | *mun*: ``double``
        | *mup*: ``double``
        | *dednn*: ``double``
        | *dednp*: ``double``
        | *dedpp*: ``double``
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_f_inv_number_suscept
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,mun,mup,dednn._ptr,dednp._ptr,dedpp._ptr)
        return

    def saturation(self):
        """
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_saturation
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def calc_mun_e(self,nn,np):
        """
        | Parameters:
        | *nn*: ``double``
        | *np*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_mun_e
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_mup_e(self,nn,np):
        """
        | Parameters:
        | *nn*: ``double``
        | *np*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_mup_e
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_ed(self,nn,np):
        """
        | Parameters:
        | *nn*: ``double``
        | *np*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_ed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_pr(self,nn,np):
        """
        | Parameters:
        | *nn*: ``double``
        | *np*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_pr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,np)
        return ret

    def calc_nn_p(self,mun,mup):
        """
        | Parameters:
        | *mun*: ``double``
        | *mup*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_nn_p
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,mun,mup)
        return ret

    def calc_np_p(self,nn,mup):
        """
        | Parameters:
        | *nn*: ``double``
        | *mup*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_np_p
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nn,mup)
        return ret

    def calc_dmu_delta(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_dmu_delta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def calc_musum_delta(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_musum_delta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def calc_pressure_nb(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_pressure_nb
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

    def calc_edensity_nb(self,nb,delta):
        """
        | Parameters:
        | *nb*: ``double``
        | *delta*: ``double``
        | Returns: ``ctypes.c_double`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_had_base_calc_edensity_nb
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        ret=func(self._ptr,nb,delta)
        return ret

class eos_had_eden_base(eos_had_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_eden_base <o2scle:eos_had_eden_base>`.
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_eden_base .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_eden_base
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
        Delete function for class eos_had_eden_base .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_eden_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

class eos_had_pres_base(eos_had_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_pres_base <o2scle:eos_had_pres_base>`.
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_pres_base .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_pres_base
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
        Delete function for class eos_had_pres_base .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_pres_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

class eos_had_temp_base(eos_had_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_temp_base <o2scle:eos_had_temp_base>`.
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_temp_base .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_temp_base
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
        Delete function for class eos_had_temp_base .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_temp_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

class eos_had_temp_eden_base(eos_had_temp_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_temp_eden_base <o2scle:eos_had_temp_eden_base>`.
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_temp_eden_base .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_temp_eden_base
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
        Delete function for class eos_had_temp_eden_base .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_temp_eden_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

class eos_had_temp_pres_base(eos_had_temp_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_temp_pres_base <o2scle:eos_had_temp_pres_base>`.
    """

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_temp_pres_base .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_temp_pres_base
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
        Delete function for class eos_had_temp_pres_base .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_temp_pres_base
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

class eos_had_skyrme(eos_had_temp_eden_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_skyrme <o2scle:eos_had_skyrme>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_skyrme .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_skyrme
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
        Delete function for class eos_had_skyrme .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_skyrme
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def t0(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_t0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t0.setter
    def t0(self,value):
        """
        Setter function for eos_had_skyrme::t0 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_t0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def t1(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_t1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t1.setter
    def t1(self,value):
        """
        Setter function for eos_had_skyrme::t1 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_t1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def t2(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_t2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t2.setter
    def t2(self,value):
        """
        Setter function for eos_had_skyrme::t2 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_t2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def t3(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_t3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @t3.setter
    def t3(self,value):
        """
        Setter function for eos_had_skyrme::t3 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_t3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x0(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_x0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x0.setter
    def x0(self,value):
        """
        Setter function for eos_had_skyrme::x0 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_x0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x1(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_x1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x1.setter
    def x1(self,value):
        """
        Setter function for eos_had_skyrme::x1 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_x1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x2(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_x2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x2.setter
    def x2(self,value):
        """
        Setter function for eos_had_skyrme::x2 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_x2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def x3(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_x3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @x3.setter
    def x3(self,value):
        """
        Setter function for eos_had_skyrme::x3 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_x3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def alpha(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_alpha
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @alpha.setter
    def alpha(self,value):
        """
        Setter function for eos_had_skyrme::alpha .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_alpha
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_a
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a.setter
    def a(self,value):
        """
        Setter function for eos_had_skyrme::a .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_a
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_b
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b.setter
    def b(self,value):
        """
        Setter function for eos_had_skyrme::b .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_b
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def W0(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_W0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @W0.setter
    def W0(self,value):
        """
        Setter function for eos_had_skyrme::W0 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_W0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b4(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_b4
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b4.setter
    def b4(self,value):
        """
        Setter function for eos_had_skyrme::b4 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_b4
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b4p(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_b4p
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b4p.setter
    def b4p(self,value):
        """
        Setter function for eos_had_skyrme::b4p .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_b4p
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def parent_method(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_parent_method
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @parent_method.setter
    def parent_method(self,value):
        """
        Setter function for eos_had_skyrme::parent_method .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_parent_method
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_reference(self,reference):
        """
        Object of type :class:`std::string`
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_reference
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,reference._ptr)
        return

    def set_reference(self,value):
        """
        Setter function for eos_had_skyrme::reference .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_reference
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_nrfd(self,nrfd):
        """
        Object of type :class:`o2scl::fermion_deriv_nr`
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_get_nrfd
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,nrfd._ptr)
        return

    def set_nrfd(self,value):
        """
        Setter function for eos_had_skyrme::nrfd .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_skyrme_set_nrfd
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

class eos_had_apr(eos_had_temp_eden_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_apr <o2scle:eos_had_apr>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_apr .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_apr
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
        Delete function for class eos_had_apr .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_apr
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def pion(self):
        """
        Property of type ctypes.c_int
        """
        func=self._link.o2scl_eos.o2scl_eos_had_apr_get_pion
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @pion.setter
    def pion(self,value):
        """
        Setter function for eos_had_apr::pion .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_apr_set_pion
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def parent_method(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_had_apr_get_parent_method
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @parent_method.setter
    def parent_method(self,value):
        """
        Setter function for eos_had_apr::parent_method .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_apr_set_parent_method
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

class eos_had_rmf(eos_had_temp_pres_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_had_rmf <o2scle:eos_had_rmf>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_had_rmf .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_had_rmf
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
        Delete function for class eos_had_rmf .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_had_rmf
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def calc_e_steps(self):
        """
        Property of type ctypes.c_size_t
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_calc_e_steps
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @calc_e_steps.setter
    def calc_e_steps(self,value):
        """
        Setter function for eos_had_rmf::calc_e_steps .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_calc_e_steps
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def calc_e_relative(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_calc_e_relative
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @calc_e_relative.setter
    def calc_e_relative(self,value):
        """
        Setter function for eos_had_rmf::calc_e_relative .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_calc_e_relative
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def zm_mode(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_zm_mode
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @zm_mode.setter
    def zm_mode(self,value):
        """
        Setter function for eos_had_rmf::zm_mode .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_zm_mode
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def verbose(self):
        """
        Property of type ctypes.c_int
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for eos_had_rmf::verbose .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for eos_had_rmf::err_nonconv .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def mnuc(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_mnuc
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mnuc.setter
    def mnuc(self,value):
        """
        Setter function for eos_had_rmf::mnuc .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_mnuc
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ms(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_ms
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ms.setter
    def ms(self,value):
        """
        Setter function for eos_had_rmf::ms .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_ms
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def mw(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_mw
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mw.setter
    def mw(self,value):
        """
        Setter function for eos_had_rmf::mw .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_mw
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def mr(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_mr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mr.setter
    def mr(self,value):
        """
        Setter function for eos_had_rmf::mr .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_mr
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def cs(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_cs
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cs.setter
    def cs(self,value):
        """
        Setter function for eos_had_rmf::cs .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_cs
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def cw(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_cw
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cw.setter
    def cw(self,value):
        """
        Setter function for eos_had_rmf::cw .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_cw
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def cr(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_cr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @cr.setter
    def cr(self,value):
        """
        Setter function for eos_had_rmf::cr .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_cr
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_b
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b.setter
    def b(self,value):
        """
        Setter function for eos_had_rmf::b .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_b
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def c(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_c
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @c.setter
    def c(self,value):
        """
        Setter function for eos_had_rmf::c .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_c
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def zeta(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_zeta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @zeta.setter
    def zeta(self,value):
        """
        Setter function for eos_had_rmf::zeta .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_zeta
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def xi(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_xi
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @xi.setter
    def xi(self,value):
        """
        Setter function for eos_had_rmf::xi .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_xi
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a1(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_a1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a1.setter
    def a1(self,value):
        """
        Setter function for eos_had_rmf::a1 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_a1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a2(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_a2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a2.setter
    def a2(self,value):
        """
        Setter function for eos_had_rmf::a2 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_a2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a3(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_a3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a3.setter
    def a3(self,value):
        """
        Setter function for eos_had_rmf::a3 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_a3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a4(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_a4
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a4.setter
    def a4(self,value):
        """
        Setter function for eos_had_rmf::a4 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_a4
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a5(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_a5
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a5.setter
    def a5(self,value):
        """
        Setter function for eos_had_rmf::a5 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_a5
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def a6(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_a6
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @a6.setter
    def a6(self,value):
        """
        Setter function for eos_had_rmf::a6 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_a6
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b1(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_b1
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b1.setter
    def b1(self,value):
        """
        Setter function for eos_had_rmf::b1 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_b1
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b2(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_b2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b2.setter
    def b2(self,value):
        """
        Setter function for eos_had_rmf::b2 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_b2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def b3(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_get_b3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @b3.setter
    def b3(self,value):
        """
        Setter function for eos_had_rmf::b3 .
        """
        func=self._link.o2scl_eos.o2scl_eos_had_rmf_set_b3
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class eos_quark(eos_base):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_quark <o2scle:eos_quark>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_quark .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_quark
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
        Delete function for class eos_quark .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_quark
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

class eos_quark_bag(eos_quark):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_quark_bag <o2scle:eos_quark_bag>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_quark_bag .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_quark_bag
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
        Delete function for class eos_quark_bag .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_quark_bag
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def bag_constant(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_bag_get_bag_constant
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @bag_constant.setter
    def bag_constant(self,value):
        """
        Setter function for eos_quark_bag::bag_constant .
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_bag_set_bag_constant
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class eos_quark_njl(eos_quark):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_quark_njl <o2scle:eos_quark_njl>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_quark_njl .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_quark_njl
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
        Delete function for class eos_quark_njl .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_quark_njl
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def B0(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_get_B0
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @B0.setter
    def B0(self,value):
        """
        Setter function for eos_quark_njl::B0 .
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_set_B0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def L(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_get_L
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @L.setter
    def L(self,value):
        """
        Setter function for eos_quark_njl::L .
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_set_L
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def G(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_get_G
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @G.setter
    def G(self,value):
        """
        Setter function for eos_quark_njl::G .
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_set_G
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def K(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_get_K
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @K.setter
    def K(self,value):
        """
        Setter function for eos_quark_njl::K .
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_set_K
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def limit(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_get_limit
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @limit.setter
    def limit(self,value):
        """
        Setter function for eos_quark_njl::limit .
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_set_limit
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def fromqq(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_get_fromqq
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @fromqq.setter
    def fromqq(self,value):
        """
        Setter function for eos_quark_njl::fromqq .
        """
        func=self._link.o2scl_eos.o2scl_eos_quark_njl_set_fromqq
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

class eos_tov:
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_tov <o2scle:eos_tov>`.
    """

    _ptr=0
    _link=0
    _owner=True

    @abstractmethod
    def __init__(self,link,pointer=0):
        """
        Init function for class eos_tov .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_tov
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
        Delete function for class eos_tov .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_tov
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def verbose(self):
        """
        Property of type ctypes.c_int
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for eos_tov::verbose .
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    def has_baryons(self):
        """
        | Returns: ``ctypes.c_bool`` object
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_has_baryons
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

class eos_tov_buchdahl(eos_tov):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_tov_buchdahl <o2scle:eos_tov_buchdahl>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_tov_buchdahl .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_tov_buchdahl
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
        Delete function for class eos_tov_buchdahl .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_tov_buchdahl
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def Pstar(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_buchdahl_get_Pstar
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @Pstar.setter
    def Pstar(self,value):
        """
        Setter function for eos_tov_buchdahl::Pstar .
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_buchdahl_set_Pstar
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

class eos_tov_polytrope(eos_tov):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_tov_polytrope <o2scle:eos_tov_polytrope>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_tov_polytrope .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_tov_polytrope
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
        Delete function for class eos_tov_polytrope .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_tov_polytrope
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    def set_coeff_index(self,coeff,index):
        """
        | Parameters:
        | *coeff*: ``double``
        | *index*: ``double``
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_polytrope_set_coeff_index
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        func(self._ptr,coeff,index)
        return

class eos_tov_linear(eos_tov):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_tov_linear <o2scle:eos_tov_linear>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_tov_linear .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_tov_linear
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
        Delete function for class eos_tov_linear .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_tov_linear
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    def set_cs2_eps0(self,cs2,eps0):
        """
        | Parameters:
        | *cs2*: ``double``
        | *eps0*: ``double``
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_linear_set_cs2_eps0
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        func(self._ptr,cs2,eps0)
        return

class eos_tov_interp(eos_tov):
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`eos_tov_interp <o2scle:eos_tov_interp>`.
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class eos_tov_interp .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_eos_tov_interp
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
        Delete function for class eos_tov_interp .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_eos_tov_interp
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def err_nonconv(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for eos_tov_interp::err_nonconv .
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def read_table(self,eos,s_cole,s_colp,s_colnb):
        """
        | Parameters:
        | *eos*: :ref:`table_units<>` object
        | *s_cole*: string
        | *s_colp*: string
        | *s_colnb*: string
        """
        s_cole_=ctypes.c_char_p(force_bytes(s_cole))
        s_colp_=ctypes.c_char_p(force_bytes(s_colp))
        s_colnb_=ctypes.c_char_p(force_bytes(s_colnb))
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_read_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
        func(self._ptr,eos._ptr,s_cole_,s_colp_,s_colnb_)
        return

    def default_low_dens_eos(self):
        """
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_default_low_dens_eos
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def sho11_low_dens_eos(self):
        """
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_sho11_low_dens_eos
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def s12_low_dens_eos(self,model,external):
        """
        | Parameters:
        | *model*: string
        | *external*: ``bool``
        """
        model_=ctypes.c_char_p(force_bytes(model))
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_s12_low_dens_eos
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool]
        func(self._ptr,model_,external)
        return

    def gcp10_low_dens_eos(self,model,external):
        """
        | Parameters:
        | *model*: string
        | *external*: ``bool``
        """
        model_=ctypes.c_char_p(force_bytes(model))
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_gcp10_low_dens_eos
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool]
        func(self._ptr,model_,external)
        return

    def ngl13_low_dens_eos(self,L,model,external):
        """
        | Parameters:
        | *L*: ``double``
        | *model*: string
        | *external*: ``bool``
        """
        model_=ctypes.c_char_p(force_bytes(model))
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_ngl13_low_dens_eos
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_char_p,ctypes.c_bool]
        func(self._ptr,L,model_,external)
        return

    def ngl13_low_dens_eos2(self,S,L,nt,fname):
        """
        | Parameters:
        | *S*: ``double``
        | *L*: ``double``
        | *nt*: ``double``
        | *fname*: string
        """
        fname_=ctypes.c_char_p(force_bytes(fname))
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_ngl13_low_dens_eos2
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_char_p]
        func(self._ptr,S,L,nt,fname_)
        return

    def no_low_dens_eos(self):
        """
        """
        func=self._link.o2scl_eos.o2scl_eos_tov_interp_no_low_dens_eos
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

class tov_solve:
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`tov_solve <o2scle:tov_solve>`.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class tov_solve .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_tov_solve
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
        Delete function for class tov_solve .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_tov_solve
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def buffer_size(self):
        """
        Property of type ctypes.c_size_t
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_buffer_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @buffer_size.setter
    def buffer_size(self,value):
        """
        Setter function for tov_solve::buffer_size .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_buffer_size
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def max_table_size(self):
        """
        Property of type ctypes.c_size_t
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_max_table_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @max_table_size.setter
    def max_table_size(self,value):
        """
        Setter function for tov_solve::max_table_size .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_max_table_size
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def mass(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_mass
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @mass.setter
    def mass(self,value):
        """
        Setter function for tov_solve::mass .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_mass
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def rad(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_rad
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @rad.setter
    def rad(self,value):
        """
        Setter function for tov_solve::rad .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_rad
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def bmass(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_bmass
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @bmass.setter
    def bmass(self,value):
        """
        Setter function for tov_solve::bmass .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_bmass
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def gpot(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_gpot
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @gpot.setter
    def gpot(self,value):
        """
        Setter function for tov_solve::gpot .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_gpot
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def last_rjw(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_last_rjw
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @last_rjw.setter
    def last_rjw(self,value):
        """
        Setter function for tov_solve::last_rjw .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_last_rjw
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def last_f(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_last_f
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @last_f.setter
    def last_f(self,value):
        """
        Setter function for tov_solve::last_f .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_last_f
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def domega_rat(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_domega_rat
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @domega_rat.setter
    def domega_rat(self,value):
        """
        Setter function for tov_solve::domega_rat .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_domega_rat
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def pcent_max(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_pcent_max
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @pcent_max.setter
    def pcent_max(self,value):
        """
        Setter function for tov_solve::pcent_max .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_pcent_max
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def reformat_results(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_reformat_results
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @reformat_results.setter
    def reformat_results(self,value):
        """
        Setter function for tov_solve::reformat_results .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_reformat_results
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def baryon_mass(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_baryon_mass
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @baryon_mass.setter
    def baryon_mass(self,value):
        """
        Setter function for tov_solve::baryon_mass .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_baryon_mass
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def ang_vel(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_ang_vel
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @ang_vel.setter
    def ang_vel(self,value):
        """
        Setter function for tov_solve::ang_vel .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_ang_vel
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def gen_rel(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_gen_rel
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @gen_rel.setter
    def gen_rel(self,value):
        """
        Setter function for tov_solve::gen_rel .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_gen_rel
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def calc_gpot(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_calc_gpot
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @calc_gpot.setter
    def calc_gpot(self,value):
        """
        Setter function for tov_solve::calc_gpot .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_calc_gpot
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def step_min(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_step_min
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @step_min.setter
    def step_min(self,value):
        """
        Setter function for tov_solve::step_min .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_step_min
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def step_max(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_step_max
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @step_max.setter
    def step_max(self,value):
        """
        Setter function for tov_solve::step_max .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_step_max
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def step_start(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_step_start
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @step_start.setter
    def step_start(self,value):
        """
        Setter function for tov_solve::step_start .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_step_start
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def verbose(self):
        """
        Property of type ctypes.c_int
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for tov_solve::verbose .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def max_integ_steps(self):
        """
        Property of type ctypes.c_size_t
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_max_integ_steps
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @max_integ_steps.setter
    def max_integ_steps(self,value):
        """
        Setter function for tov_solve::max_integ_steps .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_max_integ_steps
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for tov_solve::err_nonconv .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def pmax_default(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_pmax_default
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @pmax_default.setter
    def pmax_default(self,value):
        """
        Setter function for tov_solve::pmax_default .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_pmax_default
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def prbegin(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_prbegin
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @prbegin.setter
    def prbegin(self,value):
        """
        Setter function for tov_solve::prbegin .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_prbegin
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def prend(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_prend
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @prend.setter
    def prend(self,value):
        """
        Setter function for tov_solve::prend .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_prend
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def princ(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_princ
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @princ.setter
    def princ(self,value):
        """
        Setter function for tov_solve::princ .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_princ
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def fixed_pr_guess(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_fixed_pr_guess
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @fixed_pr_guess.setter
    def fixed_pr_guess(self,value):
        """
        Setter function for tov_solve::fixed_pr_guess .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_fixed_pr_guess
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def max_begin(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_max_begin
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @max_begin.setter
    def max_begin(self,value):
        """
        Setter function for tov_solve::max_begin .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_max_begin
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def max_end(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_max_end
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @max_end.setter
    def max_end(self,value):
        """
        Setter function for tov_solve::max_end .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_max_end
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def max_inc(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_max_inc
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @max_inc.setter
    def max_inc(self,value):
        """
        Setter function for tov_solve::max_inc .
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_max_inc
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def set_eos(self,eos):
        """
        | Parameters:
        | *eos*: :ref:`eos_tov` object
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_set_eos
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,eos._ptr)
        return

    def mvsr(self):
        """
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_mvsr
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def fixed(self,mass):
        """
        | Parameters:
        | *mass*: ``double``
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_fixed
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,mass)
        return ret

    def max(self):
        """
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_max
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def get_results(self):
        """
        | Returns: :class:`shared_ptr_table_units`.
        """
        func=self._link.o2scl_eos.o2scl_tov_solve_get_results
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        sp=shared_ptr_table_units(self._link,func(self._ptr))
        return sp

class tov_love:
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`tov_love <o2scle:tov_love>`.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class tov_love .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_tov_love
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
        Delete function for class tov_love .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_tov_love
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def show_ode(self):
        """
        Property of type ctypes.c_int
        """
        func=self._link.o2scl_eos.o2scl_tov_love_get_show_ode
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @show_ode.setter
    def show_ode(self,value):
        """
        Setter function for tov_love::show_ode .
        """
        func=self._link.o2scl_eos.o2scl_tov_love_set_show_ode
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def addl_testing(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_tov_love_get_addl_testing
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @addl_testing.setter
    def addl_testing(self,value):
        """
        Setter function for tov_love::addl_testing .
        """
        func=self._link.o2scl_eos.o2scl_tov_love_set_addl_testing
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_tov_love_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for tov_love::err_nonconv .
        """
        func=self._link.o2scl_eos.o2scl_tov_love_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def get_results(self,results):
        """
        Object of type :class:`table_units<>`
        """
        func=self._link.o2scl_eos.o2scl_tov_love_get_results
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,results._ptr)
        return

    def set_results(self,value):
        """
        Setter function for tov_love::results .
        """
        func=self._link.o2scl_eos.o2scl_tov_love_set_results
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    @property
    def delta(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_love_get_delta
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @delta.setter
    def delta(self,value):
        """
        Setter function for tov_love::delta .
        """
        func=self._link.o2scl_eos.o2scl_tov_love_set_delta
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def eps(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_tov_love_get_eps
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @eps.setter
    def eps(self,value):
        """
        Setter function for tov_love::eps .
        """
        func=self._link.o2scl_eos.o2scl_tov_love_set_eps
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def calc_y(self,yR,beta,k2,lambda_km5,lambda_cgs,tabulate):
        """
        | Parameters:
        | *yR*: ``double``
        | *beta*: ``double``
        | *k2*: ``double``
        | *lambda_km5*: ``double``
        | *lambda_cgs*: ``double``
        | *tabulate*: ``bool``
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_tov_love_calc_y
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]
        ret=func(self._ptr,yR._ptr,beta._ptr,k2._ptr,lambda_km5._ptr,lambda_cgs._ptr,tabulate)
        return ret

    def add_disc(self,rd):
        """
        | Parameters:
        | *rd*: ``double``
        """
        func=self._link.o2scl_eos.o2scl_tov_love_add_disc
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,rd)
        return

    def clear_discs(self):
        """
        """
        func=self._link.o2scl_eos.o2scl_tov_love_clear_discs
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return

    def calc_H(self,yR,beta,k2,lambda_km5,lambda_cgs):
        """
        | Parameters:
        | *yR*: ``double``
        | *beta*: ``double``
        | *k2*: ``double``
        | *lambda_km5*: ``double``
        | *lambda_cgs*: ``double``
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_tov_love_calc_H
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,yR._ptr,beta._ptr,k2._ptr,lambda_km5._ptr,lambda_cgs._ptr)
        return ret

class nstar_cold:
    """
    Python interface for O\ :sub:`2`\ scl class :ref:`nstar_cold <o2scle:nstar_cold>`.
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class nstar_cold .
        """

        if pointer==0:
            f=link.o2scl_eos.o2scl_create_nstar_cold
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
        Delete function for class nstar_cold .
        """

        if self._owner==True:
            f=self._link.o2scl_eos.o2scl_free_nstar_cold
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
        return

    @property
    def well_formed(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_well_formed
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @well_formed.setter
    def well_formed(self,value):
        """
        Setter function for nstar_cold::well_formed .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_well_formed
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def pressure_dec(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_pressure_dec
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @pressure_dec.setter
    def pressure_dec(self,value):
        """
        Setter function for nstar_cold::pressure_dec .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_pressure_dec
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def allow_urca(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_allow_urca
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @allow_urca.setter
    def allow_urca(self,value):
        """
        Setter function for nstar_cold::allow_urca .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_allow_urca
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def deny_urca(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_deny_urca
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @deny_urca.setter
    def deny_urca(self,value):
        """
        Setter function for nstar_cold::deny_urca .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_deny_urca
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def acausal(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_acausal
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @acausal.setter
    def acausal(self,value):
        """
        Setter function for nstar_cold::acausal .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_acausal
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def acausal_ed(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_acausal_ed
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @acausal_ed.setter
    def acausal_ed(self,value):
        """
        Setter function for nstar_cold::acausal_ed .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_acausal_ed
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def acausal_pr(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_acausal_pr
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @acausal_pr.setter
    def acausal_pr(self,value):
        """
        Setter function for nstar_cold::acausal_pr .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_acausal_pr
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def solver_tol(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_solver_tol
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @solver_tol.setter
    def solver_tol(self,value):
        """
        Setter function for nstar_cold::solver_tol .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_solver_tol
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def verbose(self):
        """
        Property of type ctypes.c_int
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for nstar_cold::verbose .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def nb_start(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_nb_start
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nb_start.setter
    def nb_start(self,value):
        """
        Setter function for nstar_cold::nb_start .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_nb_start
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def nb_end(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_nb_end
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @nb_end.setter
    def nb_end(self,value):
        """
        Setter function for nstar_cold::nb_end .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_nb_end
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def dnb(self):
        """
        Property of type ctypes.c_double
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_dnb
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @dnb.setter
    def dnb(self,value):
        """
        Setter function for nstar_cold::dnb .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_dnb
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def include_muons(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_include_muons
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @include_muons.setter
    def include_muons(self,value):
        """
        Setter function for nstar_cold::include_muons .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_include_muons
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def err_nonconv(self):
        """
        Property of type ctypes.c_bool
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_err_nonconv
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @err_nonconv.setter
    def err_nonconv(self,value):
        """
        Setter function for nstar_cold::err_nonconv .
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_err_nonconv
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def set_eos(self,eos):
        """
        | Parameters:
        | *eos*: :ref:`eos_had_base` object
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_set_eos
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,eos._ptr)
        return

    def calc_eos(self,np_0):
        """
        | Parameters:
        | *np_0*: ``double``
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_calc_eos
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,np_0)
        return ret

    def calc_nstar(self):
        """
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_calc_nstar
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def fixed(self,target_mass):
        """
        | Parameters:
        | *target_mass*: ``double``
        | Returns: ``ctypes.c_int`` object
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_fixed
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,target_mass)
        return ret

    def get_eos_results(self):
        """
        | Returns: :class:`shared_ptr_table_units`.
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_eos_results
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        sp=shared_ptr_table_units(self._link,func(self._ptr))
        return sp

    def get_tov_results(self):
        """
        | Returns: :class:`shared_ptr_table_units`.
        """
        func=self._link.o2scl_eos.o2scl_nstar_cold_get_tov_results
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        sp=shared_ptr_table_units(self._link,func(self._ptr))
        return sp

def skyrme_load(link,sk,model,external,verbose):
    """
    Wrapper for skyrme_load() .
    """
    model_=ctypes.c_char_p(force_bytes(model))
    func=link.o2scl_eos.o2scl_skyrme_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool,ctypes.c_int]
    func(sk._ptr,model_,external,verbose)
    return

def rmf_load(link,rmf,model,external):
    """
    Wrapper for rmf_load() .
    """
    model_=ctypes.c_char_p(force_bytes(model))
    func=link.o2scl_eos.o2scl_rmf_load_wrapper
    func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool]
    func(rmf._ptr,model_,external)
    return

