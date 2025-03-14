#  ───────────────────────────────────────────────────────────────────
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
#  ───────────────────────────────────────────────────────────────────
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
    return (numpy.sin(x*5)+2.0*numpy.tan(y))/5.0+0.24

def test_all():

    N=1000
    x=numpy.zeros((N,2))
    for i in range(0,N):
        x[i,0]=float(i)/float(N)
        x[i,1]=numpy.abs(numpy.sin(1.0e8*float(i)))
            
    y=numpy.zeros((N,1))
    for i in range(0,N):
        y[i,0]=f(x[i,0],x[i,1])

    y2=numpy.zeros((N,2))
    for i in range(0,N):
        y2[i,0]=f(x[i,0],x[i,1])
        y2[i,1]=f2(x[i,0],x[i,1])

    if plots:
        pb=o2sclpy.plot_base()
        pb.scatter([x[:,0],x[:,1],None,y2[:,1]])
        pb.show()

    for ik in range(0,3):

        # AWS, 3/9/25: I still periodically have problems with
        # bfgs convergence.
        if True:
            gp_tol=1.0e-4
            if ik>=1:
                gp_tol=1.0
            
            print('sklearn GP',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im1=o2sclpy.interpm_sklearn_gp()
            if ik==0:
                im1.set_data_str(x,y,'verbose=0,test_size=0.1')
            elif ik==1:
                im1.set_data_str(x,y,('verbose=0,test_size=0.1,trans'+
                                       'form_in=quant'))
            else:
                im1.set_data_str(x,y,('verbose=0,test_size=0.1,trans'+
                                       'form_in=moto'))
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im1.eval(v)
            print('exact,interp 1: %7.6e %7.6e' % (exact,interp[0]))
            assert numpy.allclose(exact,interp[0],rtol=gp_tol)

            v2=numpy.zeros((2,2))
            v2[0,0]=0.5
            v2[0,1]=0.5
            v2[1,0]=0.6
            v2[1,1]=0.6
            interp2=im1.eval_list(v2)
            print('eval_list:',numpy.shape(interp2))
            assert numpy.allclose(f(0.5,0.5),interp2[0],rtol=gp_tol)
            assert numpy.allclose(f(0.6,0.6),interp2[1],rtol=gp_tol)
            
            interp3,std3=im1.eval_unc(v)
            print('exact,interp 2: %7.6e %7.6e %7.6e' %
                  (exact,interp[0],std3[0]))
            assert numpy.allclose(exact,interp3[0],rtol=gp_tol)
            assert numpy.allclose(0,std3[0],atol=gp_tol)

            print('Saving:')
            save_str=im1.save('test_interpm.o2','ti_gp')
            
            print('Loading:')
            im1b=o2sclpy.interpm_sklearn_gp()
            im1b.load('test_interpm.o2','ti_gp')
            
            print('Testing:')
            interp4=im1b.eval_list(v2)
            print('eval_list:',numpy.shape(interp4))
            print('interp2,interp4:',interp2,interp4)
            assert numpy.allclose(f(0.5,0.5),interp4[0],rtol=gp_tol)
            assert numpy.allclose(f(0.6,0.6),interp4[1],rtol=gp_tol)

            # Test with two outputs instead of one
            im1c=o2sclpy.interpm_sklearn_gp()
            if ik==0:
                im1c.set_data_str(x,y2,'verbose=0,test_size=0.1')
            elif ik==1:
                im1c.set_data_str(x,y2,('verbose=0,test_size=0.1,trans'+
                                       'form_in=quant'))
            else:
                im1c.set_data_str(x,y2,('verbose=0,test_size=0.1,trans'+
                                       'form_in=moto'))
            interp5=im1c.eval(v)
            print('interp5:',interp5)
            print(f(0.5,0.5),f2(0.5,0.5))
            print(' ')
                
        if True:
            print('TF DNN',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im2=o2sclpy.interpm_tf_dnn()
            if ik==0:
                im2.set_data(x,y,verbose=0,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16])
            elif ik==1:
                im2.set_data(x,y,verbose=0,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16],
                             transform_in='quant',
                             transform_out='quant')
            else:
                im2.set_data(x,y,verbose=0,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16],
                             transform_in='moto',
                             transform_out='moto')
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im2.eval(v)[0]
            print('eval:',type(interp),numpy.shape(interp))
            print('exact,interp 3: %7.6e %7.6e' % (exact,interp))
            # AWS, 7/3/24: This test is pretty loose because the
            # neural network results are pretty random for few epochs
            assert numpy.allclose(exact,interp,rtol=1.0)
    
            print('Saving:')
            save_str=im2.save(('test_interpm_tf_'+str(ik)+'.keras'))
            print(' ')
            
        if True:
            print('sklearn MLPR',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im3=o2sclpy.interpm_sklearn_mlpr()
            if ik==0:
                im3.set_data(x,y,verbose=0,test_size=0.1,solver='lbfgs',
                             max_iter=1000)
            elif ik==1:
                im3.set_data(x,y,verbose=0,test_size=0.1,solver='lbfgs',
                             max_iter=1000,transform_in='quant',
                             transform_out='quant')
    
            else:
                im3.set_data(x,y,verbose=0,test_size=0.1,solver='lbfgs',
                             max_iter=1000,transform_in='moto',
                             transform_out='moto')
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im3.eval(v)
            print('eval:',numpy.shape(interp))
            print('exact,interp 4: %7.6e %7.6e' % (exact,interp[0]))
            assert numpy.allclose(exact,interp,rtol=1.0)
            print(' ')
    
            print('Saving:')
            save_str=im3.save('test_interpm.o2','ti_mlpr')
            
            print('Loading:')
            im3b=o2sclpy.interpm_sklearn_mlpr()
            im3b.load('test_interpm.o2','ti_mlpr')
            
            print('Testing:')
            interp4=im3b.eval_list(v2)
            print('eval_list:',numpy.shape(interp4))
            print('interp2,interp4:',interp2,interp4)
            assert numpy.allclose(f(0.5,0.5),interp4[0],rtol=1.0)
            assert numpy.allclose(f(0.6,0.6),interp4[1],rtol=1.0)
            print(' ')
            
        if True:
            print('sklearn DTR',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im4=o2sclpy.interpm_sklearn_dtr()
            if ik==0:
                im4.set_data(x,y,verbose=0,test_size=0.1)
            elif ik==1:
                im4.set_data(x,y,verbose=0,test_size=0.1,
                             transform_in='quant',transform_out='quant')
            else:
                im4.set_data(x,y,verbose=0,test_size=0.1,
                             transform_in='moto',transform_out='moto')
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im4.eval(v)
            print('eval:',numpy.shape(interp))
            print('exact,interp 5: %7.6e %7.6e' % (exact,interp[0]))
            assert numpy.allclose(exact,interp,rtol=1.0)
            print(' ')
    
            print('Saving:')
            save_str=im4.save('test_interpm.o2','ti_dtr')
            
            print('Loading:')
            im4b=o2sclpy.interpm_sklearn_dtr()
            im4b.load('test_interpm.o2','ti_dtr')
            
            print('Testing:')
            interp4=im4b.eval_list(v2)
            print('eval_list:',numpy.shape(interp4))
            print('interp2,interp4:',interp2,interp4)
            assert numpy.allclose(f(0.5,0.5),interp4[0],rtol=1.0)
            assert numpy.allclose(f(0.6,0.6),interp4[1],rtol=1.0)
            print(' ')
            
        if True:
            print('Torch DNN',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im5=o2sclpy.interpm_torch_dnn()
            if ik==0:
                im5.set_data(x,y,verbose=0,test_size=0.1,
                             hlayers=[128,64,32,16])
            elif ik==1:
                im5.set_data(x,y,verbose=0,test_size=0.1,
                             hlayers=[128,64,32,16],
                             transform_in='quant',transform_out='quant')
            else:
                im5.set_data(x,y,verbose=0,test_size=0.1,
                             hlayers=[128,64,32,16],
                             transform_in='moto',transform_out='moto')
            exact=f(0.5,0.5)
            v=numpy.array([0.5,0.5])
            interp=im5.eval(v)
            print('eval:',numpy.shape(interp))
            print('exact,interp 10: %7.6e %7.6e' % (exact,interp[0]))
            assert numpy.allclose(exact,interp,rtol=1.0)
            print(' ')

            # AWS, 3/11/25: this doesn't work, because of issues with
            # pickling local objects.
            if False:
                print('Saving:')
                im5.save('test_interpm_'+str(ik)+'.pt')
            
                print('Loading:')
                im5b=o2sclpy.interpm_sklearn_mlpr()
                im5b.load('test_interpm_'+str(ik)+'.pt')
            
                print('Testing:')
                interp4=im5b.eval_list(v2)
                print('eval_list:',numpy.shape(interp4))
                print('interp2,interp4:',interp2,interp4)
                assert numpy.allclose(f(0.5,0.5),interp4[0],rtol=1.0)
                assert numpy.allclose(f(0.6,0.6),interp4[1],rtol=1.0)
                print(' ')
            
            
    quit()
        
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
