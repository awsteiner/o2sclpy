import o2sclpy

def test_all():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    v=o2sclpy.std_vector(link)
    v.resize(5)
    v[0]=3.0
    v[1]=1.0
    v[2]=4.0
    v[3]=1.0
    v[4]=5.0
    v2=v.to_numpy()
    for i in range(0,5):
        assert v2[i]==v[i]
    
    s=o2sclpy.std_string(link)
    s.init_bytes(b'abcXe')
    s[0]=b'a'
    s[1]=b'b'
    s[2]=b'c'
    s[3]=b'X'
    s[4]=b'e'
    assert s.to_bytes()==b'abcXe'
