#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023-2024, Andrew W. Steiner
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
#
import o2sclpy
import copy
import numpy
import ctypes

def def_table3d():
    t3d=o2sclpy.table3d()
    ug_x=o2sclpy.uniform_grid_end_width.init(1,10,1)
    ug_y=o2sclpy.uniform_grid_end.init(1,6,12)
    t3d.set_xy_grid('x',ug_x,'y',ug_y)
    t3d.function_slice('(x-5)^2+(y-3)^2','z')
    return t3d

def subtest_basic():

    t3d=def_table3d()
    z=t3d.get_slice('z')
    assert z.to_numpy().shape==(z.size1(),z.size2()),'get_slice,etc.'
    xtmp=t3d.get_grid_x(5)
    ytmp=t3d.get_grid_y(5)
    ztmp=t3d.get(5,5,'z')
    assert (xtmp-5)**2+(ytmp-3)**2==ztmp,'get'
    assert t3d.get_nx()==10,'get_nx()'
    assert t3d.get_ny()==13,'get_ny()'
    assert t3d.get_size()==(10,13),'get_size()'
    # Make sure summary() works
    t3d.summary()
    return

def subtest_hdf5(tmp_path):
    
    p=tmp_path/"table3d.o2"
    filename=bytes(str(p),'utf-8')
    
    t3d1=def_table3d()

    # Write t3d1 to a file
    hf=o2sclpy.hdf_file()
    hf.open_or_create(filename)
    o2sclpy.hdf_output_table3d(hf,t3d1,b'table3d')
    hf.close()

    # Open the file and read into t3d2
    hf.open(filename,False,True)
    name=o2sclpy.std_string()
    t3d2=o2sclpy.table3d()
    o2sclpy.hdf_input_n_table3d(hf,t3d2,name)
    hf.close()
    assert name.to_bytes()==b'table3d','name after hdf_input()'
    assert t3d2.get_nx()==t3d1.get_nx(),"nlines after hdf_input()"
    return

def test_all(tmp_path):

    subtest_basic()
    subtest_hdf5(tmp_path)
    return
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
    
