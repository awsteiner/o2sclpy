import o2sclpy
import numpy

def test_all():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    ls=link.o2scl_settings
    assert ls.eos_installed()==True, 'eos_installed()'

    obj=ls.date_compiled()
    s='check type of string properties'
    assert str(type(obj))=="<class 'bytes'>",s

    val=ls.range_check()
    assert val==True or val==False,'check the type of a bool property'
    
    cu=ls.get_convert_units()
    x=cu.convert('g','1/fm',1.0)
    assert numpy.allclose(x,2.8427e24,rtol=1.0e-4),'convert_units()'
    
    return
    
    
