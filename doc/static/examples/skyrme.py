import o2sclpy

link=o2sclpy.linker()
link.link_o2scl_o2graph(True,True)

fc=o2sclpy.find_constants(link)
hc=fc.find_unique('hbarc','MeV*fm')
print('hbarc = %7.6e' % (hc))

# Create neutron and proton
neut=o2sclpy.fermion(link)
neut.g=2.0
#neut.m=fc.find_unique('massmeutron','g')/hc
neut.m=939.6/hc

prot=o2sclpy.fermion(link)
prot.g=2.0
prot.m=938.4/hc

# Create the Skyrme object
sk=o2sclpy.eos_had_skyrme(link)
o2sclpy.skyrme_load(link,sk,'NRAPR',False,2)
sk.saturation()
print('NRAPR: n0=%7.6e 1/fm^3, E/A=%7.6e MeV' % (sk.n0,sk.eoa*hc))

# Create the nstar_cold object for automatically computing the
# beta-equilibrium EOS and solving the TOV equations.
nc=o2sclpy.nstar_cold(link)
nc.set_eos(sk)
ret1=nc.calc_eos(0.01)
eos_table=nc.get_eos_results()
arr=eos_table['nb']
arr2=eos_table['ed']
print(type(eos_table))
ret2=nc.calc_nstar()
mvsr_table=nc.get_tov_results()

