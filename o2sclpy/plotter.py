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
from o2sclpy.hdf5 import hdf5_reader
from o2sclpy.plot_base import plot_base
from o2sclpy.yt_plot_base import yt_plot_base
from o2sclpy.utils import *

class plotter(yt_plot_base):
    """ 
    A class useful for quickly plotting HDF5 data generated
    by O\ :sub:`2`\ scl . This class is a child of the
    :py:class:`o2sclpy.plot_base` class.
    """

    h5r=hdf5_reader()
    """
    Object which handles reading HDF5 files
    """
    dset=0
    """
    The current HDF5 dataset
    """
    dtype=''
    """
    The current type
    """

    def contour_plot(self,level,**kwargs):
        """
        If the current dataset is of type ``vector<contour_line>``, then
        plot the contour lines for the contour level specified in
        ``level``.
        """
        if force_bytes(self.dtype)!=b'vector<contour_line>':
            print('Wrong type',self.dtype,'for contour_plotx.')
            return
        if self.verbose>2:
            print('In plotter.contour_plot()',level,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        n_lines=self.dset['n_lines'][0]
        for i in range(0,n_lines):
            line_level=self.dset['line_'+str(i)+'/level'][0]
            if abs(level-line_level) < 1.0e-7:
                if self.logx==True:
                    if self.logy==True:
                        self.axes.loglog(self.dset['line_'+str(i)+'/x'],
                                    self.dset['line_'+str(i)+'/y'],**kwargs)
                    else:
                        self.axes.semilogx(self.dset['line_'+str(i)+'/x'],
                                      self.dset['line_'+str(i)+'/y'],**kwargs)
                else:
                    if self.logy==True:
                        self.axes.semilogy(self.dset['line_'+str(i)+'/x'],
                                      self.dset['line_'+str(i)+'/y'],**kwargs)
                    else:
                        self.axes.plot(self.dset['line_'+str(i)+'/x'],
                                  self.dset['line_'+str(i)+'/y'],**kwargs)
        return
 
    def plot(self,colx,coly,**kwargs):
        """
        If the current dataset is of type ``table``, then plot the two
        columns specified in ``colx`` and ``coly``. Otherwise, if the
        current dataset is of type ``hist``, then plot the histogram
        and ignore the values of ``colx`` and ``coly``.
        """
        if force_bytes(self.dtype)==b'table':
            if self.verbose>2:
                print('In function plotter.plot()',colx,coly,kwargs)
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
                    self.axes.loglog(self.dset['data/'+colx],
                                self.dset['data/'+coly],**kwargs)
                else:
                    self.axes.semilogx(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
            else:
                if self.logy==True:
                    self.axes.semilogy(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
                else:
                    self.axes.plot(self.dset['data/'+colx],
                              self.dset['data/'+coly],**kwargs)
            if self.xset==True:
                self.axes.set_xlim(self.xlo,self.xhi)
            if self.yset==True:
                self.axes.set_ylim(self.ylo,self.yhi)
        elif force_bytes(self.dtype)==b'hist':
            size=dset['size'][0]
            bins=dset['bins']
            weights=dset['weights']
            rmode=dset['rmode'][0]
            reps=bins[0:size-1]
            for i in range(0,size):
                reps[i]=(bins[i]+bins[i+1])/2
            if self.logx==True:
                if self.logy==True:
                    self.axes.loglog(reps,weights,**kwargs)
                else:
                    self.axes.semilogx(reps,weights,**kwargs)
            else:
                if self.logy==True:
                    self.axes.semilogy(reps,weights,**kwargs)
                else:
                    self.axes.plot(reps,weights,**kwargs)
            if self.xset==True:
                self.axes.set_xlim(self.xlo,self.xhi)
            if self.yset==True:
                self.axes.set_ylim(self.ylo,self.yhi)
            return
        return

    def scatter(self,colx,coly,cols,colc,**kwargs):
        """
        Generate a scatter plot when the current object is a table object
        from x and y columns colx and coly, with sizes in cols and
        colors in colc. 
        """
        if force_bytes(self.dtype)==b'table':
            if self.verbose>2:
                print('In function plotter.scatter()',
                      colx,coly,cols,colc,kwargs)
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                self.axes.set_xscale('log')
            if self.logy==True:
                self.axes.set_yscale('log')

            if len(colc)>0:
                if len(cols)>0:
                    self.axes.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 s=self.dset['data/'+cols],
                                 c=self.dset['data/'+colc],
                                 **kwargs)
                else:
                    self.axes.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 c=self.dset['data/'+colc],
                                 **kwargs)
            else:
                if len(cols)>0:
                    self.axes.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 s=self.dset['data/'+cols],
                                 **kwargs)
                else:
                    self.axes.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 **kwargs)
            if self.xset==True:
                self.axes.set_xlim(self.xlo,self.xhi)
            if self.yset==True:
                self.axes.set_ylim(self.ylo,self.yhi)
        return

    def plot1(self,col,**kwargs):
        """
        If the current dataset is of type ``table``, then
        plot the column specified in ``col``.
        """
        if force_bytes(self.dtype)!=b'table':
            print('Wrong type',self.dtype,'for plot1.')
            return
        if self.verbose>2:
            print('In function plotter.plot1()',col,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        tlist=range(1,len(self.dset['data/'+col])+1)
        if self.logx==True:
            if self.logy==True:
                self.axes.loglog(tlist,self.dset['data/'+col],**kwargs)
            else:
                self.axes.semilogx(tlist,self.dset['data/'+col],**kwargs)
        else:
            if self.logy==True:
                self.axes.semilogy(tlist,self.dset['data/'+col],**kwargs)
            else:
                self.axes.plot(tlist,self.dset['data/'+col],**kwargs)
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
        return

    def hist_plot(self,col,**kwargs):
        """
        If the current dataset is of type ``hist``, then
        plot the associated histogram.
        """
        if self.verbose>2:
            print('In function plotter.hist_plot().',kwargs)
        if self.canvas_flag==False:
            self.canvas()
        for key in kwargs:
            if key=='bins':
                kwargs[key]=int(kwargs[key])
        if force_bytes(self.dtype)==b'table':
            self.axes.hist(self.dset['data/'+col],**kwargs)
        else:
            print('Wrong type',self.dtype,'for hist_plot()')
        return

    def hist2d_plot(self,colx,coly,**kwargs):
        """
        If the current dataset is of type ``hist2d``, then
        plot the associated two-dimensional histogram.
        """
        if self.verbose>2:
            print('In function plotter.hist2d_plot()',colx,coly,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        for key in kwargs:
            if key=='bins':
                kwargs[key]=int(kwargs[key])
        self.axes.hist2d(self.dset['data/'+colx],
                         self.dset['data/'+coly],**kwargs)
        return

    def read(self,filename):
        """
        Read first object of type ``table`` from file ``filename``
        """
        if self.verbose>0:
            print('Reading file',filename,'.')
        self.dset=self.h5r.read_first_type(filename,'table')
        self.dtype='table'
        return

    def read_type(self,filename,loc_type):
        """
        Read first object of type ``loc_type`` from file ``filename``
        """
        if self.verbose>0:
            print('Reading object of type',loc_type,
                  'in file',filename,'.')
        self.dset=self.h5r.read_first_type(filename,loc_type)
        self.dtype=loc_type
        return

    def read_name(self,filename,name):
        """
        Read object named ``name`` from file ``filename``
        """
        if self.verbose>0:
            print('Reading object named',name,'in file',filename,'.')
        atuple=self.h5r.read_name(filename,name)
        print('here',atuple)
        self.dset=atuple[0]
        self.dtype=atuple[1]
        return

    def list(self):
        """
        If the current data set is of type ``table``,
        then list the columns.
        """
        if force_bytes(self.dtype)==b'table':
            col_list=get_str_array(self.dset['col_names'])
            if self.verbose>2:
                print('-----------------------')
            unit_list=[]
            unit_flag=self.dset['unit_flag'][0]
            print('unit_flag',unit_flag)
            if self.verbose>2:
                print('unit_flag:',unit_flag)
            if unit_flag==1:
                unit_list=get_str_array(self.dset['units'])
                if self.verbose>2:
                    print('-----------------------')
                    print('unit_list:',unit_list)
            print(len(col_list),'columns.')
            for ix in range(0,len(col_list)):
                if unit_flag:
                    print(str(ix)+'. '+col_list[ix]+' ['+unit_list[ix]+']')
                else:
                    print(str(ix)+'. '+col_list[ix])
            print(self.dset['nlines'][0],'lines.')
            if self.verbose>2:
                print('Done in list')
        elif force_bytes(self.dtype)==b'table3d':
            sl_list=get_str_array(self.dset['slice_names'])
            print(len(sl_list),'slices.')
            for ix in range(0,len(sl_list)):
                print(str(ix)+'. '+sl_list[ix])
            xgrid=self.dset['xval'].value
            ygrid=self.dset['yval'].value
            lxgrid=len(xgrid)
            lygrid=len(ygrid)
            print('X-grid start: '+str(xgrid[0])+' end: '+
                  str(xgrid[lxgrid-1])+' size '+str(lxgrid))
            print('Y-grid start: '+str(ygrid[0])+' end: '+
                  str(ygrid[lygrid-1])+' size '+str(lygrid))
        else:
            print('Cannot list type',self.dtype)
        return

    def den_plot(self,slice_name,**kwargs):
        """
        If the current object is of type ``table3d``, create a density
        plot from the slice named ``slice_name`` .
        """
        if force_bytes(self.dtype)==b'table3d':
            name='data/'+slice_name
            (nxt,nyt)=self.dset[name].shape
            sl=[[self.dset[name][i][j] for i in range(0,nxt)]
                for j in range(0,nyt)]
            xgrid=self.dset['xval']
            ygrid=self.dset['yval']
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
            lx=len(xgrid)
            ly=len(ygrid)
            tmp1=xgrid[0]-(xgrid[1]-xgrid[0])/2
            tmp2=xgrid[lx-1]+(xgrid[lx-1]-xgrid[lx-2])/2
            tmp3=ygrid[0]-(ygrid[1]-ygrid[0])/2
            tmp4=ygrid[ly-1]+(ygrid[ly-1]-ygrid[ly-2])/2
            self.last_image=self.axes.imshow(sl,interpolation='nearest',
                                             origin='lower',
                                             extent=[tmp1,tmp2,
                                                     tmp3,tmp4],
                                             aspect='auto',**kwargs)
            if self.colbar==True:
                cbar=self.fig.colorbar(self.last_image,ax=self.axes)
                cbar.ax.tick_params(labelsize=self.font*0.8)
                
        else:
            print('Cannot density plot object of type',self.dtype)
        return

    def den_plot_direct(self,table3d,slice_name,**kwargs):
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
    
