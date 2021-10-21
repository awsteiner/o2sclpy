# # Unit conversion example for O$_2$sclpy

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

# Get a copy (a pointer to) the O$_2$scl unit conversion object:

cu=link.o2scl_settings.get_convert_units()

# By default, conversions are allowed to presume that $\hbar=c=k_B=1$. This code converts 2 $\mathrm{MeV}$ to $1/\mathrm{fm}$:

val=cu.convert('MeV','1/fm',2.0)
print('%7.6e' % val)

unit=o2sclpy.convert_units_der_unit(link)

unit.set(b'Bethe',cu.convert('erg','kg*m^2/s^2',1.0e51),b'fifty one ergs',2,1,-2)

print(unit.val,unit.name.to_bytes(),unit.label.to_bytes())

#cu.add_unit_internal(unit)
cu.add_unit(b'Bethe',cu.convert('erg','kg*m^2/s^2',1.0e51),
            b'fifty one ergs',2,1,-2)

print(unit.val,unit.name.to_bytes(),unit.label.to_bytes())

cu.print_units_cout()


