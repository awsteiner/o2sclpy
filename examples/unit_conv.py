# # Unit conversion example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://awsteiner.org/code/o2sclpy for more information.

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

# Get a copy (a pointer to) the O$_2$scl unit conversion object:

o2scl_settings=o2sclpy.lib_settings_class()
cu=o2scl_settings.get_convert_units()

# By default, conversions are allowed to presume that $\hbar=c=k_B=1$.
# This code converts 2 $\mathrm{MeV}$ to $1/\mathrm{fm}$:

val=cu.convert('MeV','1/fm',2.0)
print('Conversion from MeV to 1/fm: %7.6e' % val)

# Add a new unit, a Bethe, defined to be $ 10^{51}~\mathrm{erg} $

cu.add_unit(b'Bethe',cu.convert('erg','kg*m^2/s^2',1.0e51),
            b'fifty one ergs',2,1,-2)

# Now use the new unit conversion

print(cu.convert('erg','Bethe',3.0e53))

# Unicode is supported. Set a unit named α to refer to 3 Newtons per Kelvin

cu.add_unit('α',3.0,'alpha unit',1,1,-2,-1)

# Print current unit table

cu.print_units_cout()

# Show that our unit named α works

print(cu.convert('N/K','α',27))

# Now, remove the use of natural units

cu.set_natural_units(False,False,False)





