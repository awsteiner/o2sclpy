#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023-2024, Andrew W. Steiner
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

def test_all():
    ls=o2sclpy.lib_settings_class()

    obj=ls.date_compiled()
    s='check type of string properties'
    assert str(type(obj))=="<class 'bytes'>",s

    val=ls.range_check()
    assert val==True or val==False,'check the type of a bool property'
    
    cu=ls.get_convert_units()
    x=cu.convert('g','1/fm',1.0)
    assert numpy.allclose(x,2.8427e24,rtol=1.0e-4),'convert_units()'
    
    return

if __name__ == '__main__':
    test_all()
    print('All tests passed.')
