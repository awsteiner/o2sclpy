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
#  MERCHANTABILITY or FITNESS FORA PARTICULAR PURPOSE.  See the
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
from o2sclpy.utils import is_number, arrow, icosphere, png_power_two
from o2sclpy.utils import length_without_colors, wrap_line, screenify_py
from o2sclpy.utils import string_equal_dash, latex_to_png
from o2sclpy.utils import force_string, remove_spaces, dist3
from o2sclpy.plot_base import plot_base
from o2sclpy.yt_plot_base import yt_plot_base
from o2sclpy.doc_data import version
from o2sclpy.hdf import *
from o2sclpy.base import *
from o2sclpy.kde import *

def o2scl_get_type(o2scl,amp,link):
    """
    Get the type of the current object stored in the acol_manager
    pointer and return as a bytes object.
    """

    amt=acol_manager(link,amp)
    return amt.get_type()

class material:
    """A simple GLTF-like material class
    
    Note that: the baseColorTexture is supposed to be stored in the
    sRGB colorspace and subject to hardware sRGB decoding, but the
    baseColorFactor has no hardware decoder and therefore is specified
    as linear values directly.
    """
    
    name: str
    """
    The name of the material
    """
    
    # The GLTF properties
    
    base_color=[1.0,1.0,1.0]
    """
    The base color factor (either 3 or 4 floating point numbers)

    These quantities are stored in ``pbrMetallicRoughness:baseColorFactor``.
    """
    metal: float = 0.0
    """
    The metalness

    This quantity is stored in ``pbrMetallicRoughness:metallicFactor``.
    """
    rough: float = 1.0
    """
    The roughness (should default be 0 or 1?)

    This quantity is stored in ``pbrMetallicRoughness:roughnessFactor``.
    """
    ds: bool = True
    """
    If true, the material is double-sided (default True)
    """
    txt: str = ''
    """
    The texture filename, including extension
    """
    alpha_mode: str = 'opaque'
    """
    The alpha mode, either 'opaque', 'mask', or 'blend'.
    """
    alpha_cutoff: float = 0.5
    """
    The alpha cutoff, default is 0.5.
    """
    emi_factor=[0.0,0.0,0.0]
    """
    The emissive factor
    """

    # These properties aren't explicitly used in the GLTF,
    # but are useful when mapping textures to the mesh
    
    txt_frac_w: float = 1.0
    """ 
    The fractional part of the texture width which is usable
    """
    txt_frac_h: float = 1.0
    """ 
    The fractional part of the texture height which is usable
    """
    txt_w: int = 0
    """
    The width of the texture, in pixels (always a power of two)
    """
    txt_h: int = 0
    """
    The height of the texture, in pixels (always a power of two)
    """

    def __init__(self, name: str, base_color=[1,1,1], txt: str='',
                 metal: float = 0.0, rough: float=1.0, ds: bool=True,
                 alpha_mode : str = 'opaque', alpha_cutoff: float = 0.5,
                 emi_factor=[0.0,0.0,0.0], txt_w=0, txt_h=0):
        """Create a new material with name ``name``.

        The keyword arguments are as follows:
        - material color ("baseColorFactor") in ``base_color``,
        - texture file in ``txt``,
        - metalness in ``metal``,
        - roughness in ``rough``,
        - double-sided flag in ``ds``,
        - ``alpha_mode``, and
        - ``alpha_cutoff``.

        """
        self.name=name
        self.base_color=base_color
        self.txt=txt
        self.metal=metal
        self.rough=rough
        self.ds=ds
        self.alpha_mode=alpha_mode
        self.alpha_cutoff=alpha_cutoff
        self.emi_factor=emi_factor
        self.txt_frac_w=1.0
        self.txt_frac_h=1.0
        self.txt_w=txt_w
        self.txt_h=txt_h
        return

class mesh_object:
    """A mesh object for a GLTF file.
    """
    
    vert_list=[]
    """
    List of vertices
    """
    vn_list=[]
    """
    List of vertex normals
    """
    vt_list=[]
    """
    List of texture coordinates
    """
    faces=[]
    """
    The list of faces
    """
    name: str = ''
    """
    The name of the mesh object
    """
    
    mat: str = ''
    """The name of the material (blank for none, or for different material
    for each face)

    Note that this string might be nonempty even when some of the
    faces explicitly specify a material. In this case, this string
    specifies the default material to be used for those faces which do
    not specify their own material.

    If this string is non-empty, but all of the faces specify a 
    material, then the ``sort_by_mat()`` function will
    """
    obj_type: str = 'triangles'
    """
    Either 'triangles', 'lines', or 'points'
    """

    def __init__(self, name: str, faces,
                 mat: str = '', obj_type: str = 'triangles'):
        """
        Create a group given the specfied list of faces, name, and 
        material.
        """
        self.name=name
        self.faces=faces
        self.obj_type=obj_type
        self.mat=mat
        # AWS, 1/18/24, I have found that these need to be initialized
        # to empty even though they are specified above.
        self.vert_list=[]
        self.vn_list=[]
        self.vt_list=[]
        return

    def sort_by_mat(self, verbose : int = 0):
        """Sort the faces by material name, ensuring that the group and
        material commands do not have to be issued for each face.
        """

        # If no materials are specified in faces, there is nothing to do
        found_four=False
        for i in range(0,len(self.faces)):
            if len(self.faces[i])==4 or len(self.faces[i])==7:
                found_four=True
        if verbose>0:
            print('mesh_object::sort_by_mat(): found_four',found_four)
        if found_four==False:
            return

        # Find if there at least two distinct materials 
        two_mats=False
        for i in range(0,len(self.faces)):
            if (len(self.faces[i])==4 and
                self.faces[i][3]!=self.mat):
                two_mats=True
            if (i>0 and len(self.faces[i])==4 and
                len(self.faces[i-1])==4 and
                self.faces[i][3]!=self.faces[i-1][3]):
                two_mats=True

        # If there are not two distinct materials, there's nothing to do
        if verbose>0:
            print('mesh_object::sort_by_mat(): two_mats',two_mats)
        if two_mats==False:
            return

        # Reorganize faces by material name
        mat_list=[]
        faces2=[]

        # First, if a global material is specified, add all faces
        # which don't have a material and assume that they'll use the
        # global material.
        if self.mat!='':

            # This is true if self.mat has been added to 'mat_list'
            base_name_added=False
            for i in range(0,len(self.faces)):
                if len(self.faces[i])==3:
                    if base_name_added==False:
                        mat_list.append(self.mat)
                        base_name_added=True
                    faces2.append(self.faces[i])
                    
            if base_name_added==False:
                raise ValueError('In function sort_by_mat(): '+
                                 '  A material named '+self.mat+
                                 ' was specified in "mat", but no face '+
                                 'uses that material.')

        # Now go through the list and find faces not already added to
        # mat_list
        face_copies=[False for i in range(0,len(self.faces))]
        for i in range(0,len(self.faces)):
            if len(self.faces[i])==4:
                mat_name=self.faces[i][3]
                if mat_name not in mat_list:
                    if verbose>0:
                        print('mesh_object::sort_by_mat():',
                              'At index',i,'adding faces for',mat_name)
                    mat_list.append(mat_name)
                    # If it's not found, then add the current face,
                    # and loop over the remaining faces which match
                    faces2.append(self.faces[i])
                    face_copies[i]=True
                    for j in range(i+1,len(self.faces)):
                        if self.faces[j][3]==mat_name:
                            faces2.append(self.faces[j])
                            face_copies[j]=True

        if len(self.faces)!=len(faces2):
            if verbose>0:
                print('sort_by_mat():',len(self.faces),len(faces2))
            raise SyntaxError('The lists of faces do not match up in '+
                              'sort_by_mat().')
                 
        self.faces=faces2
        return

