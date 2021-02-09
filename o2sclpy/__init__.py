#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2020, Andrew W. Steiner
#  
#  This file is part of O2sclpy.
#  
#  O2sclpy is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  O2sclpy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with O2sclpy. If not, see <http://www.gnu.org/licenses/>.
#  
#  -------------------------------------------------------------------
#
# O2sclpy is a library of classes and functions which integrates
# O2scl, python, and matplotlib. The principal purpose of the library
# is to provide a script named 'o2graph', which allows fast analysis
# and plotting of HDF5 files (especially those generated by O2scl).
#

from o2sclpy.doc_data import *
from o2sclpy.slack import *
from o2sclpy.cloud_file import *
from o2sclpy.hdf5 import *
from o2sclpy.link_o2scl import *
from o2sclpy.utils import *
from o2sclpy.plot_base import *
from o2sclpy.plotter import *
from o2sclpy.o2graph_plotter import *
from o2sclpy.plot_info import *
from o2sclpy.base import *
from o2sclpy.part import *
from o2sclpy.nuclei import *
from o2sclpy.eos import *
from o2sclpy.cap_cout import *

"""
The version number string
"""

class todo_list:
    """

    .. todo:: * Give an example of yt_filter in the docs
              * Add RGB hex values to 'colors-near'.
              * Command rect is x1 y1 x2 y2, but ellipse is x1 y1 w h, 
                which is confusing. maybe its better to make them consistent?
                Or allow the user to choose the format?
              * Also, rectanges by default are done without the axes
                transformation, which means they don't change when 
                the plot is zoomed. Maybe allow the user to pick the
                transformation?
              * An example of 'python', 'exec', 'image', 'clf'?
              * Create new functions based on yt_render() which are easier 
                called directly from python.
              * Allow the user to name axes in cbar, inset, and subplots.
              * Create a cube plot like Raph(?) showed, where
                three density plots are shown on the xy xz and yz
                planes in combination with a volume rendering. This
                demands taking a density plot and transforming it to a
                paralellogram with normal matplotlib, using yt for the
                volume rendering, and then making a yt_filter to add
                the volume rendering on top of the density plots. See
                https://matplotlib.org/3.1.0/tutorials/toolkits/axisartist.html
                for the parallelograms.
              * an example of more complicated yt annotations
              * Finish the 'moveauto' path in yt_render()
              * Create a moveauto path which includes a zoom
              * create a vector field command in yt
              * allow the creation of colormaps on the fly? 
              * add map to colormap option for yt tf's
              * Create a system of protected variables and functions using
                underscores and also create a __repr__() object
              * Ensure yt uses self.font for text objects?
              * Finish den-plot-anim for a tensor_grid objects
              * plot-set for a table3d object to create 
                a sequence of curves for each column or row, or maybe 
                do this as a 'mult-vector-spec'?
              * Simplify some of the larger functions like 
                o2graph_plotter::plot(), possibly by creating a separate
                function for each type?
              * Ensure the 'clf' command clears the yt objects?
              * New yt_path option to move along a path determined by
                an o2scl table object?
              * Anti-alias text objects in yt (also anti-alias line 
                sources?)
              * Allow user to specify slack URL and slack username as
                string specs?

    """

    def empty_class():
        print(' ')


