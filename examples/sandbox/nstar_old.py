import numpy
import o2sclpy
import random

"""
Plot the magnetic field

This is a pure dipole field given by 

\vec{B} = 3 \vec{r} (m dot r)/r^5 - \vec{m}/r^3
"""
def mag_field(r,theta,phi):
    [rx,ry,rz]=o2sclpy.spher_to_rect([r,theta,phi])
    
    mx=0.5
    my=-0.5
    fact=40
    N=10
    # vector field
    rmag=r
    dot=mx*rx+my*ry
    Bx=(3*rx*dot/rmag**5-mx/rmag**3)/fact
    By=(3*ry*dot/rmag**5-my/rmag**3)/fact
    Bz=(3*rz*dot/rmag**5-my/rmag**3)/fact
    return [Bx,By,Bz]

og=o2sclpy.o2graph_plotter()

og.xlimits(0,1)
og.ylimits(0,1)
og.zlimits(0,1)
og.td_wdir='gltf'

for i in range(0,20):
    og.td_mat('lt_blue_'+str(i),0.8+0.2*float(i)/19.0,
              0.8+0.2*float(i)/19.0,1.0,
              alpha=1.0,metal=1.0,rough=1.0,
              ds=True)
og.td_icos([0.5,0.5,0.5],n_subdiv=2,r=0.5,mat='lt_blue_0')
dtheta=0.1

for i in range(0,20):
    r=random.random()*0.2+0.5
    phi=random.random()*2.0*numpy.pi
    theta=(random.random()*2.0-1.0)
    [lx,ly,lz]=o2sclpy.spher_to_rect([r,theta,phi])
    if theta>0:
        theta=theta**(0.5)*numpy.pi/2.0
    else:
        theta=-(((-theta)**(0.5))*numpy.pi/2.0)
    print('r,phi,theta %7.6e %7.6e %7.6e ' % (r,phi,theta))
    theta2=theta+dtheta*(random.random()*2.0-1.0)
    if theta2>numpy.pi/2.0:
        theta2=numpy.pi/2.0
    if theta2<-numpy.pi/2.0:
        theta2=-numpy.pi/2.0
    [Bx1,By1,Bz1]=mag_field(r,theta,phi)
    [Bx2,By2,Bz2]=mag_field(r,theta2,phi)
    Bx1=Bx1+0.5
    By1=By1+0.5
    Bz1=Bz1+0.5
    Bx2=Bx2+0.5
    By2=By2+0.5
    Bz2=Bz2+0.5
    col='lt_blue_'+str(int(random.random()*19.999))
    og.td_cyl(Bx1,By1,Bz1,Bx2,By2,Bz2,0.01,mat=col)
    
og.to.write_gltf('gltf','nstar')    