def latex_prism(x1,y1,z1,x2,y2,z2,latex,wdir,png_file,mat_name,
                dir='x',end_mat='white',verbose=0):
    """
    Create a rectangular prism with textures from a png created by a
    LaTeX string on four sides.

    This function returns four objects: the vertices, the faces,
    the texture uv coordinates, and the material object

    The variable dir is either 'x', 'y', or 'z', depending
    on the orientation of the prism. For the 'x' direction,
    the xy and xz faces have textures from the LaTeX object,
    and the yz faces are set to the end material specified
    in ``end_mat``. The normal vectors for all six faces point
    outside the prism. 
    """
    import tempfile
    
    f=tempfile.NamedTemporaryFile(suffix='.png',delete=False)
    temp_png_name=f.name

    latex_to_png(latex,temp_png_name,verbose=verbose)
    w,h,w_new,h_new=png_power_two(temp_png_name,wdir+'/'+png_file,
                                  verbose=verbose,
                                  bgcolor=[255,255,255,255],
                                  flatten=True)
                                 
    face=[]
    vert=[]
    facet=[]
    text_uv=[]

    if dir=='x':
        xcent=(x1+x2)/2.0
        height=abs(y2-y1)
        width=w_new/h_new*height
        x1=xcent-width/2.0
        x2=xcent+width/2.0
    elif dir=='y':
        ycent=(y1+y2)/2.0
        height=abs(z2-z1)
        width=w_new/h_new*height
        y1=ycent-width/2.0
        y2=ycent+width/2.0
    else:
        zcent=(z1+z2)/2.0
        height=abs(x2-x1)
        width=w_new/h_new*height
        z1=zcent-width/2.0
        z2=zcent+width/2.0

    m=material(mat_name,txt=png_file)
    #m.txt_frac_w=float(w)/float(w_new)
    #m.txt_frac_h=float(h)/float(h_new)
    m.txt_frac_w=1.0
    m.txt_frac_h=1.0
    m.txt_w=w_new
    m.txt_h=h_new

    # Add the 8 vertices
    vert.append([x1,y1,z1])
    vert.append([x2,y1,z1])
    vert.append([x1,y2,z1])
    vert.append([x2,y2,z1])
    vert.append([x1,y1,z2])
    vert.append([x2,y1,z2])
    vert.append([x1,y2,z2])
    vert.append([x2,y2,z2])
    
    text_uv.append([0.0,float(h)/float(h_new)])
    text_uv.append([0.0,0.0])
    text_uv.append([float(w)/float(w_new),float(h)/float(h_new)])
    text_uv.append([float(w)/float(w_new),0.0])

    if dir=='x':
        
        # The four sides with labels
        face.append([1,5,2,2,1,4,mat_name])
        face.append([2,5,6,4,1,3,mat_name])
        face.append([8,7,4,4,2,3,mat_name])
        face.append([4,7,3,3,2,1,mat_name])
        face.append([1,2,3,1,3,2,mat_name])
        face.append([3,2,4,2,3,4,mat_name])
        face.append([5,7,6,2,1,4,mat_name])
        face.append([6,7,8,4,1,3,mat_name])
        
        # The two sides without labels
        face.append([2,6,4,end_mat])
        face.append([4,6,8,end_mat])
        face.append([1,3,5,end_mat])
        face.append([5,3,7,end_mat])
        
    elif dir=='y':
        
        # The four sides with labels
        face.append([3,1,4,4,2,3,mat_name])
        face.append([4,1,2,3,2,1,mat_name])
        face.append([6,5,8,2,1,4,mat_name])
        face.append([8,5,7,4,1,3,mat_name])
        face.append([4,2,8,4,2,3,mat_name])
        face.append([8,2,6,3,2,1,mat_name])
        face.append([5,1,7,2,1,4,mat_name])
        face.append([7,1,3,4,1,3,mat_name])
        
        # The two sides without labels
        face.append([3,4,7,end_mat])
        face.append([7,4,8,end_mat])
        face.append([1,5,2,end_mat])
        face.append([2,5,6,end_mat])
        
    else:
        
        # The four sides with labels
        face.append([4,8,3,1,3,2,mat_name])
        face.append([3,8,7,2,3,4,mat_name])
        face.append([2,1,6,2,1,4,mat_name])
        face.append([6,1,5,4,1,3,mat_name])
        
        face.append([8,4,6,4,2,3,mat_name])
        face.append([6,4,2,3,2,1,mat_name])
        face.append([1,3,5,2,1,4,mat_name])
        face.append([5,3,7,4,1,3,mat_name])
        
        # The two sides without labels
        face.append([1,2,3,end_mat])
        face.append([3,2,4,end_mat])
        face.append([5,7,6,end_mat])
        face.append([6,7,8,end_mat])
        
    # Rearrange for GLTF. to compute normals, we use the cross
    # products.

    norms=[[1.0,0.0,0.0],
           [-1.0,0.0,0.0],
           [0.0,1.0,0.0],
           [0.0,-1.0,0.0],
           [0.0,0.0,1.0],
           [0.0,0.0,-1.0]]
        
    vert2=[]
    txts=[]
    norms2=[]
    
    for i in range(0,len(face)):

        # Add the vertices to the new vertex array
        vert2.append(vert[face[i][0]-1])
        vert2.append(vert[face[i][1]-1])
        vert2.append(vert[face[i][2]-1])

        # Compute the norm
        p1=vert[face[i][0]-1]
        p2=vert[face[i][1]-1]
        p3=vert[face[i][2]-1]
        v1=[1]*3
        v2=[1]*3
        for j in range(0,3):
            v1[j]=p2[j]-p1[j]
            v2[j]=p3[j]-p2[j]
        norm=cross(v1,v2,norm=True)
        for k in range(0,3):
            norms2.append([norm[0],norm[1],norm[2]])

        if len(face[i])>=7:
            # Texture coordinates in the case of a image
            txts.append([text_uv[face[i][3]-1][0],
                         text_uv[face[i][3]-1][1]])
            txts.append([text_uv[face[i][4]-1][0],
                         text_uv[face[i][4]-1][1]])
            txts.append([text_uv[face[i][5]-1][0],
                         text_uv[face[i][5]-1][1]])
            face[i]=[i*3,i*3+1,i*3+2,face[i][6]]
        else:
            # Default texture coordinates for no image
            txts.append([text_uv[3][0],
                         text_uv[3][1]])
            txts.append([text_uv[0][0],
                         text_uv[0][1]])
            txts.append([text_uv[1][0],
                         text_uv[1][1]])
            face[i]=[i*3,i*3+1,i*3+2,face[i][3]]

    # Print out results
    if False:
        for ki in range(0,len(vert2),3):
            print('%d [%d,%d,%d] mat: %s' % (int(ki/3),face[int(ki/3)][0],
                                             face[int(ki/3)][1],
                                             face[int(ki/3)][2],
                                             face[int(ki/3)][3]))
            print(('0 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki][0],vert2[ki][1],
                                             vert2[ki][2],txts[ki][0],
                                             txts[ki][1],norms2[ki][0],
                                             norms2[ki][1],norms2[ki][2]))
            print(('1 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+1][0],vert2[ki+1][1],
                                             vert2[ki+1][2],txts[ki+1][0],
                                             txts[ki+1][1],norms2[ki+1][0],
                                             norms2[ki+1][1],norms2[ki+1][2]))
            print(('2 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+2][0],vert2[ki+2][1],
                                             vert2[ki+2][2],txts[ki+2][0],
                                             txts[ki+2][1],norms2[ki+2][0],
                                             norms2[ki+2][1],norms2[ki+2][2]))
            print('')
            
        #quit()

    return vert2,face,txts,norms2,m
    
def parallelogram(x1,y1,z1,x2,y2,z2,x3,y3,z3,mat_name='',verbose=0,
                  force_rect=False):
    """Create the vertices, faces, and norms for a 3d visualization of a
    parallelogram.

    Points 1, 2, and 3 should be the lower-left corner, the
    lower-right corner, and the upper-left corner, respectively. These
    three points define the first triangular face, and the second
    triangular face is formed from the lower-right corner, the
    upper-left corner, and the upper-right corner (which is
    automatically computed from the user-specified points).

    If ``force_rect=True``, then the third coordinate of the 
    parallelogram is modified to make sure the two adjacent sides
    are orthogonal.
    """

    if force_rect:
        
        #print(x1,y1,z1,x2,y2,z2,x3,y3,z3)
        
        x21=x2-x1
        y21=y2-y1
        z21=z2-z1
        x31=x3-x1
        y31=y3-y1
        z31=z3-z1
        dot=x21*x31+y21*y31+z21*z31
        mag=dist3([x1,y1,z1],[x2,y2,z2])
        # The longitudinal component of 31 in the direction of 21
        longit=[x21*dot/mag/mag,y21*dot/mag/mag,z21*dot/mag/mag]
        # The transverse part of 31 orthogonal to 21
        transv=[x31-longit[0],y31-longit[1],z31-longit[2]]

        # Shift the third coordinate
        x3=x1+transv[0]
        y3=y1+transv[1]
        z3=z1+transv[2]
        
        #print(x1,y1,z1,x2,y2,z2,x3,y3,z3)

        # Check that the updated dot product is now zero
        x21=x2-x1
        y21=y2-y1
        z21=z2-z1
        x31=x3-x1
        y31=y3-y1
        z31=z3-z1
        dot=x21*x31+y21*y31+z21*z31
        #print(dot)
    
    # Construct the fourth vertex
    x4=(x2-x1)+x3
    y4=(y2-y1)+y3
    z4=(z2-z1)+z3
    if verbose>0:
        print('parallelogram(): x1,y1,z1,mat',x1,y1,z1,mat_name)
        print('parallelogram(): x2,y2,z2',x2,y2,z2)
        print('parallelogram(): x3,y3,z3',x3,y3,z3)
        print('parallelogram(): x4,y4,z4',x4,y4,z4)
    
    face=[]
    vert=[]
    text_uv=[]
    
    # Add the 4 vertices
    vert.append([x1,y1,z1])
    vert.append([x2,y2,z2])
    vert.append([x3,y3,z3])
    vert.append([x4,y4,z4])

    # Add the 4 texture coordinates
    text_uv.append([0.0,1.0])
    text_uv.append([1.0,1.0])
    text_uv.append([0.0,0.0])
    text_uv.append([1.0,0.0])
    
    # The four sides with labels
    if mat_name=='':
        face.append([1,2,3])
        face.append([3,2,4])
    else:
        face.append([1,2,3,mat_name])
        face.append([3,2,4,mat_name])
    
    # Rearrange for GLTF. to compute normals, we use the cross
    # products.

    vert2=[]
    norms2=[]
    txt2=[]
    
    for i in range(0,len(face)):

        # Add the vertices to the new vertex array
        vert2.append(vert[face[i][0]-1])
        vert2.append(vert[face[i][1]-1])
        vert2.append(vert[face[i][2]-1])

        # Compute the norm
        p1=vert[face[i][0]-1]
        p2=vert[face[i][1]-1]
        p3=vert[face[i][2]-1]
        v1=[1]*3
        v2=[1]*3
        for j in range(0,3):
            v1[j]=p2[j]-p1[j]
            v2[j]=p3[j]-p2[j]
        norm=cross(v1,v2,norm=True)
        for k in range(0,3):
            norms2.append([norm[0],norm[1],norm[2]])

        txt2.append(text_uv[face[i][0]-1])
        txt2.append(text_uv[face[i][1]-1])
        txt2.append(text_uv[face[i][2]-1])

        if len(face[i])>3:
            face[i]=[i*3,i*3+1,i*3+2,face[i][3]]
        else:
            face[i]=[i*3,i*3+1,i*3+2]

    # Print out results
    if verbose>1:
        print('parallelogram(): index, faces, material')
        print('  i, vertex_i, norm_i')
        print('')
        for ki in range(0,len(vert2),3):
            if len(face[int(ki/3)])>=4:
                print('%d [%d,%d,%d] mat: %s' % (int(ki/3),face[int(ki/3)][0],
                                                 face[int(ki/3)][1],
                                                 face[int(ki/3)][2],
                                                 face[int(ki/3)][3]))
            else:
                print('%d [%d,%d,%d]' % (int(ki/3),face[int(ki/3)][0],
                                                 face[int(ki/3)][1],
                                                 face[int(ki/3)][2]))
            print(('  0 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e]\n    '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki][0],vert2[ki][1],
                                             vert2[ki][2],txt2[ki][0],
                                             txt2[ki][1],norms2[ki][0],
                                             norms2[ki][1],norms2[ki][2]))
            print(('  1 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e]\n    '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+1][0],vert2[ki+1][1],
                                             vert2[ki+1][2],txt2[ki+1][0],
                                             txt2[ki+1][1],norms2[ki+1][0],
                                             norms2[ki+1][1],norms2[ki+1][2]))
            print(('  2 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e]\n    '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+2][0],vert2[ki+2][1],
                                             vert2[ki+2][2],txt2[ki+2][0],
                                             txt2[ki+2][1],norms2[ki+2][0],
                                             norms2[ki+2][1],norms2[ki+2][2]))
            print('')
            
    return vert2,face,norms2,txt2
            
