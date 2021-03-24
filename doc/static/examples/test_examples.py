import math
from PIL import Image
import operator
import functools
import os

def remove_show(filename):
    f=open(filename,'r')
    f2=open('doc/static/examples/temp.scr','w')
    for line in f:
        line2=line.replace('-show','')
    f2.write(line2)
    f.close()
    f2.close()
    return

def compare_images(name):
    img1=Image.open('doc/static/figures/'+name+'_doc.png').histogram()
    img2=Image.open('doc/static/examples/'+name+'.png').histogram()
    rms = math.sqrt(functools.reduce(operator.add,
                                     map(lambda a,b: (a-b)**2,img1,img2))/
                    len(img1))
    assert rms<200, name
    return

def test_colors_near():
    os.system('cd doc/static/examples; ./colors_near.scr')
    compare_images('near_blue')
    compare_images('near_hex')
    compare_images('near_rgb')
    return

def test_markers():
    remove_show('doc/static/examples/markers.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('markers')
    return

def test_modax():
    remove_show('doc/static/examples/modax.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('modax')
    return

def test_subplots1():
    remove_show('doc/static/examples/subplots1.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('subplots1')
    return

def test_subplots2():
    remove_show('doc/static/examples/subplots2.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('subplots2')
    return

def test_subplots3():
    remove_show('doc/static/examples/subplots3.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('subplots3')
    return

def test_table_plot():
    remove_show('doc/static/examples/table_plot.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('table_plot')
    return

def test_table_plotv():
    remove_show('doc/static/examples/table_plotv.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('table_plotv')
    return

def test_table_rplot():
    remove_show('doc/static/examples/table_rplot.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('table_rplot')
    return

def test_table_errorbar():
    remove_show('doc/static/examples/table_errorbar.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('table_errorbar')
    return

def test_textbox():
    remove_show('doc/static/examples/textbox.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('textbox')
    return

def test_table_scatter():
    remove_show('doc/static/examples/table_scatter.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('table_scatter')
    return

def test_table3d_den_plot():
    remove_show('doc/static/examples/table3d_den_plot.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('table3d_den_plot')
    return

def test_yt_scatter():
    remove_show('doc/static/examples/yt_scatter.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('yt_scatter')
    return

