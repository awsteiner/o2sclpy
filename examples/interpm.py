# # Multi-dimensional interpolation example for O$_2$sclpy

# See the O$_2$sclpy documentation at https://awsteiner.org/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import random
import numpy
import sys
from IPython.utils import io

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
quit()

# Link the O$_2$scl library:

link=o2sclpy.linker()
link.link_o2scl()

# Create the data set:

ug=o2sclpy.uniform_grid_end.init(link,0,2,49)
t3d=o2sclpy.table3d(link)
t3d.set_xy_grid("x",ug,"y",ug)
t3d.new_slice("z")
for i in range(0,t3d.get_nx()):
    for j in range(0,t3d.get_ny()):
        x=t3d.get_grid_x(i)
        y=t3d.get_grid_y(j)
        r=numpy.sqrt(x**2+y**2)+numpy.cos(x*4)-y
        t3d.set(i,j,"z",numpy.sin(r*5))

# Make a density plot of the original data set:
        
if plots:
    pl=o2sclpy.plot_base()
    pl.canvas()
    pl.den_plot([t3d,"z"])
    pl.colbar=True
    pl.xtitle('x')
    pl.ytitle('y')
    plot.show()

# Collect function values scattered across this plane:

N=300
x2=numpy.zeros((N,2))
y2=numpy.zeros((N,1))
for i in range(0,N):
    x2[i,0]=random.random()*2.0
    x2[i,1]=random.random()*2.0
    y2[i,0]=t3d.interp(x2[i,0],x2[i,1],"z")

# Create the Gaussian process interpolation object and train it with
# the scattered function values
    
im=o2sclpy.interpm_sklearn_gp()
im.set_data_str(x2,y2,'test_size=0.1')

# Use the Gaussian process to fill the plane

t3d.new_slice("gp")
for i in range(0,t3d.get_nx()):
    for j in range(0,t3d.get_ny()):
        x=t3d.get_grid_x(i)
        y=t3d.get_grid_y(j)
        t3d.set(i,j,"gp",im.eval(numpy.array([x,y])))

# Make a comparison plot
        
if plots:
    pl.canvas()
    pl.den_plot([t3d,"gp"])
    pl.colbar=True
    plot.show()

# Create the neural network interpolation object
    
im2=o2sclpy.interpm_tf_dnn()
print(' ')

# Train the neural network, but capture the output

with io.capture_output() as cap:
    im2.set_data(x2,y2,verbose=1,epochs=2000,
                 transform='none',test_size=0.0,
                 activations=['relu','relu','relu','relu'],
                 hlayers=[256,128,64,16])

# Summarize the end of the training output
    
print('')
lines1=cap.stdout.split('\n')
for line in lines1[-10:]:
    print(line)

# Use the neural network to fill the plane of data. This step takes a
# few minutes.
    
# +
if t3d.is_slice("nn")[0]==False:
    t3d.new_slice("nn")
t3d.set_slice_all("nn",0.0)
for i in range(0,t3d.get_nx()):
    for j in range(0,t3d.get_ny()):
        x=t3d.get_grid_x(i)
        y=t3d.get_grid_y(j)
        with io.capture_output() as cap:
            t3d.set(i,j,"nn",im2.eval(numpy.array([x,y])));
    if i%2==1:
        print('i:',i+1,'/',t3d.get_nx())
# -

# Make a comparison plot

if plots:
    pl.canvas()
    pl.den_plot([t3d,"nn"])
    pl.colbar=True
    plot.show()

# Now perform a quantitative comparison of the performance of the
# Gaussian process and the neural network and compare them. This is
# not a complete or "fair" comparison.
    
gpt=0
nnt=0
for i in range(0,t3d.get_nx()):
    for j in range(0,t3d.get_ny()):
        gpt=gpt+numpy.abs(t3d.get(i,j,"z")-t3d.get(i,j,"gp"))
        nnt=nnt+numpy.abs(t3d.get(i,j,"z")-t3d.get(i,j,"nn"))
        
print('')
print('Gaussian proces:',gpt,'neural network:',nnt)


