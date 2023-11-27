# # Crust variation example for O$_2$sclpy

# See the O$_2$sclpy documentation at https://neutronstars.utk.edu/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import ctypes
import numpy
import sys
import random

plots=True
if 'pytest' in sys.modules:
    plots=False
# -    

# A simple function which tests to ensure that the EOS is monotonic

def test_eos(eti):
    ve=eti.get_full_vece()
    vp=eti.get_full_vecp()
    vnb=eti.get_full_vecnb()
    for i in range(0,len(ve)-1):
        if ve[i]>=ve[i+1]:
            return False
        if vp[i]>=vp[i+1]:
            return False
        if vnb[i]>=vnb[i+1]:
            return False
    return True

# Link the O$_2$scl library:

link=o2sclpy.linker()
link.link_o2scl()

# Get a copy (a pointer to) the O$_2$scl unit conversion object,
# which also allows access to the constant library

cu=link.o2scl_settings.get_convert_units()

# Create the Skyrme EOS object and load the NRAPR parameterization:

sk=o2sclpy.eos_had_skyrme(link)
o2sclpy.skyrme_load(link,sk,'NRAPR',False,0)

# Create the nstar_cold object for automatically computing the
# beta-equilibrium EOS and solving the TOV equations:

nc=o2sclpy.nstar_cold(link)

# Let the nstar_cold object know we want to use the Skyrme NRAPR EOS:

nc.set_eos(sk)

# Compute the EOS

eos_ret=nc.calc_eos(0.01)
assert eos_ret==0
tab=nc.get_eos_results()

# Create the object which interpolates the EOS for the TOV
# solver. Use the default crust EOS.

eti=o2sclpy.eos_tov_interp(link)
eti.default_low_dens_eos()
eti.read_table(tab,'ed','pr','nb')
test_eos(eti)

# Specify the EOS and determine the M-R curve

ts=nc.get_def_tov()
ts.verbose=0
ts.set_eos(eti)
ts.mvsr()

# For plotting

import matplotlib.pyplot as plot

pb=o2sclpy.plot_base()
pb.fig_dict='fig_size_x=9,fig_size_y=6'
pb.subplots(1,2)
plot.subplots_adjust(left=0.10,right=0.99,top=0.99,bottom=0.12,
                     wspace=0.20)
pb.selax('0')
pb.xtitle(r'$ \varepsilon~(\mathrm{M}_{\odot}/\mathrm{km}^3) $')
pb.ytitle(r'$ P~(\mathrm{M}_{\odot}/\mathrm{km}^3) $')
pb.xlimits(1.4e-7/2,1.4e-4)
pb.ylimits(2.3e-10/2,1.4e-6)
pb.selax('1')
pb.xtitle(r'$ \varepsilon~(\mathrm{M}_{\odot}/\mathrm{km}^3) $')
pb.xlimits(1.4e-7/2,5.0e-3)
pb.ylimits(2.3e-10/2,5.0e-3)

print('First demonstrate with NRAPR core and several crusts:\n')
print('NRAPR, default crust, M_max: %7.6e' % ts.get_results().max('gm'))

eti.gcp10_low_dens_eos()
test_eos(eti)
pb.selax('0')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
pb.selax('1')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('NRAPR, GCP10 crust, M_max: %7.6e' % ts.get_results().max('gm'))

eti.sho11_low_dens_eos()
test_eos(eti)
pb.selax('0')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
pb.selax('1')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('NRAPR, SHO11 crust, M_max: %7.6e' % ts.get_results().max('gm'))

eti.s12_low_dens_eos()
test_eos(eti)
pb.selax('0')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
pb.selax('1')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('NRAPR, S12 SLy4 crust, M_max: %7.6e' % ts.get_results().max('gm'))

eti.ngl13_low_dens_eos(80.0)
test_eos(eti)
pb.selax('0')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
pb.selax('1')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('NRAPR, NGL13 crust with L=80, M_max: %7.6e' %
      ts.get_results().max('gm'))

eti.ngl13_low_dens_eos2(34.0,80.0,0.08)
test_eos(eti)
pb.selax('0')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
pb.selax('1')
pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('NRAPR, NGL13 crust with S=34, L=80, n_t=0.08, M_max: %7.6e' %
      ts.get_results().max('gm'))

print('\nNow run with several core EOSs from MCMC output:\n')

# Now try an EOS from the 2021 PRL, first we download the file
# (if it's not already stored locally).

cf=o2sclpy.cloud_file(link)
cf.verbose=1
cf.get_file('a21_all_IS_threep_8.o2',
            ('https://isospin.roam.utk.edu/public_data/almamun21/'+
             '3P_GW_all_IS/is_threep_8_out'))

# Now we read the results table and the fixed energy density grid
# from the HDF5 file 

print('Reading the file. This takes a bit of time because',
      'it is a large file.')
hf=o2sclpy.hdf_file(link)
a21_tab=o2sclpy.table_units(link)
ug_ed=o2sclpy.uniform_grid(link)
hf.open('a21_all_IS_threep_8.o2')
o2sclpy.hdf_input_table(link,hf,a21_tab,'markov_chain_0')
o2sclpy.hdf_input_uniform_grid(link,hf,ug_ed,'e_grid')
hf.close()
print('Done reading the file. Table has',a21_tab.get_nlines(),'lines.')

# Convert the uniform_grid object to a numpy vector

ug_ed_v=o2sclpy.std_vector(link)
ug_ed.vector(ug_ed_v)
ug_ed_v=ug_ed_v.to_numpy()

# Loop over EOSs from the A21 table

for i_eos in range(0,a21_tab.get_nlines(),
                   int(a21_tab.get_nlines()/4)):

    # Get the first EOS, from row 0 of the table
    
    a21_eos=o2sclpy.table_units(link)
    a21_eos.line_of_names('ed pr')
    a21_eos.line_of_units('1/fm^4 1/fm^4')
    for i in range(0,100):
        Pi=a21_tab.get('P_'+str(i),i_eos)
        if Pi>0:
            a21_eos.line_of_data([ug_ed_v[i],Pi])

    if a21_eos.get_nlines()>50:
    
        # The maximum mass, as obtained by Mamun using bamr
    
        mmax=a21_tab.get('M_max',i_eos)
        print('Row %d, M_max: %7.6e' % (i_eos,mmax))
    
        # Load the EOS in the eos_tov object

        L=random.random()*80+30
        eti.ngl13_low_dens_eos(L)
        eti.read_table(a21_eos,'ed','pr')
        
        # Test and get M-R curve
        
        if test_eos(eti):
            pb.selax('0')
            pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
            pb.selax('1')
            pb.axes.loglog(eti.get_full_vece(),eti.get_full_vecp())
            ts.mvsr()
        
            print('A21 row %d, NGL 13 crust, L: %4.3e, M_max: %7.6e' %
                  (i_eos,L,ts.get_results().max('gm')))

# Show all the EOSs

pb.show()

# For testing using ``pytest``:

def test_fun():
    assert 0==0
    return
