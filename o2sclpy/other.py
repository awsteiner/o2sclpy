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

from o2sclpy.base import *

class slack_messenger:
    """
    Python interface for O\ :sub:`2`\ scl class ``slack_messenger``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/slack_messenger.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class slack_messenger

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_slack_messenger
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
        Delete function for class slack_messenger
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_slack_messenger
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class slack_messenger
        
        Returns: slack_messenger object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def verbose(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for slack_messenger::verbose .
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    def get_url(self):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_url
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string(self._link)
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_url(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_url
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_channel(self):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_channel
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string(self._link)
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_channel(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_channel
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_icon(self):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_icon
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string(self._link)
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_icon(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_icon
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_username(self):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_username
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        s=std_string(self._link)
        s._ptr=func(self._ptr)
        return s.to_bytes()

    def set_username(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_username
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    @property
    def min_time_between(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_min_time_between
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @min_time_between.setter
    def min_time_between(self,value):
        """
        Setter function for slack_messenger::min_time_between .
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_min_time_between
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def set_url_from_env(self,env_var):
        """
        | Parameters:
        | *env_var*: string
        | Returns: a Python boolean
        """
        env_var_=ctypes.c_char_p(force_bytes(env_var))
        func=self._link.o2scl.o2scl_slack_messenger_set_url_from_env
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,env_var_)
        return ret

    def set_channel_from_env(self,env_var):
        """
        | Parameters:
        | *env_var*: string
        | Returns: a Python boolean
        """
        env_var_=ctypes.c_char_p(force_bytes(env_var))
        func=self._link.o2scl.o2scl_slack_messenger_set_channel_from_env
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,env_var_)
        return ret

    def set_username_from_env(self,env_var):
        """
        | Parameters:
        | *env_var*: string
        | Returns: a Python boolean
        """
        env_var_=ctypes.c_char_p(force_bytes(env_var))
        func=self._link.o2scl.o2scl_slack_messenger_set_username_from_env
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,env_var_)
        return ret

    def send(self,message,err_on_fail=True):
        """
        | Parameters:
        | *message*: string
        | *err_on_fail* =true: ``bool``
        | Returns: a Python int
        """
        message_=ctypes.c_char_p(force_bytes(message))
        func=self._link.o2scl.o2scl_slack_messenger_send
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_bool]
        ret=func(self._ptr,message_,err_on_fail)
        return ret

    @classmethod
    def init(cls,link,p_channel,p_username,p_url,p_mpi_time):
        """
        Constructor-like class method for slack_messenger .

        | Parameters:

        """

        f=link.o2scl.o2scl_slack_messenger_init
        f.restype=ctypes.c_void_p
        f.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_bool]
        return cls(link,f(p_channel_,p_username_,p_url_,p_mpi_time))


class quadratic_real_coeff_gsl:
    """
    Python interface for O\ :sub:`2`\ scl class ``quadratic_real_coeff_gsl``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/quadratic_real_coeff_gsl.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class quadratic_real_coeff_gsl

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_quadratic_real_coeff_gsl
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
        Delete function for class quadratic_real_coeff_gsl
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_quadratic_real_coeff_gsl
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class quadratic_real_coeff_gsl
        
        Returns: quadratic_real_coeff_gsl object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def solve_r(self,a2,b2,c2):
        """
        | Parameters:
        | *a2*: ``double``
        | *b2*: ``double``
        | *c2*: ``double``
        | Returns: a Python int, a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_quadratic_real_coeff_gsl_solve_r
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
        r1_conv=ctypes.c_double(0)
        r2_conv=ctypes.c_double(0)
        ret=func(self._ptr,a2,b2,c2,ctypes.byref(r1_conv),ctypes.byref(r2_conv))
        return ret,r1_conv.value,r2_conv.value

    def solve_rc(self,a2,b2,c2,r1,r2):
        """
        | Parameters:
        | *a2*: ``double``
        | *b2*: ``double``
        | *c2*: ``double``
        | *r1*: :class:`std::complex<double>` object
        | *r2*: :class:`std::complex<double>` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_quadratic_real_coeff_gsl_solve_rc
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,a2,b2,c2,r1._ptr,r2._ptr)
        return ret


class quadratic_real_coeff_gsl2:
    """
    Python interface for O\ :sub:`2`\ scl class ``quadratic_real_coeff_gsl2<>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/quadratic_real_coeff_gsl2<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class quadratic_real_coeff_gsl2

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_quadratic_real_coeff_gsl2_
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
        Delete function for class quadratic_real_coeff_gsl2
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_quadratic_real_coeff_gsl2_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class quadratic_real_coeff_gsl2
        
        Returns: quadratic_real_coeff_gsl2 object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def solve_r(self,a2,b2,c2):
        """
        | Parameters:
        | *a2*: ``double``
        | *b2*: ``double``
        | *c2*: ``double``
        | Returns: a Python int, a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_quadratic_real_coeff_gsl2__solve_r
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
        r1_conv=ctypes.c_double(0)
        r2_conv=ctypes.c_double(0)
        ret=func(self._ptr,a2,b2,c2,ctypes.byref(r1_conv),ctypes.byref(r2_conv))
        return ret,r1_conv.value,r2_conv.value

    def solve_rc(self,a2,b2,c2,r1,r2):
        """
        | Parameters:
        | *a2*: ``double``
        | *b2*: ``double``
        | *c2*: ``double``
        | *r1*: :class:`std::complex<double>` object
        | *r2*: :class:`std::complex<double>` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_quadratic_real_coeff_gsl2__solve_rc
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,a2,b2,c2,r1._ptr,r2._ptr)
        return ret


