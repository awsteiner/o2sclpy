import o2sclpy
import numpy

def test_ug_all():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    ug_end=o2sclpy.uniform_grid_end.initx(link,1,5,4)
    print(ug_end)
    print(ug_end.get_npoints())
    v=[ug_end[i] for i in range(0,ug_end.get_npoints())]
    print(v)
    
    return
