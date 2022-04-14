# # DSH example for O$_2$sclpy

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
ħc=fc.find_unique('ħc','MeV*fm')
print('ħc = %7.6e\n' % (ħc))

# Get a copy (a pointer to) the O$_2$scl unit conversion object:

cu=link.o2scl_settings.get_convert_units()

# Use the cloud_file object to download the EOS

cf=o2sclpy.cloud_file(link)
cf.verbose=1
cf.get_file('dsh.o2','https://isospin.roam.utk.edu/public_data'+
            '/eos_tables/du21/fid_3_5_22.o2')

# Read the tensor which stores the average mass number

hf=o2sclpy.hdf_file(link)
tg_A=o2sclpy.tensor_grid(link)
hf.open('dsh.o2')
o2sclpy.hdf_input_tensor_grid(link,hf,tg_A,'A')
hf.close()

# Create a table3d object for Ye=0.4

t3d=o2sclpy.table3d(link)
tg_A.to_table3d()

# Now plot the results. Raw matplotlib works, but o2sclpy has
# a couple functions which make it easier. 
       
if plots:
    pl=o2sclpy.plotter()
    pl.colbar=True
    pl.xtitle(u'$ n_B~(\mathrm{fm}^{-3}) $')
    pl.ytitle(u'$ T~(\mathrm{MeV}) $')
    pl.ttext(1.25,0.5,u'$ E/A~(\mathrm{MeV}) $',rotation=90)
    pl.den_plot_direct(t3d,'EoA')
    plot.show()

# For testing purposes
    
def test_fun():
    assert numpy.allclose(sfho.n0,0.1582415,rtol=1.0e-4)
    assert numpy.allclose(sfhx.n0,0.1600292,rtol=1.0e-4)
    return


