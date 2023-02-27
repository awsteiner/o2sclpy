#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023, Andrew W. Steiner
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

class gmm_sklearn:
    """
    Use scikit-learn to generate a Gaussian mixture model of a 
    specified set of data.

    This is an experimental and very simplifed interface.
    """

    def __init__(self):
        self.verbose=0
        self.n_components=0
        self.n_dim=0

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
            if arr2[0]=='n_components':
                arr2[1]=int(arr2[1])
                    
            dct[arr2[0]]=arr2[1]

        return dct
    
    def set_data(self,in_data,verbose=0,n_components=2):
        """
        Fit the mixture model with the specified input data, 
        a numpy array of shape (n_samples,n_coordinates)
        """

        if verbose>0:
            print('gmm_sklearn::set_data():')
            print('  verbose:',verbose)
            print('  n_components:',n_components)
            print('  in_data shape:',numpy.shape(in_data))
            print('')

        from sklearn.mixture import GaussianMixture

        self.verbose=verbose
        self.n_components=n_components
        self.n_dim=numpy.shape(in_data)[1]

        try:
            self.gm=GaussianMixture(n_components=n_components).fit(in_data)
        except Exception as e:
            print('Exception in gmm_sklearn:',e)
            pass

        return

    def get_data(self):
        """
        Return the properties of the Gaussian mixture model as contiguous
        numpy arrays. This function returns, in order, the weights,
        the means, the covariances, the precisions (the inverse of the
        covariances), and the Cholesky decomposition of the
        precisions.
        """
        if self.verbose>0:
            print('gmm_sklearn::get_data():')
            print('  weights:',self.gm.weights_)
            print('  means: ',self.gm.means_)
            print('  covariances:',self.gm.covariances_)
            print('  precisions:',self.gm.precisions_)
            print('  Chol. decomp.:',self.gm.precisions_cholesky_)
            print('')
        mtemp=numpy.reshape(self.gm.means_,
                            (self.n_dim*self.n_components))
        ctemp=numpy.reshape(self.gm.covariances_,
                            (self.n_dim*self.n_dim*self.n_components))
        ptemp=numpy.reshape(self.gm.precisions_,
                            (self.n_dim*self.n_dim*self.n_components))
        pctemp=numpy.reshape(self.gm.precisions_cholesky_,
                            (self.n_dim*self.n_dim*self.n_components))
        return (numpy.ascontiguousarray(self.gm.weights_),
                numpy.ascontiguousarray(mtemp),
                numpy.ascontiguousarray(ctemp),
                numpy.ascontiguousarray(ptemp),
                numpy.ascontiguousarray(pctemp))
    
    def set_data_str(self,in_data,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=self.string_to_dict(options)
        if self.verbose>1:
            print('String:',options,'Dictionary:',dct)
              
        self.set_data(in_data,**dct)

        return

    def sample(self,n_samples=1):
        """
        Sample the Gaussian mixture model
        """
        return self.gm.sample(n_samples=n_samples)
    
    def eval(self,v):
        """
        Evaluate the mixture model at point ``v``, and return
        the normalized weights for each component as a contiguous numpy 
        array
        """
        yp=self.gm.predict_proba([v])
        if yp.ndim==1:
            if self.verbose>1:
                print('gmm_sklearn::eval(): type(yp),yp:',
                      type(yp),yp)
            return numpy.ascontiguousarray(yp)
        if self.verbose>1:
            print('gmm_sklearn::eval(): type(yp[0]),yp[0]:',
                  type(yp[0]),yp[0])
        return numpy.ascontiguousarray(yp[0])

if __name__ == '__main__':

    N=100
    x=numpy.zeros((N,2))
    for i in range(0,100):
        if i%2==0:
            x[i,0]=0.5+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.5+0.2*numpy.cos(i*1.0e6)
        else:
            x[i,0]=0.1+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.1+0.2*numpy.cos(i*1.0e6)
    
    gs=gmm_sklearn()
    gs.set_data_str(x,'verbose=2,n_components=3')
    print(gs.eval([0.7,0.7]))
    print(gs.eval([0.0,0.0]))
    print('w',gs.gm.weights_)
    print('m',gs.gm.means_)
    print('c',gs.gm.covariances_)
    print('p',gs.gm.precisions_)
    print(gs.get_data())
            
    print('All tests passed.')
