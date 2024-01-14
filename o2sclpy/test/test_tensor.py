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

def def_tensor(link):
    tensor=o2sclpy.tensor(link)
    tensor.resize([2,3,4])
    for i in range(0,2):
        for j in range(0,3):
            for k in range(0,4):
                temp_list=[i,j,k]
                tensor.set(temp_list,i+j+k)
    return tensor

def subtest_basic(link):

    tensor=def_tensor(link)
    assert tensor.get_rank()==3,'get_rank()'
    assert tensor.get_size(1)==3,'get_size()'
    assert tensor.get([1,2,0])==3,'get()'
    tensor.set([1,2,0],4)
    assert tensor.get([1,2,0])==4,'get() 2'
    assert tensor.total_size()==24,'total_size()'
    tensor2=o2sclpy.rearrange_and_copy(link,tensor,
                                       'index(0),index(1),fixed(2,2)')
    assert tensor2.total_size()==6,'total_size() after rearrange'
    assert tensor.min_value()==0
    assert tensor.max_value()==6
    
    return

def subtest_copying(link):
    
    ten1=def_tensor(link)
    ten1.set([1,2,0],4)
    ten2=copy.copy(ten1)
    assert ten2.get([1,2,0])==4,'Check the shallow copy'
    
    ten3=copy.deepcopy(ten1)
    ten2.set([1,2,0],5)
    assert ten1.get([1,2,0])==5,'Show changes in the second impact the first'
    assert ten3.get([1,2,0])==4,'Show deep copy works'
    return

def subtest_hdf5(link,tmp_path):
    
    p=tmp_path/"tensor.o2"
    filename=bytes(str(p),'utf-8')
    
    ten1=def_tensor(link)

    # Write ten1 to a file
    hf=o2sclpy.hdf_file(link)
    hf.open_or_create(filename)
    hf.setd_ten(b'tensor',ten1)
    hf.close()

    # Open the file and read into ten2
    hf.open(filename,False,True)
    name=o2sclpy.std_string(link)
    ten2=o2sclpy.tensor(link)
    hf.getd_ten(b'tensor',ten2)
    hf.close()

    sz1=ten1.get_size_arr()
    sz2=ten2.get_size_arr()
    assert len(sz1)==len(sz2),"copy after hdf_input() 1"
    assert sz1[0]==sz2[0],"copy after hdf_input() 2" 
    assert sz1[1]==sz2[1],"copy after hdf_input() 3"
    assert sz1[2]==sz2[2],"copy after hdf_input() 4"
    
    return

def test_all(tmp_path):
    link=o2sclpy.linker()
    link.link_o2scl()

    subtest_basic(link)
    subtest_copying(link)
    subtest_hdf5(link,tmp_path)
    return
        
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
