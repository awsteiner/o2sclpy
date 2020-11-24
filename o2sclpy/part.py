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

class part:

    _g=0
    _m=0
    _ms=0
    _mu=0
    _nu=0
    _ed=0
    _pr=0
    _en=0
    _non_interacting=0
    _inc_rest_mass=0
    pointer=0

    def __init__(self,link):

        op=link.o2scl_part
        
        double_ptr=ctypes.POINTER(ctypes.c_double)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        bool_ptr=ctypes.POINTER(ctypes.c_bool)
        bool_ptr_ptr=ctypes.POINTER(bool_ptr)
        self._g=double_ptr()
        self._m=double_ptr()
        self._ms=double_ptr()
        self._mu=double_ptr()
        self._nu=double_ptr()
        self._pr=double_ptr()
        self._ed=double_ptr()
        self._en=double_ptr()
        self._inc_rest_mass=bool_ptr()
        self._non_interacting=bool_ptr()
        
        op.o2scl_create_part.restype=ctypes.c_void_p
        op.o2scl_create_part.argtypes=[double_ptr_ptr,
                                       double_ptr_ptr,double_ptr_ptr,
                                       double_ptr_ptr,double_ptr_ptr,
                                       double_ptr_ptr,double_ptr_ptr,
                                       double_ptr_ptr,bool_ptr_ptr,
                                       bool_ptr_ptr]
        self.part_ptr=op.o2scl_create_part(ctypes.byref(self._g),
                                           ctypes.byref(self._m),
                                           ctypes.byref(self._ms),
                                           ctypes.byref(self._mu),
                                           ctypes.byref(self._nu),
                                           ctypes.byref(self._ed),
                                           ctypes.byref(self._pr),
                                           ctypes.byref(self._en),
                                           ctypes.byref(self._inc_rest_mass),
                                           ctypes.byref(self._non_interacting))
        return
    
    @property
    def g(self):
        return self._g.value

    @g.setter
    def g(self,value):
        self._g.value=value
        return
    
    @property
    def m(self):
        return self._m.value

    @m.setter
    def m(self.value):
        self._m.value=value
        return

    @property
    def ms(self):
        return self._ms.value

    @ms.setter
    def ms(self.value):
        self._ms.value=value
        return

    @property
    def mu(self):
        return self._mu.value

    @mu.setter
    def mu(self.value):
        self._mu.value=value
        return

    @property
    def nu(self):
        return self._nu.value

    @nu.setter
    def nu(self.value):
        self._nu.value=value
        return

    @property
    def ed(self):
        return self._ed.value

    @ed.setter
    def ed(self.value):
        self._ed.value=value
        return

    @property
    def pr(self):
        return self._pr.value

    @pr.setter
    def pr(self.value):
        self._pr.value=value
        return

    @property
    def en(self):
        return self._en.value

    @en.setter
    def en(self.value):
        self._en.value=value
        return

    @property
    def inc_rest_mass(self):
        return self._inc_rest_mass.value

    @inc_rest_mass.setter
    def inc_rest_mass(self.value):
        self._inc_rest_mass.value=value
        return

    @property
    def non_interacting(self):
        return self._non_interacting.value

    @non_interacting.setter
    def non_interacting(self.value):
        self._non_interacting.value=value
        return

    
class fermion(part):

    @property
    def kf(self):
        op.o2scl_get_part_kf.restyspe=ctypes.c_double
        op.o2scl_get_part_kf.argtypes=[ctypes.c_void_p]
        return op.o2scl_get_part_kf(self.part_ptr)
    
    @property
    def delta(self):
        op.o2scl_get_part_del.restyspe=ctypes.c_double
        op.o2scl_get_part_del.argtypes=[ctypes.c_void_p]
        return op.o2scl_get_part_del(self.part_ptr)
    
    def __init__(self):

        op.o2scl_create_fermion.restype=ctypes.c_void_p
        op.o2scl_create_fermion.argtypes=[]
        self.fermion_ptr=ctypes.c_void_p()
        self.fermion_ptr=op.o2scl_create_fermion()
        
class fermion_thermo:
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

    def fermion_density(self,m,g,T,n,nonrel=False,derivs=False):
        """
        Properties of a fermion given the density
        """
    
        op=self.link.o2scl_part

        if derivs:
            print('here')
        
        if nonrel:
        
            # Non-relativistic version without derivatives

            double_ptr=ctypes.POINTER(ctypes.c_double)
            op.o2scl_fermion_nonrel_density.argtypes=[ctypes.c_void_p,
                                                      ctypes.c_double,
                                                      ctypes.c_double,
                                                      ctypes.c_double,
                                                      ctypes.c_double,
                                                      double_ptr,
                                                      double_ptr,
                                                      double_ptr,
                                                      double_ptr]
            
            mu=ctypes.c_double(0)
            ed=ctypes.c_double(0)
            pr=ctypes.c_double(0)
            en=ctypes.c_double(0)
    
            op.o2scl_fermion_nonrel_density(self.fermion_rel_ptr,m,g,T,n,
                                            ctypes.byref(mu),ctypes.byref(ed),
                                            ctypes.byref(pr),ctypes.byref(en))
            
            return (mu.value,ed.value,pr.value,en.value)

        # Relativistic version without derivatives
        
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
    
    def fermion_mu(self,m,g,T,n,nonrel=False,derivs=False):
        """
        Properties of a fermion given the chemical potential
        """

        op=self.link.o2scl_part

        if derivs:

            # Relativistic version with derivatives
            double_ptr=ctypes.POINTER(ctypes.c_double)
            op.o2scl_fermion_deriv_mu.argtypes=[ctypes.c_void_p,
                                                ctypes.c_double,
                                                ctypes.c_double,
                                                ctypes.c_double,
                                                ctypes.c_double,
                                                double_ptr,
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
        
        # Relativistic version without derivatives
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
    
