# # O$_2$scl table example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://awsteiner.org/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import sys

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

r6=tov_tab.interp('nb',eos_tab.interp('rho',1.0e10,'nb'),'r')
r14=tov_tab.interp('nb',eos_tab.interp('rho',1.0e14,'nb'),'r')

r_scale=15
N_bins=20

ug_r=o2sclpy.uniform_grid_end.init(link,0,(r6-r14)*r_scale,N_bins)

r_rep=[]
nb_rep=[]
rho_rep=[]
nn_rep=[]
nnuc_rep=[]
Z_rep=[]
N_rep=[]

for j in range(0,N_bins):
    rad=r6-(ug_r[j]+ug_r[j+1])/2.0/r_scale
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

h=o2sclpy.hist(link)
h.set_bin_edges_grid(ug_r)
for j in range(0,h.size()):
    h.set_wgt_i(j,nn_rep[j]+nnuc_rep[j])
    print(j,r_rep[j],h[j])
    
pdh=o2sclpy.prob_dens_hist(link)
pdh.init(h)

xy_scale=1.0

M=100
for i in range(0,M):
    print(pdh.sample())
