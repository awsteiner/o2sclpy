# # Neutron star crust example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://awsteiner.org/code/o2sclpy for more information.

# Initial parameters

# The length of the simulation in meters
x_size : float = 10.0
# The height and depth of the simulation in meters
yz_size : float = 1.0
# The number of bins for the histogram
N_bins : int = 20
# The number of particles in the simulation
N_part : int = 3000
# The fudge factor for the radius to make the particles larger
r_fudge : float = 3.0
# The lower limit of the mass density
density_low : float = 1.0e9
# The upper limit of the mass density
density_high : float = 1.0e12

# +
import o2sclpy
import matplotlib.pyplot as plot
import numpy
import sys
import random
from datetime import datetime

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Link the o2scl library:

link=o2sclpy.linker()
link.link_o2scl()

# Load the crust file

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

r_out=tov_tab.interp('nb',eos_tab.interp('rho',density_low,'nb'),'r')
r_in=tov_tab.interp('nb',eos_tab.interp('rho',density_high,'nb'),'r')

# The number of meters in real space for one kilometer in NS space
x_scale=x_size/(r_out-r_in)

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
    # Correct when the interpolation gives unphysical negative values
    # for the neutron density near the neutron drip density
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

print('r_out',r_out)
print('r_in',r_in)
print('')

op=o2sclpy.o2graph_plotter()

print('Number of particles in last bin per fm^3 in the NS: %5.4e' %
      h[N_bins-1])
print('Number of particles in last bin in simulation: %5.4e' %
      (float(N_part)*h[N_bins-1]/hsum))
print('Volume of simulation in fm^3: %5.4e' %
      (float(N_part)*h[N_bins-1]/hsum/h[N_bins-1]))
print('Volume in simulation in m^3: %5.4e' %
      ((ug_r[1]-ug_r[0])*yz_size*yz_size))
cf=numpy.cbrt(((ug_r[1]-ug_r[0])*yz_size*yz_size)/
              (float(N_part)*h[N_bins-1]/hsum/h[N_bins-1]))
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
xmin=1e99
Nmax=0
Nnuclei=0

mat_flag=numpy.zeros((100),dtype=int)
found_nucleus=numpy.zeros((N_bins),dtype=int)

op.td_mat('mat_blue',0,0,1,prefix='crust_')
op.td_mat('mat_red',1,0,0,prefix='crust_')

# Nucleon radius is 0.8 femtometers
r_nucleon=0.8