class cubic_real_coeff_cern:
    """
    Python interface for O\ :sub:`2`\ scl class ``cubic_real_coeff_cern<>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/cubic_real_coeff_cern<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class cubic_real_coeff_cern

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_cubic_real_coeff_cern_
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
        Delete function for class cubic_real_coeff_cern
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_cubic_real_coeff_cern_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class cubic_real_coeff_cern
        
        Returns: cubic_real_coeff_cern object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def solve_r(self,a3,b3,c3,d3):
        """
        | Parameters:
        | *a3*: ``double``
        | *b3*: ``double``
        | *c3*: ``double``
        | *d3*: ``double``
        | Returns: a Python int, a Python float, a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_cubic_real_coeff_cern__solve_r
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
        r1_conv=ctypes.c_double(0)
        r2_conv=ctypes.c_double(0)
        r3_conv=ctypes.c_double(0)
        ret=func(self._ptr,a3,b3,c3,d3,ctypes.byref(r1_conv),ctypes.byref(r2_conv),ctypes.byref(r3_conv))
        return ret,r1_conv.value,r2_conv.value,r3_conv.value

    def solve_rc(self,a3,b3,c3,d3,r2,r3):
        """
        | Parameters:
        | *a3*: ``double``
        | *b3*: ``double``
        | *c3*: ``double``
        | *d3*: ``double``
        | *r2*: :class:`std::complex<double>` object
        | *r3*: :class:`std::complex<double>` object
        | Returns: a Python int, a Python float
        """
        func=self._link.o2scl.o2scl_cubic_real_coeff_cern__solve_rc
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.c_void_p,ctypes.c_void_p]
        r1_conv=ctypes.c_double(0)
        ret=func(self._ptr,a3,b3,c3,d3,ctypes.byref(r1_conv),r2._ptr,r3._ptr)
        return ret,r1_conv.value


class cubic_real_coeff_gsl:
    """
    Python interface for O\ :sub:`2`\ scl class ``cubic_real_coeff_gsl``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/cubic_real_coeff_gsl.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class cubic_real_coeff_gsl

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_cubic_real_coeff_gsl
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
        Delete function for class cubic_real_coeff_gsl
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_cubic_real_coeff_gsl
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class cubic_real_coeff_gsl
        
        Returns: cubic_real_coeff_gsl object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def solve_r(self,a3,b3,c3,d3):
        """
        | Parameters:
        | *a3*: ``double``
        | *b3*: ``double``
        | *c3*: ``double``
        | *d3*: ``double``
        | Returns: a Python int, a Python float, a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_cubic_real_coeff_gsl_solve_r
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
        r1_conv=ctypes.c_double(0)
        r2_conv=ctypes.c_double(0)
        r3_conv=ctypes.c_double(0)
        ret=func(self._ptr,a3,b3,c3,d3,ctypes.byref(r1_conv),ctypes.byref(r2_conv),ctypes.byref(r3_conv))
        return ret,r1_conv.value,r2_conv.value,r3_conv.value

    def solve_rc(self,a3,b3,c3,d3,r2,r3):
        """
        | Parameters:
        | *a3*: ``double``
        | *b3*: ``double``
        | *c3*: ``double``
        | *d3*: ``double``
        | *r2*: :class:`std::complex<double>` object
        | *r3*: :class:`std::complex<double>` object
        | Returns: a Python int, a Python float
        """
        func=self._link.o2scl.o2scl_cubic_real_coeff_gsl_solve_rc
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.c_void_p,ctypes.c_void_p]
        r1_conv=ctypes.c_double(0)
        ret=func(self._ptr,a3,b3,c3,d3,ctypes.byref(r1_conv),r2._ptr,r3._ptr)
        return ret,r1_conv.value


