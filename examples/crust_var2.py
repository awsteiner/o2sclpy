# # Variation in the crust and core EOS 

import o2sclpy
import matplotlib.pyplot as plot
import ctypes
import numpy
import sys
import random

plots=True
if 'pytest' in sys.modules:
    plots=False

# A simple function which tests to ensure that the EOS is monotonic

def test_eos(ve,vp):
    for i in range(0,len(ve)-1):
        if ve[i]>=ve[i+1]:
            return False
        if vp[i]>=vp[i+1]:
            return False
    return True

# Link the O$_2$scl library:

link=o2sclpy.linker()
link.link_o2scl()

# The O$_2$scl unit conversion object

cu=link.o2scl_settings.get_convert_units()

# Create the object which interpolates the EOS for the TOV
# solver. Use the default crust EOS.

eti=o2sclpy.eos_tov_interp(link)

# Specify the EOS and determine the M-R curve

ts=o2sclpy.tov_solve(link)
ts.verbose=0
ts.set_eos(eti)

# Prepare the two-panel plot

pb=o2sclpy.plot_base()
pb.fig_dict='fig_size_x=9,fig_size_y=6'
pb.subplots(1,2)
plot.subplots_adjust(left=0.10,right=0.99,top=0.98,bottom=0.12,
                     wspace=0.20)
pb.selax('0')
pb.xtitle(r'$ \varepsilon~(\mathrm{MeV}/\mathrm{fm}^3) $')
pb.ytitle(r'$ P~(\mathrm{MeV}/\mathrm{km}^3) $')
pb.xlimits(0.1,2.0e2)
pb.ylimits(2.0e-4,1.0)
pb.selax('1')
pb.xtitle(r'$ \varepsilon~(\mathrm{MeV}/\mathrm{fm}^3) $')
pb.xlimits(0.1,3.0e3)
pb.ylimits(2.0e-4,2.0e3)

# Core EOS from the 2021 PRL, first we download the file
# (if it's not already stored locally).

cf=o2sclpy.cloud_file(link)
cf.verbose=1
cf.get_file('a21_all_IS_threep_8.o2',
            ('https://isospin.roam.utk.edu/public_data/almamun21/'+
             '3P_GW_all_IS/is_threep_8_out'))

# Now we read the results table and the fixed energy density grid from
# the HDF5 file

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
                   int(a21_tab.get_nlines()/100)):

    # Get the EOS from the specified row of the table
    
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
    
        # Get a random crust and load the EOS in the eos_tov object

        L=random.random()*80+30
        eti.read_table(a21_eos,'ed','pr')
        eti.ngl13_low_dens_eos(L)
        ve=eti.get_full_vece()
        vp=eti.get_full_vecp()
        
        # Test EOS
        
        if test_eos(ve,vp):

            # Plot EOS
            
            pb.selax('0')
            ve2=[cu.convert('Msun/km^3','MeV/fm^3',ve[i]) for
                 i in range(0,len(ve))]
            vp2=[cu.convert('Msun/km^3','MeV/fm^3',vp[i]) for
                 i in range(0,len(vp))]
            pb.axes.loglog(ve2,vp2)
            pb.selax('1')
            pb.axes.loglog(ve2,vp2)

            # Get M-R curve and maximum mass
            
            ts.mvsr()
        
            print('A21 row %6d, NGL 13 crust, L: %4.3e, M_max: %7.6e' %
                  (i_eos,L,ts.get_results().max('gm')))

# Show all the EOSs

plot.savefig('crust_var2.png')
plot.show()

# For testing using ``pytest``:

def test_fun():
    assert 0==0
    return
