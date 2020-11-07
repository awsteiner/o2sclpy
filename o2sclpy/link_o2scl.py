#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2020, Andrew W. Steiner
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
import ctypes
import os

# For system type detection in build_o2scl() and link_o2scl()
import platform

# For build_o2scl(), link_o2scl()
import urllib.request

# For force_bytes() in link_o2scl()
from o2sclpy.utils import force_bytes, if_yt_then_Agg

# For find_library() in link_o2scl()
from ctypes.util import find_library

class linker:

    # O2scl library directory from command-line or environment variables
    o2scl_lib_dir=''
    
    # C++ library from command-line or environment variables
    o2scl_cpp_lib=''
    
    # Backend specification from command-line
    backend=''
    
    # Additional library list from command-line or environment variables
    o2scl_addl_libs=[]
    
    # List of additional library objects
    o2scl_addl=[]
    
    # If true, -debug-first-pass was specified on command-line
    debug_first_pass=False
    
    # Main o2scl library handle
    o2scl=0
    
    # O2scl HDF library handle
    o2scl_hdf=0
    
    # O2scl particle library handle
    o2scl_part=0

    # Additional library handles
    o2scl_addl=[]

    # System C++ library handle
    systcpp=0
    
    def link_o2scl_o2graph(self,include_part=False):
        """
        A new function for linking o2scl which came originally from
        the o2graph script
        """
    
        # Future: it appears we may need to fix the string comparisons in the
        # code below and force conversion to byte strings (even though for now
        # this code seems to work)
              
        if platform.system()=='Darwin':
        
            if (self.o2scl_cpp_lib=='' and
                os.getenv('O2SCL_CPP_LIB') is not None and
                force_bytes(os.getenv('O2SCL_CPP_LIB'))!=b'None'):
                self.o2scl_cpp_lib=os.getenv('O2SCL_CPP_LIB')
                if self.debug_first_pass:
                    print('Set o2scl_cpp_lib from environment',
                          'variable to\n  ',o2scl_cpp_lib)
        
            if self.o2scl_cpp_lib!='':
                if self.debug_first_pass:
                    print('Loading C++ library',o2scl_cpp_lib,',')
                self.systcpp=ctypes.CDLL(self.o2scl_cpp_lib,
                                         mode=ctypes.RTLD_GLOBAL)
                if self.debug_first_pass:
                    print('Finished loading C++ library.')
        
            if (len(self.o2scl_addl_libs)==0 and
                os.getenv('O2SCL_ADDL_LIBS') is not None
                and force_bytes(os.getenv('O2SCL_ADDL_LIBS'))!=b'None'):
                self.o2scl_addl_libs=os.getenv('O2SCL_ADDL_LIBS').split(',')
                if self.debug_first_pass:
                    print('Set o2scl_addl_libs from environment',
                          'variable to\n  ',
                          self.o2scl_addl_libs)

            if len(self.o2scl_addl_libs)>0:
                for i in range(0,len(self.o2scl_addl_libs)):
                    if self.debug_first_pass:
                        print('Loading additional library',
                              self.o2scl_addl_libs[i],'.')
                    self.o2scl_addl.append(ctypes.CDLL(self.o2scl_addl_libs[i],
                                                  mode=ctypes.RTLD_GLOBAL))
                if self.debug_first_pass:
                    print('Finished loading additional libraries.')
        
            # Note that we use O2SCL_LIB instead of O2SCL_LIB_DIR as
            # the former is a more common notation for library directories
            if (self.o2scl_lib_dir=='' and os.getenv('O2SCL_LIB')
                is not None and
                force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
                o2scl_lib_dir=os.getenv('O2SCL_LIB')
                if self.debug_first_pass:
                    print('Set o2scl_lib_dir from environment',
                          'variable to\n  ',
                          self.o2scl_lib_dir)
            
            if self.o2scl_lib_dir!='':
                if self.debug_first_pass:
                    print('Loading',self.o2scl_lib_dir+
                          '/libo2scl.dylib','.')
                self.o2scl=ctypes.CDLL(self.o2scl_lib_dir+
                                       '/libo2scl.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
                if self.debug_first_pass:
                    print('Loading',self.o2scl_lib_dir+
                          '/libo2scl_hdf.dylib','.')
                self.o2scl_hdf=ctypes.CDLL(self.o2scl_lib_dir+
                                           '/libo2scl_hdf.dylib',
                                      mode=ctypes.RTLD_GLOBAL)
                if include_part:
                    if self.debug_first_pass:
                        print('Loading',self.o2scl_lib_dir+
                              '/libo2scl_part.dylib','.')
                    self.o2scl_part=ctypes.CDLL(self.o2scl_lib_dir+
                                           '/libo2scl_part.dylib',
                                           mode=ctypes.RTLD_GLOBAL)
            else:
                if self.debug_first_pass:
                    print('Loading libo2scl.dylib.')
                self.o2scl=ctypes.CDLL('libo2scl.dylib',
                                       mode=ctypes.RTLD_GLOBAL)
                if self.debug_first_pass:
                    print('Loading libo2scl_hdf.dylib.')
                self.o2scl_hdf=ctypes.CDLL('libo2scl_hdf.dylib',
                                      mode=ctypes.RTLD_GLOBAL)
                if include_part:
                    if self.debug_first_pass:
                        print('Loading libo2scl_part.dylib.')
                    self.o2scl_part=ctypes.CDLL('libo2scl_part.dylib',
                                          mode=ctypes.RTLD_GLOBAL)
                
            if self.debug_first_pass:
                print('Done loading o2scl libraries.')
        
        else:
        
            if self.debug_first_pass:
                print('Loading C++ library.')
            stdcpp=ctypes.CDLL(find_library("stdc++"),
                               mode=ctypes.RTLD_GLOBAL)
            if self.debug_first_pass:
                print('Finished loading C++ library.')
          
            if (len(self.o2scl_addl_libs)==0 and
                os.getenv('O2SCL_ADDL_LIBS') is not None
                and force_bytes(os.getenv('O2SCL_ADDL_LIBS'))!=b'None'):
                self.o2scl_addl_libs=os.getenv('O2SCL_ADDL_LIBS').split(',')
                if self.debug_first_pass:
                    print('Set o2scl_addl_libs from environment',
                          'variable to\n  ',
                          self.o2scl_addl_libs)
        
            if len(self.o2scl_addl_libs)>0:
                for i in range(0,len(self.o2scl_addl_libs)):
                    if self.debug_first_pass:
                        print('Loading additional library',
                              self.o2scl_addl_libs[i],'.')
                    self.o2scl_addl.append(ctypes.CDLL(self.o2scl_addl_libs[i],
                                                  mode=ctypes.RTLD_GLOBAL))
                if self.debug_first_pass:
                    print('Finished loading additional libraries.')
            
            # Note that we use O2SCL_LIB instead of O2SCL_LIB_DIR as
            # the former is a more common notation for library directories
            if (self.o2scl_lib_dir=='' and os.getenv('O2SCL_LIB')
                is not None and
                force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
                self.o2scl_lib_dir=os.getenv('O2SCL_LIB')
                if self.debug_first_pass:
                    print('Set o2scl_lib_dir from environment',
                          'variable to\n  ',
                          self.o2scl_lib_dir)
            
            if self.o2scl_lib_dir=='':
                if self.debug_first_pass:
                    print('Loading o2scl.')
                self.o2scl=ctypes.CDLL(find_library("o2scl"),
                                  mode=ctypes.RTLD_GLOBAL)
                if self.debug_first_pass:
                    print('Loading o2scl_hdf.')
                self.o2scl_hdf=ctypes.CDLL(find_library("o2scl_hdf"),
                                      mode=ctypes.RTLD_GLOBAL)
                if include_part:
                    if self.debug_first_pass:
                        print('Loading o2scl_hdf.')
                    self.o2scl_hdf=ctypes.CDLL(find_library("o2scl_hdf"),
                                          mode=ctypes.RTLD_GLOBAL)
            else:
                if self.debug_first_pass:
                    print('Loading',self.o2scl_lib_dir+'/libo2scl.so .')
                self.o2scl=ctypes.CDLL(self.o2scl_lib_dir+'/libo2scl.so',
                                  mode=ctypes.RTLD_GLOBAL)
                if self.debug_first_pass:
                    print('Loading',self.o2scl_lib_dir+'/libo2scl_hdf.so .')
                self.o2scl_hdf=ctypes.CDLL(self.o2scl_lib_dir+
                                           '/libo2scl_hdf.so',
                                      mode=ctypes.RTLD_GLOBAL)
                if include_part:
                    if self.debug_first_pass:
                        print('Loading',self.o2scl_lib_dir+
                              '/libo2scl_hdf.so .')
                    self.o2scl_hdf=ctypes.CDLL(self.o2scl_lib_dir+
                                               '/libo2scl_hdf.so',
                                          mode=ctypes.RTLD_GLOBAL)
        
            if self.debug_first_pass:
                print('Done loading o2scl libraries.')
    
        return
    
    def get_library_settings(self,argv=[]):
        """
        Get the library settings from the command-line arguments
        """
    
        # Go through the argument list and determine settings for
        # o2scl-lib-dir, o2scl-cpp-lib, o2scl-addl-libs and determine if
        # -debug-libs was present
        
        for i in range(1,len(argv)):
            if argv[i]=='-o2scl-lib-dir':
                if i>=len(argv)-1:
                    print('Option -o2scl-lib-dir specified with no value.')
                else:
                    self.o2scl_lib_dir=argv[i+1]
                    if self.debug_first_pass:
                        print('Set o2scl_lib_dir from command-line to',
                              self.o2scl_lib_dir)
            elif argv[i]=='-o2scl-cpp-lib':
                if i>=len(argv)-1:
                    print('Option -o2scl-cpp-lib specified with no value.')
                else:
                    self.o2scl_cpp_lib=argv[i+1]
                    if self.debug_first_pass:
                        print('Set o2scl_cpp_lib from command-line to',
                              self.o2scl_cpp_lib)
            elif argv[i]=='-o2scl-addl-libs':
                if i>=len(argv)-1:
                    print('Option -o2scl-addl-libs specified with no value.')
                else:
                    self.o2scl_addl_libs=argv[i+1].split(',')
                    if self.debug_first_pass:
                        print('Set o2scl_addl_libs from command-line to',
                              self.o2scl_addl_libs)
            elif argv[i]=='-backend':
                if i>=len(argv)-1:
                    print('Option -backend specified with no value.')
                else:
                    self.backend=argv[i+1]
            elif argv[i]=='-debug-first-pass':
                self.debug_first_pass=True
                
        self.backend=if_yt_then_Agg(self.backend,argv)
        
        return self.backend

def build_o2scl(verbose=1,release=True):
    """
    This function attempts to automatically build O\ :sub:`2`\ scl using 
    homebrew on OSX and snap on Linux.

    This function is in ``link_o2scl.py``.
    """
    
    print('Would you like to try to automatically install O2scl '+
          '(requires sudo)?')
    ans=input("(y/n):")
    if ans!='y':
        print('Not building o2scl.')
        return 2
    
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

def link_o2scl_f(verbose=1):
    """
    This function attempts to automatically load O\ :sub:`2`\ scl as a 
    DLL and returns the ``o2scl`` and ``o2scl_hdf`` DLL pointers.

    This function is in ``link_o2scl.py``.
    """

    global o2scl_lib_dir, o2scl_cpp_lib, o2scl, o2scl_hdf
    
    # Handle OSX and Linux separately
    if platform.system()=='Darwin':

        if verbose>=2:
            print('Using OSX library rules.')

        if (o2scl_cpp_lib=='' and os.getenv('O2SCL_CPP_LIB') is not None
            and force_bytes(os.getenv('O2SCL_CPP_LIB'))!=b'None'):
            o2scl_cpp_lib=os.getenv('O2SCL_CPP_LIB')
            if verbose>0:
                print('Value of o2scl_cpp_lib is',o2scl_cpp_lib,'.')
        elif verbose>=2:
            print('Value of o2scl_cpp_lib is',o2scl_cpp_lib,'.')
      
        if o2scl_cpp_lib!='' and o2scl_cpp_lib!='skip':
            if verbose>0:
                print('Loading',o2scl_cpp_lib)
            systcpp=ctypes.CDLL(o2scl_cpp_lib,mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded system C++ library.')
            elif o2scl_cpp_lib=='skip' and verbose>0:
                print('Skipping load of C++ library.')
      
        rl=ctypes.CDLL('/usr/lib/libreadline.dylib',
                       mode=ctypes.RTLD_GLOBAL)
        if verbose>0:
            print('Loaded readline.')
          
        if (o2scl_lib_dir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_lib_dir=os.getenv('O2SCL_LIB')
            if verbose>0:
                print('Value of o2scl_lib_dir is ',o2scl_lib_dir,'.')
        elif verbose>=2:
                print('Value of o2scl_lib_dir is ',o2scl_lib_dir,'.')
          
        if o2scl_lib_dir!='':
            print('o2scl:',o2scl)
            try:
                if verbose>0:
                    print('Loading',o2scl_lib_dir+'/libo2scl.dylib')
                o2scl=ctypes.CDLL(o2scl_lib_dir+'/libo2scl.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
            except Exception as e:
                print('O2scl not found:',e)
                ret=build_o2scl()
                if ret==0:
                    o2scl=ctypes.CDLL(o2scl_lib_dir+'/libo2scl.dylib',
                                      mode=ctypes.RTLD_GLOBAL)
                else:
                    return 3
                
            if verbose>0:
                print('Loaded o2scl (1).')
            if verbose>0:
                print('Loading',o2scl_lib_dir+'/libo2scl_hdf.dylib')
            o2scl_hdf=ctypes.CDLL(o2scl_lib_dir+'/libo2scl_hdf.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf (1).')
        else:
            o2scl=ctypes.CDLL('libo2scl.dylib',mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl (2).')
            o2scl_hdf=ctypes.CDLL('libo2scl_hdf.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf (2).')
    
    else:
    
        stdcpp=ctypes.CDLL(find_library("stdc++"),mode=ctypes.RTLD_GLOBAL)
        if verbose>0:
            print('Loaded system C++ library.')
        
        if (o2scl_lib_dir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_lib_dir=os.getenv('O2SCL_LIB')
            print('Set o2scl-libdir to',o2scl_lib_dir)
          
        if o2scl_lib_dir=='':
            o2scl=ctypes.CDLL(find_library("o2scl"),mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl (3).')
            o2scl_hdf=ctypes.CDLL(find_library("o2scl_hdf"),
                                mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf (3).')
        else:
            o2scl=ctypes.CDLL(o2scl_lib_dir+'/libo2scl.so',
                              mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl (4).')
            o2scl_hdf=ctypes.CDLL(o2scl_lib_dir+'/libo2scl_hdf.so',
                                  mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf (4).')

    return
    
def link_o2scl_part(verbose=1):
    """
    """

    global o2scl_lib_dir, o2scl_cpp_lib, o2scl_part
    
    # Handle OSX and Linux separately
    if platform.system()=='Darwin':
    
        if verbose>=2:
            print('Using OSX library rules.')
          
        if (o2scl_lib_dir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_lib_dir=os.getenv('O2SCL_LIB')
            if verbose>0:
                print('Value of o2scl_lib_dir is ',o2scl_lib_dir,'.')
        elif verbose>=2:
                print('Value of o2scl_lib_dir is ',o2scl_lib_dir,'.')
          
        if o2scl_lib_dir!='':
            try:
                o2scl_part=ctypes.CDLL(o2scl_lib_dir+'/libo2scl_part.dylib',
                                       mode=ctypes.RTLD_GLOBAL)
            except:
                print('O2scl_part not found.')
            if verbose>0:
                print('Loaded o2scl_part (1).')
        else:
            o2scl_part=ctypes.CDLL('libo2scl_part.dylib',
                                   mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_part (2).')
    
    else:
    
        if (o2scl_lib_dir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_lib_dir=os.getenv('O2SCL_LIB')
            print('Set o2scl-libdir to',o2scl_lib_dir)
          
        if o2scl_lib_dir=='':
            o2scl_part=ctypes.CDLL(find_library("o2scl_part"),
                                   mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_part (3).')
        else:
            o2scl_part=ctypes.CDLL(o2scl_lib_dir+'/libo2scl_part.so',
                              mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_part (4).')
    return
    
