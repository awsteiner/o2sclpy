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
