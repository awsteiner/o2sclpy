#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023, Andrew W. Steiner
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
import o2sclpy
import numpy
import random

def test_kde1():
    """ 
    test with transform='none'
    """
    
    N=200
    x=numpy.zeros((N,2))
    for i in range(0,N):
        if i%2==0:
            x[i,0]=0.7+0.1*random.random()
            x[i,1]=0.5+0.1*random.random()
        else:
            x[i,0]=-0.7+0.1*random.random()
            x[i,1]=0.2+0.1*random.random()
    
    ks=o2sclpy.kde_sklearn()
    ks.set_data(x,numpy.logspace(-3,3,100),verbose=2,transform='none')
    print('bw',ks.get_bandwidth())
    for i in range(0,10):
        s=ks.sample()
        print(s[0],s[1])
    print(ks.log_pdf([-0.7,0.2]))
    print(ks.log_pdf([0,0]))
    print(ks.log_pdf([0.7,0.5]))

    return

def test_kde2():
    """
    test baseline model
    """
    
    N=200
    x=numpy.zeros((N,2))
    for i in range(0,N):
        if i%2==0:
            x[i,0]=9000*(0.7+0.1*random.random())
            x[i,1]=90*(0.5+0.1*random.random())
        else:
            x[i,0]=9000*(-0.7+0.1*random.random())
            x[i,1]=90*(0.2+0.1*random.random())
    
    ks=o2sclpy.kde_sklearn()
    ks.set_data(x,numpy.logspace(-3,3,100),verbose=2)
    print('bw',ks.get_bandwidth())
    for i in range(0,10):
        s=ks.sample()
        print(s[0],s[1])
    print(ks.log_pdf([-6300,18]))
    print(ks.log_pdf([0,0]))
    print(ks.log_pdf([6300,45]))

    return

def test_kde3():
    """
    test with scott bandwidth
    """
    
    N=200
    x=numpy.zeros((N,2))
    for i in range(0,N):
        if i%2==0:
            x[i,0]=9000*(0.7+0.1*numpy.sin(float(i*1e4)))
            x[i,1]=90*(0.5+0.1*numpy.cos(float(i*1e4)))
        else:
            x[i,0]=9000*(-0.7+0.1*numpy.sin(float(i*1e4)))
            x[i,1]=90*(0.2+0.1*numpy.cos(float(i*1e4)))
    
    ks=o2sclpy.kde_sklearn()
    ks.set_data(x,numpy.logspace(-3,3,100),verbose=2,bandwidth='scott')
    print('bw',ks.get_bandwidth())
    for i in range(0,10):
        s=ks.sample()
        print(s[0],s[1])
    print(ks.log_pdf([-6300,18]))
    print(ks.log_pdf([0,0]))
    print(ks.log_pdf([6300,45]))

    return

def test_kde4():
    """
    test scipy KDE
    """
    
    N=200
    x=numpy.zeros((N,2))
    for i in range(0,N):
        if i%2==0:
            x[i,0]=9000*(0.7+0.1*numpy.sin(float(i*1e4)))
            x[i,1]=90*(0.5+0.1*numpy.cos(float(i*1e4)))
        else:
            x[i,0]=9000*(-0.7+0.1*numpy.sin(float(i*1e4)))
            x[i,1]=90*(0.2+0.1*numpy.cos(float(i*1e4)))
    
    ks=o2sclpy.kde_scipy()
    ks.set_data(x,verbose=2)
    print('bw',ks.get_bandwidth())
    for i in range(0,10):
        s=ks.sample()
        print(s[0],s[1])
    print(ks.log_pdf([-6300,18]))
    print(ks.log_pdf([0,0]))
    print(ks.log_pdf([6300,45]))

    return

def test_kde5():
    """
    Compare log pdf of two KDEs
    """
    
    N=200
    x=numpy.zeros((N,1))
    for i in range(0,N):
        if i%2==0:
            x[i,0]=0.7+0.1*numpy.sin(float(i*1e4))
        else:
            x[i,0]=-0.7+0.1*numpy.sin(float(i*1e4))
    
    ks1=o2sclpy.kde_sklearn()
    ks2=o2sclpy.kde_scipy()
    ks1.set_data(x,[0.007],verbose=2)
    ks2.set_data(x,bw_method=0.007,verbose=2)
    print('bws:',ks1.get_bandwidth(),ks2.get_bandwidth())

    for i in range(0,100):
        xx=float(i)/50-1.0
        print('%3d %7.6e %7.6e %7.6e %7.6e %7.6e' %
              (i,xx,ks1.log_pdf([xx]),ks1.pdf([xx]),
               ks2.log_pdf([xx]),ks2.pdf([xx])))

    return

if __name__ == '__main__':
    print('----------------------------------------------------')
    test_kde1()
    print('----------------------------------------------------')
    test_kde2()
    print('----------------------------------------------------')
    test_kde3()
    print('----------------------------------------------------')
    test_kde4()
    print('----------------------------------------------------')
    test_kde5()
    print('All tests passed.')
