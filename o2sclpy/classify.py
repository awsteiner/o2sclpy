#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2024, Satyajit Roy and Andrew W. Steiner
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

class classify_sklearn_dtc:
    """
    Classify a data set using scikit-learn's decision tree classifier.
    """

    def __init__(self):
        self.dtc=0
        self.verbose=0
        self.outformat='numpy'
        
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
        
        if self.verbose>0:
            print('classify_sklearn_dtc::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
           
        # ────────────────────────────────────────────────────────────
        # Perform the train/test split
        
        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data,out_data,test_size=test_size)
            except Exception as e:
                print('Exception in classify_sklearn_dtc::set_data()',
                      'at test_train_split().',e)
        else:
            x_train=in_data
            y_train=out_data
            
        # ────────────────────────────────────────────────────────────
        # Fit the classifier
        
        try:
            from sklearn.tree import DecisionTreeClassifier
            model = DecisionTreeClassifier(criterion=criterion, 
                                           splitter=splitter,
                                           max_depth=max_depth, 
                                           max_features=max_features,
                                           random_state=random_state)
        except Exception as e:
            print('Exception in classify_sklearn_dtc::set_data()',
                  'at model definition.',e)

        try:
            model.fit(x_train,y_train)      
        except Exception as e:
            print('Exception in classify_sklearn_dtc::set_data()',
                  'at model fitting.',e)
            
        self.dtc=model

        return
    
    def eval(self,v):
        """
        Evaluate the classifier at point ``v``.
        """

        try:
            pred=self.dtc.predict([v])
        except Exception as e:
            print('Exception 4 in classify_sklearn_dtc:',e)
    
        if self.outformat=='list':
            return pred.tolist()
   
        if self.verbose>1:
            print('classify_sklearn_dtc::eval():',
                'type(pred),pred:',
                type(pred),pred)
                    
        return numpy.ascontiguousarray(pred)

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
        self.transform_in=0
        
        return
    
    def set_data(self,in_data,out_data,
                 transform_in='none',outformat='numpy',test_size=0.0,
                 hlayers=(100,),activation='relu',
                 solver='adam',alpha=0.0001,batch_size='auto', 
                 learning_rate='constant',max_iter=200,
                 random_state=None,verbose=False, 
                 early_stopping=False,n_iter_no_change=10):
                 
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        
        if self.verbose>0:
            print('classify_sklearn_mlpc::set_data():')
            print('  outformat:',outformat)
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
                print('Exception in classify_sklearn_dtc::set_data()',
                      'at test_train_split().',e)
        else:
            x_train=in_data_trans
            y_train=out_data
            
        # ────────────────────────────────────────────────────────────
        # Fit the classifier
        
        try:
            from sklearn.neural_network import MLPClassifier
            model=MLPClassifier(hidden_layer_sizes=hlayers, 
                 activation=activation,solver=solver, 
                 alpha=alpha,batch_size=batch_size, 
                 learning_rate=learning_rate,max_iter=max_iter,  
                 random_state=random_state,verbose=verbose, 
                 early_stopping=early_stopping, 
                 n_iter_no_change=n_iter_no_change)
        except Exception as e:
            print('Exception in classify_sklearn_mlpc::set_data()',
                  'at model().',e)
        try:
            y_train=y_train.reshape(y_train.shape[0])
            self.mlpc=model.fit(x_train,y_train)
        except Exception as e:
            print('Exception in classify_sklearn_mlpc::set_data()',
                  'at fit().',e)

        if test_size>0.0:
            print('score:',self.mlpc.score(x_test,y_test))

        return
    
    def eval(self,v):
        """
        Evaluate the classifier at point ``v``.
        """

        if self.transform_in!='none':
            try:
                v_trans=self.SS1.transform(v.reshape(1,-1))
            except Exception as e:
                print('Exception 4 in classify_sklearn_mlpc:',e)
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
        self.transform_in=0
        
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
            
        try:
            y_train=y_train.reshape(y_train.shape[0])
            self.gnb=model.fit(x_train,y_train)
        except Exception as e:
            print('Exception in classify_sklearn_gnb::set_data()',
                  'at fit().',e)
        
        if test_size>0.0:
            print('score:',self.gnb.score(x_test,y_test))

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
