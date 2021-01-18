import o2sclpy

l=o2sclpy.linker()
l.get_library_settings()
l.link_o2scl_o2graph(True)

ame=o2sclpy.nucmass_ame(l.o2scl_part)

o2sclpy.ame_load(l.o2scl_part,ame,'16',False)

