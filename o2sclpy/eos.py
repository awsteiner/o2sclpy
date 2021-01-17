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
        func.restype=ctypes.c_o2scl::thermo
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,def_thermo._ptr)

    def set_def_thermo(self,value):
        """
        Setter function for eos_base::def_thermo .
        """
        func=self._dll.o2scl_eos_base_set_def_thermo
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def set_thermo(self,th):
        """
        Wrapper for eos_base::set_thermo() .
        wrapper for :ref:`o2sclp:eos_base::set_thermo()`.
        """
        func=self._dll.o2scl_eos_base_set_thermo
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,th._ptr)
        return

    def get_thermo(self,):
        """
        Wrapper for eos_base::get_thermo() .
        wrapper for :ref:`o2sclp:eos_base::get_thermo()`.
        """
        func=self._dll.o2scl_eos_base_get_thermo
        func.restype=ctypes.c_o2scl::thermo
        func.argtypes=[ctypes.c_void_p,]
        ret=func(self._ptr,)
        return ret

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
        func.restype=ctypes.c_o2scl::fermion
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,def_neutron._ptr)

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
        func.restype=ctypes.c_o2scl::fermion
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,def_proton._ptr)

    def set_def_proton(self,value):
        """
        Setter function for eos_had_base::def_proton .
        """
        func=self._dll.o2scl_eos_had_base_set_def_proton
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

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
        return func(self._ptr,reference._ptr)

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
        func.restype=ctypes.c_o2scl::fermion_deriv_nr
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        return func(self._ptr,nrfd._ptr)

    def set_nrfd(self,value):
        """
        Setter function for eos_had_skyrme::nrfd .
        """
        func=self._dll.o2scl_eos_had_skyrme_set_nrfd
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

