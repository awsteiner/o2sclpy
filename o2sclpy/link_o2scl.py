#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2006-2025, Andrew W. Steiner
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

import ctypes
import os

# For system type detection in build_o2scl() and link_o2scl()
import platform

# For build_o2scl()
import urllib.request

# For force_bytes() in link_o2scl()
from o2sclpy.utils import force_bytes, if_yt_then_Agg

# For find_library() in link_o2scl()
from ctypes.util import find_library

class linker:
    """
    The class which controls the dynamic linking of the O2scl libraries
    and also the setting of the matplotlib backend for o2graph. If
    O2scl is successfully linked, this class also provides access
    to the global O2scl library settings object.
    """

    o2scl_lib_dir=''
    """
    O2scl library directory from command-line or environment variables
    """
    
    o2scl_cpp_lib=''
    """
    C++ library from command-line or environment variables
    """

    backend=''
    """
    Backend specification from command-line
    """

    o2scl_addl_libs = []
    """
    Additional library list from command-line or environment variables
    """

    o2scl_addl = []
    """
    List of additional library objects
    """

    verbose=0
    """
    If greater than 0, output more information about the linker.
    The command-line option -debug-link sets this parameter to 1.
    """

    o2scl=0
    """
    Main o2scl library handle
    """

    o2scl_addl=[]
    """
    Additional library handles
    """

    systcpp=0
    """
    System C++ library handle
    """

    o2scl_settings=0
    """
    The o2scl_settings object
    """

    def link_o2scl(self):
        """
        A function for linking the o2scl libraries.
        """

        # Future: it appears we may need to fix the string comparisons in the
        # code below and force conversion to byte strings (even though for now
        # this code seems to work)
              
        if platform.system()=='Darwin':
        
            if (self.o2scl_cpp_lib=='' and
                os.getenv('O2SCL_CPP_LIB') is not None and
                force_bytes(os.getenv('O2SCL_CPP_LIB'))!=b'None'):
                self.o2scl_cpp_lib=os.getenv('O2SCL_CPP_LIB')
                if self.verbose>0:
                    print("Set o2scl_cpp_lib from environment",
                          "variable O2SCL_CPP_LIB to\n  '"+
                          self.o2scl_cpp_lib+"'.")
        
            if self.o2scl_cpp_lib!='':
                if self.verbose>0:
                    print("Loading C++ library '"+self.o2scl_cpp_lib+"'.")
                self.systcpp=ctypes.CDLL(self.o2scl_cpp_lib,
                                         mode=ctypes.RTLD_GLOBAL)
                if self.verbose>0:
                    print('Finished loading C++ library.')
        
            if (len(self.o2scl_addl_libs)==0 and
                os.getenv('O2SCL_ADDL_LIBS') is not None
                and force_bytes(os.getenv('O2SCL_ADDL_LIBS'))!=b'None'):
                self.o2scl_addl_libs=os.getenv('O2SCL_ADDL_LIBS').split(',')
                if self.verbose>0:
                    print('Set o2scl_addl_libs from environment',
                          'variable O2SCL_ADDL_LIBS to:\n  ',
                          self.o2scl_addl_libs)

            if len(self.o2scl_addl_libs)>0:
                for i in range(0,len(self.o2scl_addl_libs)):
                    if self.verbose>0:
                        print("Loading additional library '"+
                              self.o2scl_addl_libs[i]+"'.")
                    self.o2scl_addl.append(ctypes.CDLL(self.o2scl_addl_libs[i],
                                                  mode=ctypes.RTLD_GLOBAL))
                if self.verbose>0:
                    print('Finished loading additional libraries.')
        
            # Note that we use O2SCL_LIB instead of O2SCL_LIB_DIR as
            # the former is a more common notation for library directories
            if (self.o2scl_lib_dir=='' and os.getenv('O2SCL_LIB')
                is not None and
                force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
                self.o2scl_lib_dir=os.getenv('O2SCL_LIB')
                if self.verbose>0:
                    print('Set o2scl_lib_dir from environment',
                          "variable O2SCL_LIB to\n  '"+
                          self.o2scl_lib_dir+"'.")
            
            if self.o2scl_lib_dir!='':
                if self.verbose>0:
                    print('Loading',self.o2scl_lib_dir+
                          '/libo2scl.dylib.')
                self.o2scl=ctypes.CDLL(self.o2scl_lib_dir+
                                       '/libo2scl.dylib',
                                  mode=ctypes.RTLD_GLOBAL)
            else:
                if self.verbose>0:
                    print('Loading libo2scl.dylib.')
                self.o2scl=ctypes.CDLL('libo2scl.dylib',
                                       mode=ctypes.RTLD_GLOBAL)
                
            if self.verbose>0:
                print('Done loading o2scl libraries.')
        
        else:
        
            if self.verbose>0:
                print('Loading C++ library.')
            stdcpp=ctypes.CDLL(find_library("stdc++"),
                               mode=ctypes.RTLD_GLOBAL)
            if self.verbose>0:
                print('Finished loading C++ library.')
          
            if (len(self.o2scl_addl_libs)==0 and
                os.getenv('O2SCL_ADDL_LIBS') is not None
                and force_bytes(os.getenv('O2SCL_ADDL_LIBS'))!=b'None'):
                self.o2scl_addl_libs=os.getenv('O2SCL_ADDL_LIBS').split(',')
                if self.verbose>0:
                    print('Set o2scl_addl_libs from environment',
                          'variable to\n  ',
                          self.o2scl_addl_libs)
        
            if len(self.o2scl_addl_libs)>0:
                for i in range(0,len(self.o2scl_addl_libs)):
                    if self.verbose>0:
                        print('Loading additional library',
                              self.o2scl_addl_libs[i],'.')
                    self.o2scl_addl.append(ctypes.CDLL(self.o2scl_addl_libs[i],
                                                  mode=ctypes.RTLD_GLOBAL))
                if self.verbose>0:
                    print('Finished loading additional libraries.')
            
            # Note that we use O2SCL_LIB instead of O2SCL_LIB_DIR as
            # the former is a more common notation for library directories
            if (self.o2scl_lib_dir=='' and os.getenv('O2SCL_LIB')
                is not None and
                force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
                self.o2scl_lib_dir=os.getenv('O2SCL_LIB')
                if self.verbose>0:
                    print('Set o2scl_lib_dir from environment',
                          'variable to\n  ',
                          self.o2scl_lib_dir)
            
            if self.o2scl_lib_dir=='':
                if self.verbose>0:
                    print('Loading o2scl.')
                self.o2scl=ctypes.CDLL(find_library("o2scl"),
                                  mode=ctypes.RTLD_GLOBAL)
                
            else:
                if self.verbose>0:
                    print('Loading',self.o2scl_lib_dir+'/libo2scl.so .')
                self.o2scl=ctypes.CDLL(self.o2scl_lib_dir+'/libo2scl.so',
                                  mode=ctypes.RTLD_GLOBAL)
        
            if self.verbose>0:
                print('Done loading o2scl libraries.')

        # This is necessary even if we're only including o2scl because
        # the o2scl error handler is sometimes used by GSL functions
        if self.verbose>0:
            print('Setting alternate error handler.')
        self.o2scl.o2scl_python_prep()

        # Get the global library settings pointer
        func=self.o2scl.o2scl_get_o2scl_settings
        func.restype=ctypes.c_void_p
        ptr=func()

        # Create a library settings object with the pointer
        #self.o2scl_settings=lib_settings_class(self,ptr)
        
        return
    
    def get_library_settings(self,argv=[]):
        """
        Get the library settings from environment variables or 
        the command-line arguments
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
                    if self.verbose>0:
                        print('Set o2scl_lib_dir from command-line to',
                              self.o2scl_lib_dir)
            elif argv[i]=='-o2scl-cpp-lib':
                if i>=len(argv)-1:
                    print('Option -o2scl-cpp-lib specified with no value.')
                else:
                    self.o2scl_cpp_lib=argv[i+1]
                    if self.verbose>0:
                        print('Set o2scl_cpp_lib from command-line to',
                              self.o2scl_cpp_lib)
            elif argv[i]=='-o2scl-addl-libs':
                if i>=len(argv)-1:
                    print('Option -o2scl-addl-libs specified with no value.')
                else:
                    self.o2scl_addl_libs=argv[i+1].split(',')
                    if self.verbose>0:
                        print('Set o2scl_addl_libs from command-line to',
                              self.o2scl_addl_libs)
            elif argv[i]=='-backend':
                if i>=len(argv)-1:
                    print('Option -backend specified with no value.')
                else:
                    self.backend=argv[i+1]
            elif argv[i]=='-debug-link':
                self.verbose=1
                
        self.backend=if_yt_then_Agg(self.backend,argv)
        
        return self.backend

def build_o2scl(verbose=1,release=True):
    """
    This function attempts to automatically build O2scl using 
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