class threed_objects:
    """A set of three-dimensional objects
    """
    
    mesh_list=[]
    """
    List of groups of faces
    """
    mat_list=[]
    """
    List of materials
    """

    def make_unique_name(self, prefix : str):
        """Using the specified ``prefix``, create a unique name for a mesh
        object by adding an integer suffix from 1 to 100.
        """
        for i in range(1,101):
            found=False
            name=prefix+str(i)
            for j in range(0,len(self.mesh_list)):
                if self.mesh_list[j].name==name:
                    found=True
            if found==False:
                return name
        raise ValueError('In function threed_objects::'+
                         'make_unique_name(): Could not make unique '+
                         'name with prefix '+prefix+'.')
        return
        
    
    def add_object(self, mesh: mesh_object, verbose : int = 0):
        """Add an object given 'lv', a list of vertices, and 'mesh', a mesh
        of triangular faces among those vertices.

        Optionally, also specify the vertex normals in ``normals``.

        """

        if len(mesh.vn_list)>0 and len(mesh.vn_list)!=len(mesh.vert_list):
            raise ValueError('List of normals has size',len(mesh.vn_list),
                             'and list of vertices is of size',
                             len(mesh.vert_list))
        
        if len(mesh.vt_list)>0 and len(mesh.vt_list)!=len(mesh.vert_list):
            raise ValueError('List of texture coordinates has size',
                             len(mesh.vt_list),
                             'and list of vertices is of size',
                             len(mesh.vert_list))

        # Find the first empty vertex index
        len_lv=len(mesh.vert_list)
        len_lvt=len(mesh.vt_list)
        len_lvn=len(mesh.vn_list)

        # Check that normals are normalized
        for i in range(0,len_lvn):
            mag=numpy.sqrt(mesh.vn_list[i][0]*mesh.vn_list[i][0]+
                           mesh.vn_list[i][1]*mesh.vn_list[i][1]+
                           mesh.vn_list[i][2]*mesh.vn_list[i][2])
            if mag<0.9999 or mag>1.00001:
                raise ValueError('Normal '+str(i)+' has a magnitude of '+
                                 str(mag)+' ['+str(mesh.vn_list[i])+'].')
        
        # Iterate over each face
        if verbose>0:
            print('threed_object::add_object():',
                  'Adjust faces for group',mesh.name,'and check.')
        
        for i in range(0,len(mesh.faces)):

            # Check to make sure we don't have OBJ indices in
            # GLTF mode
            if len(mesh.faces[i])>4:
                raise ValueError('Face '+str(i)+' has more than 4 '+
                                 'elements.')
            
            # Check if there is an undefined material in this face
            if len(mesh.faces[i])==4:
                mat_found=False
                mat_tmp=mesh.faces[i][3]
                for k in range(0,len(self.mat_list)):
                    if self.mat_list[k].name==mat_tmp:
                        mat_found=True
                if mat_found==False:
                    raise ValueError('Face '+str(i)+' refers to a '+
                                     'material "'+str(mat_tmp)+
                                     '" which is not in the list of '+
                                     'materials.')
                    
        # Check if there is an undefined material in the
        # mesh_object data member 'mat'
        if mesh.mat!='':
            mat_found=False
            for k in range(0,len(self.mat_list)):
                if self.mat_list[k].name==mesh.mat:
                    mat_found=True
            if mat_found==False:
                raise ValueError('The group of faces names a material '+
                                 mesh.mat+' which is not in the list of '+
                                 'materials.')

        # Sort the group of vertices by material for output later
        if verbose>0:
            print('threed_object::add_object(): Sort group named',
                  mesh.name,'by material.')
        mesh.sort_by_mat()
                
        # Add the group of faces to the list
        self.mesh_list.append(mesh)
        
        return

    def add_mat(self, m: material):
        """Add material ``m`` to the list of materials.
        """
        mat_found=False
        for i in range(0,len(self.mat_list)):
            if self.mat_list[i].name==m.name:
                mat_found=True
        if mat_found==False:
            self.mat_list.append(m)
        return
    
    def get_mat(self, mat_name: str):
        """Get material named ``mat_name``.
        """
        for i in range(0,len(self.mat_list)):
            if self.mat_list[i].name==mat_name:
                return self.mat_list[i]
        raise ValueError("No mat named "+mat_name)
    
    def add_object_mat(self, gf: mesh_object, m: material):
        """Add an object given 'lv', a list of vertices, and 'gf', a group of
        triangular faces among those vertices, and 'm', the material
        for all of the faces.

        """
        self.add_mat(m)
        if gf.mat=='':
            gf.mat=m.name
        self.add_object(gf)
        return

    def is_mat(self, m: str):
        """Return true if a a material named ``m`` has been added
        """
        for i in range(0,len(self.mat_list)):
            if self.mat_list[i].name==m:
                return True
        return False
    
    def get_mat_index(self, m: str):
        """Return true if a a material named ``m`` has been added
        """
        for i in range(0,len(self.mat_list)):
            if self.mat_list[i].name==m:
                return i
        raise ValueError("No mat named "+m)
    
    def add_object_mat_list(self, gf: mesh_object, lm):
        """Add an object given 'lv', a list of vertices, and 'gf', a group of
        triangular faces among those vertices, and 'm', the material
        for all of the faces.
        """
        
        for k in range(0,len(lm)):
            self.add_mat(lm[k])
        self.add_object(gf)
        return

    def write_gltf(self, wdir: str, prefix: str, verbose: int = 0,
                   rotate_zup: bool = True):
        """Write all objects to an '.gltf' file, creating a '.bin' file
        """

        import json
        from struct import pack
        
        # Remove suffix if it is present
        if prefix[-5:]=='.gltf':
            prefix=prefix[:-5]
        gltf_file=wdir+"/"+prefix+'.gltf'
        bin_file=wdir+"/"+prefix+'.bin'
        
        nodes_list=[]
            
        for k in range(0,len(self.mesh_list)):
            nodes_list.append(k)
                
        jdat={"asset": {"generator": "o2sclpy v"+version,
                        "version": "2.0",
                        "copyright":
                        "Copyright (C) 2023-2024, Andrew W. Steiner", },
              "scene": 0,
              "scenes": [{ "name": "Scene",
                           "nodes": nodes_list
                          }]
              }
            
        nodes_list=[]
        for k in range(0,len(self.mesh_list)):
            if rotate_zup:
                nodes_list.append({"mesh" : k,
                                   "name" : self.mesh_list[k].name,
                                   "rotation": [0.7071068286895752,0,0,
                                                -0.7071068286895752]
                                   })
            else:
                nodes_list.append({"mesh" : k,
                                   "name" : self.mesh_list[k].name})
                                   
        jdat["nodes"]=nodes_list

        mesh_list=[]
        acc_list=[]
        buf_list=[]
        mat_json=[]
        txt_list=[]
        img_list=[]
            
        f2=open(bin_file,'wb')
            
        texture_map=[-1]*len(self.mat_list)
        texture_index=0
        
        for i in range(0,len(self.mat_list)):

            this_mat=self.mat_list[i]

            # Construct a Python dictory for the material JSON
            mat_dict={"name": this_mat.name}

            pbr_dict={}
            if this_mat.txt!='':
                pbr_dict["baseColorTexture"]={"index":
                                              texture_index}
                txt_list.append({"source": texture_index})
                img_list.append({"mimeType": "image/png",
                                 "name": this_mat.name,
                                 "uri": this_mat.txt})
                texture_map[i]=texture_index
                texture_index=texture_index+1
            elif len(this_mat.base_color)>=4:
                pbr_dict["baseColorFactor"]=[
                        this_mat.base_color[0],
                        this_mat.base_color[1],
                        this_mat.base_color[2],
                        this_mat.base_color[3]]
            else:
                pbr_dict["baseColorFactor"]=[
                        this_mat.base_color[0],
                        this_mat.base_color[1],
                        this_mat.base_color[2],1.0]
            if this_mat.metal!=0.0:
                pbr_dict["metallicFactor"]=this_mat.metal
            if this_mat.rough!=1.0:
                pbr_dict["roughnessFactor"]=this_mat.rough
            mat_dict["pbrMetallicRoughness"]=pbr_dict
            
            mat_dict["doubleSided"]=this_mat.ds
            if this_mat.alpha_mode!='opaque':
                mat_dict["alphaMode"]=this_mat.alpha_mode.upper()
            if this_mat.alpha_cutoff!=0.5:
                mat_dict["alphaCutoff"]=this_mat.alpha_cutoff
            if (this_mat.emi_factor[0]>0.0 or
                this_mat.emi_factor[1]>0.0 or
                this_mat.emi_factor[2]>0.0):
                mat_dict["emissiveFactor"]=this_mat.emi_factor

            # Add this material JSON to the full material list
            mat_json.append(mat_dict)
        
        # Add each set of faces as a group
        acc_index=0
        offset=0

        for i in range(0,len(self.mesh_list)):
                
            normals=False
            if len(self.mesh_list[i].vn_list)>0:
                normals=True
                if (len(self.mesh_list[i].vert_list)!=
                    len(self.mesh_list[i].vn_list)):
                   print('Problem with normals.')
                   quit()
            texcoords=False
            if len(self.mesh_list[i].vt_list)>0:
                texcoords=True
                if (len(self.mesh_list[i].vert_list)!=
                    len(self.mesh_list[i].vt_list)):
                   print('Problem with texcoords.')
                   quit()

            long_ints=False
            if len(self.mesh_list[i].vert_list)>=32768:
                long_ints=True
                print('Function write_gltf() using long integers',
                      'for mesh',self.mesh_list[i].name+'.')

            att={}
            face_bin=[]
            norm_bin=[]
            txts_bin=[]
            vert_bin=[]
            vert_map = [-1] * len(self.mesh_list[i].vert_list)
            prim_list=[]

            if False:
                for j in range(0,len(self.mesh_list[i].vert_list)):
                    for kk in range(0,3):
                        v0=float(self.mesh_list[i].vert_list[j][kk])
                        vert_bin.append(v0)

                for j in range(0,len(self.mesh_list[i].vn_list)):
                    for kk in range(0,3):
                        v0=float(self.mesh_list[i].vn_list[j][kk])
                        norm_bin.append(v0)

                if texcoords and self.mat_list[mat_index].txt!='':
                    for j in range(0,len(self.mesh_list[i].vt_list)):
                        for kk in range(0,2):
                            v0=float(self.mesh_list[i].vt_list[j][kk])
                            txts_bin.append(v0)
                        
            for j in range(0,len(self.mesh_list[i].faces)):

                # Determine the material for this face
                mat1=''
                mat_index=-1

                lf1=len(self.mesh_list[i].faces[j])
                if lf1==4:
                    mat1=self.mesh_list[i].faces[j][lf1-1]
                    mat_index=self.get_mat_index(mat1)
                else:
                    mat1=self.mesh_list[i].mat
                    if mat1!='':
                        mat_index=self.get_mat_index(mat1)

                if False:
                    for kk in range(0,3):
                        face_bin.append(self.mesh_list[i].faces[j][kk])
                else:
                    # Map the first vertex
                    ix=self.mesh_list[i].faces[j][0]
                    if vert_map[ix]==-1:
                        # Converting the vertices to "float()"
                        # helps ensure single precision and then
                        # validators don't complain that max and
                        # min are wrong.
                        v0=float(self.mesh_list[i].vert_list[ix][0])
                        vert_bin.append(v0)
                        v1=float(self.mesh_list[i].vert_list[ix][1])
                        vert_bin.append(v1)
                        v2=float(self.mesh_list[i].vert_list[ix][2])
                        vert_bin.append(v2)
                        if normals:
                            v3=float(self.mesh_list[i].vn_list[ix][0])
                            norm_bin.append(v3)
                            v4=float(self.mesh_list[i].vn_list[ix][1])
                            norm_bin.append(v4)
                            v5=float(self.mesh_list[i].vn_list[ix][2])
                            norm_bin.append(v5)
                        if texcoords and self.mat_list[mat_index].txt!='':
                            v6=float(self.mesh_list[i].vt_list[ix][0])
                            txts_bin.append(v6)
                            v7=float(self.mesh_list[i].vt_list[ix][1])
                            txts_bin.append(v7)
                            #print(self.mesh_list[i].name,'texcoords1',v6,v7)
                        vert_map[ix]=int(len(vert_bin)/3)
                        # We have to subtract one here because
                        # the point has already been added to 'vert_bin'
                        face_bin.append(int(len(vert_bin)/3)-1)
                    else:
                        face_bin.append(vert_map[ix])
                    # Map the second vertex
                    ix=self.mesh_list[i].faces[j][1]
                    if vert_map[ix]==-1:
                        v8=float(self.mesh_list[i].vert_list[ix][0])
                        vert_bin.append(v8)
                        v9=float(self.mesh_list[i].vert_list[ix][1])
                        vert_bin.append(v9)
                        v10=float(self.mesh_list[i].vert_list[ix][2])
                        vert_bin.append(v10)
                        if normals:
                            v11=float(self.mesh_list[i].vn_list[ix][0])
                            norm_bin.append(v11)
                            v12=float(self.mesh_list[i].vn_list[ix][1])
                            norm_bin.append(v12)
                            v13=float(self.mesh_list[i].vn_list[ix][2])
                            norm_bin.append(v13)
                        if texcoords and self.mat_list[mat_index].txt!='':
                            v14=float(self.mesh_list[i].vt_list[ix][0])
                            txts_bin.append(v14)
                            v15=float(self.mesh_list[i].vt_list[ix][1])
                            txts_bin.append(v15)
                            #print(self.mesh_list[i].name,'texcoords2',v14,v15)
                        vert_map[ix]=int(len(vert_bin)/3)
                        # We have to subtract one here because
                        # the point has already been added to 'vert_bin'
                        face_bin.append(int(len(vert_bin)/3)-1)
                    else:
                        face_bin.append(vert_map[ix])
                    # Map the third vertex
                    ix=self.mesh_list[i].faces[j][2]
                    if vert_map[ix]==-1:
                        v16=float(self.mesh_list[i].vert_list[ix][0])
                        vert_bin.append(v16)
                        v17=float(self.mesh_list[i].vert_list[ix][1])
                        vert_bin.append(v17)
                        v18=float(self.mesh_list[i].vert_list[ix][2])
                        vert_bin.append(v18)
                        if normals:
                            v19=float(self.mesh_list[i].vn_list[ix][0])
                            norm_bin.append(v19)
                            v20=float(self.mesh_list[i].vn_list[ix][1])
                            norm_bin.append(v20)
                            v21=float(self.mesh_list[i].vn_list[ix][2])
                            norm_bin.append(v21)
                        if texcoords and self.mat_list[mat_index].txt!='':
                            v22=float(self.mesh_list[i].vt_list[ix][0])
                            txts_bin.append(v22)
                            v23=float(self.mesh_list[i].vt_list[ix][1])
                            txts_bin.append(v23)
                            #print(self.mesh_list[i].name,'texcoords3',v22,v23)
                        vert_map[ix]=int(len(vert_bin)/3)
                        # We have to subtract one here because
                        # the point has already been added to 'vert_bin'
                        face_bin.append(int(len(vert_bin)/3)-1)
                    else:
                        face_bin.append(vert_map[ix])

                # Determine if the next face is composed of a
                # different material, if so, set mat2 and
                # flip next_face_different_mat to True
                next_face_different_mat=False
                if j<len(self.mesh_list[i].faces)-1:
                    mat2=''
                    lf2=len(self.mesh_list[i].faces[j+1])
                    if lf2==4:
                        mat2=self.mesh_list[i].faces[j+1][lf2-1]
                        if mat1!=mat2:
                            next_face_different_mat=True

                # If we're at the end, or we're switching materials,
                # then add the primitive to the mesh and update
                # the binary data file accordingly
                if (j==len(self.mesh_list[i].faces)-1 or
                    next_face_different_mat==True):

                    # 'f' is float, 'H' is unsigned short, and 'I' is
                    # unsigned int
                    
                    dat1=pack('<'+'f'*len(vert_bin),*vert_bin)
                    f2.write(dat1)
                    if normals:
                        dat3=pack('<'+'f'*len(norm_bin),*norm_bin)
                        f2.write(dat3)
                    # If the object provides texture coordinates, but
                    # there's no texture, then there's no need to
                    # output them
                    if texcoords and self.mat_list[mat_index].txt!='':
                        dat4=pack('<'+'f'*len(txts_bin),*txts_bin)
                        f2.write(dat4)

                    if long_ints==True:
                        dat2=pack('<'+'I'*len(face_bin),*face_bin)
                        f2.write(dat2)
                    else:
                        dat2=pack('<'+'H'*len(face_bin),*face_bin)
                        f2.write(dat2)
        
                    max_v=[0,0,0]
                    min_v=[0,0,0]
                    for ii in range(0,len(vert_bin),3):
                        for jj in range(0,3):
                            if ii==0 or vert_bin[ii+jj]<min_v[jj]:
                                min_v[jj]=vert_bin[ii+jj]
                            if ii==0 or vert_bin[ii+jj]>max_v[jj]:
                                max_v[jj]=vert_bin[ii+jj]
                    
                    # 5120 is signed byte
                    # 5121 is unsigned byte
                    # 5122 is signed short
                    # 5123 is unsigned short
                    # 5125 is unsigned int
                    # 5126 is signed float
                    
                    acc_list.append({"bufferView": acc_index,
                                     "componentType": 5126,
                                     "count": int(len(vert_bin)/3),
                                     "max": max_v,
                                     "min": min_v,
                                     "type": "VEC3"})
                    att["POSITION"]=acc_index
                    acc_index=acc_index+1
                    
                    if normals:
                        acc_list.append({"bufferView": acc_index,
                                         "componentType": 5126,
                                         "count": int(len(norm_bin)/3),
                                         "type": "VEC3"})
                        att["NORMAL"]=acc_index
                        acc_index=acc_index+1
                        
                    # If the object provides texture coordinates, but
                    # there's no texture, then there's no need to
                    # output them
                    if texcoords and self.mat_list[mat_index].txt!='':
                        acc_list.append({"bufferView": acc_index,
                                         "componentType": 5126,
                                         "count": int(len(txts_bin)/2),
                                         "type": "VEC2"})
                        att["TEXCOORD_0"]=acc_index
                        acc_index=acc_index+1
                        
                    if long_ints:
                        acc_list.append({"bufferView": acc_index,
                                         "componentType": 5125,
                                         "count": int(len(face_bin)/1),
                                         "type": "SCALAR"})
                    else:
                        acc_list.append({"bufferView": acc_index,
                                         "componentType": 5123,
                                         "count": int(len(face_bin)/1),
                                         "type": "SCALAR"})
                    if self.mesh_list[i].obj_type=='triangles':
                        if mat1=='':
                            prim_list.append({"attributes": att,
                                              "indices": acc_index})
                        else:
                            prim_list.append({"attributes": att,
                                              "indices": acc_index,
                                              "material": mat_index})
                    else:
                        
                        #0 POINTS
                        #1 LINES
                        #2 LINE_LOOP
                        #3 LINE_STRIP
                        #4 TRIANGLES
                        #5 TRIANGLE_STRIP
                        #6 TRIANGLE_FAN

                        mode_num=4
                        if self.mesh_list[i].obj_type=='lines':
                            mode_num=1
                        elif self.mesh_list[i].obj_type=='points':
                            mode_num=0
                        if mat1=='':
                            prim_list.append({"attributes": att,
                                              "indices": acc_index,
                                              "mode": mode_num})
                        else:
                            prim_list.append({"attributes": att,
                                              "indices": acc_index,
                                              "material": mat_index,
                                              "mode": mode_num})
                    if j==len(self.mesh_list[i].faces)-1:
                        mesh_list.append({"name": self.mesh_list[i].name,
                                          "primitives": prim_list})
                        
                    acc_index=acc_index+1
        
                    # 34962 is "ARRAY_BUFFER"
                    # 34963 is "ELEMENT_ARRAY_BUFFER"
                    
                    buf_list.append({"buffer": 0,
                                     "byteLength": 4*len(vert_bin),
                                     "byteOffset": offset,
                                     "target": 34962})
                    offset+=4*len(vert_bin)
                    if normals:
                        buf_list.append({"buffer": 0,
                                         "byteLength": 4*len(norm_bin),
                                         "byteOffset": offset,
                                         "target": 34962})
                        offset+=4*len(norm_bin)
                    # If the object provides texture coordinates, but
                    # there's no texture, then there's no need to
                    # output them
                    if texcoords and self.mat_list[mat_index].txt!='':
                        buf_list.append({"buffer": 0,
                                         "byteLength": 4*len(txts_bin),
                                         "byteOffset": offset,
                                         "target": 34962})
                        offset+=4*len(txts_bin)
                    if long_ints==True:
                        buf_list.append({"buffer": 0,
                                         "byteLength": 4*len(face_bin),
                                         "byteOffset": offset,
                                         "target": 34963})
                        offset+=4*len(face_bin)
                    else:
                        buf_list.append({"buffer": 0,
                                         "byteLength": 2*len(face_bin),
                                         "byteOffset": offset,
                                         "target": 34963})
                        offset+=2*len(face_bin)
                    if verbose>1:
                        print('offset:',offset)

                        print('len(face_bin):',self.mesh_list[i].name,
                              len(face_bin))
                        print(('min,max: [%7.6e,%7.6e,%7.6e] '+
                              '[%7.6e,%7.6e,%7.6e]') %
                              (min_v[0],min_v[1],min_v[2],
                               max_v[0],max_v[1],max_v[2]))
                        print('')
                    
                    # Reset the primitive objects so that
                    # we can start a new one
                    att={}
                    face_bin=[]
                    vert_bin=[]
                    norm_bin=[]
                    vert_map = [-1] * len(self.mesh_list[i].vert_list)

        # Add the top-level data to the json object
        if verbose>2:
            print('Converting mesh list:')
        jdat["meshes"]=mesh_list
        if verbose>2:
            print('Converting materials:')
        if len(mat_json)>0:
            jdat["materials"]=mat_json
        if verbose>2:
            print('Converting accessors:')
        jdat["accessors"]=acc_list
        if verbose>2:
            print('Converting buffers:')
        jdat["bufferViews"]=buf_list
        jdat["buffers"]=[{"byteLength": offset,
                          "uri": prefix+'.bin'}]
        if verbose>2:
            print('Converting textures:')
        if len(txt_list)>0:
            jdat["textures"]=txt_list
            jdat["images"]=img_list

        # write the json file
        if verbose>2:
            print('Writing JSON:')
        f=open(gltf_file,'w',encoding='utf-8')
        json.dump(jdat,f,ensure_ascii=False,indent=2)
        f.close()

        if verbose>2:
            print('Closing .bin file:')
        f2.close()
            
        return
        
