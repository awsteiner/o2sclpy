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
import numpy

def subtest_std_string():
    # Test the std_string class
    s=o2sclpy.std_string()
    s.init_bytes(b'abcXe')
    s[0]=b'a'
    s[1]=b'b'
    s[2]=b'c'
    s[3]=b'X'
    s[4]=b'e'
    assert s.to_bytes()==b'abcXe','init_bytes(), set_item(), to_bytes()'
    assert s[4]==b'e','getitem'
    assert s.length()==5,'length()'
    s.resize(2)
    s[0]=b'a'
    s[1]=b'b'
    assert s.to_bytes()==b'ab','resize and to_bytes()'
    assert len(s)==2,'len()'
    s2=s
    s2[0]=b'b'
    assert s.to_bytes()==b'bb','shallow copy and to_bytes()'
    return

def subtest_std_vector():
    # Test the std_vector class
    v=o2sclpy.std_vector()
    v.resize(5)
    v[0]=3.0
    v[1]=1.0
    v[2]=4.0
    v[3]=1.0
    v[4]=5.0
    v2=v.to_numpy()
    for i in range(0,5):
        assert v2[i]==v[i],'resize(), setitem(), to_numpy()'
    v3=v
    v3[0]=1.0
    assert v[0]==1.0,'getitem and shallow copy'
    assert v3.size()==5,'size()'
    assert len(v3)==5,'len()'
    
    return

def subtest_std_vector_int():
    # Test the std_vector_int class
    v=o2sclpy.std_vector_int()
    v.resize(5)
    v[0]=3
    v[1]=1
    v[2]=4
    v[3]=1
    v[4]=5
    v2=v.to_numpy()
    for i in range(0,5):
        assert v2[i]==v[i],'resize(), setitem(), to_numpy()'
    v3=v
    v3[0]=1
    assert v[0]==1,'getitem and shallow copy'
    assert v3.size()==5,'size()'
    assert len(v3)==5,'len()'

    return

def subtest_std_vector_size_t():
    # Test the std_vector_size_t class
    v=o2sclpy.std_vector_size_t()
    v.resize(5)
    v[0]=3
    v[1]=1
    v[2]=4
    v[3]=1
    v[4]=5
    v2=v.to_numpy()
    for i in range(0,5):
        assert v2[i]==v[i],'resize(), setitem(), to_numpy()'
    v3=v
    v3[0]=1
    assert v[0]==1,'getitem and shallow copy'
    assert v3.size()==5,'size()'
    assert len(v3)==5,'len()'

    return

def subtest_std_vector_string():
    # Test the std_vector_string class
    v=o2sclpy.std_vector_string()
    v.resize(5)
    v[0]=b'abc'
    v[1]=b'def'
    v[2]=b'ghi'
    v[3]=b'jkl'
    v[4]=b'mno'
    # test set_list()
    v2=o2sclpy.std_vector_string()
    v2.set_list(['abc','def','ghi','jkl','mno'])
    for i in range(0,len(v)):
        assert v[i]==v2[i],'set item'
    # Test shallow copy
    v3=v
    v3[0]=b'pqr'
    assert v[0]==b'pqr','getitem and shallow copy'
    assert v3.size()==5,'size()'
    assert len(v3)==5,'len()'

    return

def subtest_ublas_vector():
    # Test the ublas_vector class
    v=o2sclpy.ublas_vector()
    v.resize(5)
    v[0]=3.0
    v[1]=1.0
    v[2]=4.0
    v[3]=1.0
    v[4]=5.0
    v2=v.to_numpy()
    for i in range(0,5):
        assert v2[i]==v[i],'resize(), setitem(), to_numpy()'
    v3=v
    v3[0]=1.0
    assert v[0]==1.0,'getitem and shallow copy'
    assert v3.size()==5,'size()'
    assert len(v3)==5,'len()'
    
    return

