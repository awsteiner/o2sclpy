There are three kinds of examples in this directory. (i) command-line
scripts which demonstrate the use of o2graph, (ii) Jupyter notebooks
and Python scripts which demonstrate the use of o2graph or O2sclpy's
Python interface to O2scl's C++ code.

The alphabetical list of o2graph scripts is:

arrows.scr backend.scr bl_den_plot_yaw.scr cmap_den_plot.scr cmaps.scr
colors_near.scr gltf_cyl.scr gltf_den_plot_col.scr gltf_den_plot.scr
gltf_line.scr gltf_mat.scr gltf_points_col.scr gltf_scatter_col.scr
gltf_scatter.scr kde_plot.scr markers.scr modax.scr obj_props.scr
subplots1.scr subplots2.scr subplots3.scr table3d_den_plot.scr
table_errorbar.scr table_plot_color.scr table_plot.scr table_plotv.scr
table_rplot.scr table_scatter.scr textbox.scr yt_scatter.scr
yt_tg_multvol.scr

The alphabetical list of Python scripts/Jupyter notebooks is:

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
