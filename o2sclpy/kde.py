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

class kde_sklearn:
    """
    Use scikit-learn to generate a KDE

    This is an experimental and very simplifed interface, mostly
    to provide easier interaction with C++. 
    
    Todo: add a test_train_split option?
    """

    def __init__(self):
        self.verbose=0
        self.n_dim=0
        self.kde=0
        self.outformat='numpy'
        self.transform=0
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
                    
            dct[arr2[0]]=arr2[1]

        return dct
    
    def set_data(self,in_data,bw_array,verbose=0,kernel='gaussian',
                 metric='euclidean',outformat='numpy',bandwidth=1.0,
                 transform='unit'):
        """
        Fit the mixture model with the specified input data, 
        a numpy array of shape (n_samples,n_coordinates)
        """

        if verbose>0:
            print('kde_sklearn::set_data():')
            print('  verbose:',verbose)
            print('  transform:',transform)
            print('  metric:',metric)
            print('  kernel:',kernel)
            print('')

        from sklearn.neighbors import KernelDensity
        from sklearn.model_selection import GridSearchCV
        import numpy

        self.verbose=verbose
        self.outformat=outformat
        self.transform=transform
        self.n_dim=numpy.shape(in_data)[1]

        from sklearn.preprocessing import QuantileTransformer
        from sklearn.preprocessing import MinMaxScaler

        if self.transform=='unit':
            self.SS1=MinMaxScaler(feature_range=(0,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
                
        try:
            
            grid=GridSearchCV(KernelDensity(),{"bandwidth": bw_array})
            grid.fit(in_data_trans)
            self.kde=grid.best_estimator_
            
            if self.verbose>0:
                print('Optimal bandwidth: ',grid.best_estimator_.bandwidth)
            
        except Exception as e:
            print('Exception in kde_sklearn::set_data()',
                  'KDE failed.\n  ',e)
            raise

        if self.verbose>0:
            print('kde_sklearn::set_data(): Score:',
                  self.kde.score(in_data_trans))
        
        return

    def get_bandwidth(self):
        """
        Return the bandwidth
        """
        return self.kde.bandwidth_
    
    def set_data_str(self,in_data,bw_array,options):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        dct=self.string_to_dict(options)
        if self.verbose>1:
            print('String:',options,'Dictionary:',dct)
              
        self.set_data(in_data,bw_array,**dct)

        return

    def sample(self,n_samples=1):
        """
        Sample the Gaussian mixture model
        """
        out=self.kde.sample(n_samples=n_samples)
        #print('out:',type(out),numpy.shape(out),out)
        
        if self.transform!='none':
            out_trans=self.SS1.inverse_transform(out)[0]
        else:
            out_trans=out[0]
            
        #print('out_trans:',type(out_trans),numpy.shape(out_trans),out_trans)

        if self.outformat=='list':
            return out_trans.tolist()

        return numpy.ascontiguousarray(out_trans)
        
    def log_density(self,x):
        """
        Return the log likelihood 
        """
        if self.transform!='none':
            x_trans=self.SS1.transform([x])
        else:
            x_trans=[x]
        #print('x,x_trans:',x,x_trans)
        res=self.kde.score(x_trans)
        return res
        
