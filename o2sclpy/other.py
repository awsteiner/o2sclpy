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
        
        Returns: a slack_messenger object
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

    def get_url(self,url):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_url
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,url._ptr)
        return

    def set_url(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_url
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_channel(self,channel):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_channel
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,channel._ptr)
        return

    def set_channel(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_channel
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_icon(self,icon):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_icon
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,icon._ptr)
        return

    def set_icon(self,value):
        """
        Set object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_set_icon
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,value._ptr)
        return

    def get_username(self,username):
        """
        Get object of type :class:`std::string`
        """
        func=self._link.o2scl.o2scl_slack_messenger_get_username
        func.restype=ctypes.c_char_p
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,username._ptr)
        return

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
        
        Returns: a quadratic_real_coeff_gsl object
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
        
        Returns: a quadratic_real_coeff_gsl2 object
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
        
        Returns: a cubic_real_coeff_cern object
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
        
        Returns: a cubic_real_coeff_gsl object
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
        
        Returns: a quartic_real_coeff_cern object
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
        
        Returns: a fermi_dirac_integ_gsl object
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
        
        Returns: a bessel_K_exp_integ_gsl object
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
        
        Returns: a hist object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def __deepcopy__(self,memo):
        """
        Deep copy function for class hist
        
        Returns: a new copy of the hist object
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


class fract:
    """
    Python interface for O\ :sub:`2`\ scl class ``fract``,
    See
    https://neutronstars.utk.edu/code/o2scl/html/class/fract.html .
    """

    _ptr=0
    _link=0
    _owner=True

    def __init__(self,link,pointer=0):
        """
        Init function for class fract

        | Parameters:
        | *link* :class:`linker` object
        | *pointer* ``ctypes.c_void_p`` pointer

        """

        if pointer==0:
            f=link.o2scl.o2scl_create_fract
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
        Delete function for class fract
        """

        if self._owner==True:
            f=self._link.o2scl.o2scl_free_fract
            f.argtypes=[ctypes.c_void_p]
            f(self._ptr)
            self._owner=False
            self._ptr=0
        return

    def __copy__(self):
        """
        Shallow copy function for class fract
        
        Returns: a fract object
        """

        new_obj=type(self)(self._link,self._ptr)
        return new_obj

    def nrf_z4m1(self,gx,gy,kmax,rmax,t3d,roots_x,roots_y,min,max):
        """
        | Parameters:
        | *gx*: :class:`uniform_grid<>` object
        | *gy*: :class:`uniform_grid<>` object
        | *kmax*: ``size_t``
        | *rmax*: ``double``
        | *t3d*: :class:`o2scl::table3d` object
        | *roots_x*: :class:`std_vector` object
        | *roots_y*: :class:`std_vector` object
        | *min*: :class:`std_vector` object
        | *max*: :class:`std_vector` object
        """
        func=self._link.o2scl.o2scl_fract_nrf_z4m1
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        func(self._ptr,gx._ptr,gy._ptr,kmax,rmax,t3d._ptr,roots_x._ptr,roots_y._ptr,min._ptr,max._ptr)
        return

    def itf_mandel(self,gx,gy,kmax,rmax,t3d,min,max):
        """
        | Parameters:
        | *gx*: :class:`uniform_grid<>` object
        | *gy*: :class:`uniform_grid<>` object
        | *kmax*: ``size_t``
        | *rmax*: ``double``
        | *t3d*: :class:`o2scl::table3d` object
        | *min*: ``ctypes.c_size_t``
        | *max*: ``ctypes.c_size_t``
        | Returns: a Python int, a Python int, a Python int
        """
        func=self._link.o2scl.o2scl_fract_itf_mandel
        func.restype=ctypes.c_int
        func.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_double,ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
        min_conv=ctypes.c_size_t(min)
        max_conv=ctypes.c_size_t(max)
        ret=func(self._ptr,gx._ptr,gy._ptr,kmax,rmax,t3d._ptr,ctypes.byref(min_conv),ctypes.byref(max_conv))
        return ret,min_conv.value,max_conv.value


