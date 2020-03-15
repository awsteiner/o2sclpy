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
from o2sclpy.utils import force_bytes

# For find_library() in link_o2scl()
from ctypes.util import find_library

o2scl_libdir=''
o2scl_cpplib=''
o2scl=0
o2scl_hdf=0
o2scl_part=0

def build_o2scl(verbose=1,release=True):
    """
    This function attempts to automatically build O\ :sub:`2`\ scl using 
    homebrew on OSX and snap on Linux.

    This function is in ``link_o2scl.py``.
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

def link_o2scl(verbose=1):
    """
    This function attempts to automatically load O\ :sub:`2`\ scl as a 
    DLL and returns the ``o2scl`` and ``o2scl_hdf`` DLL pointers.

    This function is in ``link_o2scl.py``.
    """

    global o2scl_libdir, o2scl_cpplib, o2scl, o2scl_hdf
    
    # Handle OSX and Linux separately
    if platform.system()=='Darwin':

        if verbose>=2:
            print('Using OSX library rules.')

        if (o2scl_cpplib=='' and os.getenv('O2SCL_CPPLIB') is not None
            and force_bytes(os.getenv('O2SCL_CPPLIB'))!=b'None'):
            o2scl_cpplib=os.getenv('O2SCL_CPPLIB')
            if verbose>0:
                print('Value of o2scl_cpplib is',o2scl_cpplib,'.')
        elif verbose>=2:
            print('Value of o2scl_cpplib is',o2scl_cpplib,'.')
      
        if o2scl_cpplib!='' and o2scl_cpplib!='skip':
            if verbose>0:
                print('Loading',o2scl_cpplib)
            systcpp=ctypes.CDLL(o2scl_cpplib,mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded system C++ library.')
            elif o2scl_cpp_lib=='skip' and verbose>0:
                print('Skipping load of C++ library.')
      
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
                if verbose>0:
                    print('Loading',o2scl_libdir+'/libo2scl.dylib')
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
                print('Loaded o2scl (1).')
            if verbose>0:
                print('Loading',o2scl_libdir+'/libo2scl_hdf.dylib')
            o2scl_hdf=ctypes.CDLL(o2scl_libdir+'/libo2scl_hdf.dylib',
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
        
        if (o2scl_libdir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_libdir=os.getenv('O2SCL_LIB')
            print('Set o2scl-libdir to',o2scl_libdir)
          
        if o2scl_libdir=='':
            o2scl=ctypes.CDLL(find_library("o2scl"),mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl (3).')
            o2scl_hdf=ctypes.CDLL(find_library("o2scl_hdf"),
                                mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf (3).')
        else:
            o2scl=ctypes.CDLL(o2scl_libdir+'/libo2scl.so',
                              mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl (4).')
            o2scl_hdf=ctypes.CDLL(o2scl_libdir+'/libo2scl_hdf.so',
                                  mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_hdf (4).')

    return
    
def link_o2scl_part(verbose=1):
    """
    """

    global o2scl_libdir, o2scl_cpplib, o2scl_part
    
    # Handle OSX and Linux separately
    if platform.system()=='Darwin':
    
        if verbose>=2:
            print('Using OSX library rules.')
          
        if (o2scl_libdir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_libdir=os.getenv('O2SCL_LIB')
            if verbose>0:
                print('Value of o2scl_libdir is ',o2scl_libdir,'.')
        elif verbose>=2:
                print('Value of o2scl_libdir is ',o2scl_libdir,'.')
          
        if o2scl_libdir!='':
            try:
                o2scl_part=ctypes.CDLL(o2scl_libdir+'/libo2scl_part.dylib',
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
    
        if (o2scl_libdir=='' and os.getenv('O2SCL_LIB') is not None and
            force_bytes(os.getenv('O2SCL_LIB'))!=b'None'):
            o2scl_libdir=os.getenv('O2SCL_LIB')
            print('Set o2scl-libdir to',o2scl_libdir)
          
        if o2scl_libdir=='':
            o2scl_part=ctypes.CDLL(find_library("o2scl_part"),
                                   mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_part (3).')
        else:
            o2scl_part=ctypes.CDLL(o2scl_libdir+'/libo2scl_part.so',
                              mode=ctypes.RTLD_GLOBAL)
            if verbose>0:
                print('Loaded o2scl_part (4).')
    return
    