class quartic_real_coeff_cern:
    """
    Python interface for O\ :sub:`2`\ scl class ``quartic_real_coeff_cern<>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/quartic_real_coeff_cern<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class quartic_real_coeff_cern

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_quartic_real_coeff_cern_
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
        Delete function for class quartic_real_coeff_cern
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_quartic_real_coeff_cern_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class quartic_real_coeff_cern
        
        Returns: quartic_real_coeff_cern object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def solve_r(self,a4,b4,c4,d4,e4):
        """
        | Parameters:
        | *a4*: ``double``
        | *b4*: ``double``
        | *c4*: ``double``
        | *d4*: ``double``
        | *e4*: ``double``
        | Returns: a Python int, a Python float, a Python float, a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_quartic_real_coeff_cern__solve_r
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
        r1_conv=ctypes.c_double(0)
        r2_conv=ctypes.c_double(0)
        r3_conv=ctypes.c_double(0)
        r4_conv=ctypes.c_double(0)
        ret=func(self._ptr,a4,b4,c4,d4,e4,ctypes.byref(r1_conv),ctypes.byref(r2_conv),ctypes.byref(r3_conv),ctypes.byref(r4_conv))
        return ret,r1_conv.value,r2_conv.value,r3_conv.value,r4_conv.value

    def solve_rc(self,a4,b4,c4,d4,e4,r1,r2,r3,r4):
        """
        | Parameters:
        | *a4*: ``double``
        | *b4*: ``double``
        | *c4*: ``double``
        | *d4*: ``double``
        | *e4*: ``double``
        | *r1*: :class:`std::complex<double>` object
        | *r2*: :class:`std::complex<double>` object
        | *r3*: :class:`std::complex<double>` object
        | *r4*: :class:`std::complex<double>` object
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_quartic_real_coeff_cern__solve_rc
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,a4,b4,c4,d4,e4,r1._ptr,r2._ptr,r3._ptr,r4._ptr)
        return ret


class fermi_dirac_integ_gsl:
    """
    Python interface for O\ :sub:`2`\ scl class ``fermi_dirac_integ_gsl``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/fermi_dirac_integ_gsl.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class fermi_dirac_integ_gsl

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_fermi_dirac_integ_gsl
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
        Delete function for class fermi_dirac_integ_gsl
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_fermi_dirac_integ_gsl
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class fermi_dirac_integ_gsl
        
        Returns: fermi_dirac_integ_gsl object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def calc_m1o2(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_fermi_dirac_integ_gsl_calc_m1o2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def calc_1o2(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_fermi_dirac_integ_gsl_calc_1o2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def calc_3o2(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_fermi_dirac_integ_gsl_calc_3o2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def calc_2(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_fermi_dirac_integ_gsl_calc_2
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def calc_3(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_fermi_dirac_integ_gsl_calc_3
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret


class bessel_K_exp_integ_gsl:
    """
    Python interface for O\ :sub:`2`\ scl class ``bessel_K_exp_integ_gsl``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/bessel_K_exp_integ_gsl.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class bessel_K_exp_integ_gsl

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_bessel_K_exp_integ_gsl
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
        Delete function for class bessel_K_exp_integ_gsl
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_bessel_K_exp_integ_gsl
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class bessel_K_exp_integ_gsl
        
        Returns: bessel_K_exp_integ_gsl object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def K1exp(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_bessel_K_exp_integ_gsl_K1exp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def K2exp(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_bessel_K_exp_integ_gsl_K2exp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def K3exp(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_bessel_K_exp_integ_gsl_K3exp
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret


class hist:
    """
    Python interface for O\ :sub:`2`\ scl class ``hist``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/hist.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class hist

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_hist
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
        Delete function for class hist
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_hist
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class hist
        
        Returns: hist object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class hist
        
        Returns: new copy of the hist object
        """

        new_obj=type(self)(self._link)
        f2=self._link.o2scl.o2scl_copy_hist
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    @property
    def extend_rhs(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_hist_get_extend_rhs
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @extend_rhs.setter
    def extend_rhs(self,value):
        """
        Setter function for hist::extend_rhs .
        """
        func=self._link.o2scl.o2scl_hist_set_extend_rhs
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    @property
    def extend_lhs(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_hist_get_extend_lhs
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @extend_lhs.setter
    def extend_lhs(self,value):
        """
        Setter function for hist::extend_lhs .
        """
        func=self._link.o2scl.o2scl_hist_set_extend_lhs
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def create_rep_vec(self,v):
        """
        | Parameters:
        | *v*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_hist_create_rep_vec
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,v._ptr)
        return

    def get_wgts(self):
        """
        | Returns: ublas_vector object
        """
        func=self._link.o2scl.o2scl_hist_get_wgts
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        ret2=ublas_vector(self._link,ret)
        return ret2

    def get_bins(self):
        """
        | Returns: ublas_vector object
        """
        func=self._link.o2scl.o2scl_hist_get_bins
        func.restype=ctypes.c_void_p
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        ret2=ublas_vector(self._link,ret)
        return ret2

    def from_table(self,t,colx,n_bins):
        """
        | Parameters:
        | *t*: :class:`table<>` object
        | *colx*: string
        | *n_bins*: ``size_t``
        """
        colx_=ctypes.c_char_p(force_bytes(colx))
        func=self._link.o2scl.o2scl_hist_from_table
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t]
        func(self._ptr,t._ptr,colx_,n_bins)
        return

    def from_table_twocol(self,t,colx,coly,n_bins):
        """
        | Parameters:
        | *t*: :class:`table<>` object
        | *colx*: string
        | *coly*: string
        | *n_bins*: ``size_t``
        """
        colx_=ctypes.c_char_p(force_bytes(colx))
        coly_=ctypes.c_char_p(force_bytes(coly))
        func=self._link.o2scl.o2scl_hist_from_table_twocol
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_size_t]
        func(self._ptr,t._ptr,colx_,coly_,n_bins)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_hist_size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def set_bin_edges_grid(self,g):
        """
        | Parameters:
        | *g*: :class:`uniform_grid<double>` object
        """
        func=self._link.o2scl.o2scl_hist_set_bin_edges_grid
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,g._ptr)
        return

    def set_bin_edges_vec(self,n,v):
        """
        | Parameters:
        | *n*: ``size_t``
        | *v*: :class:`vector<double>` object
        """
        func=self._link.o2scl.o2scl_hist_set_bin_edges_vec
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,n,v._ptr)
        return

    def update(self,x,val=1.0):
        """
        | Parameters:
        | *x*: ``double``
        | *val* =1.0: ``double``
        """
        func=self._link.o2scl.o2scl_hist_update
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        func(self._ptr,x,val)
        return

    def update_i(self,i,val=1.0):
        """
        | Parameters:
        | *i*: ``size_t``
        | *val* =1.0: ``double``
        """
        func=self._link.o2scl.o2scl_hist_update_i
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,i,val)
        return

    def get_wgt_i(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_hist_get_wgt_i
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def get_wgt(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_hist_get_wgt
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def set_wgt_i(self,i,x):
        """
        | Parameters:
        | *i*: ``size_t``
        | *x*: ``double``
        """
        func=self._link.o2scl.o2scl_hist_set_wgt_i
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double]
        func(self._ptr,i,x)
        return

    def set_wgt(self,x,val):
        """
        | Parameters:
        | *x*: ``double``
        | *val*: ``double``
        """
        func=self._link.o2scl.o2scl_hist_set_wgt
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double]
        func(self._ptr,x,val)
        return

    def __getitem__(self,i):
        """
        | Parameters:
        | *i*: ``size_t``
        """
        func=self._link.o2scl.o2scl_hist_getitem
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,i)
        return ret

    def get_bin_index(self,x):
        """
        | Parameters:
        | *x*: ``double``
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_hist_get_bin_index
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,x)
        return ret

    def function(self,func):
        """
        | Parameters:
        | *func*: string
        | Returns: a Python int
        """
        func_=ctypes.c_char_p(force_bytes(func))
        func=self._link.o2scl.o2scl_hist_function
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        ret=func(self._ptr,func_)
        return ret

    def clear(self):
        """
        """
        func=self._link.o2scl.o2scl_hist_clear
        func.argtypes=[ctypes.c_void_p]
        func(self._ptr)
        return


class contour_line:
    """
    Python interface for O\ :sub:`2`\ scl class ``contour_line``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/contour_line.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class contour_line

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_contour_line
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
        Delete function for class contour_line
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_contour_line
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class contour_line
        
        Returns: contour_line object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class contour_line
        
        Returns: new copy of the contour_line object
        """

        new_obj=type(self)(self._link)
        f2=self._link.o2scl.o2scl_copy_contour_line
        f2.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        f2(self._ptr,new_obj._ptr)
        return new_obj

    @property
    def level(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_contour_line_get_level
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @level.setter
    def level(self,value):
        """
        Setter function for contour_line::level .
        """
        func=self._link.o2scl.o2scl_contour_line_set_level
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    def get_x(self):
        """
        Get object of type :class:`std::vector<double>`
        """
        func1=self._link.o2scl.o2scl_contour_line_get_x
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector(self._link,ptr)
        return obj

    def set_x(self,value):
        """
        Set object of type :class:`std::vector<double>`
        """
        func=self._link.o2scl.o2scl_contour_line_set_x
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_y(self):
        """
        Get object of type :class:`std::vector<double>`
        """
        func1=self._link.o2scl.o2scl_contour_line_get_y
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector(self._link,ptr)
        return obj

    def set_y(self,value):
        """
        Set object of type :class:`std::vector<double>`
        """
        func=self._link.o2scl.o2scl_contour_line_set_y
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return


class vector_contour_line:
    """
    Python interface for O\ :sub:`2`\ scl class ``std::vector<contour_line>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/std::vector<contour_line>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class vector_contour_line

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_vector_contour_line_
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
        Delete function for class vector_contour_line
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_contour_line_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class vector_contour_line
        
        Returns: vector_contour_line object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __getitem__(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_contour_line__getitem
        func.restype=ctypes.c_contour_line
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        ret=func(self._ptr,n)
        return ret

    def __setitem__(self,i,value):
        """
        | Parameters:
        | *i*: ``size_t``
        | *value*: ``contour_line``
        """
        func=self._link.o2scl.o2scl_std_vector_contour_line__setitem
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_contour_line]
        func(self._ptr,i,value)
        return

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_contour_line__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_contour_line__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __len__(self):
        """
        Return the length of the vector
    
        Returns: an int
        """
        return self.length()
     

