import o2sclpy
import numpy

def test_lib_settings():
    print('h1')
    link=o2sclpy.linker()
    print('h2')
    link.link_o2scl_o2graph()

    print('h3')
    ls=link.o2scl_settings
    print('h4',ls.eos_installed())
    assert ls.eos_installed() == True, 'eos_installed()'

    print('h5')
    cu=ls.get_convert_units()
    print('h6',cu,cu._owner)
    x=cu.convert('g','1/fm',1.0)
    print('h7')
    assert numpy.allclose(x,2.8427e24,rtol=1.0e-4),'convert_units()'
    print('h8')
    
    return
    
    
