#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2022-2026, Andrew W. Steiner, Satyajit Roy, and
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

class interpm_tf_dnn:
    """Interpolate one or many multimensional data sets using a
    neural network from TensorFlow

    This is a simple implementation of a neural network with
    early stopping. 

    The variables ``verbose`` and ``outformat`` can be changed
    at any time.

    .. todo:: * Calculate derivatives
              * 'native' output format?
              * add_data() for successive improvements
              * Allow user to control CPU vs. GPU
              * Allow user to control early stopping monitor
    
    """
    verbose=0
    """
    Verbosity parameter (default 0)
    """
    outformat='numpy'
    """
    Output format, either 'numpy' or 'list' (default 'numpy')
    """

    def __init__(self):

        self.dnn=None
        self.SS1=None
        self.SS2=None
        self.transform_in=None
        self.transform_out=None
        self.outformat='numpy'
        self.nd_in=None
        self.nd_out=None
        self.loss=[]
        self.val_loss=[]
        
        import tensorflow as tf
        self.tf=tf
        
        import sklearn.preprocessing as preprocessing
        self.pp=preprocessing
        
        return

    def check_gpu(self):
        """
        Check if Tensorflow is likely to use the GPU
        """
        try:
            with self.tf.device('/GPU:0'):
                a=self.tf.constant([[1.0,2.0]])
                b=self.tf.constant([[3.0],[4.0]])
                c=self.tf.matmul(a,b)
        except:
            return False
        return True
    
    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 activations=['relu'],batch_size=None,epochs=100,
                 transform_in='none',transform_out='none',
                 test_size=0.0,evaluate=False,
                 hlayers=[8,8],loss='mean_squared_error',
                 es_min_delta=1.0e-4,es_patience=100,es_start=50,
                 tf_logs='1',tf_onednn_opts='1'):
        """Set the input and output data to train the interpolator

        Some activation functions are: 'relu', 'sigmoid', 'tanh'. If
        the number of activation functions specified in
        ``activations`` is smaller than the number of layers, then the
        activation function list is reused using the modulus operator.

        The keyword argument ``tf_logs`` specifies the value of
        the environment variable ``TF_CPP_MIN_LOG_LEVEL``.

        """

        from sklearn.model_selection import train_test_split
        import os
        os.environ['TF_ENABLE_ONEDNN_OPTS']=tf_onednn_opts
        os.environ['TF_CPP_MIN_LOG_LEVEL']=tf_logs
        
        if verbose>0:
            print('interpm_tf_dnn::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  batch_size:',batch_size)
            print('  layers:',hlayers)
            print('  activation functions:',activations)
            print('  transform_in:',transform_in)
            print('  transform_out:',transform_out)
            print('  epochs:',epochs)
            print('  test_size:',test_size)

        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        self.transform_out=transform_out
        
        self.nd_in=numpy.shape(in_data)[1]
        self.nd_out=numpy.shape(out_data)[1]

        # ----------------------------------------------------------
        # Handle the data transformations
        
        if self.transform_in=='moto':
            self.SS1=self.pp.MinMaxScaler(feature_range=(-1,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='quant':
            self.SS1=self.pp.QuantileTransformer(n_quantiles=in_data.shape[0])
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='standard':
            self.SS1=self.pp.StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
            
        if self.transform_out=='moto':
            self.SS2=self.pp.MinMaxScaler(feature_range=(-1,1))
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='quant':
            self.SS2=self.pp.QuantileTransformer(n_quantiles=out_data.shape[0])
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='standard':
            self.SS2=self.pp.StandardScaler()
            out_data_trans=self.SS2.fit_transform(out_data)
        else:
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
                raise
            
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
                raise
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
            inp=self.tf.keras.Input(shape=(nd_in,))
            layers=[inp,self.tf.keras.layers.Dense(hlayers[0],
                                              activation=activations[0])]
            if self.verbose>0:
                print('Layer: dense',hlayers[0],nd_in,activations[0])
            for i in range(1,nl):
                act=activations[i%na]
                layers.append(self.tf.keras.layers.Dense(hlayers[i],
                                                    activation=act))
                if self.verbose>0:
                    print('Layer: dense',hlayers[i],act)
            layers.append(self.tf.keras.layers.Dense(nd_out,
                                                activation='linear'))
            if self.verbose>0:
                print('Layer: dense',nd_out,'linear')
            model=self.tf.keras.Sequential(layers)
        except Exception as e:
            print('Exception in interpm_tf_dnn::set_data()',
                  'at model definition.',e)
            raise
        
        if self.verbose>0:
            print('summary:',model.summary())

        try:
            from keras.callbacks import EarlyStopping
            import keras

            #class loss_history(keras.callbacks.Callback):
            #    def on_train_begin(self,logs={}):
            #        self.loss=[]
            #        self.val_loss=[]
            #    def on_batch_end(self,batch,logs={}):
            #        self.loss.append(logs.get('loss'))
            #        self.val_loss.append(logs.get('val_loss'))
            #        print('here',self.loss,self.val_loss)
            #        quit()
            #history=loss_history()

            # Use the validation loss if we have testing data
            if test_size>0.0:
                mon_string='val_loss'
            else:
                mon_string='loss'
            
            early_stopping=EarlyStopping(monitor=mon_string,
                                         min_delta=es_min_delta,
                                         patience=es_patience,
                                         verbose=self.verbose,
                                         restore_best_weights=True,
                                         start_from_epoch=es_start,
                                         mode='min')
            model.compile(loss=loss,optimizer='adam')

            # Convert numpy array to TensorFlow tensor
            x_tf=self.tf.convert_to_tensor(x_train)
            y_tf=self.tf.convert_to_tensor(y_train)
            
            if test_size>0.0:
                # Fit the model to training data
                hist2=model.fit(x_tf,y_tf,batch_size=batch_size,
                          epochs=epochs,validation_data=(x_test,y_test),
                          verbose=self.verbose,
                          callbacks=[early_stopping])
                self.loss=hist2.history['loss']
                self.val_loss=hist2.history['val_loss']
                          
            else:
                # Fit the model to training data
                hist2=model.fit(x_tf,y_tf,batch_size=batch_size,
                                epochs=epochs,verbose=self.verbose,
                                callbacks=[early_stopping])
                self.loss=hist2.history['loss']
                self.val_loss=[]
                
        except Exception as e:
            print('Exception in interpm_tf_dnn::set_data()',
                  'at model fitting.',e)
            raise

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

        try:
            dct=string_to_dict2(options,list_of_ints=['verbose',
                                                      'batch_size',
                                                      'epochs'],
                                list_of_floats=['test_size'],
                                list_of_bools=['evaluate'])
            if "hlayers" in dct:
                htemp=dct["hlayers"]
                htemp=htemp[1:-1]
                htemp=htemp.split(',')
                htemp2=[]
                for i in range(0,len(htemp)):
                    htemp2.append(int(htemp[i]))
                dct["hlayers"]=htemp2
            if "activations" in dct:
                atemp=dct["activations"]
                atemp=atemp[1:-1]
                atemp=atemp.split(',')
                atemp2=[]
                for i in range(0,len(atemp)):
                    atemp2.append(atemp[i])
                dct["activations"]=atemp2
            print('String:',options,'Dictionary:',dct)

            self.set_data(in_data,out_data,**dct)
        except Exception as e:
            print('Calls in interpm_tf_dnn::set_data_str() failed.',e)
            raise

        return
    
    def eval(self,v):
        """
        Evaluate the NN at point ``v``.

        The input ``v`` should be a one-dimensional numpy array
        and the output is a one-dimensional numpy array, unless
        outformat is ``list``, in which case the output is a
        Python list.
        
        """

        if self.transform_in!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print('Exception at input transformation',
                      'in interpm_tf_dnn::eval()',
                      e)
                raise
        else:
            v_trans=v.reshape(1,-1)

        try:
            # Convert numpy array to TensorFlow tensor
            v_tf=self.tf.convert_to_tensor(v_trans)
                
            # We don't want output at every point, even if verbose is
            # 1, so we use self.verbose-1 here for the argument to
            # the predict function.
            if self.verbose>1:
                pred=self.dnn.predict(v_tf,verbose=self.verbose-1)
            else:
                pred=self.dnn.predict(v_tf,verbose=0)
        except Exception as e:
            print('Exception at prediction in',
                  'interpm_tf_dnn::eval().',e)
            raise
            
        if self.transform_out!='none':
            try:
                pred_trans=self.SS2.inverse_transform(pred)
            except Exception as e:
                print('Exception in output transformation in',
                      'interpm_tf_dnn::eval().',e)
                raise
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

    def eval_unc(self,v):
        """
        Empty function because this interpolator does not currently
        provide uncertainties
        """
        return self.eval(v)
        
    def eval_list(self,v):
        """
        Evaluate the neural network at the list of points given
        in ``v``.
        """

        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v)
            else:
                v_trans=v
        except Exception as e:
            print(('Exception at input transformation '+
                   'in interpm_tf_dnn::eval_list():'),e)
            raise

        try:
            # Convert numpy array to TensorFlow tensor
            v_tf=self.tf.convert_to_tensor(v_trans)
            
            yp=self.dnn.predict(v_tf, verbose=self.verbose)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_tf_dnn::eval_list():'),e)
            raise

        yp_trans=0
        try:
            if self.transform_out!='none':
                if self.nd_out==1:
                    yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
                else:
                    yp_trans=self.SS2.inverse_transform(yp)
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_tf_dnn::eval_list():'),e)
            raise
        if yp_trans.ndim==2 and len(yp_trans[0])==1:
            yp_trans=yp_trans.reshape(1,-1)[0]
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_tf_dnn::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        if self.verbose>1:
            print('interpm_tf_dnn::eval_list():',
                  'array mode type(yp),v,yp:',
                  type(yp_trans),v,yp_trans)
        return numpy.ascontiguousarray(yp_trans)
    
    def save(self,filename):
        """
        Save the interpolation settings to a pair of files. A
        ``.keras`` file for the TensorFlow model and a ``.o2``
        file for additional data.
        """
        if filename[-6:]=='.keras':
            filename=filename[:-6]
        self.dnn.save(filename+'.keras')

        import pickle

        # Construct dictionary of class data
        loc_dct={"o2sclpy_version": version,
                 "verbose": self.verbose,
                 "outformat": self.outformat,
                 "transform_in": self.transform_in,
                 "transform_out": self.transform_out,
                 "nd_in": self.nd_in,
                 "nd_out": self.nd_out,
                 "SS1": self.SS1,
                 "SS2": self.SS2}

        # Create a string from a tuple of the dictionary and the GPR
        # object
        byte_string=pickle.dumps(loc_dct)

        # Write string to an HDF5 file
        hf=o2sclpy.hdf_file()
        hf.open_or_create(filename+'.o2')
        hf.sets('interpm_tf_dnn',byte_string)
        hf.close()
        
        return
    
    def load(self,filename):
        """
        Load interpolator from a pair of ``.keras`` and ``.o2`` files.
        """
        import keras
        
        if filename[-6:]=='.keras':
            filename=filename[:-6]
        self.dnn=keras.saving.load_model(filename+'.keras')

        import pickle
        from sklearn.gaussian_process import GaussianProcessRegressor
        
        # Read string from file
        hf=o2sclpy.hdf_file()
        hf.open(filename+'.o2')
        s=o2sclpy.std_string()
        hf.gets('interpm_tf_dnn',s)
        hf.close()
        # Convert to a Python bytes object
        sb=s.to_bytes()
        
        # Extract the class data
        loc_dct=pickle.loads(sb)

        if loc_dct["o2sclpy_version"]!=version:
            raise ValueError("In function interpm_tf_dnn::load() "+
                             "Cannot read files with version "+
                             loc_dct["o2sclpy_version"])
        self.verbose=loc_dct["verbose"]
        self.outformat=loc_dct["outformat"]
        self.transform_in=loc_dct["transform_in"]
        self.transform_out=loc_dct["transform_out"]
        self.nd_in=loc_dct["nd_in"]
        self.nd_out=loc_dct["nd_out"]
        self.SS1=loc_dct["SS1"]
        self.SS2=loc_dct["SS2"]

        return
        
