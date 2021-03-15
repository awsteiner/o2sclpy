import o2sclpy

link=o2sclpy.linker()
link.link_o2scl(True)

# Create a fermion with spin 2, mass 1.1, and chemical potential 2.0
# Mass, chemical potential, and temperature have the same units.
f=o2sclpy.fermion(link)
f.g=2.0
f.m=1.1
f.mu=2.0

# Create an object with handles the thermodynamics of
# relativistic fermions
fr=o2sclpy.fermion_rel(link)

# Compute the number density, energy density, pressure, and entropy
# density at a temperature of T=1. Number density has units of mass^3,
# energy density and pressure is mass^4 and entropy density pressure
# is mass^3.
fr.calc_mu(f,1.0)
print('n=%7.6e, ed=%7.6e, pr=%7.6e, en=%7.6e' % (f.n,f.ed,f.pr,f.en))

# Check the thermodynamic identity (should be zero)
print('ti=%7.6e' % (f.n*f.mu+1.0*f.en-f.pr-f.ed))
