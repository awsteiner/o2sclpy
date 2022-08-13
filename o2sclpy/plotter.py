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
from o2sclpy.plot_base import plot_base
from o2sclpy.yt_plot_base import yt_plot_base
from o2sclpy.utils import *

class plotter(yt_plot_base):
    """ 
    A class useful for quickly plotting HDF5 data generated
    by O\ :sub:`2`\ scl . This class is a child of the
    :py:class:`o2sclpy.plot_base` class.
    """
    
    def den_plot(self,table3d,slice_name,**kwargs):
        """
        Create a density plot from a slice of a table3d object.
        """
        nxt=table3d.get_nx()
        nyt=table3d.get_ny()
        sl=table3d.get_slice(slice_name).to_numpy()
        sl=sl.transpose()
        xgrid=[table3d.get_grid_x(i) for i in range(0,nxt)]
        ygrid=[table3d.get_grid_y(i) for i in range(0,nyt)]
        if self.canvas_flag==False:
            self.canvas()
        if self.logx==True:
            for i in range(0,len(xgrid)):
                xgrid[i]=math.log(xgrid[i],10)
        if self.logy==True:
            for i in range(0,len(ygrid)):
                ygrid[i]=math.log(ygrid[i],10)
        if self.logz==1:
            for i in range(0,len(xgrid)):
                for j in range(0,len(ygrid)):
                    sl[i][j]=math.log10(sl[i][h])
        tmp1=xgrid[0]-(xgrid[1]-xgrid[0])/2
        tmp2=xgrid[nxt-1]+(xgrid[nxt-1]-xgrid[nxt-2])/2
        tmp3=ygrid[0]-(ygrid[1]-ygrid[0])/2
        tmp4=ygrid[nyt-1]+(ygrid[nyt-1]-ygrid[nyt-2])/2
        self.last_image=self.axes.imshow(sl,interpolation='nearest',
                                         origin='lower',
                                         extent=[tmp1,tmp2,
                                                 tmp3,tmp4],
                                         aspect='auto',**kwargs)
        if self.colbar==True:
            cbar=self.fig.colorbar(self.last_image,ax=self.axes)
            cbar.ax.tick_params(labelsize=self.font*0.8)
                
        return
    
