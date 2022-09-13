# # Crust variation example for O$_2$sclpy

# See the O$_2$sclpy documentation at https://neutronstars.utk.edu/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import ctypes
import numpy
import sys

def test_eos(eti):
    ve=eti.get_full_vece()
    vp=eti.get_full_vecp()
    vnb=eti.get_full_vecnb()
    for i in range(0,len(ve)-1):
        assert ve[i]<ve[i+1]
        assert vp[i]<vp[i+1]
        assert vnb[i]<vnb[i+1]
    return

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

pb=o2sclpy.plot_base()
pb.fig_dict='left_margin=0.16'
pb.canvas()
pb.xtitle(r'$ \varepsilon~(\mathrm{M}_{\odot}/\mathrm{km}^3) $')
pb.ytitle(r'$ P~(\mathrm{M}_{\odot}/\mathrm{km}^3) $')
pb.xlimits(3.0e-8,3.0e-4)
pb.ylimits(3.0e-11,1.0e-5)
import matplotlib.pyplot as plot

print('Default: %7.6e' % ts.get_results().max('gm'))

eti.gcp10_low_dens_eos()
test_eos(eti)
plot.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('GCP10 %7.6e' % ts.get_results().max('gm'))

eti.sho11_low_dens_eos()
test_eos(eti)
plot.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('SHO11 %7.6e' % ts.get_results().max('gm'))

#eti.s12_low_dens_eos('Rs')
#test_eos(eti)
#plot.loglog(eti.get_full_vece(),eti.get_full_vecp())
#ts.mvsr()

#print('S12 Rs %7.6e' % ts.get_results().max('gm'))

eti.s12_low_dens_eos()
test_eos(eti)
plot.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('S12 SLy4 %7.6e' % ts.get_results().max('gm'))

eti.ngl13_low_dens_eos(80.0)
test_eos(eti)
plot.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('NGL13 L=80 %7.6e' % ts.get_results().max('gm'))

eti.ngl13_low_dens_eos2(34.0,80.0,0.08)
test_eos(eti)
plot.loglog(eti.get_full_vece(),eti.get_full_vecp())
ts.mvsr()

print('NGL13(2) S=34 L=80 0.08 %7.6e' % ts.get_results().max('gm'))

pb.show()

# For testing using ``pytest``:

def test_fun():
    assert 0==0
    return
