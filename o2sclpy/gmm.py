#  -------------------------------------------------------------------
#  
#  Copyright (C) 2024, Andrew W. Steiner
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
#  -------------------------------------------------------------------
#
import numpy

from o2sclpy.utils import string_to_dict2

class gmm_sklearn:
    """
    Use scikit-learn to generate a Gaussian mixture model of a 
    specified set of data.
    
    This is an experimental interface to provide easier interaction
    with C++.
    """

    def __init__(self):
        self.verbose=0
        self.n_components=0
        self.n_dim=0
        self.convariance_type=0
        self.gm=0

    def set_data(self,in_data,verbose=0,n_components=2,
                 covariance_type='full',tol=0.001,reg_covar=1.0e-6,
                 max_iter=100,n_init=1):
        """
        Fit the mixture model with the specified input data, 
        a numpy array of shape (n_samples,n_coordinates)
        """

        if verbose>0:
            print('gmm_sklearn::set_data():')
            print('  verbose:',verbose)
            print('  n_components:',n_components)
            print('  covariance_type:',covariance_type)
            print('  in_data shape:',numpy.shape(in_data))
            print('')

        from sklearn.mixture import GaussianMixture

        self.verbose=verbose
        self.n_components=n_components
        self.covariance_type=covariance_type
        self.n_dim=numpy.shape(in_data)[1]

        if (covariance_type!='full' and covariance_type!='spherical' and
            covariance_type!='tied' and covariance_type!='diag'):
            raise('Incorrect covariance type in gmm_sklearn.')
        
        try:
            self.gm=GaussianMixture(n_components=n_components,
                                    covariance_type=covariance_type,
                                    verbose=verbose,tol=tol,
                                    reg_covar=reg_covar,max_iter=max_iter,
                                    n_init=n_init).fit(in_data)
        except Exception as e:
            print('Exception in gmm_sklearn::set_data()',
                  'Gaussian mixture fit failed.\n  ',e)
            raise

        return

    def get_data(self):
        """
        Return the properties of the Gaussian mixture model as contiguous
        numpy arrays. This function returns, in order, the weights,
        the means, the covariances, the precisions (the inverse of the
        covariances), and the Cholesky decomposition of the
        precisions.
        """
        if self.verbose>1:
            print('gmm_sklearn::get_data():')
            print('  weights:',self.gm.weights_)
            print('  means: ',self.gm.means_)
            print('  covariances:',self.gm.covariances_)
            print('  precisions:',self.gm.precisions_)
            print('  Chol. decomp.:',self.gm.precisions_cholesky_)
            print('')

        if self.covariance_type=='full':
            mtemp=numpy.reshape(self.gm.means_,
                                (self.n_dim*self.n_components))
            ctemp=numpy.reshape(self.gm.covariances_,
                                (self.n_dim*self.n_dim*self.n_components))
            ptemp=numpy.reshape(self.gm.precisions_,
                                (self.n_dim*self.n_dim*self.n_components))
            pctemp=numpy.reshape(self.gm.precisions_cholesky_,
                                 (self.n_dim*self.n_dim*self.n_components))
        elif self.covariance_type=='diag':
            mtemp=numpy.reshape(self.gm.means_,
                                (self.n_dim*self.n_components))
            ctemp=numpy.reshape(self.gm.covariances_,
                                (self.n_dim*self.n_components))
            ptemp=numpy.reshape(self.gm.precisions_,
                                (self.n_dim*self.n_components))
            pctemp=numpy.reshape(self.gm.precisions_cholesky_,
                                 (self.n_dim*self.n_components))
        elif self.covariance_type=='tied':
            mtemp=numpy.reshape(self.gm.means_,
                                (self.n_dim*self.n_components))
            ctemp=numpy.reshape(self.gm.covariances_,
                                (self.n_dim*self.n_dim))
            ptemp=numpy.reshape(self.gm.precisions_,
                                (self.n_dim*self.n_dim))
            pctemp=numpy.reshape(self.gm.precisions_cholesky_,
                                 (self.n_dim*self.n_dim))
        elif self.covariance_type=='spherical':
            mtemp=numpy.reshape(self.gm.means_,
                                (self.n_dim*self.n_components))
            ctemp=numpy.reshape(self.gm.covariances_,
                                (self.n_components))
            ptemp=numpy.reshape(self.gm.precisions_,
                                (self.n_components))
            pctemp=numpy.reshape(self.gm.precisions_cholesky_,
                                 (self.n_components))
            
        return (numpy.ascontiguousarray(self.gm.weights_),
                numpy.ascontiguousarray(mtemp),
                numpy.ascontiguousarray(ctemp),
                numpy.ascontiguousarray(ptemp),
                numpy.ascontiguousarray(pctemp))

    def o2graph_to_gmm(self,o2scl,amp,link,args):
        """
        The function providing the 'to-gmm' command for 
        o2graph.
        """
        
        curr_type=o2scl_get_type(o2scl,amp,link)
        amt=acol_manager(link,amp)

        n_g=int(args[0])
        cols=args[1:]
        print('otg',n_g,cols)
        n_c=len(cols)

        if curr_type!=b'table':
            print("Command 'to-gmm' not supported for type",
                  curr_type,".")
            return
            
        n_l=amt.table_obj.get_nlines()
        x=numpy.zeros((n_l,n_c))
        for i in range(0,n_c):
            for j in range(0,n_l):
                x[j,i]=amt.table_obj.get(cols[i],j)
        gs.set_data(x,'n_components='+str(n_g))

        means=numpy.reshape(self.gm.means_,
                            (self.n_dim*self.n_components))
        covars=numpy.reshape(self.gm.covariances_,
                            (self.n_dim*self.n_dim*self.n_components))
        
        return
    
    def set_data_str(self,in_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['verbose','n_components'],
                            list_of_floats=['tol','reg_covar'])
        if self.verbose>1:
            print('String:',options,'Dictionary:',dct)
              
        self.set_data(in_data,**dct)

        return

    def predict(self,v):
        """
        Predict the labels (the index of the Gaussian) given a
        vector or vectors v and return them in a one-dimensional
        numpy array with data type int64. 
        """

        if numpy.shape(v)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            yp=self.gm.predict([v])
        else:
            # Otherwise, call the predict() function as normal
            yp=self.gm.predict(v)

        if self.verbose>1:
            print('gmm_sklearn::predict(): type(yp),yp:',
                   type(yp),yp,yp.dtype)
        return numpy.ascontiguousarray(yp)
    
    def log_pdf(self,x):
        """
        Return the per-sample average log likelihood of the data as a
        single floating point value given the vector or vectors
        specified in x.
        """
        if numpy.shape(x)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            s=self.gm.score([x])
            return s

        # Otherwise, call the score() function as normal
        s=self.gm.score(x)
        
        return s
    
    def score_samples(self,x):
        """
        Given a vector (or list of vectors) in ``x``, return
        the log likelihood at each point as a numpy array.
        """
        if numpy.shape(x)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            ss=self.gm.score_samples([x])
        else:
            
            # Otherwise, call the predict() function as normal
            ss=self.gm.score_samples(x)

        # Return the scores
        if self.verbose>1:
            print('gmm_sklearn::score_samples(): type(ss),ss:',
                   type(ss),ss)
        return numpy.ascontiguousarray(ss)
    
    def sample(self,n_samples=1):
        """
        Sample the Gaussian mixture model, returning a tuple with two
        components, the first being an 2D array of the coordinates of
        the new samples and the second being a 1D array of the labels
        for each new sample.
        """
        s=self.gm.sample(n_samples=n_samples)
        return s
    
    def components(self,v):
        """
        For a point (or set of points) specified in ``v``, use the
        Gaussian mixture at to compute the density (or densities) of
        each component as a contiguous numpy array. Each array will
        have entries which sum to 1.
        """

        if numpy.shape(v)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            yp=self.gm.predict_proba([v])
        else:
            # Otherwise, call the predict_proba() function as normal
            yp=self.gm.predict_proba(v)

        if yp.ndim==1:
            # If the output is only a one-dimensional vector, then
            # just return it
            if self.verbose>1:
                print('gmm_sklearn::components(): type(yp),yp:',
                      type(yp),yp)
            return numpy.ascontiguousarray(yp)
        
        if numpy.shape(v)==((self.n_dim,)):
            # If the user input was one-dimensional, then make the
            # output one-dimensional as well
            if self.verbose>1:
                print('gmm_sklearn::components(): type(yp[0]),yp[0]:',
                      type(yp[0]),yp[0])
            return numpy.ascontiguousarray(yp[0])

        # Otherwise, just return the full output
        if self.verbose>1:
            print('gmm_sklearn::components(): type(yp),yp:',
                   type(yp),yp)
        return numpy.ascontiguousarray(yp)
        