def subtest_ublas_vector_int():
    # Test the ublas_vector class
    v=o2sclpy.ublas_vector_int()
    v.resize(5)
    v[0]=3
    v[1]=1
    v[2]=4
    v[3]=1
    v[4]=5
    v2=v.to_numpy()
    for i in range(0,5):
        assert v2[i]==v[i],'resize(), setitem(), to_numpy()'
    v3=v
    v3[0]=1
    assert v[0]==1,'getitem and shallow copy'
    assert v3.size()==5,'size()'
    assert len(v3)==5,'len()'
    
    return

def subtest_ublas_matrix():
    # Test the ublas_matrix class
    v=o2sclpy.ublas_matrix()
    v.resize(2,3)
    v[0,0]=3.0
    v[0,1]=1.0
    v[0,2]=4.0
    v[1,0]=1.0
    v[1,1]=5.0
    v[1,2]=9.0
    v2=v.to_numpy()
    assert v2.shape==(v.size1(),v.size2())
    for i in range(0,2):
        for j in range(0,3):
            assert v2[i,j]==v[i,j],'resize(), setitem(), to_numpy()'
    v3=v
    v3[0,0]=1.0
    assert v[0,0]==1.0,'getitem and shallow copy'
    assert v3.size1()==2,'size1()'
    assert v3.size2()==3,'size2()'
    
    return

def subtest_ublas_matrix_int():
    # Test the ublas_matrix class
    v=o2sclpy.ublas_matrix()
    v.resize(2,3)
    v[0,0]=3
    v[0,1]=1
    v[0,2]=4
    v[1,0]=1
    v[1,1]=5
    v[1,2]=9
    v2=v.to_numpy()
    assert v2.shape==(v.size1(),v.size2())
    for i in range(0,2):
        for j in range(0,3):
            assert v2[i,j]==v[i,j],'resize(), setitem(), to_numpy()'
    v3=v
    v3[0,0]=1
    assert v[0,0]==1,'getitem and shallow copy'
    assert v3.size1()==2,'size1()'
    assert v3.size2()==3,'size2()'
    
    return

def subtest_std_vector_vector():
    # Test the std_complex class
    vv=o2sclpy.std_vector_vector()
    vv.resize(3)
    assert vv.size()==3,'vv size'
    vv[0]=[1,2,3]
    vv[1]=[3,4]
    vv[2]=[4,5,6,7]
    assert numpy.allclose(vv[2][3],7,1.0e-14),'vv'
    return
    
def subtest_vec_vec_string():
    # Test the std_complex class
    vv=o2sclpy.vec_vec_string()
    vv.resize(3)
    assert vv.size()==3,'vv size'
    v=o2sclpy.std_vector_string()
    v.set_list(['this','is','a'])
    vv[0]=v
    v.set_list(['test','of'])
    vv[1]=v
    v.set_list(['the','emergency','broadcasting','system.'])
    vv[2]=v
    assert vv[2][3]==b'system.','vvs'
    return
    
def subtest_std_complex():
    # Test the std_complex class
    c=o2sclpy.std_complex()
    c.real_set(2)
    c.imag_set(3)
    assert numpy.allclose(c.real(),2,rtol=1.0e-12),'c real'
    assert numpy.allclose(c.imag(),3,rtol=1.0e-12),'c imag'
    c2=c.to_python()
    assert numpy.allclose(c2.real,2,rtol=1.0e-12),'c2 real'
    assert numpy.allclose(c2.imag,3,rtol=1.0e-12),'c2 imag'
    return
    

def test_all():
    subtest_std_string()
    subtest_std_vector()
    subtest_std_vector_int()
    subtest_std_vector_size_t()
    subtest_std_vector_string()
    subtest_ublas_vector()
    subtest_ublas_vector_int()
    subtest_ublas_matrix()
    subtest_ublas_matrix_int()
    subtest_std_vector_vector()
    subtest_vec_vec_string()
    subtest_std_complex()

    return
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
