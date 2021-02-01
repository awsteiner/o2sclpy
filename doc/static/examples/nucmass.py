import o2sclpy

link=o2sclpy.linker()
link.link_o2scl_o2graph(True)

fc=o2sclpy.find_constants(link)
hc=fc.find_unique('hbarc','MeV*fm')
print('hbarc = %7.6e' % (hc))

# Instantiate and load the Atomic Mass Evaluation
ame=o2sclpy.nucmass_ame(link)
o2sclpy.ame_load(link,ame,'16',False)

# Print out the number of entries
print('Number of isotopes in the AME list:',ame.get_nentries())

# Get lead-208
nuc=o2sclpy.nucleus(link)
ame.get_nucleus(82,126,nuc)

# Output the binding energy per nucleon in MeV
print('Binding energy per nucleon in Pb-208 = %7.6e ' % (nuc.be/208*hc))