class contour:
    """
    Python interface for O\ :sub:`2`\ scl class ``contour``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/contour.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class contour

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_contour
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
        Delete function for class contour
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_contour
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class contour
        
        Returns: contour object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def verbose(self):
        """
        Property of type ``ctypes.c_int``
        """
        func=self._link.o2scl.o2scl_contour_get_verbose
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @verbose.setter
    def verbose(self,value):
        """
        Setter function for contour::verbose .
        """
        func=self._link.o2scl.o2scl_contour_set_verbose
        func.argtypes=[ctypes.c_void_p,ctypes.c_int]
        func(self._ptr,value)
        return

    @property
    def lev_adjust(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_contour_get_lev_adjust
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @lev_adjust.setter
    def lev_adjust(self,value):
        """
        Setter function for contour::lev_adjust .
        """
        func=self._link.o2scl.o2scl_contour_set_lev_adjust
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def debug_next_point(self):
        """
        Property of type ``ctypes.c_bool``
        """
        func=self._link.o2scl.o2scl_contour_get_debug_next_point
        func.restype=ctypes.c_bool
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @debug_next_point.setter
    def debug_next_point(self,value):
        """
        Setter function for contour::debug_next_point .
        """
        func=self._link.o2scl.o2scl_contour_set_debug_next_point
        func.argtypes=[ctypes.c_void_p,ctypes.c_bool]
        func(self._ptr,value)
        return

    def set_data(self,ugx,ugy,udata):
        """
        | Parameters:
        | *ugx*: :class:`uniform_grid<double>` object
        | *ugy*: :class:`uniform_grid<double>` object
        | *udata*: :class:`ublas_matrix` object
        """
        func=self._link.o2scl.o2scl_contour_set_data
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,ugx._ptr,ugy._ptr,udata._ptr)
        return

    def set_levels(self,n_levels,levels):
        """
        | Parameters:
        | *n_levels*: ``size_t``
        | *levels*: :class:`vector<size_t>` object
        """
        func=self._link.o2scl.o2scl_contour_set_levels
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]
        func(self._ptr,n_levels,levels._ptr)
        return

    def calc_contours(self,clines):
        """
        | Parameters:
        | *clines*: :class:`vector<contour_line>` object
        """
        func=self._link.o2scl.o2scl_contour_calc_contours
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,clines._ptr)
        return


class prob_dens_mdim:
    """
    Python interface for O\ :sub:`2`\ scl class ``prob_dens_mdim<std::vector<double>>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/prob_dens_mdim<std::vector<double>>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class prob_dens_mdim

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_prob_dens_mdim_std_vector_double_
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
        Delete function for class prob_dens_mdim
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_prob_dens_mdim_std_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class prob_dens_mdim
        
        Returns: prob_dens_mdim object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def pdf(self,x):
        """
        | Parameters:
        | *x*: :class:`std_vector` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_std_vector_double__pdf
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,x._ptr)
        return ret

    def log_pdf(self,x):
        """
        | Parameters:
        | *x*: :class:`std_vector` object
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_std_vector_double__log_pdf
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        ret=func(self._ptr,x._ptr)
        return ret

    def dim(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_std_vector_double__dim
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret

    def __getitem__(self,x):
        """
        | Parameters:
        | *x*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_std_vector_double__getitem
        func.restype=ctypes.c_void
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,x._ptr)
        return


class prob_dens_mdim_biv_gaussian(prob_dens_mdim):
    """
    Python interface for O\ :sub:`2`\ scl class ``prob_dens_mdim_biv_gaussian<std::vector<double>>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/prob_dens_mdim_biv_gaussian<std::vector<double>>.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class prob_dens_mdim_biv_gaussian

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_prob_dens_mdim_biv_gaussian_std_vector_double_
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
        Delete function for class prob_dens_mdim_biv_gaussian
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_prob_dens_mdim_biv_gaussian_std_vector_double_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class prob_dens_mdim_biv_gaussian
        
        Returns: prob_dens_mdim_biv_gaussian object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def set(self,x_cent,y_cent,x_std,y_std,covar):
        """
        | Parameters:
        | *x_cent*: ``double``
        | *y_cent*: ``double``
        | *x_std*: ``double``
        | *y_std*: ``double``
        | *covar*: ``double``
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_biv_gaussian_std_vector_double__set
        func.argtypes=[ctypes.c_void_p,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]
        func(self._ptr,x_cent,y_cent,x_std,y_std,covar)
        return

    def get(self):
        """
        | Parameters:
        | Returns: , a Python float, a Python float, a Python float, a Python float, a Python float
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_biv_gaussian_std_vector_double__get
        func.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
        x_cent_conv=ctypes.c_double(0)
        y_cent_conv=ctypes.c_double(0)
        x_std_conv=ctypes.c_double(0)
        y_std_conv=ctypes.c_double(0)
        covar_conv=ctypes.c_double(0)
        func(self._ptr,ctypes.byref(x_cent_conv),ctypes.byref(y_cent_conv),ctypes.byref(x_std_conv),ctypes.byref(y_std_conv),ctypes.byref(covar_conv))
        return x_cent_conv.value,y_cent_conv.value,x_std_conv.value,y_std_conv.value,covar_conv.value

    def level_fixed_integral(self,integral):
        """
        | Parameters:
        | *integral*: ``double``
        | Returns: a Python float
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_biv_gaussian_std_vector_double__level_fixed_integral
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        ret=func(self._ptr,integral)
        return ret


class prob_dens_mdim_gaussian(prob_dens_mdim):
    """
    Python interface for O\ :sub:`2`\ scl class ``prob_dens_mdim_gaussian<>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/prob_dens_mdim_gaussian<>.html .
    """

    def __init__(self,link,pointer=0):
        """
        Init function for class prob_dens_mdim_gaussian

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_prob_dens_mdim_gaussian_
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
        Delete function for class prob_dens_mdim_gaussian
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_prob_dens_mdim_gaussian_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class prob_dens_mdim_gaussian
        
        Returns: prob_dens_mdim_gaussian object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


class hypercube:
    """
    Python interface for O\ :sub:`2`\ scl class ``prob_dens_mdim_amr<>::hypercube``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/prob_dens_mdim_amr<>::hypercube.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class hypercube

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_prob_dens_mdim_amr_hypercube
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
        Delete function for class hypercube
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_prob_dens_mdim_amr_hypercube
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class hypercube
        
        Returns: hypercube object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    @property
    def n_dim(self):
        """
        Property of type ``ctypes.c_size_t``
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_get_n_dim
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @n_dim.setter
    def n_dim(self,value):
        """
        Setter function for prob_dens_mdim_amr<>::hypercube::n_dim .
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_set_n_dim
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,value)
        return

    def get_low(self):
        """
        Get object of type :class:`std::vector<double>`
        """
        func1=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_get_low
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector(self._link,ptr)
        return obj

    def set_low(self,value):
        """
        Set object of type :class:`std::vector<double>`
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_set_low
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_high(self):
        """
        Get object of type :class:`std::vector<double>`
        """
        func1=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_get_high
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector(self._link,ptr)
        return obj

    def set_high(self,value):
        """
        Set object of type :class:`std::vector<double>`
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_set_high
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_inside(self):
        """
        Get object of type :class:`std::vector<size_t>`
        """
        func1=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_get_inside
        func1.restype=ctypes.c_void_p
        func1.argtypes=[ctypes.c_void_p]
        ptr=func1(self._ptr)
        obj=std_vector_size_t(self._link,ptr)
        return obj

    def set_inside(self,value):
        """
        Set object of type :class:`std::vector<size_t>`
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_set_inside
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    @property
    def frac_vol(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_get_frac_vol
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @frac_vol.setter
    def frac_vol(self,value):
        """
        Setter function for prob_dens_mdim_amr<>::hypercube::frac_vol .
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_set_frac_vol
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return

    @property
    def weight(self):
        """
        Property of type ``ctypes.c_double``
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_get_weight
        func.restype=ctypes.c_double
        func.argtypes=[ctypes.c_void_p]
        return func(self._ptr)

    @weight.setter
    def weight(self,value):
        """
        Setter function for prob_dens_mdim_amr<>::hypercube::weight .
        """
        func=self._link.o2scl.o2scl_prob_dens_mdim_amr_hypercube_set_weight
        func.argtypes=[ctypes.c_void_p,ctypes.c_double]
        func(self._ptr,value)
        return


class std_vector_hypercube:
    """
    Python interface for O\ :sub:`2`\ scl class ``std::vector<prob_dens_mdim_amr<>::hypercube>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/std::vector<prob_dens_mdim_amr<>::hypercube>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class std_vector_hypercube

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_std_vector_prob_dens_mdim_amr_hypercube_
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
        Delete function for class std_vector_hypercube
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_std_vector_prob_dens_mdim_amr_hypercube_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class std_vector_hypercube
        
        Returns: std_vector_hypercube object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def resize(self,n):
        """
        | Parameters:
        | *n*: ``size_t``
        """
        func=self._link.o2scl.o2scl_std_vector_prob_dens_mdim_amr_hypercube__resize
        func.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
        func(self._ptr,n)
        return

    def size(self):
        """
        | Returns: a Python int
        """
        func=self._link.o2scl.o2scl_std_vector_prob_dens_mdim_amr_hypercube__size
        func.restype=ctypes.c_size_t
        func.argtypes=[ctypes.c_void_p]
        ret=func(self._ptr)
        return ret


class prob_dens_mdim_amr:
    """
    Python interface for O\ :sub:`2`\ scl class ``prob_dens_mdim_amr<>``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/prob_dens_mdim_amr<>.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class prob_dens_mdim_amr

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_prob_dens_mdim_amr_
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
        Delete function for class prob_dens_mdim_amr
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_prob_dens_mdim_amr_
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class prob_dens_mdim_amr
        
        Returns: prob_dens_mdim_amr object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj


