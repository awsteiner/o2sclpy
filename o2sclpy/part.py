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
    _pointer=0

    def __init__(self,link):

        op=link.o2scl_part
        
        double_ptr=ctypes.POINTER(ctypes.c_double)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        bool_ptr=ctypes.POINTER(ctypes.c_bool)
        bool_ptr_ptr=ctypes.POINTER(bool_ptr)
        self._g=double_ptr()
        self._m=double_ptr()
        self._ms=double_ptr()
        self._mu=double_ptr_ptr()
        self._nu=double_ptr()
        self._pr=double_ptr()
        self._ed=double_ptr()
        self._en=double_ptr()
        self._inc_rest_mass=bool_ptr()
        self._non_interacting=bool_ptr()
        
        f=op.o2scl_create_part
        f.restype=ctypes.c_void_p
        f.argtypes=[double_ptr_ptr,double_ptr_ptr,double_ptr_ptr,
                    double_ptr_ptr,double_ptr_ptr,
                    double_ptr_ptr,double_ptr_ptr,
                    double_ptr_ptr,bool_ptr_ptr,
                    bool_ptr_ptr]
        self._pointer=f(ctypes.byref(self._g),
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
        return self._g.contents

    @g.setter
    def g(self,value):
        self._g.contents=ctypes.c_double(value)
        return
    
    @property
    def m(self):
        return self._m.contents

    @m.setter
    def m(self,value):
        self._m.contents=ctypes.c_double(value)
        return

    @property
    def ms(self):
        return self._ms.contents

    @ms.setter
    def ms(self,value):
        self._ms.contents=ctypes.c_double(value)
        return

    @property
    def mu(self):
        return self._mu.contents

    @mu.setter
    def mu(self,value):
        print('mu setter:',value,type(self._mu))
        self._mu.contents=ctypes.c_double(value)
        return

    @property
    def nu(self):
        return self._nu.contents

    @nu.setter
    def nu(self,value):
        self._nu.contents=ctypes.c_double(value)
        return

    @property
    def ed(self):
        return self._ed.contents

    @ed.setter
    def ed(self,value):
        self._ed.contents=ctypes.c_double(value)
        return

    @property
    def pr(self):
        return self._pr.contents

    @pr.setter
    def pr(self,value):
        self._pr.contents=ctypes.c_double(value)
        return

    @property
    def en(self):
        return self._en.contents

    @en.setter
    def en(self,value):
        self._en.contents=ctypes.c_double(value)
        return

    @property
    def inc_rest_mass(self):
        return self._inc_rest_mass.contents

    @inc_rest_mass.setter
    def inc_rest_mass(self,value):
        self._inc_rest_mass.contents=ctypes.c_bool(value)
        return

    @property
    def non_interacting(self):
        return self._non_interacting.contents

    @non_interacting.setter
    def non_interacting(self,value):
        self._non_interacting.contents=ctypes.c_bool(value)
        return

    
class fermion(part):

    _kf=0
    _delta=0
    
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
        self._kf=double_ptr()
        self._delta=double_ptr()
        
        f=op.o2scl_create_fermion
        f.restype=ctypes.c_void_p
        f.argtypes=[double_ptr_ptr,double_ptr_ptr,double_ptr_ptr,
                    double_ptr_ptr,double_ptr_ptr,double_ptr_ptr,
                    double_ptr_ptr,double_ptr_ptr,bool_ptr_ptr,
                    bool_ptr_ptr,double_ptr_ptr,double_ptr_ptr]
        self._pointer=f(ctypes.byref(self._g),
                        ctypes.byref(self._m),
                        ctypes.byref(self._ms),
                        ctypes.byref(self._mu),
                        ctypes.byref(self._nu),
                        ctypes.byref(self._ed),
                        ctypes.byref(self._pr),
                        ctypes.byref(self._en),
                        ctypes.byref(self._inc_rest_mass),
                        ctypes.byref(self._non_interacting),
                        ctypes.byref(self._kf),
                        ctypes.byref(self._delta))
        print('ptrs:',self._pointer,type(self._mu),self._mu,self._mu.contents)
        return

    @property
    def kf(self):
        return self._kf.contents

    @kf.setter
    def kf(self,value):
        print('kf setter:',value,type(self._kf))
        self._kf.contents=ctypes.c_double(value)
        return

    @property
    def delta(self):
        return self._delta.contents

    @delta.setter
    def delta(self,value):
        self._delta.contents=ctypes.c_double(value)
        return
        
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
        self.fermion_rel_ptr=op.o2scl_create_fermion_rel()

        op.o2scl_create_fermion_nonrel.restype=ctypes.c_void_p
        op.o2scl_create_fermion_nonrel.argtypes=[]
        self.fermion_nonrel_ptr=op.o2scl_create_fermion_nonrel()

        op.o2scl_create_fermion_deriv_nr.restype=ctypes.c_void_p
        op.o2scl_create_fermion_deriv_nr.argtypes=[]
        self.fermion_deriv_nr_ptr=op.o2scl_create_fermion_deriv_nr()

        op.o2scl_create_fermion_deriv_rel.restype=ctypes.c_void_p
        op.o2scl_create_fermion_deriv_rel.argtypes=[]
        self.fermion_deriv_rel_ptr=op.o2scl_create_fermion_deriv_rel()

        op.o2scl_create_boson_rel.restype=ctypes.c_void_p
        op.o2scl_create_boson_rel.argtypes=[]
        self.boson_rel_ptr=op.o2scl_create_boson_rel()

        op.o2scl_create_classical_thermo.restype=ctypes.c_void_p
        op.o2scl_create_classical_thermo.argtypes=[]
        self.classical_thermo_ptr=op.o2scl_create_classical_thermo()

        op.o2scl_create_classical_deriv_thermo.restype=ctypes.c_void_p
        op.o2scl_create_classical_deriv_thermo.argtypes=[]
        self.classical_deriv_thermo_ptr=op.o2scl_create_classical_deriv_thermo()

        op.o2scl_create_fermion_mag_zerot.restype=ctypes.c_void_p
        op.o2scl_create_fermion_mag_zerot.argtypes=[]
        self.fermion_mag_zerot_ptr=op.o2scl_create_fermion_mag_zerot()

        return

    # void o2scl_fermion_rel_calc_density(void *frp, void *fp, double T);
    def calc_density(self,f,T,nonrel=False,derivs=False):
        """
        Properties of a fermion given the density
        """
    
        op=self.link.o2scl_part

        fx=op.o2scl_fermion_rel_calc_density
        fx.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_double]
        print('hex',f._mu.contents,f._m.contents)
        fx(self.fermion_rel_ptr,f._pointer,T)
        return
    