class td_plot_base(yt_plot_base):
    """
    A class for managing 3D visualizations
    """

    latex_png_counter=0
    """
    Counter for PNGs from LaTeX used in td_mat()
    """
    
    def __init__(self):
        super().__init__()
        self.to=threed_objects()
        self.td_wdir='.'
        self.latex_png_counter=0
        return

    def td_den_plot(self,o2scl,amp,args,cmap='',mat_name='white',
                    normals=False):
        """Documentation for o2graph command ``td-den-plot``:

        Create a 3D density plot (experimental).

        Command-line arguments: ``<x label> <y label> <z label> [kwargs]``

        Note that normals are typically not specified, because the
        density plot presumes flat shading. Blender, for example, uses
        smooth shading for GLTF files when normals are specified, and
        this can complicate the density plot.
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
                cmap_mats.append(material('cmap_'+str(i),
                                          [rgb[0],rgb[1],rgb[2]]))
                
            colors=True
            if self.verbose>2:
                print('td_den_plot(): Using colors from cmap',cmap)
            
        # Vertices for the density plot
        den_vert=[]
        # Faces for the density plot
        den_face=[]
        # Normals for the density plot
        den_norm=[]
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
                    arr1=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i,j]-self.zlo)/(self.zhi-self.zlo)]
                    arr2=[(xgrid[i+1]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i+1,j]-self.zlo)/(self.zhi-self.zlo)]
                    arr3=[(xgrid[i+1]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j+1]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i+1,j+1]-self.zlo)/(self.zhi-self.zlo)]
                elif i<nxt-1:
                    arr1=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j-1]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i,j-1]-self.zlo)/(self.zhi-self.zlo)]
                    arr2=[(xgrid[i+1]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j-1]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i+1,j-1]-self.zlo)/(self.zhi-self.zlo)]
                    arr3=[(xgrid[i+1]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i+1,j]-self.zlo)/(self.zhi-self.zlo)]
                elif j<nyt-1:
                    arr1=[(xgrid[i-1]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i-1,j]-self.zlo)/(self.zhi-self.zlo)]
                    arr2=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i,j]-self.zlo)/(self.zhi-self.zlo)]
                    arr3=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j+1]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i,j+1]-self.zlo)/(self.zhi-self.zlo)]
                else:
                    arr1=[(xgrid[i-1]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j-1]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i-1,j-1]-self.zlo)/(self.zhi-self.zlo)]
                    arr2=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j-1]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i,j-1]-self.zlo)/(self.zhi-self.zlo)]
                    arr3=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                          (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                          (sl[i,j]-self.zlo)/(self.zhi-self.zlo)]
                diff12=[arr2[kk]-arr1[kk] for kk in range(0,3)]
                diff23=[arr3[kk]-arr2[kk] for kk in range(0,3)]
                den_norm.append(cross(diff12,diff23,True))
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
                        arr3=[k+2+nyt,k+2,k+1+nyt,cmap_name]
                        den_face.append(arr3)
                        
                    else:
                        
                        arr2=[k+1,k+nyt+1,k+2]
                        den_face.append(arr2)
                        arr3=[k+2+nyt,k+2,k+1+nyt]
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

            if False:
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
            else:
                norms2.append(den_norm[den_face[i][0]-1])
                norms2.append(den_norm[den_face[i][1]-1])
                norms2.append(den_norm[den_face[i][2]-1])

            if colors==True:
                den_face[i]=[i*3,i*3+1,i*3+2,den_face[i][3]]
            else:
                den_face[i]=[i*3,i*3+1,i*3+2]

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
            if normals:
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
            if normals:
                gf.vn_list=norms2
            self.to.add_object_mat(gf,white)

        return
        
    def td_scatter(self,o2scl,amp,args,n_subdiv: int = 0, r: float = 0.04,
                   metal: str = '',rough: str = ''):
        """Documentation for o2graph command ``td-scatter``:

        Create a 3D scatter plot (experimental).

        Command-line arguments: ``<x column> <y column> <z column> 
        [r column] [g column] [b column] [kwargs]``

        Full desc.
        """
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        # If true, then a color map has been specified and we need
        # to add materials for each face
        colors=False
        
        if curr_type==b'table':
            col_x=args[0]
            col_y=args[1]
            col_z=args[2]
            col_r=''
            col_g=''
            col_b=''
            col_m=''
            col_ro=''
            if len(args)>4:
                col_r=args[3]
                col_g=args[4]
                col_b=args[5]
                colors=True
        else:
            print("Command 'td-scatter' not supported for type",
                  curr_type,".")
            return

        if metal[0:4]=='col:':
            col_m=metal[4:]
            print('Setting metalness to value from column',col_m)
            
        if rough[0:4]=='col:':
            col_ro=rough[4:]
            print('Setting roughness to value from column',col_ro)
        
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
            if col_m!='':
                cm=table[col_m][0:n]
                mlo=numpy.min(cm)
                mhi=numpy.max(cm)
            if col_ro!='':
                cro=table[col_ro][0:n]
                rolo=numpy.min(cro)
                rohi=numpy.max(cro)
            
        if colors==False:

            gf=mesh_object('scatter',[])
            
            for i in range(0,n):
                xnew=(cx[i]-self.xlo)/(self.xhi-self.xlo)
                ynew=(cy[i]-self.ylo)/(self.yhi-self.ylo)
                znew=(cz[i]-self.zlo)/(self.zhi-self.zlo)
                vtmp,ntmp,ftmp,ttmp=icosphere(xnew,ynew,znew,r,
                                              n_subdiv=n_subdiv)
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
                vtmp,ntmp,ftmp,ttmp=icosphere(xnew,ynew,znew,r,
                                              n_subdiv=n_subdiv)
                lv=len(gf.vert_list)
                for k in range(0,len(vtmp)):
                    gf.vert_list.append(vtmp[k])
                for k in range(0,len(ntmp)):
                    gf.vn_list.append(ntmp[k])
                for k in range(0,len(ftmp)):
                    gf.faces.append([ftmp[k][0]+lv,ftmp[k][1]+lv,
                                     ftmp[k][2]+lv,'mat_point_'+str(i)])

                if metal=='':
                    metal_float=0.0
                elif col_m=='':
                    metal_float=float(metal)
                else:
                    metal_float=(cm[i]-mlo)/(mhi-mlo)
                if rough=='':
                    rough_float=1.0
                elif col_ro=='':
                    rough_float=float(rough)
                else:
                    rough_float=(cro[i]-rolo)/(rohi-rolo)

                mat=material('mat_point_'+str(i),[(cr[i]-rlo)/(rhi-rlo),
                                                  (cg[i]-glo)/(ghi-glo),
                                                  (cb[i]-blo)/(bhi-blo)],
                             metal=metal_float,rough=rough_float)
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

    def td_icos(self,args,n_subdiv=0,r=0.04,phi_cut='',mat=''):
        """Documentation for o2graph command ``td-icos``:

        Create a 3D icosphere (experimental).

        Command-line arguments: ``<x> <y> <z> [kwargs]``

        Note that normals are typically not specified, because the
        density plot presumes flat shading. Blender, for example, uses
        smooth shading for GLTF files when normals are specified, and
        this can complicate the density plot.
        """
        import copy
        
        if mat=='':
            if self.to.is_mat('white')==False:
                m=material('white',[1,1,1])
                self.to.add_mat(m)
            else:
                m=self.to.get_mat('white')
        else:
            if self.to.is_mat(mat)==False:
                raise ValueError("No mat named "+mat+" in td_icos().")
            m=self.to.get_mat(mat)
            
        val_x=float(args[0])
        val_y=float(args[1])
        val_z=float(args[2])
        if self.xset==False:
            if val_x<0:
                self.xlo=val_x*2
                self.xhi=0
            elif val_x==0:
                self.xlo=-1
                self.xhi=+1
            else:
                self.xlo=0
                self.xhi=val_x*2
            if self.verbose>2:
                print('td_icos(): x limits not set, so setting to',
                      self.xlo,',',self.xhi)
        if self.yset==False:
            if val_y<0:
                self.ylo=val_y*2
                self.yhi=0
            elif val_y==0:
                self.ylo=-1
                self.yhi=+1
            else:
                self.ylo=0
                self.yhi=val_y*2
            if self.verbose>2:
                print('td_icos(): y limits not set, so setting to',
                      self.ylo,',',self.yhi)
        if self.zset==False:
            if val_z<0:
                self.zlo=val_z*2
                self.zhi=0
            elif val_z==0:
                self.zlo=-1
                self.zhi=+1
            else:
                self.zlo=0
                self.zhi=val_z*2
            if self.verbose>2:
                print('td_icos(): z limits not set, so setting to',
                      self.zlo,',',self.zhi)

        uname=self.to.make_unique_name('icos')
                
        gf=mesh_object(uname,[],mat=mat)
            
        xnew=(val_x-self.xlo)/(self.xhi-self.xlo)
        ynew=(val_y-self.ylo)/(self.yhi-self.ylo)
        znew=(val_z-self.zlo)/(self.zhi-self.zlo)
        if phi_cut=='':
            vtmp,ntmp,ftmp,ttmp=icosphere(xnew,ynew,znew,
                                          r,n_subdiv=n_subdiv)
        else:
            vtmp,ntmp,ftmp,ttmp=icosphere(xnew,ynew,znew,
                                          r,n_subdiv=n_subdiv,
                                          phi_cut=phi_cut)
            
        for k in range(0,len(vtmp)):
            gf.vert_list.append(vtmp[k])
            #print('m',len(gf.vert_list),vtmp[k])
        for k in range(0,len(ntmp)):
            gf.vn_list.append(ntmp[k])
        if m.txt!='':
            for k in range(0,len(ttmp)):
                txtx=copy.deepcopy(ttmp[k])
                txtx[0]=txtx[0]*m.txt_frac_w
                txtx[1]=txtx[1]*m.txt_frac_h
                gf.vt_list.append(txtx)
        for k in range(0,len(ftmp)):
            ftmp[k][0]=ftmp[k][0]
            ftmp[k][1]=ftmp[k][1]
            ftmp[k][2]=ftmp[k][2]
            gf.faces.append(ftmp[k])
                    
        # Convert to GLTF
                
        vert2=[]
        norms2=[]
        txt2=[]
        #print('txt',txt,len(gf.vt_list),len(ttmp))
        
        for i in range(0,len(gf.faces)):

            # Add the vertices to the new vertex array
            vert2.append(gf.vert_list[gf.faces[i][0]])
            vert2.append(gf.vert_list[gf.faces[i][1]])
            vert2.append(gf.vert_list[gf.faces[i][2]])
    
            # Add the normals to the new normal array
            norms2.append(gf.vn_list[gf.faces[i][0]])
            norms2.append(gf.vn_list[gf.faces[i][1]])
            norms2.append(gf.vn_list[gf.faces[i][2]])

            if m.txt!='':
                # Add the textures to the new texture coordinate array
                txt2.append(gf.vt_list[gf.faces[i][0]])
                txt2.append(gf.vt_list[gf.faces[i][1]])
                txt2.append(gf.vt_list[gf.faces[i][2]])

        if False:
            print('td_icos:')
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

        gf.vert_list=vert2
        if m.txt!='':
            gf.vt_list=txt2
        if mat!='':
            gf.mat=m.name
        gf.vn_list=norms2
                
        self.to.add_object(gf)

        return

    def td_line(self,x1,y1,z1,x2,y2,z2,name='line',mat='white',
                coords='user'):
        """Documentation for o2graph command ``td-line``:

        Plot a line in a 3d visualization (experimental)

        Command-line arguments: ``<x1> <y1> <z1> <x2> <y2> <z2> 
        [kwargs]``

        By default, the line
        coordinates are specified in the internal coordinate system.
        If the keyword argument ``coords`` is ``user``, then the
        coordinates are in the user coordinate system.
        """
        uname=self.to.make_unique_name(name)

        if coords=='user':
            if self.xset==False or self.yset==False or self.zset==False:
                raise ValueError("User coordinates not set in"+
                                 " 'td-arrow'.")
            x1=(x1-self.xlo)/(self.xhi-self.xlo)
            y1=(y1-self.ylo)/(self.yhi-self.ylo)
            z1=(z1-self.zlo)/(self.zhi-self.zlo)
            x2=(x2-self.xlo)/(self.xhi-self.xlo)
            y2=(y2-self.ylo)/(self.yhi-self.ylo)
            z2=(z2-self.zlo)/(self.zhi-self.zlo)
            
        line_vert=[[x1,y1,z1],[x2,y2,z2]]
    
        if type(mat)==str:
            if not self.to.is_mat(mat):
                if mat=='white':
                    white=material('white',[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('No material named',mat,'in td-line')
                    return
            if self.verbose>2:
                print('td_line(): creating group named',name,'with material',
                      mat+'.')
            gf=mesh_object(uname,arr_face,mat=mat,obj_type='lines')
            gf.vert_list=line_vert
            self.to.add_object(gf)
                               
        else:
            
            if self.verbose>2:
                print('td_line(): creating group named',uname,'with material',
                      mat.name+'.')
            if not self.to.is_mat(mat.name):
                self.to.add_mat(mat)
            gf=mesh_object(uname,arr_face,mat=mat.name,obj_type='line')
            gf.vert_list=line_vert
            self.to.add_object(gf)
            
        return

    def td_grid(self,n,name='grid',mat='white',auto_labels=False):
        """
        Documentation for o2graph command ``td-grid``:

        Plot an axis in a 3d visualization (experimental)

        Command-line arguments: ``[kwargs]``

        Plot a grid of lines
        """
        if n<2:
            raise ValueError('Cannot have n<2 in td_grid.')
        
        uname=self.to.make_unique_name(name)

        for i in range(0,n):
            xi=float(i)/(float(n)-1.0)
            for j in range(0,n):
                yj=float(j)/(float(n)-1.0)
                td_line(xi,yj,0,xi,yj,1,mat=mat)
        for i in range(0,n):
            xi=float(i)/(float(n)-1.0)
            for k in range(0,n):
                zk=float(k)/(float(n)-1.0)
                td_line(xi,0,zk,xi,1,zk,mat=mat)
        for j in range(0,n):
            yj=float(j)/(float(n)-1.0)
            for k in range(0,n):
                zk=float(k)/(float(n)-1.0)
                td_line(xi,0,zk,xi,1,zk,mat=mat)

        #def latex_rectangle(x1,y1,z1,x2,y2,z2,x3,y3,z3,latex,wdir,png_file,
        #mat_name,flatten=True):

        """
        if labels:
            for i in range(0,n):
                xi=float(i)/(float(n)-1.0)
                for j in range(0,n):
                    yj=float(j)/(float(n)-1.0)
                    latex_rectangle(xi-0.01,yj,0.01,
                                    xi-0.06,yj,0.01,
                                    xi-0.06,yj,0.11,'',mat=mat)
            for i in range(0,n):
                xi=float(i)/(float(n)-1.0)
                for k in range(0,n):
                    zk=float(k)/(float(n)-1.0)
                    td_line(xi,0,zk,xi,1,zk,mat=mat)
                    latex_rectangle(xi,0.01,zk-0.01,
                                    xi,0.01,zk-0.06,
                                    xi,0.11,zk-0.06,mat=mat)
            for j in range(0,n):
                yj=float(j)/(float(n)-1.0)
                for k in range(0,n):
                    zk=float(k)/(float(n)-1.0)
                    td_line(xi,0,zk,xi,1,zk,mat=mat)
                    latex_rectangle(xi,0.01,zk-0.01,
                                    xi,0.01,zk-0.06,
                                    xi,0.11,zk-0.06,mat=mat)
        """
            
        return
    
    def td_mat(self, name: str, r: float, g: float, b: float,
               alpha: float=1, metal: float=0, rough: float=1,
               ds: bool=True, txt: str='',
               alpha_mode : str = 'opaque', alpha_cutoff: float = 0.5,
               efr: float = 0.0, efg: float = 0.0, efb: float = 0.0,
               packages: str = '', prefix: str = ''):
        """Documentation for o2graph command ``td-mat``:

        Create a 3d material (experimental)

        Command-line arguments: ``<name> <r> <g> <b> [kwargs]``

        Create a new material with the specified properties. 

        LaTeX textures are created in the working directory with
        the name ``[prefix]latex%d.png`` and then resized, if necessary,
        to files named ``[prefix]latexr%d.png``.
        """
        import os.path
        import tempfile

        if self.to.is_mat(name):
            raise ValueError('Already a material with the name '+
                             name+' in td_plot_base::td_mat().')
        
        if efr<0.0 or efg<0.0 or efb<0.0:
            raise ValueError('Emissive factor cannot be negative.')
            
        emi_factor=[efr,efg,efb]

        # These defaults will serve as the values of `txt_frac_w`,
        # `txt_frac_h`, `txt_w`, and `txt_h` for the new material.
        txt_dim=(1.0,1.0)
        w_new=0
        h_new=0
            
        # First, if the texture is to be built from a LaTeX string,
        # then generate the associated png and replace the string
        # ``txt`` with the png filename.

        latex_png=False
        
        if txt[0:6]=='latex:':
            latex=txt[6:]
            self.latex_png_counter=self.latex_png_counter+1
            tex_png_name=(self.td_wdir+'/'+prefix+'latex'+
                          str(self.latex_png_counter)+'.png')

            pack_split=[]
            if packages!='':
                pack_split=packages.split(',')
            
            if self.verbose>0:
                print('td_mat(): converting',latex,'to',
                      tex_png_name)
            latex_to_png(latex,tex_png_name,packages=pack_split)
                         
            txt=tex_png_name
            latex_png=True

        txt_out_base=txt
            
        if txt!='':
            
            # Process the texture:
            #
            # 1. Test if destination file exists in wdir
            # 2. If so, test to see if the destination is properly sized.
            #    If so, return early. If not, throw an error
            # 3. If not, run png_power_two()

            if latex_png==True:
                txt_dir=self.td_wdir
                txt_base=os.path.basename(txt)
                txt_out_base=(prefix+'latexr'+str(self.latex_png_counter)+
                              '.png')
                txt_out=self.td_wdir+'/'+txt_out_base
                
            else:
                txt_dir=os.path.dirname(txt)
                txt_base=os.path.basename(txt)
                txt_out_base=txt_base
                txt_out=self.td_wdir+'/'+txt_out_base
                
            if self.verbose>0:
                print('td_mat(): Reading file named '+txt_base+
                      ' from directory '+txt_dir+' and writing\n '+
                      ' file '+txt_out)
            
            txt_two_done=False
                
            if False and os.path.isfile(txt_out):

                # This section avoids overwriting textures and reuses
                # those already in the working directory
                from PIL import Image
                img=Image.open(txt_out)
                w=img.width
                h=img.height
                if self.verbose>1:
                    print('td_mat(): Found output file '+txt_out+', with',
                          'width',w,'and height',str(h)+'.')
                w_new=2**(int(numpy.log2(w-1))+1)
                h_new=2**(int(numpy.log2(h-1))+1)
                if w!=w_new or h!=h_new:
                    raise ValueError('Output file '+txt_out+' exists but '+
                                     'is not properly sized.')
                # Clear memory associated with the image (if any)
                del img
                txt_two_done=True

            if txt_two_done==False:
                bgcolor=[(int)(r*255),(int)(g*255),(int)(b*255),
                         (int)(alpha*255)]
                w,h,w_new,h_new=png_power_two(txt,txt_out,
                                              bgcolor=bgcolor,
                                              verbose=self.verbose)
                if False:
                    txt_dim=(float(w)/float(w_new),
                             float(h)/float(h_new))
                else:
                    txt_dim=(1.0,1.0)
                if self.verbose>1:
                    print('td_mat(): txt_dim:',txt_dim)

        mat=material(name,[r,g,b,alpha],txt=txt_out_base,metal=metal,
                     rough=rough,
                     ds=ds,alpha_mode=alpha_mode,alpha_cutoff=alpha_cutoff,
                     emi_factor=emi_factor)
        
        mat.txt_frac_w=txt_dim[0]
        mat.txt_frac_h=txt_dim[1]
        mat.txt_w=w_new
        mat.txt_h=h_new

        self.to.add_mat(mat)
        
        if self.verbose>0:
            print('td_plot_base::td_mat(): Added material named',mat.name+'.')
            
        return
    
    def td_arrow(self,x1,y1,z1,x2,y2,z2,name='arrow',
                 mat='white',r=0,tail_ratio=0.9,n_theta=20,
                 head_width=3,coords='internal'):
        """Documentation for o2graph command ``td-arrow``:

        Plot an arrow in a 3d visualization (experimental)

        Command-line arguments: ``<x1> <y1> <z1> <x2> <y2> <z2> 
        [kwargs]``

        This command plots and arrow (a combination of a cylinder for
        the body of the arrow and a cone for the head) from point
        (x1,y1,z1) to point (x2,y2,z2). By default, the arrow
        coordinates are specified in the internal coordinate system.
        If the keyword argument ``coords`` is ``user``, then the
        coordinates are in the user coordinate system.

        The fraction of the length of
        the cylinder to the distance between the user-specified points
        is given in ``tail_ratio`` and defaults to 0.9. The value
        ``r`` is the radius of the cylinder, and the base of the code
        has a radius of twice ``r``. If the user-specified value of
        ``r`` is zero or negative, then the default value is used (the
        length of the arrow divided by 80). The argument ``n_theta``
        specifies the number of vertices in the azimuthal direction.
        The total number of faces is always three times ``n_theta``.
        """
        uname=self.to.make_unique_name(name)

        if coords=='user':
            if self.xset==False or self.yset==False or self.zset==False:
                raise ValueError("User coordinates not set in"+
                                 " td_plot_base::td-arrow().")
            x1=(x1-self.xlo)/(self.xhi-self.xlo)
            y1=(y1-self.ylo)/(self.yhi-self.ylo)
            z1=(z1-self.zlo)/(self.zhi-self.zlo)
            x2=(x2-self.xlo)/(self.xhi-self.xlo)
            y2=(y2-self.ylo)/(self.yhi-self.ylo)
            z2=(z2-self.zlo)/(self.zhi-self.zlo)
        
        arr_vert,arr_norm,arr_face=arrow(x1,y1,z1,x2,y2,z2)

        if type(mat)==str:
            
            if not self.to.is_mat(mat):
                if mat=='white':
                    white=material('white',[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('No material named',mat,
                          'in td_plot_base::td_arrow().')
                    return
            if self.verbose>2:
                print('td_plot_base::td_arrow(): creating group named',uname,
                      'with material',mat+'.')
                
            gf=mesh_object(uname,arr_face,mat)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)
            
        else:
            
            if self.verbose>2:
                print('td_plot_base::td_arrow(): creating group named',
                      uname,'with material',mat.name+'.')
            if not self.to.is_mat(mat.name):
                self.to.add_mat(mat)
            gf=mesh_object(uname,arr_face,mat.name)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)

        return

    def td_pgram(self,x1,y1,z1,x2,y2,z2,x3,y3,z3,
                 name='pgram',mat='',force_rect=False,
                 match_txt=False,coords='user'):
        """Documentation for o2graph command ``td-pgram``:

        Plot a parallelogram in a 3D visualization (experimental)

        Command-line arguments: ``<x1> <y1> <z1> <x2> <y2> <z2> 
        <x3> <y3> <z3> [kwargs]``
        """
        uname=self.to.make_unique_name(name)

        if coords=='user':
            if self.xset==False or self.yset==False or self.zset==False:
                raise ValueError("User coordinates not set in"+
                                 " td_plot_base::td_pgram().")
            x1=(x1-self.xlo)/(self.xhi-self.xlo)
            y1=(y1-self.ylo)/(self.yhi-self.ylo)
            z1=(z1-self.zlo)/(self.zhi-self.zlo)
            x2=(x2-self.xlo)/(self.xhi-self.xlo)
            y2=(y2-self.ylo)/(self.yhi-self.ylo)
            z2=(z2-self.zlo)/(self.zhi-self.zlo)
            x3=(x3-self.xlo)/(self.xhi-self.xlo)
            y3=(y3-self.ylo)/(self.yhi-self.ylo)
            z3=(z3-self.zlo)/(self.zhi-self.zlo)

        # Get the material info
        m=self.to.get_mat(mat)
        
        if match_txt:

            if self.verbose>2:
                print('td_pgram(): match_txt is True')
                print('  p2,p3:',x2,y2,z2,x3,y3,z3)

            # Adjust the distance between 1->2 and 3->4 from the LaTeX
            old_height=dist3([x1,y1,z1],[x3,y3,z3])
            old_width=dist3([x1,y1,z1],[x2,y2,z2])

            w_img=m.txt_w*m.txt_frac_w
            h_img=m.txt_h*m.txt_frac_h
            
            if w_img/h_img>old_width/old_height:
                
                # The LaTeX image is wider, so set the new width to
                # the old width and then fix the height to match
                new_width=old_width
                new_height=h_img*old_width/w_img
                
                x3=(x3-x1)*new_height/old_height+x1
                y3=(y3-y1)*new_height/old_height+y1
                z3=(z3-z1)*new_height/old_height+z1
                
            else:
        
                # The LaTeX image is taller, so set the new height to
                # the old height and then fix the width to match
                new_height=old_height
                new_width=w_img*old_height/h_img
                
                x2=(x2-x1)*new_width/old_width+x1
                y2=(y2-y1)*new_width/old_width+y1
                z2=(z2-z1)*new_width/old_width+z1
                
            if self.verbose>2:
                print('td_pgram(): match_txt is True')
                print('  p2,p3 (post):',x2,y2,z2,x3,y3,z3)

        (pgram_vert,pgram_face,
         pgram_norm,pgram_txt)=parallelogram(x1,y1,z1,x2,y2,z2,x3,y3,z3,
                                             mat_name=mat,
                                             verbose=self.verbose,
                                             force_rect=force_rect)

        if self.verbose>2:
            print('td_pgram(): creating group named',uname,
                  'with material',mat+'.')
            
        gf=mesh_object(uname,pgram_face,mat)
        gf.vert_list=pgram_vert
        gf.vn_list=pgram_norm

        # If there is a texture, then add the texture coordinates
        if m.txt!='':

            import copy
            
            txt2=copy.deepcopy(pgram_txt)
            for i in range(0,len(pgram_txt)):
                txt2[i][0]=pgram_txt[i][0]*m.txt_frac_w
                txt2[i][1]=pgram_txt[i][1]*m.txt_frac_h
            gf.vt_list=txt2
            
        self.to.add_object(gf)

        return

    def td_axis_label(self, ldir : str, tex_label : str,
                      tex_mat_name : str = '', end_mat_name: str = 'white',
                      png_file : str = '', group_name : str = '',
                      offset : float = 0.1, height : float = 0.1,
                      flatten : str = 'white'):
        """Documentation for o2graph command ``td-axis-label``:

        Create an axis label in a 3d visualization (experimental).

        Command-line arguments: ``<ldir> <tex_label> [kwargs]``

        Create an axis label in the direction ``ldir`` with label
        ``tex_label``.

        Direction, ``ldir``, must be either ``x``, ``y``, or ``z``.
        The LaTeX image from ``tex_label`` will be stored in file
        named ``png_file``. A new material will be created from the
        LaTeX image, named ``tex_mat_name`` and added to the material
        list before the corresponding mesh is added. If
        ``tex_mat_name`` is empty, then ``mat_xtitle``,
        ``mat_ytitle``, or ``mat_ztitle`` will be used, depending on
        the direction. If ``group_name`` is empty, then ``x_title``,
        ``y_title``, or ``z_title`` will be used, depending on the
        direction.
        
        The material named ``end_mat_name`` will be used for the two
        faces which do not have labels. If ``end_mat_name`` is the
        default, ``white``, then a default white material will be
        created for that purpose. Otherwise, it is presumed the user
        has already added the material.

        The number ``offset`` is the offset of the label from the
        x-axis, in the internal coordinate system. The number
        ``height`` is used for the height dimension of the faces with
        the LaTeX image, and the width is computed automatically from
        the aspect ratio of the LaTeX output.
        """

        if end_mat_name=='white':
            if self.to.is_mat('white')==False:
                white=material('white',[1,1,1])
                self.to.add_mat(white)
        
        if ldir=='x':
            
            if png_file=='':
                png_file='xtitle.png'
            if tex_mat_name=='':
                tex_mat_name='mat_xtitle'
            if group_name=='':
                group_name='x_title'

            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'tex_mat_name:',
                      tex_mat_name,'group_name:',group_name,'flatten:',
                      flatten,type(flatten))

            x_v,x_f,x_t,x_n,x_m=latex_prism(0.5,-offset-height/2.0,
                                            -offset+height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset-height/2.0,
                                            tex_label,
                                            self.td_wdir,png_file,tex_mat_name,
                                            dir=ldir,end_mat=end_mat_name)

            self.to.add_mat(x_m)
            gf=mesh_object(group_name,x_f)
            gf.vert_list=x_v
            gf.vn_list=x_n
            gf.vt_list=x_t
            self.to.add_object(gf)

        elif ldir=='y':
            
            if png_file=='':
                png_file='ytitle.png'
            if tex_mat_name=='':
                tex_mat_name='mat_ytitle'
            if group_name=='':
                group_name='y_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'tex_mat_name:',
                      tex_mat_name,'group_name:',group_name)

            y_v,y_f,y_t,y_n,y_m=latex_prism(-offset-height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset-height/2.0,
                                            tex_label,
                                            self.td_wdir,png_file,tex_mat_name,
                                            dir=ldir,end_mat=end_mat_name)
            
            self.to.add_mat(y_m)
            gf=mesh_object(group_name,y_f)
            gf.vert_list=y_v
            gf.vn_list=y_n
            gf.vt_list=y_t
            self.to.add_object(gf)

        elif ldir=='z':
            
            if png_file=='':
                png_file='ztitle.png'
            if tex_mat_name=='':
                tex_mat_name='mat_ztitle'
            if group_name=='':
                group_name='z_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'tex_mat_name:',
                      tex_mat_name,'group_name:',group_name)
                
            z_v,z_f,z_t,z_n,z_m=latex_prism(-offset-height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset+height/2.0,
                                            -offset-height/2.0,0.5,
                                            tex_label,
                                            self.td_wdir,png_file,tex_mat_name,
                                            dir=ldir,end_mat=end_mat_name)
            
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
    
