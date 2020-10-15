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
import sys
import ctypes
import numpy
import os
import readline

import matplotlib.pyplot as plot

# For wrapping help text
import textwrap

# For code.interact() in 'python' command
import code 

# For rectangles
import matplotlib.patches as patches

from o2sclpy.doc_data import cmaps, new_cmaps, base_list
from o2sclpy.doc_data import extra_types, extra_list, param_list
from o2sclpy.doc_data import yt_param_list, acol_help_topics
from o2sclpy.doc_data import o2graph_help_topics
from o2sclpy.utils import parse_arguments, string_to_dict, terminal
from o2sclpy.utils import force_bytes, default_plot, get_str_array
from o2sclpy.utils import is_number, table_get_column, o2scl_get_type
from o2sclpy.utils import length_without_colors, wrap_line
from o2sclpy.utils import get_ic_ptrs_to_list, string_equal_dash
from o2sclpy.plot_base import plot_base
from o2sclpy.plot_info import marker_list, markers_plot, colors_near
from o2sclpy.plot_info import cmap_list_func, cmaps_plot, xkcd_colors_list
from o2sclpy.plot_info import colors_plot, color_list
from o2sclpy import version

class o2graph_plotter(plot_base):
    """
    A plotting class for the o2graph script. This class is a child of the
    :py:class:`o2sclpy.plot_base` class.

    This class is not necessarily intended to be instantiated by the 
    end user. 

    The function parameter `o2scl_hdf` must always be a ctypes DLL 
    object which points to the libo2scl_hdf shared library (.so on
    linux and .dylib on OSX). The function parameter `amp` must
    always be a pointer to the 
    :ref:`o2scl_acol::acol_manager<o2scl:acol_manager>` object.
    """

    def set_wrapper(self,o2scl_hdf,amp,args):
        """
        Wrapper around :py:func:`o2sclpy.plot_base.set` which sets
        plot-related parameters and sends other parameters to
        ``acol_manager``.
        """

        # First determine if it's an o2graph or yt parameter
        match=False
        for line in param_list:
            if args[0]==line[0]:
                match=True
                
        for line in yt_param_list:
            if args[0]==line[0]:
                match=True

        # If it's an o2graph or yt parameter, then call the parent
        # set() function
        if match==True:
            self.set(args[0],args[1])

        # If we're modifying the verbose parameter, then make sure
        # both the o2graph and the acol version match. Otherwise, if
        # it's only an o2graph or yt parameter, then just return.
        if (match==True and 
            force_bytes(args[0])!=b'verbose'):
            return

        # Call the acol 'set' function
        str_args='-set'
        size_type=ctypes.c_int * (len(args)+1)
        sizes=size_type()
        sizes[0]=len('set')+1
            
        for i in range(0,len(args)):
            str_args=str_args+args[i]
            sizes[i+1]=len(args[i])
        ccp=ctypes.c_char_p(force_bytes(str_args))
    
        parse_fn=o2scl_hdf.o2scl_acol_parse
        parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                           size_type,ctypes.c_char_p]
            
        parse_fn(amp,len(args)+1,sizes,ccp)

        # End of function o2graph_plotter::set_wrapper()
        return

    def get_wrapper(self,o2scl_hdf,amp,args):
        """
        Wrapper around :py:func:`o2sclpy.plot_base.get` which
        gets plot-related parameters and gets other parameters
        from ``acol_manager``.
        """
        match=False
        for line in param_list:
            if args[0]==line[0]:
                match=True

        for line in yt_param_list:
            if args[0]==line[0]:
                match=True
                
        if match==True:
            
            self.get(args[0])
                            
        else:
                        
            str_args='-get'
            size_type=ctypes.c_int * (len(args)+1)
            sizes=size_type()
            sizes[0]=len('get')+1
        
            for i in range(0,len(args)):
                str_args=str_args+args[i]
                sizes[i+1]=len(args[i])
            ccp=ctypes.c_char_p(force_bytes(str_args))
        
            parse_fn=o2scl_hdf.o2scl_acol_parse
            parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                              size_type,ctypes.c_char_p]
        
            parse_fn(amp,len(args)+1,sizes,ccp)

        # End of function o2graph_plotter::get_wrapper()
        return
            
    def gen_acol(self,o2scl_hdf,amp,cmd_name,args):
        """
        Run a general ``acol`` command named ``cmd_name`` with arguments
        stored in ``args``. This function uses the O\ :sub:`2`\ scl function
        ``o2scl_acol_parse()``.
        """

        str_args='-'+cmd_name
        size_type=ctypes.c_int * (len(args)+1)
        sizes=size_type()
        sizes[0]=len(cmd_name)+1
        
        for i in range(0,len(args)):
            str_args=str_args+args[i]
            sizes[i+1]=len(args[i])
        ccp=ctypes.c_char_p(force_bytes(str_args))

        parse_fn=o2scl_hdf.o2scl_acol_parse
        parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                           size_type,ctypes.c_char_p]
        
        parse_fn(amp,len(args)+1,sizes,ccp)

        # End of function o2graph_plotter::gen_acol()
        return

    def den_plot(self,o2scl_hdf,amp,args):
        """
        Density plot from a ``table3d``, ``hist_2d``, ``tensor_grid``,
        ``tensor``, ``tensor<int>``, or ``tensor<size_t>`` object.
        """

        int_ptr=ctypes.POINTER(ctypes.c_int)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)

        curr_type=o2scl_get_type(o2scl_hdf,amp)

        # Handle tensor and table3d types
        if (curr_type==b'tensor' or curr_type==b'tensor<size_t>' or
            curr_type==b'tensor_grid' or curr_type==b'tensor<int>' or
            curr_type==b'table3d'):

            kwstring=''
            
            # If the object is a tensor, convert to a table3d
            # object before plotting
            if curr_type!=b'table3d':
                index1=0
                index2=1
                if len(args)==1:
                    kwstring=args[0]
                if len(args)>=2:
                    index1=int(args[0])
                    index2=int(args[1])
                if len(args)>=3:
                    kwstring=args[2]
                if index1+index2!=1 and index1*index2!=0:
                    print('Indices must be "0 1" or "1 0" in',
                          'in den-plot.')
                    return
                    
                conv_fn=o2scl_hdf.o2scl_acol_tensor_to_table3d
                conv_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
                conv_fn.restype=ctypes.c_int
                
                conv_ret=conv_fn(amp,index1,index2)
                if conv_ret!=0:
                    print('Automatic conversion to table3d failed.')
                    return
                slice_name="tensor"
            else:
                slice_name=args[0]
                if len(args)>=2:
                    kwstring=args[1]

            # Now that we are guaranteed to have a table3d
            # object to use, use that to create the density
            # plot
            get_fn=o2scl_hdf.o2scl_acol_get_slice
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr,
                             int_ptr,double_ptr_ptr,double_ptr_ptr]

            slice=ctypes.c_char_p(force_bytes(slice_name))
            nx=ctypes.c_int(0)
            ptrx=double_ptr()
            ny=ctypes.c_int(0)
            ptry=double_ptr()
            ptrs=double_ptr()
            get_fn(amp,slice,ctypes.byref(nx),ctypes.byref(ptrx),
                   ctypes.byref(ny),ctypes.byref(ptry),
                   ctypes.byref(ptrs))

            xgrid=[ptrx[i] for i in range(0,nx.value)]
            ygrid=[ptry[i] for i in range(0,ny.value)]
            stemp=[ptrs[i] for i in range(0,nx.value*ny.value)]
            stemp2=numpy.array(stemp)
            sl=stemp2.reshape(nx.value,ny.value)
            sl=sl.transpose()

            # If logz was specified, then manually apply the
            # log to the data. Alternatively, we should consider
            # using 'LogNorm' here, as suggested in
            
            #https://stackoverflow.com/questions/2546475/
            #how-can-i-draw-a-log-normalized-imshow-plot-
            #with-a-colorbar-representing-the-raw

            if self.logz==True:
                fail_found=False
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
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
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
                        if sl[i][j]>self.zhi:
                            sl[i][j]=self.zhi
                        elif sl[i][j]<self.zlo:
                            sl[i][j]=self.zlo

            if self.canvas_flag==False:
                self.canvas()

            dctt=string_to_dict(kwstring)
            if dctt.pop('pcm',None)==True:
                
                print('Creating density plot using pcolormesh()')
                if self.logx==True:
                    self.axes.set_xscale('log')
                if self.logy==True:
                    self.axes.set_yscale('log')
                self.last_image=self.axes.pcolormesh(xgrid,ygrid,sl,**dctt)
                
            else:

                # The imshow() function doesn't work with a log axis, so we
                # set the scales back to linear and manually take the log
                self.axes.set_xscale('linear')
                self.axes.set_yscale('linear')
            
                if self.logx==True:
                    xgrid=[math.log(ptrx[i],10) for i in
                           range(0,nx.value)]
                if self.logy==True:
                    ygrid=[math.log(ptry[i],10) for i in
                           range(0,ny.value)]

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
                extent2=xgrid[nx.value-1]+(xgrid[nx.value-1]-
                                           xgrid[nx.value-2])/2
                extent3=ygrid[0]-(ygrid[1]-ygrid[0])/2
                extent4=ygrid[ny.value-1]+(ygrid[ny.value-1]-
                                           ygrid[ny.value-2])/2

                f=self.axes.imshow
                if len(kwstring)==0:
                    self.last_image=f(sl,interpolation='nearest',
                                      origin='lower',extent=[extent1,extent2,
                                                             extent3,extent4],
                                      aspect='auto')
                else:
                    self.last_image=f(sl,interpolation='nearest',
                                      origin='lower',extent=[extent1,extent2,
                                                             extent3,extent4],
                                      aspect='auto',
                                      **string_to_dict(kwstring))

                # AWS 7/1/2020: I'm not sure why imshow() is now
                # apparently mangling the minor tick settings. This
                # restores them. 
                self.axes.minorticks_on()
                self.axes.tick_params('both',length=12,width=1,which='major')
                self.axes.tick_params('both',length=5,width=1,which='minor')
                self.axes.tick_params(labelsize=self.font*0.8)

            # The color bar is added later below...

            # End of section for tensor types and table3d
        elif curr_type==b'hist_2d':

            get_fn=o2scl_hdf.o2scl_acol_get_hist_2d
            get_fn.argtypes=[ctypes.c_void_p,int_ptr,double_ptr_ptr,
                             int_ptr,double_ptr_ptr,double_ptr_ptr]

            nx=ctypes.c_int(0)
            ptrx=double_ptr()
            ny=ctypes.c_int(0)
            ptry=double_ptr()
            ptrs=double_ptr()
            get_fn(amp,ctypes.byref(nx),ctypes.byref(ptrx),
                   ctypes.byref(ny),ctypes.byref(ptry),
                   ctypes.byref(ptrs))

            xgrid=[ptrx[i] for i in range(0,nx.value)]
            ygrid=[ptry[i] for i in range(0,ny.value)]
            stemp=[ptrs[i] for i in range(0,nx.value*ny.value)]
            stemp2=numpy.array(stemp)
            sl=stemp2.reshape(nx.value,ny.value)
            sl=sl.transpose()

            if self.logx==True:
                xgrid=[math.log(ptrx[i],10) for i in
                       range(0,nx.value)]
            if self.logy==True:
                ygrid=[math.log(ptry[i],10) for i in
                       range(0,ny.value)]

            if self.zset==True:
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
                        if sl[i][j]>self.zhi:
                            sl[i][j]=self.zhi
                        elif sl[i][j]<self.zlo:
                            sl[i][j]=self.zlo
                            
            if self.logz==True:
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
                        sl[i][j]=math.log10(sl[i][j])
                        
            if self.canvas_flag==False:
                self.canvas()

            extent1=xgrid[0]-(xgrid[1]-xgrid[0])/2
            extent2=xgrid[nx.value-1]+(xgrid[nx.value-1]-
                                       xgrid[nx.value-2])/2
            extent3=ygrid[0]-(ygrid[1]-ygrid[0])/2
            extent4=ygrid[ny.value-1]+(ygrid[ny.value-1]-
                                       ygrid[ny.value-2])/2
                        
            if len(args)<1:
                self.last_image=self.axes.imshow(sl,interpolation='nearest',
                            origin='lower',extent=[extent1,extent2,
                                                   extent3,extent4],
                            aspect='auto')
            else:
                self.last_image=self.axes.imshow(sl,interpolation='nearest',
                            origin='lower',extent=[extent1,extent2,
                                                   extent3,extent4],
                            aspect='auto',**string_to_dict(args[0]))

            # The color bar is added later below...

            # End of section for type hist_2d
        else:
            print("Command 'den-plot' not supported for type",
                  curr_type,".")
            return

        if self.colbar==True:
            cbar=self.fig.colorbar(self.last_image,ax=self.axes)
            cbar.ax.tick_params('both',length=6,width=1,which='major')
            cbar.ax.tick_params(labelsize=self.font*0.8)

    def den_plot_rgb(self,o2scl_hdf,amp,args):
        """
        Density plot from a ``table3d`` object using three slices
        to specify the red, green, and blue values.
        """

        int_ptr=ctypes.POINTER(ctypes.c_int)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)

        curr_type=o2scl_get_type(o2scl_hdf,amp)

        # Handle tensor and table3d types
        if (curr_type==b'tensor' or curr_type==b'tensor<size_t>' or
            curr_type==b'tensor_grid' or curr_type==b'tensor<int>' or
            curr_type==b'table3d'):

            # If the object is a tensor, convert to a table3d
            # object before plotting
            if curr_type!=b'table3d':
                index1=0
                index2=1
                if len(args)==1:
                    kwstring=args[0]
                if len(args)>=2:
                    index1=int(args[0])
                    index2=int(args[1])
                if len(args)>=3:
                    kwstring=args[2]
                if index1+index2!=1 and index1*index2!=0:
                    print('Indices must be "0 1" or "1 0" in',
                          'in den-plot.')
                    return
                    
                conv_fn=o2scl_hdf.o2scl_acol_tensor_to_table3d
                conv_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
                conv_fn.restype=ctypes.c_int
                
                conv_ret=conv_fn(amp,index1,index2)
                if conv_ret!=0:
                    print('Automatic conversion to table3d failed.')
                    return
                slice_name="tensor"
            else:
                r_slice_name=args[0]
                g_slice_name=args[1]
                b_slice_name=args[2]
                if len(args)>=4:
                    kwstring=args[3]

            # Now that we are guaranteed to have a table3d
            # object to use, use that to create the density
            # plot
            get_fn=o2scl_hdf.o2scl_acol_get_slice
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr,
                             int_ptr,double_ptr_ptr,double_ptr_ptr]

            r_slice=ctypes.c_char_p(force_bytes(r_slice_name))
            nx=ctypes.c_int(0)
            ptrx=double_ptr()
            ny=ctypes.c_int(0)
            ptry=double_ptr()
            ptrs_r=double_ptr()
            get_fn(amp,r_slice,ctypes.byref(nx),ctypes.byref(ptrx),
                   ctypes.byref(ny),ctypes.byref(ptry),
                   ctypes.byref(ptrs_r))

            # Allocate the python storage
            sl_all=numpy.zeros((ny.value,nx.value,3))
            xgrid=numpy.zeros((nx.value))
            ygrid=numpy.zeros((ny.value))

            # Copy from the C pointer to the python storage
            ix=0
            for i in range(0,nx.value):
                for j in range(0,ny.value):
                    sl_all[j,i,0]=ptrs_r[ix]
                    ix=ix+1

            # Copy the grid
            for i in range(0,nx.value):
                xgrid[i]=ptrx[i]
            for j in range(0,ny.value):
                ygrid[j]=ptry[j]
            
            g_slice=ctypes.c_char_p(force_bytes(g_slice_name))
            nx=ctypes.c_int(0)
            ptrx=double_ptr()
            ny=ctypes.c_int(0)
            ptry=double_ptr()
            ptrs_g=double_ptr()
            get_fn(amp,g_slice,ctypes.byref(nx),ctypes.byref(ptrx),
                   ctypes.byref(ny),ctypes.byref(ptry),
                   ctypes.byref(ptrs_g))

            # Copy from the C pointer to the python storage
            ix=0
            for i in range(0,nx.value):
                for j in range(0,ny.value):
                    sl_all[j,i,1]=ptrs_g[ix]
                    ix=ix+1
            
            b_slice=ctypes.c_char_p(force_bytes(b_slice_name))
            nx=ctypes.c_int(0)
            ptrx=double_ptr()
            ny=ctypes.c_int(0)
            ptry=double_ptr()
            ptrs_b=double_ptr()
            get_fn(amp,b_slice,ctypes.byref(nx),ctypes.byref(ptrx),
                   ctypes.byref(ny),ctypes.byref(ptry),
                   ctypes.byref(ptrs_b))

            # Copy from the C pointer to the python storage
            ix=0
            for i in range(0,nx.value):
                for j in range(0,ny.value):
                    sl_all[j,i,2]=ptrs_b[ix]
                    ix=ix+1

            
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

            if self.canvas_flag==False:
                self.canvas()

            # The imshow() function doesn't work with a log axis, so we
            # set the scales back to linear and manually take the log
            self.axes.set_xscale('linear')
            self.axes.set_yscale('linear')
            
            if self.logx==True:
                xgrid=[math.log(ptrx[i],10) for i in
                       range(0,nx.value)]
            if self.logy==True:
                ygrid=[math.log(ptry[i],10) for i in
                       range(0,ny.value)]

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
            extent2=xgrid[nx.value-1]+(xgrid[nx.value-1]-
                                       xgrid[nx.value-2])/2
            extent3=ygrid[0]-(ygrid[1]-ygrid[0])/2
            extent4=ygrid[ny.value-1]+(ygrid[ny.value-1]-
                                       ygrid[ny.value-2])/2
                        
            f=self.axes.imshow
            if len(kwstring)==0:
                self.last_image=f(sl_all,
                                  interpolation='nearest',
                                  origin='lower',extent=[extent1,extent2,
                                                         extent3,extent4],
                                  aspect='auto')
            else:
                self.last_image=f(sl_all,
                                  interpolation='nearest',
                                  origin='lower',extent=[extent1,extent2,
                                                         extent3,extent4],
                                  aspect='auto',
                                  **string_to_dict(kwstring))

            # The color bar is added later below...

            # End of section for tensor types and table3d
        else:
            print("Command 'den-plot-rgb' not supported for type",
                  curr_type,".")
            return

        if self.colbar==True:
            cbar=self.fig.colorbar(self.last_image,ax=self.axes)
            cbar.ax.tick_params('both',length=6,width=1,which='major')
            cbar.ax.tick_params(labelsize=self.font*0.8)

    def plot(self,o2scl_hdf,amp,args):
        """
        Plot a two-dimensional set of data
        """

        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':
                            
            failed=False

            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            coly=ctypes.c_char_p(force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]
        
                if self.canvas_flag==False:
                    self.canvas()
                if self.logx==True:
                    if self.logy==True:
                        if len(args)<3:
                            self.axes.loglog(xv,yv)
                        else:
                            self.axes.loglog(xv,yv,**string_to_dict(args[2]))
                    else:
                        if len(args)<3:
                            self.axes.semilogx(xv,yv)
                        else:
                            self.axes.semilogx(xv,yv,**string_to_dict(args[2]))
                else:
                    if self.logy==True:
                        if len(args)<3:
                            self.axes.semilogy(xv,yv)
                        else:
                            self.axes.semilogy(xv,yv,**string_to_dict(args[2]))
                    else:
                        if len(args)<3:
                            self.axes.plot(xv,yv)
                        else:
                            self.axes.plot(xv,yv,**string_to_dict(args[2]))

            # End of section for 'table' type
        elif curr_type==b'hist':

            get_reps_fn=o2scl_hdf.o2scl_acol_get_hist_reps
            get_reps_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            get_wgts_fn=o2scl_hdf.o2scl_acol_get_hist_wgts
            get_wgts_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_reps_fn(amp,ctypes.byref(idx),
                        ctypes.byref(ptrx))

            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_wgts_fn(amp,ctypes.byref(idy),
                        ctypes.byref(ptry))

            xv=[ptrx[i] for i in range(0,idx.value)]
            yv=[ptry[i] for i in range(0,idy.value)]
    
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
                    if len(args)<1:
                        self.axes.loglog(xv,yv)
                    else:
                        self.axes.loglog(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        self.axes.semilogx(xv,yv)
                    else:
                        self.axes.semilogx(xv,yv,**string_to_dict(args[0]))
            else:
                if self.logy==True:
                    if len(args)<1:
                        self.axes.semilogy(xv,yv)
                    else:
                        self.axes.semilogy(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        self.axes.plot(xv,yv)
                    else:
                        self.axes.plot(xv,yv,**string_to_dict(args[0]))
                            
            # End of section for 'hist' type
        elif curr_type==b'prob_dens_mdim_amr':

            get_base_fn=o2scl_hdf.o2scl_acol_pdma_get_base
            get_base_fn.argtypes=[ctypes.c_void_p,int_ptr,
                                  int_ptr,double_ptr_ptr,double_ptr_ptr]
                            
            get_cube_fn=o2scl_hdf.o2scl_acol_pdma_get_cube
            get_cube_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                                  double_ptr_ptr,double_ptr_ptr,
                                  double_ptr,double_ptr]
                            
            ndimx=ctypes.c_int(0)
            nx=ctypes.c_int(0)
            lowx=double_ptr()
            highx=double_ptr()
            get_base_fn(amp,ctypes.byref(ndimx),ctypes.byref(nx),
                        ctypes.byref(lowx),ctypes.byref(highx))

            dimx=int(args[0])
            dimy=int(args[1])

            self.xlo=lowx[dimx]
            self.ylo=lowx[dimy]
            self.xset=True
            self.xhi=highx[dimx]
            self.yhi=highx[dimy]
            self.yset=True

            if self.canvas_flag==False:
                self.canvas()

            # Need to figure out here how to convert fill function
            # to a value, keeping in mind it can depend on
            # fvy.value (fractional volume) or wy.value (weight)
                
            fill_fn='None'
            if len(args)>=3:
                fill_fn=args[2]
                
            print('Fill function',fill_fn)
                
            for i in range(0,nx.value):

                iy=ctypes.c_int(i)
                lowy=double_ptr()
                highy=double_ptr()
                fvy=ctypes.c_double(0.0)
                wy=ctypes.c_double(0.0)
                get_cube_fn(amp,iy,ctypes.byref(lowy),
                            ctypes.byref(highy),
                            ctypes.byref(fvy),
                            ctypes.byref(wy))
                
                left=lowy[dimx]
                lower=lowy[dimy]
                right=highy[dimx]
                upper=highy[dimy]
                w=right-left
                h=upper-lower

                if len(args)<4:
                    r=patches.Rectangle((left,lower),w,h,0.0,
                                        alpha=fvy.value)
                    self.axes.add_patch(r)
                else:
                    strtemp='alpha='+str(fvy.value)+','+args[3]
                    r=patches.Rectangle((left,lower),w,h,0.0,
                                        **string_to_dict(strtemp))
                    self.axes.add_patch(r)
                            
            # End of section for 'prob_dens_mdim_amr' type
        elif curr_type==b'vector<contour_line>':

            # Get the total number of contour lines
            cont_n_fn=o2scl_hdf.o2scl_acol_contours_n
            cont_n_fn.argtypes=[ctypes.c_void_p]
            cont_n_fn.restype=ctypes.c_int
            nconts=cont_n_fn(amp)

            # Define types for extracting each contour line
            cont_line_fn=o2scl_hdf.o2scl_acol_contours_line
            cont_line_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                                   int_ptr,double_ptr_ptr,
                                   double_ptr_ptr]
            cont_line_fn.restype=ctypes.c_double

            if self.canvas_flag==False:
                self.canvas()

            # Loop over all contour lines
            for k in range(0,nconts):
                idx=ctypes.c_int(0)
                ptrx=double_ptr()
                ptry=double_ptr()
                lev=cont_line_fn(amp,k,ctypes.byref(idx),
                                 ctypes.byref(ptrx),ctypes.byref(ptry))
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idx.value)]
                
                if self.logx==True:
                    if self.logy==True:
                        if len(args)<1:
                            self.axes.loglog(xv,yv)
                        else:
                            self.axes.loglog(xv,yv,**string_to_dict(args[0]))
                    else:
                        if len(args)<1:
                            self.axes.semilogx(xv,yv)
                        else:
                            self.axes.semilogx(xv,yv,**string_to_dict(args[0]))
                else:
                    if self.logy==True:
                        if len(args)<1:
                            self.axes.semilogy(xv,yv)
                        else:
                            self.axes.semilogy(xv,yv,**string_to_dict(args[0]))
                    else:
                        if len(args)<1:
                            self.axes.plot(xv,yv)
                        else:
                            self.axes.plot(xv,yv,**string_to_dict(args[0]))
            # End of section for 'vector<contour_line>' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::plot()
        return
                                 
    def plot_color(self,o2scl_hdf,amp,args):
        """
        Plot a set of line segments, coloring according to a third 
        variable.
        """

        if len(args)<4:
            raise ValueError('Function plot_color() requires four values '+
                             'for the args list.')
        
        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':
                            
            failed=False

            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            coly=ctypes.c_char_p(force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            colz=ctypes.c_char_p(force_bytes(args[2]))
            idz=ctypes.c_int(0)
            ptrz=double_ptr()
            get_ret=get_fn(amp,colz,ctypes.byref(idz),ctypes.byref(ptrz))
            if get_ret!=0:
                print('Failed to get column named "'+args[2]+'".')
                failed=True

            cmap=args[3]

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]
                zv=[ptrz[i] for i in range(0,idz.value)]

                if self.logx:
                    for i in range(0,len(xv)):
                        xv[i]=math.log10(xv)
                if self.logy:
                    for i in range(0,len(yv)):
                        yv[i]=math.log10(yv)
                if self.logz:
                    for i in range(0,len(zv)):
                        zv[i]=math.log10(zv)
                
                if self.canvas_flag==False:
                    self.canvas()

                import matplotlib
                import matplotlib.cm as cm
                
                norm=matplotlib.colors.Normalize(vmin=min(zv),
                                                 vmax=max(zv),
                                                 clip=True)
                mapper=cm.ScalarMappable(norm=norm,cmap=cmap)
                    
                for i in range(0,len(xv)-1):

                    col=mapper.to_rgba(zv[i])
                    if len(args)<5:
                        self.axes.plot([xv[i],xv[i+1]],
                                       [yv[i],yv[i+1]],
                                       color=col)
                    else:
                        self.axes.plot([xv[i],xv[i+1]],
                                       [yv[i],yv[i+1]],
                                       color=col,
                                       **string_to_dict(args[4]))

                if self.colbar==True:
                    cbar=self.fig.colorbar(mapper,
                                           ax=self.axes)
                    cbar.ax.tick_params('both',length=6,width=1,which='major')
                    cbar.ax.tick_params(labelsize=self.font*0.8)
                    
            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::plot_color()
        return
                                 
    def rplot(self,o2scl_hdf,amp,args):
        """
        Plot a region inside a curve or in between two curves
        """

        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':
                            
            failed=False

            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx1=ctypes.c_char_p(force_bytes(args[0]))
            idx1=ctypes.c_int(0)
            ptrx1=double_ptr()
            get_ret=get_fn(amp,colx1,ctypes.byref(idx1),ctypes.byref(ptrx1))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            coly1=ctypes.c_char_p(force_bytes(args[1]))
            idy1=ctypes.c_int(0)
            ptry1=double_ptr()
            get_ret=get_fn(amp,coly1,ctypes.byref(idy1),ctypes.byref(ptry1))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx1[i] for i in range(0,idx1.value)]
                yv=[ptry1[i] for i in range(0,idy1.value)]
                
            if len(args)>3:
                colx2=ctypes.c_char_p(force_bytes(args[2]))
                idx2=ctypes.c_int(0)
                ptrx2=double_ptr()
                get_ret=get_fn(amp,colx2,ctypes.byref(idx2),ctypes.byref(ptrx2))
                if get_ret!=0:
                    print('Failed to get column named "'+args[2]+'".')
                    failed=True

                coly2=ctypes.c_char_p(force_bytes(args[3]))
                idy2=ctypes.c_int(0)
                ptry2=double_ptr()
                get_ret=get_fn(amp,coly2,ctypes.byref(idy2),ctypes.byref(ptry2))
                if get_ret!=0:
                    print('Failed to get column named "'+args[3]+'".')
                    failed=True

                if failed==False:
                    for i in range(0,idx2.value):
                        xv.append(ptrx2[idx2.value-1-i])
                        yv.append(ptry2[idy2.value-1-i])

            if failed==False:
                # Make sure the loop is closed
                xv.append(ptrx1[0])
                yv.append(ptry1[0])
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)==3:
                    self.axes.fill(xv,yv,**string_to_dict(args[2]))
                elif len(args)==5:
                    self.axes.fill(xv,yv,**string_to_dict(args[4]))
                else:
                    self.axes.fill(xv,yv)

                if self.logx==True:
                    self.axes.set_xscale('log')
                if self.logy==True:
                    self.axes.set_yscale('log')
                    
                if self.xset==True:
                    self.axes.set_xlim(self.xlo,self.xhi)
                if self.yset==True:
                    self.axes.set_ylim(self.ylo,self.yhi)
                                 
            # End of section for 'table' type
        else:
            print("Command 'rplot' not supported for type",
                  curr_type,".")
            return
        
        # End of function o2graph_plotter::rplot()
        return
                                 
    def scatter(self,o2scl_hdf,amp,args):
        """
        Generate a scatter plot.
        """

        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':
                            
            failed=False

            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            coly=ctypes.c_char_p(force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]

            sv=[]
            cv=[]

            if (len(args)>2 and force_bytes(args[2])!=b'None' and
                force_bytes(args[2])!=b'none'):
                cols=ctypes.c_char_p(force_bytes(args[2]))
                ids=ctypes.c_int(0)
                ptrs=double_ptr()
                get_ret=get_fn(amp,cols,ctypes.byref(ids),ctypes.byref(ptrs))
                if get_ret!=0:
                    print('Failed to get column named "'+args[2]+'".')
                    failed=True
                else:
                    sv=[ptrs[i] for i in range(0,ids.value)]

            if (len(args)>3 and force_bytes(args[3])!=b'None' and
                force_bytes(args[3])!=b'none'):
                colc=ctypes.c_char_p(force_bytes(args[3]))
                idc=ctypes.c_int(0)
                ptrc=double_ptr()
                get_ret=get_fn(amp,colc,ctypes.byref(idc),ctypes.byref(ptrc))
                if get_ret!=0:
                    print('Failed to get column named "'+args[3]+'".')
                    failed=True
                else:
                    cv=[ptrc[i] for i in range(0,idc.value)]

            if failed==False:
                
                if self.canvas_flag==False:
                    self.canvas()
                if len(sv)>0:
                    if len(cv)>0:
                        if len(args)>4:
                            self.axes.scatter(xv,yv,s=sv,c=cv,
                                         **string_to_dict(args[4]))
                        else:
                            self.axes.scatter(xv,yv,s=sv,c=cv)
                    else:
                        if len(args)>4:
                            self.axes.scatter(xv,yv,s=sv,
                                         **string_to_dict(args[4]))
                        else:
                            self.axes.scatter(xv,yv,s=sv)
                else:
                    if len(cv)>0:
                        if len(args)>4:
                            self.axes.scatter(xv,yv,c=cv,
                                         **string_to_dict(args[4]))
                        else:
                            self.axes.scatter(xv,yv,c=cv)
                    else:
                        if len(args)>4:
                            self.axes.scatter(xv,yv,**string_to_dict(args[4]))
                        else:
                            self.axes.scatter(xv,yv)

                if self.logx==True:
                    self.axes.set_xscale('log')
                if self.logy==True:
                    self.axes.set_yscale('log')
                    
                if self.xset==True:
                    self.axes.set_xlim(self.xlo,self.xhi)
                if self.yset==True:
                    self.axes.set_ylim(self.ylo,self.yhi)
                if self.colbar==True and len(cv)>0:
                    cbar=plot.colorbar(ax=self.axes)
                    cbar.ax.tick_params('both',length=6,width=1,
                                        which='major')
                    cbar.ax.tick_params(labelsize=self.font*0.8)
                    
            # End of section for 'table' type
        else:
            print("Command 'scatter' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::scatter()
        return
                                 
    def hist_plot(self,o2scl_hdf,amp,args):
        """
        Plot a histogram.
        """

        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':
                            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            failed=False
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)<2:
                    self.axes.hist(xv)
                else:
                    self.axes.hist(xv,**string_to_dict(args[1]))

        elif curr_type==b'hist':
                    
            get_reps_fn=o2scl_hdf.o2scl_acol_get_hist_reps
            get_reps_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            get_wgts_fn=o2scl_hdf.o2scl_acol_get_hist_wgts
            get_wgts_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            get_bins_fn=o2scl_hdf.o2scl_acol_get_hist_bins
            get_bins_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_reps_fn(amp,ctypes.byref(idx),
                        ctypes.byref(ptrx))
            xv=[ptrx[i] for i in range(0,idx.value)]

            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_wgts_fn(amp,ctypes.byref(idy),
                        ctypes.byref(ptry))
            yv=[ptry[i] for i in range(0,idy.value)]

            idz=ctypes.c_int(0)
            ptrz=double_ptr()
            get_bins_fn(amp,ctypes.byref(idz),
                        ctypes.byref(ptrz))
            zv=[ptrz[i] for i in range(0,idz.value)]
            
            if self.canvas_flag==False:
                self.canvas()
            if len(args)<1:
                self.axes.hist(xv,weights=yv,bins=zv)
            else:
                self.axes.hist(xv,weights=yv,bins=zv,
                               **string_to_dict(args[0]))
            
            # End of section for 'table' type
        else:
            print("Command 'hist_plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::hist_plot()
        return
                                 
    def hist2d_plot(self,o2scl_hdf,amp,args):
        """
        Plot a two-dimensional histogram.
        """

        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':
                            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            failed=False

            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True
            
            coly=ctypes.c_char_p(force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)<3:
                    c,x,y,self.last_image=self.axes.hist2d(xv,yv)
                else:
                    c,x,y,self.last_image=self.axes.hist2d(xv,yv,**string_to_dict(args[2]))
                
                if self.colbar==True:
                    cbar=plot.colorbar(self.last_image,ax=self.axes)
                    cbar.ax.tick_params('both',length=6,width=1,
                                        which='major')
                    cbar.ax.tick_params(labelsize=self.font*0.8)
                    
            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::hist2d_plot()
        return
                                 
    def errorbar(self,o2scl_hdf,amp,args):
        """
        Create a plot with error bars.
        """

        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':

            xv=table_get_column(o2scl_hdf,amp,args[0])
            yv=table_get_column(o2scl_hdf,amp,args[1])

            if len(args)>=6 and args[2]=='None' or args[2]=='none':
                if is_number(args[3]):
                    xerrv=float(args[3]);
                else:
                    xerrv=table_get_column(o2scl_hdf,amp,args[3])
            if len(args)>=6 and args[3]=='None' or args[3]=='none':
                if is_number(args[2]):
                    xerrv=float(args[2]);
                else:
                    xerrv=table_get_column(o2scl_hdf,amp,args[2])
            elif len(args)>=6:
                if is_number(args[2]):
                    if is_number(args[3]):
                        xerrv=[[float(args[2]),float(args[3])]
                               for i in range(0,idxerr.value)]
                    else:
                        colxerr=ctypes.c_char_p(force_bytes(args[3]))
                        idxerr=ctypes.c_int(0)
                        ptrxerr=double_ptr()
                        get_fn(amp,colxerr,ctypes.byref(idxerr),
                               ctypes.byref(ptrxerr))
                        xerrv=[[float(args[2]),ptrxerr[i]] for i in
                               range(0,idxerr.value)]
                else:
                    if is_number(args[3]):
                        colxerr=ctypes.c_char_p(force_bytes(args[2]))
                        idxerr=ctypes.c_int(0)
                        ptrxerr=double_ptr()
                        get_fn(amp,colxerr,ctypes.byref(idxerr),
                               ctypes.byref(ptrxerr))
                        xerrv=[[ptrxerr[i],float(args[3])] for i in
                               range(0,idxerr.value)]
                    else:
                        colxerr=ctypes.c_char_p(force_bytes(args[2]))
                        idxerr=ctypes.c_int(0)
                        ptrxerr=double_ptr()
                        get_fn(amp,colxerr,ctypes.byref(idxerr),
                               ctypes.byref(ptrxerr))
                        colxerr2=ctypes.c_char_p(force_bytes(args[3]))
                        idxerr2=ctypes.c_int(0)
                        ptrxerr2=double_ptr()
                        get_fn(amp,colxerr2,ctypes.byref(idxerr2),
                               ctypes.byref(ptrxerr2))
                        xerrv=[[ptrxerr[i],ptrxerr2[i]] for i in
                               range(0,idxerr.value)]
            else:
                if args[2]=='None' or args[2]=='none':
                    xerrv=0.0
                elif is_number(args[2]):
                    xerrv=float(args[2])
                else:
                    xerrv=table_get_column(o2scl_hdf,amp,args[2])
    
            if args[3]=='None' or args[3]=='none':
                yerrv=0.0
            elif is_number(args[3]):
                yerrv=float(args[3])
            else:
                yerrv=table_get_column(o2scl_hdf,amp,args[3])

            if self.canvas_flag==False:
                self.canvas()
            if len(args)<5:
                self.axes.errorbar(xv,yv,yerr=yerrv,xerr=xerrv)
            else:
                self.axes.errorbar(xv,yv,yerr=yerrv,xerr=xerrv,
                                   **string_to_dict(args[4]))
                
            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::errorbar()
        return
                                 
    def plot1(self,o2scl_hdf,amp,args):
        """
        Plot one array of data versus an integer x axis.
        """

        int_ptr=ctypes.POINTER(ctypes.c_int)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
                        
        if curr_type==b'table':
            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            failed=False
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            if failed==False:
                xv=[i for i in range(0,idx.value)]
                yv=[ptrx[i] for i in range(0,idx.value)]
        
                if self.canvas_flag==False:
                    self.canvas()
                if self.logx==True:
                    if self.logy==True:
                        if len(args)<2:
                            self.axes.loglog(xv,yv)
                        else:
                            self.axes.loglog(xv,yv,**string_to_dict(args[1]))
                    else:
                        if len(args)<2:
                            self.axes.semilogx(xv,yv)
                        else:
                            self.axes.semilogx(xv,yv,**string_to_dict(args[1]))
                else:
                    if self.logy==True:
                        if len(args)<2:
                            self.axes.semilogy(xv,yv)
                        else:
                            self.axes.semilogy(xv,yv,**string_to_dict(args[1]))
                    else:
                        if len(args)<2:
                            self.axes.plot(xv,yv)
                        else:
                            self.axes.plot(xv,yv,**string_to_dict(args[1]))
                                
                if self.xset==True:
                    self.axes.set_xlim(self.xlo,self.xhi)
                if self.yset==True:
                    self.axes.set_ylim(self.ylo,self.yhi)
                    
        elif (curr_type==b'double[]' or curr_type==b'int[]' or
              curr_type==b'size_t[]'):

            get_fn=o2scl_hdf.o2scl_acol_get_double_arr
            get_fn.argtypes=[ctypes.c_void_p,int_ptr,double_ptr_ptr]
                            
            id=ctypes.c_int(0)
            ptr=double_ptr()
            get_fn(amp,ctypes.byref(id),ctypes.byref(ptr))
            
            xv=[i for i in range(0,id.value)]
            yv=[ptr[i] for i in range(0,id.value)]

            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
                    if len(args)<1:
                        self.axes.loglog(xv,yv)
                    else:
                        self.axes.loglog(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        self.axes.semilogx(xv,yv)
                    else:
                        self.axes.semilogx(xv,yv,**string_to_dict(args[0]))
            else:
                if self.logy==True:
                    if len(args)<1:
                        self.axes.semilogy(xv,yv)
                    else:
                        self.axes.semilogy(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        self.axes.plot(xv,yv)
                    else:
                        self.axes.plot(xv,yv,**string_to_dict(args[0]))
                            
            if self.xset==True:
                self.axes.set_xlim(self.xlo,self.xhi)
            if self.yset==True:
                self.axes.set_ylim(self.ylo,self.yhi)
                    
        # End of function o2graph_plotter::plot1()
        return
            
    def plotv(self,o2scl_hdf,amp,args):
        """
        Plot one or two multiple vector specifications
        """

        char_ptr=ctypes.POINTER(ctypes.c_char)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)
        
        if curr_type==b'vector<contour_line>':
             print('Store and clear the vector<contour_line> object '+
                   'before using \'plotv\'.')
             return 1
        
        conv_fn=o2scl_hdf.o2scl_acol_mult_vectors_to_conts
        conv_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                          ctypes.c_char_p]
        conv_fn.restype=ctypes.c_int

        if len(args)>=2:
            if self.verbose>1:
                print('Calling mult_vectors_to_conts() with',
                      args[0],'and',args[1])
            mvs1=ctypes.c_char_p(force_bytes(args[0]))
            mvs2=ctypes.c_char_p(force_bytes(args[1]))
            conv_ret=conv_fn(amp,mvs1,mvs2)
            if conv_ret!=0:
                print('Failed to read "'+args[0]+'" and "'+args[1]+'".')
                return 2
        else:
            if self.verbose>1:
                print('Calling mult_vectors_to_conts() with',
                      args[0])
            mvs1=ctypes.c_char_p(0)
            mvs2=ctypes.c_char_p(force_bytes(args[0]))
            conv_ret=conv_fn(amp,mvs1,mvs2)
            if conv_ret!=0:
                print('Failed to read "'+args[0])
                return 2
        
        
        # Get the total number of contour lines
        cont_n_fn=o2scl_hdf.o2scl_acol_contours_n
        cont_n_fn.argtypes=[ctypes.c_void_p]
        cont_n_fn.restype=ctypes.c_int
        nconts=cont_n_fn(amp)

        # Define types for extracting each contour line
        cont_line_fn=o2scl_hdf.o2scl_acol_contours_line
        cont_line_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                               int_ptr,double_ptr_ptr,
                               double_ptr_ptr]
        cont_line_fn.restype=ctypes.c_double

        if self.canvas_flag==False:
            self.canvas()

        # Loop over all contour lines
        for k in range(0,nconts):
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            ptry=double_ptr()
            lev=cont_line_fn(amp,k,ctypes.byref(idx),
                             ctypes.byref(ptrx),ctypes.byref(ptry))
            xv=[ptrx[i] for i in range(0,idx.value)]
            yv=[ptry[i] for i in range(0,idx.value)]
                
            if self.logx==True:
                if self.logy==True:
                    if len(args)<3:
                        self.axes.loglog(xv,yv)
                    else:
                        self.axes.loglog(xv,yv,**string_to_dict(args[2]))
                else:
                    if len(args)<3:
                        self.axes.semilogx(xv,yv)
                    else:
                        self.axes.semilogx(xv,yv,**string_to_dict(args[2]))
            else:
                if self.logy==True:
                    if len(args)<3:
                        self.axes.semilogy(xv,yv)
                    else:
                        self.axes.semilogy(xv,yv,**string_to_dict(args[2]))
                else:
                    if len(args)<3:
                        self.axes.plot(xv,yv)
                    else:
                        self.axes.plot(xv,yv,**string_to_dict(args[2]))
                        
        # End of function o2graph_plotter::plotv()
        return
        
    def print_param_docs(self):
        """
        Print parameter documentation.

        Called by help_func().
        """

        ter=terminal()
        str_line=ter.horiz_line()
        print('\n'+str_line)
        print('\nO2graph parameter list:')
        print(' ')
        for line in param_list:
            if line[0]!='verbose':
                if line[0]=='colbar':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.colbar))
                elif line[0]=='fig-dict':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.fig_dict))
                elif line[0]=='font':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.font))
                elif line[0]=='logx':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.logx))
                elif line[0]=='logy':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.logy))
                elif line[0]=='logz':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.logz))
                elif line[0]=='xhi':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.xhi))
                elif line[0]=='xlo':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.xlo))
                elif line[0]=='xset':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.xset))
                elif line[0]=='yhi':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.yhi))
                elif line[0]=='ylo':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.ylo))
                elif line[0]=='yset':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.yset))
                elif line[0]=='zhi':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.zhi))
                elif line[0]=='zlo':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.zlo))
                elif line[0]=='zset':
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg())+' '+str(self.zset))
                else:
                    print((ter.red_fg()+ter.bold()+line[0]+
                           ter.default_fg()))
                print(' '+line[1])
                print(' ')
        print(str_line)
        print('\nyt-related settings:')
        print(' ')
        for line in yt_param_list:
            if line[0]=='yt_filter':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+self.yt_filter)
            if line[0]=='yt_focus':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+self.yt_focus)
            if line[0]=='yt_position':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+self.yt_position)
            if line[0]=='yt_width':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+self.yt_width)
            if line[0]=='yt_north':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+self.yt_north)
            if line[0]=='yt_path':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+str(self.yt_path))
            if line[0]=='yt_resolution':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+str(self.yt_resolution))
            if line[0]=='yt_sigma_clip':
                print((ter.red_fg()+ter.bold()+line[0]+
                       ter.default_fg())+' '+str(self.yt_sigma_clip))
            print(' '+line[1])
            print(' ')

        # End of function o2graph_plotter::print_param_docs()
        return
            
    def parse_argv(self,argv,o2scl_hdf):
        """
        Parse command-line arguments.

        This is the main function used by the :ref:`o2graph_script` .
        Once it has created a list of strings from argv, it calls
        parse_string_list() to call the proper functions. It 
        creates the pointer to the o2scl acol_manager object 
        called `amp`.
        """
        
        # Create an acol_manager object and get the pointer
        o2scl_hdf.o2scl_create_acol_manager.restype=ctypes.c_void_p
        amp=o2scl_hdf.o2scl_create_acol_manager()

        names_fn=o2scl_hdf.o2scl_acol_set_names
        names_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p,
                           ctypes.c_int,ctypes.c_char_p,ctypes.c_int,
                           ctypes.c_char_p]

        # Get current type
        ter=terminal()
        cmd_name=b'o2graph'
        cmd_desc=(b'o2graph: A data viewing and '+
                  b'processing program for '+force_bytes(ter.bold())+
                  b'O2scl'+force_bytes(ter.default_fg())+
                  b'.\n  Version: '+force_bytes(version)+b'\n')
        env_var=b'O2GRAPH_DEFAULTS'
        names_fn(amp,len(cmd_name),ctypes.c_char_p(cmd_name),
                 len(cmd_desc),ctypes.c_char_p(cmd_desc),
                 len(env_var),ctypes.c_char_p(env_var))

        # Apply aliases before parsing. We convert argv 
        # to a set of integer and character arrays, then
        # pass them to o2scl_acol_apply_aliases()
        if True:

            orig_len=len(argv)
            
            int_ptr=ctypes.POINTER(ctypes.c_int)
            char_ptr=ctypes.POINTER(ctypes.c_char)
            int_ptr_ptr=ctypes.POINTER(int_ptr)
            char_ptr_ptr=ctypes.POINTER(char_ptr)

            # Allocate space for arrays
            tiarr=(ctypes.c_int*len(argv))()
            ttot=0
            for i in range(0,len(argv)):
                ttot+=len(argv[i])
            tcarr=(ctypes.c_char*ttot)()

            # Fill arrays with data
            tcnt=0
            for i in range(0,len(argv)):
                tiarr[i]=len(argv[i])
                #print(i,tiarr[i])
                for j in range(0,len(argv[i])):
                    tcarr[tcnt]=bytes(argv[i][j],'utf8')
                    #print(j,tcarr[tcnt])
                    tcnt=tcnt+1

            # Call the alias_counts() function to find out how big the
            # destination arrays need to be. This two step-process
            # allows python to handle the memory allocation.
            count_fn=o2scl_hdf.o2scl_acol_alias_counts
            count_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,int_ptr,
                               ctypes.c_char_p,int_ptr,int_ptr]
            n_new=ctypes.c_int(0)
            s_new=ctypes.c_int(0)
            count_fn(amp,len(argv),tiarr,tcarr,ctypes.byref(n_new),
                     ctypes.byref(s_new))

            # Allocate the new integer and string arrays
            tiarr2=(ctypes.c_int*n_new.value)()
            tcarr2=(ctypes.c_char*s_new.value)()

            # Setup and call alias function
            alias_fn=o2scl_hdf.o2scl_acol_apply_aliases
            alias_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,int_ptr,
                               ctypes.c_char_p,int_ptr,ctypes.c_char_p]
            alias_fn(amp,len(argv),tiarr,tcarr,tiarr2,tcarr2)

            # Construct the new argv list. We skip alias
            # definitions because they are already taken care of
            argv=[]
            icnt=0
            cnt=0
            iskip=0
            if len(tiarr2)!=orig_len:
                print('After applying alias,',orig_len,'->',len(tiarr2))
            for i in range(0,n_new.value):
                tstr=''
                for j in range(0,tiarr2[i]):
                    tstr=tstr+tcarr2[cnt].decode('utf-8')
                    cnt=cnt+1
                if tstr=='-alias':
                    iskip=2
                elif iskip==0:
                    argv.append(tstr)
                    if len(tiarr2)!=orig_len:
                        print(icnt,argv[icnt])
                    icnt=icnt+1
                else:
                    iskip=iskip-1
            
        if len(argv)<=1:
            done_flag=False
            readline.parse_and_bind('tab: complete')
            readline.parse_and_bind('set editing-mode emacs')
            while done_flag==False:
                line=input('o2graph> ')
                if line[0:4]=='quit' or line[0:4]=='exit':
                    done_flag=True
                else:
                    strlist=line.split(' ')
                    strlist[0]='-'+strlist[0]
                    self.parse_string_list(strlist,o2scl_hdf,amp)
        else:
            strlist=[str(argv[i]) for i in range(1,len(argv))]
            if self.verbose>2:
                print('Number of arguments:',len(strlist),'arguments.')
                print('Argument List:',strlist)
            self.parse_string_list(strlist,o2scl_hdf,amp)

        # End of function o2graph_plotter::parse_argv()
        return

    def yt_add_vol(self,o2scl_hdf,amp,keyname='o2graph_vol'):
        """
        Add a volume source to a yt visualization from a
        tensor_grid object.
        """

        int_ptr=ctypes.POINTER(ctypes.c_int)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)

        if curr_type==b'tensor_grid':
            self.yt_check_backend()
            import yt
            from yt.visualization.volume_rendering.api \
                import VolumeSource
            from yt.visualization.volume_rendering.transfer_function_helper \
                import TransferFunctionHelper

            # Set up wrapper for get function
            get_fn=o2scl_hdf.o2scl_acol_get_tensor_grid3
            get_fn.argtypes=[ctypes.c_void_p,int_ptr,int_ptr,
                             int_ptr,double_ptr_ptr,
                             double_ptr_ptr,double_ptr_ptr,
                             double_ptr_ptr]
            get_fn.restype=ctypes.c_int
             # Call get function
            nx=ctypes.c_int(0)
            ny=ctypes.c_int(0)
            nz=ctypes.c_int(0)
            ret=ctypes.c_int(0)
            gridx=double_ptr()
            gridy=double_ptr()
            gridz=double_ptr()
            data=double_ptr()
            ret=get_fn(amp,ctypes.byref(nx),ctypes.byref(ny),
                       ctypes.byref(nz),ctypes.byref(gridx),
                       ctypes.byref(gridy),ctypes.byref(gridz),
                       ctypes.byref(data))
            if ret==2:
                print("Object of type 'tensor_grid' does not have rank 3.")
                return
            elif ret==1:
                print("Object is not of type 'tensor_grid'.")
                return

            nx=nx.value
            ny=ny.value
            nz=nz.value
            total_size=nx*ny*nz

            if self.xset==False:
                self.xlo=gridx[0]
                self.xhi=gridx[nx-1]
                self.xset=True
            if self.yset==False:
                self.ylo=gridy[0]
                self.yhi=gridy[ny-1]
                self.yset=True
            if self.zset==False:
                self.zlo=gridz[0]
                self.zhi=gridz[nz-1]
                self.zset=True
            print('o2graph_plotter:yt-add-vol: axis limits:',
                  self.xlo,self.xhi,
                  self.ylo,self.yhi,self.zlo,self.zhi)
            
            arr=numpy.ctypeslib.as_array(data,shape=(nx,ny,nz))
            self.yt_volume_data.append(numpy.copy(arr))
            # Rescale to the internal coordinate system
            bbox=numpy.array([[(gridx[0]-self.xlo)/(self.xhi-self.xlo),
                               (gridx[nx-1]-self.xlo)/(self.xhi-self.xlo)],
                              [(gridy[0]-self.ylo)/(self.yhi-self.ylo),
                               (gridy[ny-1]-self.ylo)/(self.yhi-self.ylo)],
                              [(gridz[0]-self.zlo)/(self.zhi-self.zlo),
                               (gridz[nz-1]-self.zlo)/(self.zhi-self.zlo)]])
            self.yt_volume_bbox.append(numpy.copy(bbox))
            arr2=self.yt_volume_data[len(self.yt_volume_data)-1]
            bbox2=self.yt_volume_bbox[len(self.yt_volume_bbox)-1]

            func=yt.load_uniform_grid
            self.yt_data_sources.append(func(dict(density=arr2),
                                             arr2.shape,bbox=bbox2))
            ds=self.yt_data_sources[len(self.yt_data_sources)-1]

            self.yt_vols.append(VolumeSource(ds,field='density'))
            vol=self.yt_vols[len(self.yt_vols)-1]
            vol.log_field=False

            # Setup the transfer function
            if self.yt_tf!=0:
                vol.set_transfer_function(self.yt_tf)
                print(self.yt_tf)
            else:
                tfh=TransferFunctionHelper(ds)
                tfh.set_field('density')
                tfh.set_log(False)
                tfh.set_bounds()
                tfh.build_transfer_function()
                tfh.tf.add_layers(3)
                #tfh.plot('tf.png')
                vol.set_transfer_function(tfh.tf)
                print(tfh.tf)
                        
            if self.yt_created_scene==False:
                self.yt_create_scene()

            kname=self.yt_unique_keyname(keyname)
            self.yt_vol_keynames.append(kname)
            self.yt_scene.add_source(vol,keyname=kname)
                            
            if self.yt_created_camera==False:
                self.yt_create_camera(ds)
                
        # End of function o2graph_plotter::yt_add_vol()
        return
        
    def den_plot_anim(self,o2scl_hdf,amp,args):
        """
        Create an mp4 animation of a density plot from a tensor_grid3 
        object. The first argument specifies which tensor index is
        along the x axis, the second argument is the tensor index is
        along the y axis, and the third argument is the tensor index
        which will be animated.

        Experimental.
        """

        int_ptr=ctypes.POINTER(ctypes.c_int)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        
        curr_type=o2scl_get_type(o2scl_hdf,amp)

        if curr_type==b'tensor_grid':

            # Set up wrapper for get function
            get_fn=o2scl_hdf.o2scl_acol_get_tensor_grid3
            get_fn.argtypes=[ctypes.c_void_p,int_ptr,int_ptr,
                             int_ptr,double_ptr_ptr,
                             double_ptr_ptr,double_ptr_ptr,
                             double_ptr_ptr]
            get_fn.restype=ctypes.c_int
            
             # Call get function
            nx=ctypes.c_int(0)
            ny=ctypes.c_int(0)
            nz=ctypes.c_int(0)
            ret=ctypes.c_int(0)
            gridx=double_ptr()
            gridy=double_ptr()
            gridz=double_ptr()
            data=double_ptr()
            ret=get_fn(amp,ctypes.byref(nx),ctypes.byref(ny),
                       ctypes.byref(nz),ctypes.byref(gridx),
                       ctypes.byref(gridy),ctypes.byref(gridz),
                       ctypes.byref(data))
            if ret==2:
                print("Object of type 'tensor_grid' does not have rank 3.")
                return
            elif ret==1:
                print("Object is not of type 'tensor_grid'.")
                return

            nx=nx.value
            ny=ny.value
            nz=nz.value
            total_size=nx*ny*nz

            if args[0]=='0':
                xgrid=[gridx[i] for i in range(0,nx)]
                nx2=nx
            elif args[0]=='1':
                xgrid=[gridy[i] for i in range(0,ny)]
                nx2=ny
            else:
                xgrid=[gridz[i] for i in range(0,nz)]
                nx2=nz
            
            if args[1]=='0':
                ygrid=[gridx[i] for i in range(0,nx)]
                ny2=nx
            elif args[1]=='1':
                ygrid=[gridy[i] for i in range(0,ny)]
                ny2=ny
            else:
                ygrid=[gridz[i] for i in range(0,nz)]
                ny2=nz

            if args[2]=='0':
                n_frames=nx
            elif args[2]=='0r':
                n_frames=nx
            elif args[2]=='1':
                n_frames=ny
            elif args[2]=='1r':
                n_frames=ny
            elif args[2]=='2':
                n_frames=nz
            elif args[2]=='2r':
                n_frames=nz

            if n_frames>9999:
                print('Large number of frames (',n_frames,') not',
                      'supported in den-plot-anim.')
                return
            
            arr=numpy.ctypeslib.as_array(data,shape=(nx,ny,nz))
            print(arr.shape)

            if self.colbar==True:
                # The animation of the colorbar messes up the
                # automatic colorbar placement, so this is a hack to
                # attempt make sure the colorbar is placed correctly
                # in all frames.
                dct=string_to_dict(self.fig_dict)
                if ('right_margin' not in dct.keys() or
                    dct['right_margin']<0.1):
                    dct['right_margin']=0.15
                if ('top_margin' not in dct.keys() or
                    dct['top_margin']<0.06):
                    dct['top_margin']=0.06
                if 'left_margin' not in dct.keys():
                    dct['left_margin']=0.14
                if 'bottom_margin' not in dct.keys():
                    dct['bottom_margin']=0.12
                rm=dct['right_margin']
                lm=dct['left_margin']
                tm=dct['top_margin']
                bm=dct['bottom_margin']
                if self.canvas_flag==False:
                    if 'fontsize' not in dct.keys():
                        dct['fontsize']=self.font
                    (self.fig,self.axes)=default_plot(**dct)
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
            else:
                # If there's no colorbar, then we can use
                # the standard approach
                if self.canvas_flag==False:
                    self.canvas()
                
            if self.logx==True:
                for i in range(0,len(xgrid)):
                    xgrid[i]=math.log(xgrid[i],10)
                    
            if self.logy==True:
                for i in range(0,len(ygrid)):
                    ygrid[i]=math.log(ygrid[i],10)
                        
            for k in range(0,n_frames):
                if args[2]=='0':
                    sl=arr[k,:,:]
                elif args[2]=='0r':
                    sl=arr[n_frames-1-k,:,:]
                elif args[2]=='1':
                    sl=arr[:,k,:]
                elif args[2]=='0r':
                    sl=arr[:,n_frames-1-k,:]
                elif args[2]=='2':
                    sl=arr[:,:,k]
                elif args[2]=='2r':
                    sl=arr[:,:,n_frames-1-k]
                sl=sl.transpose()
 
                if self.logz==True:
                    fail_found=False
                    for i in range(0,len(ygrid)):
                        for j in range(0,len(xgrid)):
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
                    for i in range(0,ny2):
                        for j in range(0,nx2):
                            if sl[i][j]>self.zhi:
                                sl[i][j]=self.zhi
                            elif sl[i][j]<self.zlo:
                                sl[i][j]=self.zlo
                            
                diffs_x=[xgrid[i+1]-xgrid[i] for i in range(0,len(xgrid)-1)]
                mean_x=numpy.mean(diffs_x)
                std_x=numpy.std(diffs_x)
                diffs_y=[ygrid[i+1]-ygrid[i] for i in range(0,len(ygrid)-1)]
                mean_y=numpy.mean(diffs_y)
                std_y=numpy.std(diffs_y)
            
                if std_x/mean_x>1.0e-4 or std_x/mean_x>1.0e-4:
                    print('Warning in o2graph::o2graph_plotter::'+
                          'den_plot_anim():')
                    print('  Nonlinearity of x or y grid is greater than '+
                          '10^{-4}.')
                    print('  Value of std(diff_x)/mean(diff_x): %7.6e .' %
                          (std_x/mean_x))
                    print('  Value of std(diff_y)/mean(diff_y): %7.6e .' %
                          (std_y/mean_y))
                    print('  The density plot may not be properly scaled.')
                
                tmp1=xgrid[0]-(xgrid[1]-xgrid[0])/2
                tmp2=xgrid[nx2-1]+(xgrid[nx2-1]-xgrid[nx2-2])/2
                tmp3=ygrid[0]-(ygrid[1]-ygrid[0])/2
                tmp4=ygrid[ny2-1]+(ygrid[ny2-1]-ygrid[ny2-2])/2
                
                if k>0:
                    # It's important to remove the last image and
                    # colorbar to free up the space. We have to
                    # remmove the colorbar first, then the image.
                    if self.colbar==True:
                        self.cbar.remove()
                        del self.cbar
                    self.last_image.remove()
                    del self.last_image
                        
                self.last_image=self.axes.imshow(sl,interpolation='nearest',
                                                 origin='lower',
                                                 extent=[tmp1,tmp2,
                                                         tmp3,tmp4],
                                                 aspect='auto')
                
                if self.colbar==True:
                    dpa_cax2=self.fig.add_axes([1.0-rm*0.9,
                                                bm,rm*0.3,
                                                1.0-bm-tm])
                    self.cbar=self.fig.colorbar(self.last_image,
                                                cax=dpa_cax2)
                    self.cbar.ax.tick_params('both',length=6,width=1,
                                             which='major')
                    self.cbar.ax.tick_params(labelsize=self.font*0.8)
                    
                if n_frames<10:
                    fname='/tmp/dpa_'+str(k)+'.png'
                elif n_frames<100:
                    if k<10:
                        fname='/tmp/dpa_0'+str(k)+'.png'
                    else:
                        fname='/tmp/dpa_'+str(k)+'.png'
                elif n_frames<1000:
                    if k<10:
                        fname='/tmp/dpa_00'+str(k)+'.png'
                    elif k<100:
                        fname='/tmp/dpa_0'+str(k)+'.png'
                    else:
                        fname='/tmp/dpa_'+str(k)+'.png'
                elif n_frames<10000:
                    if k<10:
                        fname='/tmp/dpa_000'+str(k)+'.png'
                    elif k<100:
                        fname='/tmp/dpa_00'+str(k)+'.png'
                    elif k<1000:
                        fname='/tmp/dpa_0'+str(k)+'.png'
                    else:
                        fname='/tmp/dpa_'+str(k)+'.png'
                print('Saving to',fname)
                plot.savefig(fname)

                # End of loop, continue to next frame

            # Now after loop, compile frames into a movie
            prefix='/tmp/dpa_'
            suffix='.png'
            mov_fname=args[3]
            if n_frames>=1000:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%04d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
            elif n_frames>=100:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%03d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
            elif n_frames>=10:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%02d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
            else:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%01d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
            print('ffmpeg command:',cmd)
            os.system(cmd)

            # End of "if curr_type==b'tensor_grid':"
                
        # End of function o2graph_plotter::den_plot_anim()
        return
        
    def help_func(self,o2scl_hdf,amp,args):
        """
        Function to process the help command.
        """
        
        cmd=''

        ter=terminal()
                    
        str_line=ter.horiz_line()

        # Get current type
        curr_type=''
        curr_type=o2scl_get_type(o2scl_hdf,amp)

        if len(args)==1:
            cmd=args[0]
        elif len(args)==2:
            # If both a type and command are specified
                        
            curr_type=args[0]
            cmd=args[1]

        # See if we matched an o2graph command
        match=False
                    
        # Handle the case of an o2graph command from the
        # base list
        for line in base_list:
            if cmd==line[0]:
                match=True
                print('Usage: '+ter.cyan_fg()+ter.bold()+cmd+
                      ter.default_fg()+
                      ' '+line[2]+'\n\n'+line[1]+'\n')
                tempx_arr=wrap_line(line[3])
                for i in range (0,len(tempx_arr)):
                    print(tempx_arr[i])
                                
        # Handle the case of an o2graph command from the
        # extra list
        for line in extra_list:
            if ((curr_type==line[0] or
                 curr_type==force_bytes(line[0])) and
                cmd==line[1]):
                match=True
                print('Usage: '+ter.cyan_fg()+cmd+ter.default_fg()+
                      ' '+line[3]+'\n\n'+line[2]+'\n')
                tempx_arr=wrap_line(line[4])
                for i in range (0,len(tempx_arr)):
                    print(tempx_arr[i])

        # If we haven't matched yet, then show commands for
        # other types
        if match==False:
            for line in extra_list:
                if cmd==line[1]:
                    match=True
                    str_line=ter.horiz_line()
                    print('\n'+str_line)
                    print('Type '+ter.magenta_fg()+line[0]+
                          ter.default_fg()+':')
                    print('Usage: '+cmd+' '+ter.cyan_fg()+line[3]+
                          ter.default_fg()+'\n\n'+line[2]+'\n')
                    
                    tempx_arr=line[4].split('\n')
                    for j in range(0,len(tempx_arr)):
                        if len(tempx_arr[j])<79:
                            print(tempx_arr[j])
                        else:
                            str_list=textwrap.wrap(tempx_arr[j],79)
                            for i in range (0,len(str_list)):
                                print(str_list[i])

        # If we haven't matched yet, check for get/set parameters
        if match==False:
            for line in param_list:
                if cmd==line[0]:
                    match=True
                    print('O2graph parameter modified by get/set: '+
                          line[0]+'\n')
                    
                    tempx_arr=line[1].split('\n')
                    for j in range(0,len(tempx_arr)):
                        if len(tempx_arr[j])<79:
                            print(tempx_arr[j])
                        else:
                            str_list=textwrap.wrap(tempx_arr[j],79)
                            for i in range (0,len(str_list)):
                                print(str_list[i])

        # If we haven't matched yet, check for get/set parameters
        # from yt
        if match==False:
            for line in yt_param_list:
                if cmd==line[0]:
                    match=True
                    print('yt parameter modified by get/set: '+line[0]+'\n')
                    
                    tempx_arr=line[1].split('\n')
                    for j in range(0,len(tempx_arr)):
                        if len(tempx_arr[j])<79:
                            print(tempx_arr[j])
                        else:
                            str_list=textwrap.wrap(tempx_arr[j],79)
                            for i in range (0,len(str_list)):
                                print(str_list[i])
                                
        finished=False
        
        if cmd=='cmaps' and len(args)==1:
            cmap_list_func()
            finished=True

        if (len(args)==1 or len(args)==2) and args[0]=='cmaps-plot':
            if len(args)==2:
                cmaps_plot(args[1])
            else:
                cmaps_plot()
            finished=True
            
        if (len(args)==1 or len(args)==2) and args[0]=='colors-plot':
            if len(args)==2:
                colors_plot(args[1])
            else:
                colors_plot()
            finished=True

        if (len(args)<=3 and len(args)>=1 and args[0]=='colors-near'):
            if len(args)==3:
                colors_near(col=args[1],fname=args[2])
            elif len(args)==2:
                colors_near(col=args[1])
            else:
                colors_near()
            finished=True
                        
        if (cmd=='colors') and len(args)==1:
            color_list()
            finished=True
                        
        if (cmd=='xkcd-colors') and len(args)==1:
            xkcd_colors_list()
            finished=True

        if (cmd=='markers') and len(args)==1:
            marker_list()
            finished=True
            
        if (len(args)==1 or len(args)==2) and args[0]=='markers-plot':
            if len(args)==2:
                markers_plot(args[1])
            else:
                markers_plot()
            finished=True

        if match==False and finished==False:
            
            # C types
            int_ptr=ctypes.POINTER(ctypes.c_int)
            int_ptr_ptr=ctypes.POINTER(int_ptr)
            char_ptr=ctypes.POINTER(ctypes.c_char)
            char_ptr_ptr=ctypes.POINTER(char_ptr)
        
            # Function interface
            get_fn=o2scl_hdf.o2scl_acol_get_cli_options
            get_fn.argtypes=[ctypes.c_void_p,int_ptr,int_ptr_ptr,
                             char_ptr_ptr]
            get_fn.restype=ctypes.c_int

            # Arguments
            size=ctypes.c_int(0)
            iptr=int_ptr()
            cptr=char_ptr()
        
            # Function call
            get_ret=get_fn(amp,ctypes.byref(size),
                           ctypes.byref(iptr),ctypes.byref(cptr))

            desc_fn=o2scl_hdf.o2scl_acol_cli_option_desc
            desc_fn.argtypes=[ctypes.c_void_p,char_ptr,int_ptr,
                              char_ptr_ptr]
            desc_fn.restype=ctypes.c_int

            # tlist is the list of acol commands
            tlist=get_ic_ptrs_to_list(size,iptr,cptr)

            # If specified, look up command in acol list
            acol_match=False
            if len(args)>0:
                for j in range(0,len(tlist)):
                    if string_equal_dash(tlist[j],args[0]):
                        acol_match=True

            # If there was no match, do a command list
            if acol_match==False:
                print('o2graph: A data viewing and '+
                      'processing program for '+ter.bold()+
                      'O2scl'+ter.default_fg()+
                      '.\n  Version: '+version)
                print(' ')
                if curr_type==b'':
                    print('List of command-line options which',
                          'do not require a current object:\n')
                else:
                    print('List of command-line options',
                          '(current object type is',
                          curr_type.decode('utf-8')+'):\n')
                full_list=[]
                for j in range(0,len(tlist)):
                    opt_name=ctypes.c_char_p(tlist[j])
                    desc_ret=desc_fn(amp,opt_name,iptr,cptr)
                    desc=b''
                    for k in range(0,iptr[0]):
                        desc=desc+cptr[k]
                    full_list.append([tlist[j],desc])
                for line in base_list:
                    full_list.append([force_bytes(line[0]),
                                      force_bytes(line[1])])
                if curr_type!='':
                    for line in extra_list:
                        if force_bytes(line[0])==curr_type:
                            full_list.append([force_bytes(line[1]),
                                              force_bytes(line[2])])
                full_list2=sorted(full_list,key=lambda x: x[0])
                max_len=0
                for k in range(0,len(full_list2)):
                    full_list2[k][0]=(ter.cyan_fg()+ter.bold()+
                                      full_list2[k][0].decode('utf-8')+
                                      ter.default_fg())
                    full_list2[k][1]=full_list2[k][1].decode('utf-8')
                    if length_without_colors(full_list2[k][0])>max_len:
                        max_len=length_without_colors(full_list2[k][0])
                for k in range(0,len(full_list2)):
                    strt='  '
                    extra=max_len-length_without_colors(full_list2[k][0])
                    strt+='-'+full_list2[k][0]
                    for ij in range(0,extra):
                        strt+=' '
                    strt+=' '+full_list2[k][1]
                    print(strt)
                print('\n'+str_line)
                help_topics=sorted(acol_help_topics+o2graph_help_topics)
                strt='Additional help topics: '
                for j in range(0,len(help_topics)):
                    if j<len(help_topics)-1:
                        strt+=(ter.green_fg()+ter.bold()+
                               help_topics[j]+ter.default_fg()+', ')
                    else:
                        strt+=('and '+ter.green_fg()+ter.bold()+
                               help_topics[j]+ter.default_fg()+'.')
                tlist=wrap_line(strt)
                for j in range(0,len(tlist)):
                    print(tlist[j])
            else:
                # Otherwise, it's an acol command so
                self.gen_acol(o2scl_hdf,amp,'help',args)
            
        # If the user specified 'help set', then print
        # the o2graph parameter documentation
        if (cmd=='set' or cmd=='get') and len(args)==1:
            self.print_param_docs()

        # End of function o2graph_plotter::help_func()
        return
        
    def yt_tf_func(self,args):
        """
        Update the yt transfer function.
        """

        if len(args)==0:
            print('Function yt_tf_func() requires arguments.')
            print('  For a new transfer function, args should be '+
                  "('new','min','max') or ('new','min','max','nbins')")
            print('  To add a Gaussian, args should be '+
                  "('gauss','loc','width','red','green','blue','alpha')")
            print('  To add a step function, args should be '+
                  "('step','low','high','red','green','blue','alpha')")
            print('  To plot the transfer function, args should be '+
                  "('plot','filename')")
            return

        if args[0]=='new':
            if len(args)<3:
                print('yt-tf new requires 3 arguments.')
                return
            import yt
            print('o2graph:yt-tf: New transfer function.')
            print('o2graph:yt-tf: min:',args[1],
                  'max:',args[2])
            if len(args)>=4:
                self.yt_tf=yt.ColorTransferFunction((float(eval(args[1])),
                                                     float(eval(args[2]))),
                                                    nbins=int(eval(args[3])),
                                                    grey_opacity=False)
            else:
                self.yt_tf=yt.ColorTransferFunction((float(eval(args[1])),
                                                     float(eval(args[2]))),
                                                    grey_opacity=False)
                
        elif args[0]=='gauss':
            if len(args)<7:
                print('yt-tf gauss requires 6 arguments.')
                return
            print('o2graph:yt-tf: Adding Gaussian to',
                  'transfer function.')
            print('o2graph:yt-tf: location:',args[1],
                  'width:',args[2])
            print('o2graph:yt-tf: r,g,b,a:',
                  args[3],args[4],
                  args[5],args[6])
            self.yt_tf.add_gaussian(float(eval(args[1])),
                                    float(eval(args[2])),
                                    [float(eval(args[3])),
                                     float(eval(args[4])),
                                     float(eval(args[5])),
                                     float(eval(args[6]))])
            
        elif args[0]=='plot':
            if len(args)<2:
                print('yt-tf plot requires 1 argument.')
                return
            print('o2graph:yt-tf: Storing',
                  'transfer function in file',args[1])
            self.yt_tf.plot(args[1])

        elif args[0]=='step':
            if len(args)<7:
                print('yt-tf step requires 6 arguments.')
                return
            print('o2graph:yt-tf: Adding step to',
                  'transfer function.')
            print('o2graph:yt-tf: start:',args[1],
                  'stop:',args[2])
            print('o2graph:yt-tf: r,g,b,a:',
                  args[3],args[4],
                  args[5],args[6])
            self.yt_tf.add_step(float(eval(args[1])),
                                float(eval(args[2])),
                                [float(eval(args[3])),
                                 float(eval(args[4])),
                                 float(eval(args[5])),
                                 float(eval(args[6]))])

        # End of function o2graph_plotter::yt_tf_func()
        return

    def yt_path_func(self,o2scl_hdf,amp,args):
        """
        Add a path to the list of yt animations for the next
        yt render.
        """

        self.yt_path.append(args)
        print('yt_path is',self.yt_path)
        
        return

    def yt_ann_func(self,o2scl_hdf,amp,args):
        """
        Add the o2graph commands specified in `args` to the 
        list of yt annotations to be used in the next yt render.
        The list or arguments in `args` must end with 'end'. 
        If `args` contains only one entry ('end'), then the
        list of annotations is cleared.
        """

        if len(args)==1 and force_bytes(args[0])==b'end':
            print('Clearing all yt annotations.')
        else:
            for i in range(0,len(args)):
                if force_bytes(args[i])!=b'end':
                    self.yt_ann.append(args[i])
            print('yt_ann is',self.yt_ann)
        
        return

    def yt_scatter(self,o2scl_hdf,amp,args):
        """
        Create a 3D scatter plot with yt using data from an
        O\ :sub:`2`\ scl table object
        """

        if len(args)<3:
            print('Function yt_scatter() requires three ',
                  'column arguments.')
            return

        column_x=args[0]
        column_y=args[1]
        column_z=args[2]
        size_column=''
        red_column=''
        green_column=''
        blue_column=''
        alpha_column=''
        if len(args)>=4:
            size_column=args[3]
        if len(args)>=5:
            red_column=args[4]
        if len(args)>=6:
            green_column=args[5]
        if len(args)>=7:
            blue_column=args[6]
        if len(args)>=8:
            alpha_column=args[7]
        
        int_ptr=ctypes.POINTER(ctypes.c_int)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
                    
        curr_type=o2scl_get_type(o2scl_hdf,amp)

        if curr_type==b'table':
            if self.yt_check_backend()==1:
                return

            import yt
            from yt.visualization.volume_rendering.api \
                import PointSource
                        
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int
                        
            colx=ctypes.c_char_p(force_bytes(column_x))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),
                           ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+
                      column_x+'".')
                failed=True
                            
            coly=ctypes.c_char_p(force_bytes(column_y))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),
                           ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+
                      column_y+'".')
                failed=True

            colz=ctypes.c_char_p(force_bytes(column_z))
            idz=ctypes.c_int(0)
            ptrz=double_ptr()
            get_ret=get_fn(amp,colz,ctypes.byref(idz),
                           ctypes.byref(ptrz))
            if get_ret!=0:
                print('Failed to get column named "'+
                      column_z+'".')
                failed=True

            if (force_bytes(size_column)==b'None' or
                force_bytes(size_column)==b'none'):
                size_column=''
            if (force_bytes(red_column)==b'None' or
                force_bytes(red_column)==b'none'):
                red_column=''
            if (force_bytes(green_column)==b'None' or
                force_bytes(green_column)==b'none'):
                green_column=''
            if (force_bytes(blue_column)==b'None' or
                force_bytes(blue_column)==b'none'):
                blue_column=''
            if (force_bytes(alpha_column)==b'None' or
                force_bytes(alpha_column)==b'none'):
                alpha_column=''

            print('size,red,green,blue,alpha:',size_column,red_column,
                  green_column,blue_column,alpha_column)
            
            if size_column!='':
                cols=ctypes.c_char_p(force_bytes(size_column))
                ids=ctypes.c_int(0)
                ptrs=double_ptr()
                get_ret=get_fn(amp,cols,ctypes.byref(ids),
                               ctypes.byref(ptrs))
                
            if red_column!='':
                colr=ctypes.c_char_p(force_bytes(red_column))
                idr=ctypes.c_int(0)
                ptrr=double_ptr()
                get_ret=get_fn(amp,colr,ctypes.byref(idr),
                               ctypes.byref(ptrr))
                
            if green_column!='':
                colg=ctypes.c_char_p(force_bytes(green_column))
                idg=ctypes.c_int(0)
                ptrg=double_ptr()
                get_ret=get_fn(amp,colg,ctypes.byref(idg),
                               ctypes.byref(ptrg))
                
            if blue_column!='':
                colb=ctypes.c_char_p(force_bytes(blue_column))
                idb=ctypes.c_int(0)
                ptrb=double_ptr()
                get_ret=get_fn(amp,colb,ctypes.byref(idb),
                               ctypes.byref(ptrb))
                
            if alpha_column!='':
                cola=ctypes.c_char_p(force_bytes(alpha_column))
                ida=ctypes.c_int(0)
                ptra=double_ptr()
                get_ret=get_fn(amp,cola,ctypes.byref(ida),
                               ctypes.byref(ptra))

            if red_column!='' and blue_column!='' and green_column!='':
                rescale_r=False
                rescale_g=False
                rescale_b=False
                for i in range(0,idr.value):
                    if ptrr[i]<0.0:
                        if rescale_r==False:
                            rescale_r=True
                            min_r=ptrr[i]
                            max_r=ptrr[i]
                        elif ptrr[i]<min_r:
                            min_r=ptrr[i]
                    if ptrr[i]>1.0:
                        if rescale_r==False:
                            rescale_r=True
                            min_r=ptrr[i]
                            max_r=ptrr[i]
                        elif ptrr[i]>max_r:
                            max_r=ptrr[i]
                    if ptrg[i]<0.0:
                        if rescale_g==False:
                            rescale_g=True
                            min_g=ptrg[i]
                            max_g=ptrg[i]
                        elif ptrg[i]<min_g:
                            min_g=ptrg[i]
                    if ptrg[i]>1.0:
                        if rescale_g==False:
                            rescale_g=True
                            min_g=ptrg[i]
                            max_g=ptrg[i]
                        elif ptrg[i]>max_g:
                            max_g=ptrg[i]
                    if ptrb[i]<0.0:
                        if rescale_b==False:
                            rescale_b=True
                            min_b=ptrb[i]
                            max_b=ptrb[i]
                        elif ptrb[i]<min_b:
                            min_b=ptrb[i]
                    if ptrb[i]>1.0:
                        if rescale_b==False:
                            rescale_b=True
                            min_b=ptrb[i]
                            max_b=ptrb[i]
                        elif ptrb[i]>max_b:
                            max_b=ptrb[i]
                if rescale_r:
                    print('Rescaling red range   (%0.6e,%0.6e) to (0,1)' %
                          (min_r,max_r))
                    for i in range(0,idr.value):
                        ptrr[i]=(ptrr[i]-min_r)/(max_r-min_r)
                if rescale_g:
                    print('Rescaling green range (%0.6e,%0.6e) to (0,1)' %
                          (min_g,max_g))
                    for i in range(0,idg.value):
                        ptrg[i]=(ptrg[i]-min_g)/(max_g-min_g)
                if rescale_b:
                    print('Rescaling blue range  (%0.6e,%0.6e) to (0,1)' %
                          (min_b,max_b))
                    for i in range(0,idb.value):
                        ptrb[i]=(ptrb[i]-min_b)/(max_b-min_b)
                
            if self.xset==False:
                self.xlo=ptrx[0]
                self.xhi=ptrx[0]
                for i in range(0,idx.value):
                    if ptrx[i]<self.xlo:
                        self.xlo=ptrx[i]
                    if ptrx[i]>self.xhi:
                        self.xhi=ptrx[i]
                print('Set xlimits to (%0.6e,%0.6e)' % (self.xlo,self.xhi))
                self.xset=True
            if self.yset==False:
                self.ylo=ptry[0]
                self.yhi=ptry[0]
                for i in range(0,idy.value):
                    if ptry[i]<self.ylo:
                        self.ylo=ptry[i]
                    if ptry[i]>self.yhi:
                        self.yhi=ptry[i]
                print('Set ylimits to (%0.6e,%0.6e)' % (self.ylo,self.yhi))
                self.yset=True
            if self.zset==False:
                self.zlo=ptrz[0]
                self.zhi=ptrz[0]
                for i in range(0,idz.value):
                    if ptrz[i]<self.zlo:
                        self.zlo=ptrz[i]
                    if ptrz[i]>self.zhi:
                        self.zhi=ptrz[i]
                print('Set zlimits to (%0.6e,%0.6e)' % (self.zlo,self.zhi))
                self.zset=True
            x_range=self.xhi-self.xlo
            y_range=self.yhi-self.ylo
            z_range=self.zhi-self.zlo

            icnt=0
            if self.yt_scene!=0:
                for key, value in self.yt_scene.sources.items():
                    print('yt-source-list',icnt,key,type(value))
                    icnt=icnt+1
            if icnt==0:
                self.yt_def_vol()
            
            pts=[]
            cols=[]
            sizes=[]
            for i in range(0,idx.value):
                pts.append([(ptrx[i]-self.xlo)/x_range,
                            (ptry[i]-self.ylo)/y_range,
                            (ptrz[i]-self.zlo)/z_range])
                if red_column=='' or blue_column=='' or green_column=='':
                    cols.append([1.0,1.0,1.0,0.5])
                else:
                    if alpha_column=='':
                        cols.append([ptrr[i],ptrg[i],ptrb[i],1.0])
                    else:
                        cols.append([ptrr[i],ptrg[i],ptrb[i],ptra[i]])
                if size_column=='':
                    sizes.append(3)
                else:
                    sizes.append(int(ptrs[i]))
            pts2=numpy.array(pts)
            cols2=numpy.array(cols)
            sizes2=numpy.array(sizes)
            #print('cols2:',cols2[0],cols2[1],cols2[len(cols2)-1])
            #print('sizes2:',sizes2[0],sizes2[1],sizes2[len(sizes2)-1])

            if len(args)>=9:
                ps=PointSource(pts2,colors=cols2,radii=sizes2,
                               **string_to_dict(args[8]))
            else:
                ps=PointSource(pts2,colors=cols2,radii=sizes2)

            #if self.yt_created_scene==False:
            #self.yt_create_scene()

            print('o2graph:yt-scatter: Adding point source.')
            kname=self.yt_unique_keyname('o2graph_scatter')
            self.yt_scene.add_source(ps,keyname=kname)
                        
            #if self.yt_created_camera==False:
            #self.yt_create_camera(ps)

        else:
            # The object curr_type is a bytes object, so we just use
            # commas and avoid trying to add the strings together
            print('Command yt-scatter does not work with type',
                  curr_type,'.')
            
        # End of function o2graph_plotter::yt_scatter()
        return
        
    def yt_vertex_list(self,o2scl_hdf,amp,args):
        """
        Plot a series of line segments between a list of
        vertices specified in an O\ :sub:`2`\ scl table.
        """

        if len(args)<3:
            print('Function yt_vertex_list() requires three ',
                  'column arguments.')
            return

        column_x=args[0]
        column_y=args[1]
        column_z=args[2]
        
        icnt=0
        if self.yt_scene!=0:
            for key, value in self.yt_scene.sources.items():
                print('yt-source-list',icnt,key,type(value))
                icnt=icnt+1
        if icnt==0:
            self.yt_def_vol()
        
        int_ptr=ctypes.POINTER(ctypes.c_int)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
                    
        curr_type=o2scl_get_type(o2scl_hdf,amp)

        if curr_type==b'table':
            if self.yt_check_backend()==1:
                return

            import yt
            from yt.visualization.volume_rendering.api \
                import LineSource
                        
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int
                        
            colx=ctypes.c_char_p(force_bytes(column_x))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),
                           ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+
                      column_x+'".')
                failed=True
                            
            coly=ctypes.c_char_p(force_bytes(column_y))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),
                           ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+
                      column_y+'".')
                failed=True

            colz=ctypes.c_char_p(force_bytes(column_z))
            idz=ctypes.c_int(0)
            ptrz=double_ptr()
            get_ret=get_fn(amp,colz,ctypes.byref(idz),
                           ctypes.byref(ptrz))
            if get_ret!=0:
                print('Failed to get column named "'+
                      column_z+'".')
                failed=True

            if self.xset==False:
                self.xlo=ptrx[0]
                self.xhi=ptrx[0]
                for i in range(0,idx.value):
                    if ptrx[i]<self.xlo:
                        self.xlo=ptrx[i]
                    if ptrx[i]>self.xhi:
                        self.xhi=ptrx[i]
                print('Set xlimits to (%0.6e,%0.6e)' % (self.xlo,self.xhi))
                self.xset=True
            if self.yset==False:
                self.ylo=ptry[0]
                self.yhi=ptry[0]
                for i in range(0,idy.value):
                    if ptry[i]<self.ylo:
                        self.ylo=ptry[i]
                    if ptry[i]>self.yhi:
                        self.yhi=ptry[i]
                print('Set ylimits to (%0.6e,%0.6e)' % (self.ylo,self.yhi))
                self.yset=True
            if self.zset==False:
                self.zlo=ptrz[0]
                self.zhi=ptrz[0]
                for i in range(0,idz.value):
                    if ptrz[i]<self.zlo:
                        self.zlo=ptrz[i]
                    if ptrz[i]>self.zhi:
                        self.zhi=ptrz[i]
                print('Set zlimits to (%0.6e,%0.6e)' % (self.zlo,self.zhi))
                self.zset=True
            x_range=self.xhi-self.xlo
            y_range=self.yhi-self.ylo
            z_range=self.zhi-self.zlo

            pts=[]
            cols=[]
            sizes=[]
            for i in range(0,idx.value-1):
                pts.append([[(ptrx[i]-self.xlo)/x_range,
                             (ptry[i]-self.ylo)/y_range,
                             (ptrz[i]-self.zlo)/z_range],
                            [(ptrx[i+1]-self.xlo)/x_range,
                             (ptry[i+1]-self.ylo)/y_range,
                             (ptrz[i+1]-self.zlo)/z_range]])
                cols.append([1.0,1.0,1.0,1.0])
            pts2=numpy.array(pts)
            cols2=numpy.array(cols)

            ls=LineSource(pts2,cols2)

            #if self.yt_created_scene==False:
            #self.yt_create_scene()

            print('o2graph:yt-vertex-list: Adding point source.')
            kname=self.yt_unique_keyname('o2graph_vertex_list')
            self.yt_scene.add_source(ls,keyname=kname)
                        
            #if self.yt_created_camera==False:
            #self.yt_create_camera(ps)

        else:
            print('Command yt-vertex-list does not work with type',
                  curr_type+'.')
            
        # End of function o2graph_plotter::yt_vertex_list()
        return
        
    def commands(self,o2scl_hdf,amp,args):
        """
        Output the currently available commands.
        """

        self.gen_acol(o2scl_hdf,amp,'commands',args)
                    
        if len(args)>0:
            
            curr_type=args[0]
                        
        else:

            # Get current type
            int_ptr=ctypes.POINTER(ctypes.c_int)
            char_ptr=ctypes.POINTER(ctypes.c_char)
            char_ptr_ptr=ctypes.POINTER(char_ptr)
            
            curr_type=o2scl_get_type(o2scl_hdf,amp)
                
        print('O2graph commands for type '+
              str(curr_type)+':\n')
        strout=''
        for line in base_list:
            strout+=line[0]+' '
        for line in extra_list:
            if (curr_type==line[0] or
                curr_type==force_bytes(line[0])):
                strout+=line[1]+' '
        str_list=textwrap.wrap(strout,79)
        for i in range (0,len(str_list)):
            print(str_list[i])

        # End of function o2graph_plotter::commands()
        return

    def yt_save_annotate(self,o2scl_hdf,amp,fname):
        """
        Create a .png image, then add 2D annotations, 
        save to file named 'fname', and then apply any filters
        
        """
        
        if len(self.yt_ann)==0:
            
            # No animation and no annotation, so just call
            # scene.save()
            print('o2graph:yt_save_annotate: Calling yt_scene.save()',
                  'with filename',fname)
            self.yt_scene.save(fname,sigma_clip=self.yt_sigma_clip)
            
        else:

            # This segment of code is based off of yt's save_annotate()
            # function.
            self.yt_scene.render()
            fa=self.yt_scene._show_mpl
            axt=fa(self.yt_scene._last_render.swapaxes(0,1),
                   sigma_clip=self.yt_sigma_clip,dpi=100)
            self.yt_trans=self.yt_scene._render_figure.transFigure
            self.axes=axt.axes
            self.fig=self.yt_scene._render_figure
            self.canvas_flag=True
            print('Adding annotations:')
            self.parse_string_list(self.yt_ann,o2scl_hdf,amp)
            print('Done adding annotations:')
            #self.text(0.1,0.9,'x',color='w',fontsize=self.font*1.25,
                #transform=tf)
            self.canvas_flag=False
            #axt.axes.text(0.1,0.9,'test',color='w',transform=tf,
            #fontsize=self.font*1.25)
            from yt.visualization._mpl_imports import FigureCanvasAgg
            canvast=FigureCanvasAgg(self.yt_scene._render_figure)
            self.yt_scene._render_figure.canvas=canvast
            #self.yt_scene._render_figure.tight_layout(pad=0.0)
            plot.subplots_adjust(left=0.0,bottom=0.0,
                                 right=1.0,top=1.0)
            print('o2graph:yt-render: Calling savefig() with annotations.')
            self.yt_scene._render_figure.savefig(fname,facecolor='black',
                                                 pad_inches=0)

        # After having saved the image, filter it
        self.filter_image(fname)
            
        return

    def _make_fname(self,prefix,suffix,i_frame,n_frames):
        """
        Construct the animation filename from frame index and frame total,
        padding with zeros when necessary.
        """
        if n_frames>=1000:
            if i_frame<10:
                fname2=prefix+'000'+str(i_frame)+suffix
            elif i_frame<100:
                fname2=prefix+'00'+str(i_frame)+suffix
            elif i_frame<1000:
                fname2=prefix+'0'+str(i_frame)+suffix
            else:
                fname2=prefix+str(i_frame)+suffix
        elif n_frames>=100:
            if i_frame<10:
                fname2=prefix+'00'+str(i_frame)+suffix
            elif i_frame<100:
                fname2=prefix+'0'+str(i_frame)+suffix
            else:
                fname2=prefix+str(i_frame)+suffix
        elif n_frames>=10:
            if i_frame<10:
                fname2=prefix+'0'+str(i_frame)+suffix
            else:
                fname2=prefix+str(i_frame)+suffix
        else:
            fname2=prefix+str(i_frame)+suffix
        return fname2

    def restore_position(self,pos):
        """
        Restore the value of self.yt_position from the array 'pos'
        which is 
        """
        
        if self.yt_position=='default':
            self.yt_position=str([pos[0]*(self.xhi-self.xlo)+
                                  self.xlo,
                                  pos[1]*(self.yhi-self.ylo)+
                                  self.ylo,
                                  pos[2]*(self.zhi-self.zlo)+
                                  self.zlo])
        elif len(self.yt_position.split(' '))==2:
            splittemp=self.yt_position.split(' ')
            if splittemp[1]=='internal':
                self.yt_position=(str([pos[0],pos[1],pos[2]])+
                                  ' internal')
            else:
                self.yt_position=str([pos[0]*(self.xhi-self.xlo)+
                                      self.xlo,
                                      pos[1]*(self.yhi-self.ylo)+
                                      self.ylo,
                                      pos[2]*(self.zhi-self.zlo)+
                                      self.zlo])
        else:
            self.yt_position=str([pos[0]*(self.xhi-self.xlo)+
                                  self.xlo,
                                  pos[1]*(self.yhi-self.ylo)+
                                  self.ylo,
                                  pos[2]*(self.zhi-self.zlo)+
                                  self.zlo])
        print('restored self.yt_position:',
              self.yt_position)
        return

    def restore_focus(self,foc):
        """
        Restore the value of self.yt_focus from the array 'foc'.
        """
        
        if (len(self.yt_focus.split(' '))==2 and
            self.yt_focus.split(' ')[1]=='internal'):
            self.yt_focus=(str([foc[0],foc[1],foc[2]])+
                           ' internal')
        else:
            self.yt_focus=str([foc[0]*(self.xhi-self.xlo)+self.xlo,
                               foc[1]*(self.yhi-self.ylo)+self.ylo,
                               foc[2]*(self.zhi-self.zlo)+self.zlo])
        print('restored self.yt_focus:',
              self.yt_focus)

    def restore_north(self,nor):
        """
        Restore the value of self.yt_north from the array 'nor'.
        """
        self.yt_north=[nor[0],nor[1],nor[2]]
        return
        
    def restore_width(self,wid):
        """
        Restore the value of self.yt_width from the array 'wid'.
        """
        self.yt_width=[wid[0],wid[1],wid[2]]
        return
        
    def create_camera_vecs(self):
        """
        Create vectors (pos,foc,nor,wid) from the user settings in
        yt_position, yt_focus, yt_north and yt_width. This function is
        used in yt_render to keep track of the camera properties.
        The output vectors are always created in the internal 
        coordinate system.
        """
        
        # Create position array
        if self.yt_position=='default':
            pos=[1.5,0.6,0.7]
        elif len(self.yt_position.split(' '))==2:
            splittemp=self.yt_position.split(' ')
            if splittemp[1]=='internal':
                pos=[float(splittemp[0][0]),
                     float(splittemp[0][1]),
                     float(splittemp[0][2])]
            else:
                pos=[(float(splittemp[0][0])-self.xlo)/
                     (self.xhi-self.xlo),
                     (float(splittemp[0][1])-self.ylo)/
                     (self.yhi-self.ylo),
                     (float(splittemp[0][2])-self.zlo)/
                     (self.zhi-self.zlo)]
        else:
            pos=[(eval(self.yt_position)[0]-self.xlo)/
                 (self.xhi-self.xlo),
                 (eval(self.yt_position)[1]-self.ylo)/
                 (self.yhi-self.ylo),
                 (eval(self.yt_position)[2]-self.zlo)/
                 (self.zhi-self.zlo)]

        # Create focus array
        if self.yt_focus=='default':
            foc=[0.5,0.5,0.5]
        elif len(self.yt_focus.split(' '))==2:
            splittemp=self.yt_focus.split(' ')
            if splittemp[1]=='internal':
                foc=[float(splittemp[0][0]),
                     float(splittemp[0][1]),
                     float(splittemp[0][2])]
            else:
                foc=[(float(splittemp[0][0])-self.xlo)/
                     (self.xhi-self.xlo),
                     (float(splittemp[0][1])-self.ylo)/
                     (self.yhi-self.ylo),
                     (float(splittemp[0][2])-self.zlo)/
                     (self.zhi-self.zlo)]
        else:
            foc=[(eval(self.yt_focus)[0]-self.xlo)/
                 (self.xhi-self.xlo),
                 (eval(self.yt_focus)[1]-self.ylo)/
                 (self.yhi-self.ylo),
                 (eval(self.yt_focus)[2]-self.zlo)/
                 (self.zhi-self.zlo)]

        if self.yt_north=='default':
            nor=[0.0,0.0,1.0]
        else:
            nor=[float(eval(self.yt_north))[0],
                 float(eval(self.yt_north))[1],
                 float(eval(self.yt_north))[2]]
            
        if self.yt_width=='default':
            wid=[1.5,1.5,1.5]
        else:
            wid=[self.yt_width[0],
                 self.yt_width[1],
                 self.yt_width[2]]
            
        return (pos,foc,nor,wid)

    def filter_image(self,fname):
        """
        If a filter has been defined, apply that filter to the image
        stored in file ``fname``. This function is used in
        yt_save_annotate() to filter the images after saving them to a
        file.
        """
        if self.yt_filter!='':
            print('Found filter')
            cmd=self.yt_filter
            cmd=cmd.replace('%i',fname)
            cmd=cmd.replace('%o','/tmp/yt_filtered.png')
            print('Running filter command:\n  ',cmd)
            os.system(cmd)
            print('Moving file back:',
                  'mv /tmp/yt_filtered.png '+fname)
            os.system('mv /tmp/yt_filtered.png '+fname)
        return
    
    def yt_render(self,o2scl_hdf,amp,fname,mov_fname=''):
        """
        Complete the yt render and save the image to a file. If necessary,
        compile the images into a movie and save into the specified
        file name.
        """

        if self.yt_scene==0:
            print('Cannot perform a yt render without a scene.')
            return
        
        # AWS 10/14/19 the call to save() below does
        # the render() so I don't think I need this
        #self.yt_scene.render()

        if len(self.yt_path)==0:

            # No path, so just call save and finish
            self.yt_save_annotate(o2scl_hdf,amp,fname);

        else:

            # Setup destination filename
            if mov_fname=='':
                print('No movie filename specified so using',
                      'o2graph.mp4')
                mov_fname='o2graph.mp4'

            # Parse image file pattern
            asterisk=fname.find('*')
            prefix=fname[0:asterisk]
            suffix=fname[asterisk+1:len(fname)]
            print('o2graph:yt-render:',
                  'fname,prefix,suffix,mov_fname:\n  ',
                  fname,prefix,suffix,mov_fname)
                            
            # Count total frames
            n_frames=0
            for ip in range(0,len(self.yt_path)):
                n_frames=n_frames+int(self.yt_path[ip][1])
            print(n_frames,'total frames')

            # Render initial frame
            i_frame=0
            fname2=self._make_fname(prefix,suffix,i_frame,n_frames)
            self.yt_save_annotate(o2scl_hdf,amp,fname2);

            # Loop over all movements
            for ip in range(0,len(self.yt_path)):

                # Number of frames for this movement
                n_frames_move=int(self.yt_path[ip][1])
            
                if self.yt_path[ip][0]=='yaw':

                    angle=(float(self.yt_path[ip][2])*numpy.pi*2.0/
                           n_frames_move)

                    # Create arrays
                    (pos,foc,nor,wid)=self.create_camera_vecs()
                    print('yaw: camera pos, foc:',pos,foc)
                    print('yaw: camera nor, wid:',nor,wid)
                    
                    for ifr in range(0,n_frames_move):
                        
                        i_frame=i_frame+1
                        
                        print(self.yt_camera)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)

                        # We can't use the yt yaw() function because
                        # it modifies the camera properties in an
                        # undocumented way. 
                        
                        from yt.units.yt_array import YTArray
                        rv=YTArray([0,0,1])
                        #rc=YTArray([0.5,0.5,0.5])
                        self.yt_camera.rotate(angle,rot_vector=rv)
                        
                        xt=pos[0]-foc[0]
                        yt=pos[1]-foc[1]
                        zt=pos[2]-foc[2]
                        r=math.sqrt(xt**2+yt**2+zt**2)
                        theta=math.acos(zt/r)
                        phi=math.atan2(yt,xt)
                        phi+=angle
                        xt=r*math.sin(theta)*math.cos(phi)
                        yt=r*math.sin(theta)*math.sin(phi)
                        zt=r*math.cos(theta)
                        
                        pos[0]=foc[0]+xt
                        pos[1]=foc[1]+yt
                        pos[2]=foc[2]+zt
                        #print('yaw: new position:',pos)

                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.switch_orientation()
                            
                        print('Camera width [%0.6e,%0.6e,%0.6e]' %
                              (self.yt_camera.width[0],
                               self.yt_camera.width[1],
                               self.yt_camera.width[2]))
                            
                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl_hdf,amp,fname2);
                    
                        # End of 'for ifr in range(0,n_frames_move)'
                    
                    # Restore position array
                    self.restore_position(pos)
                    
                    # End of loop 'if self.yt_path[ip][0]=='yaw''
                    
                elif self.yt_path[ip][0]=='zoom':
                    
                    factor=float(self.yt_path[ip][2])

                    for ifr in range(0,n_frames_move):
                        
                        i_frame=i_frame+1
                        
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)
                        
                        # Move camera
                        ifactor=factor**(1.0/float(n_frames_move-1))
                        print('ifactor',ifactor)
                        self.yt_camera.zoom(ifactor)

                        print('Camera width [%0.6e,%0.6e,%0.6e]' %
                              (self.yt_camera.width[0],
                               self.yt_camera.width[1],
                               self.yt_camera.width[2]))
                        
                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl_hdf,amp,fname2);
                        
                        # End of 'for ifr in range(0,n_frames_move)'

                    # Width
                    self.restore_width(self.yt_camera.width)
                        
                    # End of loop 'if self.yt_path[ip][0]=='zoom''
                    
                elif self.yt_path[ip][0]=='move':

                    # Move the camera without changing the focus

                    dest=eval(self.yt_path[ip][2])
                    unit_system=self.yt_path[ip][3]
                    if unit_system=='user':
                        dest=[(float(dest[0])-self.xlo)/
                              (self.xhi-self.xlo),
                              (float(dest[1])-self.ylo)/
                              (self.yhi-self.ylo),
                              (float(dest[2])-self.zlo)/
                        (self.zhi-self.zlo)]
                    
                    # Create arrays
                    (source,foc,nor,wid)=self.create_camera_vecs()
                    print('move: camera pos, foc:',source,foc)
                    print('move: camera nor, wid:',nor,wid)
                    print('move: camera dest:',dest)

                    for ifr in range(0,n_frames_move):
                        
                        i_frame=i_frame+1
                    
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)

                        # Create the new position array
                        pos[0]=(source[0]+(dest[0]-source[0])*ifr/
                                (float(n_frames_move-1)))
                        pos[1]=(source[1]+(dest[1]-source[1])*ifr/
                                (float(n_frames_move-1)))
                        pos[2]=(source[2]+(dest[2]-source[2])*ifr/
                                (float(n_frames_move-1)))
                        
                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.switch_orientation()

                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl_hdf,amp,fname2);

                        # End of 'for ifr in range(0,n_frames_move)'
                        
                    # Restore position array
                    self.restore_position(pos)

                    # End of loop 'if self.yt_path[ip][0]=='move''
                    
                elif self.yt_path[ip][0]=='turn':

                    # Modify the focus without moving
                    
                    new_focus=eval(self.yt_path[ip][2])
                    unit_system=self.yt_path[ip][3]
                    if unit_system=='user':
                        new_focus=[(float(dest[0])-self.xlo)/
                                   (self.xhi-self.xlo),
                                   (float(dest[1])-self.ylo)/
                                   (self.yhi-self.ylo),
                                   (float(dest[2])-self.zlo)/
                                   (self.zhi-self.zlo)]
                    
                    # Create arrays
                    (pos,old_focus,nor,wid)=self.create_camera_vecs()
                    print('move: camera pos, foc:',pos,old_focus)
                    print('move: camera nor, wid:',nor,wid)
                    print('move: camera new focus:',new_focus)

                    for ifr in range(0,int(self.yt_path[ip][1])):
                        
                        i_frame=i_frame+1
                    
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)

                        # Create the new focus array
                        foc[0]=(old_focus[0]+(new_focus[0]-old_focus[0])*ifr/
                                (float(n_frames_move-1)))
                        foc[1]=(old_focus[1]+(new_focus[1]-old_focus[1])*ifr/
                                (float(n_frames_move-1)))
                        foc[2]=(old_focus[2]+(new_focus[2]-old_focus[2])*ifr/
                                (float(n_frames_move-1)))
                        
                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.switch_orientation()

                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl_hdf,amp,fname2);

                        # End of 'for ifr in range(0,n_frames_move)'
                        
                elif self.yt_path[ip][0]=='moveauto':

                    # Move the camera, automatically changing the
                    # focus to lie along the direction of motion
                    #
                    # The idea here is to do the turn at the beginning
                    # of the movement so that the initial frames turn
                    # toward the new focus while moving and the final
                    # frames just move to the final camera position.

                    print('unfinished')
                    quit()

                    # This is just a copy of the 'move' code from
                    # above
                    dest=eval(self.yt_path[ip][2])
                    unit_system=self.yt_path[ip][3]
                    if unit_system=='user':
                        dest=[(float(dest[0])-self.xlo)/
                              (self.xhi-self.xlo),
                              (float(dest[1])-self.ylo)/
                              (self.yhi-self.ylo),
                              (float(dest[2])-self.zlo)/
                        (self.zhi-self.zlo)]
                        
                    # Create arrays
                    (source,old_focus,nor,wid)=self.create_camera_vecs()

                    # The new focus is just beyond the destination,
                    # we arbitrarily choose 0.1
                    new_focus=[dest[0]-source[0]*0.1+dest[0],
                               dest[1]-source[1]*0.1+dest[1],
                               dest[2]-source[2]*0.1+dest[2]]
                    
                    print('move: camera old position, old focus:',source,
                          old_focus)
                    print('move: camera nor, wid:',nor,wid)
                    print('move: camera dest:',dest)
                    print('move: camera new focus:',new_focus)

                    for ifr in range(0,self.yt_path[ip][1]):
                        
                        i_frame=i_frame+1
                    
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)

                        frame_ratio=(float(ifr)/
                                     (float(self.yt_path[ip][1])-1))
                        
                        # Create the new position array
                        pos[0]=source[0]+(dest[0]-source[0])*frame_ratio
                        pos[1]=source[1]+(dest[1]-source[1])*frame_ratio
                        pos[2]=source[2]+(dest[2]-source[2])*frame_ratio

                        # This function makes the focus change quickly
                        # at first and then slowly at the end
                        foc_factor=0.11/(frame_ratio+0.1)-0.1

                        # Create the new focus array
                        foc[0]=(old_focus[0]+
                                (new_focus[0]-old_focus[0])*foc_factor)
                        foc[1]=(old_focus[1]+
                                (new_focus[1]-old_focus[1])*foc_factor)
                        foc[2]=(old_focus[2]+
                                (new_focus[2]-old_focus[2])*foc_factor)
                                
                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.switch_orientation()

                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl_hdf,amp,fname2);

                        # End of 'for ifr in range(0,n_frames_move)'
                        
                # End of 'for ip in range(0,len(self.yt_path)):'

            # -r is rate (in frames/sec), -f is format, -vcodec is
            # video codec (apparently 420p works well with quicktime),
            # -pix_fmt sepcifies the pixel format, -crf is the quality
            # (15-25 recommended) -y forces overwrite of the movie
            # file if it already exists

            if n_frames>=1000:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%04d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
            elif n_frames>=100:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%03d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
            elif n_frames>=10:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%02d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
            else:
                cmd=('ffmpeg -y -r 10 -f image2 -i '+
                     prefix+'%01d'+suffix+' -vcodec libx264 '+
                     '-crf 25 -pix_fmt yuv420p '+mov_fname)
                
            print('ffmpeg command:',cmd)
            os.system(cmd)

            # End of else for 'if len(self.yt_path)==0:'
            
        # End of function o2graph_plotter::yt_render()
        return

    def parse_string_list(self,strlist,o2scl_hdf,amp):
        """
        Parse a list of strings.

        This function is called by parse_argv().
        """
        if self.verbose>2:
            print('In parse_string_list()',strlist)
        
        ix=0
        while ix<len(strlist):
            
            if self.verbose>2:
                print('Processing index',ix,'with value',strlist[ix],'.')
                
            # Find first option, at index ix
            initial_ix_done=False
            while initial_ix_done==False:
                if ix==len(strlist):
                    initial_ix_done=True
                elif strlist[ix][0]=='-':
                    initial_ix_done=True
                else:
                    if self.verbose>2:
                         print('Incrementing ix')
                    ix=ix+1

            # If there is an option, then ix is its index
            if ix<len(strlist):
                
                cmd_name=strlist[ix][1:]
                # If there was two dashes, one will be left so
                # remove it
                if cmd_name[0]=='-':
                    cmd_name=cmd_name[1:]
                if self.verbose>2:
                    print('Found option',cmd_name,'at index',ix)
                # Set ix_next to the next option, or to the end if
                # there is no next option
                ix_next=ix+1
                ix_next_done=False
                while ix_next_done==False:

                    # Normally, o2graph and acol commands are ended by
                    # the next command-line argument which begins with
                    # a dash. We make an exception for yt-ann, which
                    # annotates a yt plot. yt-ann commands require
                    # the keyword "end" and the end to indicate that
                    # they are complete.
                    
                    if ix_next==len(strlist):
                        ix_next_done=True
                    elif (cmd_name!='yt-ann' and
                    len(strlist[ix_next])>0 and strlist[ix_next][0]=='-'):
                        ix_next_done=True
                    elif (cmd_name=='yt-ann' and ix_next>0 and
                    strlist[ix_next-1]=='end'):
                        ix_next_done=True
                    else:
                        if self.verbose>2:
                            print('Incrementing ix_next')
                        ix_next=ix_next+1

                # List of 'acol' commands for option processing loop
                acol_list=['a','alias','assign','autocorr','c',
                           'calc','cat','commands','contours','convert-unit',
                           'convert_unit','create','d','D',
                           'delete-col','delete-rows','delete-rows-tol',
                           'delete_col','delete_rows','delete_rows_tol',
                           'deriv','deriv2',
                           'download','entry','f','filelist','find-row',
                           'find_row','fit','function','g','gen3-list',
                           'gen3_list','generic','get-conv','get-row',
                           'get-unit','get_conv','get_row','get_unit',
                           'h','help','i','I','index','insert','insert-full',
                           'insert_full','integ','internal','interp',
                           'interp-type','interp_type','l','license','list',
                           'max','min','N','nlines','o','output','P',
                           'preview','q',
                           'r','read','rename','run',
                           's','S','select','select-rows',
                           'select_rows','select-rows2','select_rows2',
                           'set-data','set_data','set-unit',
                           'set_unit','show-units','show_units','slice',
                           'sort','stats','sum','to-hist','to_hist',
                           'to-hist-2d' 'to_hist_2d',
                           'to_table3d','to-table','to_table','to-table3d',
                           'type','v','warranty']
                
                # Now process the option
                if cmd_name=='set':

                    if self.verbose>2:
                        print('Process set.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for set option.')
                    else:
                        self.set_wrapper(o2scl_hdf,amp,strlist[ix+1:ix_next])
                        
                elif cmd_name=='get':
                    
                    if self.verbose>2:
                        print('Process get.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        self.get('No parameter specified to get.')
                    else:
                        self.get_wrapper(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='commands':
                    
                    if self.verbose>2:
                        print('Process commands.')
                        print('args:',strlist[ix:ix_next])

                    self.commands(o2scl_hdf,amp,
                                  strlist[ix+1:ix_next])
                    
                elif cmd_name=='yt-add-vol':

                    if self.verbose>2:
                        print('Process yt-add-vol.')
                        print('args:',strlist[ix:ix_next])

                    self.yt_add_vol(o2scl_hdf,amp)
                    
                elif cmd_name=='yt-scatter':

                    if self.verbose>2:
                        print('Process yt-scatter.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<4:
                        print('Not enough parameters for yt-scatter.')
                    else:
                        self.yt_scatter(o2scl_hdf,amp,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-path':

                    if self.verbose>2:
                        print('Process yt-path.')
                        print('args:',strlist[ix:ix_next])

                    if strlist[ix+1]=='reset':
                        print('Resetting yt-path.')
                        self.yt_path=[]
                    elif ix_next-ix<4:
                        print('Not enough parameters for yt-path.')
                    else:
                        self.yt_path_func(o2scl_hdf,amp,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-ann':

                    if self.verbose>2:
                        print('Process yt-ann.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<4:
                        print('Not enough parameters for yt-ann.')
                    else:
                        self.yt_ann_func(o2scl_hdf,amp,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-text':

                    if self.verbose>2:
                        print('Process yt-text.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<5:
                        print('Not enough parameters for yt-text.')
                    elif ix_next-ix>5:
                        self.yt_text(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     strlist[ix+4],
                                     **string_to_dict(strlist[ix+5]))
                    else:
                        self.yt_text(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     strlist[ix+4])
                                                    
                elif cmd_name=='yt-line':

                    if self.verbose>2:
                        print('Process yt-line.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<7:
                        print('Not enough parameters for yt-line.')
                    elif ix_next-ix>7:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_line([x1,y1,z1],[x2,y2,z2],
                                      **string_to_dict(strlist[ix+7]))
                    else:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_line([x1,y1,z1],[x2,y2,z2])
                                                    
                elif cmd_name=='yt-box':

                    if self.verbose>2:
                        print('Process yt-box.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<7:
                        print('Not enough parameters for yt-box.')
                    elif ix_next-ix>=8:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_box([x1,y1,z1],[x2,y2,z2],
                                      **string_to_dict(strlist[ix+7]))
                    else:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_box([x1,y1,z1],[x2,y2,z2])
                                                    
                elif cmd_name=='yt-arrow':

                    if self.verbose>2:
                        print('Process yt-arrow.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<6:
                        print('Not enough parameters for yt-arrow.')
                    elif ix_next-ix>=7:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_arrow([x1,y1,z1],[x2,y2,z2],
                                      **string_to_dict(strlist[ix+7]))
                    else:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_arrow([x1,y1,z1],[x2,y2,z2])
                                                    
                elif cmd_name=='yt-vertex-list':

                    if self.verbose>2:
                        print('Process yt-vertex-list.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<4:
                        print('Not enough parameters for yt-vertex-list.')
                    else:
                        self.yt_vertex_list(o2scl_hdf,amp,
                                            strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-source-list':

                    if self.verbose>2:
                        print('Process yt-source-list.')
                        print('args:',strlist[ix:ix_next])
                        
                    icnt=0
                    for key, value in self.yt_scene.sources.items():
                        tstr=("<class 'yt.visualization.volume_"+
                              "rendering.render_source.")
                        print('yt-source-list',icnt,key,
                              str(type(value)).replace(tstr,"<class '..."))
                        icnt=icnt+1
                    if icnt==0:
                        print('No yt sources.')
                    
                elif cmd_name=='yt-axis':

                    if self.verbose>2:
                        print('Process yt-axis.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        self.yt_plot_axis()
                    else:
                        self.yt_plot_axis(**string_to_dict(strlist[ix+1]))

                elif cmd_name=='yt-render':

                    if self.verbose>2:
                        print('Process render.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for yt-render.')
                    elif ix_next-ix<3:
                        self.yt_render(o2scl_hdf,amp,strlist[ix+1])
                    else:
                        self.yt_render(o2scl_hdf,amp,strlist[ix+1],
                                       mov_fname=strlist[ix+2])

                elif cmd_name=='yt-tf':

                    if self.verbose>2:
                        print('Process yt-tf.')
                        print('args:',strlist[ix:ix_next])

                    self.yt_tf_func(strlist[ix+1:ix_next])
                    
                elif cmd_name=='help' or cmd_name=='h':
                    
                    if self.verbose>2:
                        print('Process help.')
                        print('args:',strlist[ix:ix_next])

                    self.help_func(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='plot':
                    
                    if self.verbose>2:
                        print('Process plot.')
                        print('args:',strlist[ix:ix_next])

                    self.plot(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='plot-color':
                    
                    if self.verbose>2:
                        print('Process plot-color.')
                        print('args:',strlist[ix:ix_next])

                    self.plot_color(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='rplot':
                    
                    if self.verbose>2:
                        print('Process rplot.')
                        print('args:',strlist[ix:ix_next])

                    self.rplot(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='scatter':
                    
                    if self.verbose>2:
                        print('Process scatter.')
                        print('args:',strlist[ix:ix_next])

                    self.scatter(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='hist-plot':
                    
                    if self.verbose>2:
                        print('Process hist-plot.')
                        print('args:',strlist[ix:ix_next])

                    self.hist_plot(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='errorbar':
                    
                    if self.verbose>2:
                        print('Process errorbar.')
                        print('args:',strlist[ix:ix_next])

                    self.errorbar(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='hist2d-plot':
                    
                    if self.verbose>2:
                        print('Process hist2d-plot.')
                        print('args:',strlist[ix:ix_next])
                        
                    self.hist2d_plot(o2scl_hdf,amp,strlist[ix+1:ix_next])
                            
                elif cmd_name=='den-plot':
                    
                    if self.verbose>2:
                        print('Process den-plot.')
                        print('args:',strlist[ix:ix_next])

                    self.den_plot(o2scl_hdf,amp,strlist[ix+1:ix_next])
                
                elif cmd_name=='den-plot-rgb':
                    
                    if self.verbose>2:
                        print('Process den-plot-rgb.')
                        print('args:',strlist[ix:ix_next])

                    self.den_plot_rgb(o2scl_hdf,amp,strlist[ix+1:ix_next])
                
                elif cmd_name=='den-plot-anim':
                    
                    if self.verbose>2:
                        print('Process den-plot-anim.')
                        print('args:',strlist[ix:ix_next])

                    self.den_plot_anim(o2scl_hdf,amp,strlist[ix+1:ix_next])
                
                elif cmd_name=='plot1':
                    
                    if self.verbose>2:
                        print('Process plot1.')
                        print('args:',strlist[ix:ix_next])
                        
                    self.plot1(o2scl_hdf,amp,strlist[ix+1:ix_next])
                            
                elif cmd_name=='plotv':
                    
                    if self.verbose>2:
                        print('Process plotv.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for plotv option.')
                    else:
                        self.plotv(o2scl_hdf,amp,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='text':
                    
                    if self.verbose>2:
                        print('Process text.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for text option.')
                    elif ix_next-ix<5:
                        self.text(strlist[ix+1],strlist[ix+2],strlist[ix+3])
                    else:
                        self.text(strlist[ix+1],strlist[ix+2],strlist[ix+3],
                                  **string_to_dict(strlist[ix+4]))
                        
                elif cmd_name=='ttext':
                    
                    if self.verbose>2:
                        print('Process ttext.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for ttext option.')
                    elif ix_next-ix<5:
                        self.ttext(strlist[ix+1],strlist[ix+2],strlist[ix+3])
                    else:
                        self.ttext(strlist[ix+1],strlist[ix+2],strlist[ix+3],
                                   **string_to_dict(strlist[ix+4]))
                        
                elif cmd_name=='xlimits':
                    
                    if self.verbose>2:
                        print('Process xlimits.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for xlimits option.')
                    else:
                        self.xlimits(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])))
                        
                elif cmd_name=='ylimits':
                    
                    if self.verbose>2:
                        print('Process ylimits.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for ylimits option.')
                    else:
                        self.ylimits(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])))
                        
                elif cmd_name=='save':
                    
                    if self.verbose>2:
                        print('Process save.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for save option.')
                    else:
                        plot.savefig(strlist[ix+1])
                        
                elif cmd_name=='subplots':
                    
                    if self.verbose>2:
                        print('Process subplots.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for subplots option.')
                    elif ix_next-ix<3:
                        self.subplots(int(strlist[ix+1]))
                    elif ix_next-ix<4:
                        self.subplots(int(strlist[ix+1]),int(strlist[ix+2]))
                    else:
                        self.subplots(int(strlist[ix+1]),int(strlist[ix+2]),
                                      **string_to_dict(strlist[ix+3]))
                        
                elif cmd_name=='selax':
                    
                    if self.verbose>2:
                        print('Process selax.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for selax option.')
                    else:
                        self.selax(int(strlist[ix+1]))
                        
                elif cmd_name=='addcbar':
                    
                    if self.verbose>5:
                        print('Process addcbar.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for addcbar option.')
                    elif ix_next-ix<6:
                        self.addcbar(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     float(eval(strlist[ix+4])))
                    else:
                        self.addcbar(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     float(eval(strlist[ix+4])),
                                     **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='inset':
                    
                    if self.verbose>5:
                        print('Process inset.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for inset option.')
                    elif ix_next-ix<6:
                        self.inset(float(eval(strlist[ix+1])),
                                   float(eval(strlist[ix+2])),
                                   float(eval(strlist[ix+3])),
                                   float(eval(strlist[ix+4])))
                    else:
                        self.inset(float(eval(strlist[ix+1])),
                                   float(eval(strlist[ix+2])),
                                   float(eval(strlist[ix+3])),
                                   float(eval(strlist[ix+4])),
                                   **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='modax':
                    
                    if self.verbose>1:
                        print('Process modax.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for inset option.')
                    else:
                        self.modax(**string_to_dict(strlist[ix+1]))
                        
                elif cmd_name=='subadj':
                    
                    if self.verbose>2:
                        print('Process subadj.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for subadj option.')
                    else:
                        plot.subplots_adjust(**string_to_dict(strlist[ix+1]))
                        
                elif cmd_name=='xtitle':

                    if self.verbose>2:
                        print('Process xtitle.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for xtitle option.')
                    elif ix_next-ix==2:
                        self.xtitle(strlist[ix+1])
                    elif ix_next-ix>2 and ix_next-ix<5:
                        print('All three location parameters needed.')
                    elif ix_next-ix==5:
                        self.xtitle(strlist[ix+1],
                                    loc=[float(eval(strlist[ix+2])),
                                         float(eval(strlist[ix+3])),
                                         float(eval(strlist[ix+4]))])
                        
                elif cmd_name=='ytitle':
                    
                    if self.verbose>2:
                        print('Process ytitle.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for ytitle option.')
                    elif ix_next-ix==2:
                        self.ytitle(strlist[ix+1])
                    elif ix_next-ix>2 and ix_next-ix<5:
                        print('All three location parameters needed.')
                    elif ix_next-ix==5:
                        self.ytitle(strlist[ix+1],
                                    loc=[float(eval(strlist[ix+2])),
                                         float(eval(strlist[ix+3])),
                                         float(eval(strlist[ix+4]))])
                        
                # elif cmd_name=='ztitle':
                    
                #     if self.verbose>2:
                #         print('Process ztitle.')

                #     if ix_next-ix<2:
                #         print('Not enough parameters for ztitle option.')
                #     elif ix_next-ix==2:
                #         self.ztitle(strlist[ix+1])
                #     elif ix_next-ix>2 and ix_next-ix<5:
                #         print('All three location parameters needed.')
                #     elif ix_next-ix==5:
                #         self.ztitle(strlist[ix+1],
                #                     loc=[float(eval(strlist[ix+2])),
                #                          float(eval(strlist[ix+3])),
                #                          float(eval(strlist[ix+4]))])
                        
                elif cmd_name=='line':
                    
                    if self.verbose>2:
                        print('Process line.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for line option.')
                    elif ix_next-ix<6:
                        self.line(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4])
                    else:
                        self.line(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='o2scl-cpp-lib':
                    
                    if self.verbose>2:
                        print('Process o2scl-cpp-lib.')
                        print('args:',strlist[ix:ix_next])
                        
                elif cmd_name=='o2scl-lib-dir':
                    
                    if self.verbose>2:
                        print('Process o2scl-lib-dir.')
                        print('args:',strlist[ix:ix_next])
                    
                elif cmd_name=='o2scl-addl-libs':
                    
                    if self.verbose>2:
                        print('Process o2scl-addl-libs.')
                        print('args:',strlist[ix:ix_next])
                    
                elif cmd_name=='debug-first-pass':
                    
                    if self.verbose>2:
                        print('Process debug-first-pass.')
                        print('args:',strlist[ix:ix_next])
                    
                elif cmd_name=='textbox':
                    
                    if self.verbose>2:
                        print('Process textbox.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for textbox option.')
                    elif ix_next-ix<5:
                        self.textbox(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3])
                    elif ix_next-ix<6:
                        self.textbox(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4])
                    else:
                        self.textbox(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4],
                                     **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='arrow':
                    
                    if self.verbose>2:
                        print('Process arrow.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<6:
                        print('Not enough parameters for arrow option.')
                    elif ix_next-ix<7:
                        self.arrow(strlist[ix+1],strlist[ix+2],
                                   strlist[ix+3],strlist[ix+4],
                                   strlist[ix+5])
                    else:
                        self.arrow(strlist[ix+1],strlist[ix+2],
                                   strlist[ix+3],strlist[ix+4],
                                   strlist[ix+5],
                                   **string_to_dict(strlist[ix+6]))
                        
                elif cmd_name=='point':
                    
                    if self.verbose>2:
                        print('Process point.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for point option.')
                    elif ix_next-ix<4:
                        self.point(strlist[ix+1],strlist[ix+2])
                    else:
                        self.point(strlist[ix+1],strlist[ix+2],
                                   **string_to_dict(strlist[ix+3]))
                        
                elif cmd_name=='error-point':
                    
                    if self.verbose>2:
                        print('Process point.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for point option.')
                    elif ix_next-ix>=8:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4],
                                         strlist[ix+5],strlist[ix+6],
                                         **string_to_dict(strlist[ix+7]))
                    elif ix_next-ix>=7:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4],
                                         strlist[ix+5],strlist[ix+6])
                    elif ix_next-ix>=6:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4],
                                         **string_to_dict(strlist[ix+5]))
                    else:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4])
                        
                elif cmd_name=='python':
                    
                    if self.verbose>2:
                        print('Process python.')
                        print('args:',strlist[ix:ix_next])

                    print("The o2graph_plotter() object is named 'self'.")
                    print("Use 'import o2sclpy' and 'help(o2sclpy)' +"
                          "for more help on o2sclpy "+
                          "classes and functions.")
                    code.interact(local=locals())
                    
                elif cmd_name=='eval':
                    
                    if self.verbose>2:
                        print('Process eval.')
                        print('args:',strlist[ix:ix_next])

                    eval(strlist[ix+1],None,locals())
                    
                elif cmd_name=='exec':
                    
                    if self.verbose>2:
                        print('Process exec.')
                        print('args:',strlist[ix:ix_next])

                    exec(open(strlist[ix+1]).read(),None,locals())
                    
                elif cmd_name=='image':
                    
                    if self.verbose>2:
                        print('Process image.')
                        print('args:',strlist[ix:ix_next])

                    import matplotlib.image as img
                    im = img.imread(strlist[ix+1])
                    default_plot(0.0,0.0,0.0,0.0)
                    plot.imshow(im)
                    plot.show()
                    
                elif cmd_name=='rect':
                    
                    if self.verbose>2:
                        print('Process rect.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for rect option.')
                    elif ix_next-ix<6:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4])
                    elif ix_next-ix<7:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  strlist[ix+5])
                    else:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  strlist[ix+5],
                                  **string_to_dict(strlist[ix+6]))
                        
                elif cmd_name=='ellipse':
                    
                    if self.verbose>2:
                        print('Process ellipse.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for ellipse option.')
                    elif ix_next-ix<6:
                        self.ellipse(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4])
                    elif ix_next-ix<7:
                        self.ellipse(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4],
                                     strlist[ix+5])
                    else:
                        self.ellipse(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4],
                                     strlist[ix+5],
                                     **string_to_dict(strlist[ix+6]))
                        
                elif cmd_name=='show':
                    if self.verbose>2:
                        print('Process show.')
                        print('args:',strlist[ix:ix_next])
                    self.show()
                elif cmd_name=='move-labels':
                    if self.verbose>2:
                        print('Process move-labels.')
                        print('args:',strlist[ix:ix_next])
                    self.move_labels()
                elif cmd_name=='canvas':
                    if self.verbose>2:
                        print('Process canvas.')
                        print('args:',strlist[ix:ix_next])
                    self.canvas()
                elif cmd_name=='clf':
                    if self.verbose>2:
                        print('Process clf.')
                        print('args:',strlist[ix:ix_next])
                    plot.clf()
                    self.canvas_flag=False
                elif cmd_name=='backend':
                    if self.verbose>2:
                        print('Process backend in __init__.py.')
                        print('args:',strlist[ix:ix_next])
                else:
                    if self.verbose>2:
                        print('Process acol command '+cmd_name+'.')
                        print('args:',strlist[ix:ix_next])
                    self.gen_acol(o2scl_hdf,amp,cmd_name,
                                  strlist[ix+1:ix_next])
                    
                # Increment to the next option
                ix=ix_next
                
            if self.verbose>2:
                print('Going to next.')
                
        # End of function o2graph_plotter::parse_string_list()
        return
    
