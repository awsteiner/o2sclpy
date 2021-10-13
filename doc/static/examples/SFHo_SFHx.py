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

#xarr=[i*0.02+0.02 for i in range(0,16)]
#for T in numpy.arange(0,20,5):
#    sfho.calc_

def test_fun():
    assert numpy.allclose(sfho.n0,0.1582415,rtol=1.0e-4)
    assert numpy.allclose(sfhx.n0,0.1600292,rtol=1.0e-4)
    return