class bgmm_sklearn:
    """
    Use scikit-learn to generate a Bayesian Gaussian mixture model of a 
    specified set of data.

    This is an experimental interface to provide easier interaction
    with C++.
    """

    def __init__(self):
        self.verbose=0
        self.n_components=0
        self.n_dim=0
        self.convariance_type=0
        self.bgm=0

    def set_data(self,in_data,verbose=0,n_components=2,
                 covariance_type='full',tol=0.001,reg_covar=1.0e-6,
                 max_iter=100,n_init=1):
        """
        Fit the mixture model with the specified input data, 
        a numpy array of shape (n_samples,n_coordinates)
        """

        if verbose>0:
            print('bgmm_sklearn::set_data():')
            print('  verbose:',verbose)
            print('  n_components:',n_components)
            print('  covariance_type:',covariance_type)
            print('  in_data shape:',numpy.shape(in_data))
            print('')

        from sklearn.mixture import BayesianGaussianMixture

        self.verbose=verbose
        self.n_components=n_components
        self.covariance_type=covariance_type
        self.n_dim=numpy.shape(in_data)[1]

        if (covariance_type!='full' and covariance_type!='spherical' and
            covariance_type!='tied' and covariance_type!='diag'):
            raise('Incorrect covariance type in bgmm_sklearn.')
        
        try:
            self.bgm=BayesianGaussianMixture(n_components=n_components,
                                            covariance_type=covariance_type,
                                            verbose=verbose,tol=tol,
                                            reg_covar=reg_covar,
                                            max_iter=max_iter,
                                            n_init=n_init).fit(in_data)
        except Exception as e:
            print('Exception in bgmm_sklearn::set_data()',
                  'Gaussian mixture fit failed.\n  ',e)
            raise

        if self.verbose>0:
            print('bgmm_sklearn::set_data(): Score:',self.bgm.score(in_data))
        
        return

    def get_data(self):
        """
        Return the properties of the Gaussian mixture model as contiguous
        numpy arrays. This function returns, in order, the weights,
        the means, the covariances, the precisions (the inverse of the
        covariances), and the Cholesky decomposition of the
        precisions.
        """
        if self.verbose>1:
            print('bgmm_sklearn::get_data():')
            print('  weights:',self.bgm.weights_)
            print('  means: ',self.bgm.means_)
            print('  covariances:',self.bgm.covariances_)
            print('  precisions:',self.bgm.precisions_)
            print('  Chol. decomp.:',self.bgm.precisions_cholesky_)
            print('')

            if self.covariance_type=='full':
                mtemp=numpy.reshape(self.bgm.means_,
                                    (self.n_dim*self.n_components))
                ctemp=numpy.reshape(self.bgm.covariances_,
                                    (self.n_dim*self.n_dim*self.n_components))
                ptemp=numpy.reshape(self.bgm.precisions_,
                                    (self.n_dim*self.n_dim*self.n_components))
                pctemp=numpy.reshape(self.bgm.precisions_cholesky_,
                                     (self.n_dim*self.n_dim*self.n_components))
            elif self.covariance_type=='diag':
                mtemp=numpy.reshape(self.bgm.means_,
                                    (self.n_dim*self.n_components))
                ctemp=numpy.reshape(self.bgm.covariances_,
                                    (self.n_dim*self.n_components))
                ptemp=numpy.reshape(self.bgm.precisions_,
                                    (self.n_dim*self.n_components))
                pctemp=numpy.reshape(self.bgm.precisions_cholesky_,
                                     (self.n_dim*self.n_components))
            elif self.covariance_type=='tied':
                mtemp=numpy.reshape(self.bgm.means_,
                                    (self.n_dim*self.n_components))
                ctemp=numpy.reshape(self.bgm.covariances_,
                                    (self.n_dim*self.n_dim))
                ptemp=numpy.reshape(self.bgm.precisions_,
                                    (self.n_dim*self.n_dim))
                pctemp=numpy.reshape(self.bgm.precisions_cholesky_,
                                     (self.n_dim*self.n_dim))
            elif self.covariance_type=='spherical':
                mtemp=numpy.reshape(self.bgm.means_,
                                    (self.n_dim*self.n_components))
                ctemp=numpy.reshape(self.bgm.covariances_,
                                    (self.n_components))
                ptemp=numpy.reshape(self.bgm.precisions_,
                                    (self.n_components))
                pctemp=numpy.reshape(self.bgm.precisions_cholesky_,
                                     (self.n_components))
        return (numpy.ascontiguousarray(self.bgm.weights_),
                numpy.ascontiguousarray(mtemp),
                numpy.ascontiguousarray(ctemp),
                numpy.ascontiguousarray(ptemp),
                numpy.ascontiguousarray(pctemp))

    def o2graph_to_bgmm(self,o2scl,amp,link,args):
        """
        The function providing the 'to-bgmm' command for 
        o2graph.
        """
        
        curr_type=o2scl_get_type(o2scl,amp,link)
        amt=acol_manager(link,amp)

        n_g=int(args[0])
        cols=args[1:]
        print('otg',n_g,cols)
        n_c=len(cols)

        if curr_type!=b'table':
            print("Command 'to-bgmm' not supported for type",
                  curr_type,".")
            return
            
        n_l=amt.table_obj.get_nlines()
        x=numpy.zeros((n_l,n_c))
        for i in range(0,n_c):
            for j in range(0,n_l):
                x[j,i]=amt.table_obj.get(cols[i],j)
        gs.set_data(x,'n_components='+str(n_g))

        means=numpy.reshape(self.bgm.means_,
                            (self.n_dim*self.n_components))
        covars=numpy.reshape(self.bgm.covariances_,
                            (self.n_dim*self.n_dim*self.n_components))
        
        return
    
    def set_data_str(self,in_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=string_to_dict2(options,list_of_ints=['verbose','n_components'],
                            list_of_floats=['tol','reg_covar'])
        if self.verbose>1:
            print('String:',options,'Dictionary:',dct)
              
        self.set_data(in_data,**dct)

        return

    def predict(self,v):
        """
        Predict the labels (the index of the Gaussian) given a
        vector or vectors v and return them in a one-dimensional
        numpy array with data type int64. 
        """

        if numpy.shape(v)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            yp=self.bgm.predict([v])
        else:
            # Otherwise, call the predict() function as normal
            yp=self.bgm.predict(v)

        if self.verbose>1:
            print('gmm_sklearn::predict(): type(yp),yp:',
                   type(yp),yp,yp.dtype)
        return numpy.ascontiguousarray(yp)
    
    def log_pdf(self,x):
        """
        Return the per-sample average log likelihood of the data as a
        single floating point value given the vector or vectors
        specified in x.
        """
        if numpy.shape(x)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            s=self.bgm.score([x])
            return s
        
        # Otherwise, call the score() function as normal
        s=self.bgm.score(x)
        
        return s
    
    def score_samples(self,x):
        """
        Given a vector (or list of vectors) in ``x``, return
        the log likelihood at each point as a numpy array.
        """
        if numpy.shape(x)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            ss=self.bgm.score_samples([x])
        else:
            
            # Otherwise, call the predict() function as normal
            ss=self.bgm.score_samples(x)

        # Return the scores
        if self.verbose>1:
            print('gmm_sklearn::score_samples(): type(ss),ss:',
                   type(ss),ss)
        return numpy.ascontiguousarray(ss)
    
    def sample(self,n_samples=1):
        """
        Sample the Gaussian mixture model, returning a tuple with two
        components, the first being an 2D array of the coordinates of
        the new samples and the second being a 1D array of the labels
        for each new sample.
        """
        s=self.bgm.sample(n_samples=n_samples)
        return s
    
    def components(self,v):
        """
        For a point (or set of points) specified in ``v``, use the
        Gaussian mixture at to compute the density (or densities) of
        each component as a contiguous numpy array. Each array will
        have entries which sum to 1.
        """

        if numpy.shape(v)==((self.n_dim,)):
            # If the user just gave a one-dimensional vector, then
            # convert to a two-dimensional vector
            yp=self.bgm.predict_proba([v])
        else:
            # Otherwise, call the predict_proba() function as normal
            yp=self.bgm.predict_proba(v)

        if yp.ndim==1:
            # If the output is only a one-dimensional vector, then
            # just return it
            if self.verbose>1:
                print('gmm_sklearn::components(): type(yp),yp:',
                      type(yp),yp)
            return numpy.ascontiguousarray(yp)
        
        if numpy.shape(v)==((self.n_dim,)):
            # If the user input was one-dimensional, then make the
            # output one-dimensional as well
            if self.verbose>1:
                print('gmm_sklearn::components(): type(yp[0]),yp[0]:',
                      type(yp[0]),yp[0])
            return numpy.ascontiguousarray(yp[0])

        # Otherwise, just return the full output
        if self.verbose>1:
            print('gmm_sklearn::components(): type(yp),yp:',
                   type(yp),yp)
        return numpy.ascontiguousarray(yp)
