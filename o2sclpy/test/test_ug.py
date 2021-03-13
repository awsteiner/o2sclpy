import o2sclpy
import numpy

def test_all():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    ug_end=o2sclpy.uniform_grid_end.init(link,1,5,4)
    v=[ug_end[i] for i in range(0,ug_end.get_npoints())]
    numpy.testing.assert_array_equal(v,[1,2,3,4,5],'getitem')
    assert ug_end.get_npoints()==5,'get_npoints()'
    assert ug_end.get_end()==5.0,'get_end()'

    v2=o2sclpy.std_vector(link)
    ug_end.vector(v2)
    assert len(v2)==5,'vector()+len()'
    numpy.testing.assert_array_equal(v2.to_numpy(),[1,2,3,4,5],'vector()')

    # Write to a file
    hf=o2sclpy.hdf_file(link)
    hf.open_or_create(b'temp.o2')
    o2sclpy.hdf_output_uniform_grid(link,hf,ug_end,b'ug_end')
    hf.close()

    # Open the file and read into tab2
    hf.open(b'temp.o2',False,True)
    name=o2sclpy.std_string(link)
    ug=o2sclpy.uniform_grid(link)
    o2sclpy.hdf_input_n_uniform_grid(link,hf,ug,name)
    hf.close()
    assert name.to_bytes()==b'ug_end','name after hdf_input()'
    assert ug_end.get_end()==ug.get_end(),'get_end() after hdf_input()'
    
    return
