import math
from PIL import Image
from PIL import ImageChops
import operator
import functools
import os

def compare_images(name):
    """
    Compare the script image with the version in the figures
    directory and ensure they are nearly identical.
    """
    img1=Image.open('doc/static/figures/'+name+'.png')
    img2=Image.open('examples/figures/'+name+'.png')
    img1h=img1.histogram()
    img2h=img2.histogram()
    rms = math.sqrt(functools.reduce(operator.add,
                                     map(lambda a,b: (a-b)**2,img1h,img2h))/
                    len(img1h))
    #img3=ImageChops.subtract(img1,img2)
    #img3.save('figures/'+name+'_diff.png')
    assert rms<200, name
    return

def test_colors_near():
    ret=os.system('cd examples; ./colors_near.scr')
    assert ret==0
    compare_images('near_blue')
    compare_images('near_hex')
    compare_images('near_rgb')
    return

def test_cmaps():
    ret=os.system('cd examples; ./cmaps.scr')
    assert ret==0
    compare_images('cmaps')
    return

def test_markers():
    ret=os.system('cd examples; ./markers.scr')
    assert ret==0
    compare_images('markers')
    return

def test_modax():
    ret=os.system('cd examples; ./modax.scr')
    assert ret==0
    compare_images('modax')
    return

def test_subplots1():
    ret=os.system('cd examples; ./subplots1.scr')
    assert ret==0
    compare_images('subplots1')
    return

def test_subplots2():
    ret=os.system('cd examples; ./subplots2.scr')
    assert ret==0
    compare_images('subplots2')
    return

def test_subplots3():
    ret=os.system('cd examples; ./subplots3.scr')
    assert ret==0
    compare_images('subplots3')
    return

def test_table_plot():
    ret=os.system('cd examples; ./table_plot.scr')
    assert ret==0
    compare_images('table_plot')
    return

def test_table_plot_color():
    ret=os.system('cd examples; ./table_plot_color.scr')
    assert ret==0
    compare_images('table_plot_color')
    return

def test_table_plotv():
    ret=os.system('cd examples; ./table_plotv.scr')
    assert ret==0
    compare_images('table_plotv')
    return

def test_table_rplot():
    ret=os.system('cd examples; ./table_rplot.scr')
    assert ret==0
    compare_images('table_rplot')
    return

def test_table_errorbar():
    ret=os.system('cd examples; ./table_errorbar.scr')
    assert ret==0
    compare_images('table_errorbar')
    return

def test_textbox():
    ret=os.system('cd examples; ./textbox.scr')
    assert ret==0
    compare_images('textbox')
    return

def test_table_scatter():
    ret=os.system('cd examples; ./table_scatter.scr')
    assert ret==0
    compare_images('table_scatter')
    return

def test_table3d_den_plot():
    ret=os.system('cd examples; ./table3d_den_plot.scr')
    assert ret==0
    compare_images('table3d_den_plot')
    return

def test_yt_scatter():
    ret=os.system('cd examples; ./yt_scatter.scr')
    assert ret==0
    compare_images('yt_scatter')
    return

# We comment this one out because its time consuming
#def test_yt_tg_multvol():
#    ret=os.system('cd examples; ./yt_tg_multvol.scr')
#    assert ret==0
#    compare_images('yt_tg_multvol')
#    return

if __name__ == '__main__':
    test_colors_near()
    test_cmaps()
    test_markers()
    test_modax()
    test_subplots1()
    test_subplots2()
    test_subplots3()
    test_table_plot()
    test_table_plot_color()
    test_table_plotv()
    test_table_rplot()
    test_table_errorbar()
    test_textbox()
    test_table_scatter()
    test_table3d_den_plot()
    test_yt_scatter()
    print('All tests passed.')
