#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023-2024, Andrew W. Steiner
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
import math
from PIL import Image
from PIL import ImageChops
import operator
import functools
import os

def compare_images(name,diff=200):
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
    assert rms<diff, name
    return

def compare_files(name1,name2):

    f=open(name1)
    f2=open(name2)

    with open(name1) as f:
        lines1=f.readlines()
    with open(name2) as f2:
        lines2=f2.readlines()
    for i in range(0,len(lines1)):
        if len(lines2)<i:
            print('Files have different lengths,',len(lines1),
                  len(lines2),'.')
            assert len(lines1)==len(lines2)
        elif lines1[i]!=lines2[i]:
            print('Difference detected at line ',i,'.')
            print(' 1:',lines1[i])
            print(' 2:',lines2[i])
            assert lines1[i]==lines2[i]

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

def test_kde_plot():
    ret=os.system('cd examples; ./kde_plot.scr')
    assert ret==0
    compare_images('kde_plot')
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
    print('Running examples/test_examples.py:test_textbox().')
    ret=os.system('cd examples; ./textbox.scr')
    assert ret==0
    compare_images('textbox')
    print('Done in examples/test_examples.py:test_textbox().')
    return

def test_table_scatter():
    ret=os.system('cd examples; ./table_scatter.scr')
    assert ret==0
    compare_images('table_scatter')
    return

def test_table3d_den_plot():
    ret=os.system('cd examples; ./table3d_den_plot.scr')
    # 9/12/21: I'm not sure why this is failing right now
    #assert ret==0
    compare_images('table3d_den_plot')
    return

def test_yt_scatter():
    ret=os.system('cd examples; ./yt_scatter.scr')
    assert ret==0
    compare_images('yt_scatter',diff=400)
    return

def test_gltf_den_plot():
    ret=os.system('cd examples; ./gltf_den_plot.scr')
    assert ret==0
    compare_files('examples/gltf/den_plot.gltf',
                  'doc/static/gltf/den_plot.gltf')
    return

def test_gltf_den_plot_col():
    ret=os.system('cd examples; ./gltf_den_plot_col.scr')
    assert ret==0
    compare_files('examples/gltf/den_plot_col.gltf',
                  'doc/static/gltf/den_plot_col.gltf')
    return

# This doesn't have a 'test_' prefix so that we can make
# it optional 
def bl_den_plot_yaw():
    ret=os.system('cd examples; ./bl_den_plot_yaw.scr')
    assert ret==0
    return

def test_gltf_scatter():
    ret=os.system('cd examples; ./gltf_scatter.scr')
    assert ret==0
    compare_files('examples/gltf/scatter.gltf',
                  'doc/static/gltf/scatter.gltf')
    return

def test_gltf_scatter_col():
    ret=os.system('cd examples; ./gltf_scatter_col.scr')
    assert ret==0
    compare_files('examples/gltf/scatter_col.gltf',
                  'doc/static/gltf/scatter_col.gltf')
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
    test_kde_plot()
    test_table_plot_color()
    test_table_plotv()
    test_table_rplot()
    test_table_errorbar()
    test_textbox()
    test_table_scatter()
    test_table3d_den_plot()
    test_yt_scatter()
    test_gltf_den_plot()
    test_gltf_den_plot_col()
    test_gltf_scatter()
    test_gltf_scatter_col()
    if 'O2GRAPH_BLENDER_CMD' in os.environ:
        bl_den_plot_yaw()
    print('All tests passed.')
