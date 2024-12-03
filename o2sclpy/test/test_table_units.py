#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023-2025, Andrew W. Steiner
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
import copy
import numpy

def def_table_units():
    table=o2sclpy.table_units()
    table.line_of_names('col1 col2 col3')
    table.set_unit('col1','km')
    table.set_unit('col2','Msun')
    table.set_unit('col3','Msun/km')
    table.set_nlines(5)
    table.set('col1',0,3)
    table.set('col1',1,1)
    table.set('col1',2,4)
    table.set('col1',3,1)
    table.set('col1',4,5)
    table.function_column('2*col1','col2')
    table.function_column('sin(col2)','col3')
    return table

def subtest_basic():

    table=def_table_units()
    assert table.get_unit('col1')==b'km','get_unit()'
    return

def subtest_copying():
    
    tab1=def_table_units()
    tab2=copy.copy(tab1)
    assert tab2.get('col1',2)==4,'Check the shallow copy'
    tab2.set('col1',2,3)
    assert tab1.get('col1',2)==3,'Show changes in the second impact the first'
    tab3=copy.deepcopy(tab1)
    tab3.set('col1',2,2)
    assert tab1.get('col1',2)==3,'Show deep copy produces unique table'
    return

def subtest_hdf5(tmp_path):
    
    p=tmp_path/"table_units.o2"
    filename=bytes(str(p),'utf-8')
    
    tab1=def_table_units()

    # Write tab1 to a file
    hf=o2sclpy.hdf_file()
    hf.open_or_create(filename)
    o2sclpy.hdf_output_table_units(hf,tab1,b'table_units')
    hf.close()

    # Open the file and read into tab2
    hf.open(filename,False,True)
    name=o2sclpy.std_string()
    tab2=o2sclpy.table_units()
    o2sclpy.hdf_input_n_table_units(hf,tab2,name)
    hf.close()
    assert name.to_bytes()==b'table_units','name after hdf_input()'
    assert tab2.get_nlines()==tab1.get_nlines(),"nlines after hdf_input()"
    return

def test_all(tmp_path):
    subtest_basic()
    subtest_copying()
    subtest_hdf5(tmp_path)
    return
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
