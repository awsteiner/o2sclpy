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
import sys

# For os.getenv() and os.path.exists()
import os

# For numpy.bytes_
import numpy

def get_azi_angle(v):
    """
    Return the azimuthal angle in :math:`[0,\\pi]` for a three-element
    vector in Cartesian coordinates.
    """
    x=v[0]
    y=v[1]
    z=v[2]
    # arctan2 returns a number in [-pi,pi]
    phi=numpy.arctan2(y,x)
    return phi

def change_phi(v,phi_new):
    """
    Modify the azimuthal angle of a Cartesian vector, effectively rotating
    it around the z axis.
    """
    x=v[0]
    y=v[1]
    z=v[2]
    r=numpy.sqrt(x*x+y*y+z*z)
    # arccos is always [0,pi]
    theta=numpy.arccos(z/r)
    v[0]=r*numpy.cos(phi_new)*numpy.sin(theta)
    v[1]=r*numpy.sin(phi_new)*numpy.sin(theta)
    # We don't need to change v[2] because it is unchanged by the rotation
    return

def rect_to_spher(v):
    """
    Convert a three-element Cartesian vector to spherical coordinates 
    and return a three-element vector containing the radius, the azimuthal
    angle, and the polar angle (in that order). The azimuthal angle is 
    always in the range :math:`[-\\pi,\\pi]` and the polar angle is 
    always in the range :math:`[0,\\pi]`.
    """
    x=v[0]
    y=v[1]
    z=v[2]
    r=numpy.sqrt(x*x+y*y+z*z)
    # arccos is always [0,pi]
    theta=numpy.arccos(z/r)
    # arctan2 returns a number in [-pi,pi]
    phi=numpy.arctan2(y,x)

    # AWS, 5/21/24: These are just for testing but I've never seen them
    # occur in practice.
    if phi<-numpy.pi or phi>numpy.pi:
        raise ValueError('Problem 1')
    if theta<0 or theta>numpy.pi:
        raise ValueError('Problem 2.')
    
    return [r,phi,theta]

def spher_to_rect(v):
    """
    Desc
    """
    r=v[0]
    theta=v[1]
    phi=v[2]

    x=r*numpy.sin(theta)*numpy.cos(phi)
    y=r*numpy.sin(theta)*numpy.sin(phi)
    z=r*numpy.cos(theta)

    return [x,y,z]

def cross(x,y,norm=False):
    """Return the cross product between two vectors

    If ``norm`` is ``True``, then normalize the cross product to 
    unity before returning it.
    """
    cross=[x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],
           x[0]*y[1]-y[0]*x[1]]
    if norm:
        cross_norm=numpy.sqrt(cross[0]*cross[0]+cross[1]*cross[1]+
                              cross[2]*cross[2])
        cross[0]=cross[0]/cross_norm
        cross[1]=cross[1]/cross_norm
        cross[2]=cross[2]/cross_norm
    return cross

def norm3(x):
    """Normalize the three-element Cartesian vector ``x``."""
    mag=numpy.sqrt(x[0]*x[0]+x[1]*x[1]+x[2]*x[2])
    x[0]=x[0]/mag
    x[1]=x[1]/mag
    x[2]=x[2]/mag
    return

def mag3(x):
    """Return the length of a three-element Cartesian vector ``x``."""
    mag=numpy.sqrt(x[0]*x[0]+x[1]*x[1]+x[2]*x[2])
    return mag

def dist3(x,y):
    """Return the length of the vector representing the difference
    of two three-element Cartesian vectors, ``x``, and ``y``."""
    mag=numpy.sqrt((x[0]-y[0])*(x[0]-y[0])+(x[1]-y[1])*(x[1]-y[1])+
                   (x[2]-y[2])*(x[2]-y[2]))
    return mag

def renorm(x,r):
    """Take the three-element Cartesian vector ``x``, and rescale it
    to ensure that its length is equal to ``r``."""
    mag=numpy.sqrt(x[0]*x[0]+x[1]*x[1]+x[2]*x[2])
    x[0]=r*x[0]/mag
    x[1]=r*x[1]/mag
    x[2]=r*x[2]/mag
    return

