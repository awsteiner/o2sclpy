import o2sclpy

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

def test():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    subtest_std_string(link)
    subtest_std_vector(link)
    subtest_std_vector_int(link)
    subtest_std_vector_size_t(link)
    subtest_ublas_vector(link)

    return
    
    
