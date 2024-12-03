#  -------------------------------------------------------------------
#  
#  Copyright (C) 2022-2025, Satyajit Roy, Mahamudul Hasan Anik, and
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
import sys

plots=True
if 'pytest' in sys.modules:
    plots=False

def f(x,y):
    return (numpy.sin(x*10)+2.0*numpy.tan(y))/5.0+0.14

def f2(x,y):
    fv=f(x,y)
    return 2.0-fv*fv*fv

def test_all():

    N=1000
    x=numpy.zeros((N,2))
    for i in range(0,N):
        x[i,0]=float(i)/float(N)
        x[i,1]=numpy.abs(numpy.sin(1.0e8*float(i)))
            
    y=numpy.zeros((N,1))
    for i in range(0,N):
        y[i,0]=f(x[i,0],x[i,1])

    if plots:
        pb=o2sclpy.plot_base()
        pb.scatter([x[:,0],x[:,1],None,y[:,0]])
        pb.show()

    for ik in range(0,3):
        
        if True:
            im=o2sclpy.interpm_sklearn_gp()
            if ik==0:
                im.set_data_str(x,y,'verbose=2,test_size=0.1')
            elif ik==1:
                im.set_data_str(x,y,('verbose=2,test_size=0.1,trans'+
                                     'form_in=quant,transform_out=quant'))
            else:
                im.set_data_str(x,y,('verbose=2,test_size=0.1,trans'+
                                     'form_in=moto,transform_out=moto'))
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im.eval(v)
            print('exact,interp 1: %7.6e %7.6e' % (exact,interp[0]))
            assert numpy.allclose(exact,interp[0],rtol=1.0)

            v2=numpy.zeros((2,2))
            v2[0,0]=0.5
            v2[0,1]=0.5
            v2[1,0]=0.6
            v2[1,1]=0.6
            interp2=im.eval_list(v2)
            assert numpy.allclose(f(0.5,0.5),interp2[0],rtol=1.0)
            assert numpy.allclose(f(0.6,0.6),interp2[1],rtol=1.0)
            
            interp3,std3=im.eval_unc(v)
            print('exact,interp 2: %7.6e %7.6e %7.6e' %
                  (exact,interp[0],std3[0]))
            assert numpy.allclose(exact,interp3[0],rtol=1.0)
            assert numpy.allclose(0,std3[0],atol=1.0)

            print('saving')
            save_str=im.save('test_interpm.o2','ti')
            
            print('loading')
            imx=o2sclpy.interpm_sklearn_gp()
            imx.load('test_interpm.o2','ti')
            
            print('testing')
            interp4=im.eval_list(v2)
            print(interp2,interp4)
            assert numpy.allclose(f(0.5,0.5),interp4[0],rtol=1.0)
            assert numpy.allclose(f(0.6,0.6),interp4[1],rtol=1.0)
    
        if True:
            im2=o2sclpy.interpm_tf_dnn()
            if ik==0:
                im2.set_data(x,y,verbose=1,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16])
            elif ik==1:
                im2.set_data(x,y,verbose=1,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16],
                             transform_in='quant',
                             transform_out='quant')
            else:
                im2.set_data(x,y,verbose=1,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16],
                             transform_in='moto',
                             transform_out='moto')
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im2.eval(v)[0]
            print('exact,interp 3: %7.6e %7.6e' % (exact,interp))
            # AWS, 7/3/24: This test is pretty loose because the
            # neural network results are pretty random for few epochs
            assert numpy.allclose(exact,interp,rtol=1.0)
    
        if True:
            im3=o2sclpy.interpm_sklearn_mlpr()
            im3.set_data(x,y,verbose=0,test_size=0.1,solver='lbfgs',
                         max_iter=1000)
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im3.eval(v)
            print('exact,interp 4:', exact,interp)
            assert numpy.allclose(exact,interp,rtol=1.0)
    
    if True:
        im2=o2sclpy.interpm_sklearn_dtr()
        im2.set_data(x,y,verbose=0,test_size=0.1)
        exact=f(0.5,0.5)
        v=numpy.array([0.5,0.5])
        interp=im2.eval(v)
        print('exact,interp 3:', exact,interp)
        assert numpy.allclose(exact,interp,rtol=1.0)
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
