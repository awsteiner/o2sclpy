"""
   -------------------------------------------------------------------
   Docstring for sphinx
   -------------------------------------------------------------------
"""
"""
   Todos:
   - new 'version' command
"""

import getopt, sys, h5py, math, os, hashlib
import matplotlib.pyplot as plot
from matplotlib.colors import LinearSegmentedColormap
import urllib.request
import numpy
import ctypes

version='0.921'

class cloud_file:
""" 
This class does what.
Or maybe this works.
"""
    
    force_subdir=False
    env_var=''
    username=''
    password=''
    verbose=1
    
    def md5(fname):
        """
        Compute the md5 hash of the specified file. This function
        reads 4k bytes at a time and updates the hash for each
        read in order to prevent from having to read the entire
        file in memory at once.
        """
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def download_file(self,data_dir,fname_orig,url,mhash):
        """ 
        Desc.
        Desc2.
        """
        force_subdir_val=self.force_subdir
        self.force_subdir=False
        fname=self.download_file_subdir(data_dir,'',fname_orig,url,
                                        mhash)
        self.force_subdir=force_subdir_val
        return fname

    def download_file_subdir(self,data_dir,subdir_orig,fname_orig,url,
                             mhash):
        """
        This function attempts to find a file named 'fname_orig' in
        subdirectory 'subdir_orig' of the data directory 'data_dir'. If
        'data_dir' is empty, it attempts to set it equal to the value of
        the environment variable 'env_var'. If that environment variable
        is not present, the user is prompted for the correct data
        directory. If the file is not found, then this function uses curl
        (or wget if curl was unsuccessful) to download the file from
        'url'. If this process was successful at finding or downloading
        the file, then the full filename is returned. Otherwise, an
        exception is thrown.
        
        Warning: this function has several potential security issues 
        and should not be used without due care.
    
        """
        # First obtain the data directory
        method=''
        if data_dir!='':
            method='arg'
        else:
            if self.env_var in os.environ:
                data_dir=os.environ[self.env_var]
                method='ev'
            if data_dir=='':
                data_dir=input('Data directory not set. Enter data directory: ')
                if data_dir!='':
                    method='ui'
        if data_dir=='' or method=='':
            raise ValueError('Failed to obtain data directory.')
        if method=='arg':
            if verbose>0:
                print('Data directory set (by function argument) to:',data_dir)
        elif method=='ev':
            if verbose>0:
                print('Data directory set (by environment variable) to:',
                      data_dir)
        else:
            if verbose>0:
                print('Data directory set (by user input) to:',data_dir)
    
        # Now test for the existence of the subdirectory and create it if
        # necessary
        subdir=''
        if self.force_subdir==True:
            subdir=data_dir+'/'+subdir_orig
            if os.path.isdir(subdir)==False:
                if verbose>0:
                    print('Directory not found and force_subdir is true.')
                    print('Trying to automatically create using "mkdir -p"')
                cmd='mkdir -p '+subdir
                ret=os.system(cmd)
                if ret!=0:
                    raise FileNotFoundError('Correct subdirectory does '+
                                            'not exist and failed to create.')
        else:
            subdir=data_dir

        # The local filename
        fname=subdir+'/'+fname_orig
        hash_match=False
        if os.path.isfile(fname)==True:
            mhash2=mda5(fname)
            if mhash==mhash2:
                hash_match=True
            elif verbose>0:
                print('Hash of file',fname,'did not match',mhash)
        elif verbose>0:
            print('Could not find file',fname)
            
        # Now download the file if it's not already present
        if hash_match==False or os.path.isfile(fname)==False:
            response=input('Hash did not match or data file '+fname+
                           ' not found. Download (y/Y/n/N)? ')
            ret=1
            if response=='y' or response=='Y':
                if verbose>0:
                    print('Trying two download:')
                urllib.request.urlretrieve(url,fname)
                ret=0
            if ret==0:
                mhash2=mda5(fname)
                if mhash!=mhash2:
                    raise ConnectionError('Downloaded file but '+
                                          'has does not match.')
            if ret!=0:
                raise ConnectionError('Failed to obtain data file.')
    
        # Return the final filename
        return fname

class hdf5_reader:
    """
    This class 
    """

    list_of_dsets=[]
    search_type=''

    def hdf5_is_object_type(self,name,obj):
        """
        If object 'obj' named 'name' is of type 'search_type', then add
        that name to 'list_of_dsets'
        """
        # Convert search_type to a bytes object
        search_type_bytes=bytes(self.search_type,'utf-8')
        if isinstance(obj,h5py.Group):
            if 'o2scl_type' in obj.keys():
                o2scl_type_dset=obj['o2scl_type']
                if o2scl_type_dset.__getitem__(0) == search_type_bytes:
                    self.list_of_dsets.append(name)
        return

    def h5read_first_type(self,fname,loc_type):
        """
        Read the first object of type 'loc_type' from file named 'fname'
        """
        del self.list_of_dsets[:]
        self.search_type=loc_type
        file=h5py.File(fname,'r')
        file.visititems(self.hdf5_is_object_type)
        if len(self.list_of_dsets)==0:
            str='Could not object of type '+loc_type+' in file '+fname+'.'
            raise RuntimeError(str)
        return file[self.list_of_dsets[0]]

    def h5read_name(self,fname,name):
        """
        Read object named 'name' from file named 'fname'
        """
        file=h5py.File(fname,'r')
        obj=file[name]
        o2scl_type_dset=obj['o2scl_type']
        loc_type=o2scl_type_dset.__getitem__(0)
        return (obj,loc_type)
    
    def h5read_type_named(self,fname,loc_type,name):
        """
        Read object of type 'loc_type' named 'name' from file named 'fname'
        """
        del self.list_of_dsets[:]
        self.search_type=loc_type
        file=h5py.File(fname,'r')
        file.visititems(self.hdf5_is_object_type)
        if name in self.list_of_dsets:
            return file[name]
        str='No object of type '+loc_type+' named '+name+' in file '+fname+'.'
        raise RuntimeError(str)
        return
    

# This is probably best replaced by get_str_array() below
#
# def parse_col_names(dset):
#     nc=dset['nc'].__getitem__(0)
#     nw=dset['nw'].__getitem__(0)
#     counter=dset['counter']
#     data=dset['data']
#     clist=[]
#     k=0
#     for i in range(0,nw):
#         column=''
#         for j in range(0,counter[i]):
#             column=column+str(unichr(data[k]))
#             k=k+1
#         clist.append(column)
#     return clist

def default_plot(lmar=0.14,bmar=0.12,rmar=0.04,tmar=0.04):
    """
    Common plot defaults
    """
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')
    plot.rcParams['lines.linewidth']=0.5
    fig=plot.figure(1,figsize=(6.0,6.0))
    fig.set_facecolor('white')
    ax=plot.axes([lmar,bmar,1.0-lmar-rmar,1.0-tmar-bmar])
    ax.minorticks_on()
    ax.tick_params('both',length=12,width=1,which='major')
    ax.tick_params('both',length=5,width=1,which='minor')
    plot.grid(False)
    return (fig,ax)
    
