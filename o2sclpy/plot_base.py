#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2022, Andrew W. Steiner
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
import platform

# To create new color maps
from matplotlib.colors import LinearSegmentedColormap

# For rectangles and ellipses
import matplotlib.patches as patches

from o2sclpy.utils import parse_arguments, string_to_dict
from o2sclpy.utils import force_bytes, default_plot, get_str_array
from o2sclpy.utils import string_to_color

class plot_base:
    """
    A base class for plotting classes :py:class:`o2sclpy.plotter` and
    :py:class:`o2sclpy.o2graph_plotter` . The principal purpose
    of this class is just to provide some additional simplification
    to python code which makes plots using matplotlib.

    """

    cbar=0
    """ 
    Colorbar?
    """

    last_image=0
    """
    The last image object created (used for addcbar)
    """
    axes=0
    """ 
    Axis object
    """
    axes_dict={}
    """
    Dictionary of axis objects 
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
    If True, then include a color legend for density plots (default False)
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
    Font size for :py:func:`o2sclpy.plot_base.text()`,
    :py:func:`o2sclpy.plot_base.ttext()`, and axis titles (default
    16). Axis labels are set by this size times 0.8 .
    """
    fig_dict=''
    """
    A dictionary which refers to the figure and axis defaults for
    :py:func:`o2sclpy.default_plot()`. The default value is
    ``('fig_size_x=6.0,fig_size_y=6.0,ticks_in=False,'+
    'rt_ticks=False,left_margin=0.14,right_margin=0.04,'+
    'bottom_margin=0.12,top_margin=0.04,fontsize=16')`` . The x and y
    sizes of the figure object are in fig_size_x and fig_size_y. The
    value ticks_in refers to whether or not the ticks are inside or
    outside the plot. The value of rt_ticks refers to whether or not
    tick marks are plotted on the right and top sides of the plot. The
    font size parameter is multiplied by 0.8 and then used for the
    axis labels.
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
    If true, open the editor
    """
    ax_left_panel=0
    ax_right_panel=0
    
    def __init__(self):
        """
        Desc
        """
        self.new_cmaps()
    
    def cmap(self,cmap_name,col_list):
        """Documentation for o2graph command ``cmap``:

        Create a continuous colormap.

        Command-line arguments: ``<cmap name> <color 1> <color 2> 
        [color3]...``

        Create a new color map named <cmap name> which consists of
        equal-sized gradients between the specified list of at least
        two colors. Matplotlib colors, (r,g,b) colors, and xkcd colors
        are all allowed. For example 'o2graph -cmap c forestgreen
        \"(0.5,0.5,0.7)\" \"xkcd:light red\" -create table3d x
        grid:0,40,1 y grid:0,40,1 z \"x+y\" -den-plot z cmap=c -show'.
        """

        if self.verbose>1:
            print('cmap name:',cmap_name,'list:',col_list)
        
        # This value is used to indicate values in the colormap
        # tuples that are ignored by LinearSegmentedColormap()
        unused=0.0

        N=len(col_list)
        
        col_r=numpy.ones((N,3))
        col_g=numpy.ones((N,3))
        col_b=numpy.ones((N,3))

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
            if i==0:
                col_r[i][1]=unused
                col_g[i][1]=unused
                col_b[i][1]=unused
                col_r[i][2]=rgb_list[0][0]
                col_g[i][2]=rgb_list[0][1]
                col_b[i][2]=rgb_list[0][2]
            elif i==N-1:
                col_r[i][1]=rgb_list[N-1][0]
                col_g[i][1]=rgb_list[N-1][1]
                col_b[i][1]=rgb_list[N-1][2]
                col_r[i][2]=unused
                col_g[i][2]=unused
                col_b[i][2]=unused
            else:
                col_r[i][1]=rgb_list[i][0]
                col_g[i][1]=rgb_list[i][1]
                col_b[i][1]=rgb_list[i][2]
                col_r[i][2]=rgb_list[i][0]
                col_g[i][2]=rgb_list[i][1]
                col_b[i][2]=rgb_list[i][2]

            if self.verbose>1:
                print('red',col_r[i][0],col_r[i][1],col_r[i][2])
                print('green',col_g[i][0],col_g[i][1],col_g[i][2])
                print('blue',col_b[i][0],col_b[i][1],col_b[i][2])
                print('')

        cdict={'red': col_r, 'green': col_g, 'blue': col_b}
        
        import matplotlib.pyplot as plot

        cmap_obj=LinearSegmentedColormap(cmap_name,cdict)
        plot.register_cmap(cmap=cmap_obj)
            
        # Colormap reversed
        cmapr_obj=cmap_obj.reversed()
        plot.register_cmap(cmap=cmapr_obj)
        
        return
        
    def cmap2(self,cmap_name,col_list):
        """Documentation for o2graph command ``cmap2``:

        Create a colormap with sharp transitions

        Command-line arguments: ``<cmap name> <color 1> <color 2>
        [color3 color4]...``

        Create a new color map named <cmap name> which consists of
        equal-sized gradients between the list of specified color
        pairs. Matplotlib colors, (r,g,b) colors, and xkcd colors are
        all allowed. For example 'o2graph -cmap2 c \"(0.5,0.5,0.7)\"
        \"xkcd:light red\" -create table3d x grid:0,40,1 y grid:0,40,1
        z \"x+y\" -den-plot z cmap=c -show'.
        """

        N=len(col_list)
        
        if N%2==1:
            print('Must have an even number of arguments in cmap2.')
            return
        
        if self.verbose>1:
            print('cmap name:',cmap_name,'list:',col_list)
        
        # This value is used to indicate values in the colormap
        # tuples that are ignored by LinearSegmentedColormap()
        unused=0.0

        col_r=numpy.ones((N/2+1,3))
        col_g=numpy.ones((N/2+1,3))
        col_b=numpy.ones((N/2+1,3))

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

        for i in range(0,N/2+1):
            col_r[i][0]=float(i)/float(N-1)
            col_g[i][0]=float(i)/float(N-1)
            col_b[i][0]=float(i)/float(N-1)
            if i==0:
                col_r[i][1]=unused
                col_g[i][1]=unused
                col_b[i][1]=unused
                col_r[i][2]=rgb_list[0][0]
                col_g[i][2]=rgb_list[0][1]
                col_b[i][2]=rgb_list[0][2]
            elif i==N/2:
                col_r[i][1]=rgb_list[N-1][0]
                col_g[i][1]=rgb_list[N-1][1]
                col_b[i][1]=rgb_list[N-1][2]
                col_r[i][2]=unused
                col_g[i][2]=unused
                col_b[i][2]=unused
            else:
                col_r[i][1]=rgb_list[i/2+1][0]
                col_g[i][1]=rgb_list[i/2+1][1]
                col_b[i][1]=rgb_list[i/2+1][2]
                col_r[i][2]=rgb_list[i/2+2][0]
                col_g[i][2]=rgb_list[i/2+2][1]
                col_b[i][2]=rgb_list[i/2+2][2]

            if self.verbose>1:
                print('red',col_r[i][0],col_r[i][1],col_r[i][2])
                print('green',col_g[i][0],col_g[i][1],col_g[i][2])
                print('blue',col_b[i][0],col_b[i][1],col_b[i][2])
                print('')

        cdict={'red': col_r, 'green': col_g, 'blue': col_b}
        
        import matplotlib.pyplot as plot

        cmap_obj=LinearSegmentedColormap(cmap_name,cdict)
        plot.register_cmap(cmap=cmap_obj)
            
        # Colormap reversed
        cmapr_obj=cmap_obj.reversed()
        plot.register_cmap(cmap=cmapr_obj)
        
        return
        
    def new_cmaps(self):
        """
        Add a few new colormaps
        """

        import matplotlib.pyplot as plot

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
            plot.register_cmap(cmap=reds2)
            
            # Colormap reds2, reversed
            reds2_r=reds2.reversed()
            plot.register_cmap(cmap=reds2_r)
            
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
            plot.register_cmap(cmap=jet2)
    
            # Colormap jet2, reversed
            jet2_r=jet2.reversed()
            plot.register_cmap(cmap=jet2_r)
    
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
            plot.register_cmap(cmap=pastel2)
            
            # Colormap pastel2, reversed
            pastel2_r=pastel2.reversed()
            plot.register_cmap(cmap=pastel2_r)
    
            # A white to green colormap
            cdict={'red': ((0.0,unused,1.0),(1.0,0.0,unused)),
                   'green': ((0.0,unused,1.0),(1.0,1.0,unused)),
                   'blue': ((0.0,unused,1.0),(1.0,0.0,unused))}
            greens2=LinearSegmentedColormap('greens2',cdict)
            plot.register_cmap(cmap=greens2)
            
            # Colormap greens2, reversed
            greens2_r=greens2.reversed()
            plot.register_cmap(cmap=greens2_r)
            
            # A white to blue colormap
            cdict={'red': ((0.0,unused,1.0),(1.0,0.0,unused)),
                   'green': ((0.0,unused,1.0),(1.0,0.0,unused)),
                   'blue': ((0.0,unused,1.0),(1.0,1.0,unused))}
            blues2=LinearSegmentedColormap('blues2',cdict)
            plot.register_cmap(cmap=blues2)
            
            # Colormap blues2, reversed
            blues2_r=blues2.reversed()
            plot.register_cmap(cmap=blues2_r)

        # End of function plot_base::new_cmaps()
        return

    def set(self,name,value):
        """
        Set the value of parameter named ``name`` to value ``value``
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
        """
        Output the value of parameter named ``name``
        """
        if name=='colbar':
            print('The value of colbar is',self.colbar,'.')
        if name=='logx':
            print('The value of logx is',self.logx,'.')
        if name=='logy':
            print('The value of logy is',self.logy,'.')
        if name=='logz':
            print('The value of logz is',self.logz,'.')
        if name=='verbose':
            print('The value of verbose is',self.verbose,'.')
        if name=='xhi':
            print('The value of xhi is',self.xhi,'.')
        if name=='xlo':
            print('The value of xlo is',self.xlo,'.')
        if name=='xset':
            print('The value of xset is',self.xset,'.')
        if name=='yhi':
            print('The value of yhi is',self.yhi,'.')
        if name=='ylo':
            print('The value of ylo is',self.ylo,'.')
        if name=='yset':
            print('The value of yset is',self.yset,'.')
        if name=='zhi':
            print('The value of zhi is',self.zhi,'.')
        if name=='zlo':
            print('The value of zlo is',self.zlo,'.')
        if name=='zset':
            print('The value of zset is',self.zset,'.')
        if name=='fig_dict':
            print('The value of fig_dict is',self.fig_dict,'.')
        if name=='yt_axis':
            print('The value of yt_axis is',self.yt_axis,'.')
        if name=='yt_axis_color':
            print('The value of yt_axis_color is',self.yt_axis_color,'.')
        if name=='yt_axis_labels_flat':
            print('The value of yt_axis_labels_flat is',
                  self.yt_axis_labels_flat,'.')
        if name=='yt_axis_resolution':
            print('The value of yt_axis_resolution is',
                  self.yt_axis_resolution,'.')
        if name=='yt_focus':
            print('The value of yt_focus is',self.yt_focus,'.')
        if name=='yt_sigma_clip':
            print('The value of yt_sigma_clip is',self.yt_sigma_clip,'.')
        if name=='yt_position':
            print('The value of yt_position is',self.yt_position,'.')
        if name=='yt_path':
            print('The value of yt_path is',self.yt_path,'.')
        # End of function plot_base::get()
        return

    def xlimits(self,xlo,xhi):
        """
        Set the x-axis limits
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
        Set the y-axis limits
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
        """
        Set the z-axis limits
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
        """
        Plot a line from :math:`(x_1,y_1)` to :math:`(x_2,y_2)`
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

            * arrowstyle=->,connectionstyle=arc3
            * arrowstyle=-|>,connectionstyle=arc,fc=red,ec=blue
            * arrowstyle=-|>,connectionstyle=arc,head_length=4.0,
              head_width=1.0
            * arrowstyle=->,connectionstyle=arc3,head_length=4.0,
              head_width=1.0,rad=-0.1 
            * arrowstyle=fancy,connectionstyle=arc3,head_length=4.0,
              head_width=1.0,rad=-0.1
        
        Summary for arrowstyle argument (angleB is renamed to 
        as_angleB)::

            Name    Attributes
            -       None
            ->      head_length=0.4,head_width=0.2
            -[      widthB=1.0,lengthB=0.2,as_angleB=None
            |-      widthA=1.0,widthB=1.0
            -|      head_length=0.4,head_width=0.2
            <-      head_length=0.4,head_width=0.2
            <|      head_length=0.4,head_width=0.2
            fancy   head_length=0.4,head_width=0.4,tail_width=0.4
            simple  head_length=0.5,head_width=0.5,tail_width=0.2
            wedge   tail_width=0.3,shrink_factor=0.5
        
        (note that fancy, simple or wedge require arc3 or angle3 connection 
        styles)

        Summary for connectionstyle argument (angleB is renamed to 
        cs_angleB)::

            Name    Attributes
            * angle   angleA=90,cs_angleB=0,rad=0.0
            * angle3  angleA=90,cs_angleB=0
            * arc     angleA=0,cs_angleB=0,armA=None,armB=None,rad=0.0
            * arc3    rad=0.0
            * bar     armA=0.0,armB=0.0,fraction=0.3,angle=None

        See https://matplotlib.org/2.0.2/users/annotations.html for more.

        """
        if self.verbose>2:
            print('Arrow',x1,y1,x2,y1,arrowprops)
        if self.canvas_flag==False:
            self.canvas()
        self.axes.annotate("",xy=(float(eval(x2)),float(eval(y2))),
                           xycoords='data',
                           xytext=(float(eval(x1)),float(eval(y1))),
                           textcoords='data',
                           arrowprops=string_to_dict(arrowprops))
        # End of function plot_base::arrow()
        return

    def point(self,xval,yval,**kwargs):
        """
        Plot a point at location (xval,yval)
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
        Plot a point at location (xval,yval)
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
        """
        Plot a rectangle from :math:`(x_1,y_1)` to :math:`(x_2,y_2)`
        """
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
        r=patches.Rectangle((left,lower),w,h,angle,**kwargs)
        self.axes.add_patch(r)
        # End of function plot_base::rect()
        return

    def ellipse(self,x,y,w,h,angle=0,**kwargs):
        """
        Plot an ellipse
        """
        if self.verbose>2:
            print('Ellipse',x,y,w,h,angle)
        if self.canvas_flag==False:
            self.canvas()
        fx=float(eval(x))
        fy=float(eval(y))
        fw=float(eval(w))
        fh=float(eval(h))
        fangle=float(eval(angle))
        if self.canvas_flag==False:
            self.canvas()
        r=patches.Ellipse((fx,fy),fw,fh,fangle,**kwargs)
        self.axes.add_patch(r)
        # End of function plot_base::ellipse()
        return

    def show(self):
        """
        Call the ``matplotlib`` show function.
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
        Save plot to file named ``filename``. If the verbose parameter is
        greater than zero, then this function prints the filename to
        the screen.
        """
        
        import matplotlib.pyplot as plot
        
        if self.verbose>0:
            print('Saving as',filename,'.')
        plot.savefig(filename)
        # End of function plot_base::save()
        return

    def ttext(self,tx,ty,textstr,**kwargs):
        """
        Plot text in the native coordinate system using a transAxes
        transformation. This function uses the class font size and and
        centering in the horizontal and vertical directions by
        default. A figure and axes are created using
        :py:func:`o2sclpy.plot_base.canvas()`, if they have not been
        created already. If ``tx`` and ``ty`` are strings, then they
        are passed through the ``eval()`` function and converted to
        floating-point numbers.
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

    def text(self,tx,ty,textstr,**kwargs):
        """Plot text in the axis coordinate system transforming using the
        class font size and and centering in the horizontal and
        vertical directions by default. A figure and axes are created
        using :py:func:`o2sclpy.plot_base.canvas()`, if they have not
        been created already. If ``tx`` and ``ty`` are strings, then
        they are passed through the ``eval()`` function and converted
        to floating-point numbers.
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

        self.axes.text(tx,ty,textstr,**kwargs)
        
        # End of function plot_base::text()
        return

    def textbox(self,tx,ty,strt,boxprops='',**kwargs):
        """
        Plot text in the axis coordinate system with a box
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

    def subplots(self,nr,nc=1,**kwargs):
        """
        Create ``nr`` rows and ``nc`` columns of subplots. The axis
        objects are extracted and placed in a (one-dimensional) list
        in ``axes_dict``.
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
                                                  dct["fig_size_y"]))
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
        Select an axis from the current list of axes
        """

        if name=='':
            print('Axes names:',self.axes_dict.keys())
        elif len(name)==1:
            self.axes=self.axes_dict["subplot"+name]
        else:
            self.axes=self.axes_dict[name]
        
        # End of function plot_base::selax()
        return

    def inset(self,left,bottom,width,height,**kwargs):
        """
        Create a new axis inside the current figure?

        Useful kwargs are projection (None, 'aitoff', 'hammer', 'lambert',
        'mollweide', 'polar', 'rectilinear', str}) and polar (T/F)
        and many other axis kwargs (which may be difficult to 
        modify in this simplified form)
        """

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
        Modify the current axes properties
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
        """
        Documentation for o2graph command ``addcbar``:

        Add a color bar.
        
        Command-line arguments: ``<left> <bottom> <width> <height>
        [kwargs]``

        Add a new colorbar or a colorbar from the most recently created
        image at the location specified by ``left``, ``bottom``,
        ``width`` and ``height``. If the image keyword is 'last', 
        then the last density plot (command 'den-plot') or 2d 
        histogram plot (command 'hist2d-plot') is used. If 
        the image keyword is 'new', then a colormap must be 
        specified using the 'cmap' keyword and the color map is
        used to create the colorbar.
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
        """
        Documentation for o2graph command ``canvas``:

        Create a plotting canvas.

        Command-line arguments: (No arguments.)

        Create an empty plotting canvas. For example 'o2graph
        -canvas -show'. Typically, 'o2graph' creates
        the canvas automatically so explicitly using this command
        is unnecessary.

        This function creates a default figure using default_plot()
        and axis object using the xtitle and ytitle for the
        axis titles and xlo, xhi, ylo, and yhi for the axis limits.
        """
        if self.verbose>2:
            print('Canvas',self.fig_dict)

        dct=string_to_dict(self.fig_dict)
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

