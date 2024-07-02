#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2022-2024, Mahamudul Hasan Anik, Satyajit Roy, and
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

import numpy

class interpm_sklearn_gp:
    """
    Interpolate one or many multimensional data sets using a 
    Gaussian process from scikit-learn
    """

    def __init__(self):
        self.gp=0
        self.verbose=0
        self.kernel=0
        self.outformat='numpy'
        self.SS1=0

    def string_to_dict(self,s):
        """
        Convert a string to a dictionary, converting strings to 
        values when necessary.
        """
        
        # First split into keyword = value pairs
        arr=s.split(',')
        # Create empty dictionary
        dct={}

        if len(s)==0:
            return dct
        
        for i in range(0,len(arr)):

            # For each pair, split keyword and value.
            arr2=arr[i].split('=')
        
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

            if arr2[0]=='verbose':
                arr2[1]=int(arr2[1])
            if arr2[0]=='test_size':
                arr2[1]=float(arr2[1])
            if arr2[0]=='normalize_y':
                arr2[1]=(arr2[1]=='True')
                    
            dct[arr2[0]]=arr2[1]

        return dct
    
    def set_data(self,in_data,out_data,
                 kernel='1.0*RBF(1.0,(1e-2,1e2))',test_size=0.0,
                 normalize_y=True,outformat='numpy',verbose=0):
        """
        Set the input and output data to train the interpolator
        """

        if verbose>0:
            print('interpm_sklearn_gp::set_data():')
            print('  kernel:',kernel)
            print('  normalize_y:',normalize_y)
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))

        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import RBF, DotProduct
        from sklearn.gaussian_process.kernels import RationalQuadratic
        from sklearn.gaussian_process.kernels import Matern, WhiteKernel
        from sklearn.preprocessing import QuantileTransformer

        self.kernel=eval(kernel)
        self.outformat=outformat
        self.verbose=verbose
        self.SS1=QuantileTransformer(n_quantiles=len(in_data[1]))
        in_data_trans=self.SS1.fit_transform(in_data)

        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                in_train,in_test,out_train,out_test=train_test_split(
                    in_data_trans,out_data,test_size=test_size)
            except Exception as e:
                print('Exception in interpm_sklearn_gp::set_data()',
                      'at test_train_split().',e)
                pass
        else:
            in_train=in_data_trans
            out_train=out_data
            
        try:
            func=GaussianProcessRegressor
            self.gp=func(normalize_y=True,
                         kernel=self.kernel).fit(in_train,out_train)
        except Exception as e:
            print('Exception in interpm_sklearn_gp::set_data()',
                  'at fit().',e)
            pass

        if test_size>0.0:
            print('score:',self.gp.score(in_test,out_test))

        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=self.string_to_dict(options)
        print('String:',options,'Dictionary:',dct)
              
        self.set_data(in_data,out_data,**dct)

        return
    
    def eval(self,v):
        """
        Evaluate the GP at point ``v``.
        """

        # AWS, 3/27/24: Keep in mind that o2scl::interpm_python.eval()
        # expects the return type to be a numpy array. 
        v_trans=0
        try:
            v_trans=self.SS1.transform(v.reshape(1,-1))
        except Exception as e:
            print('Exception at input transformation in interpm_sklearn_gp:',
                      e)
            pass
        
        yp=self.gp.predict([v_trans])
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval(): list mode type(yp),v,yp:',
                      type(yp),v,yp)
            return yp[0].tolist()
        if yp.ndim==1:
            if self.verbose>1:
                print('interpm_sklearn_gp::eval(): ndim=1 mode type(yp),v,yp:',
                      type(yp),v,yp)
            return numpy.ascontiguousarray(yp)
        if self.verbose>1:
            print('interpm_sklearn_gp::eval(): array mode type(yp[0]),v,yp[0]:',
                  type(yp[0]),v,yp[0])
        return numpy.ascontiguousarray(yp[0])

    def eval_unc(self,v):
        """
        Evaluate the GP and its uncertainty at point ``v``.

        # AWS, 3/27/24: Keep in mind that
        # o2scl::interpm_python.eval_unc() expects the return type to
        # be a tuple of numpy arrays. 
        """
    
        v_trans=0
        try:
            v_trans=self.SS1.transform(v.reshape(1,-1))
        except Exception as e:
            print('Exception at input transformation in interpm_sklearn_gp:',
                      e)
            pass

        yp,std=self.gp.predict(v_trans,return_std=True)
        if self.outformat=='list':
            return yp[0].tolist(),std[0].tolist()
        if yp.ndim==1:
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_unc(): type(yp),v,yp:',
                      type(yp),v,yp)
            return (numpy.ascontiguousarray(yp),
                    numpy.ascontiguousarray(std))
        if self.verbose>1:
            print('interpm_sklearn_gp::eval_unc(): type(yp[0]),v,yp[0]:',
                  type(yp[0]),v,yp[0])
        return (numpy.ascontiguousarray(yp[0]),
                numpy.ascontiguousarray(std[0]))