def arrow(x1,y1,z1,x2,y2,z2,r=0,tail_ratio=0.9,n_theta=20,
          head_width=3):
    """Create a set of vertices and triangular faces for an
    arrow.

    The tail a cylinder with radius r beginning at (x1,y1,z1) and the
    head is a cone with radius 2r with a point at (x2,y2,z2). The
    variable tail_ratio specifies the length of the cylinder divided
    by the distance between point 1 and point 2. The argument n_theta
    specifies the number of vertices in the azimuthal direction.
    If r is zero or negative, then it is set to the length of the
    arrow divided by 80.

    This function returns a set of three lists, the first is the
    vertices (a list of size n_theta times nine), the second is the
    vertex normals (a list of size n_theta times nine), and the third
    are the faces a list of size n_theta times three). The normal
    vectors always point out away from the axis, except for the single
    vertex at the head of the arrow, which points in the direction of
    the arrow.

    """
    
    # The length of the arrow
    arrow_len=numpy.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

    if r<=0:
        r=arrow_len/80
    
    # The end point of the tail (and the starting point of the head)
    tail_end=[x1+(x2-x1)*tail_ratio,y1+(y2-y1)*tail_ratio,
              z1+(z2-z1)*tail_ratio]
    
    vert=[]
    vn=[]
    face=[]

    # Construct an arbitrary vector not along the arrow's axis
    arb=[1,0,0]
    if y1==y2 and z1==z2:
        arb=[0,1,0]

    # Take the transverse component
    arb=[arb[0]-arb[0]*(x2-x1),
         arb[1]-arb[1]*(y2-y1),
         arb[2]-arb[2]*(z2-z1)]

    # Renormalize to the correct length
    arb_norm=numpy.sqrt(arb[0]*arb[0]+arb[1]*arb[1]+arb[2]*arb[2])
    arb[0]=arb[0]/arb_norm*r
    arb[1]=arb[1]/arb_norm*r
    arb[2]=arb[2]/arb_norm*r

    # The cross product of the arrow's axis with arb
    cross=[(y2-y1)*arb[2]-(z2-z1)*arb[1],
           (z2-z1)*arb[0]-(x2-x1)*arb[2],
           (x2-x1)*arb[1]-(y2-y1)*arb[0]]
    cross_norm=numpy.sqrt(cross[0]*cross[0]+cross[1]*cross[1]+
                          cross[2]*cross[2])
    for j in range(0,3):
        cross[j]=cross[j]/cross_norm*r

    # Handle the tail
    for i in range(0,n_theta):
        theta=float(i)*numpy.pi*2/float(n_theta)
        vert.append([x1+arb[0]*numpy.cos(theta)+
                     cross[0]*numpy.sin(theta),
                     y1+arb[1]*numpy.cos(theta)+
                     cross[1]*numpy.sin(theta),
                     z1+arb[2]*numpy.cos(theta)+
                     cross[2]*numpy.sin(theta)])
        ntmp=[arb[0]*numpy.cos(theta)+
                    cross[0]*numpy.sin(theta),
                    arb[1]*numpy.cos(theta)+
                    cross[1]*numpy.sin(theta),
                    arb[2]*numpy.cos(theta)+
                    cross[2]*numpy.sin(theta)]
        norm3(ntmp)
        vn.append(ntmp)
        vert.append([tail_end[0]+arb[0]*numpy.cos(theta)+
                     cross[0]*numpy.sin(theta),
                     tail_end[1]+arb[1]*numpy.cos(theta)+
                     cross[1]*numpy.sin(theta),
                     tail_end[2]+arb[2]*numpy.cos(theta)+
                     cross[2]*numpy.sin(theta)])
        ntmp=[arb[0]*numpy.cos(theta)+
                   cross[0]*numpy.sin(theta),
                   arb[1]*numpy.cos(theta)+
                   cross[1]*numpy.sin(theta),
                   arb[2]*numpy.cos(theta)+
                   cross[2]*numpy.sin(theta)]
        norm3(ntmp)
        vn.append(ntmp)
        if i!=n_theta-1:
            face.append([2*i+1,2*i+3,2*i+2])
            face.append([2*i+2,2*i+3,2*i+4])
        else:
            face.append([2*i+2,2*i+1,1])
            face.append([2,2*i+2,1])

    # Handle the head
    vert.append([x2,y2,z2])
    ntmp=[x2-x1,y2-y1,z2-z1]
    norm3(ntmp)
    vn.append(ntmp)
    
    point_index=len(vert)
    
#    for j in range(0,3):
#        cross[j]=cross[j]/cross_norm*r*2.0
        
    for i in range(0,n_theta):
        theta=float(i)*numpy.pi*2/float(n_theta)
        vert.append([tail_end[0]+head_width*arb[0]*numpy.cos(theta)+
                     head_width*cross[0]*numpy.sin(theta),
                     tail_end[1]+head_width*arb[1]*numpy.cos(theta)+
                     head_width*cross[1]*numpy.sin(theta),
                     tail_end[2]+head_width*arb[2]*numpy.cos(theta)+
                     head_width*cross[2]*numpy.sin(theta)])
        ntmp=[head_width*arb[0]*numpy.cos(theta)+
                    head_width*cross[0]*numpy.sin(theta),
                    head_width*arb[1]*numpy.cos(theta)+
                    head_width*cross[1]*numpy.sin(theta),
                    head_width*arb[2]*numpy.cos(theta)+
                    head_width*cross[2]*numpy.sin(theta)]
        norm3(ntmp)
        vn.append(ntmp)
        if i==n_theta-1:
            face.append([point_index+i+1,point_index+1,
                         point_index])
        else:
            face.append([point_index+i+1,point_index+i+2,
                         point_index])

    if False:
        print('vert:',len(vert))
        for ki in range(0,len(vert)):
            print('vert %d [%7.6e,%7.6e,%7.6e]' % (ki,vert[ki][0],vert[ki][1],
                                     vert[ki][2]))
        print('vn:',len(vn))
        for ki in range(0,len(vn)):
            print('vn %d [%7.6e,%7.6e,%7.6e]' % (ki,vn[ki][0],vn[ki][1],
                                     vn[ki][2]))
        print('face:')
        for ki in range(0,len(face)):
            print('face %d [%d,%d,%d]' % (ki,face[ki][0],face[ki][1],
                                     face[ki][2]))
    # Rearrange for GLTF
            
    vert2=[]
    norms2=[]
    face2=[]

    for i in range(0,len(face)):

        # Add the vertices to the new vertex array
        vert2.append(vert[face[i][0]-1])
        vert2.append(vert[face[i][1]-1])
        vert2.append(vert[face[i][2]-1])

        norms2.append(vn[face[i][0]-1])
        norms2.append(vn[face[i][1]-1])
        norms2.append(vn[face[i][2]-1])

        face2.append([i*3,i*3+1,i*3+2])

    # Print out results
    if False:
        for ki in range(0,len(vert2),3):
            print('%d [%d,%d,%d]' % (int(ki/3),face2[int(ki/3)][0],
                                             face2[int(ki/3)][1],
                                             face2[int(ki/3)][2]))
            print(('0 [%7.6e,%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki][0],vert2[ki][1],
                                             vert2[ki][2],norms2[ki][0],
                                             norms2[ki][1],norms2[ki][2]))
            print(('1 [%7.6e,%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+1][0],vert2[ki+1][1],
                                             vert2[ki+1][2],norms2[ki+1][0],
                                             norms2[ki+1][1],norms2[ki+1][2]))
            print(('2 [%7.6e,%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+2][0],vert2[ki+2][1],
                                             vert2[ki+2][2],norms2[ki+2][0],
                                             norms2[ki+2][1],norms2[ki+2][2]))
            print('')

        print(len(vert2),len(norms2),len(face2))
        #quit()
            
    return vert2,norms2,face2

