import o2sclpy
import copy
import numpy

def def_table(link):
    table=o2sclpy.table(link)
    table.line_of_names('col1 col2 col3')
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

    table=def_table(link)
    assert table.get_nlines()==5,'get_nlines()'
    assert table.get_ncolumns()==3,'get_ncolumns()'
    assert table.get('col1',2)==4,'get()'
    assert table.get_column_name(2)==b'col3','get_column_name()'
    assert table.get('col2',2)==8.0,'function_column()'
    v=table['col2']
    assert len(v)==5, 'get_column()'
    assert v[4]==10.0, 'get_column()'
    v2=table['col2']
    numpy.testing.assert_array_equal(v,v2,'operator[] vs. get_column')
    table.init_column('col3',3)
    assert table.get('col3',4)==3.0,'init_column()'
    table.delete_column('col3')
    assert table.is_column('col3')==False,'is_column()'
    table.line_of_data([2,1])
    assert table.get('col1',5)==2.0,'line_of_data'
    assert table.get_nlines()==6,'line_of_data'
    table.new_column('col4')
    assert table.get_ncolumns()==3,'new_column() and get_ncolumns()'
    table.rename_column('col4','col3')
    assert table.get_column_name(2)==b'col3','rename_column()'
    table.init_column('col3',9.0)
    assert table.get('col3',4)==9.0,'init_column()'
    assert table.lookup_column('col2')==1,'lookup_column()'
    table.copy_column('col3','ccol3')
    assert table.get('ccol3',4)==9.0,'copy_column()'
    nrows1=table.get_nlines()
    table.new_row(2)
    nrows2=table.get_nlines()
    assert nrows1+1==nrows2,'new_row()'
    assert table.get('col1',3)==4.0,'new_row()'
    table.copy_row(3,2)
    assert table.get('col1',2)==4.0,'copy_row()'
    table.functions_columns('col5=col1+col2 col6=col1-col2')
    assert table.get('col5',1)==table.get('col1',1)+table.get('col2',1)
    # Make sure summary() works
    table.summary()
    return

def subtest_copying(link):
    
    tab1=def_table(link)
    tab2=copy.copy(tab1)
    assert tab2.get('col1',2)==4,'Check the shallow copy'
    tab2.set('col1',2,3)
    assert tab1.get('col1',2)==3,'Show changes in the second impact the first'
    tab3=copy.deepcopy(tab1)
    tab3.set('col1',2,2)
    assert tab1.get('col1',2)==3,'Show deep copy produces unique table'
    return

def subtest_hdf5(link):
    
    tab1=def_table(link)

    # Write tab1 to a file
    hf=o2sclpy.hdf_file(link)
    hf.open_or_create(b'o2sclpy/test/temp.o2')
    o2sclpy.hdf_output_table(link,hf,tab1,b'table')
    hf.close()

    # Open the file and read into tab2
    hf.open(b'o2sclpy/test/temp.o2',False,True)
    name=o2sclpy.std_string(link)
    tab2=o2sclpy.table(link)
    o2sclpy.hdf_input_n_table(link,hf,tab2,name)
    hf.close()
    assert name.to_bytes()==b'table','name after hdf_input()'
    assert tab2.get_nlines()==tab1.get_nlines(),"nlines after hdf_input()"
    return

def test_all():
    link=o2sclpy.linker()
    link.link_o2scl()

    subtest_basic(link)
    subtest_copying(link)
    subtest_hdf5(link)
    return
    
    
