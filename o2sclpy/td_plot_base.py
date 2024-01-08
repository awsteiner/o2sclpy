#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023-2024, Andrew W. Steiner
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
import numpy
import os

from o2sclpy.doc_data import cmaps, new_cmaps, extra_types
from o2sclpy.doc_data import acol_help_topics, version
from o2sclpy.doc_data import o2graph_help_topics, acol_types
from o2sclpy.utils import parse_arguments, string_to_dict, terminal_py
from o2sclpy.utils import force_bytes, default_plot, cross
from o2sclpy.utils import is_number, arrow, icosphere
from o2sclpy.utils import length_without_colors, wrap_line, screenify_py
from o2sclpy.utils import string_equal_dash, latex_to_png
from o2sclpy.utils import force_string, remove_spaces
from o2sclpy.plot_base import plot_base
from o2sclpy.yt_plot_base import yt_plot_base
from o2sclpy.doc_data import version
from o2sclpy.hdf import *
from o2sclpy.base import *
from o2sclpy.kde import *

class td_plot_base(yt_plot_base):
    """
    A class for managing plots of three-dimensional data
    """

    def __init__(self):
        super().__init__()
        self.to=threed_objects()
        self.td_wdir='.'
        return

    def td_den_plot(self,o2scl,amp,args,cmap='',mat_name='white'):
        """
        Desc
        """
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        slice_name=''
        slice=args[0]

        if curr_type==b'table3d':
            slice_name=args[0]
            if len(args)>=2:
                kwstring=args[1]
        else:
            print("Command 'td-den-plot' not supported for type",
                  curr_type,".")
            return

        table3d=amt.get_table3d_obj()
        nxt=table3d.get_nx()
        nyt=table3d.get_ny()
        sl=table3d.get_slice(slice).to_numpy()
        xgrid=[table3d.get_grid_x(i) for i in range(0,nxt)]
        ygrid=[table3d.get_grid_y(i) for i in range(0,nyt)]
        
        if self.xset==False:
            self.xlo=numpy.min(xgrid)
            self.xhi=numpy.max(xgrid)
            if self.verbose>2:
                print('td_den_plot(): x limits not set, so setting to'+
                      str(self.xlo)+' and '+str(self.xhi)+'.')
        if self.yset==False:
            self.ylo=numpy.min(ygrid)
            self.yhi=numpy.max(ygrid)
            if self.verbose>2:
                print('td_den_plot(): y limits not set, so setting to'+
                      str(self.ylo)+' and '+str(self.yhi)+'.')
        if self.zset==False:
            self.zlo=numpy.min(sl)
            self.zhi=numpy.max(sl)
            if self.verbose>2:
                print('td_den_plot(): z limits not set, so setting to'+
                      str(self.zlo)+' and '+str(self.zhi))
        
        # If true, then a color map has been specified and we need
        # to add materials
        colors=False
        
        # The list of 256 materials defined by the color map
        # (not all will be needed for the 3d object
        cmap_mats=[]
        
        if cmap!='':
            
            import matplotlib.cm as cm
            from matplotlib.colors import Normalize
            import matplotlib.pyplot as plot
            
            color_map=cm.get_cmap(cmap)
            norm=plot.Normalize(0,255)
            
            for i in range(0,256):
                rgb=color_map(norm(float(i)))[:3]
                cmap_mats.append(material('cmap_'+str(i),[rgb[0],rgb[1],
                                                       rgb[2]]))
                
            colors=True
            if self.verbose>2:
                print('td_den_plot(): Using colors from cmap',cmap)
            
        # Vertices for the density plot
        den_vert=[]
        # Faces for the density plot
        den_face=[]
        # Materials for the density plot
        den_ml=[]
        
        # Vertex index for faces
        k=0
        for i in range(0,nxt):
            for j in range(0,nyt):
                arr=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                     (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                     (sl[i,j]-self.zlo)/(self.zhi-self.zlo)]
                den_vert.append(arr)
                if i<nxt-1 and j<nyt-1:
                    if colors==True:
                        # Construct the colormap index
                        cmap_ix=int(arr[2]*256)
                        if cmap_ix>255:
                            cmap_ix=255
                        cmap_name='cmap_'+str(cmap_ix)
                        # See if the corresponding material is already
                        # in the list named 'den_ml'
                        mat_found=False
                        for ell in range(0,len(den_ml)):
                            if den_ml[ell].name==cmap_name:
                                mat_found=True
                        # If it was not found, find it in the list
                        # named 'cmap_mats'
                        if mat_found==False:
                            for ell in range(0,len(cmap_mats)):
                                if cmap_mats[ell].name==cmap_name:
                                    #print('Adding material',cmap_name)
                                    den_ml.append(cmap_mats[ell])
                                    ell=len(cmap_mats)
                         # Add the two triangles 
                        arr2=[k+1,k+nyt+1,k+2,cmap_name]
                        den_face.append(arr2)
                        arr3=[k+1+nyt,k+2,k+2+nyt,cmap_name]
                        den_face.append(arr3)
                        
                    else:
                        
                        arr2=[k,k+nyt,k+1]
                        den_face.append(arr2)
                        arr3=[k+nyt,k+1+nyt,k+1]
                        den_face.append(arr3)
                        
                k=k+1

        #for k in range(0,41):
        #print(k,den_vert[k])
                
        # Convert to GLTF
                
        vert2=[]
        norms2=[]
        
        for i in range(0,len(den_face)):

            #print('old faces:',den_face[i])
            
            # Add the vertices to the new vertex array
            vert2.append(den_vert[den_face[i][0]-1])
            vert2.append(den_vert[den_face[i][1]-1])
            vert2.append(den_vert[den_face[i][2]-1])
    
            # Compute the norm
            p1=den_vert[den_face[i][0]-1]
            p2=den_vert[den_face[i][1]-1]
            p3=den_vert[den_face[i][2]-1]
            v1=[1]*3
            v2=[1]*3
            for j in range(0,3):
                v1[j]=p2[j]-p1[j]
                v2[j]=p3[j]-p2[j]
            norm=cross(v1,v2,norm=True)
            for k in range(0,3):
                norms2.append([norm[0],norm[1],norm[2]])
    
            den_face[i]=[i*3,i*3+1,i*3+2,den_face[i][3]]

            #print('new faces:',den_face[i])
            #print('face:',den_face[i])
            #print('verts:',vert2[den_face[i][0]],
            #      vert2[den_face[i][1]],vert2[den_face[i][2]])
            #temp=input('Press a key to continue. ')

        if self.verbose>2:
            print('td_den_plot(): adding',len(den_face),'faces.')
        if colors==True:
            gf=mesh_object('plot',den_face)
            gf.vert_list=vert2
            gf.vn_list=norms2
            self.to.add_object_mat_list(gf,den_ml)
            #for i in range(0,len(self.to.mat_list)):
                #print('to.mat_list',i,self.to.mat_list[i].name)
        else:
            
            if self.to.is_mat(mat_name)==False:
                
                if mat_name=='white':
                    white=material(mat_name,[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('Material '+mat_name+' not found in td-den-plot.')
                    return
            
            gf=mesh_object('plot',den_face)
            gf.vert_list=vert2
            gf.vn_list=norms2
            self.to.add_object_mat(gf,white)

        return
        
    def td_scatter(self,o2scl,amp,args,n_subdiv=0,r=0.04):
        """
        Desc
        """
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        colors=False
        if curr_type==b'table':
            col_x=args[0]
            col_y=args[1]
            col_z=args[2]
            col_r=''
            col_g=''
            col_b=''
            if len(args)>4:
                col_r=args[3]
                col_g=args[4]
                col_b=args[5]
                colors=True
        else:
            print("Command 'td-scatter' not supported for type",
                  curr_type,".")
            return
        
        table=amt.get_table_obj()
        n=table.get_nlines()
        cx=table[col_x][0:n]
        cy=table[col_y][0:n]
        cz=table[col_z][0:n]
        
        if self.xset==False:
            self.xlo=numpy.min(cx)
            self.xhi=numpy.max(cx)
            if self.xlo==self.xhi:
                self.xhi=self.xhi+1
            if self.verbose>2:
                print('td_scatter(): x limits not set, so setting to',
                      self.xlo,',',self.xhi)
        if self.yset==False:
            self.ylo=numpy.min(cy)
            self.yhi=numpy.max(cy)
            if self.ylo==self.yhi:
                self.yhi=self.yhi+1
            if self.verbose>2:
                print('td_scatter(): y limits not set, so setting to',
                      self.ylo,',',self.yhi)
        if self.zset==False:
            self.zlo=numpy.min(cz)
            self.zhi=numpy.max(cz)
            if self.zlo==self.zhi:
                self.zhi=self.zhi+1
            if self.verbose>2:
                print('td_scatter(): z limits not set, so setting to',
                      self.zlo,',',self.zhi)

        if colors==True:
            cr=table[col_r][0:n]
            cg=table[col_g][0:n]
            cb=table[col_b][0:n]
            rlo=numpy.min(cr)
            rhi=numpy.max(cr)
            glo=numpy.min(cg)
            ghi=numpy.max(cg)
            blo=numpy.min(cb)
            bhi=numpy.max(cb)

        # If true, then a color map has been specified and we need
        # to add materials
        colors=False
        if col_r!='' and col_g!='' and col_b!='':
            cr=table[col_r]
            cg=table[col_g]
            cb=table[col_b]
            colors=True

        if colors==False:

            gf=mesh_object('scatter',[])
            
            for i in range(0,n):
                xnew=(cx[i]-self.xlo)/(self.xhi-self.xlo)
                ynew=(cy[i]-self.ylo)/(self.yhi-self.ylo)
                znew=(cz[i]-self.zlo)/(self.zhi-self.zlo)
                vtmp,ntmp,ftmp=icosphere(xnew,ynew,znew,r,n_subdiv=n_subdiv)
                lv=len(gf.vert_list)
                for k in range(0,len(vtmp)):
                    gf.vert_list.append(vtmp[k])
                for k in range(0,len(ntmp)):
                    gf.vn_list.append(ntmp[k])
                for k in range(0,len(ftmp)):
                    ftmp[k][0]=ftmp[k][0]+lv
                    ftmp[k][1]=ftmp[k][1]+lv
                    ftmp[k][2]=ftmp[k][2]+lv
                    gf.faces.append(ftmp[k])
                    
        else:

            gf=mesh_object('scatter',[])
            
            for i in range(0,n):
                
                xnew=(cx[i]-self.xlo)/(self.xhi-self.xlo)
                ynew=(cy[i]-self.ylo)/(self.yhi-self.ylo)
                znew=(cz[i]-self.zlo)/(self.zhi-self.zlo)
                vtmp,ntmp,ftmp=icosphere(xnew,ynew,znew,r,n_subdiv=n_subdiv)
                lv=len(gf.vert_list)
                for k in range(0,len(vtmp)):
                    gf.vert_list.append(vtmp[k])
                for k in range(0,len(ntmp)):
                    gf.vn_list.append(ntmp[k])
                for k in range(0,len(ftmp)):
                    gf.faces.append([ftmp[k][0]+lv,ftmp[k][1]+lv,
                                     ftmp[k][2]+lv,'mat_point_'+str(i)])
                
                mat=material('mat_point_'+str(i),[(cr[i]-rlo)/(rhi-rlo),
                                                  (cg[i]-glo)/(ghi-glo),
                                                  (cb[i]-blo)/(bhi-blo)])
                self.to.add_mat(mat)
            
        # Convert to GLTF
                
        vert2=[]
        norms2=[]
        
        for i in range(0,len(gf.faces)):

            # Add the vertices to the new vertex array
            vert2.append(gf.vert_list[gf.faces[i][0]])
            vert2.append(gf.vert_list[gf.faces[i][1]])
            vert2.append(gf.vert_list[gf.faces[i][2]])
    
            # Add the normals to the new normal array
            norms2.append(gf.vn_list[gf.faces[i][0]])
            norms2.append(gf.vn_list[gf.faces[i][1]])
            norms2.append(gf.vn_list[gf.faces[i][2]])

        if False:
            print('td_scatter:')
            for ki in range(0,len(gf.faces)):
                print('%d [%d,%d,%d]' % (ki,gf.faces[ki][0],
                                         gf.faces[ki][1],
                                         gf.faces[ki][2]))
                print(('0 [%7.6e,%7.6e,%7.6e] '+
                       '[%7.6e,%7.6e,%7.6e]') %
                      (vert2[gf.faces[ki][0]][0],vert2[gf.faces[ki][0]][1],
                       vert2[gf.faces[ki][0]][2],norms2[gf.faces[ki][0]][0],
                       norms2[gf.faces[ki][0]][1],norms2[gf.faces[ki][0]][2]))
                print(('1 [%7.6e,%7.6e,%7.6e] '+
                       '[%7.6e,%7.6e,%7.6e]') %
                      (vert2[gf.faces[ki][1]][0],vert2[gf.faces[ki][1]][1],
                       vert2[gf.faces[ki][1]][2],norms2[gf.faces[ki][1]][0],
                       norms2[gf.faces[ki][1]][1],norms2[gf.faces[ki][1]][2]))
                print(('2 [%7.6e,%7.6e,%7.6e] '+
                       '[%7.6e,%7.6e,%7.6e]') %
                      (vert2[gf.faces[ki][2]][0],vert2[gf.faces[ki][2]][1],
                       vert2[gf.faces[ki][2]][2],norms2[gf.faces[ki][2]][0],
                       norms2[gf.faces[ki][2]][1],norms2[gf.faces[ki][2]][2]))
                print('')
    
            print(len(vert2),len(norms2),len(gf.faces))
            quit()
        
        if self.to.is_mat('white')==False:
            white=material('white',[1,1,1])
            self.to.add_mat(white)
            
        gf.vert_list=vert2
        gf.vn_list=norms2
        if colors==False:
            gf.mat='white'
        self.to.add_object(gf)

        return
        
    def td_arrow(self,x1,y1,z1,x2,y2,z2,name,
                 mat='white'):
        """Documentation for o2graph command ``td-arrow``:

        Plot an axis in a 3d visualization

        Command-line arguments: ``x1 y1 z1 x2 y2 z2 group_name [kwargs]``
        """
        arr_vert,arr_norm,arr_face=arrow(x1,y1,z1,x2,y2,z2)

        if type(mat)==str:
            if not self.to.is_mat(mat):
                if mat=='white':
                    white=material('white',[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('No material named',mat,'in td-arrow')
                    return
            if self.verbose>2:
                print('td_arrow(): creating group named',name,'with material',
                      mat+'.')
            gf=mesh_object(name,arr_face,mat)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)
                               
        else:
            if self.verbose>2:
                print('td_arrow(): creating group named',name,'with material',
                      mat.name+'.')
            if not self.to.is_mat(mat.name):
                self.to.add_mat(mat)
            gf=mesh_object(name,arr_face,mat.name)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)

        return

    def td_axis_label(self, ldir : str, tex_label : str,
                      mat_name : str = '', png_file : str = '',
                      group_name : str = '', offset : float = 0.1,
                      height : float = 0.1):
        """Create an axis label in the direction ``ldir`` with label
        ``tex_label``.
        """

        white_found=False
        for i in range(0,len(self.to.mat_list)):
            if self.to.mat_list[i].name=='white':
                white_found=True
        if white_found==False:
            white=material('white',[1,1,1])
            self.to.add_mat(white)
        
        if ldir=='x':
            
            if png_file=='':
                png_file='xtitle.png'
            if mat_name=='':
                mat_name='mat_xtitle'
            if group_name=='':
                group_name='x_title'

            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)

            x_v,x_f,x_t,x_n,x_m=latex_prism(0.5,-offset-height/2.0,
                                            -offset+height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset-height/2.0,
                                            tex_label,
                                            self.td_wdir,png_file,mat_name,
                                            dir=ldir)

            self.to.add_mat(x_m)
            gf=mesh_object(group_name,x_f)
            gf.vert_list=x_v
            gf.vn_list=x_n
            gf.vt_list=x_t
            self.to.add_object(gf)

        elif ldir=='y':
            
            if png_file=='':
                png_file='ytitle.png'
            if mat_name=='':
                mat_name='mat_ytitle'
            if group_name=='':
                group_name='y_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)
                
            y_v,y_f,y_t,y_n,y_m=latex_prism(-offset-height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset-height/2.0,
                                            tex_label,
                                            self.td_wdir,png_file,mat_name,
                                            dir=ldir)
            
            self.to.add_mat(y_m)
            gf=mesh_object(group_name,y_f)
            gf.vert_list=y_v
            gf.vn_list=y_n
            gf.vt_list=y_t
            self.to.add_object(gf)

        elif ldir=='z':
            
            if png_file=='':
                png_file='ztitle.png'
            if mat_name=='':
                mat_name='mat_ztitle'
            if group_name=='':
                group_name='z_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)
                
            z_v,z_f,z_t,z_n,z_m=latex_prism(-offset-height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset+height/2.0,
                                            -offset-height/2.0,0.5,
                                            tex_label,
                                            self.td_wdir,png_file,mat_name,
                                            dir=ldir)
            
            self.to.add_mat(z_m)
            gf=mesh_object(group_name,z_f)
            gf.vert_list=z_v
            gf.vn_list=z_n
            gf.vt_list=z_t
            self.to.add_object(gf)

        else:
            if type(ldir)==str:
                raise ValueError('Direction '+ldir+' is not one of "x", "y",'+
                                 ' or "z" in function td_axis_label().')
            else:
                raise ValueError('Direction is not one of "x", "y",'+
                                 ' or "z" in function td_axis_label().')
            
        return
    
class td_plot_base(yt_plot_base):
    """
    A class for managing plots of three-dimensional data
    """

    def __init__(self):
        super().__init__()
        self.to=threed_objects()
        self.td_wdir='.'
        return

    def td_den_plot(self,o2scl,amp,args,cmap='',mat_name='white'):
        """
        Desc
        """
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        slice_name=''
        slice=args[0]

        if curr_type==b'table3d':
            slice_name=args[0]
            if len(args)>=2:
                kwstring=args[1]
        else:
            print("Command 'td-den-plot' not supported for type",
                  curr_type,".")
            return

        table3d=amt.get_table3d_obj()
        nxt=table3d.get_nx()
        nyt=table3d.get_ny()
        sl=table3d.get_slice(slice).to_numpy()
        xgrid=[table3d.get_grid_x(i) for i in range(0,nxt)]
        ygrid=[table3d.get_grid_y(i) for i in range(0,nyt)]
        
        if self.xset==False:
            self.xlo=numpy.min(xgrid)
            self.xhi=numpy.max(xgrid)
            if self.verbose>2:
                print('td_den_plot(): x limits not set, so setting to'+
                      str(self.xlo)+' and '+str(self.xhi)+'.')
        if self.yset==False:
            self.ylo=numpy.min(ygrid)
            self.yhi=numpy.max(ygrid)
            if self.verbose>2:
                print('td_den_plot(): y limits not set, so setting to'+
                      str(self.ylo)+' and '+str(self.yhi)+'.')
        if self.zset==False:
            self.zlo=numpy.min(sl)
            self.zhi=numpy.max(sl)
            if self.verbose>2:
                print('td_den_plot(): z limits not set, so setting to'+
                      str(self.zlo)+' and '+str(self.zhi))
        
        # If true, then a color map has been specified and we need
        # to add materials
        colors=False
        
        # The list of 256 materials defined by the color map
        # (not all will be needed for the 3d object
        cmap_mats=[]
        
        if cmap!='':
            
            import matplotlib.cm as cm
            from matplotlib.colors import Normalize
            import matplotlib.pyplot as plot
            
            color_map=cm.get_cmap(cmap)
            norm=plot.Normalize(0,255)
            
            for i in range(0,256):
                rgb=color_map(norm(float(i)))[:3]
                cmap_mats.append(material('cmap_'+str(i),[rgb[0],rgb[1],
                                                       rgb[2]]))
                
            colors=True
            if self.verbose>2:
                print('td_den_plot(): Using colors from cmap',cmap)
            
        # Vertices for the density plot
        den_vert=[]
        # Faces for the density plot
        den_face=[]
        # Materials for the density plot
        den_ml=[]
        
        # Vertex index for faces
        k=0
        for i in range(0,nxt):
            for j in range(0,nyt):
                arr=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                     (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                     (sl[i,j]-self.zlo)/(self.zhi-self.zlo)]
                den_vert.append(arr)
                if i<nxt-1 and j<nyt-1:
                    if colors==True:
                        # Construct the colormap index
                        cmap_ix=int(arr[2]*256)
                        if cmap_ix>255:
                            cmap_ix=255
                        cmap_name='cmap_'+str(cmap_ix)
                        # See if the corresponding material is already
                        # in the list named 'den_ml'
                        mat_found=False
                        for ell in range(0,len(den_ml)):
                            if den_ml[ell].name==cmap_name:
                                mat_found=True
                        # If it was not found, find it in the list
                        # named 'cmap_mats'
                        if mat_found==False:
                            for ell in range(0,len(cmap_mats)):
                                if cmap_mats[ell].name==cmap_name:
                                    #print('Adding material',cmap_name)
                                    den_ml.append(cmap_mats[ell])
                                    ell=len(cmap_mats)
                         # Add the two triangles 
                        arr2=[k+1,k+nyt+1,k+2,cmap_name]
                        den_face.append(arr2)
                        arr3=[k+1+nyt,k+2,k+2+nyt,cmap_name]
                        den_face.append(arr3)
                        
                    else:
                        
                        arr2=[k,k+nyt,k+1]
                        den_face.append(arr2)
                        arr3=[k+nyt,k+1+nyt,k+1]
                        den_face.append(arr3)
                        
                k=k+1

        #for k in range(0,41):
        #print(k,den_vert[k])
                
        # Convert to GLTF
                
        vert2=[]
        norms2=[]
        
        for i in range(0,len(den_face)):

            #print('old faces:',den_face[i])
            
            # Add the vertices to the new vertex array
            vert2.append(den_vert[den_face[i][0]-1])
            vert2.append(den_vert[den_face[i][1]-1])
            vert2.append(den_vert[den_face[i][2]-1])
    
            # Compute the norm
            p1=den_vert[den_face[i][0]-1]
            p2=den_vert[den_face[i][1]-1]
            p3=den_vert[den_face[i][2]-1]
            v1=[1]*3
            v2=[1]*3
            for j in range(0,3):
                v1[j]=p2[j]-p1[j]
                v2[j]=p3[j]-p2[j]
            norm=cross(v1,v2,norm=True)
            for k in range(0,3):
                norms2.append([norm[0],norm[1],norm[2]])
    
            den_face[i]=[i*3,i*3+1,i*3+2,den_face[i][3]]

            #print('new faces:',den_face[i])
            #print('face:',den_face[i])
            #print('verts:',vert2[den_face[i][0]],
            #      vert2[den_face[i][1]],vert2[den_face[i][2]])
            #temp=input('Press a key to continue. ')

        if self.verbose>2:
            print('td_den_plot(): adding',len(den_face),'faces.')
        if colors==True:
            gf=mesh_object('plot',den_face)
            gf.vert_list=vert2
            gf.vn_list=norms2
            self.to.add_object_mat_list(gf,den_ml)
            #for i in range(0,len(self.to.mat_list)):
                #print('to.mat_list',i,self.to.mat_list[i].name)
        else:
            
            if self.to.is_mat(mat_name)==False:
                
                if mat_name=='white':
                    white=material(mat_name,[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('Material '+mat_name+' not found in td-den-plot.')
                    return
            
            gf=mesh_object('plot',den_face)
            gf.vert_list=vert2
            gf.vn_list=norms2
            self.to.add_object_mat(gf,white)

        return
        
    def td_scatter(self,o2scl,amp,args,n_subdiv=0,r=0.04):
        """
        Desc
        """
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        colors=False
        if curr_type==b'table':
            col_x=args[0]
            col_y=args[1]
            col_z=args[2]
            col_r=''
            col_g=''
            col_b=''
            if len(args)>4:
                col_r=args[3]
                col_g=args[4]
                col_b=args[5]
                colors=True
        else:
            print("Command 'td-scatter' not supported for type",
                  curr_type,".")
            return
        
        table=amt.get_table_obj()
        n=table.get_nlines()
        cx=table[col_x][0:n]
        cy=table[col_y][0:n]
        cz=table[col_z][0:n]
        
        if self.xset==False:
            self.xlo=numpy.min(cx)
            self.xhi=numpy.max(cx)
            if self.xlo==self.xhi:
                self.xhi=self.xhi+1
            if self.verbose>2:
                print('td_scatter(): x limits not set, so setting to',
                      self.xlo,',',self.xhi)
        if self.yset==False:
            self.ylo=numpy.min(cy)
            self.yhi=numpy.max(cy)
            if self.ylo==self.yhi:
                self.yhi=self.yhi+1
            if self.verbose>2:
                print('td_scatter(): y limits not set, so setting to',
                      self.ylo,',',self.yhi)
        if self.zset==False:
            self.zlo=numpy.min(cz)
            self.zhi=numpy.max(cz)
            if self.zlo==self.zhi:
                self.zhi=self.zhi+1
            if self.verbose>2:
                print('td_scatter(): z limits not set, so setting to',
                      self.zlo,',',self.zhi)

        if colors==True:
            cr=table[col_r][0:n]
            cg=table[col_g][0:n]
            cb=table[col_b][0:n]
            rlo=numpy.min(cr)
            rhi=numpy.max(cr)
            glo=numpy.min(cg)
            ghi=numpy.max(cg)
            blo=numpy.min(cb)
            bhi=numpy.max(cb)

        # If true, then a color map has been specified and we need
        # to add materials
        colors=False
        if col_r!='' and col_g!='' and col_b!='':
            cr=table[col_r]
            cg=table[col_g]
            cb=table[col_b]
            colors=True

        if colors==False:

            gf=mesh_object('scatter',[])
            
            for i in range(0,n):
                xnew=(cx[i]-self.xlo)/(self.xhi-self.xlo)
                ynew=(cy[i]-self.ylo)/(self.yhi-self.ylo)
                znew=(cz[i]-self.zlo)/(self.zhi-self.zlo)
                vtmp,ntmp,ftmp=icosphere(xnew,ynew,znew,r,n_subdiv=n_subdiv)
                lv=len(gf.vert_list)
                for k in range(0,len(vtmp)):
                    gf.vert_list.append(vtmp[k])
                for k in range(0,len(ntmp)):
                    gf.vn_list.append(ntmp[k])
                for k in range(0,len(ftmp)):
                    ftmp[k][0]=ftmp[k][0]+lv
                    ftmp[k][1]=ftmp[k][1]+lv
                    ftmp[k][2]=ftmp[k][2]+lv
                    gf.faces.append(ftmp[k])
                    
        else:

            gf=mesh_object('scatter',[])
            
            for i in range(0,n):
                
                xnew=(cx[i]-self.xlo)/(self.xhi-self.xlo)
                ynew=(cy[i]-self.ylo)/(self.yhi-self.ylo)
                znew=(cz[i]-self.zlo)/(self.zhi-self.zlo)
                vtmp,ntmp,ftmp=icosphere(xnew,ynew,znew,r,n_subdiv=n_subdiv)
                lv=len(gf.vert_list)
                for k in range(0,len(vtmp)):
                    gf.vert_list.append(vtmp[k])
                for k in range(0,len(ntmp)):
                    gf.vn_list.append(ntmp[k])
                for k in range(0,len(ftmp)):
                    gf.faces.append([ftmp[k][0]+lv,ftmp[k][1]+lv,
                                     ftmp[k][2]+lv,'mat_point_'+str(i)])
                
                mat=material('mat_point_'+str(i),[(cr[i]-rlo)/(rhi-rlo),
                                                  (cg[i]-glo)/(ghi-glo),
                                                  (cb[i]-blo)/(bhi-blo)])
                self.to.add_mat(mat)
            
        # Convert to GLTF
                
        vert2=[]
        norms2=[]
        
        for i in range(0,len(gf.faces)):

            # Add the vertices to the new vertex array
            vert2.append(gf.vert_list[gf.faces[i][0]])
            vert2.append(gf.vert_list[gf.faces[i][1]])
            vert2.append(gf.vert_list[gf.faces[i][2]])
    
            # Add the normals to the new normal array
            norms2.append(gf.vn_list[gf.faces[i][0]])
            norms2.append(gf.vn_list[gf.faces[i][1]])
            norms2.append(gf.vn_list[gf.faces[i][2]])

        if False:
            print('td_scatter:')
            for ki in range(0,len(gf.faces)):
                print('%d [%d,%d,%d]' % (ki,gf.faces[ki][0],
                                         gf.faces[ki][1],
                                         gf.faces[ki][2]))
                print(('0 [%7.6e,%7.6e,%7.6e] '+
                       '[%7.6e,%7.6e,%7.6e]') %
                      (vert2[gf.faces[ki][0]][0],vert2[gf.faces[ki][0]][1],
                       vert2[gf.faces[ki][0]][2],norms2[gf.faces[ki][0]][0],
                       norms2[gf.faces[ki][0]][1],norms2[gf.faces[ki][0]][2]))
                print(('1 [%7.6e,%7.6e,%7.6e] '+
                       '[%7.6e,%7.6e,%7.6e]') %
                      (vert2[gf.faces[ki][1]][0],vert2[gf.faces[ki][1]][1],
                       vert2[gf.faces[ki][1]][2],norms2[gf.faces[ki][1]][0],
                       norms2[gf.faces[ki][1]][1],norms2[gf.faces[ki][1]][2]))
                print(('2 [%7.6e,%7.6e,%7.6e] '+
                       '[%7.6e,%7.6e,%7.6e]') %
                      (vert2[gf.faces[ki][2]][0],vert2[gf.faces[ki][2]][1],
                       vert2[gf.faces[ki][2]][2],norms2[gf.faces[ki][2]][0],
                       norms2[gf.faces[ki][2]][1],norms2[gf.faces[ki][2]][2]))
                print('')
    
            print(len(vert2),len(norms2),len(gf.faces))
            quit()
        
        if self.to.is_mat('white')==False:
            white=material('white',[1,1,1])
            self.to.add_mat(white)
            
        gf.vert_list=vert2
        gf.vn_list=norms2
        if colors==False:
            gf.mat='white'
        self.to.add_object(gf)

        return
        
    def td_arrow(self,x1,y1,z1,x2,y2,z2,name,
                 mat='white'):
        """Documentation for o2graph command ``td-arrow``:

        Plot an axis in a 3d visualization

        Command-line arguments: ``x1 y1 z1 x2 y2 z2 group_name [kwargs]``
        """
        arr_vert,arr_norm,arr_face=arrow(x1,y1,z1,x2,y2,z2)

        if type(mat)==str:
            if not self.to.is_mat(mat):
                if mat=='white':
                    white=material('white',[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('No material named',mat,'in td-arrow')
                    return
            if self.verbose>2:
                print('td_arrow(): creating group named',name,'with material',
                      mat+'.')
            gf=mesh_object(name,arr_face,mat)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)
                               
        else:
            if self.verbose>2:
                print('td_arrow(): creating group named',name,'with material',
                      mat.name+'.')
            if not self.to.is_mat(mat.name):
                self.to.add_mat(mat)
            gf=mesh_object(name,arr_face,mat.name)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)

        return

    def td_axis_label(self, ldir : str, tex_label : str,
                      mat_name : str = '', png_file : str = '',
                      group_name : str = '', offset : float = 0.1,
                      height : float = 0.1):
        """Create an axis label in the direction ``ldir`` with label
        ``tex_label``.
        """

        white_found=False
        for i in range(0,len(self.to.mat_list)):
            if self.to.mat_list[i].name=='white':
                white_found=True
        if white_found==False:
            white=material('white',[1,1,1])
            self.to.add_mat(white)
        
        if ldir=='x':
            
            if png_file=='':
                png_file='xtitle.png'
            if mat_name=='':
                mat_name='mat_xtitle'
            if group_name=='':
                group_name='x_title'

            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)

            x_v,x_f,x_t,x_n,x_m=latex_prism(0.5,-offset-height/2.0,
                                            -offset+height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset-height/2.0,
                                            tex_label,
                                            self.td_wdir,png_file,mat_name,
                                            dir=ldir)

            self.to.add_mat(x_m)
            gf=mesh_object(group_name,x_f)
            gf.vert_list=x_v
            gf.vn_list=x_n
            gf.vt_list=x_t
            self.to.add_object(gf)

        elif ldir=='y':
            
            if png_file=='':
                png_file='ytitle.png'
            if mat_name=='':
                mat_name='mat_ytitle'
            if group_name=='':
                group_name='y_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)
                
            y_v,y_f,y_t,y_n,y_m=latex_prism(-offset-height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset-height/2.0,
                                            tex_label,
                                            self.td_wdir,png_file,mat_name,
                                            dir=ldir)
            
            self.to.add_mat(y_m)
            gf=mesh_object(group_name,y_f)
            gf.vert_list=y_v
            gf.vn_list=y_n
            gf.vt_list=y_t
            self.to.add_object(gf)

        elif ldir=='z':
            
            if png_file=='':
                png_file='ztitle.png'
            if mat_name=='':
                mat_name='mat_ztitle'
            if group_name=='':
                group_name='z_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)
                
            z_v,z_f,z_t,z_n,z_m=latex_prism(-offset-height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset+height/2.0,
                                            -offset-height/2.0,0.5,
                                            tex_label,
                                            self.td_wdir,png_file,mat_name,
                                            dir=ldir)
            
            self.to.add_mat(z_m)
            gf=mesh_object(group_name,z_f)
            gf.vert_list=z_v
            gf.vn_list=z_n
            gf.vt_list=z_t
            self.to.add_object(gf)

        else:
            if type(ldir)==str:
                raise ValueError('Direction '+ldir+' is not one of "x", "y",'+
                                 ' or "z" in function td_axis_label().')
            else:
                raise ValueError('Direction is not one of "x", "y",'+
                                 ' or "z" in function td_axis_label().')
            
        return
    
