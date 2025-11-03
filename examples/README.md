O2sclpy examples README file
============================

There are two kinds of examples in this directory: (i) command-line
scripts which demonstrate the use of o2graph, and (ii) Jupyter notebooks
and Python scripts which demonstrate the use of o2graph or O2sclpy's
Python interface to O2scl's C++ code.

o2graph example scripts
-----------------------

The current figure list along with the documentation file where they
are found (in the ../doc folder) is:

------------------------- ------------
cmaps.scr                 plot_ref.rst
colors_near.scr           plot_ref.rst
markers.scr               plot_ref.rst
------------------------- ------------
arrows.scr                o2graph.rst
backend.scr               o2graph.rst
cmap_den_plot.scr         o2graph.rst
kde_plot.scr              o2graph.rst
modax.scr                 o2graph.rst
obj_props.scr             o2graph.rst
subplots1.scr             o2graph.rst
subplots2.scr             o2graph.rst
subplots3.scr             o2graph.rst
table_errorbar.scr        o2graph.rst
table_plot_color.scr      o2graph.rst
table_plot.scr            o2graph.rst
table_plotv.scr           o2graph.rst
table_rplot.scr           o2graph.rst
table_scatter.scr         o2graph.rst
table3d_den_plot.scr      o2graph.rst
textbox.scr               o2graph.rst
------------------------- ------------
yt_scatter.scr            yt.rst
yt_tg_multvol.scr         yt.rst
------------------------- ------------
gltf_den_plot_col.scr     gltf.rst
gltf_scatter_col.scr      gltf.rst
bl_den_plot_yaw.scr       gltf.rst

The script 'backend.scr' does not generate any figures.

Python/Jupyter examples
-----------------------

bayes_nstar_rot.py buchdahl.ipynb buchdahl.py DSH.ipynb DSH.py
interpm.ipynb interpm.py link_o2scl.ipynb link_o2scl.py
nstar_rot.ipynb nstar_rot.py nucmass.ipynb nucmass.py plot_info.ipynb
SFHo_SFHx.ipynb SFHo_SFHx.py skyrme.ipynb skyrme.py table.ipynb
table.py tov.ipynb tov.py unit_conv.ipynb unit_conv.py

All of the Python scripts except bayes_nstar_rot.py and DSH.py are
tested when one runs "make test" or "make testq" in the root o2sclpy
directory. The Jupyter notebook "plot_info.ipynb" has no corresponding
Python script and is also not run by the testing makefile targets.
There is a Python script called 'test_examples.py' which is used by
pytest to test the o2graph scripts. The testing target also uses
the scripts in the o2sclpy/test directory for testing.

