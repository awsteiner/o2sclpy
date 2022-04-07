# # SFHo/SFHx example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://neutronstars.utk.edu/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import numpy
import sys

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Link the O$_2$scl library:

link=o2sclpy.linker()
link.link_o2scl()

# Get the value of $\hbar c$ from an O$_2$scl find_constants object:

fc=o2sclpy.find_constants(link)
hc=fc.find_unique('hbarc','MeV*fm')
print('hbarc = %7.6e' % (hc))

# Get a copy (a pointer to) the O$_2$scl unit conversion object:

cu=link.o2scl_settings.get_convert_units()

sfho=o2sclpy.eos_had_rmf(link)
o2sclpy.rmf_load(link,sfho,'SFHo')
sfhx=o2sclpy.eos_had_rmf(link)
o2sclpy.rmf_load(link,sfhx,'SFHx')

# Compute nuclear saturation and output the saturation density
# and binding energy:

sfho.saturation()
print(('SFHo: n0=%7.6e 1/fm^3, E/A=%7.6e MeV, K=%7.6e MeV, '+
       'M*/M=%7.6e, S=%7.6e MeV, L=%7.6e MeV') % 
      (sfho.n0,sfho.eoa*hc,sfho.comp*hc,sfho.msom,sfho.esym*hc,
       sfho.fesym_slope(sfho.n0)*hc))
print('')

sfhx.saturation()
print(('SFHx: n0=%7.6e 1/fm^3, E/A=%7.6e MeV, K=%7.6e MeV, '+
       'M*/M=%7.6e, S=%7.6e MeV, L=%7.6e MeV') % 
      (sfhx.n0,sfhx.eoa*hc,sfhx.comp*hc,sfhx.msom,sfhx.esym*hc,
       sfhx.fesym_slope(sfhx.n0)*hc))
print('')

# Baryon density grid in $1/\mathrm{fm}^3$. The O$_2$scl object
# `uniform_grid_end_width` is like numpy.arange() but is numerically
# stable.

ug_nb=o2sclpy.uniform_grid_end_width.init(link,0.01,1.0,0.01)

# Temperature grid in MeV

ug_T=o2sclpy.uniform_grid_end_width.init(link,0.1,10.0,0.1)

# Store the EOS in a table3d object

t3d=o2sclpy.table3d(link)
t3d.set_xy_grid('nB',ug_nb,'T',ug_T)

# Create a new slice for the energy per baryon

t3d.new_slice('EoA')

# AWS: I need to fix this to make sure get_def_neutron and
# get_def_proton() get a reference rather than a copy

n=o2sclpy.fermion(link)
n2=o2sclpy.fermion(link)
sfho.get_def_neutron(n)
sfho.get_def_neutron(n2)
print(n._ptr,n._owner)
print(n2._ptr,n2._owner)
#p=sfho.get_def_proton()
th=sfho.get_def_thermo()

for i in range(0,t3d.get_nx()):
   for j in range(0,t3d.get_ny()):
       #n.n=ug_nb[i]/2.0
       #p.n=ug_nb[i]/2.0
       #sfho.calc_temp_e(n,p,ug_T[j]/197.33,th)
       #t3d.set(i,j,'EoA',th.ed/ug_nb[i])

if plots:
    plot.den_plot(t3d,'EoA')
    plot.show()
    
# +
#xarr=[i*0.02+0.02 for i in range(0,16)]
#for T in numpy.arange(0,20,5):
#   sfho.calc_
# -

def test_fun():
    assert numpy.allclose(sfho.n0,0.1582415,rtol=1.0e-4)
    assert numpy.allclose(sfhx.n0,0.1600292,rtol=1.0e-4)
    return


