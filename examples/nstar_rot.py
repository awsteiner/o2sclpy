# # Rotating neutron star example for O$_2$sclpy

# For the underlying C++ code, see the O$_2$scl documentation at https://awsteiner.org/code/o2scl/html. The Python wrapper, O$_2$sclpy, is documentated at https://awsteiner.org/code/o2sclpy. This rotating neutron star code is a Python wrapper to a C++ version which was based on the original RNS code developed by Stergioulas and Morsink. See https://awsteiner.org/code/o2scl/html/class/nstar_rot.html.

# Imports
import o2sclpy
import matplotlib.pyplot as plot
import numpy
import sys

# +
plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Get a copy (a pointer to) the O$_2$scl unit conversion object, which
# also allows access to the constant library
o2scl_settings=o2sclpy.lib_settings_class()
cu=o2scl_settings.get_convert_units()

# Set up an EOS designed with the original RNS code (see
# https://awsteiner.org/code/o2scl/html/class/eos_nstar_rot_C.html)
eC=o2sclpy.eos_nstar_rot_C()
eC.set(True)

# Create the rotating neutron star object and set the EOS
nr=o2sclpy.nstar_rot()
nr.verbose=1
nr.set_eos(eC)

# Compute a configuration with a fixed central energy density and
# a fixed axis ratio
nr.fix_cent_eden_axis_rat(2.0e15,0.59)

# Obtain the output as a table3d object. See
# https://awsteiner.org/code/o2scl/html/class/table3d.html.
t3d=o2sclpy.table3d()
nr.output_table(t3d)

# Output the slice names: ed, pr, h, vsq, rho, gamma, omega, alpha.
# Each of these slices is a two-dimensional array of numbers.
for i in range(0,t3d.get_nslices()):
    print(i,t3d.get_slice_name(i))

# Print out the gravitational mass
print('Mass: %7.6e' % (nr.Mass/nr.MSUN))

# Take the log carefully so we can plot
t3d.function_slice('if(pr>1.0e-12,log10(pr),-12.0)','log10_pr')

# Plot the pressure in the internal coordinate system
if plots:
    pb=o2sclpy.plot_base()
    pb.colbar=True
    pb.den_plot([t3d,'log10_pr'])
    pb.save('nr1.png')
    plot.close()
    
# Create a new table for the output in Cartesian coordinates
# +
t3db=o2sclpy.table3d()
t3db.set_interp_type(o2sclpy.itp_linear)
rad_eq=nr.R_e/1.0e5
coord_grid=o2sclpy.uniform_grid_end.init(0.01,rad_eq*1.1,100)
t3db.set_xy_grid('x',coord_grid,'z',coord_grid)
t3db.line_of_names('ed pr')
# -

# Interpolate into Cartesian coordinates
# +
for i in range(0,t3db.get_nx()):
    for j in range(0,t3db.get_ny()):
        r=numpy.sqrt(coord_grid[i]**2+coord_grid[j]**2)
        theta=numpy.atan(-coord_grid[j]/coord_grid[i])+numpy.pi/2.0
        t3db.set(i,j,'ed',t3d.interp(r/(r+rad_eq),
                                     numpy.cos(theta),'ed'))
        t3db.set(i,j,'pr',t3d.interp(r/(r+rad_eq),
                                     numpy.cos(theta),'pr'))
# -
    
# Take the log carefully so we can plot
t3db.function_slice('if(pr>1.0e-5,log10(pr),-5.0)','log10_pr')

# Plot the rotating star
if plots:
    pb=o2sclpy.plot_base()
    pb.fig_dict='dpi=250'
    pb.colbar=True
    pb.den_plot([t3db,'log10_pr'])
    pb.save('nr2.png')
    plot.close()
    
# Set up the EOS
    
a=13
alpha=0.49
S=32
L=44
b=S-16-a
beta=(L-3*a*alpha)/b/3
n0=0.16
print('b,beta:',b,beta)

