#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2022-2025, Andrew W. Steiner, Satyajit Roy, and
#  Mahamudul Hasan Anik
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

def dfdx(x,y):
    return (10.0*numpy.cos(x*10)+2.0*numpy.tan(y))/5.0

def dfdy(x,y):
    return (numpy.sin(x*10)+(2.0/numpy.cos(y))**2)/5.0

def d2fdx2(x,y):
    return (-100.0*numpy.sin(x*10)+2.0*numpy.tan(y))/5.0

def g(x,y):
    return (numpy.sin(x*5)+2.0*numpy.tan(y))/5.0+0.24

def dgdx(x,y):
    return (4.0*numpy.cos(x*5)+2.0*numpy.tan(y))/5.0

def dgdy(x,y):
    return (numpy.sin(x*5)+2.0/(numpy.cos(y))**2)/5.0

def p(a):
    if len(a)==1:
        return ('%7.6e' % a[0])
    for i in range(0,len(a)):
        if i==0:
            stng=('%7.6e' % a[0])
        else:
            stng+=(' %7.6e' % a[i])
    return (stng)

def p2(h,a):
    stng=h
    for j in range(0,len(a)):
        for i in range(0,len(a[j])):
            if i==0:
                stng+=('%7.6e' % a[j][0])
            else:
                stng+=(' %7.6e' % a[j][i])
        if j!=len(a)-1:
            stng+='\n'
            for k in range(0,len(h)):
                stng+=' '
    print(stng)
    return

