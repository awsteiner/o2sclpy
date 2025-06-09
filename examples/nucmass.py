import o2sclpy
import numpy

link=o2sclpy.linker()
link.link_o2scl()

# Get a copy (a pointer to) the O$_2$scl unit conversion object, which
# also allows access to the constant library, then get ħc.

o2scl_settings=o2sclpy.lib_settings_class()
cu=o2scl_settings.get_convert_units()

hc=cu.find_unique('hbarc','MeV*fm')
print('hbarc = %7.6e' % (hc))

# Instantiate and load the Atomic Mass Evaluation
ame=o2sclpy.nucmass_ame()
ame.load('20')

# Print out the number of entries
print('Number of isotopes in the AME list:',ame.get_nentries())

# Get lead-208
nuc=o2sclpy.nucleus()
ame.get_nucleus(82,126,nuc)

# Output the binding energy per nucleon in MeV
print('Binding energy per nucleon in Pb-208 = %7.6e ' % (nuc.be/208*hc))

def test_fun():
    assert numpy.allclose(nuc.be/208*hc,-7.867,rtol=1.0e-3)
    return
