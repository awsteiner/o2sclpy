#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2022-2026, Andrew W. Steiner, Satyajit Roy, and
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

class interpm_torch_dnn:
    """Interpolate one or many multidimensional data sets using
    PyTorch.

    .. todo:: * Calculate second derivatives
              * More activation functions
              * move function_approx class outside of function
              * better handling of torch tensors as input and output
              * 'native' output format
              * partial derivatives inefficient because always computes
                gradient
              * add_data() for successive improvements
              * Allow user to control CPU vs. GPU
    """

    verbose=0
    """
    Verbosity parameter (default 0)
    """
    outformat='numpy'
    """
    Output format, either 'native', 'c++', or 'list' (default 'native')
    """
    
    def __init__(self):
        self.dnn=None
        self.SS1=None
        self.SS2=None
        self.transform_in=None
        self.transform_out=None
        self.nd_in=None
        self.nd_out=None
        self.device=None
        self.activation=None
        self.hlayers=None
        self.layer_norm=None

        # Import torch only once
        import torch
        
        self.torch=torch
        self.nn=torch.nn
        self.optim=torch.optim

        # sklearn imports
        
        import sklearn.preprocessing as preprocessing
        self.pp=preprocessing
        
        from sklearn.model_selection import train_test_split
        self.tts=train_test_split
        
        return

    def _string_to_activation(self, name):
        """
        Convert a string to an activation function
        """
        name = (name or 'relu').lower()
        if name == 'relu':
            return self.nn.ReLU()
        if name == 'tanh':
            return self.nn.Tanh()
        if name == 'gelu':
            return self.nn.GELU()
        return self.nn.ReLU()

    def set_data(self,in_data,out_data,outformat='numpy',verbose=0,
                 hlayers=[8,8],epochs=100,transform_in='none',
                 transform_out='none',test_size=0.0,activation='relu',
                 patience=20,device=None,seed=None,
                 layer_norm=True):
        """Early stopping is set with patience, and if patience is 0
        then the training never stops early.
        """

        if verbose>0:
            print('interpm_torch_dnn::set_data():')
            print('  outformat:',outformat)
            print('  in_data shape:',numpy.shape(in_data))
            print('  out_data shape:',numpy.shape(out_data))
            print('  transform_in:',transform_in)
            print('  transform_out:',transform_out)
            print('  test_size:',test_size)
            print('  device:',device)
            print('  activation:',activation)
            print('  hlayers:',hlayers)
            print('  layer_norm:',layer_norm)

        self.outformat=outformat
        self.verbose=verbose
        self.transform_in=transform_in
        self.transform_out=transform_out
        self.device=device
        self.hlayers=hlayers
        self.activation=activation
        self.layer_norm=layer_norm

        # ----------------------------------------------------------
        
        if seed is not None:
            numpy.random.seed(seed)
            self.torch.manual_seed(seed)

        if device is None:
            self.device=self.torch.device('cuda'
                                          if self.torch.cuda.is_available()
                                          else 'cpu')
        else:
            self.device=self.torch.device(device)
        
        # ----------------------------------------------------------
        # Handle the data transformations
        
        if self.transform_in=='moto':
            self.SS1=self.pp.MinMaxScaler(feature_range=(-1,1))
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='quant':
            self.SS1=self.pp.QuantileTransformer(n_quantiles=
                                                 in_data.shape[0])
            in_data_trans=self.SS1.fit_transform(in_data)
        elif self.transform_in=='standard':
            self.SS1=self.pp.StandardScaler()
            in_data_trans=self.SS1.fit_transform(in_data)
        else:
            in_data_trans=in_data
            
        if self.transform_out=='moto':
            self.SS2=self.pp.MinMaxScaler(feature_range=(-1,1))
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='quant':
            self.SS2=self.pp.QuantileTransformer(n_quantiles=
                                                 out_data.shape[0])
            out_data_trans=self.SS2.fit_transform(out_data)
        elif self.transform_out=='standard':
            self.SS2=self.pp.StandardScaler()
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

            print('interpm_torch_dnn::set_data():')
            print('  min,max before transformation: %7.6e %7.6e' %
                  (minv_old,maxv_old))
            print('  min,max after transformation : %7.6e %7.6e' %
                  (minv,maxv))
            
        if test_size>0.0:
            try:
                x_train,x_test,y_train,y_test=self.tts(
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
        self.nd_out=numpy.shape(y_train)[1]

        act=self._string_to_activation(self.activation)
        
        layers2=[]
        layers2.append(self.nn.Linear(self.nd_in,hlayers[0]))
        if layer_norm==True:
            layers2.append(self.nn.LayerNorm(hlayers[0]))
        layers2.append(act)
        for k in range(0,len(hlayers)-1):
            layers2.append(self.nn.Linear(hlayers[k],hlayers[k+1]))
            if layer_norm==True:
                layers2.append(self.nn.LayerNorm(hlayers[k+1]))
            layers2.append(act)
        layers2.append(self.nn.Linear(hlayers[len(hlayers)-1],
                                      self.nd_out))
        self.dnn=self.nn.Sequential(*layers2).to(self.device)
        
        # Convert numpy to torch, there's probably a better way...
        ten_in=self.torch.from_numpy(x_train).float().to(self.device)
        ten_out=self.torch.from_numpy(y_train).float().to(self.device)
        test_in=self.torch.from_numpy(x_test).float().to(self.device)
        test_out=self.torch.from_numpy(y_test).float().to(self.device)

        crit=self.nn.MSELoss()
        opt=self.optim.Adam(self.dnn.parameters(),lr=0.01)
        
        best_loss=0
        trigger=0
        best_model=0
        done=False
        epoch=0

        print('interpm_torch_dnn::set_data():')
        
        while done==False and epoch<epochs:
            
            self.dnn.train()
            opt.zero_grad()
            pred=self.dnn(ten_in)
            loss=crit(pred,ten_out)
            loss.backward()
            opt.step()

            self.dnn.eval()

            if test_size>0.0:
                with self.torch.no_grad():
                    test_pred=self.dnn(test_in)
                    test_loss=crit(test_pred,test_out)
            else:
                test_loss=loss
                
            if self.verbose>0:
                if test_size>0.0:
                    print('  Epoch:',str(epoch+1)+'/'+str(epochs),
                          ('loss: %7.6e, best_loss: %7.6e, '+
                           'test_loss: %7.6e') %
                          (loss.item(),best_loss,test_loss))
                           
                else:
                    print('  Epoch',str(epoch+1)+'/'+str(epochs),
                          'loss %7.6e, best_loss: %7.6e' %
                          (loss.item(),best_loss))
                    
            if epoch==0 or test_loss<best_loss:
                best_loss=test_loss
                best_model=copy.deepcopy(self.dnn.state_dict())
                trigger=0
            elif patience>0:
                # (Disable early stopping if patience is 0)
                trigger+=1
                if trigger>=patience:
                    if self.verbose>0:
                        print('  Stopping early.')
                    done=True
            
            epoch+=1

        self.dnn.load_state_dict(best_model)
            
        return
    
    def eval(self,v):
        """
        Evaluate the NN at point ``v``.
        """

        #print('eval,v',v)
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
        #print('eval,v_trans',v_trans)

        try:

            ten_in=self.torch.from_numpy(v_trans).float()
            self.dnn.eval()
            with self.torch.no_grad():
                pred=self.dnn(ten_in).cpu()
        except Exception as e:
            print('Exception 4 in interpm_torch_dnn:',e)
            raise
            
        #print('eval,pred',pred)
        if self.transform_out!='none':
            try:
                predx=pred.detach().numpy()
                if predx.ndim==1:
                    predx=predx.reshape(-1,1)
                pred_trans=self.SS2.inverse_transform(predx)
            except Exception as e:
                print('Exception 5 in interpm_torch_dnn:',e)
                raise
        else:
            pred_trans=pred.detach().numpy()
        #print('eval,pred_trans',pred_trans)
    
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
        #print('el,v',v)
        try:
            if self.transform_in!='none':
                v_trans=self.SS1.transform(v)
            else:
                v_trans=v
        except Exception as e:
            print('Exception at input transformation ',
                  'in interpm_torch_dnn::eval_list():',e)
            raise
        #print('el,v_trans',v_trans)

        try:
            ten_in=self.torch.from_numpy(v).float()
            self.dnn.eval()
            with self.torch.no_grad():
                pred=self.dnn(ten_in).cpu()
        except Exception as e:
            print('Exception at evaluation in '+
                  'interpm_torch_dnn::eval_list():',e)
            raise
        #print('el,pred',pred)

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
        #print('el,pred_trans',pred_trans)
    
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
            
            ten_in=self.torch.from_numpy(v_trans).float()
                
            ten_in.requires_grad_(True)
            self.dnn.eval()
            pred=self.dnn(ten_in)
            
            from torch.autograd.functional import jacobian
            def f(inp):
                return self.dnn(inp).squeeze(0)
            jac=jacobian(f,ten_in)  # shape (n_out, n_in)
            jac=jac.detach().cpu().numpy()
            
        except Exception as e:
            print('Exception at model evalution',
                  'in interpm_torch_dnn::deriv():',e)
            raise
            
        if self.transform_out=='none':
            return jac
        
        if self.transform_out!='moto' and self.transform_out!='standard':
            raise ValueError("Cannot get derivative.")
        
        try:
            # sklearn: inverse is y = scale_ * y_scaled + mean_
            scales=getattr(self.SS2,'scale_',None)
            if scales is None:
                raise RuntimeError("transform_out has no scale_ attribute")
            # multiply each output row by scale
            jac=(jac.T*scales.reshape(-1)).T
        except:
            raise ValueError("Rescale.")
            
        return jac

        #if self.outformat=='list':
        #     return pgrad_trans.tolist()

        #if pgrad_trans.ndim==1:
        #    
        #    if self.verbose>1:
        #        print('interpm_torch_dnn::deriv():',
        #              'type(pgrad_trans),pgrad_trans:',
        #              type(pgrad_trans),pgrad_trans)
        #            
        #    return numpy.ascontiguousarray(pgrad_trans)
        
        #if self.verbose>1:
        #    print('interpm_torch_dnn::deriv():',
        #'type(pgrad_trans),pgrad_trans:',
        #          type(pgrad_trans),pgrad_trans)

        #return numpy.ascontiguousarray(pgrad_trans)

    def save(self,filename):
        """
        Save the interpolation settings to a file

        (No custom object support)
        """
        if filename[-3:]!='.pt':
            filename=filename+'.pt'
            
        #self.torch.save(self.dnn,filename)
        self.torch.save({'model_state': self.dnn.state_dict(),
                         'nd_in': self.nd_in,
                         'nd_out': self.nd_out,
                         'activation': self.activation,
                         'hlayers': self.hlayers},filename)
        
        return
    
    def load(self,filename,device=None):
        """Load the interpolation settings from a file
        """        
        if filename[-3:]!='.pt':
            filename=filename+'.pt'
            
        if device is None:
            self.device=self.torch.device('cuda'
                                          if self.torch.cuda.is_available()
                                          else 'cpu')
        else:
            self.device=self.torch.device(device)
            
        data=self.torch.load(filename,map_location=self.device)
        
        if (not 'model_state' in data or
            not 'nd_in' in data or
            not 'nd_out' in data or
            not 'activation' in data or
            not 'hlayers' in data):
            raise RuntimeError("Missing information in "+
                               "interpm_torch_dnn::load()")
        
        self.nd_in=data['nd_in']
        self.nd_out=data['nd_out']
        self.activation=data['activation']
        self.hlayers=data['hlayers']
        
        act=self._string_to_activation(self.activation)
        
        layers2=[]
        layers2.append(self.nn.Linear(self.nd_in,self.hlayers[0]))
        layers2.append(act)
        for k in range(0,len(self.hlayers)-1):
            layers2.append(self.nn.Linear(self.hlayers[k],
                                          self.hlayers[k+1]))
            layers2.append(act)
        layers2.append(self.nn.Linear(self.hlayers[len(self.hlayers)-1],
                                      self.nd_out))
        self.dnn=self.nn.Sequential(*layers2).to(self.device)
        
        self.dnn.load_state_dict(data['model_state'])

        return

