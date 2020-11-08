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

class part_class:
    """
    Non-interacting particle thermodynamics
    """

    link=0
    fermion_rel_ptr=0
    fermion_nonrel_ptr=0
    fermion_deriv_nr_ptr=0
    fermion_deriv_rel_ptr=0
    boson_rel_ptr=0
    fermion_mag_zerot_ptr=0
    classical_thermo_ptr=0
    classical_deriv_thermo_ptr=0
    
    def __init__(self,link):
        """
        Initialize all of the pointers to the o2scl
        thermo objects
        """

        self.link=link
        op=link.o2scl_part
        
        op.o2scl_create_fermion_rel.restype=ctypes.c_void_p
        op.o2scl_create_fermion_rel.argtypes=[]
        self.fermion_rel_ptr=ctypes.c_void_p()
        self.fermion_rel_ptr=op.o2scl_create_fermion_rel()

        op.o2scl_create_fermion_nonrel.restype=ctypes.c_void_p
        op.o2scl_create_fermion_nonrel.argtypes=[]
        self.fermion_nonrel_ptr=ctypes.c_void_p()
        self.fermion_nonrel_ptr=op.o2scl_create_fermion_nonrel()

        op.o2scl_create_fermion_deriv_nr.restype=ctypes.c_void_p
        op.o2scl_create_fermion_deriv_nr.argtypes=[]
        self.fermion_deriv_nr_ptr=ctypes.c_void_p()
        self.fermion_deriv_nr_ptr=op.o2scl_create_fermion_deriv_nr()

        op.o2scl_create_fermion_deriv_rel.restype=ctypes.c_void_p
        op.o2scl_create_fermion_deriv_rel.argtypes=[]
        self.fermion_deriv_rel_ptr=ctypes.c_void_p()
        self.fermion_deriv_rel_ptr=op.o2scl_create_fermion_deriv_rel()

        op.o2scl_create_boson_rel.restype=ctypes.c_void_p
        op.o2scl_create_boson_rel.argtypes=[]
        self.boson_rel_ptr=ctypes.c_void_p()
        self.boson_rel_ptr=op.o2scl_create_boson_rel()

        op.o2scl_create_classical_thermo.restype=ctypes.c_void_p
        op.o2scl_create_classical_thermo.argtypes=[]
        self.classical_thermo_ptr=ctypes.c_void_p()
        self.classical_thermo_ptr=op.o2scl_create_classical_thermo()

        op.o2scl_create_classical_deriv_thermo.restype=ctypes.c_void_p
        op.o2scl_create_classical_deriv_thermo.argtypes=[]
        self.classical_deriv_thermo_ptr=ctypes.c_void_p()
        self.classical_deriv_thermo_ptr=op.o2scl_create_classical_deriv_thermo()

        op.o2scl_create_fermion_mag_zerot.restype=ctypes.c_void_p
        op.o2scl_create_fermion_mag_zerot.argtypes=[]
        self.fermion_mag_zerot_ptr=ctypes.c_void_p()
        self.fermion_mag_zerot_ptr=op.o2scl_create_fermion_mag_zerot()

        return

    def fermion_density(self,m,g,T,n):
        """
        Properties of a fermion given the density
        """
    
        op=self.link.o2scl_part
        
        double_ptr=ctypes.POINTER(ctypes.c_double)
        op.o2scl_fermion_density.argtypes=[ctypes.c_void_p,ctypes.c_double,
                                           ctypes.c_double,ctypes.c_double,
                                           ctypes.c_double,double_ptr,
                                           double_ptr,double_ptr,
                                           double_ptr]
        mu=ctypes.c_double(0)
        ed=ctypes.c_double(0)
        pr=ctypes.c_double(0)
        en=ctypes.c_double(0)
        
        op.o2scl_fermion_density(self.fermion_rel_ptr,m,g,T,n,
                                 ctypes.byref(mu),ctypes.byref(ed),
                                 ctypes.byref(pr),ctypes.byref(en))
        
        return (mu.value,ed.value,pr.value,en.value)
    
    def fermion_mu(self,m,g,T,n):
        """
        Properties of a fermion given the chemical potential
        """
    
        op=self.link.o2scl_part
        
        double_ptr=ctypes.POINTER(ctypes.c_double)
        op.o2scl_fermion_mu.argtypes=[ctypes.c_void_p,ctypes.c_double,
                                      ctypes.c_double,ctypes.c_double,
                                      ctypes.c_double,double_ptr,
                                      double_ptr,double_ptr,
                                      double_ptr]
        n=ctypes.c_double(0)
        ed=ctypes.c_double(0)
        pr=ctypes.c_double(0)
        en=ctypes.c_double(0)
        
        op.o2scl_fermion_mu(self.fermion_rel_ptr,m,g,T,mu,
                            ctypes.byref(n),ctypes.byref(ed),
                            ctypes.byref(pr),ctypes.byref(en))
        
        return (n.value,ed.value,pr.value,en.value)
    
    def fermion_deriv_mu(self,m,g,T,mu):
        """
        Properties of a fermion given the chemical potential
        """
    
        op=self.link.o2scl_part
        
        double_ptr=ctypes.POINTER(ctypes.c_double)
        op.o2scl_fermion_deriv_mu.argtypes=[ctypes.c_void_p,ctypes.c_double,
                                            ctypes.c_double,ctypes.c_double,
                                            ctypes.c_double,double_ptr,
                                            double_ptr,double_ptr,
                                            double_ptr,double_ptr,
                                            double_ptr,double_ptr]
        n=ctypes.c_double(0)
        ed=ctypes.c_double(0)
        pr=ctypes.c_double(0)
        en=ctypes.c_double(0)
        dndT=ctypes.c_double(0)
        dsdT=ctypes.c_double(0)
        dndmu=ctypes.c_double(0)
        
        op.o2scl_fermion_deriv_mu(self.fermion_deriv_rel_ptr,m,g,T,mu,
                                  ctypes.byref(n),ctypes.byref(ed),
                                  ctypes.byref(pr),ctypes.byref(en),
                                  ctypes.byref(dndT),ctypes.byref(dsdT),
                                  ctypes.byref(dndmu))
        
        return (n.value,ed.value,pr.value,en.value,dndT.value,
                dsdT.value,dndmu.value)
    
