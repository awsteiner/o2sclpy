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
from o2sclpy.utils import string_to_dict2

class classify_sklearn_dtc:
    """
    Interpolate one dimensional data sets using 
    a Decision tree classifier from sklearn
    """

    def __init__(self):
        self.dtc=0
        self.verbose=0
        self.outformat='numpy'
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,test_size=0.0,
                 criterion='gini', splitter='best', max_depth=None, 
                 min_samples_split=2, min_samples_leaf=1, 
                 min_weight_fraction_leaf=0.0, max_features=None, 
                 random_state=None, max_leaf_nodes=None, 
                 min_impurity_decrease=0.0, class_weight=None, 
                 ccp_alpha=0.0, monotonic_cst=None):
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        
        if self.verbose>0:
            print('classify_sklearn_dtc::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))

        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                x_train,x_test,y_train,y_test=train_test_split(
                    in_data,out_data,test_size=test_size,random_state=42)
            except Exception as e:
                print('Exception in classify_sklearn_dtc::set_data()',
                      'at test_train_split().',e)
        else:
            x_train=in_data
            y_train=out_data
            
        try:
            from sklearn.tree import DecisionTreeClassifier
            model = DecisionTreeClassifier(criterion=criterion, 
                 splitter=splitter, max_depth=max_depth, 
                 min_samples_split=min_samples_split, 
                 min_samples_leaf=min_samples_leaf, 
                 min_weight_fraction_leaf=min_weight_fraction_leaf, 
                 max_features=max_features,class_weight=class_weight,  
                 random_state=random_state, 
                 max_leaf_nodes=max_leaf_nodes, 
                 min_impurity_decrease=min_impurity_decrease, 
                 ccp_alpha=ccp_alpha, monotonic_cst=monotonic_cst)
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
        Evaluate the NN at point ``v``.
        """

        try:
            pred=self.dtr.predict([v])#, verbose=0
        except Exception as e:
            print('Exception 4 in classify_sklearn_dtc:',e)
    
        if self.outformat=='list':
            return pred.tolist()
   
        if self.verbose>1:
            print('classify_sklearn_dtc::eval():',
                'type(pred),pred:',
                type(pred),pred)
        # The output from tf.keras is float32, so we have to convert to
        # float64 
        n_out=numpy.shape(pred)[0]
        out_double=numpy.zeros((n_out))
        for i in range(0,n_out):
            out_double[i]=pred[i]
                    
            return numpy.ascontiguousarray(out_double)

class classify_sklearn_mlpc:
    """
    Interpolate one dimensional data sets using a 
    Multi-layer Perceptron classifier scikit-learn
    """

    def __init__(self):
        self.mlpc=0
        self.verbose=0
        self.outformat='numpy'
        self.SS1=0
        self.SS2=0
        
        return
    
    def set_data(self,in_data,out_data,outformat='numpy',test_size=0.0,
                 hidden_layer_sizes=(100,), activation='relu',
                 solver='adam', alpha=0.0001, batch_size='auto', 
                 learning_rate='adaptive', learning_rate_init=0.001, 
                 power_t=0.5, max_iter=500, shuffle=True, 
                 random_state=1, tol=0.0001, verbose=0, 
                 warm_start=False, momentum=0.9, nesterovs_momentum=True, 
                 early_stopping=True, validation_fraction=0.1, 
                 beta_1=0.9, beta_2=0.999, epsilon=1e-08, 
                 n_iter_no_change=10, max_fun=15000):
        """
        Set the input and output data to train the interpolator
        """
        self.outformat=outformat
        self.verbose=verbose
        
        if self.verbose>0:
            print('interpm_sklearn_mlpr::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  solver:',solver)

        from sklearn.preprocessing import StandardScaler
        
        self.SS1=StandardScaler()
        self.SS2=StandardScaler()
        in_data_trans=self.SS1.fit_transform(in_data)
        out_data_trans=self.SS2.fit_transform(out_data)

        if test_size>0.0:
            try:
                from sklearn.model_selection import train_test_split
                in_train,in_test,out_train,out_test=train_test_split(
                    in_data_trans,out_data_trans,test_size=test_size,random_state=42)
            except Exception as e:
                print('Exception in interpm_sklearn_mlpr::set_data()',
                      'at test_train_split().',e)
        else:
            in_train=in_data_trans
            out_train=out_data_trans
            
        try:
            from sklearn.neural_network import MLPRegressor
            self.mlpr=MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, 
                 activation=activation,solver=solver, 
                 alpha=alpha, batch_size=batch_size, 
                 learning_rate=learning_rate, shuffle=shuffle,
                 learning_rate_init=learning_rate_init, 
                 power_t=power_t, max_iter=max_iter,  
                 random_state=random_state, tol=tol, verbose=verbose, 
                 warm_start=warm_start, momentum=momentum, 
                 nesterovs_momentum=nesterovs_momentum, 
                 early_stopping=early_stopping, 
                 validation_fraction=validation_fraction, 
                 beta_1=beta_1, beta_2=beta_2, epsilon=epsilon, 
                 n_iter_no_change=n_iter_no_change, 
                 max_fun=max_fun).fit(in_train,out_train)
        except Exception as e:
            print('Exception in interpm_sklearn_mlpr::set_data()',
                  'at fit().',e)

        if test_size>0.0:
            print('score:',self.mlpr.score(in_test,out_test))

        return
    
    def eval(self,v):
        """
        Evaluate the NN at point ``v``.
        """

        try:
            v_trans=self.SS1.transform(v.reshape(1,-1))
            pred=self.mlpr.predict(v_trans)#, verbose=0
            pred_trans=self.SS2.inverse_transform(pred.reshape(1,-1))
        except Exception as e:
            print('Exception 4 in interpm_sklearn_mlpr:',e)
    
        if self.outformat=='list':
            return pred.tolist()

        if pred_trans.ndim==1:
            
            if self.verbose>1:
                print('interpm_sklearn_mlpr::eval():',
                      'type(pred),pred:',
                      type(pred_trans),pred_trans)
            # The output from tf.keras is float32, so we have to convert to
            # float64 
            n_out=numpy.shape(pred_trans)[0]
            out_double=numpy.zeros((n_out))
            for i in range(0,n_out):
                out_double[i]=pred_trans[i]
                    
            return numpy.ascontiguousarray(out_double)
        
        if self.verbose>1:
            print('interpm_sklearn_mlpr::eval():',
                  'type(pred_trans[0]),pred_trans[0]:',
                  type(pred_trans[0]),pred_trans[0])

        # The output from tf.keras is float32, so we have to convert to
        # float64 
        n_out=numpy.shape(pred_trans[0])[0]
        out_double=numpy.zeros((n_out))
        for i in range(0,n_out):
            out_double[i]=pred_trans[0][i]
            
        return numpy.ascontiguousarray(out_double)
    