def get_str_array(dset):
    """
    Extract a string array from O2scl HDF5 dataset dset as a list
    """
    nw=dset['nw'][0]
    nc=dset['nc'][0]
    data=dset['data']
    counter=dset['counter']
    char_counter=1
    word_counter=0
    list=[]
    col=''
    for ix in range(0,nc):
        # Skip empty strings in the array
        done=0
        while done==0:
            if word_counter==nw:
                done=1
            elif counter[word_counter]==0:
                word_counter=word_counter+1
                list.append('')
            else:
                done=1
        col=col+str(chr(data[ix]))
        if char_counter==counter[word_counter]:
            list.append(col)
            col=''
            word_counter=word_counter+1
            char_counter=1
        else:
            char_counter=char_counter+1
    # We're done with the characters, but there are some blank
    # strings left. Add the appropriate blanks at the end.
    while word_counter<nw:
        list.append('')
        word_counter=word_counter+1
    return list
    
def parse_arguments(argv,verbose=0):
    """
    Parse command
    """
    list=[]
    unproc_list=[]
    if verbose>1:
        print('Number of arguments:', len(argv), 'arguments.')
        print('Argument List:', str(argv))
    ix=1
    while ix<len(argv):
        if verbose>1:
            print('Processing index',ix,'with value',argv[ix],'.')
        # Find first option, at index ix
        initial_ix_done=0
        while initial_ix_done==0:
            if ix==len(argv):
                initial_ix_done=1
            elif argv[ix][0]=='-':
                initial_ix_done=1
            else:
                if verbose>1:
                     print('Adding',argv[ix],' to unprocessed list.')
                unproc_list.append(argv[ix])
                ix=ix+1
        # If there is an option, then ix is its index
        if ix<len(argv):
            list_one=[]
            # Strip single and double dashes
            cmd_name=argv[ix][1:]
            if cmd_name[0]=='-':
                cmd_name=cmd_name[1:]
            # Add command name to list
            list_one.append(cmd_name)
            if verbose>1:
                print('Found option',cmd_name,'at index',ix)
            # Set ix_next to the next option, or to the end if
            # there is no next option
            ix_next=ix+1
            ix_next_done=0
            while ix_next_done==0:
                if ix_next==len(argv):
                    ix_next_done=1
                elif argv[ix_next][0]=='-':
                    ix_next_done=1
                else:
                    if verbose>1:
                        print('Adding '+argv[ix_next]+' with index '+
                              str(ix_next)+' to list for '+cmd_name)
                    list_one.append(argv[ix_next])
                    ix_next=ix_next+1
            list.append(list_one)
            ix=ix_next
    return (list,unproc_list)

def string_to_dict(s):
    """ 
    Desc
    """
    # First split into keyword = value pairs
    arr=s.split(',')
    # Create empty dictionary
    dct={}
    for i in range(0,len(arr)):
        # For each pair, split keyword and value...
        arr2=arr[i].split('=')
        # ...then assign to dictionary
        dct[arr2[0]]=arr2[1]
    return dct

