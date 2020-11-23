#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2020, Andrew W. Steiner
#  
#  This file is part of O2sclpy.
#  
#  O2sclpy is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  O2sclpy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with O2sclpy. If not, see <http://www.gnu.org/licenses/>.
#  
#  -------------------------------------------------------------------
import ctypes

from o2sclpy.link_o2scl import linker

class hadronic_eos:
    """
    Non-interacting particle thermodynamics
    """

    link=0
    eos_had_base_ptr=0
    
    def __init__(self,link):
        """
        Initialize all of the pointers to the o2scl
        thermo objects
        """

        self.link=link
        oe=link.o2scl_eos

        return

    def select_model(self,eos_type,name):
        """
        Properties of a fermion given the density
        """

        if oe!=0:
            oe.o2scl_create_eos_had_base.argtypes=[ctypes.c_void_p]
            vp=ctypes.c_void_p(self.eos_had_base_ptr)
            oe.o2scl_free_eos_had_base(vp)
        return

        ceos_type=ctypes.c_char_p(force_bytes(eos_type))
        cname=ctypes.c_char_p(force_bytes(name))
        
        oe.o2scl_eos_had_strings.restype=ctypes.c_void_p
        oe.o2scl_create_eos_had_base.argtypes=[ctypes.c_char_p,
                                               ctypes.c_char_p]    
        self.eos_had_base_ptr=oe.o2scl_free_eos_had_base(ceos_type,cname)

        return
    
    def calc_density(self,nn,np,T=0):

        oe.o2scl_eos_had_calc_density_zerot.argtypes=
        [ctypes.c_double,ctypes.c_double,
         ctypes.c_double_p,ctypes.c_double_p,
         ctypes.c_double_p,ctypes.c_double_p]

        ed=POINTER(ctypes.c_double)()
        pr=POINTER(ctypes.c_double)()
        mun=POINTER(ctypes.c_double)()
        mup=POINTER(ctypes.c_double)()
        oe.o2scl_eos_had_calc_density_zerot(nn,np,ed,pr,mun,mup)
        
        return (ed,pr,mun,mup)
    
