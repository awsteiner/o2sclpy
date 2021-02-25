import o2sclpy

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

def test_simple():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    table=o2sclpy.table(link)
    table.line_of_names('col1 col2 col3')
    table.set_nlines(5)
    table.set('col1',0,3)
    table.set('col1',1,1)
    table.set('col1',2,4)
    table.set('col1',3,1)
    table.set('col1',4,5)
    assert table.get_nlines()==5,'get_nlines()'
    assert table.get('col1',2)==4,'get()'
    table.function_column('2*col1','col2')
    table.function_column('sin(col2)','col3')
    table.summary()
    return

def test_copying():
    link=o2sclpy.linker()
    link.link_o2scl_o2graph()

    tab=def_table(link)
    tab.summary()