for i in range(0,N_part):

    xt=pdh.sample()
    if xt<xmin:
        xmin=xt

    i_bin=0
    for k in range(1,N_bins):
        if xt>ug_r[k] and xt<ug_r[k+1]:
            i_bin=k
    if xt>ug_r[N_bins]:
        print('Problem',xt,ug_r[0],ug_r[N_bins])
        quit()
        
    rt=r_out-xt/x_scale
    nbt=tov_tab.interp('r',rt,'nb')
    rhot=eos_tab.interp('nb',nbt,'rho')
    nnt=eos_tab.interp('nb',nbt,'nn')
    if nnt<1.0e-7:
        nnt=0.0
    nnuct=eos_tab.interp('nb',nbt,'nnuc')
    Zt=eos_tab.interp('nb',nbt,'Z')
    Nt=eos_tab.interp('nb',nbt,'N')
    Ni=int(Nt+1.0e-10)
    if Ni>100:
        Ni=100
    if Ni<1:
        Ni=1
    if Nt>Nmax:
        Nmax=Nt
    Zi=int(Zt+1.0e-10)
    if Zi>100:
        Zi=100
    if Zi<1:
        Zi=1
    ratio=nnuct/(nnuct+nnt)
    yt=yz_size*random.random()
    zt=yz_size*random.random()
    
    mat_name='mat_'+str(Ni)
    if mat_flag[Ni-1]==0:
        mat_flag[Ni-1]=1
        op.td_mat(mat_name,1.0-float(Ni-1)/99.0,
                   1.0-float(Ni-1)/99.0,1.0,1.0,prefix='crust_')
    
    if random.random()<ratio:

        rnuc=numpy.cbrt(3*(Zt+Nt)/0.16/4/numpy.pi)
        
        if found_nucleus[i_bin]==0:
            
            found_nucleus[i_bin]=1

            op.td_mat('nuc_sign_'+str(i_bin),1.0,1.0,1.0,
                      prefix='crust_',
                      txt='latex:('+str(Zi)+','+str(Ni)+')',
                      resize=True,ds=False)
            op.td_pgram(xt,yt+0.1,zt,
                        xt,yt+0.1,zt+0.1,
                        xt,yt+0.2,zt,
                        mat='nuc_sign_'+str(k),match_txt=True)
            
            print('Adding nucleus, Z',Zi,'N',Ni,'for bin',i_bin)
            for k in range(0,Ni):
                rshift=random.random()*rnuc*cf*r_fudge
                ctshift=random.random()*2-1
                tshift=numpy.arcsin(ctshift)
                pshift=random.random()*2.0*numpy.pi
                xshift=rshift*numpy.cos(pshift)*numpy.sin(tshift)
                yshift=rshift*numpy.sin(pshift)*numpy.sin(tshift)
                zshift=rshift*numpy.cos(tshift)
                if k<2:
                    print('ct,r,t,p: %6.5e %6.5e %6.5e %6.5e' %
                          (ctshift,rshift,tshift,pshift))
                    print('rshift,rnuc,rnucl: %6.5e %6.5e %6.5e' %
                          (rshift,rnuc,r_nucleon))
                    print('x,y,z,x2,y2,z2: %6.5e %6.5e %6.5e %6.5e %6.5e %6.5e' %
                          (xt,yt,zt,xshift,yshift,zshift))
                    #quit()
                op.td_icos([xt+xshift,yt+xshift,zt+zshift],
                           r=r_nucleon*cf*r_fudge,mat='mat_blue',
                           name='icos_'+str(i),n_subdiv=1)
            for k in range(0,Zi):
                rshift=random.random()*rnuc*cf*r_fudge
                ctshift=random.random()*2-1
                tshift=numpy.arcsin(ctshift)
                pshift=random.random()*2.0*numpy.pi
                xshift=rshift*numpy.cos(pshift)*numpy.sin(tshift)
                yshift=rshift*numpy.sin(pshift)*numpy.sin(tshift)
                zshift=rshift*numpy.cos(tshift)
                op.td_icos([xt+xshift,yt+xshift,zt+zshift],
                           r=r_nucleon*cf*r_fudge,mat='mat_red',
                           name='icos_'+str(i),n_subdiv=1)

        else:
            
            op.td_icos([xt,yt,zt],r=rnuc*cf*r_fudge,mat=mat_name,
                       name='icos_'+str(i),n_subdiv=1)
            
        if i<100:
            print('nuc %5.4e %5.4e %5.4e %5.4e %5.4e %5.4e' %
                  (xt,yt,zt,rnuc*cf,Zt,Nt))
                
        Nnuclei=Nnuclei+1

    else:

        op.td_icos([xt,yt,zt],r=r_nucleon*cf*r_fudge,mat='mat_blue',
                   name='icos_'+str(i),n_subdiv=1)
        if i<100:
            print('n   %5.4e %5.4e %5.4e %5.4e' % 
                  (xt,yt,zt,r_nucleon*cf))

    if i%1000==999:
        print('Completed particle',i+1,' of ',N_part)
            
print('Minimum x coordinate:',xmin)
print('Maximum neutron number:',Nmax)
print('Number of nuclei:',Nnuclei)

# This section may need to be modified if the initial settings
# are changed

width=0.33
height=0.33

sign_array=[
    ['first.png',5.0],
    ['ns.png',4.2],
    ['crust.png',3.4],
    ['nuclei.png',2.6],
    ['scale.png',1.8],
    ['electrons.png',1.0],
    ['e9.png',0.2],
    ['e12.png',10.0]
]

for k in range(0,len(sign_array)):    
    op.td_mat('sign_'+str(k),1.0,1.0,1.0,prefix='crust_',
              txt=sign_array[k][0],resize=True,ds=False)
    op.td_pgram(sign_array[k][1]-width/2.0,0.0,0.5-height/2.0,
                sign_array[k][1]+width/2.0,0.0,0.5-height/2.0,
                sign_array[k][1]-width/2.0,0.0,0.5+height/2.0,
                mat='sign_'+str(k),match_txt=True)

# 

op.to.write_gltf(op.td_wdir,'crust',zip_file='crust.zip')        

