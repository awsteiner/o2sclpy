#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2025, Andrew W. Steiner
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
from o2sclpy.doc_data import version
from o2sclpy.base import *

class dimred_sklearn_pca:
    """
    """

    verbose=0
    """
    Verbosity parameter (default 0)
    """

    def __init__(self):

        self.verbose=0
        self.random_state=None
        self.n_components=0
        self.whiten=False
        self.tol=0.0
        self.svn_solver='auto'
        self.pca=0
        self.SS1=0
        self.transform=0
        
        return
    
    def run(self,in_data,n_components=None,verbose=0,
            svd_solver='auto',tol=0.0,random_state=None,
            transform='standard',whiten=False):
            
        """Set the input and output data to train the classifier

        The variable ``in_data`` should be an array of shape
        ``(n_points,n_dim)``
        """
        self.verbose=verbose
        self.n_components=n_components
        self.random_state=random_state
        self.whiten=whiten
        self.svd_solver=svd_solver
        self.tol=tol
        self.transform=transform
        
        if self.verbose>0:
            print('dimred_sklearn_pca::set_data():')
            print('  in_data shape:',numpy.shape(in_data))
            print('  verbose:',verbose)
            print('  n_components:',n_components)
            print('  random_state:',random_state)
            print('  tol:',tol)
            print('  whiten:',whiten)
            print('  svd_solver:',svd_solver)
            print('  transform:',transform)

        # ----------------------------------------------------------
        # Handle the data transformation
        
        from sklearn.preprocessing import QuantileTransformer
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.preprocessing import StandardScaler
        
        if self.transform=='moto':
            self.SS1=MinMaxScaler(feature_range=(-1,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform=='quant':
            self.SS1=QuantileTransformer(n_quantiles=in_data.shape[0])
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform=='standard':
            self.SS1=StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
            
        try:
            from sklearn.decomposition import PCA
            self.pca=PCA(n_components=self.n_components,
                         random_state=self.random_state,
                         whiten=self.whiten,tol=self.tol,
                         svd_solver=self.svd_solver)
            out_data=self.pca.fit_transform(in_data_trans)
            
        except Exception as e:
            print('Exception in dimred_PCA::run()',
                  'at fit_transform().',e)
            raise

        return out_data

    def run_table(self,tab,in_cols,n_components=None,verbose=0,
                  replace=False,out_prefix='pca_',out_cols=[],
                  random_state=None,svd_solver='auto',whiten=False,
                  tol=0.0):

        # First check that all columns specified in 'in_cols' are
        # actually in the table.

        for i in range(0,len(in_cols)):
            if tab.is_column(in_cols[i])==False:
                raise ValueError('Column '+in_cols[i]+
                                 ' is not in the table.')

        # Construct the list of output columns from out_prefix and out_cols
            
        out_cols_loc=[]
        if n_components is not None:
            for i in range(0,n_components):
                if i<len(out_cols):
                    out_cols_loc.append(out_cols[i])
                else:
                    out_cols_loc.append(out_prefix+str(i))

        if verbose>0:
            print("dimred_sklearn_pca::run_table():")
            print("  Input columns:",in_cols)
            print("  Output columns:",out_cols_loc)
            print("  Components:",n_components)

        # Construct the input data matrix (brute force)
        in_data=numpy.zeros((tab.get_nlines(),len(in_cols)))
        for i in range(0,tab.get_nlines()):
            for j in range(0,len(in_cols)):
                in_data[i][j]=tab.get(in_cols[j],i)

        # Perform the dimensional reduction
        out_data=self.run(in_data,n_components,verbose=verbose,
                          random_state=random_state,
                          tol=tol,whiten=whiten,
                          svd_solver=svd_solver)

        # Remove the old columns if requested
        if replace==True:
            for i in range(i,len(in_cols)):
                tab.delete_column(in_cols[i])
        
        # Add the output data to the table
        if n_components is None:
            n_components=numpy.shape(out_data)[1]
            print('Setting n_components to ',n_components)

        for j in range(0,n_components):
            if tab.is_column(out_cols_loc[j])==False:
                tab.new_column(out_cols_loc[j])
            for i in range(0,tab.get_nlines()):
                tab.set(out_cols_loc[j],i,out_data[i][j])
                
        return
    
    def run_table_str(self,tab,n_components,input_cols,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['random_state',
                                                  'n_components',
                                                  'verbose'],
                            list_of_floats=['tol'],
                            list_of_bools=['replace','whiten'])
        
        if self.verbose>2:
            print('In dimred_sklearn_pca::set_data_str(): string:',
                  options,'Dictionary:',dct)

        out_col_arr=dct.pop("out_cols",'').split(' ')
        if len(out_col_arr)>0 and out_col_arr[-1]=='':
            out_col_arr=out_col_arr[:-2]
            
        try:
            if len(out_col_arr)>0:
                self.run_table(tab,input_cols,n_components=n_components,
                               out_cols=out_col_arr,**dct)
            else:
                self.run_table(tab,input_cols,n_components=n_components,
                               **dct)
        except Exception as e:
            print('Exception in dimred_sklearn_pca::set_data_str()',e)
            raise

        if self.transform=='standard':
            print("mean:",self.SS1.inverse_transform([self.pca.mean_]))
        else:
            print("mean:",self.pca.mean_)
            
        print("explained variance ratio:",self.pca.explained_variance_ratio_)
        print("components:",self.pca.components_)
        
        return

    
class dimred_sklearn_tsne:
    """
    """

    verbose=0
    """
    Verbosity parameter (default 0)
    """

    def __init__(self):

        self.verbose=0
        self.random_state=None
        self.n_components=0
        self.min_grad_norm=1.0e-7
        self.transform=0
        self.SS1=0
        self.tsne=0
        
        return
    
    def run(self,in_data,n_components=2,verbose=0,
            min_grad_norm=1.0e-7,random_state=None,
            transform='standard'):
        """Set the input and output data to train the classifier

        The variable ``in_data`` should be an array of shape
        ``(n_points,n_dim)``
        """
        self.verbose=verbose
        self.transform=transform
        self.n_components=n_components
        self.random_state=random_state
        self.min_grad_norm=min_grad_norm
       
        if self.verbose>0:
            print('dimred_sklearn_tsne::set_data():')
            print('  in_data shape:',numpy.shape(in_data))
            print('  verbose:',verbose)
            print('  transform:',transform)
            print('  n_components:',n_components)
            print('  random_state:',random_state)
            print('  min_grad_norm:',min_grad_norm)

        # ----------------------------------------------------------
        # Handle the data transformation
        
        from sklearn.preprocessing import QuantileTransformer
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.preprocessing import StandardScaler
        
        if self.transform=='moto':
            self.SS1=MinMaxScaler(feature_range=(-1,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform=='quant':
            self.SS1=QuantileTransformer(n_quantiles=in_data.shape[0])
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform=='standard':
            self.SS1=StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
            
        try:
            from sklearn.manifold import TSNE
            self.tsne=TSNE(n_components=self.n_components,
                           random_state=self.random_state,
                           min_grad_norm=self.min_grad_norm,
                           n_jobs=1)
            out_data=self.tsne.fit_transform(in_data_trans)
            
        except Exception as e:
            print('Exception in dimred_TSNE::run()',
                  'at fit_transform().',e)
            raise

        return out_data

    def run_table(self,tab,in_cols,n_components=2,verbose=0,
                  replace=False,out_prefix='tsne_',out_cols=[],
                  random_state=None,min_grad_norm=0.0):

        # First check that all columns specified in 'in_cols' are
        # actually in the table.

        for i in range(0,len(in_cols)):
            if tab.is_column(in_cols[i])==False:
                raise ValueError('Column '+in_cols[i]+
                                 ' is not in the table.')

        # Construct the list of output columns from out_prefix and out_cols
            
        out_cols_loc=[]
        if n_components is not None:
            for i in range(0,n_components):
                if i<len(out_cols):
                    out_cols_loc.append(out_cols[i])
                else:
                    out_cols_loc.append(out_prefix+str(i))

        if verbose>0:
            print("dimred_sklearn_tsne::run_table():")
            print("  Input columns:",in_cols)
            print("  Output columns:",out_cols_loc)
            print("  Components:",n_components)
                    
        # Construct the input data matrix (brute force)
        in_data=numpy.zeros((tab.get_nlines(),len(in_cols)))
        for i in range(0,tab.get_nlines()):
            for j in range(0,len(in_cols)):
                in_data[i][j]=tab.get(in_cols[j],i)

        # Perform the TSNE
        out_data=self.run(in_data,n_components=n_components,
                          verbose=verbose,random_state=random_state,
                          min_grad_norm=min_grad_norm)

        # Remove the old columns if requested
        if replace==True:
            for i in range(i,len(in_cols)):
                tab.delete_column(in_cols[i])
        
        # Add the output data to the table
        if n_components is None:
            n_components=numpy.shape(out_data)[1]
            print('Setting n_components to ',n_components)
        
        for j in range(0,n_components):
            if tab.is_column(out_cols_loc[j])==False:
                tab.new_column(out_cols_loc[j])
            for i in range(0,tab.get_nlines()):
                tab.set(out_cols_loc[j],i,out_data[i][j])
                
        return
    
    def run_table_str(self,tab,input_cols,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['random_state',
                                                  'n_components',
                                                  'verbose'],
                            list_of_floats=['min_grad_norm'],
                            list_of_bools=['replace'])

        if self.verbose>2:
            print('In dimred_sklearn_tsne::set_data_str(): string:',
                  options,'Dictionary:',dct)

        out_col_arr=dct.pop("out_cols",'').split(' ')
        if len(out_col_arr)>0 and out_col_arr[-1]=='':
            out_col_arr=out_col_arr[:-2]
            
        try:
            if len(out_col_arr)>0:
                self.run_table(tab,input_cols,out_cols=out_col_arr,**dct)
            else:
                self.run_table(tab,input_cols,**dct)
                
        except Exception as e:
            print('Exception in dimred_sklearn_tsne::set_data_str()',e)
            raise

        return

    
