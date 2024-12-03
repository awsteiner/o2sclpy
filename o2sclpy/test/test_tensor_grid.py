#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023-2025, Andrew W. Steiner
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
import math

def f(x,y,z):
    return (math.sin(x)+math.sin(2*y))*math.exp(-z*z)

def def_tensor_grid():
    tg=o2sclpy.tensor_grid()
    tg.resize([21,21,21])
    lst2=o2sclpy.std_vector()
    lst3=[]
    for i in range(0,21):
        lst3.append(i*0.1-1.0)
    for i in range(0,21):
        lst3.append(i*0.1)
    for i in range(0,21):
        lst3.append(i*0.1+1.0)
    lst2.from_list(lst3)
    tg.set_grid_packed(lst2)
    for i in range(0,21):
        for j in range(0,21):
            for k in range(0,21):
                temp_list=[i,j,k]
                x=tg.get_grid(0,i)
                y=tg.get_grid(1,j)
                z=tg.get_grid(2,k)
                tg.set(temp_list,f(x,y,z))
    return tg

def subtest_basic():

    tg=def_tensor_grid()
    assert tg.get_rank()==3,'get_rank()'
    assert tg.get_size(1)==21,'get_size()'
    assert tg.total_size()==9261,'total_size()'
    assert tg.is_grid_set()==True,'is_grid_set()'
    
    return

def subtest_interp():

    tg=def_tensor_grid()

    sv=o2sclpy.std_vector()
    sv.from_list([0.12,0.56,1.34])
    assert numpy.allclose(tg.interp_linear(sv),
                          f(sv[0],sv[1],sv[2]),4.0e-3),'interp_linear'
    
    return

def subtest_rearrange():

    tg=def_tensor_grid()

    tg2=o2sclpy.grid_rearrange_and_copy(tg,
                                        'index(0),index(1),fixed(2,2)')
    assert str(type(tg2))=="<class 'o2sclpy.base.tensor_grid'>",'type'
    assert tg2.total_size()==441,'total_size() after rearrange'
    
    return

def subtest_copy_table3d():
    
    tg=def_tensor_grid()
    
    sv=o2sclpy.std_vector_size_t()
    sv.resize(3)
    sv[1]=5
    t3d=o2sclpy.table3d()
    tg.copy_table3d_align(0,2,sv,t3d)
    
    return

def subtest_hdf5(tmp_path):
    
    p=tmp_path/"tensor_grid.o2"
    filename=bytes(str(p),'utf-8')
    
    ten1=def_tensor_grid()

    # Write ten1 to a file
    hf=o2sclpy.hdf_file()
    hf.open_or_create(filename)
    o2sclpy.hdf_output_tensor_grid(hf,ten1,b'tensor_grid')
    hf.close()

    # Open the file and read into ten2
    hf.open(filename,False,True)
    name=o2sclpy.std_string()
    ten2=o2sclpy.tensor_grid()
    o2sclpy.hdf_input_tensor_grid(hf,ten2,b'tensor_grid')
    hf.close()

    sz1=ten1.get_size_arr()
    sz2=ten2.get_size_arr()
    assert len(sz1)==len(sz2),"copy after hdf_input() 1"
    assert sz1[0]==sz2[0],"copy after hdf_input() 2"
    assert sz1[1]==sz2[1],"copy after hdf_input() 3"
    assert sz1[2]==sz2[2],"copy after hdf_input() 4"
    
    return

def subtest_copying():
    
    ten1=def_tensor_grid()
    ten1.set([1,2,0],4)
    ten2=copy.copy(ten1)
    assert ten2.get([1,2,0])==4,'Check the shallow copy'
    
    ten3=copy.deepcopy(ten1)
    ten2.set([1,2,0],5)
    assert ten1.get([1,2,0])==5,'Show changes in the second impact the first'
    assert ten3.get([1,2,0])==4,'Show deep copy works'
    
    return

def test_all(tmp_path):
    subtest_basic()
    subtest_copying()
    subtest_copy_table3d()
    subtest_interp()
    subtest_rearrange()
    subtest_hdf5(tmp_path)
    return
        
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
