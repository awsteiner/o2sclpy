# # O$_2$scl library linking example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://awsteiner.org/code/o2sclpy for more information.

# +
import sys
import o2sclpy

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Importing ``o2sclpy'' automatically links the O$_2$scl library.
# Environment variables can be used to specify the location of various
# libraries which need to be added. See
# http://awsteiner.org/code/o2sclpy/link_cpp.html#linking-with-o2scl
# for more detail.

# To print the DLL handle obtain on import

print('O₂scl library DLL:',o2sclpy.doc_data.top_linker.o2scl)

# Obtain the O$_2$scl version from the DLL:

o2scl_settings=o2sclpy.lib_settings_class()

print('O₂scl library version',o2scl_settings.o2scl_version())

def test_fun():
    assert o2scl_settings.o2scl_version()==b'0.931'
    return
