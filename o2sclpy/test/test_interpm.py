#  -------------------------------------------------------------------
#  
#  Copyright (C) 2022-2023, Mahamudul Hasan Anik, Satyajit Roy, and
#  Andrew W. Steiner
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

def f(x,y):
    return (numpy.sin(x*10)+2.0*numpy.tan(y))/5.0+0.14

def f2(x,y):
    fv=f(x,y)
    return 2.0-fv*fv*fv

def test_all():

    N=100
    x=numpy.zeros((N,2))
    for i in range(0,N):
        x[i,0]=float(i)/float(N)
        x[i,1]=numpy.abs(numpy.sin(1.0e8*float(i)))
            
    y=numpy.zeros((N,1))
    for i in range(0,N):
        y[i,0]=f(x[i,0],x[i,1])

    if True:
        im=o2sclpy.interpm_sklearn_gp()
        im.set_data_str(x,y,'verbose=2')
        exact=f(0.5,0.5)
        v=numpy.array([0.5,0.5])
        interp=im.eval(v)
        print('exact,interp: %7.6e %7.6e' % (exact,interp))
        assert numpy.allclose(exact,interp,rtol=1.0e-4)
        
        interp2,std2=im.eval_unc(v)
        print('exact,interp: %7.6e %7.6e %7.6e' % (exact,interp,std2))
        assert numpy.allclose(exact,interp2,rtol=1.0e-4)
        assert numpy.allclose(0,std2,atol=1.0e-5)

    if True:
        im2=o2sclpy.interpm_tf_dnn()
        im2.set_data(x,y,verbose=1,epochs=600,
                     test_size=0.15,batch_size=8,transform='none',
                     activations=['relu','relu','relu','relu'],
                     hlayers=[128,64,32,16])
        exact=f(0.5,0.5)
        v=numpy.array([0.5,0.5])
        interp=im2.eval(v)[0]
        print('exact,interp: %7.6e %7.6e' % (exact,interp))
        assert numpy.allclose(exact,interp,rtol=1.0)

        im2.verbose=0
        for i in range(0,N,10):
            print('%2d %7.6e %7.6e' % (i,im2.eval(x[i])[0],y[i,0]))

    return

if __name__ == '__main__':
    test_all()
    print('All tests passed.')
