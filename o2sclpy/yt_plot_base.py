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
from o2sclpy.plot_base import plot_base

class yt_plot_base(plot_base):
    """
    A base class with simplifications for plots generated in yt
    """

    # yt settings modifiable by get and set

    yt_filter=''
    """
    Filter for yt images. If non-empty, must contain the 
    strings '%i' for input file and '%o' for output file. A typical
    example is something like

    convert -contrast-stretch 0 %i %o 

    which uses imagemagick to adjust the color curve.
    """
    yt_resolution=(512,512)
    """
    Resolution for yt rendering (default (512,512))
    """
    yt_focus='default'
    """
    yt camera focus as a string. The string 'default' is equivalent
    to '[0.5,0.5,0.5] internal'. Either in the 'internal' or 'user' 
    unit system.
    """
    yt_position='default'
    """
    yt camera position as a string. The string 'default' is equivalent
    to '[1.5,0.6,0.7] internal'. Either in the 'internal' or 'user' 
    unit system.
    """
    yt_width='default'
    """
    yt camera width as a string. The string 'default' is equivalent to 
    '[1.5,1.5,1.5]'. Always in the internal unit system.
    """
    yt_north='default'
    """
    yt camera north vector string. The string 'default' is equivalent to
    '[1.0,0.0,0.0]'. Always in the internal unit system.
    """
    yt_sigma_clip=4.0
    """
    The sigma_clip parameter for yt (default 4.0)
    """

    # Other yt settings
    
    yt_path=[]
    """
    yt animation path (default []), as list of lists. The
    list contains instructions such as

    ['yaw',100,0.01]
    ['zoom',100,2.0]
    ...

    where the first entry in each sublist is always a type
    move, and the second entry in each sublist is always the 
    number of frames over which to complete the move.

    Note that this is not set using -set or -get but by the
    'yt-path' command.
    """
    yt_ann=[]
    """
    Annotations for yt renders. This list is controlled by
    the 'yt-ann' command.
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
                                      textcolor=self.yt_text_objects[i][6],
                                      dpi=self.yt_text_objects[i][7],
                                      scale=self.yt_text_objects[i][8],
                                      font=self.yt_text_objects[i][9],
                                      keyname=self.yt_text_objects[i][0])
        
        # End of function plot_base::yt_update_text()
        return

    def yt_line(self,point1,point2,color=[1.0,1.0,1.0,0.5],
                coords='user',keyname='o2sclpy_line'):
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

        # Coordinate transformation
        if coords!='internal':
            x1=(x1-self.xlo)/(self.xhi-self.xlo)
            y1=(y1-self.ylo)/(self.yhi-self.ylo)
            z1=(z1-self.zlo)/(self.zhi-self.zlo)
            x2=(x2-self.xlo)/(self.xhi-self.xlo)
            y2=(y2-self.ylo)/(self.yhi-self.ylo)
            z2=(z2-self.zlo)/(self.zhi-self.zlo)

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
                 frac_length=0.05,radius=0.0125,coords='user',
                 keyname='o2sclpy_arrow'):
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
        
    def yt_box(self,point1,point2,color=[1.0,1.0,1.0,0.5],
               coords='user',keyname='o2sclpy_box'):
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


        # Coordinate transformation
        if coords!='internal':
            x1=(x1-self.xlo)/(self.xhi-self.xlo)
            y1=(y1-self.ylo)/(self.yhi-self.ylo)
            z1=(z1-self.zlo)/(self.zhi-self.zlo)
            x2=(x2-self.xlo)/(self.xhi-self.xlo)
            y2=(y2-self.ylo)/(self.yhi-self.ylo)
            z2=(z2-self.zlo)/(self.zhi-self.zlo)

            
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
        kname=self.yt_unique_keyname(keyname)
        self.yt_scene.add_source(ls,keyname=kname)

        # End of function plot_base::yt_box()
        return
        
    def yt_text(self,tx,ty,tz,textstr,textcolor=(1,1,1,0.5),
                reorient=False,scale=0.6,font=30,
                keyname='o2sclpy_text',dpi=100,filename='',
                coords=''):
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
                                     textcolor,dpi,scale,font])

        self.yt_text_to_scene([xval,yval,zval],textstr,scale=scale,
                              font=font,keyname=kname,filename=filename,
                              dpi=dpi,textcolor=textcolor)

        # End of function plot_base::yt_text()
        return

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
    
    def yt_text_to_points(self,veco,vecx,vecy,text,dpi=100,font=30,
                          textcolor=(1,1,1,0.5),show=False,filename=''):
        """
        Take three 3D vectors 'veco' (origin), 'vecx' (x direction) and
        'vecy' (y direction), and a string of text ('text'), and
        return a numpy array of shape (6,npoints) which has entries
        (x,y,z,r,g,b). The values r, g, and b are between 0 and 1.

        The alpha value of 'textcolor' is also used for the alpha value
        of the points.

        Generally, to increase the point resolution of the text
        rendering, you increase the dpi parameter by some factor
        and decrease the scale factor by the same amount. However, 
        be careful because increasing the number of points
        will slow down the yt rendering considerably.

        Note that this function presumes a black background so it
        cannot handle black text. 

        Using the default dpi and font size is usually sufficient for
        lines of text containing about 30 characters. If more
        characters are required, then font must be decreased and dpi
        must be increased by the same factor in order to ensure all
        characters fit in the temporary figure which this function
        generates.
        """
        
        import matplotlib.pyplot as plot
        
        plot.rc('text',usetex=True)
        fig=plot.figure(1,figsize=(6.4,4.8),dpi=dpi)
        axes=plot.axes([0,0,1,1])
        fig.set_facecolor((0,0,0))
        axes.set_facecolor((0,0,0))

        from matplotlib.colors import to_rgba
        alpha=to_rgba(textcolor)[3]
        
        axes.text(0.5,0.5,text,fontsize=font,ha='center',va='center',
                  color=textcolor)
        
        fig.canvas.draw()
        if filename!='':
            print("Saving render of text '"+text+
                  "' in file named "+filename+'.')
            plot.savefig(filename)
        if show:
            plot.show()
            
        X=numpy.array(fig.canvas.renderer._renderer)
        Y=[]
        Y2=[]

        # Note that the array is flipped, so ymax is obtained
        # from the width and xmax is obtained from the height
        ymax=int(fig.get_dpi()*fig.get_figwidth())
        xmax=int(fig.get_dpi()*fig.get_figheight())
        
        for i in range(0,xmax):
            for j in range(0,ymax):
                if X[i,j,0]!=0 or X[i,j,1]!=0 or X[i,j,2]!=0:
                    xold=2.0*(i-float(xmax)/2)/float(xmax)
                    yold=2.0*(j-float(ymax)/2)/float(ymax)
                    vecnew=[veco[0]-vecy[0]*xold+vecx[0]*yold,
                            veco[1]-vecy[1]*xold+vecx[1]*yold,
                            veco[2]-vecy[2]*xold+vecx[2]*yold]
                    Y.append([vecnew[0],vecnew[1],vecnew[2]])
                    Y2.append([X[i,j,0]/255.0,X[i,j,1]/255.0,
                               X[i,j,2]/255.0,alpha])
        print('plot_base.yt_text_to_points():\n\t',
              'Number of points for',text,'is',len(Y))

        # Close the figure so that the memory is released now
        # that we have the point data
        plot.close(fig)
        
        # End of function plot_base::yt_text_to_points()
        return(numpy.array(Y),numpy.array(Y2))

    def yt_text_to_scene(self,loc,text,textcolor=(1,1,1,0.5),scale=0.6,
                         dpi=100,font=30,keyname='o2sclpy_text',
                         filename=''):
        """
        At location 'loc' put text 'text' into the scene using specified
        scale parameter and keyname. This function uses the current yt
        camera to orient the text so that it is upright and parallel
        to the camera. Increasing 'scale' increase the size of the
        text and the 'font' parameter is passed on to the
        yt_text_to_points() function.

        Generally, to increase the point resolution of the text
        rendering, you increase the dpi parameter by some factor
        and decrease the scale factor by the same amount. However, 
        be careful because increasing the number of points
        will slow down the yt rendering considerably.

        Note that this function presumes a black background so it
        cannot handle black text. 
        """

        # Imports
        from yt.visualization.volume_rendering.api \
            import PointSource
        
        # Construct orientation vectors. We arrange the text to be
        # upright and parallel to the camera.
        view_y=self.yt_camera.north_vector
        view_x=-numpy.cross(view_y,self.yt_camera.focus-
                         self.yt_camera.position)

        # Normalize view_x and view_y
        view_x=view_x/numpy.sqrt(view_x[0]**2+view_x[1]**2+view_x[2]**2)
        view_y=view_y/numpy.sqrt(view_y[0]**2+view_y[1]**2+view_y[2]**2)
    
        # Choose scale. The extra factor of 0.8 for y seems to be required
        # to make the text look correctly scaled.
        view_x=view_x*scale
        view_y=view_y*scale*0.8
        
        # Convert text to points
        (Y,Y2)=self.yt_text_to_points(loc,view_x,view_y,text,
                                      textcolor=textcolor,font=font,
                                      dpi=dpi,filename=filename)
    
        # Add the point source from the arrays returned by
        # the yt_text_to_points() function.
        points_xalabels=PointSource(Y,colors=Y2)
        kname=self.yt_unique_keyname(keyname)
        self.yt_scene.add_source(points_xalabels,keyname=kname)

        # End of function plot_base::yt_text_to_scene()
        return
    
    def yt_plot_axis(self,xval=1.0,yval=1.0,zval=1.0,
                     color=[1.0,1.0,1.0,0.5],
                     coords='internal',keyname='o2sclpy_axis'):
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
        kname=self.yt_unique_keyname(keyname+'_o')
        self.yt_scene.add_source(points,keyname=kname)

        self.yt_arrow(origin,ihat,color=color,keyname=keyname+'_x',
                      coords=coords)
        self.yt_arrow(origin,jhat,color=color,keyname=keyname+'_y',
                      coords=coords)
        self.yt_arrow(origin,khat,color=color,keyname=keyname+'_z',
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
            import create_volume_source

        if self.verbose>0:
            print('No volume object, adding yt volume.')
            
        self.yt_tf=yt.ColorTransferFunction((0,1),grey_opacity=False)
        self.yt_tf.add_gaussian(2.0,0.1,[0,0,0,0])
            
        arr=numpy.zeros(shape=(2,2,2))
        bbox=numpy.array([[0.0,1.0],[0.0,1.0],[0.0,1.0]])
        self.yt_data_sources.append(yt.load_uniform_grid(dict(density=arr),
                                                         arr.shape,bbox=bbox))
        ds=self.yt_data_sources[len(self.yt_data_sources)-1]
        self.yt_vols.append(create_volume_source(ds,field='density'))
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
            
    def text2(self,tx,ty,textstr,**kwargs):
        """
        A wrapper for plot_base::yt() which ensures that the
        yt transformations are done
        """
        
        # If we're doing a yt text annotation, then add the proper
        # transformation
        if self.yt_scene!=0:
            kwargs=dict(kwargs,transform=self.yt_trans)

        self.text(tx,ty,textstr,**kwargs)

        return
