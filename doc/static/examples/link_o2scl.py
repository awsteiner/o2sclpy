# # O$_2$scl library linking example for O$_2$sclpy

# See the O$_2$sclpy documentation at
# https://neutronstars.utk.edu/code/o2sclpy for more information.

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
# http://neutronstars.utk.edu/code/o2sclpy/link_cpp.html#linking-with-o2scl
# for more detail. We set the verbose parameter to 1 to output more
# information about which libraries are being linked.

link=o2sclpy.linker()
link.verbose=1
link.link_o2scl()

# To test that the link worked, obtain the O$_2$scl version from the DLL:

print(link.o2scl_settings.o2scl_version())

# The linker class also has some documentation which may be helpful:

help(o2sclpy.linker)

def test_fun():
    assert link.o2scl_settings.o2scl_version()=='0.927a1'
    return
