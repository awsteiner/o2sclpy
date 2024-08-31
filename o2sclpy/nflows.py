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
    """Neural spline flow probability density distribution
    from normflows which uses pytorch

    This class is experimental.
    
    This code was originally based on
    https://github.com/VincentStimper/normalizing-flows/blob/master/examples/circular_nsf.ipynb
    .
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
        self.base=0
        self.device=0
        self.adam_lr=0
        self.adam_decay=0

    def set_data(self,in_data,verbose=0,
                 num_layers=20,num_hidden_channels=128,
                 max_iter=20000,outformat='numpy',adam_lr=1.0e-4,
                 adam_decay=1.0e-4):
        """
        Fit the mixture model with the specified input data, 
        a numpy array of shape (n_samples,n_coordinates)

        adam_lr is Adam learning rate (pytorch default is 1.0e-3)
        adam_decay is the Adam weight decay (pytorch default is 0)
        """

        import torch
        import normflows
        
        if verbose>0:
            print('nflows_nsf::set_data():')
            print('  verbose:',verbose)
            print('  outformat:',outformat)
            print('  max_iter:',max_iter)
            print('  num_layers:',num_layers)
            print('  num_hidden_channels:',num_hidden_channels)
            print('  adam_lr:',adam_lr)
            print('  adam_decay:',adam_decay)
            print('')

        from sklearn.preprocessing import StandardScaler
        
        # Move model on GPU if available
        enable_cuda=True
        self.device=torch.device('cuda' if torch.cuda.is_available() and
                            enable_cuda else 'cpu')
        if self.verbose>0:
            print('device:',self.device)

        self.verbose=verbose
        self.outformat=outformat
        self.n_dim=numpy.shape(in_data)[1]
        self.n_pts=numpy.shape(in_data)[0]
        self.data=in_data
        self.num_layers=num_layers
        self.max_iter=max_iter
        self.num_hidden_channels=num_hidden_channels
        self.adam_lr=adam_lr
        self.adam_decay=adam_decay
        
        try:
            self.SS1=StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        except Exception as e:
            print('Exception at transform in nflows_nsf::set_data().',e)
            raise
        
        try:

            # Convert numpy to torch, there's probably a better way...
            ten_in=torch.zeros((self.n_pts,self.n_dim),device=self.device)
            for i in range(0,self.n_pts):
                for j in range(0,self.n_dim):
                    ten_in[i,j]=in_data_trans[i,j]
                    
            self.base=normflows.distributions.base.DiagGaussian(self.n_dim)

            # Create normalizing flow
            layer_func=normflows.flows.AutoregressiveRationalQuadraticSpline
            
            flow_layers=[]
            for i in range(num_layers):
                flow_layers+=[layer_func(self.n_dim,1,
                                         self.num_hidden_channels,
                                         permute_mask=True)]
                
            self.model=normflows.NormalizingFlow(self.base,flow_layers)

            self.model=self.model.to(self.device)

            self.model.eval()
            self.model.train()

            optimizer=torch.optim.Adam(self.model.parameters(),
                                       lr=self.adam_lr,
                                       weight_decay=self.adam_decay)

            for it in range(0,self.max_iter):
                
                optimizer.zero_grad()
                loss=self.model.forward_kld(ten_in)

                if ~(torch.isnan(loss) | torch.isinf(loss)):
                    loss.backward()
                    optimizer.step()

                print('it,max_iter,loss: %d %d %7.6e' %
                      (it,max_iter,loss.to('cpu').data.numpy()))
                
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
                                                      'max_iter'],
                                list_of_floats=['adam_lr','adam_decay'])
            if self.verbose>1:
                print('String:',options,'Dictionary:',dct)
                  
            self.set_data(in_data,**dct)
        except Exception as e:
            print('Exception in nflows_nsf::set_data_str()',
                  'Failed.\n  ',e)
            raise

        return

    def sample(self,n_samples=1):
        """Sample the distribution

        The output is a list or numpy array, depending on which option
        was specified to set_data() or set_data_str(). The list or
        numpy array is only one-dimensional if ``n_samples`` is 1.
        """
        
        out,out_prob=self.model.sample(n_samples)
        if self.device!='cpu':
            out=out.to('cpu')
        out=out.detach().numpy()
        
        if n_samples==1:
            out_trans=self.SS1.inverse_transform(out)[0]
        else:
            out_trans=self.SS1.inverse_transform(out)

        if self.verbose>2:
            print('out_trans:',type(out_trans),numpy.shape(out_trans),
                  out_trans,self.outformat)

        if self.outformat=='list':
            return out_trans.tolist()

        out_numpy=numpy.ascontiguousarray(out_trans)

        return out_numpy
        
    def log_pdf(self,x):
        """Return the log likelihood

        The value ``x`` can be a single point, expressed as a
        one-dimensional list or numpy array, or a series of
        points specified as a numpy array.
        
        If ``x`` contains only one point, then only a single floating
        point value is returned. Otherwise, the return type is a list
        or numpy array, depending on the value of ``outformat``.
        """
        import torch

        # Validate input
        if isinstance(x,list):
            if isinstance(x[0],list):
                if len(x[0])!=self.n_dim:
                    print('List does not have correct dimension',
                          'in nflows_nsf::log_pdf().')
                    raise ValueError(('List does not have correct '+
                                      'dimension in nflows_nsf::log_pdf().'))
                x_trans=self.SS1.transform(x)
            else:
                if len(x)!=self.n_dim:
                    print('Single point (list) does not have correct',
                          'dimension in nflows_nsf::log_pdf().')
                    raise ValueError(('Single point (list) does not '+
                                      'have correct dimension '+
                                      'in nflows_nsf::log_pdf().'))
                x_trans=self.SS1.transform([x])
        else:
            if len(x.shape)==2:
                if x.shape[1]!=self.n_dim:
                    print('Array does not have correct dimension',
                          'in nflows_nsf::log_pdf().')
                    raise ValueError(('Array does not have correct '+
                                      'dimension in nflows_nsf::log_pdf().'))
                x_trans=self.SS1.transform(x)
            else:
                if x.shape[0]!=self.n_dim:
                    print('Single point (numpy) does not have correct',
                          'dimension in nflows_nsf::log_pdf().')
                    raise ValueError(('Single point (numpy) does not '+
                                      'have correct dimension '+
                                      'in nflows_nsf::log_pdf().'))
                x_trans=self.SS1.transform([x])
            
        if self.verbose>2:
            print('x,x_trans:',x,x_trans,type(x_trans))
        x2=torch.zeros((x_trans.shape[0],
                        self.n_dim),device=self.device)
        for j in range(0,x_trans.shape[0]):
            for i in range(0,self.n_dim):
                x2[j,i]=x_trans[j,i]
            
        res=self.model.log_prob(x2)
        if self.device!='cpu':
            res=res.to('cpu')
        res=res.detach().numpy()
        
        if self.verbose>2:
            print(type(res),res)

        if len(res.shape)==1 and res.shape[0]==1:
            return res[0]

        if self.outformat=='list':
            return res.tolist()
        
        return res

    def pdf(self,x):
        """
        Return the likelihood 
        """
        return numpy.exp(self.log_pdf(x))
        
