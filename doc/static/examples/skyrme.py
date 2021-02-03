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
o2sclpy.skyrme_load(link,sk,'NRAPR',False,0)
sk.saturation()
print('NRAPR: n0=%7.6e 1/fm^3, E/A=%7.6e MeV' % (sk.n0,sk.eoa*hc))
print('')

# Create the nstar_cold object for automatically computing the
# beta-equilibrium EOS and solving the TOV equations.
nc=o2sclpy.nstar_cold(link)
nc.set_eos(sk)
ret1=nc.calc_eos(0.01)

eos_table=nc.get_eos_results()
print('EOS table:')
for i in range(0,eos_table.get_ncolumns()):
    col=eos_table.get_column_name(i)
    unit=eos_table.get_unit(col)
    print('Column',i,str(col,'UTF-8'),str(unit,'UTF-8'))
print('')
          
ret2=nc.calc_nstar()
tov_table=nc.get_tov_results()
print('')

print('TOV table:')
for i in range(0,tov_table.get_ncolumns()):
    col=tov_table.get_column_name(i)
    unit=tov_table.get_unit(col)
    print('Column',i,str(col,'UTF-8'),str(unit,'UTF-8'))
print('')

