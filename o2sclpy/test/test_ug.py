import o2sclpy
import numpy

def test_all():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    ug_end=o2sclpy.uniform_grid_end.init(link,1,5,4)
    v=[ug_end[i] for i in range(0,ug_end.get_npoints())]
    numpy.testing.assert_array_equal(v,[1,2,3,4,5],'uniform_grid')
    
    return
