#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2024, Andrew W. Steiner
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
import math
import numpy
import os

# For system type detection
#import platform

# To create new color maps

from o2sclpy.utils import parse_arguments, string_to_dict
from o2sclpy.utils import force_bytes, default_plot
from o2sclpy.utils import string_to_color
from o2sclpy.base import std_vector
from o2sclpy.plot_info import cmap_list_func, cmaps_plot, xkcd_colors_list
from o2sclpy.plot_info import colors_plot, color_list, colors_near

class plot_base:
    """
    This class currently has two goals: (i) some simplifications for
    making plots using matplotlib and (ii) provide an interface for
    easily plotting o2scl objects with matplotlib.
    """

    last_image=0
    """
    The last image object created (used for addcbar())
    """
    axes=0
    """ 
    Current axis object
    """
    axes_dict={}
    """
    Dictionary of axis objects (used by subplots() and selax() to manage
    multiple axis objects)
    """
    fig=0
    """ 
    Figure object
    """
    canvas_flag=False
    """
    If True, then the figure and axes objects have been created
    (default False)
    """
    
    # Quantities modified by set/get
    
    logx=False
    """
    If True, then use a logarithmic x axis (default False)
    """
    logy=False
    """
    If True, then use a logarithmic y axis (default False)
    """
    logz=False
    """
    If True, then use a logarithmic z axis (default False)
    """
    xlo=0
    """
    Lower limit for x axis (default 0)
    """
    xhi=0
    """
    Upper limit for x axis (default 0)
    """
    xset=False
    """ 
    If True, then the x axis limits have been set (default False)
    """
    ylo=0
    """
    Lower limit for y axis (default 0)
    """
    yhi=0
    """
    Upper limit for y axis (default 0)
    """
    yset=False
    """ 
    If True, then the y axis limits have been set (default False)
    """
    zlo=0
    """
    Lower limit for z axis (default 0)
    """
    zhi=0
    """
    Upper limit for z axis (default 0)
    """
    zset=False
    """ 
    If True, then the z axis limits have been set (default False)
    """
    verbose=1
    """
    Verbosity parameter (default 1)
    """
    colbar=False
    """
    If True, then include a color bar for density plots (default False)
    """
    left_margin=0.14
    """
    Left plot margin (default 0.14)
    """
    right_margin=0.04
    """
    Right plot margin (default 0.04)
    """
    top_margin=0.04
    """
    Top plot margin (default 0.04)
    """
    bottom_margin=0.12
    """
    Bottom plot margin (default 0.12)
    """
    font=16
    """
    Font size text objects and axis titles (default 16)
    """
    fig_dict=''
    """
    A dictionary which refers to the figure and axis defaults
    """
    ticks_in=False
    """
    If true, move the ticks inside (default False)
    """
    rt_ticks=False
    """
    If true, include ticks on right side and top (default False)
    """
    editor=False
    """
    If true, open the GUI editor (experimental)
    """
    ax_left_panel=0
    """
    Left panel axis for the editor
    """
    ax_right_panel=0
    """
    Right panel axis for the editor
    """
    link2=0
    """
    Link to the O2scl library DLL
    """
    usetex=True
    """
    If true, then use LaTeX for text objects (default True)
    """
    
    def __init__(self):
        """The plot_base init method, which only calls
        plot_base::new_cmaps().
        """
        self.new_cmaps()
    
    def colors(self,args=[]):
        """Documentation for o2graph command ``colors``:

        Show color information.

        Command-line arguments: ``list`` or ``plot [filename]`` or 
        ``near <color> [filename]`` or ``xkcd``.

        The ``colors`` command outputs or plots information about
        matplotlib colors.

        If the "list" argument is given, then the 8 base colors and
        their RGB definitions are output and then 148 CSS4 colors
        (which include the 8 base colors) are output along with their
        associated hexadecimal values.

        If the "plot" argument is given, then the 148 CSS4 colors
        are plotted in a matplotlib figure. If an additional filename
        argument is specified, the figure is written to the specified
        file. 

        If the "near" argument is given, then the 80 colors 
        closest to <color> are plotted in a matplotlib figure. If 
        an additional filename argument is specified, then the 
        figure is written to the specified file. To determine 
        which colors are "nearest", the sum of the absolute
        values of the differences in the RGB values are used.

        Finally, if the "xkcd" argument is given, then all 
        949 xkcd colors are listed along with their HTML
        hexadecimal RBG values.

        Color arguments in o2graph supports the (r,g,b) format, the
        [r,g,b,a] format, the HTML format, the grayscale single-value
        format, and the XKCD colors. For (r,g,b) colors, parentheses
        must be used, and the r, g, and b numbers should be from 0.0
        to 1.0. For [r,g,b,a] colors, square brackets must be used and
        the r, g, b, and a numbers should be from 0.0 to 1.0. The HTML
        format is #RRGGBB where RR, GG, and BB are two-digit
        hexadecimal values.
        """

        if len(args)>=1 and args[0]=='list':
            color_list()
            return

        if len(args)>=1 and args[0]=='plot':
            if len(args)>=2:
                colors_plot(args[1])
            else:
                colors_plot()
            return

        if len(args)>=1 and args[0]=='near':
            if len(args)>=3:
                colors_near(col=args[1],fname=args[2])
            elif len(args)>=2:
                colors_near(col=args[1])
            else:
                colors_near()
            return

        if len(args)>=1 and args[0]=='xkcd':
            xkcd_colors_list()
            return

        print('Arguments for command "colors" not understood.')
        return
    
    def cmap(self,cmap_name,col_list=[]):
        """Documentation for o2graph command ``cmap``:

        Create a continuous colormap or list colormaps.

        Command-line arguments: ``<cmap name> <color 1> <color 2> 
        [color3]...`` or ``<cmap name> "sharp" <color 1> <color 2>
        [color3 color4]...`` or ``list`` or ``plot [filename]``

        In the first form, this command creates a new color map named
        <cmap name> which consists of equal-sized gradients between
        the specified list of at least two colors. In the second form,
        when the keyword sharp is given, the color map consists of
        gradients between each pair of colors with a sharp transition
        between successive pairs.

        Matplotlib colors, (r,g,b) colors, [r,g,b,a] colors,
        and xkcd colors are all allowed. For example::

          o2graph -cmap c forestgreen "[0.5,0.5,0.7,0.5]" \\
          "xkcd:light red" -create table3d x grid:0,40,1 y grid:0,40,1 \\
          z "x+y" -den-plot z cmap=c -show

        or::

          o2graph -cmap c sharp "(0.5,0.5,0.7)" "xkcd:light red" \\
          green "(0,0,0)" -create table3d x grid:0,40,1 y grid:0,40,1 \\
          z "x+y" -den-plot z cmap=c -show

        In the third form, the cmap command lists all of the 
        available colormaps. Finally, in the fourth form, the 
        cmap command plots all available colormaps, optionally storing
        this plot in a file, e.g.::

          o2graph -cmap plot cmap_plot.png

        To get more information on the available colors, see::

          o2graph -colors list 
        """

        if self.verbose>1:
            print('cmap name:',cmap_name,'list:',col_list)

        if cmap_name=='list':
        
            cmap_list_func()
            return

        elif cmap_name=='plot':
        
            if len(col_list)>=1:
                cmaps_plot(col_list[0])
            else:
                cmaps_plot()
            return

        elif col_list[0]=='sharp':

            col_list=col_list[1:]
            
            N=len(col_list)
            
            if N%2==1:
                print('Must have an even number of arguments in cmap2.')
                return
            
            if self.verbose>1:
                print('cmap name:',cmap_name,'list:',col_list)
            
            # This value is used to indicate values in the colormap
            # tuples that are ignored by LinearSegmentedColormap()
            unused=0.0
    
            col_r=numpy.ones((int(N/2+1),3))
            col_g=numpy.ones((int(N/2+1),3))
            col_b=numpy.ones((int(N/2+1),3))
            col_a=numpy.ones((int(N/2+1),3))
    
            # Convert the colors to RGBA arrays (the alpha value is
            # ignored)
            rgb_list=[]
            from matplotlib.colors import to_rgba
            for i in range(0,N):
                if isinstance(col_list[i],str):
                    rgb_list.append(to_rgba(string_to_color(col_list[i])))
                else:
                    rgb_list.append(to_rgba(col_list[i]))
    
            if self.verbose>1:
                print('rgb_list:',rgb_list)

            for i in range(0,int(N/2)+1):
                col_r[i][0]=float(i)/float(N/2)
                col_g[i][0]=float(i)/float(N/2)
                col_b[i][0]=float(i)/float(N/2)
                col_a[i][0]=float(i)/float(N/2)
                if i==0:
                    col_r[i][1]=unused
                    col_g[i][1]=unused
                    col_b[i][1]=unused
                    col_a[i][1]=unused
                    col_r[i][2]=rgb_list[0][0]
                    col_g[i][2]=rgb_list[0][1]
                    col_b[i][2]=rgb_list[0][2]
                    col_a[i][2]=rgb_list[0][3]
                elif i==N/2:
                    col_r[i][1]=rgb_list[N-1][0]
                    col_g[i][1]=rgb_list[N-1][1]
                    col_b[i][1]=rgb_list[N-1][2]
                    col_a[i][1]=rgb_list[N-1][3]
                    col_r[i][2]=unused
                    col_g[i][2]=unused
                    col_b[i][2]=unused
                    col_a[i][2]=unused
                else:
                    col_r[i][1]=rgb_list[int(i/2+1)][0]
                    col_g[i][1]=rgb_list[int(i/2+1)][1]
                    col_b[i][1]=rgb_list[int(i/2+1)][2]
                    col_a[i][1]=rgb_list[int(i/2+1)][3]
                    col_r[i][2]=rgb_list[int(i/2+2)][0]
                    col_g[i][2]=rgb_list[int(i/2+2)][1]
                    col_b[i][2]=rgb_list[int(i/2+2)][2]
                    col_a[i][2]=rgb_list[int(i/2+2)][3]
    
                if self.verbose>1:
                    print('red  ',col_r[i][0],col_r[i][1],col_r[i][2])
                    print('green',col_g[i][0],col_g[i][1],col_g[i][2])
                    print('blue ',col_b[i][0],col_b[i][1],col_b[i][2])
                    print('alpha',col_a[i][0],col_a[i][1],col_a[i][2])
                    print('')
    
            cdict={'red': col_r, 'green': col_g, 'blue': col_b,
                   'alpha': col_a}
            
        else:
            
            # This value is used to indicate values in the colormap
            # tuples that are ignored by LinearSegmentedColormap()
            unused=0.0
    
            N=len(col_list)
            
            col_r=numpy.ones((N,3))
            col_g=numpy.ones((N,3))
            col_b=numpy.ones((N,3))
            col_a=numpy.ones((N,3))
    
            # Convert the colors to RGBA arrays (the alpha value is
            # ignored)
            rgb_list=[]
            from matplotlib.colors import to_rgba
            for i in range(0,N):
                if isinstance(col_list[i],str):
                    rgb_list.append(to_rgba(string_to_color(col_list[i])))
                else:
                    rgb_list.append(to_rgba(col_list[i]))
    
            if self.verbose>1:
                print('rgb_list:',rgb_list)
    
            for i in range(0,N):
                col_r[i][0]=float(i)/float(N-1)
                col_g[i][0]=float(i)/float(N-1)
                col_b[i][0]=float(i)/float(N-1)
                col_a[i][0]=float(i)/float(N-1)
                if i==0:
                    col_r[i][1]=unused
                    col_g[i][1]=unused
                    col_b[i][1]=unused
                    col_a[i][1]=unused
                    col_r[i][2]=rgb_list[0][0]
                    col_g[i][2]=rgb_list[0][1]
                    col_b[i][2]=rgb_list[0][2]
                    col_a[i][2]=rgb_list[0][3]
                elif i==N-1:
                    col_r[i][1]=rgb_list[N-1][0]
                    col_g[i][1]=rgb_list[N-1][1]
                    col_b[i][1]=rgb_list[N-1][2]
                    col_a[i][1]=rgb_list[N-1][3]
                    col_r[i][2]=unused
                    col_g[i][2]=unused
                    col_b[i][2]=unused
                    col_a[i][2]=unused
                else:
                    col_r[i][1]=rgb_list[i][0]
                    col_g[i][1]=rgb_list[i][1]
                    col_b[i][1]=rgb_list[i][2]
                    col_a[i][1]=rgb_list[i][3]
                    col_r[i][2]=rgb_list[i][0]
                    col_g[i][2]=rgb_list[i][1]
                    col_b[i][2]=rgb_list[i][2]
                    col_a[i][2]=rgb_list[i][3]
    
                if self.verbose>1:
                    print('red  ',col_r[i][0],col_r[i][1],col_r[i][2])
                    print('green',col_g[i][0],col_g[i][1],col_g[i][2])
                    print('blue ',col_b[i][0],col_b[i][1],col_b[i][2])
                    print('alpha',col_a[i][0],col_a[i][1],col_a[i][2])
                    print('')
    
            cdict={'red': col_r, 'green': col_g, 'blue': col_b,
                   'alpha': col_a}
            
        import matplotlib
        from matplotlib.colors import LinearSegmentedColormap
        #import matplotlib.pyplot as plot

        cmap_obj=LinearSegmentedColormap(cmap_name,cdict)
        #plot.register_cmap(cmap=cmap_obj)
        matplotlib.colormaps.register(cmap=cmap_obj)
                
        # Colormap reversed
        cmapr_obj=cmap_obj.reversed()
        #plot.register_cmap(cmap=cmapr_obj)
        matplotlib.colormaps.register(cmap=cmapr_obj)
        
        return
        
    def new_cmaps(self):
        """Add a few new colormaps. This function is called by
        plot_base::__init__().

        This function adds the colormaps 'jet2' 'pastel2', 'reds2',
        'greens2', and 'blues2'.
        """

        import matplotlib.pyplot as plot
        import matplotlib
        from matplotlib.colors import LinearSegmentedColormap

        if 'jet2' not in plot.colormaps():
            # LinearSegmentedColormap
            # 
            # Each row in the table for a given color is a sequence of x,
            # y0, y1 tuples. In each sequence, x must increase
            # monotonically from 0 to 1. For any input value z falling
            # between x[i] and x[i+1], the output value of a given color
            # will be linearly interpolated between y1[i] and y0[i+1]:
            # Hence y0 in the first row and y1 in the last row are never used.
    
            # This value is used to indicate values in the colormap
            # tuples that are ignored by LinearSegmentedColormap()
            unused=0.0
    
            # A white to red colormap
            cdict={'red': ((0.0,unused,1.0),(1.0,1.0,unused)),
                   'green': ((0.0,unused,1.0),(1.0,0.0,unused)),
                   'blue': ((0.0,unused,1.0),(1.0,0.0,unused))}
            reds2=LinearSegmentedColormap('reds2',cdict)
            matplotlib.colormaps.register(cmap=reds2)
            #plot.register_cmap(cmap=reds2)
            
            # Colormap reds2, reversed
            reds2_r=reds2.reversed()
            matplotlib.colormaps.register(cmap=reds2_r)
            #plot.register_cmap(cmap=reds2_r)
            
            # A new version of the ``jet`` colormap which starts with
            # white instead of blue. In order, the index colors are white,
            # blue, green, yellow, orange, and red
            cdict={'red': ((0.0,unused,1.0),(0.2,0.0,0.0),
                           (0.4,0.0,0.0),(0.6,1.0,1.0),
                           (0.8,1.0,1.0),(1.0,1.0,unused)),
                   'green': ((0.0,unused,1.0),(0.2,0.0,0.0),
                             (0.4,0.5,0.5),(0.6,1.0,1.0),
                             (0.8,0.6,0.6),(1.0,0.0,unused)),
                   'blue': ((0.0,unused,1.0),(0.2,1.0,1.0),
                            (0.4,0.0,0.0),(0.6,0.0,0.0),
                            (0.8,0.0,0.0),(1.0,0.0,unused))}
            jet2=LinearSegmentedColormap('jet2',cdict)
            matplotlib.colormaps.register(cmap=jet2)
            #plot.register_cmap(cmap=jet2)
    
            # Colormap jet2, reversed
            jet2_r=jet2.reversed()
            matplotlib.colormaps.register(cmap=jet2_r)
            #plot.register_cmap(cmap=jet2_r)
    
            # A new version of the ``pastel`` colormap which starts with
            # white instead of blue. In order, the index colors are white,
            # blue, green, yellow, orange, and red
            cdict={'red': ((0.0,unused,1.0),(0.2,0.3,0.3),
                           (0.4,0.3,0.3),(0.6,1.0,1.0),
                           (0.8,1.0,1.0),(1.0,1.0,1.0)),
                   'green': ((0.0,unused,1.0),(0.2,0.3,unused),
                             (0.4,0.5,0.5),(0.6,1.0,1.0),
                             (0.8,0.6,0.6),(1.0,0.3,unused)),
                   'blue': ((0.0,unused,1.0),(0.2,1.0,1.0),
                            (0.4,0.3,0.3),(0.6,0.3,0.3),
                            (0.8,0.3,0.3),(1.0,0.3,unused))}
            pastel2=LinearSegmentedColormap('pastel2',cdict)
            matplotlib.colormaps.register(cmap=pastel2)
            #plot.register_cmap(cmap=pastel2)
            
            # Colormap pastel2, reversed
            pastel2_r=pastel2.reversed()
            matplotlib.colormaps.register(cmap=pastel2_r)
            #plot.register_cmap(cmap=pastel2_r)
    
            # A white to green colormap
            cdict={'red': ((0.0,unused,1.0),(1.0,0.0,unused)),
                   'green': ((0.0,unused,1.0),(1.0,1.0,unused)),
                   'blue': ((0.0,unused,1.0),(1.0,0.0,unused))}
            greens2=LinearSegmentedColormap('greens2',cdict)
            matplotlib.colormaps.register(cmap=greens2)
            #plot.register_cmap(cmap=greens2)
            
            # Colormap greens2, reversed
            greens2_r=greens2.reversed()
            matplotlib.colormaps.register(cmap=greens2_r)
            #plot.register_cmap(cmap=greens2_r)
            
            # A white to blue colormap
            cdict={'red': ((0.0,unused,1.0),(1.0,0.0,unused)),
                   'green': ((0.0,unused,1.0),(1.0,0.0,unused)),
                   'blue': ((0.0,unused,1.0),(1.0,1.0,unused))}
            blues2=LinearSegmentedColormap('blues2',cdict)
            matplotlib.colormaps.register(cmap=blues2)
            #plot.register_cmap(cmap=blues2)
            
            # Colormap blues2, reversed
            blues2_r=blues2.reversed()
            matplotlib.colormaps.register(cmap=blues2_r)
            #plot.register_cmap(cmap=blues2_r)

        # End of function plot_base::new_cmaps()
        return

    def set(self,name,value):
        """Set the value of parameter named ``name`` to value ``value``. The
        documentation for the o2graph command ``set`` is given in
        O₂scl.
        """
        
        import matplotlib.pyplot as plot

        if name=='logx':
            if value=='False' or value=='0':
                self.logx=False
            else:
                self.logx=True
        elif name=='logy':
            if value=='False' or value=='0':
                self.logy=False
            else:
                self.logy=True
        elif name=='logz':
            if value=='False' or value=='0':
                self.logz=False
            else:
                self.logz=True
        elif name=='xlo':
            if value[0]=='(':
                self.xlo=float(eval(value))
            else:
                self.xlo=float(value)
            self.xset=True
        elif name=='xhi':
            if value[0]=='(':
                self.xhi=float(eval(value))
            else:
                self.xhi=float(value)
            self.xset=True
        elif name=='xset':
            if value=='False' or value=='0':
                self.xset=False
            else:
                self.xset=True
        elif name=='ylo':
            if value[0]=='(':
                self.ylo=float(eval(value))
            else:
                self.ylo=float(value)
            self.yset=True
        elif name=='yhi':
            if value[0]=='(':
                self.yhi=float(eval(value))
            else:
                self.yhi=float(value)
            self.yset=True
        elif name=='yset':
            if value=='False' or value=='0':
                self.xset=False
            else:
                self.xset=True
        elif name=='zlo':
            if value[0]=='(':
                self.zlo=float(eval(value))
            else:
                self.zlo=float(value)
            self.zset=True
        elif name=='zhi':
            if value[0]=='(':
                self.zhi=float(eval(value))
            else:
                self.zhi=float(value)
            self.zset=True
        elif name=='zset':
            if value=='False' or value=='0':
                self.zset=False
            else:
                self.zset=True
        elif name=='usetex':
            if value=='False' or value=='0':
                self.usetex=False
                plot.rc('text',usetex=False)
            else:
                self.usetex=True
                plot.rc('text',usetex=True)
        elif name=='editor':
            if value=='False' or value=='0':
                self.editor=False
            else:
                self.editor=True
        elif name=='verbose':
            self.verbose=int(value)
        elif name=='colbar':
            if value=='False' or value=='0':
                self.colbar=False
            else:
                self.colbar=True
        elif name=='font':
            self.font=float(value)
        elif name=='fig_dict':
            self.fig_dict=value
        elif name=='yt_resolution':
            # Remove parenthesis
            left_paren=value.find('(')
            right_paren=value.find(')')
            value=value[left_paren+1:right_paren]
            # Then split into two values
            value=value.split(',')
            # And reformat as a list
            self.yt_resolution=(int(value[0]),int(value[1]))
        elif name=='yt_focus':
            # We leave the focus as a string so we can parse
            # it later
            self.yt_focus=value
        elif name=='yt_sigma_clip':
            self.yt_sigma_clip=float(value)
        elif name=='yt_position':
            # We leave the position as a string so we can parse
            # it later
            self.yt_position=value
        elif name=='yt_north':
            # We leave the north as a string so we can parse
            # it later
            self.yt_north=value
        elif name=='yt_width':
            # We leave the width as a string so we can parse
            # it later
            self.yt_width=value
        elif name=='yt_filter':
            self.yt_filter=value
        elif name=='yt_path':
            self.yt_path=value
        else:
            print('No variable named',name)
            
        if self.verbose>0:
            print('Set',name,'to',value)
            
        # End of function plot_base::set()
        return

    def get(self,name):
        """Output the value of parameter named ``name``. The documentation
        for the o2graph command ``get`` is given in O₂scl.
        """
        if name=='colbar':
            print('The value of colbar is'+str(self.colbar)+'.')
        if name=='logx':
            print('The value of logx is'+str(self.logx)+'.')
        if name=='logy':
            print('The value of logy is'+str(self.logy)+'.')
        if name=='logz':
            print('The value of logz is'+str(self.logz)+'.')
        if name=='verbose':
            print('The value of verbose is'+str(self.verbose)+'.')
        if name=='xhi':
            print('The value of xhi is'+str(self.xhi)+'.')
        if name=='xlo':
            print('The value of xlo is'+str(self.xlo)+'.')
        if name=='xset':
            print('The value of xset is'+str(self.xset)+'.')
        if name=='yhi':
            print('The value of yhi is'+str(self.yhi)+'.')
        if name=='ylo':
            print('The value of ylo is'+str(self.ylo)+'.')
        if name=='yset':
            print('The value of yset is'+str(self.yset)+'.')
        if name=='zhi':
            print('The value of zhi is'+str(self.zhi)+'.')
        if name=='zlo':
            print('The value of zlo is'+str(self.zlo)+'.')
        if name=='zset':
            print('The value of zset is'+str(self.zset)+'.')
        if name=='fig_dict':
            print('The value of fig_dict is'+str(self.fig_dict)+'.')
        if name=='yt_axis':
            print('The value of yt_axis is'+str(self.yt_axis)+'.')
        if name=='yt_axis_color':
            print('The value of yt_axis_color is'+str(self.yt_axis_color)+'.')
        if name=='yt_axis_labels_flat':
            print('The value of yt_axis_labels_flat is',
                  self.yt_axis_labels_flat,'.')
        if name=='yt_axis_resolution':
            print('The value of yt_axis_resolution is',
                  self.yt_axis_resolution,'.')
        if name=='yt_focus':
            print('The value of yt_focus is'+str(self.yt_focus)+'.')
        if name=='yt_sigma_clip':
            print('The value of yt_sigma_clip is'+str(self.yt_sigma_clip)+'.')
        if name=='yt_position':
            print('The value of yt_position is'+str(self.yt_position)+'.')
        if name=='yt_path':
            print('The value of yt_path is'+str(self.yt_path)+'.')
        # End of function plot_base::get()
        return

    def xlimits(self,xlo,xhi):
        """Documentation for o2graph command ``xlimits``:

        Set the x-axis limits

        Command-line arguments: ``<x low> <x high>``

        The xlimits command sets ``xlo`` and ``xhi`` to the specified
        limits and sets ``xset`` to True. If a plotting canvas is
        currently open, then the x-limits on the current axis are
        modified. Future plots are also plot with the specified
        x-limits. If <low> and <high> are identical then ``xset`` is
        set to False and the x limits are automatically set by
        matplotlib.
        """
        if xlo==xhi:
            self.xset=False
            return
        self.xlo=xlo
        self.xhi=xhi
        self.xset=True

        if self.canvas_flag==True:
            self.axes.set_xlim(self.xlo,self.xhi)
            if self.logx==True:
                self.axes.set_xscale('log')
            else:
                self.axes.set_xscale('linear')
            
        # End of function plot_base::xlimits()
        return

    def ylimits(self,ylo,yhi):
        """
        Documentation for o2graph command ``ylimits``:

        Set the y-axis limits

        Command-line arguments: ``<y low> <y high>``

        The ``ylimits`` command sets ``ylo`` and ``yhi`` to the
        specified limits and sets ``yset`` to True. If a plotting
        canvas is currently open, then the y-limits on the current
        axis are modified. Future plots are also plot with the
        specified y-limits. If <low> and <high> are identical then
        ``yset`` is set to False and the y limits are automatically
        set by matplotlib.
        """
        if ylo==yhi:
            self.yset=False
            return
        self.ylo=ylo
        self.yhi=yhi
        self.yset=True
        
        if self.canvas_flag==True:
            self.axes.set_ylim(self.ylo,self.yhi)
            if self.logy==True:
                self.axes.set_yscale('log')
            else:
                self.axes.set_yscale('linear')
            
        # End of function plot_base::ylimits()
        return

    def zlimits(self,zlo,zhi):
        """Documentation for o2graph command ``zlimits``:

        Set the z-axis limits

        Command-line arguments: ``<z low> <z high>``

        The ``zlimits`` command sets ``zlo`` and ``zhi`` to the
        specified limits and sets ``zset`` to True. If <low> and
        <high> are identical then ``zset`` is set to False.
        """
        if zlo==zhi:
            self.zset=False
            return
        self.zlo=zlo
        self.zhi=zhi
        self.zset=True
        #if self.canvas_flag==True:
        #plot.zlim([zlo,zhi])
        # End of function plot_base::zlimits()
        return

    def line(self,x1,y1,x2,y2,**kwargs):
        """Documentation for o2graph command ``line``:

        Plot a line from :math:`(x_1,y_1)` to :math:`(x_2,y_2)`

        Command-line arguments: ``<x1> <y1> <x2> <y2> [kwargs]``

        Plot a line from ``(x1,y1)`` to ``(xy,y2)``. Some useful
        kwargs are color (c), dashes, linestyle (ls), linewidth (lw),
        marker, markeredgecolor (mec), markeredgewidth (mew),
        markerfacecolor (mfc), markerfacecoloralt (mfcalt), markersize
        (ms). For example::

            o2graph -line 0.05 0.05 0.95 0.95 \\
            lw=2,marker='+',ms=10,c=xkcd:'light purple' -show

        """
        if self.verbose>2:
            print('Line',x1,y1,x2,y1)
        if self.canvas_flag==False:
            self.canvas()
            
        if isinstance(x1,str):
            x1=float(eval(x1))
        if isinstance(y1,str):
            y1=float(eval(y1))
        if isinstance(x2,str):
            x2=float(eval(x2))
        if isinstance(y2,str):
            y2=float(eval(y2))

        self.axes.plot([x1,x2],[y1,y2],**kwargs)
        # End of function plot_base::line()
        return

    def arrow(self,x1,y1,x2,y2,arrowprops,**kwargs):
        """Documentation for o2graph command ``arrow``:

        Plot an arrow.
        
        Command-line arguments: ``x1 y1 x2 y2 <arrow properties> [kwargs]``

        Plot an arrow from :math:`(x_1,y_1)` to :math:`(x_2,y_2)`. The
        ``arrow`` command uses axes.annotate() to generate an arrow
        with an empty string as the first argument to annotate(). The
        o2graph argument <arrow properties> is the python dictionary
        for the 'arrowprops' argument to annotate(). The arrowstyle
        and connectionstyle attributes should be listed along with
        other arrowprops attributes. Examples for arrowprops are::

            * arrowstyle=->,connectionstyle=arc3 \\
            * arrowstyle=-|>,connectionstyle=arc,fc=red,ec=blue \\
            * arrowstyle=-|>,connectionstyle=arc,head_length=4.0,
              head_width=1.0 \\
            * arrowstyle=->,connectionstyle=arc3,head_length=4.0,
              head_width=1.0,rad=-0.1 \\
            * arrowstyle=fancy,connectionstyle=arc3,head_length=4.0,
              head_width=1.0,rad=-0.1 \\
        
        Summary for arrowstyle argument (angleB is renamed to 
        as_angleB)::

            Name    Attributes \\
            -       None \\
            ->      head_length=0.4,head_width=0.2 \\
            -[      widthB=1.0,lengthB=0.2,as_angleB=None \\
            |-      widthA=1.0,widthB=1.0 \\
            -|      head_length=0.4,head_width=0.2 \\
            <-      head_length=0.4,head_width=0.2 \\
            <|      head_length=0.4,head_width=0.2 \\
            fancy   head_length=0.4,head_width=0.4,tail_width=0.4 \\
            simple  head_length=0.5,head_width=0.5,tail_width=0.2 \\
            wedge   tail_width=0.3,shrink_factor=0.5 \\
        
        (note that fancy, simple or wedge require arc3 or angle3 connection 
        styles)

        Summary for connectionstyle argument (angleB is renamed to 
        cs_angleB)::

            Name    Attributes \\
            * angle   angleA=90,cs_angleB=0,rad=0.0 \\
            * angle3  angleA=90,cs_angleB=0 \\
            * arc     angleA=0,cs_angleB=0,armA=None,armB=None,rad=0.0 \\
            * arc3    rad=0.0 \\
            * bar     armA=0.0,armB=0.0,fraction=0.3,angle=None \\

        See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html for more. 
        """
        if self.verbose>2:
            print('Arrow',x1,y1,x2,y1,arrowprops)
        if self.canvas_flag==False:
            self.canvas()
        if isinstance(x1,str):
            x1=float(eval(x1))
        if isinstance(y1,str):
            y1=float(eval(y1))
        if isinstance(x2,str):
            x2=float(eval(x2))
        if isinstance(y2,str):
            y2=float(eval(y2))

        # Convert the arrow properties string to a dict
        ap_dict=string_to_dict(arrowprops)

        # The arrowstyle and connectionstyle arguments have to be a
        # part the string argument of arrowstyle, so we have to reorganize
        # these arguments from the dict and add them to the string.

        # These are the arrowstyle arugments (except for angleB
        # which has to be handled separately)
        as_args=["head_width","head_length","tail_width",
                 "shrink_factor","widthA","widthB",
                 "lengthA","lengthB"]

        # Update the arrowstyle string
        if "arrowstyle" in ap_dict:
            for j in range(0,len(as_args)):
                if as_args[j] in ap_dict:
                    ap_dict["arrowstyle"]=(ap_dict["arrowstyle"]+
                                           ','+as_args[j]+'='+
                                           ap_dict.pop(as_args[j]))
            if "as_angleB" in ap_dict:
                ap_dict["arrowstyle"]=(ap_dict["arrowstyle"]+
                                       ',angleB='+
                                       ap_dict.pop("as_angleB"))
            print('arrowstyle:',ap_dict["arrowstyle"])

        # These are the connectionstyle arugments (except for angleB
        # which has to be handled separately)
        cs_args=["angleA","armA","armB","rad","fraction",
                 "angle"]
            
        # Update the connectionstyle string
        if "connectionstyle" in ap_dict:
            for j in range(0,len(cs_args)):
                if cs_args[j] in ap_dict:
                    ap_dict["connectionstyle"]=(ap_dict["connectionstyle"]+
                                                ','+cs_args[j]+'='+
                                                ap_dict.pop(cs_args[j]))
            if "cs_angleB" in ap_dict:
                ap_dict["connectionstyle"]=(ap_dict["connectionstyle"]+
                                            ',angleB='+
                                            ap_dict.pop("cs_angleB"))
            print('connectionstyle:',ap_dict["connectionstyle"])
            
        self.axes.annotate("",xy=(x2,y2),xycoords='data',
                           xytext=(x1,y1),textcoords='data',
                           arrowprops=ap_dict)
        # End of function plot_base::arrow()
        return

    def point(self,xval,yval,**kwargs):
        """Documentation for o2graph command ``point``:

        Plot a single point.

        Command-line arguments: ``<x> <y> <kwargs>``

        Plot a single point. Some useful kwargs are color, marker,
        markeredgecolor (mec), markeredgewidth (mew), and markersize
        (ms). Note that the 'marker' keyword argument to specify the
        marker type must be specified. For example::

            o2graph -xlimits 0 1 -ylimits 0 1 -point 0.5 0.5 \\
            marker='o',ms=10,c='xkcd:sea green',mec=blue,mew=2 -show

        or::

            o2graph -xlimits 0 1 -ylimits 0 1 -point 0.5 0.5 \\
            marker='$\\int_0^{\\infty}x^2~dx$',ms=300,c=green,mec=red -show

        To list the marker types, use::

            o2graph -help markers

        or::

            o2graph -help markers-plot

        """
        if self.verbose>2:
            print('point',xval,yval,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        if isinstance(xval,str):
            xval=float(eval(xval))
        if isinstance(yval,str):
            yval=float(eval(yval))
        self.axes.plot([xval],[yval],**kwargs)
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
        # End of function plot_base::point()
        return

    def error_point(self,xval,yval,err1=None,err2=None,
                    err3=None,err4=None,**kwargs):
        """
        Documentation for o2graph command ``error-point``:

        Plot a single point with errorbars.

        Command-line arguments: ``<x> <y> [<x err> <yerr>] or 
        [<x lo> <x hi> <y lo> <y hi>]``

        Some useful kwargs for the ``error-point`` command are::
        
            keyword    description                       default value \\
            ecolor     error bar color                   None \\
            capsize    cap size in points                None \\
            barsabove  plot error bars on top of point   False \\
            lolims     y value is lower limit            False \\
            uplims     y value is upper limit            False \\
            xlolims    x value is lower limit            False \\
            xuplims    x value is upper limit            False \\
            errorevery draw error bars on subset of data 1 \\
            capthick   thickness of error bar cap        None

        See also ``errorbar`` for for plotting columns from a table object
        and the documentation at
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.errorbar.html

        """
        if err1=='None' or err1=='none':
            err1=None
        if err2=='None' or err2=='none':
            err2=None
        if err3=='None' or err3=='none':
            err3=None
        if err4=='None' or err4=='none':
            err4=None
        if self.verbose>2:
            print('error-point',xval,yval,err1,err2,err3,err4,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        if isinstance(xval,str):
            xval=float(eval(xval))
        if isinstance(yval,str):
            yval=float(eval(yval))
        if err1==None and err2==None and err3==None and err4==None:
            self.axes.point([float(eval(xval))],
                            [float(eval(yval))],**kwargs)
        elif err3==None and err4==None:
            if isinstance(err2,str):
                err2=float(eval(err2))
            if isinstance(err1,str):
                err1=float(eval(err1))
            self.axes.errorbar([xval],[yval],
                               yerr=[err2],xerr=[err1],**kwargs)
        elif err2==None:
            if isinstance(err4,str):
                err4=float(eval(err4))
            if isinstance(err3,str):
                err3=float(eval(err3))
            if isinstance(err1,str):
                err1=float(eval(err1))
            self.axes.errorbar([xval],[yval],
                               yerr=[[err3],[err4]],
                               xerr=[err1],**kwargs)
        elif err4==None:
            if isinstance(err2,str):
                err2=float(eval(err2))
            if isinstance(err1,str):
                err1=float(eval(err1))
            if isinstance(err3,str):
                err3=float(eval(err3))
            self.axes.errorbar([xval],[yval],yerr=[err3],
                               xerr=[[err1],[err2]],**kwargs)
        else:
            if isinstance(err2,str):
                err2=float(eval(err2))
            if isinstance(err1,str):
                err1=float(eval(err1))
            if isinstance(err4,str):
                err4=float(eval(err4))
            if isinstance(err3,str):
                err3=float(eval(err3))
            self.axes.errorbar([xval],[yval],
                               yerr=[[err3],[err4]],
                               xerr=[[err1],[err2]],**kwargs)
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
        # End of function plot_base::point()
        return

    def rect(self,x1,y1,x2,y2,angle=0,**kwargs):
        """Documentation for o2graph command ``rect``:

        Plot a rectangle.

        Command-line arguments: ``<x1> <y1> <x2> <y2> [angle] [kwargs]``

        Plot a rectange from (x1,y1) to (xy,y2) with rotation angle
        <angle>. By default, the rectangle has no border, but the
        linewidth ('lw') and edgecolor kwargs can be used to specify
        one if desired. Some useful kwargs are alpha, color, edgecolor
        (ec), facecolor (fc), fill, hatch ('/', '\\', '|', '-', '+',
        'x', 'o', 'O', '.', '*'), linestyle (ls), linewidth (lw). In
        order to specify keyword arguments, an angle must be also
        specified.

        For example::

            o2graph -xlimits 0 0.8 -ylimits 0 0.6 \\
            -text 0.55 0.35 "blah" -rect 0.2 0.2 0.5 0.5 \\
            -rect 0.3 0.3 0.7 0.4 0 \\
            fc=green,alpha=0.5,ls=-.,ec='xkcd:burnt orange',lw=2,hatch='///' \\
            -show

        """
        import matplotlib.patches as patches

        if self.verbose>2:
            print('Rect',x1,y1,x2,y1)
        if self.canvas_flag==False:
            self.canvas()

        if isinstance(x1,str):
            x1=float(eval(x1))
        if isinstance(x2,str):
            x2=float(eval(x2))
        if isinstance(y1,str):
            y1=float(eval(y1))
        if isinstance(y2,str):
            y2=float(eval(y2))

        left=x1
        if x2<x1:
            left=x2
        lower=y1
        if y2<y1:
            lower=y2
        w=abs(x1-x2)
        h=abs(y1-y2)
        if self.canvas_flag==False:
            self.canvas()
        r=patches.Rectangle((left,lower),w,h,angle=angle,**kwargs)
        self.axes.add_patch(r)
        # End of function plot_base::rect()
        return

    def ellipse(self,x,y,w,h,angle=0,**kwargs):
        """
        Documentation for o2graph command ``ellipse``:

        Plot an ellipse.

        Command-line arguments: ``<x> <y> <w> <h> [angle] [kwargs]``

        Plot an ellipse centered at (x,y) with width w and height h,
        optionally rotated by the specified angle. By default, the
        ellipse has no border, but the linewidth ('lw') and edgecolor
        kwargs can be used to specify one if desired. Some useful
        kwargs are alpha, color, edgecolor (ec), facecolor (fc), fill,
        hatch, linestyle (ls), linewidth (lw). For example::

            o2graph -ellipse 0.5 0.5 0.8 0.2 45 \\
            fc='#ccccff',ec=black,lw=2,hatch='|||',ls=':' -show
        
        """
        import matplotlib.patches as patches

        if self.verbose>2:
            print('Ellipse',x,y,w,h,angle)
        if self.canvas_flag==False:
            self.canvas()
        if isinstance(x,str):
            x=float(eval(x))
        if isinstance(y,str):
            y=float(eval(y))
        if isinstance(w,str):
            w=float(eval(w))
        if isinstance(h,str):
            h=float(eval(h))
        if isinstance(angle,str):
            angle=float(eval(angle))
        if self.canvas_flag==False:
            self.canvas()
        r=patches.Ellipse((x,y),w,h,angle=angle,**kwargs)
        self.axes.add_patch(r)
        # End of function plot_base::ellipse()
        return

    def show(self):
        """
        Documentation for o2graph command ``show``:

        Show the current plot.

        (No arguments.)

        Show the current plot on the screen and begin the graphical
        user interface. When the editor is not enabled this just
        runs ``matplotlib.pyplot.show()``.
        """

        import matplotlib.pyplot as plot

        if self.editor:
            
            def disable(ax):
                b=ax.get_position().bounds
                if b[0]<1:
                    b2=[b[0]+1,b[1],b[2],b[3]]
                else:
                    b2=[b[0],b[1],b[2],b[3]]
                ax.set_position(b2)
                return
                
            def enable(ax):
                b=ax.get_position().bounds
                if b[0]>1:
                    b2=[b[0]-1,b[1],b[2],b[3]]
                else:
                    b2=[b[0],b[1],b[2],b[3]]
                ax.set_position(b2)
                return
                
            from matplotlib.widgets import Button, Slider, TextBox

            plot.rc('text',usetex=False)
            
            title=r'$ \mathrm{O}_2\mathrm{graph~Plot~Editor}$'
            editor_title=self.ax_right_panel.text(0.02,0.955,title,
                                                  ha='left',va='center',
                                                  fontsize=16)

            inst_text=('Begin by selecting a plot element above '+
                       'to modify.')
            instructions=self.ax_right_panel.text(0.02,0.91,inst_text,
                                                  ha='left',va='center',
                                                  fontsize=16)
            
            # The 'close' button
            ax_close_button=plot.axes([0.915,0.93,0.08,0.06])
            close_button=Button(ax_close_button,r'close')
            close_button.label.set_size(14)

            # The 'figure' button
            ax_figure_button=plot.axes([0.505,0.81,0.1,0.06])
            figure_button=Button(ax_figure_button,'figure')
            figure_button.label.set_size(14)

            # The 'axes' button
            ax_axes_button=plot.axes([0.715,0.81,0.1,0.06])
            axes_button=Button(ax_axes_button,'axes')
            axes_button.label.set_size(14)
            
            # The 'subplot' button
            ax_subplot_button=plot.axes([0.61,0.81,0.1,0.06])
            subplot_button=Button(ax_subplot_button,'subplot')
            subplot_button.label.set_size(14)
            
            # The 'text' button
            ax_text_button=plot.axes([0.82,0.81,0.1,0.06])
            text_button=Button(ax_text_button,'text')
            text_button.label.set_size(14)

            # figure margin sliders
            
            ax_left_margin_slider=plot.axes([0.63,0.7,0.30,0.05],
                                            facecolor='#bbbbbb')
            left_margin_slider=Slider(ax_left_margin_slider,'left margin',
                                      0,0.5,valinit=self.left_margin,
                                      valstep=0.005,color='#777777')
            left_margin_slider.label.set_size(14)
            left_margin_slider.valtext.set_size(14)
            
            ax_right_margin_slider=plot.axes([0.63,0.58,0.30,0.05],
                                             facecolor='#bbbbbb')
            right_margin_slider=Slider(ax_right_margin_slider,'right margin',
                                      0,0.5,valinit=self.right_margin,
                                      valstep=0.005,color='#777777')
            right_margin_slider.label.set_size(14)
            right_margin_slider.valtext.set_size(14)
            
            ax_top_margin_slider=plot.axes([0.63,0.52,0.30,0.05],
                                            facecolor='#bbbbbb')
            top_margin_slider=Slider(ax_top_margin_slider,'top margin',
                                      0,0.5,valinit=self.top_margin,
                                      valstep=0.005,color='#777777')
            top_margin_slider.label.set_size(14)
            top_margin_slider.valtext.set_size(14)
            
            ax_bottom_margin_slider=plot.axes([0.63,0.64,0.30,0.05],
                                            facecolor='#bbbbbb')
            bottom_margin_slider=Slider(ax_bottom_margin_slider,'bottom margin',
                                        0,0.5,valinit=self.bottom_margin,
                                        valstep=0.005,color='#777777')
            bottom_margin_slider.label.set_size(14)
            bottom_margin_slider.valtext.set_size(14)

            disable(ax_left_margin_slider)
            disable(ax_right_margin_slider)
            disable(ax_top_margin_slider)
            disable(ax_bottom_margin_slider)

            # axis limit text boxes
            
            ax_xlo_tbox=plot.axes([0.63,0.7,0.30,0.05])
            ax_xhi_tbox=plot.axes([0.63,0.64,0.30,0.05])
            if self.xset==False:
                limt=self.axes.get_xlim()
                self.xlo=limt[0]
                self.xhi=limt[1]
            xlo_tbox=TextBox(ax_xlo_tbox,'x low:',
                             initial=('%5.4g' % self.xlo))
            xhi_tbox=TextBox(ax_xhi_tbox,'x high:',
                             initial=('%5.4g' % self.xhi))
            xlo_tbox.label.set_size(14)
            xhi_tbox.label.set_size(14)
            
            ax_ylo_tbox=plot.axes([0.63,0.58,0.30,0.05])
            ax_yhi_tbox=plot.axes([0.63,0.52,0.30,0.05])
            if self.yset==False:
                limt=self.axes.get_ylim()
                self.ylo=limt[0]
                self.yhi=limt[1]
            ylo_tbox=TextBox(ax_ylo_tbox,'y low:',
                             initial=('%5.4g' % self.ylo))
            yhi_tbox=TextBox(ax_yhi_tbox,'y high:',
                             initial=('%5.4g' % self.yhi))
            ylo_tbox.label.set_size(14)
            yhi_tbox.label.set_size(14)

            disable(ax_xlo_tbox)
            disable(ax_xhi_tbox)
            disable(ax_ylo_tbox)
            disable(ax_yhi_tbox)
            
            # Callback for 'close editor' button
            def close_editor(event):
                self.fig.set_size_inches(6,6,forward=True)

                disable(ax_close_button)
                disable(ax_figure_button)
                disable(ax_axes_button)
                disable(ax_text_button)
                disable(ax_subplot_button)
                #ax_close_button.set_position([1.1,1.1,0.1,0.1])
                #ax_figure_button.set_position([1.1,1.1,0.1,0.1])
                #ax_axes_button.set_position([1.1,1.1,0.1,0.1])
                #ax_text_button.set_position([1.1,1.1,0.1,0.1])
                #ax_subplot_button.set_position([1.1,1.1,0.1,0.1])

                disable(ax_xlo_tbox)
                disable(ax_xhi_tbox)
                disable(ax_ylo_tbox)
                disable(ax_yhi_tbox)
                #ax_xlo_tbox.set_position([1,1,0.111,0.111])
                #ax_xhi_tbox.set_position([1,1,0.112,0.112])
                #ax_ylo_tbox.set_position([1,1,0.113,0.113])
                #ax_yhi_tbox.set_position([1,1,0.114,0.114])

                disable(ax_left_margin_slider)
                disable(ax_right_margin_slider)
                disable(ax_top_margin_slider)
                disable(ax_bottom_margin_slider)
                #ax_left_margin_slider.set_position([1,1,0.103,0.103])
                #ax_bottom_margin_slider.set_position([1,1,0.104,0.104])
                #ax_right_margin_slider.set_position([1,1,0.105,0.105])
                #ax_top_margin_slider.set_position([1,1,0.106,0.106])

                self.ax_left_panel.set_position([0,0,1,1])
                self.ax_right_panel.set_position([1,1,1,1])
                self.axes.set_position([self.left_margin,
                                        self.bottom_margin,
                                        1.0-self.left_margin-self.right_margin,
                                        1.0-self.top_margin-self.bottom_margin])
                self.fig.canvas.draw_idle()
                return

            def figure_editor(event):
                
                instructions.set_text('')
                
                enable(ax_left_margin_slider)
                enable(ax_right_margin_slider)
                enable(ax_top_margin_slider)
                enable(ax_bottom_margin_slider)
                
                disable(ax_xlo_tbox)
                disable(ax_xhi_tbox)
                disable(ax_ylo_tbox)
                disable(ax_yhi_tbox)
                
                self.fig.canvas.draw_idle()
                return

            def axes_editor(event):
                instructions.set_text('')
                
                disable(ax_left_margin_slider)
                disable(ax_right_margin_slider)
                disable(ax_top_margin_slider)
                disable(ax_bottom_margin_slider)

                enable(ax_xlo_tbox)
                enable(ax_xhi_tbox)
                enable(ax_ylo_tbox)
                enable(ax_yhi_tbox)

                self.fig.canvas.draw_idle()
                return

            def margin_update():
                self.axes.set_position([self.left_margin/2.0,
                                        self.bottom_margin,
                                        (1.0-self.left_margin-
                                         self.right_margin)/2.0,
                                        1.0-self.top_margin-self.bottom_margin])
                self.fig.canvas.draw_idle()
                return
                
            def left_margin_update(val):
                self.left_margin=val
                margin_update()
                return
            def right_margin_update(val):
                self.right_margin=val
                margin_update()
                return
            def bottom_margin_update(val):
                self.bottom_margin=val
                margin_update()
                return
            def top_margin_update(val):
                self.top_margin=val
                margin_update()
                return

            def xlim_lo_update(val):
                self.axes.set_xlim([float(val),self.xhi])
                return
            def xlim_hi_update(val):
                self.axes.set_xlim([self.xlo,float(val)])
                return
            def ylim_lo_update(val):
                self.axes.set_ylim([float(val),self.yhi])
                return
            def ylim_hi_update(val):
                self.axes.set_ylim([self.ylo,float(val)])
                return

            close_button.on_clicked(close_editor)
            figure_button.on_clicked(figure_editor)
            axes_button.on_clicked(axes_editor)
            left_margin_slider.on_changed(left_margin_update)
            right_margin_slider.on_changed(right_margin_update)
            top_margin_slider.on_changed(top_margin_update)
            bottom_margin_slider.on_changed(bottom_margin_update)
            xlo_tbox.on_submit(xlim_lo_update)
            xhi_tbox.on_submit(xlim_hi_update)
            ylo_tbox.on_submit(ylim_lo_update)
            yhi_tbox.on_submit(ylim_hi_update)
            
            plot.rc('text',usetex=True)

        plot.show()
        
        # End of function plot_base::show()
        return

    def save(self,filename):
        """
        Save plot to file named ``filename``, using the extension to set
        the file type. If the verbose parameter is greater than zero,
        then this function prints the filename to the screen.
        """
        
        import matplotlib.pyplot as plot
        
        if self.verbose>0:
            print('Saving as',filename,'.')
        plot.savefig(filename)
        # End of function plot_base::save()
        return

    def text(self,tx,ty,textstr,**kwargs):
        """Documentation for o2graph command ``text``:

        Plot text in the data coordinates.

        Command-line arguments: ``<x> <y> <text> [kwargs]``

        The ``text`` command plots text in the data coordinates
        defined by the current axes with the font size determined by
        the value of the parameter ``font``. LaTeX is used for text
        rendering by default, but this setting can be changed using,
        e.g. '-set usetex 0'. Some useful kwargs are fontfamily
        ('serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'),
        fontstyle ('normal', 'italic', 'oblique'), fontsize, color,
        backgroundcolor, rotation, horizontalalignment (ha), and
        verticalalignment (va). Note that you must disable LaTeX
        rendering to change fontfamily or fontstyle.

        If <x> or <y> are strings, then they are passed through the
        ``eval()`` function and converted to floating-point numbers. A
        figure and axes are created using
        :py:func:`o2sclpy.plot_base.canvas()`, if necessary.
        """
        if self.canvas_flag==False:
            self.canvas()
            
        ha_present=False
        for key in kwargs:
            if key=='ha' or key=='horizontalalignment':
                ha_present=True
        if ha_present==False:
            kwargs=dict(kwargs,ha='center')
            
        va_present=False
        for key in kwargs:
            if key=='va' or key=='verticalalignment':
                va_present=True
        if va_present==False:
            kwargs=dict(kwargs,va='center')

        fontsize_present=False
        for key in kwargs:
            if key=='fontsize':
                fontsize_present=True
        if fontsize_present==False:
            kwargs=dict(kwargs,fontsize=self.font)

        if isinstance(tx,str):
            tx=float(eval(tx))
        if isinstance(ty,str):
            ty=float(eval(ty))

        import matplotlib.pyplot as plot
        if self.usetex==False or self.usetex==0:
            print('false')
            plot.rc('text',usetex=False)
        else:
            print('true')
            plot.rc('text',usetex=True)
        
        self.axes.text(tx,ty,textstr,**kwargs)
        
        # End of function plot_base::text()
        return

    def textbox(self,tx,ty,strt,boxprops='',**kwargs):
        """Documentation for o2graph command ``textbox``:

        Plot a box with text.

        Command-line arguments: ``<x1> <y1> <text> [bbox properties] 
        [kwargs]``
        
        Plot text <text> and a box at location <x1> <y1>. For example::
        
          textbox 0.5 0.5 \"$ f(x) $\" \"alpha=0.8,facecolor=white\"

        This command uses the standard axis text function, but adds a
        bounding box with the specified properties. Typical bbox
        properties are boxstyle (Circle, DArrow, LArrow, RArrow,
        Round, Round4, Roundtooth, Sawtooth, Square), alpha, color,
        edgecolor (ec), facecolor (fc), fill, hatch ({'/', '\', '|',
        '-', '+', 'x', 'o', 'O', '.', '*'}), linestyle (ls), and
        linewidth (lw). The keyword arguments are for the text
        properties, and follow those of the text command.

        For more information, see:
        https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.FancyBboxPatch.html
        """
        if self.canvas_flag==False:
            self.canvas()

        ha_present=False
        for key in kwargs:
            if key=='ha':
                ha_present=True
        if ha_present==False:
            kwargs=dict(kwargs,ha='center')
            
        va_present=False
        for key in kwargs:
            if key=='va':
                va_present=True
        if va_present==False:
            kwargs=dict(kwargs,va='center')

        fontsize_present=False
        for key in kwargs:
            if key=='fontsize':
                fontsize_present=True
        if fontsize_present==False:
            kwargs=dict(kwargs,fontsize=self.font)

        if isinstance(tx,str):
            tx=float(eval(tx))
        if isinstance(ty,str):
            ty=float(eval(ty))
            
        self.axes.text(tx,ty,strt,
                       transform=self.axes.transAxes,
                       bbox=string_to_dict(boxprops),**kwargs)
        
        # End of function plot_base::textbox()
        return

    def ttext(self,tx,ty,textstr,**kwargs):
        """Documentation for o2graph command ``ttext``:

        Plot text in window coordinates [(0,0) to (1,1)].

        Command-line arguments: ``<x> <y> <text> [kwargs]``

        The ``ttext`` command plots text in the window coordinates
        [typically (0,0) to (1,1)] with the font size determined by
        the value of the parameter ``font``. LaTeX is used for text
        rendering by default, but this setting can be changed using,
        e.g. '-set usetex 0'. Some useful kwargs are fontfamily,
        fontstyle, fontsize, color, backgroundcolor, rotation,
        horizontalalignment (ha), and verticalalignment (va).
        Specifying fontsize overrides the font parameter. Note that
        you must disable LaTeX rendering to change fontfamily or
        fontstyle.

        If <x> or <y> are strings, then they are passed through the
        ``eval()`` function and converted to floating-point numbers. A
        figure and axes are created using
        :py:func:`o2sclpy.plot_base.canvas()`, if necessary.

        """
        if self.canvas_flag==False:
            self.canvas()
            
        ha_present=False
        for key in kwargs:
            if key=='ha' or key=='horizontalalignment':
                ha_present=True
        if ha_present==False:
            kwargs=dict(kwargs,ha='center')
            
        va_present=False
        for key in kwargs:
            if key=='va' or key=='verticalalignment':
                va_present=True
        if va_present==False:
            kwargs=dict(kwargs,va='center')

        fontsize_present=False
        for key in kwargs:
            if key=='fontsize':
                fontsize_present=True
        if fontsize_present==False:
            kwargs=dict(kwargs,fontsize=self.font)

        transform_present=False
        for key in kwargs:
            if key=='transform':
                transform_present=True
        if transform_present==False:
            kwargs=dict(kwargs,transform=self.axes.transAxes)

        if isinstance(tx,str):
            tx=float(eval(tx))
        if isinstance(ty,str):
            ty=float(eval(ty))

        self.axes.text(tx,ty,textstr,**kwargs)

        # End of function plot_base::ttext()
        return

    def subplots(self,nr,nc=1,**kwargs):
        """
        Documentation for o2graph command ``subplot``:

        Create subplots.

        Command-line arguments: ``<nrows> <ncols> [kwargs]``

        Create a grid of <nrows> by <ncols> subplots. The kwargs
        currently supported are 'sharex=True|False', and
        'sharey=True|False'. Subplots are named 'subplot0',
        'subplot1', ... with the indexes moving to the right before
        proceeding to the next row.

        This command allows ``o2graph`` to track the figure and
        axis objects so the user can easily refer to them.
        """
        
        import matplotlib.pyplot as plot
        
        plot.rc('text',usetex=True)
        plot.rc('font',family='serif')
        plot.rcParams['lines.linewidth']=0.5
        dct=string_to_dict(self.fig_dict)
        if not('fig_size_x' in dct):
            dct['fig_size_x']=6.0
        if not('fig_size_y' in dct):
            dct['fig_size_y']=6.0

        # Make the call to subplots()
        self.fig,axis_temp=plot.subplots(nrows=nr,ncols=nc,
                                         figsize=(dct["fig_size_x"],
                                                  dct["fig_size_y"]),**kwargs)
        
        # Reformulate the axis objects into the axes_dict
        nsub=0
        if nr==1 and nc==1:
            self.axes_dict["subplot0"]=axis_temp
            print('Created new axes named subplot0.')
            nsub=1
        elif nr==1:
            for i in range(0,nc):
                self.axes_dict["subplot"+str(i)]=axis_temp[i]
                print('Created new axes named subplot'+str(i)+'.')
            nsub=nc
        elif nc==1:
            for i in range(0,nr):
                self.axes_dict["subplot"+str(i)]=axis_temp[i]
                print('Created new axes named subplot'+str(i)+'.')
            nsub=nr
        else:
            cnt=0
            for i in range(0,nr):
                for j in range(0,nc):
                    self.axes_dict["subplot"+str(cnt)]=axis_temp[i][j]
                    print('Created new axes named subplot'+str(cnt)+'.')
                    cnt=cnt+1
            nsub=cnt

        # Apply default preferences to the axes, similar to
        # default_plot().
        for i in range(0,nsub):
            axt=self.axes_dict["subplot"+str(i)]
            axt.minorticks_on()
            axt.tick_params('both',length=12,width=1,which='major')
            axt.tick_params('both',length=5,width=1,
                            which='minor')
            axt.tick_params(labelsize=self.font*0.8)

        # Flip the canvas flag
        self.canvas_flag=True
        
        # End of function plot_base::subplots()
        return

    def xtitle(self,textstr):
        """
        Add a title for the x-axis
        """

        # Note that this function no longer works inside of yt
        # visualizations because they need to be accessible for
        # annotations on top of yt
        
        if textstr!='' and textstr!='none':
            if self.canvas_flag==False:
                self.canvas()
            self.axes.set_xlabel(textstr,fontsize=self.font)
            
        # End of function plot_base::xtitle()
        return
            
    def ytitle(self,textstr):
        """
        Add a title for the y-axis
        """

        # Note that this function no longer works inside of yt
        # visualizations because they need to be accessible for
        # annotations on top of yt
        
        if textstr!='' and textstr!='none':
            if self.canvas_flag==False:
                self.canvas()
            self.axes.set_ylabel(textstr,fontsize=self.font)
        # End of function plot_base::ytitle()
        return
    
    def selax(self,name=''):
        """
        Documentation for o2graph command ``selax``:

        Select an axis from the current list of axes

        Command-line arguments: ``[name]``

        Select which axis to use for subsequent plotting commands. If
        [name] is not specified, then the names of all current axes
        objects are listed.
        """

        if name=='':
            print('Axes names:',self.axes_dict.keys())
        elif len(str(name))==1 or len(str(name))==2:
            self.axes=self.axes_dict["subplot"+str(name)]
        else:
            self.axes=self.axes_dict[name]
        
        # End of function plot_base::selax()
        return

    def inset(self,left,bottom,width,height,**kwargs):
        """Documentation for o2graph command ``inset``:
        
        Add a new set of axes
        
        Command-line arguments: ``<left> <bottom> <width> <height>
        [kwargs]``

        This command creates a new set of axes, adds the new axes to
        the list of axes, and sets the new axes as the current. The
        values <left>, <bottom>, <width>, and <height> refer to a
        normalized coordinate system where the lower-left hand corner
        of the figure is (0,0) and the upper-right hand corner is
        (1,1). The axes object is named 'inset0' for the first inset,
        then 'inset1', and so on. For example::

            o2graph -inset 0.5 0.2 0.4 0.4 -selax main \\
            -line 100 100 900 900 -selax inset0 \\
            -line 0.1 0.9 0.9 0.1 -show
        """
        if self.canvas_flag==False:
            self.canvas()
            
        # Create a unique axes label i.e. inset0
        ifound=9
        for i in range(0,8):
            if ifound==9:
                axname="inset"+str(i)
                if axname not in self.axes_dict:
                    ifound=i
        axname="inset"+str(ifound)
        self.axes=self.fig.add_axes([left,bottom,width,height],
                                    label=axname)
        self.axes_dict[axname]=self.axes
        print('Created new axes named',axname)
        
        # the same defaults as default_plot()
        self.axes.minorticks_on()
        self.axes.tick_params('both',length=12,width=1,which='major')
        self.axes.tick_params('both',length=5,width=1,which='minor')
        self.axes.tick_params(labelsize=self.font*0.8)
        
    def modax(self,**kwargs):
        """
        Documentation for o2graph command ``modax``:

        Modify current axes properties.

        Command-line arguments: ``[kwargs]``

        The axis properties which can be modified are::

            Property         Values       Description \\
            alpha            float>0      alpha value for region inside axes \\
            labelsize        float>0      font size for labels \\
            x_loc            b,t,tb       placement of x-axis (bottom, top, or both) \\
            x_major_loc      float>0      linear increment for x-axis major ticks \\
            x_minor_loc      float>0      linear increment for x-axis minor ticks \\
            x_minor_tick_dir in,out,inout direction of x-axis minor ticks \\
            x_minor_tick_len float>0      length of x-axis minor ticks \\
            x_minor_tick_wid float>0      width of x-axis minor ticks \\
            x_tick_dir       in,out,inout direction of x-axis major ticks \\
            x_tick_len       float>0      length of x-axis major ticks \\
            x_tick_wid       float>0      width of x-axis major ticks \\
            x_visible        T/F          set x-axis visible or invisible \\
            y_loc            l,r,lr       placement of y-axis (left, right, or both) \\
            y_major_loc      float>0      linear increment for x-axis major ticks \\
            y_minor_loc      float>0      linear increment for x-axis minor ticks \\
            y_minor_tick_dir in,out,inout direction of y-axis minor ticks \\
            y_minor_tick_len float>0      length of y-axis minor ticks \\
            y_minor_tick_wid float>0      width of y-axis minor ticks \\
            y_tick_dir       in,out,inout direction of y-axis major ticks \\
            y_tick_len       float>0      length of y-axis major ticks \\
            y_tick_wid       float>0      width of y-axis major ticks \\
            y_visible        T/F          set y-axis visible or invisible \\

        """

        import matplotlib.pyplot as plot
        
        if 'x_major_loc' in kwargs:
            self.axes.get_xaxis().set_major_locator(plot.MultipleLocator
                                        (float(kwargs['x_major_loc'])))
        if 'x_minor_loc' in kwargs:
            self.axes.get_xaxis().set_minor_locator(plot.MultipleLocator
                                        (float(kwargs['x_minor_loc'])))
            
        if 'y_major_loc' in kwargs:
            self.axes.get_yaxis().set_major_locator(plot.MultipleLocator
                                        (float(kwargs['y_major_loc'])))
        if 'y_minor_loc' in kwargs:
            self.axes.get_yaxis().set_minor_locator(plot.MultipleLocator
                                        (float(kwargs['y_minor_loc'])))
            
        if 'x_visible' in kwargs:
            if kwargs['x_visible']=='False':
                self.axes.get_xaxis().set_visible(False)
        if 'y_visible' in kwargs:
            if kwargs['y_visible']=='False':
                self.axes.get_yaxis().set_visible(False)
                
        if 'labelsize' in kwargs:
            self.axes.tick_params(labelsize=float(kwargs['labelsize']))
                
        if 'alpha' in kwargs:
            self.axes.patch.set_alpha(float(kwargs['alpha']))

        if 'y_loc' in kwargs:
            if kwargs['y_loc']=='rl' or kwargs['y_loc']=='lr':
                self.axes.tick_params('y',which='both',
                                      right=True,left=True,labelright=True,
                                      labelleft=True)
            elif kwargs['y_loc']=='l':
                self.axes.tick_params('y',which='both',left=True,
                                      labelleft=True,right=False,
                                      labelright=False)
            elif kwargs['y_loc']=='r':
                self.axes.tick_params('y',which='both',right=True,
                                      labelright=True,left=False,
                                      labelleft=False)
            
        if 'x_loc' in kwargs:
            if kwargs['x_loc']=='bt' or kwargs['x_loc']=='tb':
                self.axes.tick_params('x',which='both',bottom=True,top=True,
                                      labelbottom=True,labeltop=True)
            elif kwargs['x_loc']=='t':
                self.axes.tick_params('x',which='both',top=True,
                                      labeltop=True,bottom=False,
                                      labelbottom=False)
            elif kwargs['x_loc']=='b':
                self.axes.tick_params('x',which='both',bottom=True,
                                      labelbottom=True,top=False,
                                      labeltop=False)
            
        if 'x_tick_dir' in kwargs:
            self.axes.tick_params('x',which='major',
                                  direction=kwargs['x_tick_dir'])
        if 'x_minor_tick_dir' in kwargs:
            self.axes.tick_params('x',which='minor',
                                  direction=kwargs['x_minor_tick_dir'])
                
        if 'y_tick_dir' in kwargs:
            self.axes.tick_params('y',which='major',
                                  direction=kwargs['y_tick_dir'])
        if 'y_minor_tick_dir' in kwargs:
            self.axes.tick_params('y',which='minor',
                                  direction=kwargs['y_minor_tick_dir'])
            
        if 'x_tick_len' in kwargs:
            self.axes.tick_params('x',which='major',
                                  length=kwargs['x_tick_len'])
        if 'x_minor_tick_len' in kwargs:
            self.axes.tick_params('x',which='minor',
                                  length=kwargs['x_minor_tick_len'])
                
        if 'y_tick_len' in kwargs:
            self.axes.tick_params('y',which='major',
                                  length=float(kwargs['y_tick_len']))
        if 'y_minor_tick_len' in kwargs:
            self.axes.tick_params('y',which='minor',
                                  length=float(kwargs['y_minor_tick_len']))

        if 'x_tick_wid' in kwargs:
            self.axes.tick_params('x',which='major',
                                  width=kwargs['x_tick_wid'])
        if 'x_minor_tick_wid' in kwargs:
            self.axes.tick_params('x',which='minor',
                                  width=kwargs['x_minor_tick_wid'])
                
        if 'y_tick_wid' in kwargs:
            self.axes.tick_params('y',which='major',
                                  width=float(kwargs['y_tick_wid']))
        if 'y_minor_tick_wid' in kwargs:
            self.axes.tick_params('y',which='minor',
                                  width=float(kwargs['y_minor_tick_wid']))
        return
    
    def addcbar(self,left,bottom,width,height,image='last',cmap='',**kwargs):
        """Documentation for o2graph command ``addcbar``:
        
        Add a color bar.
        
        Command-line arguments: ``<left> <bottom> <width> <height>
        [kwargs]``

        Add a new colorbar or a colorbar from the most recently
        created image at the location specified by ``left``,
        ``bottom``, ``width`` and ``height``. This command has a
        keyword ``image`` which specifies the image which the colorbar
        should refer to. If the image keyword is 'last', then the last
        density plot (e.g. from command ``den-plot``) or
        two-dimensional histogram plot (e.g. from command
        ``hist2d-plot``) is used. If the image keyword is 'new', then
        a colormap must be specified using the 'cmap' keyword and the
        color map is used to create the colorbar.
        """

        import matplotlib.pyplot as plot
        
        # Create a unique axes label i.e. cbar0
        ifound=9
        for i in range(0,8):
            if ifound==9:
                axname="cbar"+str(i)
                if axname not in self.axes_dict:
                    ifound=i
        axname="cbar"+str(ifound)
        if cmap[0:5]=='cmyt.':
            import cmyt
                
        if image=='last':
            self.axes=self.fig.add_axes([left,bottom,width,height])
            self.axes_dict[axname]=self.axes
            print('Created new axes named',axname)
            cbar=self.fig.colorbar(self.last_image,cax=self.axes,**kwargs)
            cbar.ax.tick_params(labelsize=self.font*0.8)
        elif image=='new':
            self.axes=self.fig.add_axes([left,bottom,width,height])
            # This doesn't work and I'm not quite sure why yet
            #axis_temp.set_frame_on(False)
            self.axes_dict[axname]=self.axes
            print('Created new axes named',axname)
            if cmap=='':
                print('New colorbar needs colormap in addcbar().')
                return
            tempsm=plot.cm.ScalarMappable(cmap=cmap,
                                          norm=plot.Normalize(vmin=0,vmax=1))
            cbar=self.fig.colorbar(tempsm,cax=self.axes,
                                   orientation='horizontal')
            cbar.ax.tick_params(labelsize=0,length=0)
        else:
            print('Invalid value of image in addcbar().')
            return
        
        # End of function plot_base::addcbar()
        return

    def canvas(self):
        """Documentation for o2graph command ``canvas``:

        Create a plotting canvas.

        Command-line arguments: (No arguments.)

        Create an empty plotting canvas. For example 'o2graph -canvas
        -show'. Typically, 'o2graph' creates the canvas automatically
        when the first object is plotted so explicitly using this
        command is unnecessary.

        This function creates a default figure using default_plot()
        and axis object using the xtitle and ytitle for the
        axis titles and xlo, xhi, ylo, and yhi for the axis limits.
        """
        if self.verbose>2:
            print('Canvas',self.fig_dict)

        dct=string_to_dict(self.fig_dict)
        if 'dpi' in dct.keys():
            import matplotlib.pyplot as plot
            plot.rcParams['figure.dpi']=dct['dpi']
            del dct['dpi']
            
        if 'fontsize' not in dct.keys():
            dct['fontsize']=self.font
        if self.editor:
            (self.fig,self.axes,self.ax_left_panel,
             self.ax_right_panel)=default_plot(**dct,editor=True)
        else:
            (self.fig,self.axes)=default_plot(**dct)

        # Add axes object to the dictionary
        self.axes_dict["main"]=self.axes
        
        # Plot limits
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)

        # Set log mode for x and y axes if requested
        if self.logx==True:
            self.axes.set_xscale('log')
        if self.logy==True:
            self.axes.set_yscale('log')
            
        self.canvas_flag=True
        # End of function plot_base::canvas()
        return

    # def move_labels(self):
    #     """
    #     Move tick labels
    #     """
    #     for label in self.axes.get_xticklabels():
    #         t=label.get_position()
    #         t2=t[0],t[1]-0.01
    #         label.set_position(t2)
    #         label.set_fontsize(16)
    #     for label in self.axes.get_yticklabels():
    #         t=label.get_position()
    #         t2=t[0]-0.01,t[1]
    #         label.set_position(t2)
    #         label.set_fontsize(16)
    #     # End of function plot_base::move_labels()
    #     return

    def plot(self,args,**kwargs):
        """Plot a two-dimensional set of data
        
        The argument list ``args`` can be of the form ``[table,column
        name 1, column name 2]`` or ``[table_units,column name
        1,column name 2]`` or ``[shared_ptr_table_units, column name
        1, column name 2]`` or ``[hist]`` or ``[vec_vec_double,
        column index 1]`` or ``[vec_vec_double, column index1, column
        index 2]``. Otherwise, ``args[0]`` and ``args[1]`` are
        interpreted as arrays to be directly sent to the
        matplotlib.pyplot.plot() function.

        The documentation for the o2graph ``plot`` command is 
        in the docstring for
        :py:func:`o2sclpy.o2graph_plotter.plot_o2graph()`.
        """

        if len(args)<2:
            print('Failed, not enough information to plot.')
            return

        if (str(type(args[0]))=='<class \'o2sclpy.base.table\'>' or
            str(type(args[0]))=='<class \'o2sclpy.base.table_units\'>' or
            str(type(args[0]))==
            '<class \'o2sclpy.base.shared_ptr_table_units\'>'):
            
            failed=False

            tab=args[0]
            xv=tab[force_bytes(args[1])][0:tab.get_nlines()]
            yv=tab[force_bytes(args[2])][0:tab.get_nlines()]
            
        elif str(type(args[0]))=='<class \'o2sclpy.other.hist\'>':

            if self.link2==0:
                print('o2scl library dll not set.')
                return
            
            failed=False

            h=args[0]
            n=h.size()
            yv=[h[i] for i in range(0,n)]
            reps=std_vector(self.link2)
            h.create_rep_vec(reps)
            xv=[reps[i] for i in range(0,n)]

        elif str(type(args[0]))=='<class \'o2sclpy.base.std_vector_vector\'>':
            
            failed=False

            if len(args)>2:
                vvd=args[0]
                n1=len(vvd[int(args[1])])
                n2=len(vvd[int(args[2])])
                if n1<n2:
                    xv=vvd[int(args[1])][0:n1]
                    yv=vvd[int(args[2])][0:n1]
                else:
                    xv=vvd[int(args[1])][0:n2]
                    yv=vvd[int(args[2])][0:n2]
            else:
                vvd=args[0]
                n1=len(vvd[int(args[1])])
                xv=[i for i in range(0,n1)]
                yv=vvd[int(args[1])]

        else:

            failed=False
            
            xv=args[0]
            yv=args[1]
            
        if failed==False:
    
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
                    self.axes.loglog(xv,yv,**kwargs)
                else:
                    self.axes.semilogx(xv,yv,**kwargs)
            else:
                if self.logy==True:
                    self.axes.semilogy(xv,yv,**kwargs)
                else:
                    self.axes.plot(xv,yv,**kwargs)

            # AWS, added 5/3/23, I think this should be here?
            if self.xset==True:
                self.axes.set_xlim(self.xlo,self.xhi)
            if self.yset==True:
                self.axes.set_ylim(self.ylo,self.yhi)
                            
        return

    def den_plot(self,args,**kwargs):
        """Create a density plot from a matrix, a slice of a table3d object,
        or a hist_2d object.

        The argument list ``args`` can be of the form ``[numpy
        matrix]`` or ``[table3d,slice name]`` or ``[hist_2d]``.

        The documentation for the o2graph ``den-plot`` command is in
        the docstring for
        :py:func:`o2sclpy.o2graph_plotter.den_plot_o2graph()`.

        If a cmyt colormap is used, then the ``cmyt`` Python package is
        required.
        """
        
        if len(args)<1:
            print('Failed, not enough information to plot.')
            return

        val=kwargs.pop('pcm',None)
        if val==True:
            pcm=True
        else:
            pcm=False

        # If necessary, import cmyt for the cmyt colormaps
        if 'cmap' in kwargs and kwargs['cmap'][0:5]=='cmyt.':
            import cmyt
            
        extent_from_grid=False
            
        if str(type(args[0]))=='<class \'o2sclpy.base.table3d\'>':

            table3d=args[0]
            slice_name=args[1]
            nxt=table3d.get_nx()
            nyt=table3d.get_ny()
            sl=table3d.get_slice(slice_name).to_numpy()
            sl=sl.transpose()
            xgrid=[table3d.get_grid_x(i) for i in range(0,nxt)]
            ygrid=[table3d.get_grid_y(i) for i in range(0,nyt)]

            if pcm==False:
                extent_from_grid=True

        elif str(type(args[0]))=='<class \'o2sclpy.other.hist_2d\'>':

            h2d=args[0]
            nxt=h2d.size_x()
            nyt=h2d.size_y()
            sl=h2d.get_wgts().to_numpy()
            sl=sl.transpose()

            if pcm==False:
                extent1=h2d.get_x_low_i(0)
                extent2=h2d.get_x_high_i(nxt-1)
                extent3=h2d.get_y_low_i(0)
                extent4=h2d.get_y_high_i(nyt-1)
            else:
                if self.link2==0:
                    print('o2scl library dll not set.')
                    return
                xgrid=o2sclpy.std_vector_size_t(self.link2)
                ygrid=o2sclpy.std_vector_size_t(self.link2)
                h2d.create_x_rep_vec(xgrid)
                h2d.create_y_rep_vec(ygrid)

        elif str(type(args[0]))=='<class \'o2sclpy.base.tensor\'>':

            ten=args[0]
            rk=ten.get_rank()

            if rk<2:
                print('Must have rank of at least 2.')
            
            nx=ten.get_size(0)
            ny=ten.get_size(1)
            
            sl=numpy.zeros((nx,ny))
            ix=[0 for i in range(0,rk)]
            for i in range(0,nx):
                for j in range(0,ny):
                    ix[0]=i
                    ix[1]=j
                    sl[i][j]=ten.get(ix)

            xgrid=[i for i in range(0,nx)]
            ygrid=[j for j in range(0,ny)]

            if pcm==False:
                extent_from_grid=True
            
        elif str(type(args[0]))=='<class \'o2sclpy.base.tensor_grid\'>':
                
            ten=args[0]
            rk=ten.get_rank()

            if rk<2:
                print('Must have rank of at least 2.')
            
            nx=ten.get_size(0)
            ny=ten.get_size(1)
            
            sl=numpy.zeros((nx,ny))
            ix=[0 for i in range(0,rk)]
            for i in range(0,nx):
                for j in range(0,ny):
                    ix[0]=i
                    ix[1]=j
                    sl[i][j]=ten.get(ix)

            xgrid=[ten.get_grid(0,i) for i in range(0,nx)]
            ygrid=[ten.get_grid(1,j) for j in range(0,ny)]

            if pcm==False:
                extent_from_grid=True
            
        elif len(args)<3:

            sl=args[0]
            sl=sl.transpose()
            shap=sl.shape()
            nxt=shap[0]
            xyt=shap[1]
            xgrid=[i for i in range(0,nxt)]
            ygrid=[i for i in range(0,nyt)]

            if pcm==False:
                extent_from_grid=True
            
        else:

            xgrid=args[0]
            ygrid=args[1]
            nxt=len(xgrid)
            nyt=len(ygrid)
            sl=args[2]
            sl=sl.transpose()

            if pcm==False:
                extent_from_grid=True
                
        if extent_from_grid==True:
                
            if self.logx==True:
                xgrid=[math.log(xgrid[i],10) for i in
                       range(0,nxt)]
            if self.logy==True:
                ygrid=[math.log(ygrid[i],10) for i in
                       range(0,nyt)]

            diffs_x=[xgrid[i+1]-xgrid[i] for i in range(0,len(xgrid)-1)]
            mean_x=numpy.mean(diffs_x)
            std_x=numpy.std(diffs_x)
            diffs_y=[ygrid[i+1]-ygrid[i] for i in range(0,len(ygrid)-1)]
            mean_y=numpy.mean(diffs_y)
            std_y=numpy.std(diffs_y)
            
            if std_x/mean_x>1.0e-4 or std_x/mean_x>1.0e-4:
                print('Warning in o2graph::o2graph_plotter::den_plot():')
                print('  Nonlinearity of x or y grid is greater than '+
                      '10^{-4}.')
                print('  Value of std(diff_x)/mean(diff_x): %7.6e .' %
                      (std_x/mean_x))
                print('  Value of std(diff_y)/mean(diff_y): %7.6e .' %
                      (std_y/mean_y))
                print('  The density plot may not be properly scaled.')
                
            extent1=xgrid[0]-(xgrid[1]-xgrid[0])/2
            extent2=xgrid[nxt-1]+(xgrid[nxt-1]-
                                  xgrid[nxt-2])/2
            extent3=ygrid[0]-(ygrid[1]-ygrid[0])/2
            extent4=ygrid[nyt-1]+(ygrid[nyt-1]-
                                  ygrid[nyt-2])/2
            
        # If logz was specified, then manually apply the
        # log to the data. Alternatively, we should consider
        # using 'LogNorm' here, as suggested in
            
        #https://stackoverflow.com/questions/2546475/
        #how-can-i-draw-a-log-normalized-imshow-plot-
        #with-a-colorbar-representing-the-raw

        if self.logz==True:
            fail_found=False
            for i in range(0,nyt):
                for j in range(0,nxt):
                    if sl[i][j]>0.0:
                        sl[i][j]=math.log10(sl[i][j])
                    else:
                        if fail_found==False:
                            print('Failed to take log of',sl[i][j],
                                  'at (i,j)=(',j,',',i,') or (',
                                  xgrid[j],',',ygrid[i],
                                  '). Setting point to zero and',
                                  'suppressing future warnings.')
                        fail_found=True
                        sl[i][j]=0.0

        # If the z range was specified, truncate all values
        # outside that range (this truncation is done after
        # the application of the log above)
        if self.zset==True:
            for i in range(0,nyt):
                for j in range(0,nxt):
                    if sl[i][j]>self.zhi:
                        sl[i][j]=self.zhi
                    elif sl[i][j]<self.zlo:
                        sl[i][j]=self.zlo

        if self.canvas_flag==False:
            self.canvas()
            
        if pcm==True:
            
            print('Creating density plot using pcolormesh()')
            if self.logx==True:
                self.axes.set_xscale('log')
            if self.logy==True:
                self.axes.set_yscale('log')
            self.last_image=self.axes.pcolormesh(xgrid,ygrid,sl,**kwargs)

        else:

            # The imshow() function doesn't work with a log axis, so we
            # set the scales back to linear and manually take the log
            self.axes.set_xscale('linear')
            self.axes.set_yscale('linear')
            
            f=self.axes.imshow
            self.last_image=f(sl,interpolation='nearest',
                              origin='lower',extent=[extent1,extent2,
                                                     extent3,extent4],
                              aspect='auto',**kwargs)

            # AWS 7/1/2020: I'm not sure why imshow() is now
            # apparently mangling the minor tick settings. This
            # restores them. 
            self.axes.minorticks_on()
            self.axes.tick_params('both',length=12,width=1,which='major')
            self.axes.tick_params('both',length=5,width=1,which='minor')
            self.axes.tick_params(labelsize=self.font*0.8)

        if self.colbar==True:
            cbar=self.fig.colorbar(self.last_image,ax=self.axes)
            cbar.ax.tick_params('both',length=6,width=1,which='major')
            cbar.ax.tick_params(labelsize=self.font*0.8)
                
        return
    
    def den_plot_rgb(self,table3d,slice_r,slice_g,slice_b,
                     make_png='',renorm=False,**kwargs):
        """Density plot from a ``table3d`` object using three slices
        to specify the red, green, and blue values.

        If make_png is non-empty, then a .png is created, with no
        axes, and stored in a file given the specified name.
        In the case a .png file is to be created and renorm is 
        True, then the data is renormalized to ensure the minimum
        is 0 and the maximum is 255. Otherwise, the data is 
        set to 0 if it is less than 0 and set to 255 when it is
        greater than 255. 

        The documentation for the o2graph ``den-plot-rgb`` command is
        in the docstring for
        :py:func:`o2sclpy.o2graph_plotter.den_plot_rgb_o2graph()`.

        If the make_png keyword argument is specified, then ``Pillow``
        Python package is required.
        """

        nxt=table3d.get_nx()
        nyt=table3d.get_ny()
        xgrid=[table3d.get_grid_x(i) for i in range(0,nxt)]
        ygrid=[table3d.get_grid_y(i) for i in range(0,nyt)]

        slr=table3d.get_slice(slice_r).to_numpy()
        # Commented out on 11/5 for ima.cpp
        #slr=slr.transpose()
        slg=table3d.get_slice(slice_g).to_numpy()
        # Commented out on 11/5 for ima.cpp
        #slg=slg.transpose()
        slb=table3d.get_slice(slice_b).to_numpy()
        # Commented out on 11/5 for ima.cpp
        #slb=slb.transpose()

        # Allocate the python storage
        sl_all=numpy.zeros((nyt,nxt,3))

        for i in range(0,nxt):
            for j in range(0,nyt):
                sl_all[j,i,0]=slr[i,j]
                sl_all[j,i,1]=slg[i,j]
                sl_all[j,i,2]=slb[i,j]
        
        # If logz was specified, then manually apply the
        # log to the data. Alternatively, we should consider
        # using 'LogNorm' here, as suggested in
            
        # If the z range was specified, truncate all values
        # outside that range (this truncation is done after
        # the application of the log above)
            
        # if self.zset==True:
        #     for i in range(0,ny.value):
        #         for j in range(0,nx.value):
        #             if sl_r[i][j]>self.zhi:
        #                 sl_r[i][j]=self.zhi
        #             elif sl_r[i][j]<self.zlo:
        #                 sl_r[i][j]=self.zlo
        #             if sl_g[i][j]>self.zhi:
        #                 sl_g[i][j]=self.zhi
        #             elif sl_g[i][j]<self.zlo:
        #                 sl_g[i][j]=self.zlo
        #             if sl_b[i][j]>self.zhi:
        #                 sl_b[i][j]=self.zhi
        #             elif sl_b[i][j]<self.zlo:
        #                 sl_b[i][j]=self.zlo

        if len(make_png)>0:
            try:
                from PIL import Image
                im=Image.new(mode='RGB',size=(nxt,nyt))
                pixels=im.load()
            except Exception as e:
                print('Exception in den_plot_rgb() create image',e)
                raise

            if renorm:
                min_val=sl_all[0,0,0]
                max_val=sl_all[0,0,0]
            
                for i in range(0,nxt):
                    for j in range(0,nyt):
                        if sl_all[j,i,0]<min_val:
                            min_val=sl_all[j,i,0]
                        if sl_all[j,i,1]<min_val:
                            min_val=sl_all[j,i,1]
                        if sl_all[j,i,2]<min_val:
                            min_val=sl_all[j,i,2]
                        if sl_all[j,i,0]>max_val:
                            max_val=sl_all[j,i,0]
                        if sl_all[j,i,1]>max_val:
                            max_val=sl_all[j,i,1]
                        if sl_all[j,i,2]>max_val:
                            max_val=sl_all[j,i,2]

                print('o2graph::den_plot_rgb (make-png)(): Minimum is',
                      min_val,'maximum is',max_val,'.')
                        
                for i in range(0,nxt):
                    for j in range(0,nyt):
                        pixels[i,j]=(int(256*(sl_all[j,i,0]-min_val)/
                                         (max_val-min_val)),
                                     int(256*(sl_all[j,i,1]-min_val)/
                                         (max_val-min_val)),
                                     int(256*(sl_all[j,i,2]-min_val)/
                                         (max_val-min_val)))
            else:
                for i in range(0,nxt):
                    for j in range(0,nyt):
                        if sl_all[j,i,0]<0:
                            sl_all[j,i,0]=0
                        if sl_all[j,i,1]<0:
                            sl_all[j,i,1]=0
                        if sl_all[j,i,2]<0:
                            sl_all[j,i,2]=0
                        if sl_all[j,i,0]>255:
                            sl_all[j,i,0]=255
                        if sl_all[j,i,1]>255:
                            sl_all[j,i,1]=255
                        if sl_all[j,i,2]>255:
                            sl_all[j,i,2]=255
                        pixels[i,j]=(int(sl_all[j,i,0]),
                                     int(sl_all[j,i,1]),
                                     int(sl_all[j,i,2]))

            try:
                im.save(make_png,optimize=True)
            except Exception as e:
                print('Exception in den_plot_rgb() save image',e)
                raise
            return
        
        if renorm:
            min_val=sl_all[0,0,0]
            max_val=sl_all[0,0,0]
            
            for i in range(0,nxt):
                for j in range(0,nyt):
                    if sl_all[j,i,0]<min_val:
                        min_val=sl_all[j,i,0]
                    if sl_all[j,i,1]<min_val:
                        min_val=sl_all[j,i,1]
                    if sl_all[j,i,2]<min_val:
                        min_val=sl_all[j,i,2]
                    if sl_all[j,i,0]>max_val:
                        max_val=sl_all[j,i,0]
                    if sl_all[j,i,1]>max_val:
                        max_val=sl_all[j,i,1]
                    if sl_all[j,i,2]>max_val:
                        max_val=sl_all[j,i,2]

            print('o2graph::den_plot_rgb(): Minimum is',
                  min_val,'maximum is',max_val,'.')
                        
            for i in range(0,nxt):
                for j in range(0,nyt):
                    sl_all[j,i,0]=((sl_all[j,i,0]-min_val)/
                                   (max_val-min_val))
                    sl_all[j,i,1]=((sl_all[j,i,1]-min_val)/
                                   (max_val-min_val))
                    sl_all[j,i,2]=((sl_all[j,i,2]-min_val)/
                                   (max_val-min_val))
                    
        if self.canvas_flag==False:
            self.canvas()

        # The imshow() function doesn't work with a log axis, so we
        # set the scales back to linear and manually take the log
        self.axes.set_xscale('linear')
        self.axes.set_yscale('linear')
            
        if self.logx==True:
            xgrid=[math.log(ptrx[i],10) for i in
                   range(0,nxt)]
        if self.logy==True:
            ygrid=[math.log(ptry[i],10) for i in
                   range(0,nyt)]

        diffs_x=[xgrid[i+1]-xgrid[i] for i in range(0,len(xgrid)-1)]
        mean_x=numpy.mean(diffs_x)
        std_x=numpy.std(diffs_x)
        diffs_y=[ygrid[i+1]-ygrid[i] for i in range(0,len(ygrid)-1)]
        mean_y=numpy.mean(diffs_y)
        std_y=numpy.std(diffs_y)
            
        if std_x/mean_x>1.0e-4 or std_x/mean_x>1.0e-4:
            print('Warning in plot_base::den_plot_rgb():')
            print('  Nonlinearity of x or y grid is greater than '+
                  '10^{-4}.')
            print('  Value of std(diff_x)/mean(diff_x): %7.6e .' %
                  (std_x/mean_x))
            print('  Value of std(diff_y)/mean(diff_y): %7.6e .' %
                  (std_y/mean_y))
            print('  The density plot may not be properly scaled.')
                
        extent1=xgrid[0]-(xgrid[1]-xgrid[0])/2
        extent2=xgrid[nxt-1]+(xgrid[nxt-1]-
                                   xgrid[nxt-2])/2
        extent3=ygrid[0]-(ygrid[1]-ygrid[0])/2
        extent4=ygrid[nyt-1]+(ygrid[nyt-1]-
                                   ygrid[nyt-2])/2
                        
        f=self.axes.imshow
        self.last_image=f(sl_all,
                          interpolation='nearest',
                          origin='lower',extent=[extent1,extent2,
                                                 extent3,extent4],
                          aspect='auto',**kwargs)

        if self.colbar==True:
            cbar=self.fig.colorbar(self.last_image,ax=self.axes)
            cbar.ax.tick_params('both',length=6,width=1,which='major')
            cbar.ax.tick_params(labelsize=self.font*0.8)

        return

    def make_png(self,table3d,slice_r,slice_g,slice_b,fname,**kwargs):
        """Create png from a ``table3d`` object using three slices
        to specify the red, green, and blue values.

        The documentation for the o2graph ``make-png`` command is in
        the docstring for
        :py:func:`o2sclpy.o2graph_plotter.make_png_o2graph()`.

        This command requires the ``Pillow`` Python package.

        """
        
        nxt=table3d.get_nx()
        nyt=table3d.get_ny()
        xgrid=[table3d.get_grid_x(i) for i in range(0,nxt)]
        ygrid=[table3d.get_grid_y(i) for i in range(0,nyt)]

        slr=table3d.get_slice(slice_r).to_numpy()
        slr=slr.transpose()
        slg=table3d.get_slice(slice_g).to_numpy()
        slg=slg.transpose()
        slb=table3d.get_slice(slice_b).to_numpy()
        slb=slb.transpose()

        # Allocate the python storage
        sl_all=numpy.zeros((nyt,nxt,3))

        for i in range(0,nxt):
            for j in range(0,nyt):
                sl_all[j,i,0]=slr[i,j]
                sl_all[j,i,1]=slg[i,j]
                sl_all[j,i,2]=slb[i,j]
        
        from PIL import Image
        im=Image.new(mode='RGB',size=(nxt,nyt))
        pixels=im.load()
            
        min_val=sl_all[0,0,0]
        max_val=sl_all[0,0,0]
            
        for i in range(0,nxt):
            for j in range(0,nyt):
                if sl_all[j,i,0]<min_val:
                    min_val=sl_all[j,i,0]
                if sl_all[j,i,1]<min_val:
                    min_val=sl_all[j,i,1]
                if sl_all[j,i,2]<min_val:
                    min_val=sl_all[j,i,2]
                if sl_all[j,i,0]>max_val:
                    max_val=sl_all[j,i,0]
                if sl_all[j,i,1]>max_val:
                    max_val=sl_all[j,i,1]
                if sl_all[j,i,2]>max_val:
                    max_val=sl_all[j,i,2]

        print('plot_base::make-png(): Minimum is',
              min_val,'maximum is',max_val,'.')
                        
        for i in range(0,nxt):
            for j in range(0,nyt):
                pixels[i,j]=(int(256*(sl_all[j,i,0]-min_val)/
                                 (max_val-min_val)),
                             int(256*(sl_all[j,i,1]-min_val)/
                                 (max_val-min_val)),
                             int(256*(sl_all[j,i,2]-min_val)/
                                 (max_val-min_val)))

        im.save(fname,optimize=True)
            
        return
    
