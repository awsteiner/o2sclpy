import math
from PIL import Image
import operator
import functools
import os

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
    os.system('cd doc/static/examples; ./markers.scr')
    compare_images('markers')
    return

def test_modax():
    os.system('cd doc/static/examples; ./modax.scr')
    compare_images('modax')
    return

def test_subplots1():
    os.system('cd doc/static/examples; ./subplots1.scr')
    compare_images('subplots1')
    return

def test_subplots2():
    os.system('cd doc/static/examples; ./subplots2.scr')
    compare_images('subplots2')
    return

def test_subplots3():
    os.system('cd doc/static/examples; ./subplots3.scr')
    compare_images('subplots3')
    return

def test_table_plot():
    os.system('cd doc/static/examples; ./table_plot.scr')
    compare_images('table_plot')
    return

def test_table_plotv():
    os.system('cd doc/static/examples; ./table_plotv.scr')
    compare_images('table_plotv')
    return

def test_table_rplot():
    os.system('cd doc/static/examples; ./table_rplot.scr')
    compare_images('table_rplot')
    return

def test_table_errorbar():
    os.system('cd doc/static/examples; ./table_errorbar.scr')
    compare_images('table_errorbar')
    return

def test_textbox():
    os.system('cd doc/static/examples; ./textbox.scr')
    compare_images('textbox')
    return

def test_table_scatter():
    os.system('cd doc/static/examples; ./table_scatter.scr')
    compare_images('table_scatter')
    return

def test_table3d_den_plot():
    os.system('cd doc/static/examples; ./table3d_den_plot.scr')
    compare_images('table3d_den_plot')
    return

def test_yt_scatter():
    os.system('cd doc/static/examples; ./yt_scatter.scr')
    compare_images('yt_scatter')
    return