def icosphere(x,y,z,r,n_subdiv: int = 0, phi_cut=[0,0]):
    """Construct the vertices and faces of an icosphere centered at
    (x,y,z) with radius r

    This function is based on material from [1]. The icosphere
    is constructed from the corners of three golden rectangles
    aligned along the axes.

    This function returns a set of three lists, the first is the
    vertices, the second are the vertex normals, and the third are the
    faces. The normal vectors always point outwards.

    The phi_cut keyword argument does not yet work.

    [1] https://danielsieger.com/blog/2021/03/27/generating-spheres.html
    """
    import copy

    phi=(1.0+numpy.sqrt(5.0))*0.5
    b=r/phi;
    fact=numpy.sqrt(phi)/(5**0.25)
    
    vert=[]
    vn=[]

    # Start with an icosahedron with each vertex at radius r We use
    # deep copy to ensure the vertexes and normals occupy different
    # memory locations. The vertices, normals and faces are stored
    # here in an '.obj' like format, and then we convert to '.gltf'
    # below.

    # 1
    tmp=[0,b*fact,-r*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 2
    tmp=[b*fact,r*fact,0]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 3
    tmp=[-b*fact,r*fact,0]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 4
    tmp=[0,b*fact,r*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 5
    tmp=[0,-b*fact,r*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 6
    tmp=[-r*fact,0,b*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 7
    tmp=[0,-b*fact,-r*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 8
    tmp=[r*fact,0,-b*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 9
    tmp=[r*fact,0,b*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 10
    tmp=[-r*fact,0,-b*fact]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 11
    tmp=[b*fact,-r*fact,0]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # 12
    tmp=[-b*fact,-r*fact,0]
    vert.append(tmp)
    tmp2=copy.deepcopy(tmp)
    norm3(tmp2)
    vn.append(tmp2)

    # Enumerate the faces
    
    face=[]
    face.append([3,2,1])
    face.append([2,3,4])
    face.append([6,5,4])
    face.append([5,9,4])
    face.append([8,7,1])
    
    face.append([7,10,1])
    face.append([12,11,5])
    face.append([11,12,7])
    face.append([10,6,3])
    face.append([6,10,12])
    
    face.append([9,8,2])
    face.append([8,9,11])
    face.append([3,6,4])
    face.append([9,2,4])
    face.append([10,3,1])
    
    face.append([2,8,1])
    face.append([12,10,7])
    face.append([8,11,7])
    face.append([6,12,5])
    face.append([11,9,5])

    # Subdivide if requested

    for k in range(0,n_subdiv):
        
        face_new=[]
        
        for i in range(0,len(face)):
            i1=face[i][0]
            i2=face[i][1]
            i3=face[i][2]
    
            v12=[(vert[i1-1][k]+vert[i2-1][k])/2 for k in range(0,3)]
            renorm(v12,r)
            vert.append(v12)
            i12=len(vert)
    
            tmp1=copy.deepcopy(v12)
            norm3(tmp1)
            vn.append(tmp1)
                
            v13=[(vert[i1-1][k]+vert[i3-1][k])/2 for k in range(0,3)]
            renorm(v13,r)
            vert.append(v13)
            i13=len(vert)
    
            tmp2=copy.deepcopy(v13)
            norm3(tmp2)
            vn.append(tmp2)
                
            v23=[(vert[i2-1][k]+vert[i3-1][k])/2 for k in range(0,3)]
            renorm(v23,r)
            vert.append(v23)
            i23=len(vert)
    
            tmp3=copy.deepcopy(v23)
            norm3(tmp3)
            vn.append(tmp3)
    
            if False:
                print(len(vert),len(face),i12,i13,i23)
                print(vert[i1-1],vert[i2-1],vert[i3-1])
                print(v12,v13,v23)
                quit()
    
            face_new.append([i1,i12,i13])
            face_new.append([i12,i2,i23])
            face_new.append([i12,i23,i13])
            face_new.append([i3,i13,i23])

        face=face_new

    # If requested, make an azimuthal cutout
    if phi_cut[0]!=phi_cut[1]:
        
        if phi_cut[0]<0 or phi_cut[1]<0:
            raise ValueError('Phi cut values cannot be negative.')
        if phi_cut[0]>numpy.pi*2.0 or phi_cut[1]>numpy.pi*2.0:
            raise ValueError('Phi cut values cannot be larger than 2 pi.')
        if phi_cut[0]>phi_cut[1]:
            temp=phi_cut[0]
            phi_cut[0]=phi_cut[1]
            phi_cut[1]=temp
        phi_mid=(phi_cut[0]+phi_cut[1])/2

        # Delete faces which are only in the cutoff region.
        # This algorithm is 
        
        found=True
        while found==True:
            found=False
            iface=0
            while iface<len(face) and found==False:
                count_low=0
                count_high=0
                j=0
                while j<3 and found==False:
                    phi=get_azi_angle(vert[face[iface][j]-1])
                    if (phi<0.0):
                        phi=phi+numpy.pi*2.0
                    if phi<=phi_mid and phi>phi_cut[0]:
                        count_low=count_low+1
                    if phi>phi_mid and phi<phi_cut[1]:
                        count_high=count_high+1
                    if count_low>0 and count_high>0:
                        del face[iface]
                        found=True
                    j=j+1
                iface=iface+1

        # First pass, determine if we need to shift vertex
        # up or down in phi
        vert_flags=[0]*len(vert)
        for ivert in range(0,len(vert)):
            phi=get_azi_angle(vert[ivert])
            if (phi<0.0):
                phi=phi+numpy.pi*2.0
            if phi<=phi_mid and phi>phi_cut[0]:
                #if vert_flags[ivert]!=0:
                #print('Subtracting from',vert_flags[ivert])
                vert_flags[ivert]=vert_flags[ivert]-1
            if phi>phi_mid and phi<phi_cut[1]:
                #if vert_flags[ivert]!=0:
                #print('Adding to',vert_flags[ivert])
                vert_flags[ivert]=vert_flags[ivert]+1

        for ivert in range(0,len(vert)):
            if vert_flags[ivert]==1:
                change_phi(vert[ivert],phi_cut[1])
            elif vert_flags[ivert]==1:
                change_phi(vert[ivert],phi_cut[0])

    # Create texture coordinates
    texcoord=[]
    for i in range(0,len(vert)):
        tc=rect_to_spher(vert[i])
        xx=tc[1]/numpy.pi/2.0+0.5
        yy=tc[2]/numpy.pi
        texcoord.append([tc[1]/numpy.pi/2.0+0.5,tc[2]/numpy.pi])

    # Shift the origin to the user-specified coordinates
    for i in range(0,len(vert)):
        vert[i][0]=vert[i][0]+x
        vert[i][1]=vert[i][1]+y
        vert[i][2]=vert[i][2]+z

    # Rearrange for GLTF
            
    vert2=[]
    norms2=[]
    face2=[]
    texcoord2=[]

    if False:
        for k in range(0,len(vn)):
            print('k',vn[k])
        print('')

    for i in range(0,len(face)):

        #print(i,face[i][0],face[i][1],face[i][2])
        
        # Add the vertices to the new vertex array
        vert2.append(vert[face[i][0]-1])
        vert2.append(vert[face[i][1]-1])
        vert2.append(vert[face[i][2]-1])

        norms2.append(vn[face[i][0]-1])
        norms2.append(vn[face[i][1]-1])
        norms2.append(vn[face[i][2]-1])

        face2.append([i*3,i*3+1,i*3+2])

        # Add the texture coordinates to the new vertex array
        tx0=copy.deepcopy(texcoord[face[i][0]-1])
        tx1=copy.deepcopy(texcoord[face[i][1]-1])
        tx2=copy.deepcopy(texcoord[face[i][2]-1])

        # This modification helps ensure faces have nearby
        # vertices and avoid texture artifacts on the sphere
        
        debug=False
        #if tx0[1]>0.99 or tx1[1]>0.99 or tx2[1]>0.99:
        #debug=True
        if False:
            print('sx: %d %d %d %7.6e %7.6e %7.6e %7.6e %7.6e %7.6e ' %
                  (face[i][0]-1,face[i][1]-1,face[i][2]-1,
                   tx0[0],tx0[1],tx1[0],tx1[1],tx2[0],tx2[1]))
        if tx0[0]<0.25 and tx1[0]>0.75 and tx2[0]>0.75:
            tx0[0]=tx0[0]+1.0
            if debug:
                print('1')
        elif tx0[0]>0.75 and tx1[0]<0.25 and tx2[0]<0.25:
            tx0[0]=tx0[0]-1.0
            if debug:
                print('2')
        elif tx1[0]<0.25 and tx0[0]>0.75 and tx2[0]>0.75:
            tx1[0]=tx1[0]+1.0
            if debug:
                print('3')
        elif tx1[0]>0.75 and tx0[0]<0.25 and tx2[0]<0.25:
            tx1[0]=tx1[0]-1.0
            if debug:
                print('4')
        elif tx2[0]<0.25 and tx0[0]>0.75 and tx1[0]>0.75:
            tx2[0]=tx2[0]+1.0
            if debug:
                print('5')
        elif tx2[0]>0.75 and tx0[0]<0.25 and tx1[0]<0.25:
            tx2[0]=tx2[0]-1.0
            if debug:
                print('6')
        if debug:
            print('tx: %7.6e %7.6e %7.6e %7.6e %7.6e %7.6e ' %
                  (tx0[0],tx0[1],tx1[0],tx1[1],tx2[0],tx2[1]))
            
        texcoord2.append([tx0[0],tx0[1]])
        texcoord2.append([tx1[0],tx1[1]])
        texcoord2.append([tx2[0],tx2[1]])
        
    if False:
        for k in range(0,len(norms2)):
            print('k',norms2[k])
    
    # Print out results
    if False:
        print('x,y,z,r:',x,y,z,r)
        print('index face[index][0,1,2]')
        print('  0 vert norm')
        print('  1 vert norm')
        print('  2 vert norm')
        for ki in range(0,len(vert2),3):
            print('%d [%d,%d,%d]' % (int(ki/3),face2[int(ki/3)][0],
                                     face2[int(ki/3)][1],
                                     face2[int(ki/3)][2]))
            print(('0 [%7.6e,%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki][0],vert2[ki][1],
                                             vert2[ki][2],norms2[ki][0],
                                             norms2[ki][1],norms2[ki][2]))
            print(('1 [%7.6e,%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+1][0],vert2[ki+1][1],
                                             vert2[ki+1][2],norms2[ki+1][0],
                                             norms2[ki+1][1],norms2[ki+1][2]))
            print(('2 [%7.6e,%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+2][0],vert2[ki+2][1],
                                             vert2[ki+2][2],norms2[ki+2][0],
                                             norms2[ki+2][1],norms2[ki+2][2]))
            # xtmp=[vert2[ki][0],vert2[ki][1],vert2[ki][2]]
            # ytmp=[vert2[ki+1][0],vert2[ki+1][1],vert2[ki+1][2]]
            # ztmp=[vert2[ki+2][0],vert2[ki+2][1],vert2[ki+2][2]]
            # print('d1 %7.6e' % (numpy.sqrt((xtmp[0]-ytmp[0])**2+
            #                                (xtmp[1]-ytmp[1])**2+
            #                                (xtmp[2]-ytmp[2])**2)))
            # print('d2 %7.6e' % (numpy.sqrt((ztmp[0]-ytmp[0])**2+
            #                                (ztmp[1]-ytmp[1])**2+
            #                                (ztmp[2]-ytmp[2])**2)))
            # print('d3 %7.6e' % (numpy.sqrt((xtmp[0]-ztmp[0])**2+
            #                                (xtmp[1]-ztmp[1])**2+
            #                                (xtmp[2]-ztmp[2])**2)))
            print('')

        print(len(vert2),len(norms2),len(face2))
        #quit()
        
    return vert2,norms2,face2,texcoord2
    
def cpp_test(x):
    """
    Desc
    """
    return x*numpy.pi

def remove_spaces(string : str):
    """
    Remove spaces at the beginning specified string and return the 
    result.

    This function is in ``utils.py``.
    """
    while len(string)>0 and string[0]==' ':
        string=string[1:]
    return string

def string_to_color(str_in : str):
    """
    Convert a string to a color, either ``(r,g,b)`` to an RGB color
    or ``[r,g,b,a]`` to an RGBA color.
    """

    if str_in[0]=='(':
        temps=str_in[1:len(str_in)-1]
        temp2=temps.split(',')
        return (float(temp2[0]),float(temp2[1]),float(temp2[2]))
    elif str_in[0]=='[':
        temps=str_in[1:len(str_in)-1]
        temp2=temps.split(',')
        return [float(temp2[0]),float(temp2[1]),float(temp2[2]),
                float(temp2[3])]
    
    return str_in

def if_yt_then_Agg(backend : str, argv):
    """
    Determine if yt commands are present, and if found, then automatically
    convert to the Agg backend.
    """
            
    yt_found=False
    for i in range(1,len(argv)):
        if argv[i][0:4]=='-yt-' and yt_found==False:
            if backend!='' and backend!='agg' and backend!='Agg':
                print('Backend was not set to Agg but yt '+
                      'commands were found.')
            yt_found=True
            backend='Agg'
    return backend

def is_number(s: str):
    """
    Return true if 's' is likely a number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def force_bytes(obj):
    """
    This function returns the bytes object corresponding to ``obj``
    in case it is a string using UTF-8. 
    """
    if isinstance(obj,numpy.bytes_)==False and isinstance(obj,bytes)==False:
        return bytes(obj,'utf-8')
    return obj

def force_string(obj):
    """
    This function returns the bytes object corresponding to ``obj``
    in case it is a string using UTF-8. 
    """
    if isinstance(obj,numpy.bytes_)==True or isinstance(obj,bytes)==True:
        return obj.decode('utf-8')
    return obj


def png_power_two(png_input: str, png_output: str, bgcolor=[0,0,0,0],
                  verbose: int = 0, flatten: bool = False,
                  resize: bool = True):
    """Read a PNG image from ``png_input``, resize it to ensure the width
    and height are both a power of two, and store the resulting file
    in ``png_output``.

    This function returns a tuple of four numbers, the width and
    height of the usable part of the image and the width and height of
    the full image. The latter two numbers are always a power of two.

    This function uses the Pillow python package to determine the
    original width and height and perform the resizing. If the width
    and height are already both a power of two, then the file is
    simply copied, unless the input and output filenames are the same,
    in which case this function does nothing. If the input and output
    filenames are the same, and the width and height are not a power
    of two, then this function will throw an exception to help prevent
    the user from inadvertently overwriting the original file. This
    function always overwrites the output file when the input and
    output filenames are different.

    When resize is True, the image is resized to fit the new width
    and height. When resize is False, then the original image is
    centered in the new canvas, and the canvas is filled with the
    background color.

    If flatten is True and bgcolor[3] is non-zero,
    then any pixels with alpha=0 are replaced with bgcolor. This
    is particularly useful for pngs created by the latex_to_png()
    function.

    The background color argument should consist of integers from 0 to
    255. The default background color is transparent black.

    If verbose is greater than 1, then several details are written to 
    stdout.

    """
    import tempfile
    from PIL import Image
    
    if verbose>1:
        print('png_power_two(): png_input, png_output:',
              png_input,png_output)
        
    if os.path.isfile(png_input)==False:
        raise ValueError('In function png_power_two(): String '+
                         png_input+' does not appear to refer to a file.')

    img=Image.open(png_input)
    
    w=img.width
    h=img.height
    w_new=2**(int(numpy.log2(w-1))+1)
    h_new=2**(int(numpy.log2(h-1))+1)
    if verbose>1:
        print('png_power_two(): w, h, w_new, h_new:',w,h,w_new,h_new)

    wadj=w+(w%2)
    hadj=h+(h%2)
    
    odd=False
    if w%2==1 or h%2==1:
        odd=True
        
    # If these are all equal, there is nothing to do
    if w_new==w and h_new==h and odd==False:

        # No resizing required and the files are the same
        if png_input==png_output:
            if verbose>1:
                print('png_power_two(): Skipping.')
            return w,h,w,h
        
        # No resizing required, so just copy
        cmd='cp '+png_input+' '+png_output
        if verbose>1:
            print('png_power_two(): Running shell command to copy:',cmd)
        os.system(cmd)

    if png_input==png_output:
        raise ValueError('In function png_power_two(): Resizing '+
                         'appears to be required, but the input and ouput '+
                         'filenames are the same.')

    if resize:
        
        if verbose>1:
            print('png_power_two(): resizing to',w_new,'by',h_new)
        img_new=img.resize((w_new,h_new))
        wadj=w_new
        hadj=h_new

        # If we're going to flatten the image below, we need
        # to convert modes
        if flatten and bgcolor[3]!=0:
            img_new=img_new.convert('RGBA')
        
    else:
        
        if verbose>1:
            print('png_power_two(): padding image edges')
        # Use Pillow to resize the image, giving new pixels the color
        # specified in bgcolor
        img_new=Image.new('RGBA',(w_new,h_new),
                          ('rgba('+str(bgcolor[0])+','+str(bgcolor[1])+','+
                           str(bgcolor[2])+','+str(bgcolor[3])+')'))

        # Ensure the image is centered
        img_new.paste(img,(int((w_new-w)/2),int((h_new-h)/2)))

    # If requested, flatten all transparent pixels
    if flatten and bgcolor[3]!=0:
        
        dat=img_new.getdata()
        dat_new=[]
        for px in dat:
            # Convert transparent pixels to the specified background
            # color
            if px[3]==0:
                dat_new.append((bgcolor[0],bgcolor[1],bgcolor[2],
                                bgcolor[3]))
            else:
                dat_new.append(px)
        img_new.putdata(dat_new)

    # Save the new image in the output PNG file
    img_new.save(png_output)
    
    return wadj,hadj,w_new,h_new

def cmap_to_png(cmap: str, png_file: str, verbose: int = 0):
    """
    Convert a cmap to a png file which is 2 pixels high and
    256 pixels wide and store it in ``png_file``. 
    """

    from PIL import Image
    import matplotlib.cm as cm
    from matplotlib.colors import Normalize
    import matplotlib.pyplot as plot
    
    img=Image.new('RGBA',(256,2))

    color_map=cm.get_cmap(cmap)
    norm=plot.Normalize(0,255)
    
    dat=[]
    for i in range(0,512):

        ifl=float(i%256)/255.0
        rgb=color_map(ifl)[:3]
        dat.append((int(255*rgb[0]),int(255*rgb[1]),
                    int(255*rgb[2]),255))

    img.putdata(dat)
    img.save(png_file)
            
    return
    
def latex_to_png(tex: str, png_file: str, verbose: int = 0,
                 packages = []):
    """A simple routine to convert a LaTeX string to a png image.

    Math mode is not assumed, so equations may need to be surrounded
    by dollar signs. A temporary file is created, and then that file
    is processed by ``pdflatex`` and then the output is renamed to the
    filename specified by the user with ``mv``. 

    The standalone LaTeX package is used to make png, and the default
    background is transparent, but the antialiasing used to render the
    equations means that only white backgrounds work without creating
    edge effects. The additional LaTeX packages listed in ``packages``
    are loaded with the ``usepackage`` LaTeX command. A common use-case
    is to load the color package to get colored LaTeX output.

    The destination file ``png_file`` will be silently overwritten
    if it is already present.
    """
    import tempfile

    if verbose>1:
        print('latex_to_png(): Converting',tex,
              '\n  to png file',png_file)

    # Create the LaTeX file
    f=tempfile.NamedTemporaryFile(suffix='.tex',delete=False)
    tex_file_name=f.name

    # Fill the LaTeX file with the correct source code
    f.write(force_bytes('\\documentclass[crop,border=0.5pt,'+
                        'convert={outext=.png}]{standalone}\n'))
    for i in range(0,len(packages)):
        f.write(force_bytes('\\usepackage{'+packages[i]+'}\n'))
    f.write(force_bytes('\\begin{document}\n'))
    f.write(force_bytes(tex+'\n'))
    f.write(force_bytes('\\end{document}\n'))
    f.close()

    # Create a file to store the pdflatex output
    f2=tempfile.NamedTemporaryFile(suffix='.out',delete=False)
    out_file_name=f2.name
    f2.close()
    
    tdir=os.path.dirname(tex_file_name)
    tfile=os.path.basename(tex_file_name)
    
    cmd1=('cd '+tdir+' && pdflatex --shell-escape '+tfile+' > '+
          out_file_name+' 2>&1')
    if verbose>1:
        print('latex_to_png(): Running first shell command:\n  ',cmd1)
    os.system(cmd1)

    cmd2='mv '+tex_file_name[:-4]+'.png '+png_file
    if verbose>1:
        print('latex_to_png(): Running second shell command:\n  ',cmd2)
    os.system(cmd2)

    return

def default_plot(left_margin=0.14,bottom_margin=0.12,
                 right_margin=0.04,top_margin=0.04,fontsize=16,
                 fig_size_x=6.0,fig_size_y=6.0,ticks_in=False,
                 rt_ticks=False,editor=False):
    
    import matplotlib.pyplot as plot

    """
    This function sets up the O2sclpy ``matplotlib``
    defaults. It returns a pair of objects, the figure object and axes
    object. The fontsize argument times 0.8 is used 
    for the size of the font labels. Setting the ``ticks_in`` argument
    to ``True`` makes the ticks point inwards instead of outwards
    and setting ``rt_ticks`` to ``True`` puts ticks (but not labels)
    on the right and top edges of the plot. 
    
    This function is in ``utils.py``.
    """
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')
    plot.rcParams['lines.linewidth']=0.5
    
    if editor:
        
        fig=plot.figure(1,figsize=(fig_size_x*2,fig_size_y))
        fig.set_facecolor('white')
        
        ax_left_panel=plot.axes([0,0,0.5,1],facecolor=(1,1,1,0),
                                autoscale_on=False)
        ax_left_panel.margins(x=0,y=0)
        ax_left_panel.axis('off')
        
        ax_right_panel=plot.axes([0.5,0,0.5,1],facecolor=(0.9,0.9,0.9,1),
                                 autoscale_on=False)
        ax_right_panel.margins(x=0,y=0)
        ax_right_panel.get_xaxis().set_visible(False)
        ax_right_panel.get_yaxis().set_visible(False)
        ax=plot.axes([left_margin/2.0,bottom_margin,
                           (1.0-left_margin-right_margin)/2,
                           1.0-top_margin-bottom_margin])
    else:
        
        fig=plot.figure(1,figsize=(fig_size_x,fig_size_y))
        fig.set_facecolor('white')
        
        ax=plot.axes([left_margin,bottom_margin,
                      1.0-left_margin-right_margin,
                      1.0-top_margin-bottom_margin])
        
    ax.minorticks_on()
    # Make the ticks longer than default
    ax.tick_params('both',length=12,width=1,which='major')
    ax.tick_params('both',length=5,width=1,which='minor')
    ax.tick_params(labelsize=fontsize*0.8)
    plot.grid(False)

    if editor:
        return (fig,ax,ax_left_panel,ax_right_panel)
    
    return (fig,ax)
    
def get_str_array(dset):
    """
    Extract a string array from O2scl HDF5 dataset ``dset``
    as a python list

    This function is in ``utils.py``.
    """
    nw=dset['nw'][0]
    nc=dset['nc'][0]
    data=dset['data']
    counter=dset['counter']
    char_counter=1
    word_counter=0
    list=[]
    col=''
    for ix in range(0,nc):
        # Skip empty strings in the array
        done=0
        while done==0:
            if word_counter==nw:
                done=1
            elif counter[word_counter]==0:
                word_counter=word_counter+1
                list.append('')
            else:
                done=1
        col=col+str(chr(data[ix]))
        if char_counter==counter[word_counter]:
            list.append(col)
            col=''
            word_counter=word_counter+1
            char_counter=1
        else:
            char_counter=char_counter+1
    # We're done with the characters, but there are some blank
    # strings left. Add the appropriate blanks at the end.
    while word_counter<nw:
        list.append('')
        word_counter=word_counter+1
    return list

def parse_arguments(argv,verbose=0):
    """
    Old command-line parser (this is currently unused and
    it's not clear if it will be useful in the future).

    This function is in ``utils.py``.
    """
    list=[]
    unproc_list=[]
    if verbose>1:
        print('Number of arguments:', len(argv), 'arguments.')
        print('Argument List:', str(argv))
    ix=1
    while ix<len(argv):
        if verbose>1:
            print('Processing index',ix,'with value',argv[ix],'.')
        # Find first option, at index ix
        initial_ix_done=0
        while initial_ix_done==0:
            if ix==len(argv):
                initial_ix_done=1
            elif argv[ix][0]=='-':
                initial_ix_done=1
            else:
                if verbose>1:
                     print('Adding',argv[ix],' to unprocessed list.')
                unproc_list.append(argv[ix])
                ix=ix+1
        # If there is an option, then ix is its index
        if ix<len(argv):
            list_one=[]
            # Strip single and double dashes
            cmd_name=argv[ix][1:]
            if cmd_name[0]=='-':
                cmd_name=cmd_name[1:]
            # Add command name to list
            list_one.append(cmd_name)
            if verbose>1:
                print('Found option',cmd_name,'at index',ix)
            # Set ix_next to the next option, or to the end if
            # there is no next option
            ix_next=ix+1
            ix_next_done=0
            while ix_next_done==0:
                if ix_next==len(argv):
                    ix_next_done=1
                elif argv[ix_next][0]=='-':
                    ix_next_done=1
                else:
                    if verbose>1:
                        print('Adding '+argv[ix_next]+' with index '+
                              str(ix_next)+' to list for '+cmd_name)
                    list_one.append(argv[ix_next])
                    ix_next=ix_next+1
            list.append(list_one)
            ix=ix_next
    return (list,unproc_list)

def string_to_dict2(s,list_of_ints=[],list_of_floats=[],list_of_bools=[],
                    list_of_colors=[]):
    """
    Convert a string to a dictionary, converting strings to 
    values when necessary.

    This function is in ``utils.py``.
    """
        
    # First split into keyword = value pairs
    arr_old=s.split(',')
    # Create empty dictionary
    dct={}

    if len(s)==0:
        return dct

    # Go through the array and combine adjacent terms if they're
    # part of a bracketed section
    arr=[]
    count=0
    temps=''
    for i in range(0,len(arr_old)):
        for j in range(len(arr_old[i])):
            if arr_old[i][j]=='[':
                count=count+1
            if arr_old[i][j]==']':
                count=count-1
        if len(temps)==0:
            temps=arr_old[i]
        else:
            temps=temps+','+arr_old[i]            
        if count==0:
            arr.append(temps)
            temps=''
        #print('s',s,'arr_old[i]',arr_old[i],'count',
        #count,'temps x'+temps+'x')
    if len(temps)>0:
        arr.append(temps)
    #print('arr:',arr)
    #quit()

    i=0
    done=False
    while done==False:

        # For each pair, split keyword and value.
        arr2=arr[i].split('=')
        if len(arr2)<2:
            print('Failed to find an assignment in string_to_dict2() ',
                  'argument.')
            print('  arr_old:',arr_old)
            print('  arr:',arr)
            print('  arr2:',arr2)
            quit()
            raise ValueError('Failed to find an assignment in ',
                             'string_to_dict2() argument.')
        
        # Remove preceeding and trailing whitespace from the
        # keywords (not for the values)
        while arr2[0][0].isspace():
            arr2[0]=arr2[0][1:]
        while arr2[0][len(arr2[0])-1].isspace():
            arr2[0]=arr2[0][:-1]

        # Remove quotes if necessary
        if len(arr2)>1 and len(arr2[1])>2:
            if arr2[1][0]=='\'' and arr2[1][len(arr2[1])-1]=='\'':
                arr2[1]=arr2[1][1:len(arr2[1])-1]
            if arr2[1][0]=='"' and arr2[1][len(arr2[1])-1]=='"':
                arr2[1]=arr2[1][1:len(arr2[1])-1]

        if arr2[0] in list_of_ints:
            arr2[1]=int(arr2[1])
        if arr2[0] in list_of_floats:
            arr2[1]=float(arr2[1])
        if arr2[0] in list_of_bools:
            if arr2[1].lower() in ['true', '1', 't', 'y', 'yes']:
                arr2[1]=True
            else:
                arr2[1]=False
        if arr2[0] in list_of_colors:
            # Handle the case of a parenthesis, presumed to be
            # (r,g,b)
            if arr2[1].find('(')!=-1:
                if False:
                    print('()arr_old:',arr_old)
                    print('arr2[0]:',arr2[0])
                    print('arr2[1]:',arr2[1])
                arr2[1]=(float(arr2[1][arr2[1].find('(')+1:]),
                         float(arr[i+1]),
                         float(arr[i+2][:arr[i+2].find(')')]))
                i=i+2
                if False:
                    print('()arr2[1]:',type(arr2[1]),arr2[1])
            # Handle the case of a square bracket, presumed to be
            # [r,g,b,a]
            elif arr2[1].find('[')!=-1:
                if False:
                    print('[]arr_old:',arr_old)
                    print('arr2[0]:',arr2[0])
                    print('arr2[1]:',arr2[1])
                arr2[1]=arr2[1][arr2[1].find('[')+1:
                                 arr2[1].find(']')].split(',')
                arr2[1]=[float(arr2[1][0]),
                         float(arr2[1][1]),
                         float(arr2[1][2]),
                         float(arr2[1][3])]
                if False:
                    print('[]arr2[1]:',type(arr2[1]),arr2[1])

        dct[arr2[0]]=arr2[1]

        i=i+1
        if i>=len(arr):
            done=True

    return dct

def string_to_dict(s):
    """
    Convert a string to a dictionary, with extra processing for
    colors, subdictionaries, and matplotlib keyword arguments which
    are expected to have integer or floating point values.

    This function is in ``utils.py``.
    """

    # Slowly converting this to the new function
    return string_to_dict2(s,list_of_floats=['zorder','lw','linewidth',
                                             'elinewidth','alpha',
                                             'fig_size_x','fig_size_y',
                                             'left_margin','right_margin',
                                             'top_margin','bottom_margin',
                                             'left','right','top',
                                             'bottom','wspace','hspace',
                                             'font','scale','dpi',
                                             'capsize','capthick',
                                             'rotation','fontsize',
                                             'labelsize','headlength',
                                             'headwidth','width',
                                             'shrink'],
                          list_of_bools=['sharex','lolims','reorient',
                                         'uplims','xlolims','xuplims',
                                         'sharey','squeeze','fill',
                                         'ticks_in','rt_ticks',
                                         'pcm'],
                           list_of_ints=['shrinkA','shrinkB','bins'],
                           list_of_colors=['color','c','textcolor',
                                           'edgecolor','facecolor','fc',
                                           'ec','markerfacecolor','mfc',
                                           'markeredgecolor','mec',
                                           'markerfacecoloralt','mfcalt',
                                           'ecolor'])

class terminal_py:
    """
    Handle vt100 formatting sequences
    """
    
    redirected=False
    """
    If true, then the output is being redirected to a file, so 
    don't use the formatting sequences
    """
    
    def __init__(self):
        """
        Determine if the output is being redirected or not
        """
        if sys.stdout.isatty()==False:
            self.redirected=True
        return
    
    def cyan_fg(self):
        """
        Set the foreground color to cyan
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[36m'
        return strt
    
    def red_fg(self):
        """
        Set the foreground color to red
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[31m'
        return strt
    
    def magenta_fg(self):
        """
        Set the foreground color to magenta
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[35m'
        return strt
    
    def green_fg(self):
        """
        Set the foreground color to green
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[32m'
        return strt
    
    def bold(self):
        """
        Set the face to bold
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[1m'
        return strt
    
    def default_fgbg(self):
        """
        Set the foreground color to the default
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[m'
        return strt
    
    def horiz_line(self):
        """
        Return a string which represents a horizontal line. If possible,
        vt100-like terminal sequences are used to create a line.
        Otherwise, dashes are used.
        """
        str_line=''
        if self.redirected:
            for jj in range(0,78):
                str_line+='-'
        else:
            str_line=str_line+chr(27)+'(0'
            for jj in range(0,78):
                str_line+='q'
            str_line=str_line+chr(27)+'(B'
        return str_line

    def type_str(self,strt,amt):
        return (force_string(amt.get_type_color())+strt+
                force_string(amt.get_default_color()))
    
    def cmd_str(self,strt,amt):
        return (force_string(amt.get_command_color())+strt+
                force_string(amt.get_default_color()))
    
    def topic_str(self,strt,amt):
        return (force_string(amt.get_help_color())+strt+
                force_string(amt.get_default_color()))
    
    def var_str(self,strt,amt):
        return (force_string(amt.get_param_color())+strt+
                force_string(amt.get_default_color()))

def length_without_colors(strt : str):
    """
    Compute the length of strt, ignoring characters which correspond
    to VT100 formatting sequences
    """
    count=0
    index=0
    while index<len(strt):
        if strt[index]!=chr(27):
            count=count+1
        elif index+2<len(strt) and strt[index+1]=='[' and strt[index+2]=='m':
            # default_fgbg case
            index=index+2
        elif index+3<len(strt) and strt[index+1]=='[' and strt[index+3]=='m':
            # underline, lowint, bold case
            index=index+3
        elif index+4<len(strt) and strt[index+1]=='[' and strt[index+4]=='m':
            # red_fg, blue_fg, etc. case
            index=index+4
        elif index+2<len(strt) and strt[index+1]=='(' and strt[index+2]=='0':
            # alt font case
            index=index+2
        elif index+2<len(strt) and strt[index+1]=='(' and strt[index+2]=='B':
            # normal font case
            index=index+2
        elif (index+8<len(strt) and strt[index+1]=='[' and
              (strt[index+2]=='3' or strt[index+2]=='4') and
              strt[index+3]=='8' and strt[index+4]==';' and
              strt[index+5]=='5' and strt[index+6]==';' and
              strt[index+8]=='m'):
            # eight bit fg/bg case with single digit color
            index=index+8
        elif (index+9<len(strt) and strt[index+1]=='[' and
              (strt[index+2]=='3' or strt[index+2]=='4') and
              strt[index+3]=='8' and strt[index+4]==';' and
              strt[index+5]=='5' and strt[index+6]==';' and
              strt[index+9]=='m'):
            # eight bit fg/bg case with double digit color
            index=index+9
        elif (index+10<len(strt) and strt[index+1]=='[' and
              (strt[index+2]=='3' or strt[index+2]=='4') and
              strt[index+3]=='8' and strt[index+4]==';' and
              strt[index+5]=='5' and strt[index+6]==';' and
              strt[index+10]=='m'):
            # eight bit fg/bg case with triple digit color
            index=index+10
        index=index+1
    return count
            
def wrap_line(line : str, ncols=79):
    """
    From a string 'line', create a list of strings which adds return
    characters in order to attempt to ensure each line is less than
    or equal to ncols characters long. This function also respects
    explicit carriage returns, ensuring they force a new line 
    independent of the line length. This function uses the
    'length_without_colors()' function above, to ensure VT100 formatting
    sequences aren't included in the count.
    """
    list=[]
    # First, just split by carriage returns
    post_list=line.split('\n')
    for i in range(0,len(post_list)):
        # If this line is already short enough, then just handle
        # it directly below
        if length_without_colors(post_list[i])>ncols:
            # A temporary string which will hold the current line
            strt=''
            # Now split by spaces
            post_word=post_list[i].split(' ')
            # Proceed word by word
            for j in range(0,len(post_word)):
                # If the current word is longer than ncols, then
                # clear the temporary string and add it to the list
                if length_without_colors(post_word[j])>ncols:
                    if length_without_colors(strt)>0:
                        list.append(strt)
                    list.append(post_word[j])
                    strt=''
                elif (length_without_colors(strt)+
                      length_without_colors(post_word[j])+1)>ncols:
                    # Otherwise if the next word will take us over the
                    # limit
                    list.append(strt)
                    strt=post_word[j]
                elif len(strt)==0:
                    strt=post_word[j]
                else:
                    strt=strt+' '+post_word[j]
            # If after the last word we still have anything in the
            # temporary string, then add it to the list
            if length_without_colors(strt)>0:
                list.append(strt)
        else:
            # Now if the line was already short enough, add it
            # to the list
            list.append(post_list[i])
                
    return list
            
def string_equal_dash(str1 : str, str2 : str):
    """
    Desc
    """
    b1=force_bytes(str1)
    b2=force_bytes(str2)
    for i in range(0,len(b1)):
        if b1[i]==b'-':
            b1[i]=b'-'
    for i in range(0,len(b2)):
        if b2[i]==b'-':
            b2[i]=b'-'
    if b1==b2:
        return True
    return False

def screenify_py(tlist, ncols : int = 79):
    """
    Desc
    """
    maxlen=0
    for i in range(0,len(tlist)):
        if length_without_colors(tlist[i])>maxlen:
            maxlen=length_without_colors(tlist[i])
    # Add to ensure there is at least one space between columns
    maxlen=maxlen+1
    ncolumns=int(ncols/maxlen)
    nrows=int(len(tlist)/ncolumns)
    while nrows*ncolumns<len(tlist):
        nrows=nrows+1
    output_list=[]
    for i in range(0,nrows):
        row=''
        for j in range(0,ncolumns):
            if i+j*nrows<len(tlist):
                colt=tlist[i+j*nrows]
                while length_without_colors(colt)<maxlen:
                    colt=colt+' '
                row=row+colt
        output_list.append(row)
    return output_list