tab=o2sclpy.table_units()
tab.line_of_names('nb ed pr')
tab.line_of_units('1/fm^3 1/fm^4 1/fm^4')
tab.set_nlines(25)
for i in range(0,25):
    print('i',i)
    nb=0.08+i*0.01
    tab.set('nb',i,nb)
    tab.set('ed',i,939.0/197.33*nb+(nb*a*(nb/n0)**alpha+
                                    nb*b*(nb/n0)**beta)/197.33)
    tab.set('pr',i,(n0*a*alpha*(nb/n0)**(1.0+alpha)+
                    n0*b*beta*(nb/n0)**(1.0+beta))/197.33)
    
ed32=tab.get('ed',tab.get_nlines()-1)
pr32=tab.get('pr',tab.get_nlines()-1)

n1=0.8
coeff1=pr32/ed32**(1.0+1.0/n1)
p1=o2sclpy.eos_tov_polytrope()
p1.set_coeff_index(coeff1,n1)
p1.set_baryon_density(0.32,ed32)

nbtrans=0.64

for i in range(1,33):
    nb=0.32+i*(nbtrans-0.32)/32
    tab.line_of_data([nb,p1.ed_from_nb(nb),p1.pr_from_nb(nb)])
    
edlast=tab.get('ed',tab.get_nlines()-1)
prlast=tab.get('pr',tab.get_nlines()-1)

n2=0.7
coeff2=prlast/edlast**(1.0+1.0/n2)
p2=o2sclpy.eos_tov_polytrope()
p2.set_coeff_index(coeff2,n2)
p2.set_baryon_density(nbtrans,edlast)

for i in range(1,33):
    nb=nbtrans+i*(1.5-nbtrans)/32
    tab.line_of_data([nb,p2.ed_from_nb(nb),p2.pr_from_nb(nb)])
    
for i in range(0,tab.get_nlines()):
    print('%7.6e %7.6e %7.6e' % (tab.get('nb',i),tab.get('ed',i),
                                 tab.get('pr',i)))

eti=o2sclpy.eos_tov_interp()
eti.default_low_dens_eos()
eti.read_table(tab,'ed','pr','nb')
ts=o2sclpy.tov_solve()
ts.set_eos(eti)
ts.verbose=1
ts.mvsr()

# Delete table rows larger than the maximum mass
nonrot=ts.get_results()
prmax=nonrot.get('pr',nonrot.lookup('gm',nonrot.max('gm')))
nonrot.delete_rows_func('pr>'+str(prmax))

edmax=nonrot.max('ed')
print('edmax',edmax,nonrot.get_unit('ed'))
edmax2=cu.convert('Msun/km^3','1/fm^4',edmax)
print('edmax2',edmax2,'1/fm^4')
tab.deriv_col('ed','pr','cs2')
cs2_max=0
for i in range(0,tab.get_nlines()):
    print(i,tab.get('ed',i),edmax2,tab.get('cs2',i))
    if tab.get('ed',i)<edmax2 and tab.get('cs2',i)>cs2_max:
        cs2_max=tab.get('cs2',i)
print('cs2_max',cs2_max)

# The radius of a 1.4 solar mass neutron star
rad14=nonrot.interp('gm',1.4,'r')
print('rad14 %7.6e' % (rad14))

enri=o2sclpy.eos_nstar_rot_interp()
edv=o2sclpy.std_vector()    
prv=o2sclpy.std_vector()    
nbv=o2sclpy.std_vector()
for i in range(0,tab.get_nlines()):
    edv.push_back(tab.get('ed',i))
    prv.push_back(tab.get('pr',i))
    nbv.push_back(tab.get('nb',i))
enri.set_eos_fm(tab.get_nlines(),edv,prv,nbv)
    
# Construct a configuration with a specified central energy density
# and axis ratio
    
nr=o2sclpy.nstar_rot()
nr.verbose=1
nr.set_eos(enri)
nr.fix_cent_eden_axis_rat(2.0e15,0.59)

print('Mass: %7.6e' % (nr.Mass/nr.MSUN))
    
