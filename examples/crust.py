# # O$_2$scl table example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://awsteiner.org/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import numpy
import sys
import random

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Link the o2scl library:

link=o2sclpy.linker()
link.link_o2scl()

# Create an HDF5 file object and open the table in O$_2$scl's data file for the Akmal, Pandharipande, and Ravenhall equation of state. The `open()` function for the `hdf_file` class is documented [here](https://awsteiner.org/code/o2sclpy/hdf.html#o2sclpy.hdf_file.open).

hf=o2sclpy.hdf_file(link)
hf.open(b'crust_SLy4_fcs2.o2')

# We create a table object and specify a blank name to indicate
# that we just want to read the first table in the file.

eos_tab=o2sclpy.table(link)
name=b''

# Read the table:

o2sclpy.hdf_input_table(link,hf,eos_tab,name)

# Close the HDF5 file.

hf.close()

# Read the second table

hf.open(b'tov_SLy4_14.o2')
tov_tab=o2sclpy.table(link)
name=b''
o2sclpy.hdf_input_table(link,hf,tov_tab,name)
hf.close()

# We use the `cap_cout` class to capture `std::cout` to the Jupyter notebook. The `summary()` function lists the columns in the table.

eos_tab.summary()
tov_tab.summary()

r_out=tov_tab.interp('nb',eos_tab.interp('rho',1.0e8,'nb'),'r')
r_in=tov_tab.interp('nb',eos_tab.interp('rho',1.0e12,'nb'),'r')

# The number of meters in real space for one kilometer in NS space
x_scale=10/(r_out-r_in)
N_bins=20

ug_r=o2sclpy.uniform_grid_end.init(link,0,(r_out-r_in)*x_scale,N_bins)

r_rep=[]
nb_rep=[]
rho_rep=[]
nn_rep=[]
nnuc_rep=[]
Z_rep=[]
N_rep=[]

print('xlow       xhi        r          nb         rho       ',
      'nn         nnuc       Z        N')
for j in range(0,N_bins):
    rad=r_out-(ug_r[j]+ug_r[j+1])/2.0/x_scale
    nb=tov_tab.interp('r',rad,'nb')
    
    r_rep.append(rad)
    nb_rep.append(nb)
    rho_rep.append(eos_tab.interp('nb',nb,'rho'))
    nn=eos_tab.interp('nb',nb,'nn')
    if nn<1.0e-7:
        nn=0.0
    nn_rep.append(nn)
    nnuc_rep.append(eos_tab.interp('nb',nb,'nnuc'))
    Z_rep.append(eos_tab.interp('nb',nb,'Z'))
    N_rep.append(eos_tab.interp('nb',nb,'N'))

    print('%5.4e %5.4e %5.4e %5.4e %5.4e %5.4e %5.4e %5.4e %5.4e' %
          (ug_r[j],ug_r[j+1],r_rep[j],nb_rep[j],rho_rep[j],nn_rep[j],
           nnuc_rep[j],Z_rep[j],N_rep[j]))
print('')    

print(' j x          r          nn+nnuc')
h=o2sclpy.hist(link)
h.set_bin_edges_grid(ug_r)
hsum=0.0
for j in range(0,h.size()):
    h.set_wgt_i(j,nn_rep[j]+nnuc_rep[j])
    print('%2d %5.4e %5.4e %5.4e' % (j,(ug_r[j]+ug_r[j+1])/2,r_rep[j],h[j]))
    hsum=hsum+h[j]
print('')    
    
pdh=o2sclpy.prob_dens_hist(link)
pdh.init(h)

# width and height of simulation in meters
yz_scale=1.0

print('r_out',r_out)
print('r_in',r_in)
print('')

op=o2sclpy.o2graph_plotter()

M=10000
print('Number of particles in last bin per fm^3 in the NS: %5.4e' % h[19])
print('Number of particles in last bin in simulation: %5.4e' %
      (float(M)*h[19]/hsum))
print('Volume of simulation in fm^3: %5.4e' % (float(M)*h[19]/hsum/h[19]))
print('Volume in simulation in m^3: %5.4e' %
      ((ug_r[1]-ug_r[0])*yz_scale*yz_scale))
cf=numpy.cbrt(((ug_r[1]-ug_r[0])*yz_scale*yz_scale)/
              (float(M)*h[19]/hsum/h[19]))
print('Conversion factor in m/fm: %5.4e' % cf)
print('')

op.xlo=0
op.xhi=1
op.xset=True
op.ylo=0
op.yhi=1
op.yset=True
op.zlo=0
op.zhi=1
op.zset=True

op.td_wdir='gltf'

#print('x          r')
for i in range(0,100):
    xt=pdh.sample()
    rt=r_out-xt/x_scale
    nbt=tov_tab.interp('r',rt,'nb')
    rhot=eos_tab.interp('nb',nbt,'rho')
    nnt=eos_tab.interp('nb',nbt,'nn')
    if nnt<1.0e-7:
        nnt=0.0
    nnuct=eos_tab.interp('nb',nbt,'nnuc')
    Zt=eos_tab.interp('nb',nbt,'Z')
    Nt=eos_tab.interp('nb',nbt,'N')
    ratio=nnuct/(nnuct+nnt)
    yt=yz_scale*random.random()
    zt=yz_scale*random.random()
    if random.random()<ratio:
        rnuc=numpy.cbrt(3*(Zt+Nt)/0.16/4/numpy.pi)
        op.td_icos([xt,yt,zt],r=rnuc*cf)
        print('nuc %5.4e %5.4e %5.4e %5.4e %5.4e %5.4e' %
              (xt,yt,zt,rnuc*cf,Zt,Nt))
    else:
        rneut=0.8
        op.td_icos([xt,yt,zt],r=rneut*cf)
        print('n   %5.4e %5.4e %5.4e %5.4e' % 
              (xt,yt,zt,rneut*cf))

op.to.write_gltf(op.td_wdir,'crust',2)        


