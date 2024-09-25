#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2022-2024, Satyajit Roy, Mahamudul Hasan Anik, and
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
from o2sclpy.utils import string_to_dict2

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
        self.transform_in=0
        self.transform_out=0
        self.SS1=0
        self.SS2=0
        self.alpha=0
        self.random_state=0

    def save(self):
        """
        Save the interpolation settings to a string and return it
        """
        import pickle
        
        loc_dct={"verbose": self.verbose,
                 "kernel": self.kernel,
                 "outformat": self.outformat,
                 "transform_in": self.transform_in,
                 "transform_out": self.transform_out,
                 "SS1": self.SS1,
                 "SS2": self.SS2,
                 "alpha": self.alpha,
                 "random_state": self.random_state}
        params=self.gp.get_params(deep=True)
        return pickle.dumps((loc_dct,params))

    def load(self,s):
        """
        Load the interpolation settings from a string
        """
        import pickle
        from sklearn.gaussian_process import GaussianProcessRegressor
        
        tup=pickle.loads(s)
        loc_dct=tup[0]
        self.verbose=loc_dct["verbose"]
        self.kernel=loc_dct["kernel"]
        self.outformat=loc_dct["outformat"]
        self.transform_in=loc_dct["transform_in"]
        self.transform_out=loc_dct["transform_out"]
        self.SS1=loc_dct["SS1"]
        self.SS2=loc_dct["SS2"]
        self.alpha=loc_dct["alpha"]
        self.random_state=loc_dct["random_state"]
        
        func=GaussianProcessRegressor
        self.gp=func(normalize_y=True,
                     kernel=self.kernel,alpha=self.alpha,
                     random_state=self.random_state)
        self.gp.set_params(**(tup[1]))
        
        return
        
    def set_data(self,in_data,out_data,
                 kernel='1.0*RBF(1.0,(1e-2,1e2))',test_size=0.0,
                 normalize_y=True,transform_in='none',alpha=1.0e-10,
                 transform_out='none',outformat='numpy',verbose=0,
                 random_state=None):
        """
        Set the input and output data to train the interpolator
        """

        if verbose>0:
            print('interpm_sklearn_gp::set_data():')
            print('  kernel:',kernel)
            print('  normalize_y:',normalize_y)
            print('  transform_in:',transform_in)
            print('  transform_out:',transform_out)
            print('  outformat:',outformat)
            print('  alpha:',alpha)
            print('  random_state:',random_state)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))

        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import RBF, DotProduct
        from sklearn.gaussian_process.kernels import RationalQuadratic
        from sklearn.gaussian_process.kernels import Matern, WhiteKernel
        from sklearn.gaussian_process.kernels import PairwiseKernel
        from sklearn.gaussian_process.kernels import CompoundKernel
        from sklearn.gaussian_process.kernels import ConstantKernel
        from sklearn.gaussian_process.kernels import ExpSineSquared
        from sklearn.gaussian_process.kernels import Exponentiation
        from sklearn.gaussian_process.kernels import Product
        from sklearn.gaussian_process.kernels import Hyperparameter
        from sklearn.gaussian_process.kernels import Sum, WhiteKernel

        try:
            self.kernel=eval(kernel)
        except Exception as e:
            print('Exception in interpm_sklearn_gp::set_data()',
                  'at kernel eval.',e)
        self.outformat=outformat
        self.alpha=alpha
        self.random_state=random_state
        self.verbose=verbose
        self.transform_in=transform_in
        self.transform_out=transform_out

        # ----------------------------------------------------------
        # Handle the data transformations
        
        from sklearn.preprocessing import QuantileTransformer
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.preprocessing import StandardScaler
        
        if self.transform_in=='moto':
            self.SS1=MinMaxScaler(feature_range=(-1,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='quant':
            self.SS1=QuantileTransformer(n_quantiles=in_data.shape[0])
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='standard':
            self.SS1=StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
            
        if self.transform_out=='moto':
            self.SS2=MinMaxScaler(feature_range=(-1,1))
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='quant':
            self.SS2=QuantileTransformer(n_quantiles=out_data.shape[0])
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='standard':
            self.SS2=StandardScaler()
            out_data_trans=self.SS2.fit_transform(out_data)
        else:
            out_data_trans=out_data

        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                in_train,in_test,out_train,out_test=train_test_split(
                    in_data_trans,out_data_trans,test_size=test_size,
                    random_state=self.random_state)
            except Exception as e:
                print('Exception in interpm_sklearn_gp::set_data()',
                      'at test_train_split().',e)
        else:
            in_train=in_data_trans
            out_train=out_data_trans
            
        try:
            func=GaussianProcessRegressor
            self.gp=func(normalize_y=True,
                         kernel=self.kernel,alpha=self.alpha,
                         random_state=self.random_state).fit(in_train,out_train)
        except Exception as e:
            print('Exception in interpm_sklearn_gp::set_data()',
                  'at fit().',e)

        if test_size>0.0:
            print('score:',self.gp.score(in_test,out_test))

        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        ktemp=''
        if options.find('kernel=')!=-1:
            #print('old options:',options)
            ktemp=options[options.find('kernel=')+7:]
            options=options[:options.find('kernel=')]
            if options[-1:]==',':
                options=options[:-1]
            #print('new options:')
            #print(' ',ktemp)
            #print(' ',options)
        dct=string_to_dict2(options,list_of_ints=['verbose'],
                            list_of_floats=['test_size','alpha'],
                            list_of_bools=['normalize_y'])
        if ktemp!='':
            dct["kernel"]=ktemp
        print('interpm_sklearn_gp::set_data_str():')
        print('  string:',options)
        print('  dictionary:',dct)
              
        self.set_data(in_data,out_data,**dct)

        return
    
    def eval(self,v):
        """
        Evaluate the GP at point ``v``.
        """

        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v.reshape(1,-1))
            else:
                v_trans=v.reshape(1,-1)
        except Exception as e:
            print(('Exception at input transformation '+
                   'in interpm_sklearn_gp::eval():'),e)

        try:
            # AWS, 3/27/24: Keep in mind that o2scl::interpm_python.eval()
            # expects the return type to be a numpy array. 
            yp=self.gp.predict(v_trans)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_gp::eval():'),e)

        yp_trans=0
        try:
            if self.transform_out!='none':
                yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_sklearn_gp::eval():'),e)
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans[0].tolist()
        if yp_trans.ndim==1:
            if self.verbose>1:
                print('interpm_sklearn_gp::eval():',
                      'ndim=1 mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return numpy.ascontiguousarray(yp_trans)
        if self.verbose>1:
            print('interpm_sklearn_gp::eval():',
                  'array mode type(yp[0]),v,yp[0]:',
                  type(yp_trans[0]),v,yp_trans[0])
        return numpy.ascontiguousarray(yp_trans[0])

    def eval_list(self,v):
        """
        Evaluate the GP at point ``v``.
        """

        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v)
            else:
                v_trans=v
        except Exception as e:
            print(('Exception at input transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        try:
            yp=self.gp.predict(v)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        yp_trans=0
        try:
            if self.transform_out!='none':
                yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        if self.verbose>1:
            print('interpm_sklearn_gp::eval_list():',
                  'array mode type(yp),v,yp:',
                  type(yp_trans),v,yp_trans)
        return numpy.ascontiguousarray(yp_trans)

    def eval_unc(self,v):
        """
        Evaluate the GP and its uncertainty at point ``v``.

        # AWS, 3/27/24: Keep in mind that
        # o2scl::interpm_python.eval_unc() expects the return type to
        # be a tuple of numpy arrays. 
        """

        if self.transform_in!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print(('Exception at input transformation '+
                       'in interpm_sklearn_gp:'),
                      e)
        else:
            v_trans=v.reshape(1,-1)
            
        yp,std=self.gp.predict(v_trans,return_std=True)
        
        if self.transform_out!='none':
            try:
                yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
                std_trans=self.SS2.inverse_transform(std.reshape(-1,1))
            except Exception as e:
                print('Exception 6 in interpm_sklearn_gp:',e)
        else:
            yp_trans=yp
            std_trans=std
    
        if self.outformat=='list':
            return yp_trans[0].tolist(),std_trans[0].tolist()
        if yp_trans.ndim==1:
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_unc(): type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return (numpy.ascontiguousarray(yp_trans),
                    numpy.ascontiguousarray(std_trans))
        if self.verbose>1:
            print('interpm_sklearn_gp::eval_unc(): type(yp[0]),v,yp[0]:',
                  type(yp_trans[0]),v,yp_trans[0])
        return (numpy.ascontiguousarray(yp_trans[0]),
                numpy.ascontiguousarray(std_trans[0]))

class interpm_sklearn_dtr:
    """
    Interpolate one or many multidimensional data sets using
    scikit-learn's decision tree regression.
    """

    def __init__(self):
        self.dtr=0
        self.verbose=0
        self.outformat='numpy'
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 test_size=0.0,criterion='squared_error',splitter='best',
                 max_depth=None,random_state=None):
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        
        if self.verbose>0:
            print('interpm_sklearn_dtr::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))

        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data,out_data,test_size=test_size)
            except Exception as e:
                print('Exception in interpm_sklearn_dtr::set_data()',
                      'at test_train_split().',e)
        else:
            x_train=in_data
            y_train=out_data
            
        try:
            from sklearn.tree import DecisionTreeRegressor
            model=DecisionTreeRegressor(criterion=criterion, 
                                        splitter=splitter,
                                        max_depth=max_depth,
                                        random_state=random_state)
        except Exception as e:
            print('Exception in interpm_sklearn_dtr::set_data()',
                  'at model definition.',e)

        try:
            model.fit(x_train,y_train)      
        except Exception as e:
            print('Exception in interpm_sklearn_dtr::set_data()',
                  'at model fitting.',e)
            
        self.dtr=model

        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['verbose',
                                                  'random_state'],
                            list_of_floats=['test_size'])
        print('String:',options,'Dictionary:',dct)

        self.set_data(in_data,out_data,**dct)

        return
    
    def eval(self,v):
        """
        Evaluate the regression at point ``v``.
        """

        try:
            pred=self.dtr.predict([v])
        except Exception as e:
            print('Exception 4 in interpm_sklearn_dtr:',e)
    
        if self.outformat=='list':
            return pred.tolist()

        if pred.ndim==1:
            
            if self.verbose>1:
                print('interpm_sklearn_dtr::eval():',
                      'type(pred),pred:',
                      type(pred),pred)
                    
            return numpy.ascontiguousarray(pred)
        
        if self.verbose>1:
            print('interpm_sklearn_dtr::eval():',
                  'type(pred[0]),pred[0]:',
                  type(pred[0]),pred[0])

        return numpy.ascontiguousarray(pred)

    def eval_list(self,v):
        """
        Evaluate the GP at point ``v``.
        """

        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v)
            else:
                v_trans=v
        except Exception as e:
            print(('Exception at input transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        try:
            yp=self.dtr.predict([v])
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        yp_trans=0
        try:
            if self.transform_out!='none':
                yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        if self.verbose>1:
            print('interpm_sklearn_gp::eval_list():',
                  'array mode type(yp),v,yp:',
                  type(yp_trans),v,yp_trans)
        return numpy.ascontiguousarray(yp_trans)


class interpm_sklearn_mlpr:
    """
    Interpolate one or many multidimensional data sets using
    scikit-learn's multi-layer perceptron regressor.
    """

    def __init__(self):
        self.mlpr=0
        self.verbose=0
        self.outformat='numpy'
        self.transform_in=0
        self.transform_out=0
        self.SS1=0
        self.SS2=0
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',test_size=0.0,
                 hlayers=(100,),activation='relu',transform_in='none',
                 transform_out='none',
                 solver='adam',alpha=0.0001,batch_size='auto', 
                 learning_rate='adaptive',max_iter=500,
                 random_state=1,verbose=0,early_stopping=True,
                 n_iter_no_change=10):
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        self.transform_out=transform_out
        
        if self.verbose>0:
            print('interpm_sklearn_mlpr::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  solver:',solver)

        # ----------------------------------------------------------
        # Handle the data transformations
        
        from sklearn.preprocessing import QuantileTransformer
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.preprocessing import StandardScaler
        
        if self.transform_in=='moto':
            self.SS1=MinMaxScaler(feature_range=(-1,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='quant':
            self.SS1=QuantileTransformer(n_quantiles=in_data.shape[0])
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='standard':
            self.SS1=StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
            
        if self.transform_out=='moto':
            self.SS2=MinMaxScaler(feature_range=(-1,1))
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='quant':
            self.SS2=QuantileTransformer(n_quantiles=out_data.shape[0])
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='standard':
            self.SS2=StandardScaler()
            out_data_trans=self.SS2.fit_transform(out_data)
        else:
            out_data_trans=out_data

        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                in_train,in_test,out_train,out_test=train_test_split(
                    in_data_trans,out_data_trans,test_size=test_size)
            except Exception as e:
                print('Exception in interpm_sklearn_mlpr::set_data()',
                      'at test_train_split().',e)
        else:
            in_train=in_data_trans
            out_train=out_data_trans
            
        try:
            from sklearn.neural_network import MLPRegressor
            self.mlpr=MLPRegressor(hidden_layer_sizes=hlayers, 
                 activation=activation,solver=solver, 
                 alpha=alpha,batch_size=batch_size, 
                 learning_rate=learning_rate,max_iter=max_iter,  
                 random_state=random_state,verbose=verbose, 
                 early_stopping=early_stopping, 
                 n_iter_no_change=n_iter_no_change).fit(in_train,out_train)
        except Exception as e:
            print('Exception in interpm_sklearn_mlpr::set_data()',
                  'at fit().',e)

        if test_size>0.0:
            print('score:',self.mlpr.score(in_test,out_test))

        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['verbose',
                                                  'random_state',
                                                  'max_iter',
                                                  'n_iter_no_change'],
                            list_of_floats=['test_size','alpha'],
                            list_of_bools=['early_stopping'])

        if "hlayers" in dct:
            htemp=dct["hlayers"]
            htemp=htemp[1:-1]
            htemp=htemp.split(',')
            htemp2=[]
            for i in range(0,len(htemp)):
                htemp2.append(int(htemp[i]))
            dct["hlayers"]=numpy.array(htemp2)

        print('String:',options,'Dictionary:',dct)
        
        self.set_data(in_data,out_data,**dct)

        return
    
    def eval(self,v):
        """
        Evaluate the MLP at point ``v``.
        """

        if self.transform_in!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print(('Exception at input transformation '+
                       'in interpm_sklearn_mlpr:'),
                      e)
        else:
            v_trans=v.reshape(1,-1)
            
        yp=self.mlpr.predict(v_trans)
        
        if self.transform_out!='none':
            try:
                yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
            except Exception as e:
                print('Exception 5 in interpm_sklearn_mlpr:',e)
        else:
            yp_trans=yp
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_mlpr::eval():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans[0].tolist()
        if yp_trans.ndim==1:
            if self.verbose>1:
                print('interpm_sklearn_mlpr::eval():',
                      'ndim=1 mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return numpy.ascontiguousarray(yp_trans)
        if self.verbose>1:
            print('interpm_sklearn_mlpr::eval():',
                  'array mode type(yp[0]),v,yp[0]:',
                  type(yp_trans[0]),v,yp_trans[0])
        return numpy.ascontiguousarray(yp_trans[0])
    
    def eval_list(self,v):
        """
        Evaluate the GP at point ``v``.
        """

        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v)
            else:
                v_trans=v
        except Exception as e:
            print(('Exception at input transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        try:
            yp=self.mlpr.predict(v_trans)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        yp_trans=0
        try:
            if self.transform_out!='none':
                yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        if self.verbose>1:
            print('interpm_sklearn_gp::eval_list():',
                  'array mode type(yp),v,yp:',
                  type(yp_trans),v,yp_trans)
        return numpy.ascontiguousarray(yp_trans)

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
        self.transform_in=0
        self.transform_out=0
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 activations=['relu','relu'],
                 batch_size=None,epochs=100,
                 transform_in='none',transform_out='none',
                 test_size=0.0,evaluate=False,
                 hlayers=[8,8],loss='mean_squared_error',
                 es_min_delta=1.0e-4,es_patience=100,es_start=50):
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
            print('  transform_in:',transform_in)
            print('  transform_out:',transform_out)
            print('  epochs:',epochs)
            print('  test_size:',test_size)

        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        self.transform_out=transform_out

        # ----------------------------------------------------------
        # Handle the data transformations
        
        from sklearn.preprocessing import QuantileTransformer
        from sklearn.preprocessing import MinMaxScaler
        if self.transform_in=='moto':
            self.SS1=MinMaxScaler(feature_range=(-1,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='quant':
            self.SS1=QuantileTransformer(n_quantiles=in_data.shape[0])
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='standard':
            self.SS1=StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
            
        if self.transform_out=='moto':
            self.SS2=MinMaxScaler(feature_range=(-1,1))
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='quant':
            self.SS2=QuantileTransformer(n_quantiles=out_data.shape[0])
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='standard':
            self.SS2=StandardScaler()
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
        
        if self.verbose>0:
            print('summary:',model.summary())

        try:
            from keras.callbacks import EarlyStopping

            early_stopping=EarlyStopping(monitor=loss,
                                         min_delta=es_min_delta,
                                         patience=es_patience,
                                         verbose=self.verbose,
                                         restore_best_weights=True,
                                         start_from_epoch=es_start,
                                         mode='min')
            model.compile(loss=loss,optimizer='adam')
                
            if test_size>0.0:
                # Fit the model to training data
                model.fit(x_train,y_train,batch_size=batch_size,
                          epochs=epochs,validation_data=(x_test,y_test),
                          verbose=self.verbose,
                          callbacks=[early_stopping])
                          
            else:
                # Fit the model to training data
                model.fit(x_train,y_train,batch_size=batch_size,
                          epochs=epochs,verbose=self.verbose,
                          callbacks=[early_stopping])
                
        except Exception as e:
            print('Exception in interpm_tf_dnn::set_data()',
                  'at model fitting.',e)

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

        return
    
    def eval(self,v):
        """
        Evaluate the NN at point ``v``.
        """

        if self.transform_in!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print('Exception at input transformation in interpm_tf_dnn:',
                      e)
        else:
            v_trans=v.reshape(1,-1)

        try:
            pred=self.dnn.predict(v_trans, verbose=self.verbose)
        except Exception as e:
            print('Exception 4 in interpm_tf_dnn:',e)
            
        if self.transform_out!='none':
            try:
                pred_trans=self.SS2.inverse_transform(pred)
            except Exception as e:
                print('Exception 5 in interpm_tf_dnn:',e)
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
        return self.eval(v)
        
    def eval_list(self,v):
        """
        Evaluate the GP at point ``v``.
        """

        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v)
            else:
                v_trans=v
        except Exception as e:
            print(('Exception at input transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        try:
            yp=self.dnn.predict(v_trans, verbose=self.verbose)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_gp::eval_list():'),e)

        yp_trans=0
        try:
            if self.transform_out!='none':
                yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_sklearn_gp::eval_list():'),e)
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        if self.verbose>1:
            print('interpm_sklearn_gp::eval_list():',
                  'array mode type(yp),v,yp:',
                  type(yp_trans),v,yp_trans)
        return numpy.ascontiguousarray(yp_trans)

    
