# # Crust variation example for O$_2$sclpy

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

ret1=nc.calc_eos(0.01)

# Create the object which interpolates the EOS for the TOV
# solver. Use the default crust EOS.

eti=o2sclpy.eos_tov_interp(link)
eti.default_low_dens_eos()
eti.read_table(tab,'ed','pr','nb')

# Specify the EOS and determine the M-R curve

ts=o2sclpy.tov_solve(link)
ts.set_eos(eti)
ts.mvsr()

print(ts.get_tov_results().max('gm'))

eti.gcp10_low_dens_eos()

print(ts.get_tov_results().max('gm'))

eti.s12_low_dens_eos()

print(ts.get_tov_results().max('gm'))


# For testing using ``pytest``:

def test_fun():
    assert numpy.allclose(Lambda,297.0,rtol=8.0e-3)
    return
