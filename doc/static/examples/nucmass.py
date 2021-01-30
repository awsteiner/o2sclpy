import o2sclpy

l=o2sclpy.linker()
l.get_library_settings()
l.link_o2scl_o2graph(True)

fc=o2sclpy.find_constants(l.o2scl)
hc=fc.find_unique('hbarc','MeV*fm')
print(hc)

# Instantiate and load the Atomic Mass Evaluation
ame=o2sclpy.nucmass_ame(l.o2scl_part)
o2sclpy.ame_load(l.o2scl_part,ame,'16',False)

# Print out the number of entries
print(ame.get_nentries())

# Get lead-208
nuc=o2sclpy.nucleus(l.o2scl_part)
ame.get_nucleus(82,126,nuc)

# Output the binding energy per nucleon in MeV
print(nuc.be/208*197.33)
