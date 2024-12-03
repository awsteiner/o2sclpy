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
import sys

def test_all(tmp_path):

    ug_end=o2sclpy.uniform_grid_end.init(1,5,4)
    v=[ug_end[i] for i in range(0,ug_end.get_npoints())]
    numpy.testing.assert_array_equal(v,[1,2,3,4,5],'getitem')
    assert ug_end.get_npoints()==5,'get_npoints()'
    assert ug_end.get_end()==5.0,'get_end()'

    v2=o2sclpy.std_vector()
    ug_end.vector(v2)
    assert len(v2)==5,'vector()+len()'
    numpy.testing.assert_array_equal(v2.to_numpy(),[1,2,3,4,5],'vector()')

    # Handle the tmp_path fixture gracefully if we're not using pytest
    if 'pytest' in sys.modules:
        filename=bytes(str(tmp_path/"test_uniform_grid.o2"),'utf-8')
    else:
        filename=bytes(tmp_path+"test_uniform_grid.o2",'utf-8')
    
    # Write to a file
    hf=o2sclpy.hdf_file()
    hf.open_or_create(filename)
    o2sclpy.hdf_output_uniform_grid(hf,ug_end,b'ug_end')
    hf.close()

    # Open the file and read into tab2
    hf.open(filename,False,True)
    name=o2sclpy.std_string()
    ug=o2sclpy.uniform_grid()
    o2sclpy.hdf_input_n_uniform_grid(hf,ug,name)
    hf.close()

    # Make sure they are equal
    assert name.to_bytes()==b'ug_end','name after hdf_input()'
    assert ug_end.get_end()==ug.get_end(),'get_end() after hdf_input()'
    
    return

if __name__ == '__main__':

    # Handle the tmp_path fixture gracefully if we're not using pytest
    if 'pytest' in sys.modules:
        test_all()
    else:
        test_all('./')
    print('All tests passed.')
