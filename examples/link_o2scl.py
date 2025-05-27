# # O$_2$scl library linking example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://awsteiner.org/code/o2sclpy for more information.

import sys
print(sys.path)

# +
import o2sclpy
import sys

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# This code dynamically links the O$_2$scl library. Environment
# variables can be used to specify the location of various libraries
# which need to be added. These values can also be set directly in the
# linker class (and then they override the environment variables). See
# http://awsteiner.org/code/o2sclpy/link_cpp.html#linking-with-o2scl
# for more detail. We set the verbose parameter to 1 to output more
# information about which libraries are being linked.

# To test that the link worked, obtain the O$_2$scl version from the DLL:

o2scl_settings=o2sclpy.lib_settings_class()

print(o2scl_settings.o2scl_version())

def test_fun():
    assert o2scl_settings.o2scl_version()==b'0.931a2'
    return
