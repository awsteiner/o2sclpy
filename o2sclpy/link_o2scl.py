# For system type detection in build_o2scl() and link_o2scl()
import platform

# For build_o2scl(), link_o2scl() and download_file()
import urllib.request

def build_o2scl(verbose=1,release=True):
    """
    This function attempts to automatically build O2scl using 
    homebrew on OSX and snap on Linux.
    """
    
    print('Would you like to try to automatically install O2scl '+
          '(requires sudo)?')
    
    if platform.system()=='Darwin':
        ret=os.system('brew doctor')
        if ret!=0:
            if verbose>0:
                print('Homebrew failed ('+ret+').')
            print('Enter directory')
            dir=''
            if release==True:
                urllib.request.urlretrieve('https://github.com/awsteiner/'+
                                           'o2scl/releases/download/v'+
                                           version+'/'+
                                           'o2scl-'+version+'.tar.gz',
                                           dir+'/o2scl-'+version+'.tar.gz')
            else:
                ret3=os.system('git clone https://github.com/awsteiner/'+
                               'o2scl.git')
            os.system('cd '+dir+'; tar xvzf o2scl-'+version+'.tar.gz; '+
                      './configure; make; make install')
        else:
            ret2=os.system('brew install o2scl --HEAD')
            if ret2==0:
                return 0
            else:
                if verbose>0:
                    print('Homebrew install failed ('+ret2+').')
                return 1
    else:
        ret=os.system('snap -v')
        if ret!=0:
            print('Enter directory')
            dir=''
            if release==True:
                urllib.request.urlretrieve('https://github.com/awsteiner/'+
                                           'o2scl/releases/download/v'+
                                           version+'/'+
                                           'o2scl-'+version+'.tar.gz',
                                           dir+'/o2scl-'+version+'.tar.gz')
            else:
                ret3=os.system('git clone https://github.com/awsteiner/'+
                               'o2scl.git')
            os.system('cd '+dir+'; tar xvzf o2scl-'+version+'.tar.gz; '+
                      './configure; make; sudo make install')
        else:
            ret2=os.system('snap install o2scl --devmode --edge')
                
def link_o2scl(verbose=1,o2scl_cpplib='',o2scl_libdir=''):
    """
    This function attempts to automatically load O2scl as a 
    DLL and returns the O2scl and O2scl_hdf DLL pointers.
    """

    # Handle OSX and Linux separately
    if platform.system()=='Darwin':
    
        if verbose>=2:
            print('Using OSX library rules.')
        
        if (o2scl_cpplib=='' and os.getenv('O2SCL_CPPLIB') is not None
            and force_bytes(os.getenv('O2SCL_CPPLIB'))!=b'None'):
            o2scl_cpplib=os.getenv('O2SCL_CPPLIB')
            if verbose>0:
                print('Value of o2scl_cpplib is ',o2scl_cpplib,'.')
        elif verbose>=2:
            print('Value of o2scl_cpplib is ',o2scl_cpplib,'.')
      
        if o2scl_cpplib!='':
            systcpp=ctypes.CDLL(o2scl_cpplib,mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded system C++ library.')
      
        rl=ctypes.CDLL('/usr/lib/libreadline.dylib',
                       mode=ctypes.RTLD_GLOBAL)
        if verbose>0:
            print('Loaded readline.')
          
        if (o2scl_libdir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_libdir=os.getenv('O2SCL_LIB')
            if verbose>0:
                print('Value of o2scl_libdir is ',o2scl_libdir,'.')
        elif verbose>=2:
                print('Value of o2scl_libdir is ',o2scl_libdir,'.')
          
        if o2scl_libdir!='':
            try:
                o2scl=ctypes.CDLL(o2scl_libdir+'/libo2scl.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
            except:
                print('O2scl not found.')
                ret=build_o2scl()
                if ret==0:
                    o2scl=ctypes.CDLL(o2scl_libdir+'/libo2scl.dylib',
                                      mode=ctypes.RTLD_GLOBAL)
                else:
                    return 3
                
            if verbose>0:
                print('Loaded o2scl.')
            o2scl_hdf=ctypes.CDLL(o2scl_libdir+'/libo2scl_hdf.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf.')
        else:
            o2scl=ctypes.CDLL('libo2scl.dylib',mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl.')
            o2scl_hdf=ctypes.CDLL('libo2scl_hdf.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf.')
    
    else:
    
        stdcpp=ctypes.CDLL(find_library("stdc++"),mode=ctypes.RTLD_GLOBAL)
        if verbose>0:
            print('Loaded system C++ library.')
        
        if (o2scl_libdir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_libdir=os.getenv('O2SCL_LIB')
            print('Set o2scl-libdir to',o2scl_libdir)
          
        if o2scl_libdir=='':
            o2scl=ctypes.CDLL(find_library("o2scl"),mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl.')
            o2scl_hdf=ctypes.CDLL(find_library("o2scl_hdf"),
                                mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf.')
        else:
            o2scl=ctypes.CDLL(o2scl_libdir+'/libo2scl.so',
                              mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl.')
            o2scl_hdf=ctypes.CDLL(o2scl_libdir+'/libo2scl_hdf.so',
                                  mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf.')

    return (o2scl,o2scl_hdf)
    
