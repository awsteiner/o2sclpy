import o2sclpy

# Link the O2scl library
link=o2sclpy.linker()
link.link_o2scl_o2graph(True,True)

# Get the value of hbar*c from an o2scl find_constants object
fc=o2sclpy.find_constants(link)
hc=fc.find_unique('hbarc','MeV*fm')
print('hbarc = %7.6e' % (hc))

# Get a copy (a pointer to) the O2scl unit conversion object
cu=link.o2scl_settings.get_convert_units()

# Create neutron and proton objects and set their spin degeneracy and
# masses. The masses are expected to be in units of inverse
# femtometers.
neut=o2sclpy.fermion(link)
neut.g=2.0
neut.m=cu.convert('g','1/fm',fc.find_unique('massneutron','g'))

prot=o2sclpy.fermion(link)
prot.g=2.0
prot.m=cu.convert('g','1/fm',fc.find_unique('massproton','g'))

# Create the Skyrme object and load the NRAPR parameterization
sk=o2sclpy.eos_had_skyrme(link)
o2sclpy.skyrme_load(link,sk,'NRAPR',False,0)

# Compute nuclear saturation and output the saturation density
# and binding energy
sk.saturation()
print('NRAPR: n0=%7.6e 1/fm^3, E/A=%7.6e MeV' % (sk.n0,sk.eoa*hc))
print('')

# Create the nstar_cold object for automatically computing the
# beta-equilibrium EOS and solving the TOV equations.
nc=o2sclpy.nstar_cold(link)

# Let the nstar_cold object know we want to use the NRAPR EOS
nc.set_eos(sk)

# Compute the EOS
ret1=nc.calc_eos(0.01)

# Summarize the columns in the EOS table
eos_table=nc.get_eos_results()
print('EOS table:')
for i in range(0,eos_table.get_ncolumns()):
    col=eos_table.get_column_name(i)
    unit=eos_table.get_unit(col)
    print('Column',i,str(col,'UTF-8'),str(unit,'UTF-8'))
print('')

# Compute the M-R curve using the TOV equations
ret2=nc.calc_nstar()

# Get the table for the TOV results
tov_table=nc.get_tov_results()
print('')

# Summarize the columns in the TOV table
print('TOV table:')
for i in range(0,tov_table.get_ncolumns()):
    col=tov_table.get_column_name(i)
    unit=tov_table.get_unit(col)
    print('Column',i,str(col,'UTF-8'),str(unit,'UTF-8'))
print('')

