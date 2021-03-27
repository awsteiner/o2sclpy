import o2sclpy
import copy
import numpy

def def_table_units(link):
    table=o2sclpy.table_units(link)
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

def subtest_basic(link):

    table=def_table_units(link)
    assert table.get_unit('col1')==b'km','get_unit()'
    return

def subtest_copying(link):
    
    tab1=def_table_units(link)
    tab2=copy.copy(tab1)
    assert tab2.get('col1',2)==4,'Check the shallow copy'
    tab2.set('col1',2,3)
    assert tab1.get('col1',2)==3,'Show changes in the second impact the first'
    tab3=copy.deepcopy(tab1)
    tab3.set('col1',2,2)
    assert tab1.get('col1',2)==3,'Show deep copy produces unique table'
    return

def subtest_hdf5(link):
    
    tab1=def_table_units(link)

    # Write tab1 to a file
    hf=o2sclpy.hdf_file(link)
    hf.open_or_create(b'o2sclpy/test/temp2.o2')
    o2sclpy.hdf_output_table_units(link,hf,tab1,b'table_units')
    hf.close()

    # Open the file and read into tab2
    hf.open(b'o2sclpy/test/temp2.o2',False,True)
    name=o2sclpy.std_string(link)
    tab2=o2sclpy.table_units(link)
    o2sclpy.hdf_input_n_table_units(link,hf,tab2,name)
    hf.close()
    assert name.to_bytes()==b'table_units','name after hdf_input()'
    assert tab2.get_nlines()==tab1.get_nlines(),"nlines after hdf_input()"
    return

def test_all():
    link=o2sclpy.linker()
    link.link_o2scl()

    subtest_basic(link)
    subtest_copying(link)
    subtest_hdf5(link)
    return
    
    
