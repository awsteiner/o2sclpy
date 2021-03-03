import o2sclpy
import numpy

def test_ug_all():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    ug_end=o2sclpy.uniform_grid_end.init(link,1,5,4)
    
    return
