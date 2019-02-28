    ["table","plot-ser",
     "Plot two series from a row in table.",
     "<row> <pattern 1> <pattern 2>",""],
    ["table","plot1-ser",
     "Plot a series from a row in table.","<row> <pattern>",""],
    
    def plot_ser(self,o2scl_hdf,amp,args):
        """
        """

        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        # Set up wrapper for type function
        type_fn=o2scl_hdf.o2scl_acol_get_type
        type_fn.argtypes=[ctypes.c_void_p,int_ptr,char_ptr_ptr]

        # Get current type
        it=ctypes.c_int(0)
        type_ptr=char_ptr()
        type_fn(amp,ctypes.byref(it),ctypes.byref(type_ptr))
                
        curr_type=b''
        for i in range(0,it.value):
            curr_type=curr_type+type_ptr[i]
                        
        if curr_type==b'table':
                            
            failed=False

            get_fn=o2scl_hdf.o2scl_acol_get_row_ser
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            row_ix=ctypes.c_int(int(args[0]))

            pat_x=ctypes.c_char_p(force_bytes(args[1]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,pat_x,row_ix,ctypes.byref(idx),
                           ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get row with index '+args[0]+
                      ' and pattern "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]

            pat_y=ctypes.c_char_p(force_bytes(args[2]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,pat_y,row_ix,ctypes.byref(idy),
                           ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get row with index '+args[0]+
                      ' and pattern "'+args[2]+'".')
                failed=True
                
            if failed==False:
                yv=[ptry[i] for i in range(0,idy.value)]
                
            if failed==False:
                
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)>=4:
                    plot.plot(xv,yv,**string_to_dict(args[3]))
                else:
                    plot.plot(xv,yv)

                if self.logx==True:
                    self.axes.set_xscale('log')
                if self.logy==True:
                    self.axes.set_yscale('log')
                    
                if self.xset==True:
                    plot.xlim([self.xlo,self.xhi])
                if self.yset==True:
                    plot.ylim([self.ylo,self.yhi])
                                 
            # End of section for 'table' type
        else:
            print("Command 'plot-ser' not supported for type",
                  curr_type,".")
            return
        
        # End of 'plot_ser' function
                                 
    def plot1_ser(self,o2scl_hdf,amp,args):
        """
        Perform a series of plots with a table object.
        """

        # Useful pointer types
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        int_ptr=ctypes.POINTER(ctypes.c_int)
        
        # Set up wrapper for type function
        type_fn=o2scl_hdf.o2scl_acol_get_type
        type_fn.argtypes=[ctypes.c_void_p,int_ptr,char_ptr_ptr]

        # Get current type
        it=ctypes.c_int(0)
        type_ptr=char_ptr()
        type_fn(amp,ctypes.byref(it),ctypes.byref(type_ptr))
                
        curr_type=b''
        for i in range(0,it.value):
            curr_type=curr_type+type_ptr[i]
                        
        if curr_type==b'table':
                            
            failed=False

            get_fn=o2scl_hdf.o2scl_acol_get_row_ser
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            row_ix=ctypes.c_int(int(args[0]))

            pat_y=ctypes.c_char_p(force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,pat_y,row_ix,ctypes.byref(idy),
                           ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get row with index '+args[0]+
                      ' and pattern "'+args[2]+'".')
                failed=True
                
            if failed==False:
                yv=[ptry[i] for i in range(0,idy.value)]
                
            if failed==False:
                
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)>=4:
                    plot.plot(yv,**string_to_dict(args[2]))
                else:
                    plot.plot(yv)

                if self.logx==True:
                    self.axes.set_xscale('log')
                if self.logy==True:
                    self.axes.set_yscale('log')
                    
                if self.xset==True:
                    plot.xlim([self.xlo,self.xhi])
                if self.yset==True:
                    plot.ylim([self.ylo,self.yhi])
                                 
            # End of section for 'table' type
        else:
            print("Command 'plot-ser' not supported for type",
                  curr_type,".")
            return
        
        # End of 'plot1_ser' function
                                 

                        elif cmd_name=='plot-ser' or cmd_name=='plot_ser':
                    
                    if self.verbose>2:
                        print('Process plot-ser.')

                    self.plot_ser(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='plot1-ser' or cmd_name=='plot1_ser':
                    
                    if self.verbose>2:
                        print('Process plot1-ser.')

                    self.plot1_ser(o2scl_hdf,amp,strlist[ix+1:ix_next])

    def plotm(self,colx,coly,files,**kwargs):
        """
        For each file in list ``files``, read the first object of type
        ``table`` and plot the columns with name ``colx`` and ``coly``
        from that file on the same plot.
        """
        if self.verbose>2:
            print('plotm',colx,coly,files,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        for i in range(0,len(files)):
            self.dset=self.h5r.h5read_first_type(files[i],'table')
            self.dtype='table'
            if self.logx==True:
                if self.logy==True:
                    plot.loglog(self.dset['data/'+colx],
                                self.dset['data/'+coly],**kwargs)
                else:
                    plot.semilogx(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
            else:
                if self.logy==True:
                    plot.semilogy(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
                else:
                    plot.plot(self.dset['data/'+colx],
                              self.dset['data/'+coly],**kwargs)
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
        return
    
    def plotm(self,o2scl_hdf,amp,args):
        """
        Plot the same pair of columns from several files
        """

        int_ptr=ctypes.POINTER(ctypes.c_int)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)

        # Types for the file reading
        size_type=ctypes.c_int * 2
        parse_fn=o2scl_hdf.o2scl_acol_parse
        parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                           size_type,ctypes.c_char_p]

        # Define types to obtain the column
        get_fn=o2scl_hdf.o2scl_acol_get_column
        get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                         int_ptr,double_ptr_ptr]
        get_fn.restype=ctypes.c_int

        for ifile in range(0,len(self.plotfiles)):
            # Read the file
            str_args='-read'+self.plotfiles[ifile]
            ccp=ctypes.c_char_p(force_bytes(str_args))
            sizes=size_type(5,len(self.plotfiles[ifile]))
            parse_fn(amp,2,sizes,ccp)

            failed=False

            # Get the x column
            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),
                           ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            # Get the y column
            coly=ctypes.c_char_p(force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),
                           ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                # Copy the data over
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]
    
                # Plot
                if self.canvas_flag==False:
                    self.canvas()
                if self.logx==True:
                    if self.logy==True:
                        if len(args)<3:
                            plot.loglog(xv,yv)
                        else:
                            plot.loglog(xv,yv,**string_to_dict(args[2]))
                    else:
                        if len(args)<3:
                            plot.semilogx(xv,yv)
                        else:
                            plot.semilogx(xv,yv,**string_to_dict(args[2]))
                else:
                    if self.logy==True:
                        if len(args)<3:
                            plot.semilogy(xv,yv)
                        else:
                            plot.semilogy(xv,yv,**string_to_dict(args[2]))
                    else:
                        if len(args)<3:
                            plot.plot(xv,yv)
                        else:
                            plot.plot(xv,yv,**string_to_dict(args[2]))
            if ifile==0:                
                if self.xset==True:
                    plot.xlim([self.xlo,self.xhi])
                if self.yset==True:
                    plot.ylim([self.ylo,self.yhi])

        # End of 'plotm' function
        
    def plot1m(self,o2scl_hdf,amp,args):
        """
        Plot the same column from several files
        """
        
        int_ptr=ctypes.POINTER(ctypes.c_int)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        
        # Types for the file reading
        size_type=ctypes.c_int * 2
        parse_fn=o2scl_hdf.o2scl_acol_parse
        parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                           size_type,ctypes.c_char_p]

        # Define types to obtain the column
        get_fn=o2scl_hdf.o2scl_acol_get_column
        get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                         int_ptr,double_ptr_ptr]

        for ifile in range(0,len(self.plotfiles)):
            # Read the file
            str_args='-read'+self.plotfiles[ifile]
            ccp=ctypes.c_char_p(force_bytes(str_args))
            sizes=size_type(5,len(self.plotfiles[ifile]))
            parse_fn(amp,2,sizes,ccp)

            # Get the x column
            colx=ctypes.c_char_p(force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_fn(amp,colx,ctypes.byref(idx),
                   ctypes.byref(ptrx))

            # Copy the data over
            xv=[i for i in range(0,idx.value)]
            yv=[ptrx[i] for i in range(0,idx.value)]

            # Plot
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
                    if len(args)<2:
                        plot.loglog(xv,yv)
                    else:
                        plot.loglog(xv,yv,**string_to_dict(args[1]))
                else:
                    if len(args)<2:
                        plot.semilogx(xv,yv)
                    else:
                        plot.semilogx(xv,yv,**string_to_dict(args[1]))
            else:
                if self.logy==True:
                    if len(args)<2:
                        plot.semilogy(xv,yv)
                    else:
                        plot.semilogy(xv,yv,**string_to_dict(args[1]))
                else:
                    if len(args)<2:
                        plot.plot(xv,yv)
                    else:
                        plot.plot(xv,yv,**string_to_dict(args[1]))
                        
            if self.xset==True:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==True:
                plot.ylim([self.ylo,self.yhi])
                                
        # End of 'plot1m' function

    def plot1m(self,col,files,**kwargs):
        """
        For each file in list ``files``, read the first
        object of type ``table`` and plot the column
        with name ``col`` from that file on the same plot.
        """
        if self.verbose>2:
            print('plot1m',col,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        for i in range(0,len(files)):
            self.dset=self.h5r.h5read_first_type(files[i],'table')
            self.dtype='table'
            tlist=range(1,len(self.dset['data/'+col])+1)
            if self.logx==True:
                if self.logy==True:
                    plot.loglog(tlist,self.dset['data/'+col],**kwargs)
                else:
                    plot.semilogx(tlist,self.dset['data/'+col],**kwargs)
            else:
                if self.logy==True:
                    plot.semilogy(tlist,self.dset['data/'+col],**kwargs)
                else:
                    plot.plot(tlist,self.dset['data/'+col],**kwargs)
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
        return
    
