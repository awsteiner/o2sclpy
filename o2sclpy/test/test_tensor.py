import o2sclpy
import copy
import numpy

def def_tensor(link):
    tensor=o2sclpy.tensor(link)
    tensor.resize([2,3,4])
    for i in range(0,2):
        for j in range(0,3):
            for k in range(0,4):
                temp_list=[i,j,k]
                tensor.set(temp_list,i+j+k)
    return tensor

def subtest_basic(link):

    tensor=def_tensor(link)
    """
    assert tensor.get_nlines()==5,'get_nlines()'
    assert tensor.get_ncolumns()==3,'get_ncolumns()'
    assert tensor.get('col1',2)==4,'get()'
    assert tensor.get_column_name(2)==b'col3','get_column_name()'
    assert tensor.get('col2',2)==8.0,'function_column()'
    v=tensor['col2']
    assert len(v)==5, 'get_column()'
    assert v[4]==10.0, 'get_column()'
    v2=tensor['col2']
    numpy.testing.assert_array_equal(v,v2,'operator[] vs. get_column')
    tensor.init_column('col3',3)
    assert tensor.get('col3',4)==3.0,'init_column()'
    tensor.delete_column('col3')
    assert tensor.is_column('col3')==False,'is_column()'
    tensor.line_of_data([2,1])
    assert tensor.get('col1',5)==2.0,'line_of_data'
    assert tensor.get_nlines()==6,'line_of_data'
    tensor.new_column('col4')
    assert tensor.get_ncolumns()==3,'new_column() and get_ncolumns()'
    tensor.rename_column('col4','col3')
    assert tensor.get_column_name(2)==b'col3','rename_column()'
    tensor.init_column('col3',9.0)
    assert tensor.get('col3',4)==9.0,'init_column()'
    assert tensor.lookup_column('col2')==1,'lookup_column()'
    tensor.copy_column('col3','ccol3')
    assert tensor.get('ccol3',4)==9.0,'copy_column()'
    nrows1=tensor.get_nlines()
    tensor.new_row(2)
    nrows2=tensor.get_nlines()
    assert nrows1+1==nrows2,'new_row()'
    assert tensor.get('col1',3)==4.0,'new_row()'
    tensor.copy_row(3,2)
    assert tensor.get('col1',2)==4.0,'copy_row()'
    tensor.functions_columns('col5=col1+col2 col6=col1-col2')
    assert tensor.get('col5',1)==tensor.get('col1',1)+tensor.get('col2',1)
    # Make sure summary() works
    tensor.summary()
    """
    return

def subtest_copying(link):
    
    ten1=def_tensor(link)
    """
    ten2=copy.copy(ten1)
    assert ten2.get('col1',2)==4,'Check the shallow copy'
    ten2.set('col1',2,3)
    assert ten1.get('col1',2)==3,'Show changes in the second impact the first'
    ten3=copy.deepcopy(ten1)
    ten3.set('col1',2,2)
    assert ten1.get('col1',2)==3,'Show deep copy produces unique tensor'
    """
    return

def subtest_hdf5(link,tmp_path):
    
    p=tmp_path/"tensor.o2"
    filename=bytes(str(p),'utf-8')
    
    ten1=def_tensor(link)

    # Write ten1 to a file
    hf=o2sclpy.hdf_file(link)
    hf.open_or_create(filename)
    o2sclpy.hdf_output_tensor(link,hf,ten1,b'tensor')
    hf.close()

    # Open the file and read into ten2
    hf.open(filename,False,True)
    name=o2sclpy.std_string(link)
    ten2=o2sclpy.tensor(link)
    o2sclpy.hdf_input_n_tensor(link,hf,ten2,name)
    hf.close()
    
    #assert ten2.get_nlines()==ten1.get_nlines(),"nlines after hdf_input()"
    
    return

def test_all(tmp_path):
    link=o2sclpy.linker()
    link.link_o2scl()

    subtest_basic(link)
    subtest_copying(link)
    subtest_hdf5(link,tmp_path)
    return
    
    
