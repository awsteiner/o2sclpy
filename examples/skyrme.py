# # Skyrme equation of state example for O$_2$sclpy

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

# Get the value of $\hbar c$ from an O$_2$scl find_constants object:

hc=cu.find_unique('hbarc','MeV*fm')
print('hbarc = %7.6e' % (hc))

# Create neutron and proton objects and set their spin degeneracy and
# masses. The O$_2$scl EOS classes expect these masses to be in units
# of inverse femtometers.

neut=o2sclpy.fermion(link)
neut.g=2.0
neut.m=cu.convert('g','1/fm',cu.find_unique('massneutron','g'))

prot=o2sclpy.fermion(link)
prot.g=2.0
prot.m=cu.convert('g','1/fm',cu.find_unique('massproton','g'))

# Create the Skyrme EOS object and load the NRAPR parameterization:

sk=o2sclpy.eos_had_skyrme(link)
o2sclpy.skyrme_load(link,sk,'NRAPR',False,0)

# Compute nuclear saturation and output the saturation density
# and binding energy:

sk.saturation()
print('NRAPR: n0=%7.6e 1/fm^3, E/A=%7.6e MeV' % (sk.n0,sk.eoa*hc))
print('')

# Create the nstar_cold object for automatically computing the
# beta-equilibrium EOS and solving the TOV equations:

nc=o2sclpy.nstar_cold(link)

# Let the nstar_cold object know we want to use the Skyrme NRAPR EOS:

nc.set_eos(sk)

# Compute the EOS

ret1=nc.calc_eos(0.01)

# Summarize the columns in the EOS table and their associated units.
# The strings returned by the C++ wrappers are bytes objects, so we
# need to convert them to strings to print them out.

eos_table=nc.get_eos_results()
print('EOS table:')
for i in range(0,eos_table.get_ncolumns()):
    col=eos_table.get_column_name(i)
    unit=eos_table.get_unit(col)
    print('Column',i,str(col,'UTF-8'),str(unit,'UTF-8'))
print('')

# Get the columns of the table as numpy arrays, and then plot the EOS.
# The first line requires a bit of explanation. The raw vectors stored
# in O$_2$scl table objects are often larger than the current table
# size so it can grow efficiently. Thus we truncate the vector so that
# it matches the current table size.

nb=eos_table['nb'][0:eos_table.get_nlines()]
print(type(nb))
ed=eos_table['ed'][0:eos_table.get_nlines()]
edhc=[ed[i]*hc for i in range(0,eos_table.get_nlines())]
plot.plot(nb,edhc)
plot.xlabel('baryon density (1/fm^3)')
plot.ylabel('energy density (MeV/fm^3)')
if plots:
    plot.show()

# Compute the M-R curve using the TOV equations. TOV solver
# automatically outputs some information to std::cout, and we use the
# cap_cout class to ensure that output goes here instead of the
# jupyter console.

cc=o2sclpy.cap_cout()
cc.open()
ret2=nc.calc_nstar()
cc.close()

# Get the table for the TOV results

tov_table=nc.get_tov_results()

# Summarize the columns in the TOV table and their associated units.

print('TOV table:')
for i in range(0,tov_table.get_ncolumns()):
    col=tov_table.get_column_name(i)
    unit=tov_table.get_unit(col)
    print('Column',i,str(col,'UTF-8'),str(unit,'UTF-8'))
print('')


plot.plot(tov_table['r'][0:tov_table.get_nlines()],
          tov_table['gm'][0:tov_table.get_nlines()])
plot.xlabel('radius (km)')
plot.ylabel('gravitational mass (Msun))')
if plots:
    plot.show()

# This line computes the profile of a 1.4 solar mass 
# neutron star. If you look at the console output you will
# notice that the maximum mass is computed first. This
# helps ensure the class doesn't give the profile of an
# unstable configuration.

ret2=nc.fixed(1.4)

plot.plot(tov_table['r'][0:tov_table.get_nlines()],
          tov_table['gm'][0:tov_table.get_nlines()])
plot.xlabel('radius (km)')
plot.ylabel('gravitational mass (Msun))')
if plots:
    plot.show()

# Create a O$_2$scl ``tov_love`` object to compute the tidal
# deformability of a 1.4 solar mass neutron star.

tl=o2sclpy.tov_love(link)

# The ``tov_love`` class requires the energy density and pressure to
# be in units of $ \mathrm{M}_{\odot}/\mathrm{km}^3 $, so we convert
# those columns in the table

tov_table.convert_to_unit('ed','Msun/km^3',True)
tov_table.convert_to_unit('pr','Msun/km^3',True)

# The ``tov_love`` class also requires the speed of sound, so we
# compute it using interpolation.

tov_table.deriv_col('ed','pr','cs2')

# Provide the TOV table to the ``tov_love`` object and compute the
# tidal deformability in units of $\mathrm{km}^{-5}$:

# +
tl.set_tab(tov_table)
(ret,yR,beta,k2,lambda_km5,lambda_cgs)=tl.calc_y(False)

print('%7.6e' % lambda_km5)
# -

# To get the dimensionless tidal deformability we divide by $(G M)^5$:

twoG=cu.find_unique('schwarz','m')/1.0e3
Lambda=lambda_km5/(1.4*twoG/2.0)**5
print('%7.6e' % Lambda)

# For testing using ``pytest``:

def test_fun():
    assert numpy.allclose(Lambda,297.0,rtol=8.0e-3)
    return
