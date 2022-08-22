import math
from PIL import Image
from PIL import ImageChops
import operator
import functools
import os

def reprocess(filename):
    """
    Rewrite the o2graph script examples to use the Agg backend 
    and to remove the '-show' command. The reprocessed script
    is saved to 'data/temp.scr'.
    """
    f=open(filename,'r')
    f2=open('examples/data/temp.scr','w')
    for line in f:
        line2=line.replace('-show','')
        line2=line.replace('o2graph','o2graph -backend Agg')
        f2.write(line2)
    f.close()
    f2.close()
    return

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
    reprocess('examples/markers.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('markers')
    return

def test_modax():
    reprocess('examples/modax.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('modax')
    return

def test_subplots1():
    reprocess('examples/subplots1.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('subplots1')
    return

def test_subplots2():
    reprocess('examples/subplots2.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('subplots2')
    return

def test_subplots3():
    reprocess('examples/subplots3.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('subplots3')
    return

def test_table_plot():
    reprocess('examples/table_plot.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('table_plot')
    return

def test_table_plot_color():
    reprocess('examples/table_plot_color.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('table_plot_color')
    return

def test_table_plotv():
    reprocess('examples/table_plotv.scr')
    os.system('chmod 755 examples/data/temp.scr')
    os.system('cd examples; data/temp.scr')
    compare_images('table_plotv')
    return

def test_table_rplot():
    reprocess('examples/table_rplot.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('table_rplot')
    return

def test_table_errorbar():
    reprocess('examples/table_errorbar.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('table_errorbar')
    return

def test_textbox():
    reprocess('examples/textbox.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('textbox')
    return

def test_table_scatter():
    reprocess('examples/table_scatter.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('table_scatter')
    return

def test_table3d_den_plot():
    reprocess('examples/table3d_den_plot.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('table3d_den_plot')
    return

def test_yt_scatter():
    reprocess('examples/yt_scatter.scr')
    os.system('chmod 755 examples/data/temp.scr')
    ret=os.system('cd examples; data/temp.scr')
    assert ret==0
    compare_images('yt_scatter')
    return

# We comment this one out because its time consuming
#def test_yt_tg_multvol():
#    reprocess('examples/yt_tg_multvol.scr')
#    os.system('chmod 755 examples/data/temp.scr')
#    ret=os.system('cd examples; data/temp.scr')
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
