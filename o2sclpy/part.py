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

from o2sclpy.link_o2scl import o2scl

def init_part_pointers(o2scl_part):
    if o2scl_part==0:
        print('O2scl particle library not loaded.')
        return 0

    print('here',o2scl)
    
    print('Creating pointer to fermion_rel.')
    o2scl_part.o2scl_create_fermion_rel.restype=ctypes.c_void_p
    o2scl_part.o2scl_create_fermion_rel.argtypes=[]
    fermion_rel_ptr=ctypes.c_void_p()
    fermion_rel_ptr=o2scl_part.o2scl_create_fermion_rel()
    
    return fermion_rel_ptr