class plotter:
    """ 
    Desc
    """

    h5r=hdf5_reader()
    dset=0
    axes=0
    fig=0
    canvas_flag=0
    dtype=''

    # Quantities modified by set/get
    
    logx=0
    logy=0
    logz=0
    xtitle=''
    ytitle=''
    xlo=0
    xhi=0
    xset=0
    ylo=0
    yhi=0
    yset=0
    zlo=0
    zhi=0
    zset=0
    verbose=1
    colbar=0
    plotfiles=''

    def reds2(self):
        cdict={'red': ((0.0,1.0,1.0),(1.0,1.0,1.0)),
               'green': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(1.0,0.0,0.0))}
        reds2=LinearSegmentedColormap('reds2',cdict)
        plot.register_cmap(cmap=reds2)

    def jet2(self):
        # white, blue, green, yellow, orange, red
        cdict={'red': ((0.0,1.0,1.0),(0.2,0.0,0.0),
                       (0.4,0.0,0.0),(0.6,1.0,1.0),
                       (0.8,1.0,1.0),(1.0,1.0,1.0)),
               'green': ((0.0,1.0,1.0),(0.2,0.0,0.0),
                         (0.4,0.5,0.5),(0.6,1.0,1.0),
                         (0.8,0.6,0.6),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(0.2,1.0,1.0),
                        (0.4,0.0,0.0),(0.6,0.0,0.0),
                        (0.8,0.0,0.0),(1.0,0.0,0.0))}
        jet2=LinearSegmentedColormap('jet2',cdict)
        plot.register_cmap(cmap=jet2)

    def pastel2(self):
        # white, blue, green, yellow, orange, red
        cdict={'red': ((0.0,1.0,1.0),(0.2,0.3,0.3),
                       (0.4,0.3,0.3),(0.6,1.0,1.0),
                       (0.8,1.0,1.0),(1.0,1.0,1.0)),
               'green': ((0.0,1.0,1.0),(0.2,0.3,0.3),
                         (0.4,0.5,0.5),(0.6,1.0,1.0),
                         (0.8,0.6,0.6),(1.0,0.3,0.3)),
               'blue': ((0.0,1.0,1.0),(0.2,1.0,1.0),
                        (0.4,0.3,0.3),(0.6,0.3,0.3),
                        (0.8,0.3,0.3),(1.0,0.3,0.3))}
        pastel2=LinearSegmentedColormap('pastel2',cdict)
        plot.register_cmap(cmap=pastel2)

    def greens2(self):
        cdict={'red': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'green': ((0.0,1.0,1.0),(1.0,1.0,1.0)),
               'blue': ((0.0,1.0,1.0),(1.0,0.0,0.0))}
        greens2=LinearSegmentedColormap('greens2',cdict)
        plot.register_cmap(cmap=greens2)

    def blues2(self):
        cdict={'red': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'green': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(1.0,1.0,1.0))}
        blues2=LinearSegmentedColormap('blues2',cdict)
        plot.register_cmap(cmap=blues2)
        
    def contour_plot(self,level,**kwargs):
        if self.force_bytes(self.dtype)!=b'vector<contour_line>':
            print('Wrong type',self.dtype,'for contour_plotx.')
            return
        if self.verbose>2:
            print('contour_plot',level,kwargs)
        if self.canvas_flag==0:
            self.canvas()
        n_lines=self.dset['n_lines'][0]
        for i in range(0,n_lines):
            line_level=self.dset['line_'+str(i)+'/level'][0]
            if abs(level-line_level) < 1.0e-7:
                if self.logx==1:
                    if self.logy==1:
                        plot.loglog(self.dset['line_'+str(i)+'/x'],
                                    self.dset['line_'+str(i)+'/y'],**kwargs)
                    else:
                        plot.semilogx(self.dset['line_'+str(i)+'/x'],
                                      self.dset['line_'+str(i)+'/y'],**kwargs)
                else:
                    if self.logy==1:
                        plot.semilogy(self.dset['line_'+str(i)+'/x'],
                                      self.dset['line_'+str(i)+'/y'],**kwargs)
                    else:
                        plot.plot(self.dset['line_'+str(i)+'/x'],
                                  self.dset['line_'+str(i)+'/y'],**kwargs)
        return
 
    def plot(self,colx,coly,**kwargs):
        
        if self.force_bytes(self.dtype)==b'table':
            if self.verbose>2:
                print('plot',colx,coly,kwargs)
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                if self.logy==1:
                    plot.loglog(self.dset['data/'+colx],
                                self.dset['data/'+coly],**kwargs)
                else:
                    plot.semilogx(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
            else:
                if self.logy==1:
                    plot.semilogy(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
                else:
                    plot.plot(self.dset['data/'+colx],
                              self.dset['data/'+coly],**kwargs)
            if self.xset==1:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==1:
                plot.ylim([self.ylo,self.yhi])
        elif self.force_bytes(self.dtype)==b'hist':
            size=dset['size'][0]
            bins=dset['bins']
            weights=dset['weights']
            rmode=dset['rmode'][0]
            reps=bins[0:size-1]
            for i in range(0,size):
                reps[i]=(bins[i]+bins[i+1])/2
            if self.logx==1:
                if self.logy==1:
                    plot.loglog(reps,weights,**kwargs)
                else:
                    plot.semilogx(reps,weights,**kwargs)
            else:
                if self.logy==1:
                    plot.semilogy(reps,weights,**kwargs)
                else:
                    plot.plot(reps,weights,**kwargs)
            if self.xset==1:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==1:
                plot.ylim([self.ylo,self.yhi])
            return
        return

    def plot1(self,col,**kwargs):
        if self.force_bytes(self.dtype)!=b'table':
            print('Wrong type',self.dtype,'for plot1.')
            return
        if self.verbose>2:
            print('plot1',col,kwargs)
        if self.canvas_flag==0:
            self.canvas()
        tlist=range(1,len(self.dset['data/'+col])+1)
        if self.logx==1:
            if self.logy==1:
                plot.loglog(tlist,self.dset['data/'+col],**kwargs)
            else:
                plot.semilogx(tlist,self.dset['data/'+col],**kwargs)
        else:
            if self.logy==1:
                plot.semilogy(tlist,self.dset['data/'+col],**kwargs)
            else:
                plot.plot(tlist,self.dset['data/'+col],**kwargs)
        if self.xset==1:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==1:
            plot.ylim([self.ylo,self.yhi])
        return

    def plot1m(self,col,files,**kwargs):
        if self.verbose>2:
            print('plot1m',col,kwargs)
        if self.canvas_flag==0:
            self.canvas()
        for i in range(0,len(files)):
            self.dset=self.h5r.h5read_first_type(files[i],'table')
            self.dtype='table'
            tlist=range(1,len(self.dset['data/'+col])+1)
            if self.logx==1:
                if self.logy==1:
                    plot.loglog(tlist,self.dset['data/'+col],**kwargs)
                else:
                    plot.semilogx(tlist,self.dset['data/'+col],**kwargs)
            else:
                if self.logy==1:
                    plot.semilogy(tlist,self.dset['data/'+col],**kwargs)
                else:
                    plot.plot(tlist,self.dset['data/'+col],**kwargs)
        if self.xset==1:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==1:
            plot.ylim([self.ylo,self.yhi])
        return
    
    def plotm(self,colx,coly,files,**kwargs):
        if self.verbose>2:
            print('plotm',colx,coly,files,kwargs)
        if self.canvas_flag==0:
            self.canvas()
        for i in range(0,len(files)):
            self.dset=self.h5r.h5read_first_type(files[i],'table')
            self.dtype='table'
            if self.logx==1:
                if self.logy==1:
                    plot.loglog(self.dset['data/'+colx],
                                self.dset['data/'+coly],**kwargs)
                else:
                    plot.semilogx(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
            else:
                if self.logy==1:
                    plot.semilogy(self.dset['data/'+colx],
                                  self.dset['data/'+coly],**kwargs)
                else:
                    plot.plot(self.dset['data/'+colx],
                              self.dset['data/'+coly],**kwargs)
        if self.xset==1:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==1:
            plot.ylim([self.ylo,self.yhi])
        return
    
    def hist(self,col,**kwargs):
        if self.verbose>2:
            print('hist',kwargs)
        if self.canvas_flag==0:
            self.canvas()
        for key in kwargs:
            if key=='bins':
                kwargs[key]=int(kwargs[key])
        if self.force_bytes(self.dtype)==b'table':
            plot.hist(self.dset['data/'+col],**kwargs)
        else:
            print('Wrong type',self.dtype,'for hist()')
        return

    def hist2d(self,colx,coly,**kwargs):
        if self.verbose>2:
            print('hist2d',colx,coly,kwargs)
        if self.canvas_flag==0:
            self.canvas()
        for key in kwargs:
            if key=='bins':
                kwargs[key]=int(kwargs[key])
        plot.hist2d(self.dset['data/'+colx],self.dset['data/'+coly],**kwargs)
        return

    def line(self,x1,y1,x2,y2,**kwargs):
        if self.verbose>2:
            print('Line',x1,y1,x2,y1)
        if self.canvas_flag==0:
            self.canvas()
        plot.plot([x1,x2],[y1,y2],**kwargs)
        return

    def reset_xlimits(self):
        self.xset=0
        return

    def xlimits(self,xlo,xhi):
        self.xlo=xlo
        self.xhi=xhi
        self.xset=1
        if self.canvas_flag==1:
            plot.xlim([xlo,xhi])
        return

    def reset_ylimits(self):
        self.yset=0
        return

    def ylimits(self,ylo,yhi):
        self.ylo=ylo
        self.yhi=yhi
        self.yset=1
        if self.canvas_flag==1:
            plot.ylim([ylo,yhi])
        return

    def canvas(self):
        if self.verbose>2:
            print('Canvas')
        # Default o2mpl plot
        (self.fig,self.axes)=default_plot()
        # Plot limits
        if self.xset==1:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==1:
            plot.ylim([self.ylo,self.yhi])
        # Titles
        if self.xtitle!='':
            plot.xlabel(self.xtitle,fontsize=16)
        if self.ytitle!='':
            plot.ylabel(self.ytitle,fontsize=16)
        self.canvas_flag=1
        return

    def move_labels(self):
        # Move tick labels
        for label in self.axes.get_xticklabels():
            t=label.get_position()
            t2=t[0],t[1]-0.01
            label.set_position(t2)
            label.set_fontsize(16)
        for label in self.axes.get_yticklabels():
            t=label.get_position()
            t2=t[0]-0.01,t[1]
            label.set_position(t2)
            label.set_fontsize(16)
        return

    def show(self):
        plot.show()
        return

    def save(self,filename):
        if self.verbose>0:
            print('Saving as',filename,'.')
        plot.savefig(filename)
        return

    def read(self,filename):
        if self.verbose>0:
            print('Reading file',filename,'.')
        self.dset=self.h5r.h5read_first_type(filename,'table')
        self.dtype='table'
        return

    def read_type(self,filename,loc_type):
        if self.verbose>0:
            print('Reading object of type',loc_type,
                  'in file',filename,'.')
        self.dset=self.h5r.h5read_first_type(filename,loc_type)
        self.dtype=loc_type
        return

    def read_name(self,filename,name):
        if self.verbose>0:
            print('Reading object named',name,'in file',filename,'.')
        atuple=self.h5r.h5read_name(filename,name)
        self.dset=atuple[0]
        self.dtype=atuple[1]
        return

    def force_bytes(self,obj):
        """
        In cases where we're unsure whether or not obj is
        a string or bytes object, we ensure it's a bytes
        object by converting if necessary.
        """
        if isinstance(obj,numpy.bytes_)==False and isinstance(obj,bytes)==False:
            return bytes(obj,'utf-8')
        return obj
    
    def list(self):
        if self.force_bytes(self.dtype)==b'table':
            col_list=get_str_array(self.dset['col_names'])
            if self.verbose>2:
                print('-----------------------')
            unit_list=[]
            unit_flag=self.dset['unit_flag'][0]
            print('unit_flag',unit_flag)
            if self.verbose>2:
                print('unit_flag:',unit_flag)
            if unit_flag==1:
                unit_list=get_str_array(self.dset['units'])
                if self.verbose>2:
                    print('-----------------------')
                    print('unit_list:',unit_list)
            print(len(col_list),'columns.')
            for ix in range(0,len(col_list)):
                if unit_flag:
                    print(str(ix)+'. '+col_list[ix]+' ['+unit_list[ix]+']')
                else:
                    print(str(ix)+'. '+col_list[ix])
            print(self.dset['nlines'][0],'lines.')
            if self.verbose>2:
                print('Done in list')
        elif self.force_bytes(self.dtype)==b'table3d':
            sl_list=get_str_array(self.dset['slice_names'])
            print(len(sl_list),'slices.')
            for ix in range(0,len(sl_list)):
                print(str(ix)+'. '+sl_list[ix])
            xgrid=self.dset['xval'].value
            ygrid=self.dset['yval'].value
            lxgrid=len(xgrid)
            lygrid=len(ygrid)
            print('X-grid start: '+str(xgrid[0])+' end: '+
                  str(xgrid[lxgrid-1])+' size '+str(lxgrid))
            print('Y-grid start: '+str(ygrid[0])+' end: '+
                  str(ygrid[lygrid-1])+' size '+str(lygrid))
        else:
            print('Cannot list type',self.dtype)
        return

    def den_plot(self,slice_name,**kwargs):
        if self.force_bytes(self.dtype)==b'table3d':
            name='data/'+slice_name
            sl=self.dset[name].value
            sl=sl.transpose()
            xgrid=self.dset['xval'].value
            ygrid=self.dset['yval'].value
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                for i in range(0,len(xgrid)):
                    xgrid[i]=math.log(xgrid[i],10)
            if self.logy==1:
                for i in range(0,len(ygrid)):
                    ygrid[i]=math.log(ygrid[i],10)
            lx=len(xgrid)
            ly=len(ygrid)
            plot.imshow(sl,interpolation='nearest',
                        origin='lower',
                        extent=[xgrid[0]-(xgrid[1]-xgrid[0])/2,
                                xgrid[lx-1]+(xgrid[lx-1]-xgrid[lx-2])/2,
                                ygrid[0]-(ygrid[1]-ygrid[0])/2,
                                ygrid[ly-1]+(ygrid[ly-1]-ygrid[ly-2])/2],
                        aspect='auto',**kwargs)
            if self.colbar>0:
                plot.colorbar()
                
        else:
            print('Cannot density plot object of type',self.dtype)
        return

    def set(self,name,value):
        if self.verbose>0:
            print('Set',name,'to',value)
        if name=='logx':
            self.logx=int(value)
        elif name=='logy':
            self.logy=int(value)
        elif name=='xtitle':
            self.xtitle=value
        elif name=='ytitle':
            self.ytitle=value
        elif name=='xlo':
            self.xlo=float(value)
            self.xset=1
        elif name=='xhi':
            self.xhi=float(value)
            self.xset=1
        elif name=='xset':
            self.xset=int(value)
        elif name=='ylo':
            self.ylo=float(value)
            self.yset=1
        elif name=='yhi':
            self.yhi=float(value)
            self.yset=1
        elif name=='yset':
            self.yset=int(value)
        elif name=='zlo':
            self.zlo=float(value)
            self.zset=1
        elif name=='zhi':
            self.zhi=float(value)
            self.zset=1
        elif name=='zset':
            self.zset=int(value)
        elif name=='verbose':
            self.verbose=int(value)
        elif name=='colbar':
            self.colbar=int(value)
        else:
            print('No variable named',name)
        return

    def ttext(self,tx,ty,str,**kwargs):
        if self.canvas_flag==0:
            self.canvas()
        self.axes.text(tx,ty,str,transform=self.axes.transAxes,
                       fontsize=16,va='center',ha='center',
                       **kwargs)
        return

    def text(self,tx,ty,str,**kwargs):
        if self.canvas_flag==0:
            self.canvas()
        self.axes.text(tx,ty,str,
                       fontsize=16,va='center',ha='center',**kwargs)
        return

    def get(self,name):
        if name=='colbar' or name=='':
            print('The value of colbar is',self.colbar,'.')
        if name=='logx' or name=='':
            print('The value of logx is',self.logx,'.')
        if name=='logy' or name=='':
            print('The value of logy is',self.logy,'.')
        if name=='verbose' or name=='':
            print('The value of verbose is',self.verbose,'.')
        if name=='xhi' or name=='':
            print('The value of xhi is',self.xhi,'.')
        if name=='xlo' or name=='':
            print('The value of xlo is',self.xlo,'.')
        if name=='xset' or name=='':
            print('The value of xset is',self.xset,'.')
        if name=='xtitle' or name=='':
            print('The value of xtitle is',self.xtitle,'.')
        if name=='yhi' or name=='':
            print('The value of yhi is',self.yhi,'.')
        if name=='ylo' or name=='':
            print('The value of ylo is',self.ylo,'.')
        if name=='yset' or name=='':
            print('The value of yset is',self.yset,'.')
        if name=='ytitle' or name=='':
            print('The value of ytitle is',self.ytitle,'.')
        if name=='zhi' or name=='':
            print('The value of zhi is',self.zhi,'.')
        if name=='zlo' or name=='':
            print('The value of zlo is',self.zlo,'.')
        if name=='zset' or name=='':
            print('The value of zset is',self.zset,'.')
        return

    def set_intl(self,o2scl_hdf,amp,args):
        
        if (args[0]=='logx' or args[0]=='xtitle' or
            args[0]=='logy' or args[0]=='ytitle' or
            args[0]=='xlo' or args[0]=='ylo' or
            args[0]=='xset' or args[0]=='xhi' or
            args[0]=='yhi' or args[0]=='yset' or
            args[0]=='zlo' or args[0]=='zhi' or
            args[0]=='zset' or args[0]=='colbar' or
            args[0]=='verbose'):
                
            self.set(args[0],args[1])
            
        str_args='-set'
        size_type=ctypes.c_int * (len(args)+1)
        sizes=size_type()
        sizes[0]=len('set')+1
            
        for i in range(0,len(args)):
            str_args=str_args+args[i]
            sizes[i+1]=len(args[i])
        ccp=ctypes.c_char_p(self.force_bytes(str_args))
    
        parse_fn=o2scl_hdf.o2scl_acol_parse
        parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                           size_type,ctypes.c_char_p]
            
        parse_fn(amp,len(args)+1,sizes,ccp)

    def get_intl(self,o2scl_hdf,amp,args):
        
        if (argv[ix+1]=='logx' or argv[ix+1]=='xtitle' or
            argv[ix+1]=='logy' or argv[ix+1]=='ytitle' or
            argv[ix+1]=='xlo' or argv[ix+1]=='ylo' or
            argv[ix+1]=='xset' or argv[ix+1]=='xhi' or
            argv[ix+1]=='yhi' or argv[ix+1]=='yset' or
            argv[ix+1]=='zlo' or argv[ix+1]=='zhi' or
            argv[ix+1]=='zset' or argv[ix+1]=='colbar'):
            
            self.get(args[0])
                            
        else:
                        
            str_args='-get'
            size_type=ctypes.c_int * (len(args)+1)
            sizes=size_type()
            sizes[0]=len('get')+1
        
            for i in range(0,len(args)):
                str_args=str_args+args[i]
                sizes[i+1]=len(args[i])
            ccp=ctypes.c_char_p(self.force_bytes(str_args))
        
            parse_fn=o2scl_hdf.o2scl_acol_parse
            parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                              size_type,ctypes.c_char_p]
        
            parse_fn(amp,len(args)+1,sizes,ccp)

    def gen_intl(self,o2scl_hdf,amp,cmd_name,args):

        str_args='-'+cmd_name
        size_type=ctypes.c_int * (len(args)+1)
        sizes=size_type()
        sizes[0]=len(cmd_name)+1
        
        for i in range(0,len(args)):
            str_args=str_args+args[i]
            sizes[i+1]=len(args[i])
        ccp=ctypes.c_char_p(self.force_bytes(str_args))

        parse_fn=o2scl_hdf.o2scl_acol_parse
        parse_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                           size_type,ctypes.c_char_p]
        
        parse_fn(amp,len(args)+1,sizes,ccp)

    def get_type_intl(self,o2scl_hdf,amp):
        
        int_ptr=ctypes.POINTER(ctypes.c_int)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        
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
                        
        return curr_type
        
    def den_plot_intl(self,o2scl_hdf,amp,args):

        int_ptr=ctypes.POINTER(ctypes.c_int)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)

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
                        
        if curr_type==b'table3d':
            
            get_fn=o2scl_hdf.o2scl_acol_get_slice
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr,
                             int_ptr,double_ptr_ptr,double_ptr_ptr]

            slice=ctypes.c_char_p(self.force_bytes(args[0]))
            nx=ctypes.c_int(0)
            ptrx=double_ptr()
            ny=ctypes.c_int(0)
            ptry=double_ptr()
            ptrs=double_ptr()
            get_fn(amp,slice,ctypes.byref(nx),ctypes.byref(ptrx),
                   ctypes.byref(ny),ctypes.byref(ptry),
                   ctypes.byref(ptrs))

            xgrid=[ptrx[i] for i in range(0,nx.value)]
            ygrid=[ptry[i] for i in range(0,ny.value)]
            stemp=[ptrs[i] for i in range(0,nx.value*ny.value)]
            stemp2=numpy.array(stemp)
            sl=stemp2.reshape(nx.value,ny.value)
            sl=sl.transpose()

            if self.logx==1:
                xgrid=[math.log(ptrx[i],10) for i in
                       range(0,nx.value)]
            if self.logy==1:
                ygrid=[math.log(ptry[i],10) for i in
                       range(0,ny.value)]

            if self.canvas_flag==0:
                self.canvas()

            extent1=xgrid[0]-(xgrid[1]-xgrid[0])/2
            extent2=xgrid[nx.value-1]+(xgrid[nx.value-1]-
                                       xgrid[nx.value-2])/2
            extent3=ygrid[0]-(ygrid[1]-ygrid[0])/2
            extent4=ygrid[ny.value-1]+(ygrid[ny.value-1]-
                                       ygrid[ny.value-2])/2
                        
            if len(args)<2:
                plot.imshow(sl,interpolation='nearest',
                            origin='lower',extent=[extent1,extent2,
                                                   extent3,extent4],
                            aspect='auto')
            else:
                plot.imshow(sl,interpolation='nearest',
                            origin='lower',extent=[extent1,extent2,
                                                   extent3,extent4],
                            aspect='auto',**string_to_dict(args[1]))

        elif curr_type==b'hist_2d':

            get_fn=o2scl_hdf.o2scl_acol_get_hist_2d
            get_fn.argtypes=[ctypes.c_void_p,int_ptr,double_ptr_ptr,
                             int_ptr,double_ptr_ptr,double_ptr_ptr]

            nx=ctypes.c_int(0)
            ptrx=double_ptr()
            ny=ctypes.c_int(0)
            ptry=double_ptr()
            ptrs=double_ptr()
            get_fn(amp,ctypes.byref(nx),ctypes.byref(ptrx),
                   ctypes.byref(ny),ctypes.byref(ptry),
                   ctypes.byref(ptrs))

            xgrid=[ptrx[i] for i in range(0,nx.value)]
            ygrid=[ptry[i] for i in range(0,ny.value)]
            stemp=[ptrs[i] for i in range(0,nx.value*ny.value)]
            stemp2=numpy.array(stemp)
            sl=stemp2.reshape(nx.value,ny.value)
            sl=sl.transpose()

            if self.logx==1:
                xgrid=[math.log(ptrx[i],10) for i in
                       range(0,nx.value)]
            if self.logy==1:
                ygrid=[math.log(ptry[i],10) for i in
                       range(0,ny.value)]

            if self.canvas_flag==0:
                self.canvas()

            extent1=xgrid[0]-(xgrid[1]-xgrid[0])/2
            extent2=xgrid[nx.value-1]+(xgrid[nx.value-1]-
                                       xgrid[nx.value-2])/2
            extent3=ygrid[0]-(ygrid[1]-ygrid[0])/2
            extent4=ygrid[ny.value-1]+(ygrid[ny.value-1]-
                                       ygrid[ny.value-2])/2
                        
            if len(args)<1:
                plot.imshow(sl,interpolation='nearest',
                            origin='lower',extent=[extent1,extent2,
                                                   extent3,extent4],
                            aspect='auto')
            else:
                plot.imshow(sl,interpolation='nearest',
                            origin='lower',extent=[extent1,extent2,
                                                   extent3,extent4],
                            aspect='auto',**string_to_dict(args[0]))
        else:
            print("Command 'den-plot' not supported for type",
                  curr_type,".")
            return

        if self.colbar>0:
            plot.colorbar()

    def plot_intl(self,o2scl_hdf,amp,args):

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
                            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))

            coly=ctypes.c_char_p(self.force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))

            xv=[ptrx[i] for i in range(0,idx.value)]
            yv=[ptry[i] for i in range(0,idy.value)]
    
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                if self.logy==1:
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
                if self.logy==1:
                    if len(args)<3:
                        plot.semilogy(xv,yv)
                    else:
                        plot.semilogy(xv,yv,**string_to_dict(args[2]))
                else:
                    if len(args)<3:
                        plot.plot(xv,yv)
                    else:
                        plot.plot(xv,yv,**string_to_dict(args[2]))

            # End of section for 'table' type
        elif curr_type==b'hist':

            get_reps_fn=o2scl_hdf.o2scl_acol_get_hist_reps
            get_reps_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            get_wgts_fn=o2scl_hdf.o2scl_acol_get_hist_wgts
            get_wgts_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_reps_fn(amp,ctypes.byref(idx),
                        ctypes.byref(ptrx))

            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_wgts_fn(amp,ctypes.byref(idy),
                        ctypes.byref(ptry))

            xv=[ptrx[i] for i in range(0,idx.value)]
            yv=[ptry[i] for i in range(0,idy.value)]
    
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                if self.logy==1:
                    if len(args)<1:
                        plot.loglog(xv,yv)
                    else:
                        plot.loglog(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        plot.semilogx(xv,yv)
                    else:
                        plot.semilogx(xv,yv,**string_to_dict(args[0]))
            else:
                if self.logy==1:
                    if len(args)<1:
                        plot.semilogy(xv,yv)
                    else:
                        plot.semilogy(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        plot.plot(xv,yv)
                    else:
                        plot.plot(xv,yv,**string_to_dict(args[0]))
                            
            # End of section for 'hist' type
        elif curr_type==b'vector<contour_line>':

            # Get the total number of contour lines
            cont_n_fn=o2scl_hdf.o2scl_acol_contours_n
            cont_n_fn.argtypes=[ctypes.c_void_p]
            cont_n_fn.restype=ctypes.c_int
            nconts=cont_n_fn(amp)

            # Define types for extracting each contour line
            cont_line_fn=o2scl_hdf.o2scl_acol_contours_line
            cont_line_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                                   int_ptr,double_ptr_ptr,
                                   double_ptr_ptr]
            cont_line_fn.restype=ctypes.c_double

            if self.canvas_flag==0:
                self.canvas()

            # Loop over all contour lines
            for k in range(0,nconts):
                idx=ctypes.c_int(0)
                ptrx=double_ptr()
                ptry=double_ptr()
                lev=cont_line_fn(amp,k,ctypes.byref(idx),
                                 ctypes.byref(ptrx),ctypes.byref(ptry))
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idx.value)]
                
                if self.logx==1:
                    if self.logy==1:
                        if len(args)<1:
                            plot.loglog(xv,yv)
                        else:
                            plot.loglog(xv,yv,**string_to_dict(args[0]))
                    else:
                        if len(args)<1:
                            plot.semilogx(xv,yv)
                        else:
                            plot.semilogx(xv,yv,**string_to_dict(args[0]))
                else:
                    if self.logy==1:
                        if len(args)<1:
                            plot.semilogy(xv,yv)
                        else:
                            plot.semilogy(xv,yv,**string_to_dict(args[0]))
                    else:
                        if len(args)<1:
                            plot.plot(xv,yv)
                        else:
                            plot.plot(xv,yv,**string_to_dict(args[0]))
            # End of section for 'vector<contour_line>' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==1:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==1:
            plot.ylim([self.ylo,self.yhi])
                                 
        # End of 'plot_intl' function
                                 
    def errorbar_intl(self,o2scl_hdf,amp,args):

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
                            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))

            coly=ctypes.c_char_p(self.force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))

            colxerr=ctypes.c_char_p(self.force_bytes(args[3]))
            idxerr=ctypes.c_int(0)
            ptrxerr=double_ptr()
            get_fn(amp,colxerr,ctypes.byref(idxerr),ctypes.byref(ptrxerr))

            colyerr=ctypes.c_char_p(self.force_bytes(args[2]))
            idyerr=ctypes.c_int(0)
            ptryerr=double_ptr()
            get_fn(amp,colyerr,ctypes.byref(idyerr),ctypes.byref(ptryerr))

            xv=[ptrx[i] for i in range(0,idx.value)]
            yv=[ptry[i] for i in range(0,idy.value)]
            xerrv=[ptrxerr[i] for i in range(0,idxerr.value)]
            yerrv=[ptryerr[i] for i in range(0,idyerr.value)]
    
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                if self.logy==1:
                    if len(args)<5:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr)
                    else:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr,
                                      **string_to_dict(args[2]))
                else:
                    if len(args)<5:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr)
                    else:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr,
                                      **string_to_dict(args[2]))
            else:
                if self.logy==1:
                    if len(args)<5:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr)
                    else:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr,
                                      **string_to_dict(args[2]))
                else:
                    if len(args)<5:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr)
                    else:
                        plot.errorbar(xv,yv,yerr=yerr,xerr=xerr,
                                      **string_to_dict(args[2]))

            # End of section for 'table' type
        elif curr_type==b'hist':

            get_reps_fn=o2scl_hdf.o2scl_acol_get_hist_reps
            get_reps_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            get_wgts_fn=o2scl_hdf.o2scl_acol_get_hist_wgts
            get_wgts_fn.argtypes=[ctypes.c_void_p,
                             int_ptr,double_ptr_ptr]
                            
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_reps_fn(amp,ctypes.byref(idx),
                        ctypes.byref(ptrx))

            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_wgts_fn(amp,ctypes.byref(idy),
                        ctypes.byref(ptry))

            xv=[ptrx[i] for i in range(0,idx.value)]
            yv=[ptry[i] for i in range(0,idy.value)]
    
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                if self.logy==1:
                    if len(args)<1:
                        plot.loglog(xv,yv)
                    else:
                        plot.loglog(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        plot.semilogx(xv,yv)
                    else:
                        plot.semilogx(xv,yv,**string_to_dict(args[0]))
            else:
                if self.logy==1:
                    if len(args)<1:
                        plot.semilogy(xv,yv)
                    else:
                        plot.semilogy(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        plot.plot(xv,yv)
                    else:
                        plot.plot(xv,yv,**string_to_dict(args[0]))
                            
            # End of section for 'hist' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==1:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==1:
            plot.ylim([self.ylo,self.yhi])
                                 
        # End of 'errorbar_intl' function
                                 
    def plot1_intl(self,o2scl_hdf,amp,args):

        int_ptr=ctypes.POINTER(ctypes.c_int)
        double_ptr=ctypes.POINTER(ctypes.c_double)
        char_ptr=ctypes.POINTER(ctypes.c_char)
        double_ptr_ptr=ctypes.POINTER(double_ptr)
        char_ptr_ptr=ctypes.POINTER(char_ptr)
        
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
                        
        if curr_type!=b'table':
            print("Command 'plot1' not supported for type",
                  curr_type,".")
            return
            
        get_fn=o2scl_hdf.o2scl_acol_get_column
        get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                         int_ptr,double_ptr_ptr]

        colx=ctypes.c_char_p(self.force_bytes(args[0]))
        idx=ctypes.c_int(0)
        ptrx=double_ptr()
        get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))

        xv=[i for i in range(0,idx.value)]
        yv=[ptrx[i] for i in range(0,idx.value)]

        if self.canvas_flag==0:
            self.canvas()
        if self.logx==1:
            if self.logy==1:
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
            if self.logy==1:
                if len(args)<2:
                    plot.semilogy(xv,yv)
                else:
                    plot.semilogy(xv,yv,**string_to_dict(args[1]))
            else:
                if len(args)<2:
                    plot.plot(xv,yv)
                else:
                    plot.plot(xv,yv,**string_to_dict(args[1]))
                            
        if self.xset==1:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==1:
            plot.ylim([self.ylo,self.yhi])

        # End of 'plot1_intl' function
            
    def plotm_intl(self,o2scl_hdf,amp,args):

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
            ccp=ctypes.c_char_p(self.force_bytes(str_args))
            sizes=size_type(5,len(self.plotfiles[ifile]))
            parse_fn(amp,2,sizes,ccp)

            # Get the x column
            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_fn(amp,colx,ctypes.byref(idx),
                   ctypes.byref(ptrx))

            # Get the y column
            coly=ctypes.c_char_p(self.force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_fn(amp,coly,ctypes.byref(idy),
                   ctypes.byref(ptry))

            # Copy the data over
            xv=[ptrx[i] for i in range(0,idx.value)]
            yv=[ptry[i] for i in range(0,idy.value)]

            # Plot
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                if self.logy==1:
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
                if self.logy==1:
                    if len(args)<3:
                        plot.semilogy(xv,yv)
                    else:
                        plot.semilogy(xv,yv,**string_to_dict(args[2]))
                else:
                    if len(args)<3:
                        plot.plot(xv,yv)
                    else:
                        plot.plot(xv,yv,**string_to_dict(args[2]))
            if self.xset==1:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==1:
                plot.ylim([self.ylo,self.yhi])

        # End of 'plotm_intl' function
        
    def plot1m_intl(self,o2scl_hdf,amp,args):
        
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
            ccp=ctypes.c_char_p(self.force_bytes(str_args))
            sizes=size_type(5,len(self.plotfiles[ifile]))
            parse_fn(amp,2,sizes,ccp)

            # Get the x column
            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_fn(amp,colx,ctypes.byref(idx),
                   ctypes.byref(ptrx))

            # Copy the data over
            xv=[i for i in range(0,idx.value)]
            yv=[ptrx[i] for i in range(0,idx.value)]

            # Plot
            if self.canvas_flag==0:
                self.canvas()
            if self.logx==1:
                if self.logy==1:
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
                if self.logy==1:
                    if len(args)<2:
                        plot.semilogy(xv,yv)
                    else:
                        plot.semilogy(xv,yv,**string_to_dict(args[1]))
                else:
                    if len(args)<2:
                        plot.plot(xv,yv)
                    else:
                        plot.plot(xv,yv,**string_to_dict(args[1]))
                        
            if self.xset==1:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==1:
                plot.ylim([self.ylo,self.yhi])
                                
        # End of 'plot1m_intl' function
                                 
    def parse_argv(self,argv,o2scl_hdf):

        o2scl_hdf.o2scl_create_acol_manager.restype=ctypes.c_void_p
        amp=o2scl_hdf.o2scl_create_acol_manager()
                        
        if self.verbose>2:
            print('Number of arguments:',len(argv),'arguments.')
            print('Argument List:', str(argv))
        ix=0
        while ix<len(argv):
            if self.verbose>2:
                print('Processing index',ix,'with value',argv[ix],'.')
            # Find first option, at index ix
            initial_ix_done=0
            while initial_ix_done==0:
                if ix==len(argv):
                    initial_ix_done=1
                elif argv[ix][0]=='-':
                    initial_ix_done=1
                else:
                    if self.verbose>2:
                         print('Incrementing ix')
                    ix=ix+1
            # If there is an option, then ix is its index
            if ix<len(argv):
                cmd_name=argv[ix][1:]
                # If there was two dashes, one will be left so
                # remove it
                if cmd_name[0]=='-':
                    cmd_name=cmd_name[1:]
                if self.verbose>2:
                    print('Found option',cmd_name,'at index',ix)
                # Set ix_next to the next option, or to the end if
                # there is no next option
                ix_next=ix+1
                ix_next_done=0
                while ix_next_done==0:
                    if ix_next==len(argv):
                        ix_next_done=1
                    elif argv[ix_next][0]=='-':
                        ix_next_done=1
                    else:
                        if self.verbose>2:
                            print('Incrementing ix_next')
                        ix_next=ix_next+1
                        
                # Now process the option
                if cmd_name=='set':

                    if self.verbose>2:
                        print('Process set.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for set option.')
                    else:
                        self.set_intl(o2scl_hdf,amp,argv[ix+1:ix_next])
                        
                elif cmd_name=='get':
                    
                    if self.verbose>2:
                        print('Process get.')
                        
                    if ix_next-ix<2:
                        self.get('No parameter specified to get.')
                    else:
                        self.get_intl(o2scl_hdf,amp,argv[ix+1:ix_next])

                elif cmd_name=='version':
                    
                    print('o2graph: A data table plotting and',
                          'processing program for O2scl.')
                    print(' Version '+version+'.')

                elif (cmd_name=='read' or cmd_name=='list' or
                      cmd_name=='assign' or cmd_name=='integ' or
                      cmd_name=='cat' or cmd_name=='internal' or
                      cmd_name=='commands' or cmd_name=='interp' or
                      cmd_name=='convert-unit' or cmd_name=='interp-type' or
                      cmd_name=='create' or cmd_name=='license' or
                      cmd_name=='delete-col' or cmd_name=='max' or
                      cmd_name=='delete-rows' or cmd_name=='min' or
                      cmd_name=='deriv' or cmd_name=='output' or
                      cmd_name=='deriv2' or cmd_name=='preview' or
                      cmd_name=='filelist' or cmd_name=='rename' or
                      cmd_name=='find-row' or cmd_name=='select' or
                      cmd_name=='fit' or cmd_name=='select-rows' or
                      cmd_name=='function' or cmd_name=='set-data' or
                      cmd_name=='gen3-list' or cmd_name=='set-unit' or
                      cmd_name=='generic' or cmd_name=='show_units' or
                      cmd_name=='get-conv' or cmd_name=='slice' or
                      cmd_name=='get-row' or cmd_name=='sort' or
                      cmd_name=='get-unit' or cmd_name=='status' or
                      cmd_name=='index' or cmd_name=='sum' or
                      cmd_name=='insert' or cmd_name=='contours' or
                      cmd_name=='insert-full' or cmd_name=='warranty' or
                      cmd_name=='calc' or cmd_name=='help' or
                      cmd_name=='nlines' or cmd_name=='to-hist' or
                      cmd_name=='type' or cmd_name=='entry'):
                    
                    if self.verbose>2:
                        print('Process '+cmd_name+'.')

                    self.gen_intl(o2scl_hdf,amp,cmd_name,
                                  argv[ix+1:ix_next])

                elif cmd_name=='plot':
                    
                    if self.verbose>2:
                        print('Process plot.')

                    self.plot_intl(o2scl_hdf,amp,
                                   argv[ix+1:ix_next])

                elif cmd_name=='errorbar':
                    
                    if self.verbose>2:
                        print('Process errorbar.')

                    self.errorbar_intl(o2scl_hdf,amp,
                                   argv[ix+1:ix_next])

                elif cmd_name=='hist2d':
                    
                    if self.verbose>2:
                        print('Process hist2d.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for hist2d option.')
                    else:
                        get_fn=o2scl_hdf.o2scl_acol_get_column
                        get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                                         int_ptr,double_ptr_ptr]

                        colx=ctypes.c_char_p(self.force_bytes(argv[ix+1]))
                        idx=ctypes.c_int(0)
                        ptrx=double_ptr()
                        get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))

                        coly=ctypes.c_char_p(self.force_bytes(argv[ix+2]))
                        idy=ctypes.c_int(0)
                        ptry=double_ptr()
                        get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))

                        xv=[ptrx[i] for i in range(0,idx.value)]
                        yv=[ptry[i] for i in range(0,idy.value)]

                        #(lmar=0.14,bmar=0.12,rmar=0.04,tmar=0.04):
                        
                        if self.canvas_flag==0:
                            if self.colbar>0:
                                # Default o2mpl plot
                                (self.fig,self.axes)=default_plot(0.14,0.12,
                                                                  0.0,0.04)
                                # Plot limits
                                if self.xset==1:
                                    plot.xlim([self.xlo,self.xhi])
                                if self.yset==1:
                                    plot.ylim([self.ylo,self.yhi])
                                # Titles
                                if self.xtitle!='':
                                    plot.xlabel(self.xtitle,fontsize=16)
                                if self.ytitle!='':
                                    plot.ylabel(self.ytitle,fontsize=16)
                                self.canvas_flag=1
                            else:
                                self.canvas()
                            
                        if ix_next-ix<4:
                            plot.hist2d(xv,yv)
                        else:
                            kwargs=string_to_dict(argv[ix+3])
                            for key in kwargs:
                                if key=='bins':
                                    kwargs[key]=int(kwargs[key])
                            plot.hist2d(xv,yv,**kwargs)
                            
                        if self.colbar>0:
                            plot.colorbar()
                            
                elif cmd_name=='den-plot':
                    
                    if self.verbose>2:
                        print('Process den-plot.')

                    self.den_plot_intl(o2scl_hdf,amp,
                                       argv[ix+1:ix_next])
                
                elif cmd_name=='plot1':
                    
                    if self.verbose>2:
                        print('Process plot1.')
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for plot1 option.')
                    else:
                        self.plot1_intl(o2scl_hdf,amp,
                                       argv[ix+1:ix_next])
                            
                elif cmd_name=='plotm':
                    
                    if self.verbose>2:
                        print('Process plotm.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for plotm option.')
                    else:
                        self.plotm_intl(o2scl_hdf,amp,
                                       argv[ix+1:ix_next])
                                                    
                elif cmd_name=='plot1m':
                    
                    if self.verbose>2:
                        print('Process plot1m.')
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for plot1m option.')
                    else:
                        self.plot1m_intl(o2scl_hdf,amp,
                                       argv[ix+1:ix_next])
                        
                elif cmd_name=='text':
                    if self.verbose>2:
                        print('Process text.')
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for text option.')
                    elif ix_next-ix<5:
                        self.text(argv[ix+1],argv[ix+2],argv[ix+3])
                    else:
                        self.text(argv[ix+1],argv[ix+2],argv[ix+3],
                                  **string_to_dict(argv[ix+4]))
                elif cmd_name=='plot-files':
                    if self.verbose>2:
                        print('Process plot-files.')
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for plot-files option.')
                    else:
                        self.plotfiles=[argv[i+1] for i in
                                       range(ix,ix_next-1)]
                        print('File list is',self.plotfiles)
                elif cmd_name=='ttext':
                    if self.verbose>2:
                        print('Process ttext.')
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for ttext option.')
                    elif ix_next-ix<5:
                        self.ttext(argv[ix+1],argv[ix+2],argv[ix+3])
                    else:
                        self.ttext(argv[ix+1],argv[ix+2],argv[ix+3],
                                   **string_to_dict(argv[ix+4]))
                elif cmd_name=='xlimits':
                    if self.verbose>2:
                        print('Process xlimits.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for xlimits option.')
                    else:
                        self.xlimits(float(argv[ix+1]),float(argv[ix+2]))
                elif cmd_name=='ylimits':
                    if self.verbose>2:
                        print('Process ylimits.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for ylimits option.')
                    else:
                        self.ylimits(float(argv[ix+1]),float(argv[ix+2]))
                elif cmd_name=='save':
                    if self.verbose>2:
                        print('Process save.')
                    if ix_next-ix<2:
                        print('Not enough parameters for save option.')
                    else:
                        plot.savefig(argv[ix+1])
                elif cmd_name=='line':
                    if self.verbose>2:
                        print('Process line.')
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for line option.')
                    elif ix_next-ix<6:
                        self.line(argv[ix+1],argv[ix+2],argv[ix+3],argv[ix+4])
                    else:
                        self.line(argv[ix+1],argv[ix+2],argv[ix+3],argv[ix+4],
                                  **string_to_dict(argv[ix+5]))
                elif cmd_name=='move-labels':
                    if self.verbose>2:
                        print('Process move-labels.')
                    self.move_labels()
                elif cmd_name=='show':
                    if self.verbose>2:
                        print('Process show.')
                    self.show()
                elif cmd_name=='canvas':
                    if self.verbose>2:
                        print('Process canvas.')
                    self.canvas()
                elif cmd_name=='reds2':
                    if self.verbose>2:
                        print('Process reds2.')
                    self.reds2()
                elif cmd_name=='blues2':
                    if self.verbose>2:
                        print('Process blues2.')
                    self.blues2()
                elif cmd_name=='greens2':
                    if self.verbose>2:
                        print('Process greens2.')
                    self.greens2()
                elif cmd_name=='jet2':
                    if self.verbose>2:
                        print('Process jet2.')
                    self.jet2()
                elif cmd_name=='pastel2':
                    if self.verbose>2:
                        print('Process pastel2.')
                    self.pastel2()
                else:
                    print('No option named',cmd_name)
                # Increment to the next option
                ix=ix_next
            if self.verbose>2:
                print('Going to next.')
        return

"""
   -------------------------------------------------------------------
   
   Copyright (C) 2006-2017, Andrew W. Steiner
   
   This file is part of O2scl.
   
   O2scl is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
   
   O2scl is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with O2scl. If not, see <http://www.gnu.org/licenses/>.
   
   -------------------------------------------------------------------
"""
    
