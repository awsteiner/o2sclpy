Plot reference
==============

Nearby colors
-------------

To obtain a list of colors near (in RGB space) a specified color, use
`o2graph -help colors-near <color>` where `<color>` is a named
`matplotlib` color, a HTML-like hexadecimal color, or an array
`(r,g,b)` with entries between 0 and 1. To output the plot to a
filename, use `o2graph -help colors-near <color> <filename>`. To avoid
the generation of a `matplotlib` window, choose the Agg backend first:
`o2graph -backend Agg -help colors-near <color> <filename>`.

.. include:: static/examples/colors_near_plot.scr
   :literal:
.. image:: static/figures/near_blue_doc.png
   :width: 70%
.. image:: static/figures/near_hex_doc.png
   :width: 70%
.. image:: static/figures/near_rgb_doc.png
   :width: 70%

Colormaps
---------

.. include:: static/examples/cmaps_plot.scr
   :literal:
.. image:: static/figures/cmaps_doc.png
   :width: 70%

Markers
-------

.. include:: static/examples/markers_plot.scr
   :literal:
.. image:: static/figures/markers_doc.png
   :width: 70%

