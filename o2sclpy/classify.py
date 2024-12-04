#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2024-2025, Satyajit Roy and Andrew W. Steiner
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

class classify_sklearn_dtc:
    """
    Classify a data set using scikit-learn's decision tree classifier.
    """

    def __init__(self):
        self.dtc=0
        self.verbose=0
        self.outformat='numpy'
        self.criterion='gini'
        self.splitter='best'
        self.max_depth=None
        self.max_features=None
        self.random_state=None
        self.test_size=0.0
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 test_size=0.0,criterion='gini',splitter='best',
                 max_depth=None,max_features=None, 
                 random_state=None):
        """
        Set the input and output data to train the classifier
        """
        self.outformat=outformat
        self.verbose=verbose
        self.criterion=criterion
        self.splitter=splitter
        self.max_depth=max_depth
        self.max_features=max_features
        self.random_state=random_state
        self.test_size=test_size
        
        if self.verbose>0:
            print('classify_sklearn_dtc::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  verbose:',verbose)
            print('  criterion:',criterion)
            print('  splitter:',splitter)
            print('  max_depth:',max_depth)
            print('  max_features:',max_features)
            print('  random_state:',random_state)
            print('  test_size:',test_size)
           
        # ────────────────────────────────────────────────────────────
        # Perform the train/test split
        
        if self.test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data,out_data,test_size=self.test_size)
            except Exception as e:
                print('Exception in classify_sklearn_dtc::set_data()',
                      'at test_train_split().',e)
                raise
        else:
            x_train=in_data
            y_train=out_data
            
        # ────────────────────────────────────────────────────────────
        # Fit the classifier
        
        try:
            from sklearn.tree import DecisionTreeClassifier
            model=DecisionTreeClassifier(criterion=self.criterion, 
                                            splitter=self.splitter,
                                            max_depth=self.max_depth, 
                                            max_features=self.max_features,
                                            random_state=self.random_state)
        except Exception as e:
            print('Exception in classify_sklearn_dtc::set_data()',
                  'at model definition.',e)
            raise

        try:
            self.dtc=model.fit(x_train,y_train)      
        except Exception as e:
            print('Exception in classify_sklearn_dtc::set_data()',
                  'at model fitting.',e)
            raise
            
        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['max_depth',
                                                  'max_features',
                                                  'verbose'],
                            list_of_floats=['test_size','alpha'])

        if self.verbose>2:
            print('In classify_sklearn_dtc::set_data_str(): string:',
                  options,'Dictionary:',dct)
              
        try:
            self.set_data(in_data,out_data,**dct)
        except Exception as e:
            print('Exception in classify_sklearn_dtc::set_data_str()',e)
            raise

        return

    def eval(self,v):
        """Evaluate the classifier at point ``v``. If
        ``self.outformat`` is equal to ``list``, then the output is a
        Python list, otherwise, the output is a numpy array.
        """

        try:
            pred=self.dtc.predict([v])
        except Exception as e:
            print('Exception in classify_sklearn_dtc::eval():',e)
            raise
    
        if self.outformat=='list':
            return pred.tolist()
   
        if self.verbose>1:
            print('classify_sklearn_dtc::eval():',
                'type(pred),pred:',
                type(pred),pred)
                    
        return numpy.ascontiguousarray(pred)

    def eval_list(self,v):
        """
        Evaluate the classifier at the array of points stored in ``v``.
        """

        try:
            pred=self.dtc.predict(v)
        except Exception as e:
            print('Exception in classify_sklearn_dtc::eval_list():',e)
            raise
    
        if self.outformat=='list':
            return pred.tolist()
   
        if self.verbose>1:
            print('classify_sklearn_dtc::eval_list():',
                'type(pred),pred:',
                type(pred),pred)
                    
        return numpy.ascontiguousarray(pred)

    def save(self,filename,obj_prefix="classify_sklearn_dtc"):
        """
        Save the classifer to an HDF5 file named ``filename`` as a
        string named ``obj_prefix``. 
        """
        import pickle

        if len(obj_prefix)==0:
            raise ValueError("In classify_sklearn_dtc::save() "+
                             "object prefix cannot be empty.")
        
        loc_dct={"version": version,
                 "verbose": self.verbose,
                 "outformat": self.outformat,
                 "verbose": self.verbose,
                 "criterion": self.criterion,
                 "splitter": self.splitter,
                 "max_depth": self.max_depth,
                 "max_features": self.max_features,
                 "random_state": self.random_state,
                 "test_size": self.test_size}
        
        dct_string=pickle.dumps(loc_dct)
        byte_string=pickle.dumps(self.dtc)

        if self.verbose>2:
            print('In classify_sklearn_dtc::save().')
            print('  len(dct_string):',len(dct_string))
            print('  len(byte_string):',len(byte_string))
        
        hf=o2sclpy.hdf_file()
        hf.open_or_create(filename)
        hf.sets(obj_prefix+'_dct',dct_string)
        hf.sets(obj_prefix,byte_string)
        hf.close()

        return

    def load(self,filename,obj_prefix):
        """
        Load the classifer from an HDF5 file named ``filename`` as a
        string named ``obj_prefix``. 
        """
        import pickle

        hf=o2sclpy.hdf_file()
        hf.open(filename)
        s=o2sclpy.std_string()
        s2=o2sclpy.std_string()
        hf.gets(obj_prefix,s)
        hf.gets(obj_prefix+'_dct',s2)
        hf.close()
        sb=s.to_bytes()
        sb2=s2.to_bytes()

        if self.verbose>2:
            print('In classify_sklearn_dtc::load().')
            print('  len(sb):',len(sb))
            print('  len(sb2):',len(sb2))
            
        loc_dct=pickle.loads(sb2)
        if loc_dct["version"]!=version:
            raise ValueError("In function classify_sklearn_dtc::load() "+
                             "Cannot read files with version "+
                             loc_dct["version"])
        
        self.verbose=loc_dct["verbose"]
        self.outformat=loc_dct["outformat"]
        self.verbose=loc_dct["verbose"]
        self.criterion=loc_dct["criterion"]
        self.splitter=loc_dct["splitter"]
        self.max_depth=loc_dct["max_depth"]
        self.max_features=loc_dct["max_features"]
        self.random_state=loc_dct["random_state"]
        self.test_size=loc_dct["test_size"]
        
        self.dtc=pickle.loads(sb)

        return
    
