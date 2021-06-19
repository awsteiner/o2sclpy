import math
from PIL import Image
import operator
import functools
import os

def reprocess(filename):
    """
    Rewrite the o2graph script examples to use the Agg backend 
    and to remove the '-show' command. The reprocessed script
    is saved to 'doc/static/examples/temp.scr'.
    """
    f=open(filename,'r')
    f2=open('doc/static/examples/temp.scr','w')
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
    img1=Image.open('doc/static/figures/'+name+'_doc.png').histogram()
    img2=Image.open('doc/static/examples/'+name+'.png').histogram()
    rms = math.sqrt(functools.reduce(operator.add,
                                     map(lambda a,b: (a-b)**2,img1,img2))/
                    len(img1))
    assert rms<200, name
    return

def test_colors_near():
    ret=os.system('cd doc/static/examples; ./colors_near.scr')
    assert ret==0
    compare_images('near_blue')
    compare_images('near_hex')
    compare_images('near_rgb')
    return

def test_cmaps():
    ret=os.system('cd doc/static/examples; ./cmaps.scr')
    assert ret==0
    compare_images('cmaps')
    return

def test_markers():
    reprocess('doc/static/examples/markers.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('markers')
    return

def test_modax():
    reprocess('doc/static/examples/modax.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('modax')
    return

def test_subplots1():
    reprocess('doc/static/examples/subplots1.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('subplots1')
    return

def test_subplots2():
    reprocess('doc/static/examples/subplots2.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('subplots2')
    return

def test_subplots3():
    reprocess('doc/static/examples/subplots3.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('subplots3')
    return

def test_table_plot():
    reprocess('doc/static/examples/table_plot.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('table_plot')
    return

def test_table_plot_color():
    reprocess('doc/static/examples/table_plot_color.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('table_plot_color')
    return

def test_table_plotv():
    reprocess('doc/static/examples/table_plotv.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    os.system('cd doc/static/examples; ./temp.scr')
    compare_images('table_plotv')
    return

def test_table_rplot():
    reprocess('doc/static/examples/table_rplot.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('table_rplot')
    return

def test_table_errorbar():
    reprocess('doc/static/examples/table_errorbar.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('table_errorbar')
    return

def test_textbox():
    reprocess('doc/static/examples/textbox.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('textbox')
    return

def test_table_scatter():
    reprocess('doc/static/examples/table_scatter.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('table_scatter')
    return

def test_table3d_den_plot():
    reprocess('doc/static/examples/table3d_den_plot.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('table3d_den_plot')
    return

def test_yt_scatter():
    reprocess('doc/static/examples/yt_scatter.scr')
    os.system('chmod 755 doc/static/examples/temp.scr')
    ret=os.system('cd doc/static/examples; ./temp.scr')
    assert ret==0
    compare_images('yt_scatter')
    return

# We comment this one out because its time consuming
#def test_yt_tg_multvol():
#    reprocess('doc/static/examples/yt_tg_multvol.scr')
#    os.system('chmod 755 doc/static/examples/temp.scr')
#    ret=os.system('cd doc/static/examples; ./temp.scr')
#    assert ret==0
#    compare_images('yt_tg_multvol')
#    return

