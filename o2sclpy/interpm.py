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

import numpy
from o2sclpy.utils import string_to_dict2
from o2sclpy.hdf import *
from o2sclpy.doc_data import version

class interpm_sklearn_gp:
    """
    Interpolate one or many multimensional data sets using a 
    Gaussian process from scikit-learn

    See https://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessRegressor.html .

    AWS, 3/12/25: I think sklearn uses the log of the
    marginal likelihood as the optimization function.

    The variables ``verbose`` and ``outformat`` can be changed
    at any time.
    
    .. todo:: * Calculate derivatives
              * Allow sampling, as done in interpm_krige
              * Allow different minimizers?

    """

    verbose=0
    """
    Verbosity parameter (default 0)
    """
    outformat='native'
    """
    Output format, either 'native', 'c++', or 'list' (default 'native')
    """
    score=0.0
    """
    The most recent score value given a non-zero test size
    returned by set_data()
    """

    def __init__(self):
        self.gp=0
        self.kernel=0
        self.transform_in=0
        self.SS1=0
        self.alpha=0
        self.random_state=0
        self.normalize_y=True

    def set_data(self,in_data,out_data,kernel=None,test_size=0.0,
                 normalize_y=True,transform_in='none',alpha=1.0e-10,
                 outformat='native',verbose=0,random_state=None):
                 
        """Set the input and output data to train the Gaussian
        process. The variable in_data should be a numpy array with
        shape ``(n_points,in_dim)`` and out_data should be a numpy
        array with shape ``(n_points,out_dim)``.

        If kernel is ``None``, then the default kernel,
        ``1.0*RBF(1.0,(1e-2,1e2))`` is used.

        The value ``alpha`` is added to the diagonal elements of the
        kernel matrix during fitting.

        """
        if verbose>0:
            print('interpm_sklearn_gp::set_data():')
            print('  kernel:',kernel)
            print('  normalize_y:',normalize_y)
            print('  transform_in:',transform_in)
            print('  outformat:',outformat)
            print('  alpha:',alpha)
            print('  random_state:',random_state)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))

        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import RBF

        if kernel==None:
            self.kernel=1.0*RBF(1.0,(1e-2,1e2))
        else:
            self.kernel=kernel
        self.outformat=outformat
        self.alpha=alpha
        self.random_state=random_state
        self.verbose=verbose
        self.transform_in=transform_in
        self.normalize_y=normalize_y

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
            
        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                in_train,in_test,out_train,out_test=train_test_split(
                    in_data_trans,out_data,test_size=test_size,
                    random_state=self.random_state)
            except Exception as e:
                print('Exception in interpm_sklearn_gp::set_data()',
                      'at test_train_split().',e)
                raise
        else:
            in_train=in_data_trans
            out_train=out_data

        # AWS 3/9/25: This is an alternative to the sklearn
        # optimizer which allows for some configuration,
        # but it prevents pickling, so this is commented out
        # for now until I figure out what to do with it.
        # 
        #import scipy
        #def optimizer(obj_func,x0,bounds):
        #    res=scipy.optimize.minimize(
        #        obj_func,x0,bounds=bounds,method="L-BFGS-B",jac=True,
        #        options={"maxiter": 10000})
        #    return res.x,res.fun
        
        try:
            func=GaussianProcessRegressor
            self.gp=func(normalize_y=self.normalize_y,
                         kernel=self.kernel,alpha=self.alpha,
                         random_state=self.random_state)
            self.gp.fit(in_train,out_train)
        except Exception as e:
            print('Exception in interpm_sklearn_gp::set_data()',
                  'at fit().',e)
            raise

        if test_size>0.0:
            self.score=self.gp.score(in_test,out_test)
            return self.score

        return
    
    def set_data_str(self,in_data,out_data,options):
        """Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.

        The GP kernel, if specified, should be the last option
        specified in the string (this enables easier parsing of the
        option string). The eval() function is used to convert the
        string to a sklearn kernel.

        """
        from sklearn.gaussian_process.kernels import RBF, DotProduct
        from sklearn.gaussian_process.kernels import RationalQuadratic
        from sklearn.gaussian_process.kernels import Matern, WhiteKernel
        from sklearn.gaussian_process.kernels import PairwiseKernel
        from sklearn.gaussian_process.kernels import CompoundKernel
        from sklearn.gaussian_process.kernels import ConstantKernel
        from sklearn.gaussian_process.kernels import ExpSineSquared
        from sklearn.gaussian_process.kernels import Exponentiation
        from sklearn.gaussian_process.kernels import Product, Sum
        from sklearn.gaussian_process.kernels import Hyperparameter
        
        try:
            ktemp=''
            if options.find('kernel=')!=-1:
                # Extract the kernel from the string to process it
                # separately
                ktemp=options[options.find('kernel=')+7:]
                options=options[:options.find('kernel=')]
                if options[-1:]==',':
                    options=options[:-1]
            dct=string_to_dict2(options,list_of_ints=['verbose',
                                                      'random_state'],
                                list_of_floats=['test_size','alpha'],
                                list_of_bools=['normalize_y'])
            if ktemp!='':
                dct["kernel"]=eval(ktemp)
            if "verbose" in dct and dct["verbose"]>0:
                print('interpm_sklearn_gp::set_data_str():')
                print('  string:',options)
                print('  dictionary:',dct)
        except Exception as e:
            print('Exception in interpm_sklearn_gp::set_data_str()',
                  'at fit().',e)
            raise
              
        return self.set_data(in_data,out_data,**dct)
    
    def eval(self,v):
        """
        Evaluate the GP at point ``v``.

        The input ``v`` should be a one-dimensional numpy array
        and the output is a one-dimensional numpy array, unless
        outformat is ``list``, in which case the output is a
        Python list.
        
        """

        # The sklearn transformers require two-dimensional
        # arrays as inputs and outputs.
        
        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v.reshape(1,-1))
            else:
                v_trans=v.reshape(1,-1)
        except Exception as e:
            print(('Exception at input transformation '+
                   'in interpm_sklearn_gp::eval():'),e)
            raise

        # The sklearn GPR object expects the input to be a
        # two-dimensional numpy array.
        
        try:
            yp=self.gp.predict(v_trans)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_gp::eval():'),e)
            raise

        # The output of the sklearn GPR object is either one- or
        # two-dimensional, depending on the number of outputs.
        # We don't include a 'transform_out' option since the
        # GPR class already has a 'normalize_y' option.

        yp_trans=yp
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            if yp_trans.ndim==1:
                return yp_trans.tolist()
            return yp_trans[0].tolist()
        # Return a one-dimensional numpy array in either case
        if yp_trans.ndim==1:
            if self.verbose>1:
                print('interpm_sklearn_gp::eval():',
                      'ndim=1 mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans
        if self.verbose>1:
            print('interpm_sklearn_gp::eval():',
                  'array mode type(yp[0]),v,yp[0]:',
                  type(yp_trans[0]),v,yp_trans[0])
        return yp_trans[0]

    def eval_list(self,v):
        """Evaluate the GP at the list of points given in ``v``.
        The input ``v`` should be a two-dimensional numpy
        array of size ``(n_points,n_inputs)``.

        If ``outformat`` is ``native``, then the output is a
        two-dimensional numpy array. If ``outformat`` is ``list``,
        then the output is a list. If ``outformat`` is ``c++``, then
        the output is a continuous one-dimensional numpy array.
        
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
            raise

        try:
            yp=self.gp.predict(v_trans)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_gp::eval_list():'),e)
            raise

        yp_trans=yp
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        elif self.outformat=='c++':
            if self.verbose>1:
                print('interpm_sklearn_gp::eval_list():',
                      'array mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return numpy.ascontiguousarray(yp_trans)
        return yp_trans

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
                raise
        else:
            v_trans=v.reshape(1,-1)
            
        yp,std=self.gp.predict(v_trans,return_std=True)
        
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

    def save(self,filename,obj_name):
        """Save the interpolation settings to an HDF5 file.

        This function uses the sklearn get_params() function to obtain
        the sklearn parameters. A tuple is created using the class
        parameters and the sklearn parameters and this tuple is
        pickled to a string. Finally, this function stores that string
        with name ``obj_name`` to the HDF5 file named ``filename``.

        """
        import pickle

        # Construct dictionary of class data
        loc_dct={"o2sclpy_version": version,
                 "verbose": self.verbose,
                 "kernel": self.kernel,
                 "outformat": self.outformat,
                 "transform_in": self.transform_in,
                 "SS1": self.SS1,
                 "alpha": self.alpha,
                 "random_state": self.random_state,
                 "normalize_y": self.normalize_y}

        # Create a string from a tuple of the dictionary and the GPR
        # object
        byte_string=pickle.dumps((loc_dct,self.gp))

        # Write string to an HDF5 file
        hf=o2sclpy.hdf_file()
        hf.open_or_create(filename)
        hf.sets(obj_name,byte_string)
        hf.close()

        return
    
    def load(self,filename,obj_name):
        """Load the interpolation settings from a string named
        ``obj_name`` stored in an HDF5 file named ``filename``.

        """
        import pickle
        from sklearn.gaussian_process import GaussianProcessRegressor
        
        # Read string from file
        hf=o2sclpy.hdf_file()
        hf.open(filename)
        s=o2sclpy.std_string()
        hf.gets(obj_name,s)
        hf.close()
        # Convert to a Python bytes object
        sb=s.to_bytes()

        # Extract the tuple
        tup=pickle.loads(sb)

        # Set the class data
        loc_dct=tup[0]
        if loc_dct["o2sclpy_version"]!=version:
            raise ValueError("In function interpm_sklearn_gp::load() "+
                             "Cannot read files with version "+
                             loc_dct["o2sclpy_version"])
        self.verbose=loc_dct["verbose"]
        self.kernel=loc_dct["kernel"]
        self.outformat=loc_dct["outformat"]
        self.transform_in=loc_dct["transform_in"]
        self.SS1=loc_dct["SS1"]
        self.alpha=loc_dct["alpha"]
        self.random_state=loc_dct["random_state"]
        self.normalize_y=loc_dct["normalize_y"]

        # Set the GPR object
        self.gp=tup[1]

        return
        
class interpm_sklearn_dtr:
    """
    Interpolate one or many multidimensional data sets using
    scikit-learn's decision tree regression.

    See https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html .
    """

    verbose=0
    """
    Verbosity parameter (default 0)
    """
    outformat='numpy'
    """
    Output format, either 'native', 'c++', or 'list' (default 'native')
    """
    score=0.0
    """
    The most recent score value given a non-zero test size
    returned by set_data()
    """
    
    def __init__(self):
        self.dtr=0
        self.transform_in=0
        self.transform_out=0
        self.SS1=0
        self.SS2=0
        self.nd_in=0
        self.nd_out=0
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 test_size=0.0,criterion='squared_error',splitter='best',
                 transform_in='none',transform_out='none',
                 max_depth=None,random_state=None):
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        self.transform_out=transform_out
        self.nd_in=numpy.shape(in_data)[1]
        self.nd_out=numpy.shape(out_data)[1]
        
        if self.verbose>0:
            print('interpm_sklearn_dtr::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  transform_in:',transform_in)
            print('  transform_out:',transform_out)

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
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data_trans,out_data_trans,test_size=test_size)
            except Exception as e:
                print('Exception in interpm_sklearn_dtr::set_data()',
                      'at test_train_split().',e)
                raise
        else:
            x_train=in_data_trans
            y_train=out_data_trans
            
        try:
            from sklearn.tree import DecisionTreeRegressor
            self.dtr=DecisionTreeRegressor(criterion=criterion, 
                                        splitter=splitter,
                                        max_depth=max_depth,
                                        random_state=random_state)
        except Exception as e:
            print('Exception in interpm_sklearn_dtr::set_data()',
                  'at model definition.',e)
            raise

        try:
            self.dtr.fit(x_train,y_train)      

            if test_size>0.0:
                self.score=self.dtr.score(x_test,y_test)

        except Exception as e:
            print('Exception in interpm_sklearn_dtr::set_data()',
                  'at model fitting.',e)
            raise

        if test_size>0.0:
            return self.score
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

        if self.transform_in!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print(('Exception at input transformation '+
                       'in interpm_sklearn_dtr:'),
                      e)
                raise
        else:
            v_trans=v.reshape(1,-1)

        yp=self.dtr.predict(v_trans)
        
        if self.transform_out!='none':
            try:
                if yp.ndim==1:
                    yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
                else:
                    yp_trans=self.SS2.inverse_transform(yp)
            except Exception as e:
                print('Exception 5 in interpm_sklearn_dtr:',e)
                raise
        else:
            yp_trans=yp

        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_dtr::eval():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans[0].tolist()
        if yp_trans.ndim==1:
            if self.verbose>1:
                print('interpm_sklearn_dtr::eval():',
                      'ndim=1 mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return numpy.ascontiguousarray(yp_trans)
            #return numpy.array(yp_trans)
        if self.verbose>1:
            print('interpm_sklearn_dtr::eval():',
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
                   'in interpm_sklearn_dtr::eval_list():'),e)
            raise

        try:
            yp=self.dtr.predict(v_trans)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_dtr::eval_list():'),e)
            raise

        yp_trans=0
        try:
            if self.transform_out!='none':
                if yp.ndim==1:
                    yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
                else:
                    yp_trans=self.SS2.inverse_transform(yp)
                if yp_trans.ndim==2 and len(yp_trans[0])==1:
                    yp_trans=yp_trans.reshape(1,-1)[0]
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_sklearn_dtr::eval_list():'),e)
            raise
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_dtr::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        if self.verbose>1:
            print('interpm_sklearn_dtr::eval_list():',
                  'array mode type(yp),v,yp:',
                  type(yp_trans),v,yp_trans)
        return numpy.ascontiguousarray(yp_trans)

    def save(self,filename,obj_name):
        """
        Save the interpolation settings to an HDF5 file
        """
        import pickle

        # Construct string
        loc_dct={"o2sclpy_version": version,
                 "verbose": self.verbose,
                 "transform_in": self.transform_in,
                 "transform_out": self.transform_out,
                 "SS1": self.SS1,
                 "SS2": self.SS2,
                 "outformat": self.outformat}
        byte_string=pickle.dumps((loc_dct,self.dtr))

        # Write to a file
        hf=o2sclpy.hdf_file()
        hf.open_or_create(filename)
        hf.sets(obj_name,byte_string)
        hf.close()

        return
    
    def load(self,filename,obj_name):
        """
        Load the interpolation settings from a file
        """
        import pickle
        
        # Read string from file
        hf=o2sclpy.hdf_file()
        hf.open(filename)
        s=o2sclpy.std_string()
        hf.gets(obj_name,s)
        hf.close()
        sb=s.to_bytes()

        tup=pickle.loads(sb)

        loc_dct=tup[0]
        if loc_dct["o2sclpy_version"]!=version:
            raise ValueError("In function interpm_sklearn_dtr::load() "+
                             "Cannot read files with version "+
                             loc_dct["o2sclpy_version"])
        self.verbose=loc_dct["verbose"]
        self.transform_in=loc_dct["transform_in"]
        self.transform_out=loc_dct["transform_out"]
        self.outformat=loc_dct["outformat"]
        self.SS1=loc_dct["SS1"]
        self.SS2=loc_dct["SS2"]

        self.dtr=tup[1]
        
        return
        

class interpm_sklearn_mlpr:
    """
    Interpolate one or many multidimensional data sets using
    scikit-learn's multi-layer perceptron regressor.
    """

    verbose=0
    """
    Verbosity parameter (default 0)
    """
    outformat='numpy'
    """
    Output format, either 'native', 'c++', or 'list' (default 'native')
    """
    score=0.0
    """
    The most recent score value given a non-zero test size
    returned by set_data()
    """
    
    def __init__(self):
        self.mlpr=0
        self.transform_in=0
        self.transform_out=0
        self.SS1=0
        self.SS2=0
        self.nd_in=0
        self.nd_out=0
        
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
        self.nd_in=numpy.shape(in_data)[1]
        self.nd_out=numpy.shape(out_data)[1]
        
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
                raise
        else:
            in_train=in_data_trans
            out_train=out_data_trans
            
        try:
            from sklearn.neural_network import MLPRegressor
            self.mlpr=MLPRegressor(hidden_layer_sizes=hlayers, 
                                   activation=activation,solver=solver, 
                                   batch_size=batch_size, 
                                   learning_rate=learning_rate,
                                   max_iter=max_iter,  
                                   random_state=random_state,
                                   verbose=verbose, 
                                   early_stopping=early_stopping, 
                                   n_iter_no_change=n_iter_no_change,
                                   alpha=alpha)
            if len(out_train[0])==1:
                self.mlpr.fit(in_train,out_train.ravel())
            else:
                self.mlpr.fit(in_train,out_train)
                
            if test_size>0.0:
                self.score=self.mlpr.score(in_test,out_test)

        except Exception as e:
            print('Exception in interpm_sklearn_mlpr::set_data()',
                  'at fit().',e)
            raise

        if test_size>0.0:
            if self.verbose>0:
                print('interpm_sklearn_mlpr::set_data(): score: %7.6e' %
                      (self.mlpr.score(in_test,out_test)))
            return self.score

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
                raise
        else:
            v_trans=v.reshape(1,-1)

        yp=self.mlpr.predict(v_trans)
        
        if self.transform_out!='none':
            try:
                if yp.ndim==1:
                    yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
                else:
                    yp_trans=self.SS2.inverse_transform(yp)
            except Exception as e:
                print('Exception 5 in interpm_sklearn_mlpr:',e)
                raise
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
            #return numpy.array(yp_trans)
        if self.verbose>1:
            print('interpm_sklearn_mlpr::eval():',
                  'array mode type(yp[0]),v,yp[0]:',
                  type(yp_trans[0]),v,yp_trans[0])
        return numpy.ascontiguousarray(yp_trans[0])
    
    def eval_unc(self,v):
        """
        Empty function because this interpolator does not currently
        provide uncertainties
        """
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
                   'in interpm_sklearn_mlpr::eval_list():'),e)
            raise

        try:
            yp=self.mlpr.predict(v_trans)
        except Exception as e:
            print(('Exception at prediction '+
                   'in interpm_sklearn_mlpr::eval_list():'),e)
            raise

        yp_trans=0
        try:
            if self.transform_out!='none':
                if yp.ndim==1:
                    yp_trans=self.SS2.inverse_transform(yp.reshape(-1,1))
                else:
                    yp_trans=self.SS2.inverse_transform(yp)
                if yp_trans.ndim==2 and len(yp_trans[0])==1:
                    yp_trans=yp_trans.reshape(1,-1)[0]
            else:
                yp_trans=yp
        except Exception as e:
            print(('Exception at output transformation '+
                   'in interpm_sklearn_mlpr::eval_list():'),e)
            raise
    
        if self.outformat=='list':
            if self.verbose>1:
                print('interpm_sklearn_mlpr::eval_list():',
                      'list mode type(yp),v,yp:',
                      type(yp_trans),v,yp_trans)
            return yp_trans.tolist()
        if self.verbose>1:
            print('interpm_sklearn_mlpr::eval_list():',
                  'array mode type(yp),v,yp:',
                  type(yp_trans),v,yp_trans)
        return numpy.ascontiguousarray(yp_trans)

    def save(self,filename,obj_name):
        """
        Save the interpolation settings to an HDF5 file
        """
        import pickle

        # Construct string
        loc_dct={"o2sclpy_version": version,
                 "verbose": self.verbose,
                 "outformat": self.outformat,
                 "transform_in": self.transform_in,
                 "transform_out": self.transform_out,
                 "SS1": self.SS1,
                 "SS2": self.SS2}
        byte_string=pickle.dumps((loc_dct,self.mlpr))

        # Write to a file
        hf=o2sclpy.hdf_file()
        hf.open_or_create(filename)
        hf.sets(obj_name,byte_string)
        hf.close()

        return
    
    def load(self,filename,obj_name):
        """
        Load the interpolation settings from a file
        """
        import pickle
        
        # Read string from file
        hf=o2sclpy.hdf_file()
        hf.open(filename)
        s=o2sclpy.std_string()
        hf.gets(obj_name,s)
        hf.close()
        sb=s.to_bytes()

        tup=pickle.loads(sb)
        
        loc_dct=tup[0]
        if loc_dct["o2sclpy_version"]!=version:
            raise ValueError("In function interpm_sklearn_mlpr::load() "+
                             "Cannot read files with version "+
                             loc_dct["o2sclpy_version"])
        self.verbose=loc_dct["verbose"]
        self.outformat=loc_dct["outformat"]
        self.transform_in=loc_dct["transform_in"]
        self.transform_out=loc_dct["transform_out"]
        self.SS1=loc_dct["SS1"]
        self.SS2=loc_dct["SS2"]
        
        self.mlpr=tup[1]

        return
        
class interpm_torch_dnn:

    verbose=0
    """
    Verbosity parameter (default 0)
    """
    outformat='numpy'
    """
    Output format, either 'native', 'c++', or 'list' (default 'native')
    """
    
    def __init__(self):
        self.dnn=0
        self.SS1=0
        self.SS2=0
        self.transform_in=0
        self.transform_out=0
        self.nd_in=0
        return

    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 hlayers=[8,8],epochs=100,transform_in='none',
                 transform_out='none',test_size=0.0,activation='relu'):

        from sklearn.model_selection import train_test_split
        import torch
        import torch.nn as nn
        import torch.optim as optim
        
        if verbose>0:
            print('interpm_torch_dnn::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  transform_in:',transform_in)
            print('  transform_out:',transform_out)
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
                print('Exception in interpm_torch_dnn::set_data()',
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
                print('Exception in interpm_torch_dnn::set_data()',
                      'at test_train_split().',e)
                raise
        else:
            x_train=in_data_trans
            y_train=out_data_trans

        n_pts=numpy.shape(x_train)[0]
        self.nd_in=numpy.shape(x_train)[1]
        nd_out=numpy.shape(y_train)[1]
        
        if self.verbose>0:
            print('nd_in,nd_out:',self.nd_in,nd_out)
            print('  Training DNN model.')

        class function_approx(nn.Module):
            
            def __init__(self,nd_in):
                super(function_approx,self).__init__()

                layers=[]
                layers.append(nn.Linear(nd_in,hlayers[0]))
                if activation=='relu':
                    layers.append(nn.Relu())
                elif activation=='tanh':
                    layers.append(nn.Tanh())
                for k in range(0,len(hlayers)-1):
                    layers.append(nn.Linear(hlayers[k],hlayers[k+1]))
                    if activation=='relu':
                        layers.append(nn.Relu())
                    elif activation=='tanh':
                        layers.append(nn.Tanh())
                layers.append(nn.Linear(hlayers[len(hlayers)-1],nd_out))
                self.model=nn.Sequential(*layers)
                
                return
            
            def forward(self,x):
                return self.model(x)

        # Convert numpy to torch, there's probably a better way...
        ten_in=torch.zeros((n_pts,self.nd_in))
        ten_out=torch.zeros((n_pts,nd_out))
        for i in range(0,n_pts):
            for j in range(0,self.nd_in):
                ten_in[i,j]=x_train[i,j]
            for j in range(0,nd_out):
                ten_out[i,j]=y_train[i,j]
                        
        self.dnn=function_approx(self.nd_in)
        crit=nn.MSELoss()
        opt=optim.Adam(self.dnn.parameters(),lr=0.01)

        for epoch in range(0,epochs):
            opt.zero_grad()
            pred=self.dnn(ten_in)
            loss=crit(pred,ten_out)
            loss.backward()
            opt.step()

            if self.verbose>0:
                print('Epoch',str(epoch+1)+'/'+str(epochs),
                      'loss %7.6e' % (loss.item()))
            
        return
    
    def eval(self,v):
        """
        Evaluate the NN at point ``v``.
        """

        if self.transform_in!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))[0]
            except Exception as e:
                print('Exception at input transformation ',
                      'in interpm_torch_dnn:',e)
                raise
        else:
            v_trans=v

        try:
            import torch
            ten_in=torch.zeros((1,self.nd_in))
            for j in range(0,self.nd_in):
                ten_in[0,j]=v_trans[j]
            pred=self.dnn(ten_in)
        except Exception as e:
            print('Exception 4 in interpm_torch_dnn:',e)
            raise
            
        if self.transform_out!='none':
            try:
                pred_trans=self.SS2.inverse_transform(pred.detach().numpy())
            except Exception as e:
                print('Exception 5 in interpm_torch_dnn:',e)
                raise
        else:
            pred_trans=pred.detach().numpy()
    
        if self.outformat=='list':
            return pred_trans.tolist()

        if pred_trans.ndim==1:
            
            if self.verbose>1:
                print('interpm_torch_dnn::eval():',
                      'type(pred_trans),pred_trans:',
                      type(pred_trans),pred_trans,pred_trans.ndim,
                      numpy.shape(pred_trans))
                
            return numpy.ascontiguousarray(pred_trans)
        
        if self.verbose>1:
            print('interpm_torch_dnn::eval():',
                  'type(pred_trans[0]),pred_trans[0]:',
                  type(pred_trans[0]),pred_trans[0],pred_trans.ndim,
                      numpy.shape(pred_trans))

        return numpy.ascontiguousarray(pred_trans[0])

    def eval_list(self,v):
        """
        Evaluate the NN at the list of points given in ``v``.
        """

        v_trans=0
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v)
            else:
                v_trans=v
        except Exception as e:
            print('Exception at input transformation ',
                  'in interpm_torch_dnn::eval_list():',e)
            raise

        try:
            import torch
            ten_in=torch.zeros((len(v),self.nd_in))
            for k in range(0,len(v)):
                for j in range(0,self.nd_in):
                    ten_in[k,j]=v_trans[k][j]
            pred=self.dnn(ten_in)
        except Exception as e:
            print('Exception at evaluation in '+
                  'interpm_torch_dnn::eval_list():',e)
            raise

        pred_trans=0
        try:
            if self.transform_out!='none':
                pred_trans=self.SS2.inverse_transform(pred.detach().numpy())
            else:
                pred_trans=pred.detach().numpy()
        except Exception as e:
            print('Exception at output transformation '+
                  'in interpm_torch_dnn::eval_list():',e)
            raise
    
        if self.outformat=='list':
            return pred_trans.tolist()

        # For a single output, torch outputs them in a column
        # vector, so we switch to a row vector.
        if pred_trans.ndim==2 and len(pred_trans[0])==1:
            pred_trans2=pred_trans.reshape(1,-1)[0]
        else:
            pred_trans2=pred_trans
        
        if self.verbose>1:
            print('interpm_torch_dnn::eval_list():',
                  'type(pred_trans2),pred_trans2:',
                  type(pred_trans2),pred_trans2)
            
        return numpy.ascontiguousarray(pred_trans2)

    def eval_unc(self,v):
        """
        Empty function because this interpolator does not currently
        provide uncertainties
        """
        return self.eval(v)
        
    def deriv(self,v,i):
        """
        Evaluate the derivative of the NN at point ``v`` with
        respect to the variable with index ``i``
        """

        if self.transform_in!='none':
            v_trans=0
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))[0]
            except Exception as e:
                print('Exception at input transformation in ',
                      'interpm_torch_dnn::deriv():',e)
                raise
        else:
            v_trans=v

        try:
            
            import torch
            ten_in=torch.zeros((1,self.nd_in))
            for j in range(0,self.nd_in):
                ten_in[0,j]=v_trans[j]
                
            ten_in.requires_grad_(True)
            pred=self.dnn(ten_in)
            pgrad=torch.autograd.grad(pred,ten_in,
                                      grad_outputs=torch.ones_like(pred),
                                      create_graph=True)
            # The grad function returns a tuple, and the gradient
            # is the first entry of that tuple.
            pgrad=pgrad[0][0][i]
            #print('pgrad',pgrad,type(pgrad))
            
        except Exception as e:
            print('Exception at model training',
                  'in interpm_torch_dnn::deriv():',e)
            raise
            
        if self.transform_out!='none':
            try:
                pgrad2=pgrad.detach().numpy()
                #print('hx',pgrad2,type(pgrad2),pgrad2.ndim,
                #numpy.shape(pgrad2))
                if pgrad2.ndim<=1:
                    pgrad2=pgrad2.reshape(-1,1)
                #print('hy',pgrad2,type(pgrad2),pgrad2.ndim,
                #numpy.shape(pgrad2))
                pgrad_trans=self.SS2.inverse_transform(pgrad2)
            except Exception as e:
                print('Exception at inverse transformation',
                      'in interpm_torch_dnn::deriv():',e)
                raise
        else:
            pgrad_trans=pgrad.detach().numpy()
    
        if self.outformat=='list':
            return pgrad_trans.tolist()

        if pgrad_trans.ndim==1:
            
            if self.verbose>1:
                print('interpm_torch_dnn::deriv():',
                      'type(pgrad_trans),pgrad_trans:',
                      type(pgrad_trans),pgrad_trans)
                    
            return numpy.ascontiguousarray(pgrad_trans)
        
        if self.verbose>1:
            print('interpm_torch_dnn::deriv():',
                  'type(pgrad_trans),pgrad_trans:',
                  type(pgrad_trans),pgrad_trans)

        return numpy.ascontiguousarray(pgrad_trans)

    def save(self,filename):
        """
        Save the interpolation settings to a file

        (No custom object support)
        """
        if filename[-3:]!='.pt':
            filename=filename+'.pt'
        import torch
        torch.save(self.dnn,filename)

        return
    
    def load(self,filename):
        """
        Load the interpolation settings from a file

        (No custom object support)
        """        
        if filename[-3:]!='.pt':
            filename=filename+'.pt'
        import torch
        torch.load(self.dnn,filename)

        return

class interpm_tf_dnn:
    """Interpolate one or many multimensional data sets using a
    neural network from TensorFlow

    This is a simple implementation of a neural network with
    early stopping. 

    The variables ``verbose`` and ``outformat`` can be changed
    at any time.
    
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

        self.dnn=0
        self.SS1=0
        self.SS2=0
        self.transform_in=0
        self.transform_out=0
        self.outformat='numpy'
        self.nd_in=0
        self.nd_out=0
        
        return

    def check_gpu(self):
        """
        Check if Tensorflow is likely to use the GPU
        """
        import tensorflow as tf
        try:
            with tf.device('/GPU:0'):
                a = tf.constant([[1.0, 2.0]])
                b = tf.constant([[3.0], [4.0]])
                c = tf.matmul(a, b)
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

        Some activation functions: 'relu', 'sigmoid', 'tanh'. If the
        number of activation functions specified in ``activations`` is
        smaller than the number of layers, then the activation
        function list is reused using the modulus operator.

        The keyword argument ``tf_logs`` specifies the value of
        the environment variable ``TF_CPP_MIN_LOG_LEVEL``.

        """

        from sklearn.model_selection import train_test_split
        import os
        os.environ['TF_ENABLE_ONEDNN_OPTS']=tf_onednn_opts
        os.environ['TF_CPP_MIN_LOG_LEVEL']=tf_logs
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
        
        self.nd_in=numpy.shape(in_data)[1]
        self.nd_out=numpy.shape(out_data)[1]

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
            raise
        
        if self.verbose>0:
            print('summary:',model.summary())

        try:
            from keras.callbacks import EarlyStopping
            import keras

            class loss_history(keras.callbacks.Callback):
                def on_train_begin(self,logs={}):
                    self.losses=[]
                def on_batch_end(self,batch,logs={}):
                    self.losses.append(logs.get('loss'))
            history=loss_history()

            # AWS, 3/9/25, changed from 'val_loss' to 'loss'
            # to fix warnings on stellar.
            #
            #early_stopping=EarlyStopping(monitor='val_loss',
            early_stopping=EarlyStopping(monitor='loss',
                                         min_delta=es_min_delta,
                                         patience=es_patience,
                                         verbose=self.verbose,
                                         restore_best_weights=True,
                                         start_from_epoch=es_start,
                                         mode='min')
            model.compile(loss=loss,optimizer='adam')

            # Convert numpy array to TensorFlow tensor
            x_tf=tf.convert_to_tensor(x_train)
            y_tf=tf.convert_to_tensor(y_train)
            
            if test_size>0.0:
                # Fit the model to training data
                model.fit(x_tf,y_tf,batch_size=batch_size,
                          epochs=epochs,validation_data=(x_test,y_test),
                          verbose=self.verbose,
                          callbacks=[history,early_stopping])
                          
            else:
                # Fit the model to training data
                model.fit(x_tf,y_tf,batch_size=batch_size,
                          epochs=epochs,verbose=self.verbose,
                          callbacks=[history,early_stopping])
                
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
        import tensorflow as tf

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
            v_tf=tf.convert_to_tensor(v_trans)
                
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
        import tensorflow as tf

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
            v_tf=tf.convert_to_tensor(v_trans)
            
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
        self.SS1=loc_dct["SS1"]
        self.SS2=loc_dct["SS2"]

        return
        