class interpm_tf_dnn:
    """
    Interpolate one or many multimensional data sets using 
    a deep neural network from TensorFlow
    """

    def __init__(self):
        
        self.verbose=0
        self.kernel=0
        self.outformat='numpy'
        self.dnn=0
        self.SS1=0
        self.SS2=0
        self.transform=0
        
        return
    
    def string_to_dict(self,s):
        """
        Convert a string to a dictionary, converting strings to 
        values when necessary.
        """
        
        # First split into keyword = value pairs
        arr=s.split(',')
        # Create empty dictionary
        dct={}

        if len(s)==0:
            return dct
        
        for i in range(0,len(arr)):

            # For each pair, split keyword and value.
            arr2=arr[i].split('=')
        
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

            if arr2[0]=='verbose':
                arr2[1]=int(arr2[1])
            elif arr2[0]=='batch_size':
                arr2[1]=int(arr2[1])
            elif arr2[0]=='epochs':
                arr2[1]=int(arr2[1])
            elif arr2[0]=='test_size':
                arr2[1]=float(arr2[1])
            elif arr2[0]=='evaluate':
                arr2[1]=bool(arr2[1])
                    
            dct[arr2[0]]=arr2[1]

        return dct
    
    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 activations=['sigmoid','sigmoid'],
                 batch_size=None,epochs=100,
                 transform='none',test_size=0.0,evaluate=False,
                 hlayers=[96,32],loss='mean_squared_error'):
        """
        Set the input and output data to train the interpolator

        some activation functions: 
        relu [0,\\infty]
        sigmoid [0,1]
        tanh [-1,1]

        transformations:
        quantile transforms to [0,1]
        MinMaxScaler transforms to [a,b]
        """

        from sklearn.model_selection import train_test_split
        import tensorflow as tf
        
        if verbose>0:
            print('interpm_tf_dnn::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  batch_size:',batch_size)
            print('  layers:',hlayers)
            print('  activation functions:',activations)
            print('  transform:',transform)
            print('  epochs:',epochs)
            print('  test_size:',test_size)

        self.outformat=outformat
        self.verbose=verbose
        self.transform=transform

        from sklearn.preprocessing import QuantileTransformer
        from sklearn.preprocessing import MinMaxScaler
        if self.transform=='moto':
            self.SS1=MinMaxScaler(feature_range=(-1,1))
            self.SS2=MinMaxScaler(feature_range=(-1,1))
        
            in_data_trans=self.SS1.fit_transform(in_data)
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform=='quant':
            self.SS1=QuantileTransformer()
            self.SS2=QuantileTransformer()
        
            in_data_trans=self.SS1.fit_transform(in_data)
            out_data_trans=self.SS2.fit_transform(out_data)
        else:
            in_data_trans=in_data
            out_data_trans=out_data

        if self.verbose>0:
            try:
                minv=out_data_trans[0,0]
                maxv=out_data_trans[0,0]
                minv_old=out_data[0,0]
                maxv_old=out_data[0,0]
            except Exception as e:
                print('Exception in interpm_tf_dnn::set_data()',
                      'at min,max().',e)
                pass
            
            for j in range(0,numpy.shape(out_data)[0]):
                if out_data[j,0]<minv_old:
                    minv_old=out_data[j,0]
                if out_data[j,0]>maxv_old:
                    maxv_old=out_data[j,0]
                if out_data_trans[j,0]<minv:
                    minv=out_data_trans[j,0]
                if out_data_trans[j,0]>maxv:
                    maxv=out_data_trans[j,0]

            print('min,max before transformation: %7.6e %7.6e' %
                  (minv_old,maxv_old))
            print('min,max after transformation : %7.6e %7.6e' %
                  (minv,maxv))
            
        if test_size>0.0:
            try:
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data_trans,out_data_trans,test_size=test_size)
            except Exception as e:
                print('Exception in interpm_tf_dnn::set_data()',
                      'at test_train_split().',e)
                pass
        else:
            x_train=in_data_trans
            y_train=out_data_trans

        nd_in=numpy.shape(in_data)[1]
        nd_out=numpy.shape(out_data)[1]
        
        if self.verbose>0:
            print('nd_in,nd_out:',nd_in,nd_out)
            print('  Training DNN model.')
            
        try:
            nl=len(hlayers)
            na=len(activations)
            inp=tf.keras.Input(shape=(nd_in,))
            layers=[inp,tf.keras.layers.Dense(hlayers[0],
                                              activation=activations[0])]
            if self.verbose>0:
                print('Layer: dense',hlayers[0],nd_in,activations[0])
            for i in range(1,nl):
                act=activations[i%na]
                layers.append(tf.keras.layers.Dense(hlayers[i],
                                                    activation=act))
                if self.verbose>0:
                    print('Layer: dense',hlayers[i],act)
            layers.append(tf.keras.layers.Dense(nd_out,
                                                activation='linear'))
            if self.verbose>0:
                print('Layer: dense',nd_out,'linear')
            model=tf.keras.Sequential(layers)
        except Exception as e:
            print('Exception in interpm_tf_dnn::set_data()',
                  'at model definition.',e)
            pass
        
        if self.verbose>0:
            print('summary:',model.summary())

        try:
            # Compile the model for training
            model.compile(loss=loss,optimizer='adam')
            if test_size>0.0:
                # Fit the model to training data
                model.fit(x_train,y_train,batch_size=batch_size,
                          epochs=epochs,validation_data=(x_test,y_test),
                          verbose=self.verbose)
                          
            else:
                # Fit the model to training data
                model.fit(x_train,y_train,batch_size=batch_size,
                          epochs=epochs,verbose=self.verbose)
                
        except Exception as e:
            print('Exception in interpm_tf_dnn::set_data()',
                  'at model fitting.',e)
            pass

        if evaluate==True:
            # Return loss value and metrics
            if self.verbose>0:
                print('  Training done.')
            print('  Test Score: [loss, accuracy]:',
                  model.evaluate(x_test,y_test,verbose=self.verbose))
            
        self.dnn=model

        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=self.string_to_dict(options)
        print('String:',options,'Dictionary:',dct)

        try:
            self.set_data(in_data,out_data,**dct)
        except Exception as e:
            print('Call to set_data() failed.')
            pass

        return
    
    def eval(self,v):
        """
        Evaluate the NN at point ``v``.
        """

        if self.transform!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print('Exception at input transformation in interpm_tf_dnn:',
                      e)
                pass
        else:
            v_trans=v.reshape(1,-1)

        try:
            pred=self.dnn.predict(v_trans, verbose=self.verbose)
        except Exception as e:
            print('Exception 4 in interpm_tf_dnn:',e)
            pass
            
        if self.transform!='none':
            try:
                pred_trans=self.SS2.inverse_transform(pred)
            except Exception as e:
                print('Exception 5 in interpm_tf_dnn:',e)
                pass
        else:
            pred_trans=pred
    
        if self.outformat=='list':
            return pred_trans.tolist()

        if pred_trans.ndim==1:
            
            if self.verbose>1:
                print('interpm_tf_dnn::eval():',
                      'type(pred_trans),pred_trans:',
                      type(pred_trans),pred_trans)
            # The output from tf.keras is float32, so we have to convert to
            # float64 
            n_out=numpy.shape(pred_trans[0])[0]
            out_double=numpy.zeros((n_out))
            for i in range(0,n_out):
                out_double[i]=pred_trans[i]
                    
            return numpy.ascontiguousarray(out_double)
        
        if self.verbose>1:
            print('interpm_tf_dnn::eval():',
                  'type(pred_trans[0]),pred_trans[0]:',
                  type(pred_trans[0]),pred_trans[0])

        # The output from tf.keras is float32, so we have to convert to
        # float64 
        n_out=numpy.shape(pred_trans[0])[0]
        out_double=numpy.zeros((n_out))
        for i in range(0,n_out):
            out_double[i]=pred_trans[0][i]
            
        return numpy.ascontiguousarray(out_double)