class classify_sklearn_mlpc:
    """
    Classify a data set using scikit-learn's multi-layer
    perceptron classifier.
    """

    def __init__(self):
        self.mlpc=0
        self.verbose=0
        self.outformat='numpy'
        self.SS1=0
        self.transform_in='none'
        
        return
    
    def set_data(self,in_data,out_data,
                 transform_in='none',outformat='numpy',test_size=0.0,
                 hlayers=(100,),activation='relu',
                 solver='adam',alpha=0.0001,batch_size='auto', 
                 learning_rate='constant',max_iter=200,
                 random_state=None,verbose=False, 
                 early_stopping=False,n_iter_no_change=10,
                 tol=0.0001):
                 
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        
        if self.verbose>0:
            print('classify_sklearn_mlpc::set_data():')
            print('  outformat:',outformat)
            print('  transform_in:',transform_in)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  solver:',solver)
            
        # ────────────────────────────────────────────────────────────
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
            
        # ────────────────────────────────────────────────────────────
        # Perform the train/test split
        
        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data_trans,out_data,test_size=test_size)
            except Exception as e:
                print('Exception in classify_sklearn_mlpc::set_data()',
                      'at test_train_split().',e)
                raise
        else:
            x_train=in_data_trans
            y_train=out_data
            
        # ────────────────────────────────────────────────────────────
        # Fit the classifier
        
        try:
            from sklearn.neural_network import MLPClassifier
            self.mlpc=MLPClassifier(hidden_layer_sizes=hlayers, 
                                activation=activation,solver=solver, 
                                alpha=alpha,batch_size=batch_size, 
                                learning_rate=learning_rate,
                                max_iter=max_iter,  
                                random_state=random_state,verbose=verbose, 
                                early_stopping=early_stopping, 
                                n_iter_no_change=n_iter_no_change,
                                tol=tol)
        except Exception as e:
            print('Exception in classify_sklearn_mlpc::set_data()',
                  'at model().',e)
            raise
        try:
            y_train=y_train.reshape(y_train.shape[0])
            self.mlpc.fit(x_train,y_train)
        except Exception as e:
            print('Exception in classify_sklearn_mlpc::set_data()',
                  'at fit().',e)
            raise

        if test_size>0.0:
            print('score:',self.mlpc.score(x_test,y_test))

        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['verbose',
                                                  'max_iter',
                                                  'n_iter_no_change',
                                                  'random_state'],
                            list_of_floats=['test_size','alpha','tol'],
                            list_of_bools=['early_stopping'])
        
        if "hlayers" in dct:
            htemp=dct["hlayers"]
            htemp=htemp[1:-1]
            htemp=htemp.split(',')
            htemp2=[]
            for i in range(0,len(htemp)):
                htemp2.append(int(htemp[i]))
            dct["hlayers"]=htemp2
                
        if self.verbose>2:
            print('In classify_sklearn_mlpc::set_data_str(): string:',
                  options,'Dictionary:',dct)
              
        self.set_data(in_data,out_data,**dct)

        return
    
    def eval(self,v):
        """
        Evaluate the classifier at point ``v``.
        """

        if self.transform_in!='none':
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print('hx',self.transform_in)
                print('Exception 4 in classify_sklearn_mlpc:',e)
                raise
        else:
            v_trans=v.reshape(1,-1)

        pred=self.mlpc.predict(v_trans)
            
        if self.outformat=='list':
            return pred.tolist()

        if self.verbose>1:
            print('classify_sklearn_mlpc::eval():',
                'type(pred),pred:',
                type(pred),pred)

        return numpy.ascontiguousarray(pred)

    def eval_list(self,v):
        """
        Evaluate the classifier at the array of points stored in ``v``.
        """

        try:
            pred=self.mlpc.predict(v)
        except Exception as e:
            print('Exception in classify_sklearn_mlpc::eval_list():',e)
            raise
    
        if self.outformat=='list':
            return pred.tolist()
   
        if self.verbose>1:
            print('classify_sklearn_mlpc::eval_list():',
                'type(pred),pred:',
                type(pred),pred)
                    
        return numpy.ascontiguousarray(pred)

    def save(self,filename,obj_prefix="classify_sklearn_mlpc"):
        """
        Save the classifer to an HDF5 file named ``filename`` as a
        string named ``obj_prefix``. 
        """
        import pickle

        if len(obj_prefix)==0:
            raise ValueError("In classify_sklearn_mlpc::save() "+
                             "object prefix cannot be empty.")
        
        loc_dct={"version": version}
        dct_string=pickle.dumps(loc_dct)
        byte_string=pickle.dumps(self.mlpc)

        if self.verbose>2:
            print('In classify_sklearn_mlpc::save().')
            print('  len(dct_string):',len(dct_string))
            print('  len(byte_string):',len(byte_string))
        
        hf=o2sclpy.hdf_file()
        hf.open_or_create(filename)
        hf.sets(obj_prefix+'_dct',dct_string)
        hf.sets(obj_prefix,byte_string)
        hf.close()
        
        return

    def load(self,filename,obj_prefix):
        """
        Load the classifer from an HDF5 file named ``filename`` as a
        string named ``obj_prefix``. 
        """
        import pickle

        hf=o2sclpy.hdf_file()
        hf.open(filename)
        s=o2sclpy.std_string()
        s2=o2sclpy.std_string()
        hf.gets(obj_prefix,s)
        hf.gets(obj_prefix+'_dct',s2)
        hf.close()
        sb=s.to_bytes()
        sb2=s2.to_bytes()

        if self.verbose>2:
            print('In classify_sklearn_mlpc::load().')
            print('  len(sb):',len(sb))
            print('  len(sb2):',len(sb2))
            
        loc_dct=pickle.loads(sb2)
        if loc_dct["version"]!=version:
            raise ValueError("In function classify_sklearn_mlpc::load() "+
                             "Cannot read files with version "+
                             loc_dct["version"])
        self.mlpc=pickle.loads(sb)

        return
    