def test_all():

    mode='all'
    if len(sys.argv)>=2:
        mode=sys.argv[1]
    print('Mode is',mode)

    if mode=='all':
        o2sclpy.check_cuda()
    
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
        y2[i,1]=g(x[i,0],x[i,1])

    if False and plots:
        pb=o2sclpy.plot_base()
        pb.scatter([x[:,0],x[:,1],None,y2[:,1]])
        pb.show()

    # A point for testing
    v=numpy.array([0.5,0.5])

    # Two points for testing
    v2=numpy.zeros((2,2))
    v2[0,0]=0.5
    v2[0,1]=0.5
    v2[1,0]=0.6
    v2[1,1]=0.6
    
    for ik in range(0,3):

        # AWS, 3/9/25: I still periodically have problems with
        # bfgs convergence.
        if mode=='sklearn_gp' or mode=='sklearn' or mode=='all':
            gp_tol=1.0e-4
            if ik==1:
                gp_tol=1.0e-1
            
            print('sklearn GP',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            
            im1=o2sclpy.interpm_sklearn_gp()
            if ik==0:
                im1.set_data_str(x,y,'verbose=0,test_size=0.1')
            elif ik==1:
                im1.set_data_str(x,y,('verbose=0,test_size=0.1,'+
                                      'transform_in=quant'))
            else:
                im1.set_data_str(x,y,('verbose=0,test_size=0.1,'+
                                      'transform_in=moto'))
                
            exact=[f(v[0],v[1])]
            interp1a=im1.eval(v)
            print('      exact:',p(exact))
            print('      eval()',p(interp1a))
            assert numpy.allclose(exact,interp1a[0],rtol=gp_tol)

            if False:
                # This doesn't work yet because of the product of
                # the RBF with the constant parameter
                length_scale=im1.gp.kernel_.length_scale
                
                def grad(x_star,x_train):
                    """Compute the gradient of the RBF kernel w.r.t. x_star"""
                    # Ensure x_star has shape (1, n_features)
                    x_star=np.atleast_2d(x_star)
                    K_gradient=((x_train-x_star)*np.exp(
                        -np.sum((x_train-x_star)**2,axis=1)[:,None]/
                        (2*length_scale**2))/
                                (length_scale**2))
                    return K_gradient.T
                
                interp1a=im1.apply(v,grad)
                
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp1b=im1.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp1b))
            assert numpy.allclose(exact,interp1b,rtol=gp_tol)
            
            exact=[f(v[0],v[1]),0.0]
            interp1c,std1c=im1.eval_unc(v)
            print('      exact:',p(exact))
            print(' eval_unc():',p(interp1c),p(std1c))
            assert numpy.allclose(exact[0],interp1c,rtol=gp_tol)
            assert numpy.allclose(exact[1],std1c,atol=gp_tol)

            # Saving
            save_str=im1.save('test_interpm.o2','ti_gp')
            # Loading
            im1b=o2sclpy.interpm_sklearn_gp()
            im1b.load('test_interpm.o2','ti_gp')
            
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp1d=im1b.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp1d))
            assert numpy.allclose(exact,interp1d,rtol=gp_tol)

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

            # Test eval()
            exact=[f(v[0],v[1]),g(v[0],v[1])]
            interp1e=im1c.eval(v)
            print('      exact:',p(exact))
            print('     eval():',p(interp1e))
            assert numpy.allclose(exact,interp1e,rtol=gp_tol)

            # Test eval_list()
            interp1f=im1c.eval_list(v2)
            exact=[[f(v2[0,0],v2[0,1]),g(v2[0,0],v2[0,1])],
                   [f(v2[1,0],v2[1,1]),g(v2[1,0],v2[1,1])]]
            p2('      exact: ',exact)
            p2('eval_list(): ',interp1f)
            assert numpy.allclose(exact,interp1f,rtol=gp_tol)
            
            print(' ')
                
        if mode=='tf' or mode=='all':
            print('TF DNN',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            
            im2=o2sclpy.interpm_tf_dnn()
            if ik==0:
                print('Value of check_gpu() is:',im2.check_gpu())
                im2.set_data(x,y,verbose=0,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16])
            elif ik==1:
                # For ik==1, we use test_size=0.1 to test non-zero
                # values of that parameter
                im2.set_data(x,y,verbose=0,epochs=200,
                             test_size=0.1,batch_size=8,
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
                
            exact=[f(v[0],v[1])]
            interp2a=im2.eval(v)
            print('      exact:',p(exact));
            print('     eval():',p(interp2a));
            # AWS, 7/3/24: This test is pretty loose because the
            # neural network results are pretty random for few epochs
            assert numpy.allclose(exact,interp2a,rtol=1.0)
    
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp2b=im2.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp2b))
            assert numpy.allclose(exact,interp2b,rtol=1.0)

            im2.save(('test_interpm_tf_'+str(ik)+'.keras'))
            im2b=o2sclpy.interpm_tf_dnn()
            im2b.load(('test_interpm_tf_'+str(ik)+'.keras'))

            if True:
                # This doesn't work yet because we need to store
                # the class data members in addition to the TF model
                exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
                interp2e=im2b.eval_list(v2)
                print('      exact:',p(exact))
                print('eval_list():',p(interp2e))
                assert numpy.allclose(exact,interp2e,rtol=1.0)

            # Test with two outputs instead of one
            if ik==0:
                im2.set_data(x,y2,verbose=0,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16])
            elif ik==1:
                im2.set_data(x,y2,verbose=0,epochs=200,
                             test_size=0.1,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16],
                             transform_in='quant',
                             transform_out='quant')
            else:
                im2.set_data(x,y2,verbose=0,epochs=200,
                             test_size=0.0,batch_size=8,
                             activations=['relu','relu','relu','relu'],
                             hlayers=[128,64,32,16],
                             transform_in='moto',
                             transform_out='moto')

            # Test eval()
            interp2c=im2.eval(v)
            exact=[f(v[0],v[1]),g(v[0],v[1])]
            print('      exact:',p(exact))
            print('     eval():',p(interp2c))
            assert numpy.allclose(exact,interp2c,rtol=1.0)

            # Test eval_list()
            interp2d=im2.eval_list(v2)
            exact=[[f(v2[0,0],v2[0,1]),g(v2[0,0],v2[0,1])],
                   [f(v2[1,0],v2[1,1]),g(v2[1,0],v2[1,1])]]
            p2('      exact: ',exact)
            p2('eval_list(): ',interp2d)
            assert numpy.allclose(exact,interp2d,rtol=1.0)
            
            print(' ')
                
        if mode=='sklearn_mlpr' or mode=='sklearn' or mode=='all':
            
            print('sklearn MLPR',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im3=o2sclpy.interpm_sklearn_mlpr()
            if ik==0:
                im3.set_data(x,y,verbose=0,test_size=0.0,
                             max_iter=1000,hlayers=[60,60])

            elif ik==1:
                im3.set_data(x,y,verbose=0,test_size=0.1,
                             max_iter=1000,transform_in='quant',
                             transform_out='quant',hlayers=[60,60])
    
            else:
                im3.set_data(x,y,verbose=0,test_size=0.1,
                             max_iter=1000,transform_in='moto',
                             transform_out='moto',hlayers=[60,60])
                
            exact=[f(v[0],v[1])]
            interp3a=im3.eval(v)
            print('      exact:',p(exact))
            print('     eval():',p(interp3a))
            assert numpy.allclose(exact,interp3a,rtol=1.0)
    
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp3b=im3.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp3b))
            assert numpy.allclose(exact,interp3b,rtol=1.0)
            
            save_str=im3.save('test_interpm.o2','ti_mlpr')
            im3b=o2sclpy.interpm_sklearn_mlpr()
            im3b.load('test_interpm.o2','ti_mlpr')
            
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp3c=im3b.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp3c))
            assert numpy.allclose(exact,interp3c,rtol=1.0)

            # Test with two outputs instead of one
            if ik==0:
                im3.set_data(x,y2,verbose=0,test_size=0.1,solver='lbfgs',
                             max_iter=1000)
            elif ik==1:
                im3.set_data(x,y2,verbose=0,test_size=0.1,solver='lbfgs',
                             max_iter=1000,transform_in='quant',
                             transform_out='quant')
    
            else:
                im3.set_data(x,y2,verbose=0,test_size=0.1,solver='lbfgs',
                             max_iter=1000,transform_in='moto',
                             transform_out='moto')
            
            # Test eval()
            interp3d=im3.eval(v)
            exact=[f(v[0],v[1]),g(v[0],v[1])]
            print('      exact:',p(exact))
            print('     eval():',p(interp3d))
            assert numpy.allclose(exact,interp3d,rtol=1.0)

            # Test eval_list()
            interp3e=im3.eval_list(v2)
            exact=[[f(v2[0,0],v2[0,1]),g(v2[0,0],v2[0,1])],
                   [f(v2[1,0],v2[1,1]),g(v2[1,0],v2[1,1])]]
            p2('      exact: ',exact)
            p2('eval_list(): ',interp3e)
            assert numpy.allclose(exact,interp3e,rtol=1.0)
            
            print(' ')
            
        if mode=='sklearn_dtr' or mode=='sklearn' or mode=='all':
            
            print('sklearn DTR',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im4=o2sclpy.interpm_sklearn_dtr()
            if ik==0:
                im4.set_data(x,y,verbose=0,test_size=0.0)
            elif ik==1:
                im4.set_data(x,y,verbose=0,test_size=0.1,
                             transform_in='quant',transform_out='quant')
            else:
                im4.set_data(x,y,verbose=0,test_size=0.1,
                             transform_in='moto',transform_out='moto')
                
            exact=[f(v[0],v[1])]
            interp4a=im4.eval(v)
            print('      exact:',p(exact))
            print('     eval():',p(interp4a))
            assert numpy.allclose(exact,interp4a,rtol=1.0)
    
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp4b=im4.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp4b))
            assert numpy.allclose(exact,interp4b,rtol=1.0)
            
            save_str=im4.save('test_interpm.o2','ti_dtr')
            im4b=o2sclpy.interpm_sklearn_dtr()
            im4b.load('test_interpm.o2','ti_dtr')
            
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp4c=im4b.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp4c))
            assert numpy.allclose(exact,interp4c,rtol=1.0)

            # Test with two outputs instead of one
            if ik==0:
                im4.set_data(x,y2,verbose=0,test_size=0.1)
            elif ik==1:
                im4.set_data(x,y2,verbose=0,test_size=0.1,
                             transform_in='quant',transform_out='quant')
            else:
                im4.set_data(x,y2,verbose=0,test_size=0.1,
                             transform_in='moto',transform_out='moto')
            
            # Test eval()
            exact=[f(v[0],v[1]),g(v[0],v[1])]
            interp4d=im4.eval(v)
            print('      exact:',p(exact))
            print('     eval():',p(interp4d))
            assert numpy.allclose(exact,interp4d,rtol=1.0)

            # Test eval_list()
            exact=[[f(v2[0,0],v2[0,1]),g(v2[0,0],v2[0,1])],
                   [f(v2[1,0],v2[1,1]),g(v2[1,0],v2[1,1])]]
            interp4e=im4.eval_list(v2)
            p2('      exact: ',exact)
            p2('eval_list(): ',interp4e)
            assert numpy.allclose(exact,interp4e,rtol=1.0)
            
            print(' ')
            
        if mode=='sklearn_ab' or mode=='sklearn' or mode=='all':
            
            print('sklearn AB',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im4=o2sclpy.interpm_sklearn_adaboost()
            if ik==0:
                im4.set_data(x,y,verbose=0,test_size=0.0)
            elif ik==1:
                im4.set_data(x,y,verbose=0,test_size=0.1,
                             transform_in='quant',transform_out='quant')
            else:
                im4.set_data(x,y,verbose=0,test_size=0.1,
                             transform_in='moto',transform_out='moto')
                
            exact=[f(v[0],v[1])]
            interp4a=im4.eval(v)
            print('      exact:',p(exact))
            print('     eval():',p(interp4a))
            assert numpy.allclose(exact,interp4a,rtol=1.0)
    
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp4b=im4.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp4b))
            assert numpy.allclose(exact,interp4b,rtol=1.0)
            
            save_str=im4.save('test_interpm.o2','ti_ab')
            im4b=o2sclpy.interpm_sklearn_adaboost()
            im4b.load('test_interpm.o2','ti_ab')
            
            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp4c=im4b.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp4c))
            assert numpy.allclose(exact,interp4c,rtol=1.0)

            print(' ')
            
        if mode=='torch' or mode=='all':
            
            print('Torch DNN',ik+1,'of 3')
            print(('──────────────────────────────────'+
                   '─────────────────────────────────'))
            im5=o2sclpy.interpm_torch_dnn()
            if ik==0:
                im5.set_data(x,y,verbose=0,test_size=0.1,
                             hlayers=[60,60],
                             epochs=500,patience=50,device='cpu')
            elif ik==1:
                im5.set_data(x,y,verbose=0,test_size=0.1,
                             hlayers=[60,60],
                             transform_in='quant',transform_out='standard',
                             epochs=500,patience=50,device='cpu')
            else:
                im5.set_data(x,y,verbose=0,test_size=0.1,
                             hlayers=[60,60],
                             transform_in='moto',transform_out='moto',
                             epochs=500,patience=50,device='cpu')
                
            exact=[f(v[0],v[1])]
            interp5a=im5.eval(v)
            print('      exact:',p(exact))
            print('     eval():',p(interp5a))
            assert numpy.allclose(exact,interp5a,rtol=1.0)

            exact=[f(v2[0,0],v2[0,1]),f(v2[1,0],v2[1,1])]
            interp5b=im5.eval_list(v2)
            print('      exact:',p(exact))
            print('eval_list():',p(interp5b))
            assert numpy.allclose(exact,interp5b,rtol=1.0)

            exact=[dfdx(0.5,0.5)]
            interp5c=im5.deriv(v,0)
            print('      exact:',p(exact))
            print('   deriv(0):',p(interp5c))

            exact=[dfdy(0.5,0.5)]
            interp5d=im5.deriv(v,1)
            print('      exact:',p(exact))
            print('   deriv(1):',p(interp5d))
            print(' ')
            
            # AWS, 3/11/25: this doesn't work yet
            if False:
                print('Saving:')
                im5.save('test_interpm_torch_'+str(ik)+'.pt')
            
                print('Loading:')
                im5b=o2sclpy.interpm_torch_dnn()
                im5b.load('test_interpm_torch_'+str(ik)+'.pt')
            
                print('Testing:')
                interp5c=im5b.eval_list(v2)
                print('eval_list():',numpy.shape(interp5c))
                print('interp5b,interp5c:',interp5b,interp5c)
                assert numpy.allclose(f(0.5,0.5),interp5c[0],rtol=1.0)
                assert numpy.allclose(f(0.6,0.6),interp5c[1],rtol=1.0)

    # End of test_all() function
    return
        
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
