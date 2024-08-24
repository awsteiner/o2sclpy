#  ───────────────────────────────────────────────────────────────────
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
#  ───────────────────────────────────────────────────────────────────

import numpy

from o2sclpy.utils import string_to_dict2

class nflows_nsf:
    """
    Neural spline flow probability density distribution
    from normflows which uses pytorch
    """

    def __init__(self):
        self.verbose=0
        self.n_dim=0
        self.n_pts=0
        self.model=0
        self.outformat='numpy'
        self.SS1=0
        self.data=0
        self.num_hidden_channels=0
        self.num_layers=0
        self.max_iter=0

    def set_data(self,in_data,verbose=0,
                 num_layers=20,num_hidden_channels=128,
                 max_iter=20000,outformat='numpy'):
        """
        Fit the mixture model with the specified input data, 
        a numpy array of shape (n_samples,n_coordinates)
        """

        import torch
        import normflows
        
        if verbose>0:
            print('nflows_nsf::set_data():')
            print('  verbose:',verbose)
            print('')

        from sklearn.preprocessing import StandardScaler
        
        # Move model on GPU if available
        enable_cuda=True
        self.device=torch.device('cuda' if torch.cuda.is_available() and
                            enable_cuda else 'cpu')
        print('device:',self.device)

        self.verbose=verbose
        self.outformat=outformat
        self.n_dim=numpy.shape(in_data)[1]
        self.n_pts=numpy.shape(in_data)[0]
        self.data=in_data
        self.num_layers=num_layers
        self.max_iter=max_iter
        self.num_hidden_channels=num_hidden_channels
        
        try:
            self.SS1=StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        except Exception as e:
            print('Exception 1',e)
            raise
        
        try:

            # Convert numpy to torch, there's probably a better way...
            ten_in=torch.zeros((self.n_pts,self.n_dim),device=self.device)
            for i in range(0,self.n_pts):
                for j in range(0,self.n_dim):
                    ten_in[i,j]=in_data_trans[i,j]
                    
            self.base=normflows.distributions.base.DiagGaussian(self.n_dim)

            # Create normalizing flow
            layer_func=nf.flows.AutoregressiveRationalQuadraticSpline
            
            flow_layers=[]
            for i in range(num_layers):
                flow_layers+=[layer_func(self.n_dim,1,
                                         self.num_hidden_channels,
                                         permute_mask=True)]
                
            self.model=nf.NormalizingFlow(base,flow_layers)

            self.model=self.model.to(device)

            self.model.eval()
            self.model.train()

            optimizer=torch.optim.Adam(self.model.parameters(),
                                       lr=1e-4,weight_decay=1e-4)

            for it in range(0,self.max_iter):
                optimizer.zero_grad()
                loss=model.forward_kld(ten_in)

                if ~(torch.isnan(loss) | torch.isinf(loss)):
                    loss.backward()
                    optimizer.step()

                print('loss',loss.to('cpu').data.numpy())
                
            
            if self.verbose>0:
                print('Bandwidth: ',self.kde.bandwidth_)
            
        except Exception as e:
            print('Exception in nflows_nsf::set_data()',
                  'Train failed.\n  ',e)
            raise

        return

    def set_data_str(self,in_data,options=''):
        """
        Set the input and output data to train the interpolator,
        using a string to specify the keyword arguments.
        """

        try:
            dct=string_to_dict2(options,list_of_ints=['verbose',
                                                      'num_layers',
                                                      'num_hidden_channels',
                                                      'max_iter'])
            if self.verbose>1:
                print('String:',options,'Dictionary:',dct)
                  
            self.set_data(in_data,**dct)
        except Exception as e:
            print('Exception in nflows_nsf::set_data_str()',
                  'Failed.\n  ',e)
            raise

        return

        return

    def sample(self,n_samples=1):
        """
        Sample the distribution
        """

        out=self.model.sample(n_samples).to('cpu')
        print('out:',type(out),numpy.shape(out),out)
        
        if self.transform!='none':
            if n_samples==1:
                out_trans=self.SS1.inverse_transform(out)[0]
            else:
                out_trans=self.SS1.inverse_transform(out)
        else:
            if n_samples==1:
                out_trans=out[0]
            else:
                out_trans=out
            
        print('out_trans:',type(out_trans),numpy.shape(out_trans),out_trans,
              self.outformat)

        if self.outformat=='list':
            return out_trans.tolist()

        return numpy.ascontiguousarray(out_trans)
        
    def log_pdf(self,x):
        """
        Return the log likelihood 
        """
        if self.transform!='none':
            x_trans=self.SS1.transform([x])
        else:
            x_trans=[x]
        print('x,x_trans:',x,x_trans)
        x2=torch.zeros((1,self.n_dim),device=self.device)
        for i in range(0,self.n_dim):
            x2[0,i]=x_trans[0,i]
            
        res=self.model.log_prob(x2)
        if self.device!='cpu':
            res=res.to('cpu')
        print(type(res),res)

        return res

    def pdf(self,x):
        """
        Return the likelihood 
        """
        return numpy.exp(self.log_pdf(x))
        
