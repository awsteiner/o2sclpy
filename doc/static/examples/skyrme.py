import o2sclpy

l=o2sclpy.linker()
l.link_o2scl_o2graph(True,True)

# Create neutron and proton
neut=o2sclpy.fermion(l.o2scl_part)
neut.g=2.0
neut.m=939.6/197.33

prot=o2sclpy.fermion(l.o2scl_part)
prot.g=2.0
prot.m=938.4/197.33

# Create the Skyrme object
sk=o2sclpy.eos_had_skyrme(l.o2scl_eos)
o2sclpy.skyrme_load(l.o2scl_eos,sk,'NRAPR',False,2)
sk.saturation()
print('NRAPR: n0=%7.6e 1/fm^3, E/A=%7.6e MeV' % (sk.n0,sk.eoa*197.33))

# Create the nstar_cold object for automatically computing the
# beta-equilibrium EOS and solving the TOV equations.
nc=o2sclpy.nstar_cold(l.o2scl_eos)
nc.set_eos(sk)
ret1=nc.calc_eos(0.01)
#eos_table=nc.get_eos_results()
#ret2=nc.calc_nstar()
#mvsr_table=nc.get_tov_results()