class classify_sklearn_gnb:
    """
    Classify a data set using scikit-learn's Gaussian
    naive Bayes classifier.
    """

    def __init__(self):
        self.gnb=0
        self.verbose=0
        self.outformat='numpy'
        self.SS1=0
        self.transform_in='none'
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',test_size=0.0,
                 priors=None,var_smoothing=1e-09,verbose=0,
                 transform_in='none'):
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        
        if self.verbose>0:
            print('classify_sklearn_gnb::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))   
            
        # ────────────────────────────────────────────────────────────
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
            
        # ────────────────────────────────────────────────────────────
        # Perform the train/test split
        
        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data,out_data,test_size=test_size)
            except Exception as e:
                print('Exception in classify_sklearn_gnb::set_data()',
                      'at test_train_split().',e)
                raise
        else:
            x_train=in_data
            y_train=out_data
            
        # ────────────────────────────────────────────────────────────
        # Fit the classifier
        
        try:
            from sklearn.naive_bayes import GaussianNB
            model=GaussianNB(priors=priors,var_smoothing=var_smoothing)
        except Exception as e:
            print('Exception in classify_sklearn_gnb::set_data()',
                  'at model().',e)    
            raise
            
        try:
            y_train=y_train.reshape(y_train.shape[0])
            self.gnb=model.fit(x_train,y_train)
        except Exception as e:
            print('Exception in classify_sklearn_gnb::set_data()',
                  'at fit().',e)
            raise
        
        if test_size>0.0:
            print('score:',self.gnb.score(x_test,y_test))

        return
    
    def set_data_str(self,in_data,out_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['verbose'],
                            list_of_floats=['test_size','var_smoothing'])
        
        if self.verbose>2:
            print('In classify_sklearn_gnb::set_data_str(): string:',
                  options,'Dictionary:',dct)
              
        self.set_data(in_data,out_data,**dct)

        return
    
    def eval(self,v):
        """
        Evaluate the classifier at point ``v``.
        """

        if self.transform_in!='none':
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print('Exception 4 in classify_sklearn_gbn:',e)
                raise
        else:
            v_trans=v.reshape(1,-1)
    
        pred=self.gnb.predict(v_trans)
        
        if self.outformat=='list':
            return pred.tolist()

        if self.verbose>1:
            print('classify_sklearn_gbn::eval():',
                'type(pred),pred:',
                type(pred),pred)

        return numpy.ascontiguousarray(pred)

    def eval_list(self,v):
        """
        Evaluate the classifier at the array of points stored in ``v``.
        """

        try:
            pred=self.gnb.predict(v)
        except Exception as e:
            print('Exception in classify_sklearn_gnb::eval_list():',e)
            raise
    
        if self.outformat=='list':
            return pred.tolist()
   
        if self.verbose>1:
            print('classify_sklearn_gnb::eval_list():',
                'type(pred),pred:',
                type(pred),pred)
                    
        return numpy.ascontiguousarray(pred)

    def save(self,filename,obj_prefix="classify_sklearn_gnb"):
        """
        Save the classifer to an HDF5 file named ``filename`` as a
        string named ``obj_prefix``. 
        """
        import pickle

        if len(obj_prefix)==0:
            raise ValueError("In classify_sklearn_gnb::save() "+
                             "object prefix cannot be empty.")
        
        loc_dct={"version": version}
        dct_string=pickle.dumps(loc_dct)
        byte_string=pickle.dumps(self.gnb)
        hf=o2sclpy.hdf_file()
        hf.open_or_create(filename)
        hf.sets(obj_prefix+'_dct',dct_string)
        hf.sets(obj_prefix,byte_string)
        hf.close()
        
        return

    def load(self,filename,obj_prefix="classify_sklearn_gnb"):
        """
        Load the classifer from an HDF5 file named ``filename`` as a
        string named ``obj_prefix``. 
        """
        import pickle

        hf=o2sclpy.hdf_file()
        hf.open(filename)
        s=o2sclpy.std_string()
        s2=o2sclpy.std_string()
        hf.gets(obj_prefix,s)
        hf.gets(obj_prefix+'_dct',s2)
        hf.close()
        sb=s.to_bytes()
        sb2=s2.to_bytes()

        loc_dct=pickle.loads(sb2)
        if loc_dct["version"]!=version:
            raise ValueError("In function classify_sklearn_gnb::load() "+
                             "Cannot read files with version "+
                             loc_dct["version"])
        self.gnb=pickle.loads(sb)

        return
    
    
