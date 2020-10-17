# In the milky way the number of stars per unit volume near the sun is
# about 0.14/pc^3, so there are about 100 stars in a cube with 9pc on
# each side.

import o2sclpy
import yt
import random
import numpy

p=o2sclpy.yt_plot_base()

random.seed()
stars=[]
colors=[]
sizes=[]
for i in range(0,100):
    stars.append([random.random()*9.0,
                  random.random()*9.0,
                  random.random()*9.0])
    colors.append([1,1,1])
    sizes.append([random.random()*5.0])

p.xlimits(0,9)
p.ylimits(0,9)
p.zlimits(0,9)
p.yt_position='[4.5,4.5,9]'
p.yt_def_vol()

from yt.visualization.volume_rendering.api import PointSource

ps=PointSource(numpy.array(stars),colors=numpy.array(colors),
               radii=numpy.array(sizes))
p.yt_scene.add_source(ps,keyname='stars')



