import o2sclpy
import numpy

def subtest_std_string(link):
    # Test the std_string class
    s=o2sclpy.std_string(link)
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

def subtest_std_vector(link):
    # Test the std_vector class
    v=o2sclpy.std_vector(link)
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

def subtest_std_vector_int(link):
    # Test the std_vector_int class
    v=o2sclpy.std_vector_int(link)
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

def subtest_std_vector_size_t(link):
    # Test the std_vector_size_t class
    v=o2sclpy.std_vector_size_t(link)
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

def subtest_std_vector_string(link):
    # Test the std_vector_string class
    v=o2sclpy.std_vector_string(link)
    v.resize(5)
    v[0]=b'abc'
    v[1]=b'def'
    v[2]=b'ghi'
    v[3]=b'jkl'
    v[4]=b'mno'
    # Test shallow copy
    v3=v
    v3[0]=b'pqr'
    assert v[0]==b'pqr','getitem and shallow copy'
    assert v3.size()==5,'size()'
    assert len(v3)==5,'len()'

    return

def subtest_ublas_vector(link):
    # Test the ublas_vector class
    v=o2sclpy.ublas_vector(link)
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

def subtest_ublas_matrix(link):
    # Test the ublas_matrix class
    v=o2sclpy.ublas_matrix(link)
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

def subtest_ublas_matrix_int(link):
    # Test the ublas_matrix class
    v=o2sclpy.ublas_matrix(link)
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

def subtest_std_vector_vector(link):
    # Test the std_complex class
    vv=o2sclpy.std_vector_vector(link)
    vv.resize(3)
    assert vv.size()==3,'vv size'
    vv[0]=[1,2,3]
    vv[1]=[3,4]
    vv[2]=[4,5,6,7]
    assert numpy.allclose(vv[2][3],7,1.0e-14),'vv'
    return
    
def subtest_std_complex(link):
    # Test the std_complex class
    c=o2sclpy.std_complex(link)
    c.real_set(2)
    c.imag_set(3)
    assert numpy.allclose(c.real(),2,rtol=1.0e-12),'c real'
    assert numpy.allclose(c.imag(),3,rtol=1.0e-12),'c imag'
    c2=c.to_python()
    assert numpy.allclose(c2.real,2,rtol=1.0e-12),'c2 real'
    assert numpy.allclose(c2.imag,3,rtol=1.0e-12),'c2 imag'
    return
    

def test_all():
    link=o2sclpy.linker()
    link.link_o2scl()

    subtest_std_string(link)
    subtest_std_vector(link)
    subtest_std_vector_int(link)
    subtest_std_vector_size_t(link)
    subtest_std_vector_string(link)
    subtest_ublas_vector(link)
    subtest_ublas_matrix(link)
    subtest_ublas_matrix_int(link)
    subtest_std_vector_vector(link)
    subtest_std_complex(link)

    return
    
    
