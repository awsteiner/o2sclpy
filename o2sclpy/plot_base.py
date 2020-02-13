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
import math
import numpy
import os

# For system type detection
import platform

import matplotlib.pyplot as plot

# To create new color maps
from matplotlib.colors import LinearSegmentedColormap

# For rectangles and ellipses
import matplotlib.patches as patches

from o2sclpy.utils import parse_arguments, string_to_dict
from o2sclpy.utils import force_bytes, default_plot, get_str_array

class plot_base:
    """
    A base class for plotting classes :py:class:`o2sclpy.plotter` and
    :py:class:`o2sclpy.o2graph_plotter` . The principal purpose
    of this class is just to provide some additional simplification
    to python code which makes plots using matplotlib.

    """

    last_image=0
    """
    The last image object created (used for addcbar)
    """
    axes=0
    """ 
    Axis object
    """
    axis_list=[]
    """
    2D array of axis objects when subplots is used
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
    new_cmaps_defined=False
    """
    True if new colormaps were defined with 'new-cmaps'
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

    # Yt settings modifiable by get and set
    
    yt_resolution=(512,512)
    """
    Resolution for yt rendering (default (512,512))
    """
    yt_focus='default'
    """
    yt camera focus (default [0.5,0.5,0.5])
    """
    yt_position='default'
    """
    yt camera position (default [1.5,0.6,0.7])
    """
    yt_width='default'
    """
    yt camera width (default [1.5,1.5,1.5])
    """
    yt_north='default'
    """
    yt camera north (default [1.0,0.0,0.0])
    """
    yt_sigma_clip=4.0
    """
    The sigma_clip parameter for yt (default 4.0)
    """

    # Other yt settings
    
    yt_path=[]
    """
    yt animation path (default [])
    """
    yt_ann=[]
    """
    Annotations for yt renders
    """
    yt_trans=0
    """
    Transformation for yt figure annotations
    """
    yt_tf=0
    """
    The yt transfer function
    """
    yt_vol_keynames=[]
    """
    Current list of volume keynames
    """
    yt_volume_data=[]
    """
    Current list of data objects for volume sources
    """
    yt_volume_bbox=[]
    """
    Current list of bbox arrays for volume sources
    """
    yt_vols=[]
    """
    Current list of volume source objects
    """
    yt_data_sources=[]
    """
    Current list of yt data source objects
    """
    yt_text_objects=[]
    """
    Current list of yt data source objects
    """

    # Yt scene and camera
    
    yt_scene=0
    """ 
    The yt scene object
    """
    yt_created_scene=False
    """
    If true, then the yt scene object has been created
    """
    yt_camera=0
    """ 
    The yt camera object
    """
    yt_created_camera=False
    """
    If true, then the yt camera object has been created
    """
    
    def yt_unique_keyname(self,prefix):
        """
        Construct a unique yt keyname by adding integers (beginning with
        the number 2) to the user-specified ``prefix``.
        """
        if self.yt_scene==0:
            return(prefix)
        current=prefix
        unique=False
        count=1
        while unique==False:
            unique=True
            if count>1:
                current=prefix+str(count)
            for key, value in self.yt_scene.sources.items():
                if key==current:
                    unique=False
            if unique==False:
                count=count+1
        if self.verbose>0 and count>1:
            print('Key name',prefix,'changed to unique name',current)
        # End of function plot_base::yt_unique_keyname()
        return(current)
    
    def new_cmaps(self):
        """
        Add a few new colormaps
        """
        # A white to red colormap
        cdict={'red': ((0.0,1.0,1.0),(1.0,1.0,1.0)),
               'green': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(1.0,0.0,0.0))}
        reds2=LinearSegmentedColormap('reds2',cdict)
        plot.register_cmap(cmap=reds2)
        # A new version of the ``jet`` colormap which starts with
        # white instead of blue. In order, the index colors are white,
        # blue, green, yellow, orange, and red
        cdict={'red': ((0.0,1.0,1.0),(0.2,0.0,0.0),
                       (0.4,0.0,0.0),(0.6,1.0,1.0),
                       (0.8,1.0,1.0),(1.0,1.0,1.0)),
               'green': ((0.0,1.0,1.0),(0.2,0.0,0.0),
                         (0.4,0.5,0.5),(0.6,1.0,1.0),
                         (0.8,0.6,0.6),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(0.2,1.0,1.0),
                        (0.4,0.0,0.0),(0.6,0.0,0.0),
                        (0.8,0.0,0.0),(1.0,0.0,0.0))}
        jet2=LinearSegmentedColormap('jet2',cdict)
        plot.register_cmap(cmap=jet2)
        # A new version of the ``pastel`` colormap which starts with
        # white instead of blue. In order, the index colors are white,
        # blue, green, yellow, orange, and red
        cdict={'red': ((0.0,1.0,1.0),(0.2,0.3,0.3),
                       (0.4,0.3,0.3),(0.6,1.0,1.0),
                       (0.8,1.0,1.0),(1.0,1.0,1.0)),
               'green': ((0.0,1.0,1.0),(0.2,0.3,0.3),
                         (0.4,0.5,0.5),(0.6,1.0,1.0),
                         (0.8,0.6,0.6),(1.0,0.3,0.3)),
               'blue': ((0.0,1.0,1.0),(0.2,1.0,1.0),
                        (0.4,0.3,0.3),(0.6,0.3,0.3),
                        (0.8,0.3,0.3),(1.0,0.3,0.3))}
        pastel2=LinearSegmentedColormap('pastel2',cdict)
        plot.register_cmap(cmap=pastel2)
        # A white to green colormap
        cdict={'red': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'green': ((0.0,1.0,1.0),(1.0,1.0,1.0)),
               'blue': ((0.0,1.0,1.0),(1.0,0.0,0.0))}
        greens2=LinearSegmentedColormap('greens2',cdict)
        plot.register_cmap(cmap=greens2)
        # A white to blue colormap
        cdict={'red': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'green': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(1.0,1.0,1.0))}
        blues2=LinearSegmentedColormap('blues2',cdict)
        plot.register_cmap(cmap=blues2)
        new_cmaps_defined=True
        # End of function plot_base::new_cmaps()
        return

    def yt_update_text(self):
        """
        Update the text objects during an animation by removing them from
        the scene and adding them back.
        """

        for i in range(0,len(self.yt_text_objects)):
            if self.yt_text_objects[i][1]==True:
                # Remove previous object
                del self.yt_scene.sources[self.yt_text_objects[i][0]]
                # Now add it back
                self.yt_text_to_scene([self.yt_text_objects[i][2],
                                       self.yt_text_objects[i][3],
                                       self.yt_text_objects[i][4]],
                                      self.yt_text_objects[i][5],
                                      scale=self.yt_text_objects[i][6],
                                      font=self.yt_text_objects[i][7],
                                      keyname=self.yt_text_objects[i][0])
        
        # End of function plot_base::yt_update_text()
        return
    
    def yt_line(self,point1,point2,color=[1.0,1.0,1.0,0.5],
                keyname='o2sclpy_line'):
        """
        Plot a line in a yt volume visualization.
        """

        from yt.visualization.volume_rendering.api \
            import LineSource

        x1=point1[0]
        x2=point2[0]
        y1=point1[1]
        y2=point2[1]
        z1=point1[2]
        z2=point2[2]
        
        if self.xset==False:
            if x1<x2:
                self.xlo=x1
                self.xhi=x2
            else:
                self.xlo=x2
                self.xhi=x1
            print('Set xlimits to',self.xlo,self.xhi)
            self.xset=True
        if self.yset==False:
            if y1<y2:
                self.ylo=y1
                self.yhi=y2
            else:
                self.ylo=y2
                self.yhi=y1
            print('Set ylimits to',self.ylo,self.yhi)
            self.yset=True
        if self.zset==False:
            if z1<z2:
                self.zlo=z1
                self.zhi=z2
            else:
                self.zlo=z2
                self.zhi=z1
            print('Set zlimits to',self.zlo,self.zhi)
            self.zset=True
        
        icnt=0
        if self.yt_scene!=0:
            for key, value in self.yt_scene.sources.items():
                icnt=icnt+1
        if icnt==0:
            self.yt_def_vol()

        # Convert color to [r,g,b,a] for yt
        from matplotlib.colors import to_rgba
        colt=to_rgba(color)
        colt2=[colt[0],colt[1],colt[2],colt[3]]
        colors=[colt2]
        
        vertices=numpy.array([[[(x1-self.xlo)/(self.xhi-self.xlo),
                                (y1-self.ylo)/(self.yhi-self.ylo),
                                (z1-self.zlo)/(self.zhi-self.zlo)],
                               [(x2-self.xlo)/(self.xhi-self.xlo),
                                (y2-self.ylo)/(self.yhi-self.ylo),
                                (z2-self.zlo)/(self.zhi-self.zlo)]]])
        colors=numpy.array([colt2])
        ls=LineSource(vertices,colors)
        print('o2graph:yt-line: Adding line source.')
        kname=self.yt_unique_keyname(keyname)
        self.yt_scene.add_source(ls,keyname=kname)

        # End of function plot_base::yt_line()
        return
        
    def yt_arrow(self,point1,point2,color=[1.0,1.0,1.0,0.5],n_lines=40,
                 frac_length=0.05,radius=0.0125,keyname='o2sclpy_arrow',
                 coords='user'):
        """
        Plot an arrow in a yt volume visualization. 
        """
        
        from yt.visualization.volume_rendering.api \
            import LineSource

        x1=point1[0]
        x2=point2[0]
        y1=point1[1]
        y2=point2[1]
        z1=point1[2]
        z2=point2[2]
        
        if self.xset==False:
            if x1<x2:
                self.xlo=x1
                self.xhi=x2
            else:
                self.xlo=x2
                self.xhi=x1
            print('Set xlimits to',self.xlo,self.xhi)
            self.xset=True
        if self.yset==False:
            if y1<y2:
                self.ylo=y1
                self.yhi=y2
            else:
                self.ylo=y2
                self.yhi=y1
            print('Set ylimits to',self.ylo,self.yhi)
            self.yset=True
        if self.zset==False:
            if z1<z2:
                self.zlo=z1
                self.zhi=z2
            else:
                self.zlo=z2
                self.zhi=z1
            print('Set zlimits to',self.zlo,self.zhi)
            self.zset=True
        
        icnt=0
        if self.yt_scene!=0:
            for key, value in self.yt_scene.sources.items():
                icnt=icnt+1
        if icnt==0:
            self.yt_def_vol()

        # Coordinate transformation
        if coords!='internal':
            x1=(x1-self.xlo)/(self.xhi-self.xlo)
            y1=(y1-self.ylo)/(self.yhi-self.ylo)
            z1=(z1-self.zlo)/(self.zhi-self.zlo)
            x2=(x2-self.xlo)/(self.xhi-self.xlo)
            y2=(y2-self.ylo)/(self.yhi-self.ylo)
            z2=(z2-self.zlo)/(self.zhi-self.zlo)

        # Arrow line
        vertices=[[[x1,y1,z1],[x2,y2,z2]]]
        from matplotlib.colors import to_rgba
        colt=to_rgba(color)
        colt2=[colt[0],colt[1],colt[2],colt[3]]
        colors=[colt2]

        # First convert the arrow to polar coordinates
        rarr=math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
        parr=math.atan2(y2-y1,x2-x1)
        tarr=math.acos((z2-z1)/rarr)

        # Arrow head
        for theta in range(0,n_lines):
            for z in range(1,2):

                # Construct a vector from the tail of the arrow to the
                # outer circle beneath the arrow head presuming the
                # arrow is at (0,0,1)
                vec=[radius*math.cos(theta/n_lines*2.0*math.pi),
                     radius*math.sin(theta/n_lines*2.0*math.pi),
                     1-frac_length]

                # First transform by rotating the polar angle
                mat=numpy.array([[math.cos(tarr),0,math.sin(tarr)],
                                 [0,1,0],
                                 [math.sin(tarr),0,math.cos(tarr)]])
                vec=mat.dot(vec)
                # Then transform by rotating the azimuthal angle
                mat=numpy.array([[math.cos(parr),math.sin(parr),0],
                                 [math.sin(parr),math.cos(parr),0],
                                 [0,0,1]])
                vec=mat.dot(vec)

                # Rescale by the original vector length and translate
                # to the tail of the vector
                xnew=rarr*vec[0]+x1
                ynew=rarr*vec[1]+y1
                znew=rarr*vec[2]+z1

                # Add the lines to the list for the LineSource
                vertices.append([[x2,y2,z2],[xnew,ynew,znew]])
                colors.append(colt2)
                
        arrow_source=LineSource(numpy.array(vertices),numpy.array(colors))
        kname=self.yt_unique_keyname(keyname)
        self.yt_scene.add_source(arrow_source,keyname=kname)

        # End of function plot_base::yt_arrow()
        return
        
    def yt_del_source(self,keyname):
        """
        Delete a yt source

        o2sclpy has to keep track of the sources for two reasons (i)
        to make sure volme sources refer to valid memory and (ii) to
        be able to move text objects between renders in an animation.
        Thus, this function is required to remove a source from both
        the yt scene and from the internal o2sclpy lists.
        """

        # Remove from the text objects list
        for i in range(0,len(yt_text_objects)):
            if yt_text_objects[i][0]==keyname:
                del yt_text_objects[i]
                
        # Remove from the volume objects lists
        for i in range(0,len(yt_vol_keynames)):
            if yt_vol_keynames[i]==keyname:
                del yt_vol_keynames[i]
                del yt_volume_data[i]
                del yt_volume_bbox[i]
                del yt_vols[i]
                del yt_data_sources[i]

        # Now remove it from the scene
        del self.yt_scene.sources[keyname]
        
        # End of function plot_base::yt_del_source()
        return
        
    def yt_box(self,point1,point2,color=[1.0,1.0,1.0,0.5]):
        """
        Create a box in a yt visualization. 
        """

        from yt.visualization.volume_rendering.api \
            import BoxSource
        
        x1=point1[0]
        x2=point2[0]
        y1=point1[1]
        y2=point2[1]
        z1=point1[2]
        z2=point2[2]
        
        if self.xset==False:
            if x1<x2:
                self.xlo=x1
                self.xhi=x2
            else:
                self.xlo=x2
                self.xhi=x1
            print('Set xlimits to',self.xlo,self.xhi)
            self.xset=True
        if self.yset==False:
            if y1<y2:
                self.ylo=y1
                self.yhi=y2
            else:
                self.ylo=y2
                self.yhi=y1
            print('Set ylimits to',self.ylo,self.yhi)
            self.yset=True
        if self.zset==False:
            if z1<z2:
                self.zlo=z1
                self.zhi=z2
            else:
                self.zlo=z2
                self.zhi=z1
            print('Set zlimits to',self.zlo,self.zhi)
            self.zset=True
        
        icnt=0
        if self.yt_scene!=0:
            for key, value in self.yt_scene.sources.items():
                icnt=icnt+1
        if icnt==0:
            self.yt_def_vol()

        # Convert color to [r,g,b,a] for yt
        from matplotlib.colors import to_rgba
        colt=to_rgba(color)
        colt2=[colt[0],colt[1],colt[2],colt[3]]
        colors=[colt2]
        
        colors=numpy.array([colt])
        left=numpy.array([(x1-self.xlo)/(self.xhi-self.xlo),
                          (y1-self.ylo)/(self.yhi-self.ylo),
                          (z1-self.zlo)/(self.zhi-self.zlo)])
        right=numpy.array([(x2-self.xlo)/(self.xhi-self.xlo),
                           (y2-self.ylo)/(self.yhi-self.ylo),
                           (z2-self.zlo)/(self.zhi-self.zlo)])
        ls=BoxSource(left,right,colors)
        print('o2graph:yt-box: Adding box source.')
        kname=self.yt_unique_keyname('o2sclpy_box')
        self.yt_scene.add_source(ls,keyname=kname)

        # End of function plot_base::yt_box()
        return
        
    def yt_text(self,tx,ty,tz,textstr,reorient=False,scale=0.6,font=30,
                keyname='o2sclpy_text',filename='',coords='internal'):
        """
        Plot text given in ``textstr`` in a yt volume visualization at
        location ``(tx,ty,tz)``. If reorient is ``True``, then 
        the during an animation, the text will be redrawn so that
        it is parallel to the camera. The ``scale`` and ``font``
        parameters are passed on to the yt_text_to_scene() function.

        In the future, the plan is to allow tx, ty, and tz to be
        functions of 'i', so the text can be moved. For now tx, ty,
        and tz are just floating point numbers.
        """

        if (self.xset==False or self.yset==False or
            self.zset==False):
            print('Cannot place text before limits set.')
            return

        if coords!='internal':
            xval=(tx-self.xlo)/(self.xhi-self.xlo)
            yval=(ty-self.ylo)/(self.yhi-self.ylo)
            zval=(tz-self.zlo)/(self.zhi-self.zlo)
        else:
            xval=tx
            yval=ty
            zval=tz
        
        kname=self.yt_unique_keyname(keyname)
        
        self.yt_text_objects.append([kname,reorient,xval,yval,zval,textstr,
                                     scale,font])
        
        self.yt_text_to_scene([xval,yval,zval],textstr,scale=scale,
                              font=font,keyname=kname,filename=filename)
                              

        # End of function plot_base::yt_text()
        return

    def set(self,name,value):
        """
        Set the value of parameter named ``name`` to value ``value``
        """
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
            left_paren=value.find('(')
            right_paren=value.find(')')
            value=value[left_paren+1:right_paren]
            value=value.split(',')
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
        elif name=='yt_path':
            self.yt_path=value
        else:
            print('No variable named',name)
            
        if self.verbose>0:
            print('Set',name,'to',value)
            
        # End of function plot_base::set()
        return

    def yt_create_scene(self):
        """
        Create the yt scene object and set yt_created_scene to True.
        """
        from yt.visualization.volume_rendering.api import Scene
        print('plot_base:yt_create_scene(): Creating scene.')
        self.yt_scene=Scene()
        self.yt_created_scene=True
        # End of function plot_base::yt_create_scene()
        return
        
    def yt_create_camera(self,ds):
        """
        Create the yt camera object using the class variables
        ``yt_resolution``, ``yt_position``, and ``yt_focus``, with a
        camera width based on the domain width of ``ds``.
        """
        if (self.xset==False or self.yset==False or
            self.zset==False):
            print('Cannot create camera before x, y, and z limits are set.')
            return
            
        print('plot_base:yt_create_camera(): Creating camera.')
        self.yt_camera=self.yt_scene.add_camera()
        self.yt_camera.resolution=self.yt_resolution
        if self.yt_width=='default':
            self.yt_camera.width=1.5*ds.domain_width[0]
        else:
            self.yt_camera.width=[eval(self.yt_width)[0],
                                  eval(self.yt_width)[1],
                                  eval(self.yt_width)[2]]
        print('yt_width [%0.6e,%0.6e,%0.6e]' %
              (eval(self.yt_width)[0],
               eval(self.yt_width)[1],
               eval(self.yt_width)[2]))
        print('Camera width [%0.6e,%0.6e,%0.6e]' %
              (self.yt_camera.width[0],
               self.yt_camera.width[1],
               self.yt_camera.width[2]))
        if self.yt_position=='default':
            self.yt_camera.position=[1.5,0.6,0.7]
        else:
            self.yt_camera.position=[(eval(self.yt_position)[0]-self.xlo)/
                                     (self.xhi-self.xlo),
                                     (eval(self.yt_position)[1]-self.ylo)/
                                     (self.yhi-self.ylo),
                                     (eval(self.yt_position)[2]-self.zlo)/
                                     (self.zhi-self.zlo)]
        print('Camera position [%0.6e,%0.6e,%0.6e]' %
              (self.yt_camera.position[0],
               self.yt_camera.position[1],
               self.yt_camera.position[2]))
        if self.yt_focus=='default':
            self.yt_camera.focus=[0.5,0.5,0.5]
        else:
            self.yt_camera.focus=[(eval(self.yt_focus)[0]-self.xlo)/
                                  (self.xhi-self.xlo),
                                  (eval(self.yt_focus)[1]-self.ylo)/
                                  (self.yhi-self.ylo),
                                  (eval(self.yt_focus)[2]-self.zlo)/
                                  (self.zhi-self.zlo)]
        print('Camera focus [%0.6e,%0.6e,%0.6e]' %
              (self.yt_camera.focus[0],
               self.yt_camera.focus[1],
               self.yt_camera.focus[2]))
        self.yt_camera.north_vector=[0.0,0.0,1.0]
        self.yt_camera.switch_orientation()
        self.yt_created_camera=True
        # End of function plot_base::yt_create_camera()
        return
    
    def yt_text_to_points(self,veco,vecx,vecy,text,alpha=0.5,font=30,
                          textcolor=(0,0,0),show=False,filename=''):
        """
        Take three 3D vectors 'veco' (origin), 'vecx' (x direction) and
        'vecy' (y direction), and a string of text ('text'), and
        return a numpy array of shape (6,npoints) which has entries
        (x,y,z,r,g,b). The values r, g, and b are between 0 and 1.

        Currently, textcolor is unused.
        """
        fig, axes = plot.subplots()
        plot.rc('text',usetex=True)
        
        # FIXME: The text color is messed up here because the
        # Latex rendering is done on a white background and the
        # default 3d yt volume is a black background, so we
        # have to invert the colors below. 
        axes.text(0.5,0.5,text,fontsize=font,ha='center',va='center',
                  color=textcolor)
        
        plot.axis('off')
        fig.canvas.draw()
        if filename is not '':
            print("Saving render of text '"+text+
                  "' in file named "+filename+'.')
            plot.savefig(filename)
        if show:
            plot.show()
            
        X=numpy.array(fig.canvas.renderer._renderer)
        Y=[]
        Y2=[]
        # FIXME: we should obtain these values from the properties
        # of the fig object rather than hard coding them
        xmax=480
        ymax=640
        for i in range(0,xmax):
            for j in range(0,ymax):
                if X[i,j,0]!=255 or X[i,j,1]!=255 or X[i,j,2]!=255:
                    xold=2.0*(i-float(xmax)/2)/float(xmax)
                    yold=2.0*(j-float(ymax)/2)/float(ymax)
                    vecnew=[veco[0]-vecy[0]*xold+vecx[0]*yold,
                            veco[1]-vecy[1]*xold+vecx[1]*yold,
                            veco[2]-vecy[2]*xold+vecx[2]*yold]
                    Y.append([vecnew[0],vecnew[1],vecnew[2]])
                    Y2.append([1.0-X[i,j,0]/255.0,1.0-X[i,j,1]/255.0,
                               1.0-X[i,j,2]/255.0,alpha])

        # Close the figure so that the memory is released now
        # that we have the point data
        plot.close(fig)
        
        # End of function plot_base::yt_text_to_points()
        return(numpy.array(Y),numpy.array(Y2))

    def yt_text_to_scene(self,loc,text,scale=0.6,font=30,
                         keyname='o2sclpy_text',filename=''):
        """
        At location 'loc' put text 'text' into the scene using specified
        scale parameter and keyname. This function uses the current yt
        camera to orient the text so that it is upright and parallel
        to the camera. Increasing 'scale' increase the size of the
        text and the 'font' parameter is passed on to the
        yt_text_to_points() function.
        """
        
        # Imports
        from yt.visualization.volume_rendering.api \
            import PointSource
        
        # Construct orientation vectors
        view_y=self.yt_camera.north_vector
        view_x=-numpy.cross(view_y,self.yt_camera.focus-
                         self.yt_camera.position)
        # Normalize view_x and view_y
        view_x=view_x/numpy.sqrt(view_x[0]**2+view_x[1]**2+view_x[2]**2)
        view_y=view_y/numpy.sqrt(view_y[0]**2+view_y[1]**2+view_y[2]**2)
    
        # Choose scale. The factor of 0.8 for y seems to be required
        # to make the text look correctly scaled.
        view_x=view_x*scale
        view_y=view_y*scale*0.8
        
        # Convert text to points
        (Y,Y2)=self.yt_text_to_points(loc,view_x,view_y,text,font=font,
                                      filename=filename)
    
        # Add the point source
        points_xalabels=PointSource(Y,colors=Y2)
        kname=self.yt_unique_keyname(keyname)
        self.yt_scene.add_source(points_xalabels,keyname=kname)

        # End of function plot_base::yt_text_to_scene()
        return

    def yt_plot_axis(self,xval=1.0,yval=1.0,zval=1.0,
                     color=[1.0,1.0,1.0,0.5],
                     coords='internal'):
        """
        Plot an axis in a yt volume consisting a PointSource for the
        origin and then three arrows pointing from ``origin`` to
        ``[0,0,xval]``, ``[0,yval,0]``, and ``[0,0,zval]``. The
        specified color is used for the origin and all three arrows.
        The arrows are constructed with one main LineSource and then
        several smaller LineSource objects in a conical shape to
        create the arrow heads.
        """

        if self.yt_scene==0:
            print('Cannot plot yt axis without a scene.')
            return
        
        print('plot_base:yt_plot_axis(): Adding axis.')
        
        # Imports
        from yt.visualization.volume_rendering.api \
            import PointSource, LineSource

        origin=[0,0,0]
        ihat=[xval,0,0]
        jhat=[0,yval,0]
        khat=[0,0,zval]

        # Convert color to [r,g,b,a] for yt
        from matplotlib.colors import to_rgba
        colt=to_rgba(color)
        colt2=[colt[0],colt[1],colt[2],colt[3]]
        colors=[colt2]
        
        # Point at origin
        vertex_origin=numpy.array([origin])
        color_origin=numpy.array([colt2])
        points=PointSource(vertex_origin,colors=color_origin,radii=3)
        kname=self.yt_unique_keyname('o2sclpy_origin')
        self.yt_scene.add_source(points,keyname=kname)

        self.yt_arrow(origin,ihat,color=color,keyname='o2sclpy_xaxis',
                      coords=coords)
        self.yt_arrow(origin,jhat,color=color,keyname='o2sclpy_yaxis',
                      coords=coords)
        self.yt_arrow(origin,khat,color=color,keyname='o2sclpy_zaxis',
                      coords=coords)

        # End of function plot_base::yt_plot_axis()
        return
        
    def yt_check_backend(self):
        """
        For yt, check that we're using the Agg backend, and
        print out an error message if we are not.
        """
        import matplotlib
        if (matplotlib.get_backend()!='Agg' and 
            matplotlib.get_backend()!='agg'):
            print('yt integration only works with Agg.')
            print('Current backend is',matplotlib.get_backend())
            return 1
            
        # End of function plot_base::yt_check_backend()
        return 0
    
    def yt_def_vol(self):
        """
        Create a default yt volume source for rendering other objects
        """
        import yt
        from yt.visualization.volume_rendering.api \
            import VolumeSource

        if self.verbose>0:
            print('No volume object, adding yt volume.')
            
        self.yt_tf=yt.ColorTransferFunction((0,1),grey_opacity=False)
        self.yt_tf.add_gaussian(2.0,0.1,[0,0,0,0])
            
        arr=numpy.zeros(shape=(2,2,2))
        bbox=numpy.array([[0.0,1.0],[0.0,1.0],[0.0,1.0]])
        self.yt_data_sources.append(yt.load_uniform_grid(dict(density=arr),
                                                         arr.shape,bbox=bbox))
        ds=self.yt_data_sources[len(self.yt_data_sources)-1]
        self.yt_vols.append(VolumeSource(ds,field='density'))
        vol=self.yt_vols[len(self.yt_vols)-1]
        vol.log_field=False
            
        vol.set_transfer_function(self.yt_tf)
        if self.yt_created_scene==False:
            self.yt_create_scene()

        kname=self.yt_unique_keyname('o2sclpy_vol')
        self.yt_scene.add_source(vol,keyname=kname)
                            
        if self.yt_created_camera==False:
            self.yt_create_camera(ds)
            
        # End of function plot_base::yt_def_vol()
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

    def reset_xlimits(self):
        """
        Reset x axis limits
        """
        self.xset=False
        # End of function plot_base::reset_xlimits()
        return

    def xlimits(self,xlo,xhi):
        """
        Set the x-axis limits
        """
        self.xlo=xlo
        self.xhi=xhi
        self.xset=True
        if self.canvas_flag==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        # End of function plot_base::xlimits()
        return

    def reset_ylimits(self):
        """
        Reset y axis limits
        """
        self.yset=False
        # End of function plot_base::reset_ylimits()
        return

    def ylimits(self,ylo,yhi):
        """
        Set the y-axis limits
        """
        self.ylo=ylo
        self.yhi=yhi
        self.yset=True
        if self.canvas_flag==True:
            self.axes.set_ylim(self.ylo,self.yhi)
        # End of function plot_base::ylimits()
        return

    def reset_zlimits(self):
        """
        Reset z axis limits
        """
        self.zset=False
        # End of function plot_base::reset_zlimits()
        return

    def zlimits(self,zlo,zhi):
        """
        Set the z-axis limits
        """
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
        self.axes.plot([float(eval(x1)),float(eval(x2))],
                       [float(eval(y1)),float(eval(y2))],**kwargs)
        # End of function plot_base::line()
        return

    def arrow(self,x1,y1,x2,y2,arrowprops,**kwargs):
        """
        Plot an arrow from :math:`(x_1,y_1)` to :math:`(x_2,y_2)`
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
        self.axes.plot([float(eval(xval))],[float(eval(yval))],**kwargs)
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
        fx1=float(eval(x1))
        fx2=float(eval(x2))
        fy1=float(eval(y1))
        fy2=float(eval(y2))
        left=fx1
        if fx2<fx1:
            left=fx2
        lower=fy1
        if fy2<fy1:
            lower=fy2
        w=abs(fx1-fx2)
        h=abs(fy1-fy2)
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
        plot.show()
        # End of function plot_base::show()
        return

    def save(self,filename):
        """
        Save plot to file named ``filename``. If the verbose parameter is
        greater than zero, then this function prints the filename to
        the screen.
        """
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
        :py:func:`o2sclpy.plot_base.canvas()`,
        if they
        have not been created already. If ``tx`` and ``ty`` are strings, then
        they are passed through the ``eval()`` function and converted to
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

        # If we're doing a yt text annotation, then add the proper
        # transformation
        if self.yt_scene!=0:
            kwargs=dict(kwargs,transform=self.yt_trans)
            
        if isinstance(tx,str):
            tx=float(eval(tx))
        if isinstance(ty,str):
            ty=float(eval(ty))

        self.axes.text(tx,ty,textstr,**kwargs)
        
        # End of function plot_base::text()
        return

    def textbox(self,tx,ty,str,boxprops,**kwargs):
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

        self.axes.text(float(eval(tx)),float(eval(ty)),str,
                       fontsize=self.font,
                       transform=self.axes.transAxes,
                       bbox=string_to_dict(boxprops),**kwargs)
        # End of function plot_base::textbox()
        return

    def subplots(self,nr,nc=1,**kwargs):
        """
        Create ``nr`` rows and ``nc`` columns of subplots.
        """
        plot.rc('text',usetex=True)
        plot.rc('font',family='serif')
        plot.rcParams['lines.linewidth']=0.5
        dct=string_to_dict(self.fig_dict)
        if not('fig_size_x' in dct):
            dct['fig_size_x']=6.0
        if not('fig_size_y' in dct):
            dct['fig_size_y']=6.0
        self.fig,axis_temp=plot.subplots(nrows=nr,ncols=nc,
                                         figsize=(dct["fig_size_x"],
                                                  dct["fig_size_y"]))
        if nr==1 and nc==1:
            self.axis_list.append(axis_temp)
        elif nr==1:
            for i in range(0,nc):
                self.axis_list.append(axis_temp[i])
        elif nc==1:
            for i in range(0,nr):
                self.axis_list.append(axis_temp[i])
        else:
            for i in range(0,nr):
                for j in range(0,nc):
                    self.axis_list.append(axis_temp[i][j])
        for i in range(0,len(self.axis_list)):
            self.axis_list[i].minorticks_on()
            self.axis_list[i].tick_params('both',length=12,width=1,
                                          which='major')
            self.axis_list[i].tick_params('both',length=5,width=1,
                                          which='minor')
            self.axis_list[i].tick_params(labelsize=self.font*0.8)
        self.canvas_flag=True
        # End of function plot_base::subplots()
        return

    def xtitle(self,textstr):
        """
        Add a title for the x-axis
        """
        
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
        if textstr!='' and textstr!='none':
            if self.canvas_flag==False:
                self.canvas()
            self.axes.set_ylabel(textstr,fontsize=self.font)
        # End of function plot_base::ytitle()
        return
        
    #def ztitle(self,textstr):
    # End of function plot_base::ztitle()
    #return
    
    def selax(self,nr,nc=0):
        """
        Select an axis from the current list of axes
        """
        nr_temp=len(self.axis_list)
        try:
            nc_temp=len(self.axis_list[0])
        except:
            nc_temp=1
        if nc_temp==1:
            self.axes=self.axis_list[nr]
        else:
            self.axes=self.axis_list[nr][nc]
        # End of function plot_base::selax()
        return

    def addcbar(self,left,bottom,width,height,image='last',cmap='',**kwargs):
        """
        Add a colorbar from the most recently created image
        at the location specified by ``left``, ``bottom``, ``width`` and
        ``height``. 
        """
        if image=='last':
            axis_temp=self.fig.add_axes([left,bottom,width,height])
            self.axis_list.append(axis_temp)
            self.axes=axis_temp
            cbar=self.fig.colorbar(self.last_image,cax=self.axes,**kwargs)
            cbar.ax.tick_params(labelsize=self.font*0.8)
        elif image=='new':
            axis_temp=self.fig.add_axes([left,bottom,width,height])
            # This doesn't work and I'm not quite sure why yet
            #axis_temp.set_frame_on(False)
            self.axis_list.append(axis_temp)
            self.axes=axis_temp
            if cmap=='':
                print('New colorbar needs colormap.')
                return
            tempsm=plot.cm.ScalarMappable(cmap=cmap,
                                          norm=plot.Normalize(vmin=0,vmax=1))
            cbar=self.fig.colorbar(tempsm,cax=self.axes,
                                   orientation='horizontal')
            cbar.ax.tick_params(labelsize=0,length=0)
        else:
            print('invalid value of image')
            return
        
        # End of function plot_base::addcbar()
        return

    def canvas(self):
        """
        This function creates a default figure using default_plot()
        and axis object using the xtitle and ytitle for the
        axis titles and xlo, xhi, ylo, and yhi for the axis limits.
        """
        if self.verbose>2:
            print('Canvas')
            
        dct=string_to_dict(self.fig_dict)
        (self.fig,self.axes)=default_plot(**dct)
        
        # Plot limits
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
        self.canvas_flag=True
        # End of function plot_base::canvas()
        return

    def move_labels(self):
        """
        Move tick labels
        """
        for label in self.axes.get_xticklabels():
            t=label.get_position()
            t2=t[0],t[1]-0.01
            label.set_position(t2)
            label.set_fontsize(16)
        for label in self.axes.get_yticklabels():
            t=label.get_position()
            t2=t[0]-0.01,t[1]
            label.set_position(t2)
            label.set_fontsize(16)
        # End of function plot_base::move_labels()
        return
