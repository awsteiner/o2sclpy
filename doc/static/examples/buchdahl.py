# # Buchdahl equation of state example for O$_2$sclpy

# See the O$_2$sclpy documentation at https://neutronstars.utk.edu/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import ctypes
import numpy
import sys

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Link the O$_2$scl library:

link=o2sclpy.linker()
link.link_o2scl()

# Get a copy (a pointer to) the O$_2$scl unit conversion object:

cu=link.o2scl_settings.get_convert_units()

# Create the Buchdahl EOS object

b=o2sclpy.eos_tov_buchdahl(link)

# Create the TOV solve object, set the EOS and compute the M-R curve

ts=o2sclpy.tov_solve(link)
ts.set_eos(b);
ts.fixed(1.4,1.0e-4)
print('Exact radius is %7.6e, computed radius is %7.6e.' %
      (b.rad_from_gm(1.4),ts.rad))
print('Relative difference %7.6e.' %
      (abs(b.rad_from_gm(1.4)-ts.rad)/ts.rad))

# Get the table for the TOV results

tov_table=ts.get_results()

if plots:
    pl=o2sclpy.plotter()
    pl.canvas()
    plot.plot(tov_table['r'][0:tov_table.get_nlines()],
              tov_table['gm'][0:tov_table.get_nlines()])
    pl.xtitle('radius (km)')
    pl.ytitle('gravitational mass (Msun)')
    plot.show()

    plot.clf()
    o2sclpy.default_plot()
    plot.plot(tov_table['r'][0:tov_table.get_nlines()],
              tov_table['gm'][0:tov_table.get_nlines()])
    pl.xtitle('radius (km)')
    pl.ytitle('gravitational mass (Msun)')
    plot.show()
    
# For testing using ``pytest``:

def test_fun():
    assert numpy.allclose(Lambda,297.0,rtol=8.0e-3)
    return
