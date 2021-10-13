# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import o2sclpy
import matplotlib.pyplot as plot

link=o2sclpy.linker()
link.link_o2scl()

hf=o2sclpy.hdf_file(link)

hf.open(link.o2scl_settings.get_data_dir()+b'apr98.o2',False,True)

tab=o2sclpy.table(link)

name=b''

o2sclpy.hdf_input_table(link,hf,tab,name)

cc=o2sclpy.cap_cout()
cc.open()
tab.summary()
cc.close()

plot.plot(tab['rho'],tab['nuc'])
plot.plot(tab['rho'],tab['neut'])
plot.show()


