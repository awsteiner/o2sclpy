#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2018, Andrew W. Steiner
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

import getopt, sys, h5py, math, os, hashlib
import matplotlib.pyplot as plot
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import urllib.request
import numpy
import ctypes
import readline
import textwrap

version='0.922'
"""
The version number string
"""

"""
This is a list of 4-element entries:
1: command name
2: short description
3: argument list
4: full help text
"""
base_list=[
    ["backend","Select the matplotlib backend to use.","<backend>",
     "This selects the matplotlib backend. "+
     "Typical values are 'Agg', 'TkAgg', 'WX', 'QTAgg', 'QT4Agg'. "+
     "Use -backend Agg to save the plot to a file without "+
     "opening a window."],
    ["canvas","Create a plotting canvas.","",
     "Create an empty plotting canvas. For example 'o2graph "+
     "-canvas -show'."],
    ["clf","Clear the current figure.","",
     "Clear the current figure."],
    ["line","Plot a line.","<x1> <y1> <x2> <y2> [kwargs]",
     "Plot a line from (x1,y1) to (xy,y2). Some useful "+
     "kwargs are color (c), dashes, linestyle (ls), linewidth (lw), "+
     "marker, markeredgecolor (mec), markeredgewidth (mew), "+
     "markerfacecolor (mfc), markerfacecoloralt (mfcalt), markersize "+
     "(ms). For example: o2graph -line 0.05 0.05 0.95 0.95 "+
     "lw=0,marker='+' -show"],
    ["move-labels","Move the labels.","",""],
    ["new-cmaps","Define new color maps.","",
     "Define new color maps, 'jet2', 'pastel2' "+
     "'reds2', 'greens2', and 'blues2'."],
    ["plot-files",
     "Specify a list of files for 'plotm' and 'plot1m'.",
     "<file 1> [file 2] ...",""],
    ["plot1m",
     "Plot the specified column from tables in multiple files.",
     "<y>","After using -plot-files to specify "+
     "a list of files, plot column <y> versus row number for the first "+
     "table object in all of the specified files. Some useful "+
     "kwargs are color (c), dashes, linestyle (ls), linewidth (lw), "+
     "marker, markeredgecolor (mec), markeredgewidth (mew), "+
     "markerfacecolor (mfc), markerfacecoloralt (mfcalt), markersize "+
     "(ms). For example: o2graph -plot-files file1.o2 file2.o "+
     "-plot1m ycol lw=0,marker='+' -show"],
    ["plotm",
     "Plot the specified columns from tables in multiple files.",
     "<x> <y>","After using -plot-files to specify "+
     "a list of files, plot column <y> versus column <x> for the first "+
     "table object in all of the specified files. Some useful "+
     "kwargs are color (c), dashes, linestyle (ls), linewidth (lw), "+
     "marker, markeredgecolor (mec), markeredgewidth (mew), "+
     "markerfacecolor (mfc), markerfacecoloralt (mfcalt), markersize "+
     "(ms). For example: o2graph -plot-files file1.o2 file2.o "+
     "-plotm xcol ycol lw=0,marker='+' -show"],
    ["rect","Plot a rectangle.",
     "<x1> <y1> <x2> <y2> <angle> [kwargs]",
     "Plot a rectange from (x1,y1) to (xy,y2) with "+
     "rotation angle <angle>. By default, the rectangle has no border, "+
     "but the linewidth ('lw') and edgecolor kwargs can be used to "+
     "specify one if desired."],
    ["reset-xlim","Reset the x-axis limits.","",
     "This is an alias for 'set xset False', and indicates "+
     "that the values of 'xlo' and 'xhi' are to be ignored until the "+
     "next call to 'xlimits'."],
    ["reset-ylim","Reset the y-axis limits.","",
     "This is an alias for 'set yset False', and indicates "+
     "that the values of 'ylo' and 'yhi' are to be ignored until the "+
     "next call to 'ylimits'."],
    ["reset-zlim","Reset the z-azis limits.","",
     "This is an alias for 'set zset False', and indicates "+
     "that the values of 'zlo' and 'zhi' are to be ignored until the "+
     "next call to 'zlimits'."],
    ["save","Save the current plot in a file.","<filename>",
     "Save the current plot in a file similar "+
     "to plot.savefig(). The action of this command depends on "+
     "which backend was selected. File type depends on the "+
     "extension, typically either .png, .pdf, .eps, .jpg, .raw, .svg, "+
     "and .tif ."],
    ["show","Show the current plot.","","Show the current plot "+
     "on the screen and begin "+
     "the graphical user interface. This is similar to plot.show()."],
    ["text","Plot text in the axis coordinate system.",
     "<x> <y> <text> [kwargs]",""],
    ["ttext","Plot text in the canvas default coordinate system.",
     "<x> <y> <text> [kwargs]",""],
    ["xlimits","Set the x-axis limits.","<low> <high>",
     "Set 'xlo' and 'xhi' to the specified limits, "+
     "and set 'xset' to true. If a plotting canvas is currently "+
     "open, then "+
     "the x-limits on that plot are modified. Future plots are also "+
     "set with the specified x-limits."],
    ["ylimits","Set the y-axis limits.","<low> <high>",
     "Set 'ylo' and 'yhi' to the specified limits, "+
     "and set 'yset' to true. If a plotting canvas is currently "+
     "open, then "+
     "the y-limits on that plot are modified. Future plots are also "+
     "set with the specified y-limits."],
    ["zlimits","Set the z-azis limits.","<low> <high>",
     "Set 'zlo' and 'zhi' to the specified limits, "+
     "and set 'zset' to true. If a plotting canvas is currently "+
     "open, then "+
     "the z-limits on that plot are modified. Future plots are also "+
     "set with the specified z-limits."]
]

"""
This is a list of 5-element entries:
1: object type
2: command name
3: short description
4: argument list
5: full help text
"""
extra_list=[
    ["table","plot",
     "Plot two columns from the table.",
     "<x> <y> [kwargs]",
     "If the current object is a table, then plot "+
     "column <y> versus column "+
     "<x>. If the current object is a one-dimensional histogram, then plot "+
     "the histogram weights as a function of the bin representative values. "+
     "If the current object is a set of contour lines, then plot the full "+
     "set of contour lines. Some useful kwargs are color (c), dashes, "+
     "linestyle (ls), linewidth (lw), marker, markeredgecolor (mec), "+
     "markeredgewidth (mew), markerfacecolor (mfc), markerfacecoloralt "+
     "(mfcalt), markersize (ms). For example: o2graph -create x 0 10 0.2 "+
     "-function sin(x) y -plot x y lw=0,marker='+' -show"],
    ["table","plot-ser",
     "Plot two series from a row in table.",
     "<row> <pattern 1> <pattern 2>",""],
    ["table","plot1-ser",
     "Plot a series from a row in table.","<row> <pattern>",""],
    ["table","rplot",
     "Plot a region inside a column or in between two columns.",
     "<x1> <y1> [x2 y2] [kwargs]",
     "If either 2 or 3 arguments are specified, "+
     "this command plots the "+
     "region inside the curve defined by the specified set of x and y "+
     "values. The first point is copied at the end to ensure a closed "+
     "region. If 4 or 5 arguments are specified, then this command plots the "+
     "region in between two sets of x and y values, again adding the first "+
     "point from (x1,y1) to the end to ensure a closed region."],
    ["table","scatter","Create a scatter plot from 2-4 columns.",
     "<x> <y> [s] [c] [kwargs]",
     "This command creates a scatter plot form "+
     "columns <x> and <y>, "+
     "optionally using column [s] to choose the marker size and optionally "+
     "using column [c] to choose the marker color. To vary the marker colors "+
     "while choosing the default marker size just specify 'None' as the "+
     "argument for [s]. Or, to specify keyword arguments while using the "+
     "default size and color, specify 'None' as the argument for both [s] "+
     "and [c]."],
    ["table","errorbar",
     "Plot the specified columns with errobars.",
     "<x> <y> <xerr> <yerr> [kwargs]",
     "Plot column <y> versus column <x> with "+
     "symmetric error bars given in "+
     "column <xerr> and <yerr>. For no uncertainty in either the x or y "+
     "direction, just use 0 for <xerr> or <yerr>, respectively. New kwargs "+
     "for the errorbar command are ecolor=None, elinewidth=None, "+
     "capsize=None, barsabove=False, lolims=False, uplims=False, "+
     "xlolims=False, xuplims=False, errorevery=1, capthick=None, hold=None"],
    ["table","plot1","Plot the specified column.","<y> [kwargs]",
     "Plot column <y> versus row number. Some "+
     "useful kwargs are color (c), "+
     "dashes, linestyle (ls), linewidth (lw), marker, markeredgecolor (mec), "+
     "markeredgewidth (mew), markerfacecolor (mfc), markerfacecoloralt "+
     "(mfcalt), markersize (ms). For example: o2 -create x 0 10 0.2 "+
     "-function sin(x) y -plot1 y ls='--',marker='o' -show"],
    ["table","histplot","Create a histogram plot from column in a table.",
     "<col>","For a table, create a histogram plot from the "+
     "specified column. This command uses matplotlib to construct the "+
     "histogram rather than using O2scl to create a hist_2d object."],
    ["table","hist2dplot",
     "Create a 2-D histogram plot from two columns in a table.",
     "<col x> <col y>","For a table, create a 2D histogram plot from "+
     "the specified columns. This command uses matplotlib to construct the "+
     "histogram rather than using O2scl to create a hist object."],
    ["table3d","den-plot","Create a density plot from a table3d object.",
     "<slice>",
     "Creates a density plot from the specified "+
     "slice. Logarithmic x- or "+
     "y-axes are handled by taking the base 10 log of the x- or y-grids "+
     "specified in the table3d object before plotting. A z-axis density "+
     "legend is print on the RHS if colbar is set to True before plotting. If "+
     "z-axis limits are specified, then values larger than the upper limit "+
     "are set equal to the upper limit and values smaller than the lower "+
     "limit are set equal to the lower limit before plotting."],
    ["hist","plot","Plot the histogram.","[kwargs]",
     "Plot the histogram weights as a function "+
     "of the bin representative values. "+
     "Some useful kwargs (which apply for all three object types) are "+
     "color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms). For example: o2graph "+
     "-create x 0 10 0.2 -function sin(x) y "+
     "-plot x y lw=0,marker='+' -show"],
    ["double[]","plot1","Plot the array.","[kwargs]",
     "Plot the array. Some useful kwargs "+
     "are color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms)."],
    ["int[]","plot1","Plot the array.","[kwargs]",
     "Plot the array. Some useful kwargs "+
     "are color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms)."],
    ["size_t[]","plot1","Plot the array.","[kwargs]",
     "Plot the array. Some useful kwargs "+
     "are color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms)."],
    ["vector<contour_line>","plot","Plot the contour lines.","[kwargs]",
     "Plot the set of contour lines. Some "+
     "useful kwargs (which apply for all three "+
     "object types) are color (c), dashes, linestyle (ls), linewidth (lw), "+
     "marker, markeredgecolor (mec), markeredgewidth (mew), markerfacecolor "+
     "(mfc), markerfacecoloralt (mfcalt), markersize (ms). For example: "+
     "o2graph -create x 0 10 0.2 -function sin(x) y -plot x y "+
     "lw=0,marker='+' -show"],
    ["hist_2d","den-plot","Create a density plot from a hist_2d object",
     "[kwargs]","Create a density plot from the current histogram (assuming "+
     "equally-spaced bins). Logarithmic x- or y-axes are handled by taking "+
     "the base 10 log of the x- or y-grids specified in the table3d object "+
     "before plotting. A z-axis density legend is print on the RHS if colbar "+
     "is set to 1 before plotting. If z-axis limits are specified, then "+
     "values larger than the upper limit are set equal to the upper limit "+
     "and values smaller than the lower limit are set equal to the lower "+
     "limit before plotting."]
]

param_list=[
    ["bottom-margin","Size of bottom margin for a new canvas"+
     " (default 0.12)."],
    ["colbar","If true, den-plot adds a color legend (default False)."],
    ["fig-size-x","Horizontal figure size (default 6.0)."],
    ["fig-size-y","Vertical figure size (default 6.0)."],
    ["font","Font scaling for text objects (default 16)."],
    ["left-margin","Size of left margin for a new canvas"+
     " (default 0.14)."],
    ["logx","If true, use a logarithmic x-axis (default False)."],
    ["logy","If true, use a logarithmic y-axis (default False)."],
    ["logz","If true, use a logarithmic z-axis (default False)."],
    ["right-margin","Size of right margin for a new canvas"+
     " (default 0.04)."],
    ["top-margin","Size of top margin for a new canvas"+
     " (default 0.04)."],
    ["verbose","Verbosity parameter (default 1)."],
    ["xhi","Upper limit for x-axis (function if starts with '(')."],
    ["xlo","Lower limit for x-axis (function if starts with '(')."],
    ["xset","If true, x-axis limits have been set (default False)."],
    ["xtitle","X-axis title. Latex "+
     "works, e.g. '$\\phi$' and '$\\hat{x}$' (default '')"],
    ["yhi","Upper limit for y-axis (function if starts with '(')."],
    ["ylo","Lower limit for y-axis (function if starts with '(')."],
    ["yset","If true, y-axis limits have been set (default False)."],
    ["ytitle","Y-axis title. Latex "+
     "works, e.g. '$\\phi$' and '$\\hat{x}$' (default '')"],
    ["zlo","Lower limit for z-axis (function if starts with '(')."],
    ["zhi","Upper limit for z-axis (function if starts with '(')."],
    ["zset","If true, z-axis limits have been set (default False)."]
]

param_dict={
    "bottom-margin": "Size of bottom margin for a new canvas"+
    " (default 0.12).",
    "colbar": "If true, den-plot adds a color legend (default False).",
    "fig-size-x": "Horizontal figure size (default 6.0).",
    "fig-size-y": "Vertical figure size (default 6.0).",
    "font": "Font scaling for text objects (default 16).",
    "left-margin": "Size of left margin for a new canvas"+
    " (default 0.14).",
    "logx": "If true, use a logarithmic x-axis (default False).",
    "logy": "If true, use a logarithmic y-axis (default False).",
    "logz": "If true, use a logarithmic z-axis (default False).",
    "right-margin": "Size of right margin for a new canvas"+
    " (default 0.04).",
    "top-margin": "Size of top margin for a new canvas"+
    " (default 0.04).",
    "verbose": "Verbosity parameter (default 1).",
    "xhi": "Upper limit for x-axis (function if starts with '(').",
    "xlo": "Lower limit for x-axis (function if starts with '(').",
    "xset": "If true, x-axis limits have been set (default False).",
    "xtitle": "X-axis title. Latex "+
    "works, e.g. '$\\phi$' and '$\\hat{x}$' (default '')",
    "yhi": "Upper limit for y-axis (function if starts with '(').",
    "ylo": "Lower limit for y-axis (function if starts with '(').",
    "yset": "If true, y-axis limits have been set (default False).",
    "ytitle": "Y-axis title. Latex "+
    "works, e.g. '$\\phi$' and '$\\hat{x}$' (default '')",
    "zlo": "Lower limit for z-axis (function if starts with '(').",
    "zhi": "Upper limit for z-axis (function if starts with '(').",
    "zset": "If true, z-axis limits have been set (default False)."
}

class cloud_file:
    """
    A class to manage downloading files from the internet.

    .. warning:: This class has several potential security issues
                 (even if the md5 sum is verified) and should not be
                 used without due care.
    """
    
    force_subdir=True
    """
    If true, force the same subdirectory structure
    """
    env_var=''
    """
    The environment variable which specifies the data directory
    """
    verbose=1
    """
    The verbosity parameter
    """

    # These are commented out until the code is rewritten to
    # allow for them
    #username=''
    #The HTTP username
    #password=''
    #The HTTP password

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
    
    def download_file(self,filename,url,md5sum,directory):
        """
        This function proceeds in the following way:

        First, if ``directory`` is not then the function tries to find
        the requested directory. If it is not found, then ``mkdir -p``
        is used to create it. If this doesn't work, then a
        ``FileNotFoundError`` exception is thrown.

        The function then looks for the requested file in the
        directory. If the file is found
        and ``md5sum`` is not empty, then it compares it to the MD5
        checksum of the file.

        If the file is not found or if the checksum was specified
        and didn't match, then this function prompts the user
        to proceed before using
        ``urllib.request.urlretrieve()`` to download the file from
        ``url``. Afterwards, the MD5 checksum is checked again. 
        If the file cannot be found or if the checksum doesn't
        match, a ``ConnectionError`` exception is thrown.
        Otherwise, the function was successful, and the full filename 
        (including subdirectory if applicable) is returned.

        This function works similarly to the C++ O\ :sub:`2`\ scl
        function ``o2scl::cloud_file::get_file_hash()``.
        """
        
        # Test for the existence of the directory and create it if
        # necessary
        if directory!='':
            if os.path.isdir(directory)==False:
                if verbose>0:
                    print('Directory '+directory+'not found.')
                    print('Trying to automatically create using "mkdir -p"')
                cmd='mkdir -p '+directory
                ret=os.system(cmd)
                if ret!=0:
                    raise FileNotFoundError('Directory does '+
                                            'not exist and failed to create.')
                
        # The local filename
        full_name=directory+'/'+filename

        # Check the hash
        hash_match=False
        if md5sum=='':
            hash_match=True
        elif os.path.isfile(full_name)==True:
            mhash2=mda5(full_name)
            if md5sum==mhash2:
                hash_match=True
            elif verbose>0:
                print('Hash of file',full_name,'did not match',md5sum)
        elif verbose>0:
            print('Could not find file',full_name)
            
        # Now download the file if it's not already present
        if hash_match==False or os.path.isfile(full_name)==False:
            response=input('Hash did not match or data file '+full_name+
                           ' not found. Download (y/Y/n/N)? ')
            ret=1
            if response=='y' or response=='Y':
                if verbose>0:
                    print('Trying to download:')
                urllib.request.urlretrieve(url,full_name)
                ret=0
            if ret==0:
                mhash2=mda5(full_name)
                if md5sum!=mhash2:
                    raise ConnectionError('Downloaded file but '+
                                          'has does not match.')
            if ret!=0:
                raise ConnectionError('Failed to obtain data file.')
    
        # Return 0 for success
        return 0

class hdf5_reader:
    """
    Class to read an o2scl object from an HDF5 file. This is
    used by :py:class:`o2sclpy.plotter` to read HDF5 files.
    """

    list_of_dsets=[]
    """
    Data set list used by :py:func:`cloud_file.hdf5_is_object_type`.
    """
    search_type=''
    """
    O2scl type used by :py:func:`cloud_file.hdf5_is_object_type`.
    """

    def hdf5_is_object_type(self,name,obj):
        """
        This is an internal function not intended for use by the end-user.
        If object ``obj`` named ``name`` is of type 'search_type',
        then this function adds that name to 'list_of_dsets'
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
        Read the first object of type ``loc_type`` from file named ``fname``
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
        Read object named ``name`` from file named ``fname``
        """
        file=h5py.File(fname,'r')
        obj=file[name]
        o2scl_type_dset=obj['o2scl_type']
        loc_type=o2scl_type_dset.__getitem__(0)
        return (obj,loc_type)
    
    def h5read_type_named(self,fname,loc_type,name):
        """
        Read object of type ``loc_type`` named ``name`` from file 
        named ``fname``
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

# This function is probably best replaced by get_str_array() below
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

def default_plot(left_margin=0.14,bottom_margin=0.12,
                 right_margin=0.04,top_margin=0.04,font=16,
                 fig_size_x=6.0,fig_size_y=6.0):
    """
    This function sets up my commonly-used ``matplotlib`` defaults.
    It returns a pair of objects, the figure object and axes object.
    """
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')
    plot.rcParams['lines.linewidth']=0.5
    fig=plot.figure(1,figsize=(fig_size_x,fig_size_y))
    fig.set_facecolor('white')
    ax=plot.axes([left_margin,bottom_margin,
                  1.0-left_margin-right_margin,1.0-top_margin-bottom_margin])
    ax.minorticks_on()
    ax.tick_params('both',length=12,width=1,which='major')
    ax.tick_params('both',length=5,width=1,which='minor')
    ax.tick_params(labelsize=font*0.8)
    plot.grid(False)
    return (fig,ax)
    
def get_str_array(dset):
    """
    Extract a string array from O2scl HDF5 dataset ``dset`` as a list
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
    Old command-line parser (this is currently unused and
    it's not clear if it will be useful in the future).
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
    Convert a string to a dictionary, with extra processing for some
    matplotlib keyword arguments which are expected to have integer or
    floating point values.
    """
    # First split into keyword = value pairs
    arr=s.split(',')
    # Create empty dictionary
    dct={}
    for i in range(0,len(arr)):
        # For each pair, split keyword and value.
        arr2=arr[i].split('=')

        # Remove quotes if necessary
        if arr2[1][0]=='\'' and arr2[1][len(arr2[1])-1]=='\'':
            arr2[1]=arr2[1][1:len(arr2[1])-1]
        if arr2[1][0]=='"' and arr2[1][len(arr2[1])-1]=='"':
            arr2[1]=arr2[1][1:len(arr2[1])-1]
        # convert strings to numbers if necessary
        if arr2[0]=='lw':
            arr2[1]=float(arr2[1])
        if arr2[0]=='alpha':
            arr2[1]=float(arr2[1])
        if arr2[0]=='bins':
            arr2[1]=int(arr2[1])
        if arr2[0]=='fill':
            if arr2[1]=='True':
                arr2[1]=True
            else:
                arr2[1]=False

        # assign to dictionary
        dct[arr2[0]]=arr2[1]
        
    return dct

class plot_base:
    """
    A base class for plotting classes :py:class:`o2sclpy.plotter` and
    :py:class:`o2sclpy.o2graph_plotter` .    
    """

    axes=0
    """ 
    Axis object
    """
    fig=0
    """ 
    Figure object
    """
    canvas_flag=False
    """
    If True, then the default plot canvas has been initiated
    """

    # Quantities modified by set/get
    
    logx=False
    """
    If True, then use a logarithmic x axis
    """
    logy=False
    """
    If True, then use a logarithmic y axis
    """
    logz=False
    """
    If True, then use a logarithmic z axis
    """
    xtitle=''
    """
    Title for x axis
    """
    ytitle=''
    """
    Title for y axis
    """
    xlo=0
    """
    Lower limit for x axis
    """
    xhi=0
    """
    Upper limit for x axis
    """
    xset=False
    """ 
    If True, then the x axis limits have been set
    """
    ylo=0
    """
    Lower limit for y axis
    """
    yhi=0
    """
    Upper limit for y axis
    """
    yset=False
    """ 
    If True, then the y axis limits have been set
    """
    zlo=0
    """
    Lower limit for z axis
    """
    zhi=0
    """
    Upper limit for z axis
    """
    zset=False
    """ 
    If True, then the z axis limits have been set
    """
    verbose=1
    """
    Verbosity parameter
    """
    colbar=False
    """
    If True, then include a color legend for density plots
    """
    plotfiles=''
    """
    List of filenames for multiplots
    """
    left_margin=0.14
    """
    Left plot margin (default 0.14)
    """
    right_margin=0.04
    """
    Right plot margin (default 0.04)
    """
    top_margin=0.04
    """
    Top plot margin (default 0.04)
    """
    bottom_margin=0.12
    """
    Bottom plot margin (default 0.12)
    """
    font=16
    """
    Font size for text(), ttext(), axis titles (default 16). Axis labels
    are set by this size times 0.8 .
    """
    fig_size_x=6.0
    """
    The x-scale for the figure object
    """
    fig_size_y=6.0
    """
    The y-scale for the figure object
    """
    
    def new_cmaps(self):
        """
        Add a few new colormaps
        """
        # A white to red colormap
        cdict={'red': ((0.0,1.0,1.0),(1.0,1.0,1.0)),
               'green': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(1.0,0.0,0.0))}
        reds2=LinearSegmentedColormap('reds2',cdict)
        plot.register_cmap(cmap=reds2)
        # A new version of the ``jet`` colormap which starts with
        # white instead of blue. In order, the index colors are white,
        # blue, green, yellow, orange, and red
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
        # A new version of the ``pastel`` colormap which starts with
        # white instead of blue. In order, the index colors are white,
        # blue, green, yellow, orange, and red
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
        # A white to green colormap
        cdict={'red': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'green': ((0.0,1.0,1.0),(1.0,1.0,1.0)),
               'blue': ((0.0,1.0,1.0),(1.0,0.0,0.0))}
        greens2=LinearSegmentedColormap('greens2',cdict)
        plot.register_cmap(cmap=greens2)
        # A white to blue colormap
        cdict={'red': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'green': ((0.0,1.0,1.0),(1.0,0.0,0.0)),
               'blue': ((0.0,1.0,1.0),(1.0,1.0,1.0))}
        blues2=LinearSegmentedColormap('blues2',cdict)
        plot.register_cmap(cmap=blues2)
        
    def set(self,name,value):
        """
        Set the value of parameter named ``name`` to value ``value``
        """
        if name=='logx':
            if value=='False' or value=='0':
                self.logx=False
            else:
                self.logx=True
        elif name=='logy':
            if value=='False' or value=='0':
                self.logy=False
            else:
                self.logy=True
        elif name=='logz':
            if value=='False' or value=='0':
                self.logz=False
            else:
                self.logz=True
        elif name=='xtitle':
            self.xtitle=value
        elif name=='ytitle':
            self.ytitle=value
        elif name=='xlo':
            if value[0]=='(':
                self.xlo=float(eval(value))
            else:
                self.xlo=float(value)
            self.xset=True
        elif name=='xhi':
            if value[0]=='(':
                self.xhi=float(eval(value))
            else:
                self.xhi=float(value)
            self.xset=True
        elif name=='xset':
            if value=='False' or value=='0':
                self.xset=False
            else:
                self.xset=True
        elif name=='ylo':
            if value[0]=='(':
                self.ylo=float(eval(value))
            else:
                self.ylo=float(value)
            self.yset=True
        elif name=='yhi':
            if value[0]=='(':
                self.yhi=float(eval(value))
            else:
                self.yhi=float(value)
            self.yset=True
        elif name=='yset':
            if value=='False' or value=='0':
                self.xset=False
            else:
                self.xset=True
        elif name=='zlo':
            if value[0]=='(':
                self.zlo=float(eval(value))
            else:
                self.zlo=float(value)
            self.zset=True
        elif name=='zhi':
            if value[0]=='(':
                self.zhi=float(eval(value))
            else:
                self.zhi=float(value)
            self.zset=True
        elif name=='zset':
            if value=='False' or value=='0':
                self.zset=False
            else:
                self.zset=True
        elif name=='verbose':
            self.verbose=int(value)
        elif name=='colbar':
            if value=='False' or value=='0':
                self.colbar=False
            else:
                self.colbar=True
        elif name=='font':
            self.font=float(value)
        elif name=='left-margin':
            self.left_margin=float(value)
        elif name=='right-margin':
            self.right_margin=float(value)
        elif name=='top-margin':
            self.top_margin=float(value)
        elif name=='bottom-margin':
            self.bottom_margin=float(value)
        elif name=='fig_size_x':
            self.fig_size_x=float(value)
        elif name=='fig_size_y':
            self.fig_size_y=float(value)
        else:
            print('No variable named',name)
            
        if self.verbose>0:
            print('Set',name,'to',value)
            
        return

    def get(self,name):
        """
        Output the value of parameter named ``name``
        """
        if name=='colbar':
            print('The value of colbar is',self.colbar,'.')
        if name=='logx':
            print('The value of logx is',self.logx,'.')
        if name=='logy':
            print('The value of logy is',self.logy,'.')
        if name=='logz':
            print('The value of logz is',self.logz,'.')
        if name=='verbose':
            print('The value of verbose is',self.verbose,'.')
        if name=='xhi':
            print('The value of xhi is',self.xhi,'.')
        if name=='xlo':
            print('The value of xlo is',self.xlo,'.')
        if name=='xset':
            print('The value of xset is',self.xset,'.')
        if name=='xtitle':
            print('The value of xtitle is',self.xtitle,'.')
        if name=='yhi':
            print('The value of yhi is',self.yhi,'.')
        if name=='ylo':
            print('The value of ylo is',self.ylo,'.')
        if name=='yset':
            print('The value of yset is',self.yset,'.')
        if name=='ytitle':
            print('The value of ytitle is',self.ytitle,'.')
        if name=='zhi':
            print('The value of zhi is',self.zhi,'.')
        if name=='zlo':
            print('The value of zlo is',self.zlo,'.')
        if name=='zset':
            print('The value of zset is',self.zset,'.')
        if name=='top-margin':
            print('The value of top-margin is',self.top_margin,'.')
        if name=='bottom-margin':
            print('The value of bottom-margin is',self.bottom_margin,'.')
        if name=='right-margin':
            print('The value of right-margin is',self.right_margin,'.')
        if name=='left-margin':
            print('The value of left-margin is',self.left_margin,'.')
        if name=='fig-size-x':
            print('The value of fig-size-x is',self.fig_size_x,'.')
        if name=='fig-size-y':
            print('The value of fig-size-y is',self.fig_size_y,'.')
        return

    def reset_xlimits(self):
        """
        Reset x axis limits
        """
        self.xset=False
        return

    def xlimits(self,xlo,xhi):
        """
        Set the x-axis limits
        """
        self.xlo=xlo
        self.xhi=xhi
        self.xset=True
        if self.canvas_flag==True:
            plot.xlim([xlo,xhi])
        return

    def reset_ylimits(self):
        """
        Reset y axis limits
        """
        self.yset=False
        return

    def ylimits(self,ylo,yhi):
        """
        Set the y-axis limits
        """
        self.ylo=ylo
        self.yhi=yhi
        self.yset=True
        if self.canvas_flag==True:
            plot.ylim([ylo,yhi])
        return

    def reset_zlimits(self):
        """
        Reset z axis limits
        """
        self.zset=False
        return

    def zlimits(self,zlo,zhi):
        """
        Set the z-axis limits
        """
        self.zlo=zlo
        self.zhi=zhi
        self.zset=True
        #if self.canvas_flag==True:
        #plot.zlim([zlo,zhi])
        return

    def line(self,x1,y1,x2,y2,**kwargs):
        """
        Plot a line from :math:`(x_1,y_1)` to :math:`(x_2,y_2)`
        """
        if self.verbose>2:
            print('Line',x1,y1,x2,y1)
        if self.canvas_flag==False:
            self.canvas()
        plot.plot([float(x1),float(x2)],[float(y1),float(y2)],**kwargs)
        return

    def point(self,xval,yval,**kwargs):
        """
        Desc
        """
        if self.verbose>2:
            print('point',xval,yval,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        plot.plot([float(xval)],[float(yval)],**kwargs)
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
        return

    def rect(self,x1,y1,x2,y2,angle,**kwargs):
        """
        Plot a rectangle from :math:`(x_1,y_1)` to :math:`(x_2,y_2)`
        """
        if self.verbose>2:
            print('Rect',x1,y1,x2,y1)
        if self.canvas_flag==False:
            self.canvas()
        fx1=float(x1)
        fx2=float(x2)
        fy1=float(y1)
        fy2=float(y2)
        left=fx1
        if fx2<fx1:
            left=fx2
        lower=fy1
        if fy2<fy1:
            lower=fy2
        w=abs(fx1-fx2)
        h=abs(fy1-fy2)
        if self.canvas_flag==False:
            self.canvas()
        r=patches.Rectangle((left,lower),w,h,angle,**kwargs)
        self.axes.add_patch(r)
        return

    def show(self):
        """
        Call the ``matplotlib`` show function.
        """
        plot.show()
        return

    def save(self,filename):
        """
        Save plot to file named ``filename``
        """
        if self.verbose>0:
            print('Saving as',filename,'.')
        plot.savefig(filename)
        return

    def force_bytes(self,obj):
        """
        In cases where we're unsure whether or not ``obj`` is a string or
        bytes object, we ensure it's a bytes object by converting if
        necessary.
        """
        if isinstance(obj,numpy.bytes_)==False and isinstance(obj,bytes)==False:
            return bytes(obj,'utf-8')
        return obj
    
    def ttext(self,tx,ty,str,**kwargs):
        """
        Plot text in the native coordinate system
        """
        if self.canvas_flag==False:
            self.canvas()
        ha_present=False
        for key in kwargs:
            if key=='ha':
                ha_present=True
        if ha_present==False:
            self.axes.text(float(eval(tx)),float(eval(ty)),
                           str,transform=self.axes.transAxes,
                           fontsize=self.font,va='center',ha='center',
                           **kwargs)
        else:
            self.axes.text(float(eval(tx)),float(eval(ty)),
                           str,transform=self.axes.transAxes,
                           fontsize=self.font,va='center',
                           **kwargs)
        return

    def text(self,tx,ty,str,**kwargs):
        """
        Plot text in the axis coordinate system
        """
        if self.canvas_flag==False:
            self.canvas()
        ha_present=False
        for key in kwargs:
            if key=='ha':
                ha_present=True
        if ha_present==False:
            self.axes.text(float(eval(tx)),float(eval(ty)),str,
                           fontsize=self.font,va='center',ha='center',**kwargs)
        else:
            self.axes.text(float(eval(tx)),float(eval(ty)),str,
                           fontsize=self.font,va='center',**kwargs)
        return

    def canvas(self):
        """
        Create a default figure and axis object with specified
        titles and limits .
        """
        if self.verbose>2:
            print('Canvas')
        # Default o2mpl plot
        (self.fig,self.axes)=default_plot(self.left_margin,
                                          self.bottom_margin,
                                          self.right_margin,
                                          self.top_margin,self.font,
                                          self.fig_size_x,self.fig_size_y)
        # Plot limits
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
        # Titles
        if self.xtitle!='':
            plot.xlabel(self.xtitle,fontsize=self.font)
        if self.ytitle!='':
            plot.ylabel(self.ytitle,fontsize=self.font)
        self.canvas_flag=True
        return

    def move_labels(self):
        """
        Move tick labels
        """
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

class plotter(plot_base):
    """ 
    A class useful for quickly plotting HDF5 data generated
    by O\ :sub:`2`\ scl . This class is a child of the
    :py:class:`o2sclpy.plot_base` class.
    """

    h5r=hdf5_reader()
    """
    Object which handles reading HDF5 files
    """
    dset=0
    """
    The current HDF5 dataset
    """
    dtype=''
    """
    The current type
    """

    def contour_plot(self,level,**kwargs):
        """
        If the current dataset is of type ``vector<contour_line>``, then
        plot the contour lines for the contour level specified in
        ``level``.
        """
        if self.force_bytes(self.dtype)!=b'vector<contour_line>':
            print('Wrong type',self.dtype,'for contour_plotx.')
            return
        if self.verbose>2:
            print('contour_plot',level,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        n_lines=self.dset['n_lines'][0]
        for i in range(0,n_lines):
            line_level=self.dset['line_'+str(i)+'/level'][0]
            if abs(level-line_level) < 1.0e-7:
                if self.logx==True:
                    if self.logy==True:
                        plot.loglog(self.dset['line_'+str(i)+'/x'],
                                    self.dset['line_'+str(i)+'/y'],**kwargs)
                    else:
                        plot.semilogx(self.dset['line_'+str(i)+'/x'],
                                      self.dset['line_'+str(i)+'/y'],**kwargs)
                else:
                    if self.logy==True:
                        plot.semilogy(self.dset['line_'+str(i)+'/x'],
                                      self.dset['line_'+str(i)+'/y'],**kwargs)
                    else:
                        plot.plot(self.dset['line_'+str(i)+'/x'],
                                  self.dset['line_'+str(i)+'/y'],**kwargs)
        return
 
    def plot(self,colx,coly,**kwargs):
        """
        If the current dataset is of type ``table``, then
        plot the two columns specified in ``colx`` and ``coly``.
        Otherwise, if the current dataset is of type 
        ``hist``, then plot the histogram and ignore the
        values of ``colx`` and ``coly``.
        """
        if self.force_bytes(self.dtype)==b'table':
            if self.verbose>2:
                print('plot',colx,coly,kwargs)
            if self.canvas_flag==False:
                self.canvas()
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
        elif self.force_bytes(self.dtype)==b'hist':
            size=dset['size'][0]
            bins=dset['bins']
            weights=dset['weights']
            rmode=dset['rmode'][0]
            reps=bins[0:size-1]
            for i in range(0,size):
                reps[i]=(bins[i]+bins[i+1])/2
            if self.logx==True:
                if self.logy==True:
                    plot.loglog(reps,weights,**kwargs)
                else:
                    plot.semilogx(reps,weights,**kwargs)
            else:
                if self.logy==True:
                    plot.semilogy(reps,weights,**kwargs)
                else:
                    plot.plot(reps,weights,**kwargs)
            if self.xset==True:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==True:
                plot.ylim([self.ylo,self.yhi])
            return
        return

    def scatter(self,colx,coly,cols,colc,**kwargs):
        """
        """
        if self.force_bytes(self.dtype)==b'table':
            if self.verbose>2:
                print('plot',colx,coly,kwargs)
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                self.axes.set_xscale('log')
            if self.logy==True:
                self.axes.set_yscale('log')

            if len(colc)>0:
                if len(cols)>0:
                    plot.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 s=self.dset['data/'+cols],
                                 c=self.dset['data/'+colc],
                                 **kwargs)
                else:
                    plot.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 c=self.dset['data/'+colc],
                                 **kwargs)
            else:
                if len(cols)>0:
                    plot.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 s=self.dset['data/'+cols],
                                 **kwargs)
                else:
                    plot.scatter(self.dset['data/'+colx],
                                 self.dset['data/'+coly],
                                 **kwargs)
            if self.xset==True:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==True:
                plot.ylim([self.ylo,self.yhi])
        return

    def plot1(self,col,**kwargs):
        """
        If the current dataset is of type ``table``, then
        plot the column specified in ``col``
        """
        if self.force_bytes(self.dtype)!=b'table':
            print('Wrong type',self.dtype,'for plot1.')
            return
        if self.verbose>2:
            print('plot1',col,kwargs)
        if self.canvas_flag==False:
            self.canvas()
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
    
    def histplot(self,col,**kwargs):
        """
        If the current dataset is of type ``hist``, then
        plot the associated histogram.
        """
        if self.verbose>2:
            print('histplot',kwargs)
        if self.canvas_flag==False:
            self.canvas()
        for key in kwargs:
            if key=='bins':
                kwargs[key]=int(kwargs[key])
        if self.force_bytes(self.dtype)==b'table':
            plot.hist(self.dset['data/'+col],**kwargs)
        else:
            print('Wrong type',self.dtype,'for histplot()')
        return

    def hist2dplot(self,colx,coly,**kwargs):
        """
        If the current dataset is of type ``hist2d``, then
        plot the associated two-dimensional histogram.
        """
        if self.verbose>2:
            print('hist2d',colx,coly,kwargs)
        if self.canvas_flag==False:
            self.canvas()
        for key in kwargs:
            if key=='bins':
                kwargs[key]=int(kwargs[key])
        plot.hist2d(self.dset['data/'+colx],self.dset['data/'+coly],**kwargs)
        return

    def read(self,filename):
        """
        Read first object of type ``table`` from file ``filename``
        """
        if self.verbose>0:
            print('Reading file',filename,'.')
        self.dset=self.h5r.h5read_first_type(filename,'table')
        self.dtype='table'
        return

    def read_type(self,filename,loc_type):
        """
        Read first object of type ``loc_type`` from file ``filename``
        """
        if self.verbose>0:
            print('Reading object of type',loc_type,
                  'in file',filename,'.')
        self.dset=self.h5r.h5read_first_type(filename,loc_type)
        self.dtype=loc_type
        return

    def read_name(self,filename,name):
        """
        Read object named ``name`` from file ``filename``
        """
        if self.verbose>0:
            print('Reading object named',name,'in file',filename,'.')
        atuple=self.h5r.h5read_name(filename,name)
        self.dset=atuple[0]
        self.dtype=atuple[1]
        return

    def list(self):
        """
        If the current data set is of type ``table``,
        then list the columns.
        """
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
        """
        If the current object is of type ``table3d``, create a density
        plot from the slice named ``slice_name`` .
        """
        if self.force_bytes(self.dtype)==b'table3d':
            name='data/'+slice_name
            sl=self.dset[name].value
            sl=sl.transpose()
            xgrid=self.dset['xval'].value
            ygrid=self.dset['yval'].value
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                for i in range(0,len(xgrid)):
                    xgrid[i]=math.log(xgrid[i],10)
            if self.logy==True:
                for i in range(0,len(ygrid)):
                    ygrid[i]=math.log(ygrid[i],10)
            if self.logz==1:
                for i in range(0,len(xgrid)):
                    for j in range(0,len(ygrid)):
                        sl[i][j]=math.log10(sl[i][h])
            lx=len(xgrid)
            ly=len(ygrid)
            plot.imshow(sl,interpolation='nearest',
                        origin='lower',
                        extent=[xgrid[0]-(xgrid[1]-xgrid[0])/2,
                                xgrid[lx-1]+(xgrid[lx-1]-xgrid[lx-2])/2,
                                ygrid[0]-(ygrid[1]-ygrid[0])/2,
                                ygrid[ly-1]+(ygrid[ly-1]-ygrid[ly-2])/2],
                        aspect='auto',**kwargs)
            if self.colbar==True:
                cbar=plot.colorbar()
                cbar.ax.tick_params(labelsize=self.font*0.8)
                
        else:
            print('Cannot density plot object of type',self.dtype)
        return

class o2graph_plotter(plot_base):
    """
    A plotting class for the o2graph script. This class is a child of the
    :py:class:`o2sclpy.plot_base` class.

    This class is not necessarily intended to be instantiated by the 
    end user.
    """

    def set_wrapper(self,o2scl_hdf,amp,args):
        """
        Wrapper for :py:func:`o2sclpy.plot_base.set` which sets
        plot-related parameters and sends other parameters to
        ``acol_manager``
        """

        match=False
        for line in param_list:
            if args[0]==line[0]:
                match=True
                
        if match==True:
            self.set(args[0],args[1])
            return
        
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

    def get_wrapper(self,o2scl_hdf,amp,args):
        """
        Wrapper for :py:func:`o2sclpy.plot_base.get` which
        gets plot-related parameters and gets other parameters
        from ``acol_manager``
        """
        match=False
        for line in param_list:
            if args[0]==line[0]:
                match=True
        
        if match==True:
            
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

    def gen(self,o2scl_hdf,amp,cmd_name,args):
        """
        Run a general ``acol`` command named ``cmd_name`` with arguments
        stored in ``args``.
        """

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

    def get_type(self,o2scl_hdf,amp):
        """
        Get the current O\ :sub:`2`\ scl object type
        """
        
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
        
    def den_plot(self,o2scl_hdf,amp,args):
        """
        Density plot from a ``table3d`` or ``hist_2d`` object
        """

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

            if self.logz==True:
                fail_found=False
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
                        if sl[i][j]>0.0:
                            sl[i][j]=math.log10(sl[i][j])
                        else:
                            if fail_found==False:
                                print('Failed to take log of',sl[i][j],
                                      'at (i,j)=(',j,',',i,') or (',
                                      xgrid[j],',',ygrid[i],
                                      '). Setting point to zero and',
                                      'suppressing future warnings.')
                            fail_found=True
                            sl[i][j]=0.0
                                
            if self.logx==True:
                xgrid=[math.log(ptrx[i],10) for i in
                       range(0,nx.value)]
            if self.logy==True:
                ygrid=[math.log(ptry[i],10) for i in
                       range(0,ny.value)]

            if self.zset==True:
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
                        if sl[i][j]>self.zhi:
                            sl[i][j]=self.zhi
                        elif sl[i][j]<self.zlo:
                            sl[i][j]=self.zlo

            if self.canvas_flag==False:
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

            if self.logx==True:
                xgrid=[math.log(ptrx[i],10) for i in
                       range(0,nx.value)]
            if self.logy==True:
                ygrid=[math.log(ptry[i],10) for i in
                       range(0,ny.value)]

            if self.zset==True:
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
                        if sl[i][j]>self.zhi:
                            sl[i][j]=self.zhi
                        elif sl[i][j]<self.zlo:
                            sl[i][j]=self.zlo
                            
            if self.logz==True:
                for i in range(0,ny.value):
                    for j in range(0,nx.value):
                        sl[i][j]=math.log10(sl[i][j])
                        
            if self.canvas_flag==False:
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

        if self.colbar==True:
            cbar=plot.colorbar()
            cbar.ax.tick_params(labelsize=self.font*0.8)

    def plot(self,o2scl_hdf,amp,args):
        """
        Plot a two-dimensional set of data
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

            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            coly=ctypes.c_char_p(self.force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]
        
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
    
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
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
                if self.logy==True:
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
        elif curr_type==b'prob_dens_mdim_amr':

            get_base_fn=o2scl_hdf.o2scl_acol_pdma_get_base
            get_base_fn.argtypes=[ctypes.c_void_p,int_ptr,
                                  int_ptr,double_ptr_ptr,double_ptr_ptr]
                            
            get_cube_fn=o2scl_hdf.o2scl_acol_pdma_get_cube
            get_cube_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,
                                  double_ptr_ptr,double_ptr_ptr,
                                  double_ptr,double_ptr]
                            
            ndimx=ctypes.c_int(0)
            nx=ctypes.c_int(0)
            lowx=double_ptr()
            highx=double_ptr()
            get_base_fn(amp,ctypes.byref(ndimx),ctypes.byref(nx),
                        ctypes.byref(lowx),ctypes.byref(highx))

            dimx=int(args[0])
            dimy=int(args[1])

            self.xlo=lowx[dimx]
            self.ylo=lowx[dimy]
            self.xset=True
            self.xhi=highx[dimx]
            self.yhi=highx[dimy]
            self.yset=True

            if self.canvas_flag==False:
                self.canvas()

            # Need to figure out here how to convert fill function
            # to a value, keeping in mind it can depend on
            # fvy.value (fractional volume) or wy.value (weight)
                
            fill_fn='None'
            if len(args)>=3:
                fill_fn=args[2]
                
            print('Fill function',fill_fn)
                
            for i in range(0,nx.value):

                iy=ctypes.c_int(i)
                lowy=double_ptr()
                highy=double_ptr()
                fvy=ctypes.c_double(0.0)
                wy=ctypes.c_double(0.0)
                get_cube_fn(amp,iy,ctypes.byref(lowy),
                            ctypes.byref(highy),
                            ctypes.byref(fvy),
                            ctypes.byref(wy))
                
                left=lowy[dimx]
                lower=lowy[dimy]
                right=highy[dimx]
                upper=highy[dimy]
                w=right-left
                h=upper-lower

                if len(args)<4:
                    r=patches.Rectangle((left,lower),w,h,0.0,
                                        alpha=fvy.value)
                    self.axes.add_patch(r)
                else:
                    strtemp='alpha='+str(fvy.value)+','+args[3]
                    r=patches.Rectangle((left,lower),w,h,0.0,
                                        **string_to_dict(strtemp))
                    self.axes.add_patch(r)
                            
            # End of section for 'prob_dens_mdim_amr' type
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

            if self.canvas_flag==False:
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
                
                if self.logx==True:
                    if self.logy==True:
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
                    if self.logy==True:
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
        
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
                                 
        # End of 'plot' function
                                 
    def rplot(self,o2scl_hdf,amp,args):
        """
        Plot a region inside a curve or in between two curves
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

            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx1=ctypes.c_char_p(self.force_bytes(args[0]))
            idx1=ctypes.c_int(0)
            ptrx1=double_ptr()
            get_ret=get_fn(amp,colx1,ctypes.byref(idx1),ctypes.byref(ptrx1))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            coly1=ctypes.c_char_p(self.force_bytes(args[1]))
            idy1=ctypes.c_int(0)
            ptry1=double_ptr()
            get_ret=get_fn(amp,coly1,ctypes.byref(idy1),ctypes.byref(ptry1))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx1[i] for i in range(0,idx1.value)]
                yv=[ptry1[i] for i in range(0,idy1.value)]
                
            if len(args)>3:
                colx2=ctypes.c_char_p(self.force_bytes(args[2]))
                idx2=ctypes.c_int(0)
                ptrx2=double_ptr()
                get_ret=get_fn(amp,colx2,ctypes.byref(idx2),ctypes.byref(ptrx2))
                if get_ret!=0:
                    print('Failed to get column named "'+args[2]+'".')
                    failed=True

                coly2=ctypes.c_char_p(self.force_bytes(args[3]))
                idy2=ctypes.c_int(0)
                ptry2=double_ptr()
                get_ret=get_fn(amp,coly2,ctypes.byref(idy2),ctypes.byref(ptry2))
                if get_ret!=0:
                    print('Failed to get column named "'+args[3]+'".')
                    failed=True

                if failed==False:
                    for i in range(0,idx2.value):
                        xv.append(ptrx2[idx2.value-1-i])
                        yv.append(ptry2[idy2.value-1-i])

            if failed==False:
                
                # Make sure the loop is closed
                xv.append(ptrx1[0])
                yv.append(ptry1[0])
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)==3:
                    plot.fill(xv,yv,**string_to_dict(args[2]))
                elif len(args)==5:
                    plot.fill(xv,yv,**string_to_dict(args[4]))
                else:
                    plot.fill(xv,yv)

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
            print("Command 'rplot' not supported for type",
                  curr_type,".")
            return
        
        # End of 'rplot' function
                                 
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

            pat_x=ctypes.c_char_p(self.force_bytes(args[1]))
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

            pat_y=ctypes.c_char_p(self.force_bytes(args[2]))
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

            pat_y=ctypes.c_char_p(self.force_bytes(args[1]))
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
                                 
    def scatter(self,o2scl_hdf,amp,args):
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

            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            coly=ctypes.c_char_p(self.force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]

            sv=[]
            cv=[]

            if (len(args)>2 and self.force_bytes(args[2])!=b'None' and
                self.force_bytes(args[2])!=b'none'):
                cols=ctypes.c_char_p(self.force_bytes(args[2]))
                ids=ctypes.c_int(0)
                ptrs=double_ptr()
                get_ret=get_fn(amp,cols,ctypes.byref(ids),ctypes.byref(ptrs))
                if get_ret!=0:
                    print('Failed to get column named "'+args[2]+'".')
                    failed=True
                else:
                    sv=[ptrs[i] for i in range(0,ids.value)]

            if (len(args)>3 and self.force_bytes(args[3])!=b'None' and
                self.force_bytes(args[3])!=b'none'):
                colc=ctypes.c_char_p(self.force_bytes(args[3]))
                idc=ctypes.c_int(0)
                ptrc=double_ptr()
                get_ret=get_fn(amp,colc,ctypes.byref(idc),ctypes.byref(ptrc))
                if get_ret!=0:
                    print('Failed to get column named "'+args[3]+'".')
                    failed=True
                else:
                    cv=[ptrc[i] for i in range(0,idc.value)]

            if failed==False:
                
                if self.canvas_flag==False:
                    self.canvas()
                if len(sv)>0:
                    if len(cv)>0:
                        if len(args)>4:
                            plot.scatter(xv,yv,s=sv,c=cv,
                                         **string_to_dict(args[4]))
                        else:
                            plot.scatter(xv,yv,s=sv,c=cv)
                    else:
                        if len(args)>4:
                            plot.scatter(xv,yv,s=sv,
                                         **string_to_dict(args[4]))
                        else:
                            plot.scatter(xv,yv,s=sv)
                else:
                    if len(cv)>0:
                        if len(args)>4:
                            plot.scatter(xv,yv,c=cv,
                                         **string_to_dict(args[4]))
                        else:
                            plot.scatter(xv,yv,c=cv)
                    else:
                        if len(args)>4:
                            plot.scatter(xv,yv,**string_to_dict(args[4]))
                        else:
                            plot.scatter(xv,yv)

                if self.logx==True:
                    self.axes.set_xscale('log')
                if self.logy==True:
                    self.axes.set_yscale('log')
                    
                if self.xset==True:
                    plot.xlim([self.xlo,self.xhi])
                if self.yset==True:
                    plot.ylim([self.ylo,self.yhi])
                if self.colbar==True and len(cv)>0:
                    cbar=plot.colorbar()
                    cbar.ax.tick_params(labelsize=self.font*0.8)
                    
            # End of section for 'table' type
        else:
            print("Command 'scatter' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
                                 
        # End of 'scatter' function
                                 
    def histplot(self,o2scl_hdf,amp,args):
        """
        Plot a histogram
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
                            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            failed=False
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)<2:
                    plot.hist(xv)
                else:
                    plot.hist(xv,**string_to_dict(args[1]))
                
            # End of section for 'table' type
        else:
            print("Command 'histplot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
                                 
        # End of 'histplot' function
                                 
    def hist2dplot(self,o2scl_hdf,amp,args):
        """
        Plot a two-dimensional histogram
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
                            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            failed=False

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True
            
            coly=ctypes.c_char_p(self.force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_ret=get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            if get_ret!=0:
                print('Failed to get column named "'+args[1]+'".')
                failed=True

            if failed==False:
                xv=[ptrx[i] for i in range(0,idx.value)]
                yv=[ptry[i] for i in range(0,idy.value)]
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)<3:
                    plot.hist2d(xv,yv)
                else:
                    plot.hist2d(xv,yv,**string_to_dict(args[2]))
                
            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
                                 
        # End of 'plot' function
                                 
    def errorbar(self,o2scl_hdf,amp,args):
        """
        Create a plot with error bars
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
                            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            xv=[ptrx[i] for i in range(0,idx.value)]

            coly=ctypes.c_char_p(self.force_bytes(args[1]))
            idy=ctypes.c_int(0)
            ptry=double_ptr()
            get_fn(amp,coly,ctypes.byref(idy),ctypes.byref(ptry))
            yv=[ptry[i] for i in range(0,idy.value)]

            if args[2]=='0':
                xerrv=[0.0 for i in range(0,idx.value)]
            else:
                colxerr=ctypes.c_char_p(self.force_bytes(args[2]))
                idxerr=ctypes.c_int(0)
                ptrxerr=double_ptr()
                get_fn(amp,colxerr,ctypes.byref(idxerr),ctypes.byref(ptrxerr))
                xerrv=[ptrxerr[i] for i in range(0,idxerr.value)]
    
            if args[3]=='0':
                yerrv=[0.0 for i in range(0,idy.value)]
            else:
                colyerr=ctypes.c_char_p(self.force_bytes(args[3]))
                idyerr=ctypes.c_int(0)
                ptryerr=double_ptr()
                get_fn(amp,colyerr,ctypes.byref(idyerr),ctypes.byref(ptryerr))
                yerrv=[ptryerr[i] for i in range(0,idyerr.value)]

            if self.canvas_flag==False:
                self.canvas()
            if len(args)<5:
                plot.errorbar(xv,yv,yerr=yerrv,xerr=xerrv)
            else:
                plot.errorbar(xv,yv,yerr=yerrv,xerr=xerrv,
                              **string_to_dict(args[4]))

            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            plot.xlim([self.xlo,self.xhi])
        if self.yset==True:
            plot.ylim([self.ylo,self.yhi])
                                 
        # End of 'errorbar' function
                                 
    def plot1(self,o2scl_hdf,amp,args):
        """
        Plot data versus an integer x axis
        """

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
                        
        if curr_type==b'table':
            
            get_fn=o2scl_hdf.o2scl_acol_get_column
            get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                             int_ptr,double_ptr_ptr]
            get_fn.restype=ctypes.c_int

            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),ctypes.byref(ptrx))
            failed=False
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            if failed==False:
                xv=[i for i in range(0,idx.value)]
                yv=[ptrx[i] for i in range(0,idx.value)]
        
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
                    
        elif (curr_type==b'double[]' or curr_type==b'int[]' or
              curr_type==b'size_t[]'):

            get_fn=o2scl_hdf.o2scl_acol_get_double_arr
            get_fn.argtypes=[ctypes.c_void_p,int_ptr,double_ptr_ptr]
                            
            id=ctypes.c_int(0)
            ptr=double_ptr()
            get_fn(amp,ctypes.byref(id),ctypes.byref(ptr))
            
            xv=[i for i in range(0,id.value)]
            yv=[ptr[i] for i in range(0,id.value)]

            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
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
                if self.logy==True:
                    if len(args)<1:
                        plot.semilogy(xv,yv)
                    else:
                        plot.semilogy(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        plot.plot(xv,yv)
                    else:
                        plot.plot(xv,yv,**string_to_dict(args[0]))
                            
            if self.xset==True:
                plot.xlim([self.xlo,self.xhi])
            if self.yset==True:
                plot.ylim([self.ylo,self.yhi])
                    
        # End of 'plot1' function
            
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
            ccp=ctypes.c_char_p(self.force_bytes(str_args))
            sizes=size_type(5,len(self.plotfiles[ifile]))
            parse_fn(amp,2,sizes,ccp)

            failed=False

            # Get the x column
            colx=ctypes.c_char_p(self.force_bytes(args[0]))
            idx=ctypes.c_int(0)
            ptrx=double_ptr()
            get_ret=get_fn(amp,colx,ctypes.byref(idx),
                           ctypes.byref(ptrx))
            if get_ret!=0:
                print('Failed to get column named "'+args[0]+'".')
                failed=True

            # Get the y column
            coly=ctypes.c_char_p(self.force_bytes(args[1]))
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

    def print_param_docs(self):
        # I don't know why this doesn't work right now
        # print(plot_base.logz.__doc__)
        print('O2graph parameter list:')
        print(' ')
        for line in param_list:
            if line[0]=='colbar':
                print(line[0]+' '+str(self.colbar))
            elif line[0]=='fig-size-x':
                print(line[0]+' '+str(self.fig_size_x))
            else:
                print(line[0])
            print(' '+line[1])
            print(' ')
        
    def parse_argv(self,argv,o2scl_hdf):
        """
        Parse command-line arguments.

        This is the main function used by the 
        :ref:`O2graph script`
        """

        # Create an acol_manager object and get the pointer
        o2scl_hdf.o2scl_create_acol_manager.restype=ctypes.c_void_p
        amp=o2scl_hdf.o2scl_create_acol_manager()

        names_fn=o2scl_hdf.o2scl_acol_set_names
        names_fn.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p,
                           ctypes.c_int,ctypes.c_char_p,ctypes.c_int,
                           ctypes.c_char_p]

        # Get current type
        cmd_name=b'o2graph'
        cmd_desc=(b'o2graph: A data viewing and '+
                  b'processing program for O2scl.\n')
        env_var=b'O2GRAPH_DEFAULTS'
        names_fn(amp,len(cmd_name),ctypes.c_char_p(cmd_name),
                 len(cmd_desc),ctypes.c_char_p(cmd_desc),
                 len(env_var),ctypes.c_char_p(env_var))
        
        if len(argv)<=1:
            done_flag=False
            readline.parse_and_bind('tab: complete')
            readline.parse_and_bind('set editing-mode emacs')
            while done_flag==False:
                line=input('o2graph> ')
                if line[0:4]=='quit' or line[0:4]=='exit':
                    done_flag=True
                else:
                    strlist=line.split(' ')
                    strlist[0]='-'+strlist[0]
                    self.parse_string_list(strlist,o2scl_hdf,amp)
        else:
            strlist=[str(argv[i]) for i in range(1,len(argv))]
            if self.verbose>2:
                print('Number of arguments:',len(strlist),'arguments.')
                print('Argument List:',strlist)
            self.parse_string_list(strlist,o2scl_hdf,amp)

        # End of function parse_argv
        return
            
    def parse_string_list(self,strlist,o2scl_hdf,amp):
        """
        Parse a list of strings

        This is the main function called by parse_argv
        """
        if self.verbose>2:
            print('In parse_string_list()',strlist)
        
        ix=0
        while ix<len(strlist):
            
            if self.verbose>2:
                print('Processing index',ix,'with value',strlist[ix],'.')
            # Find first option, at index ix
            initial_ix_done=0
            while initial_ix_done==0:
                if ix==len(strlist):
                    initial_ix_done=1
                elif strlist[ix][0]=='-':
                    initial_ix_done=1
                else:
                    if self.verbose>2:
                         print('Incrementing ix')
                    ix=ix+1
                    
            # If there is an option, then ix is its index
            if ix<len(strlist):
                
                cmd_name=strlist[ix][1:]
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
                    if ix_next==len(strlist):
                        ix_next_done=1
                    elif len(strlist[ix_next])>0 and strlist[ix_next][0]=='-':
                        ix_next_done=1
                    else:
                        if self.verbose>2:
                            print('Incrementing ix_next')
                        ix_next=ix_next+1

                # List of 'acol' commands for option processing loop
                acol_list=['a','alias','assign','autocorr','c',
                           'calc','cat','commands','contours','convert-unit',
                           'convert_unit','create','d','D',
                           'delete-col','delete-rows','delete-rows-tol',
                           'delete_col','delete_rows','delete_rows_tol',
                           'deriv','deriv2',
                           'download','entry','f','filelist','find-row',
                           'find_row','fit','function','g','gen3-list',
                           'gen3_list','generic','get-conv','get-row',
                           'get-unit','get_conv','get_row','get_unit',
                           'h','help','i','I','index','insert','insert-full',
                           'insert_full','integ','internal','interp',
                           'interp-type','interp_type','l','license','list',
                           'max','min','N','nlines','o','output','P',
                           'preview','q',
                           'r','read','rename','run',
                           's','S','select','select-rows',
                           'select_rows','select-rows2','select_rows2',
                           'set-data','set_data','set-unit',
                           'set_unit','show-units','show_units','slice',
                           'sort','stats','sum','to-hist','to_hist',
                           'to-hist-2d' 'to_hist_2d',
                           'to_table3d','to-table','to_table','to-table3d',
                           'type','v','warranty']
                
                # Now process the option
                if cmd_name=='set':

                    if self.verbose>2:
                        print('Process set.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for set option.')
                    else:
                        self.set_wrapper(o2scl_hdf,amp,strlist[ix+1:ix_next])
                        
                elif cmd_name=='get':
                    
                    if self.verbose>2:
                        print('Process get.')
                        
                    if ix_next-ix<2:
                        self.get('No parameter specified to get.')
                    else:
                        self.get_wrapper(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='commands':
                    
                    if self.verbose>2:
                        print('Process commands.')
                        
                    self.gen(o2scl_hdf,amp,cmd_name,
                             strlist[ix+1:ix_next])

                    if (ix_next-ix)==2:
                        
                        curr_type=strlist[ix+1]
                        
                    else:

                        # Get current type
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

                    print('O2graph commands for type '+
                          str(curr_type)+':\n')
                    strout=''
                    for line in base_list:
                        strout+=line[0]+' '
                    for line in extra_list:
                        if (curr_type==line[0] or
                            curr_type==self.force_bytes(line[0])):
                            strout+=line[1]+' '
                    str_list=textwrap.wrap(strout,79)
                    for i in range (0,len(str_list)):
                        print(str_list[i])
                            
                elif cmd_name=='help':
                    
                    if self.verbose>2:
                        print('Process help.')

                    curr_type=''
                    cmd=''

                    # If only a command is specified
                    if (ix_next-ix)==2:

                        # Get current type
                        int_ptr=ctypes.POINTER(ctypes.c_int)
                        char_ptr=ctypes.POINTER(ctypes.c_char)
                        char_ptr_ptr=ctypes.POINTER(char_ptr)

                        # Set up wrapper for type function
                        type_fn=o2scl_hdf.o2scl_acol_get_type
                        type_fn.argtypes=[ctypes.c_void_p,int_ptr,
                                          char_ptr_ptr]

                        # Get current type
                        it=ctypes.c_int(0)
                        type_ptr=char_ptr()
                        type_fn(amp,ctypes.byref(it),ctypes.byref(type_ptr))
                
                        curr_type=b''
                        for i in range(0,it.value):
                            curr_type=curr_type+type_ptr[i]
                            
                        cmd=strlist[ix+1]

                    elif (ix_next-ix)==3:
                        # If both a type and command are specified
                        
                        curr_type=strlist[ix+1]
                        cmd=strlist[ix+2]

                    # See if we matched an o2graph command
                    match=False
                    
                    # Handle the case of an o2graph command from the
                    # base list
                    for line in base_list:
                        if cmd==line[0]:
                            match=True
                            print('Usage: '+cmd+' '+line[2]+'\n\n'+
                                  line[1]+'\n')
                            str_list=textwrap.wrap(line[3],79)
                            for i in range (0,len(str_list)):
                                print(str_list[i])
                                
                    # Handle the case of an o2graph command from the
                    # extra list
                    for line in extra_list:
                        if ((curr_type==line[0] or
                             curr_type==self.force_bytes(line[0])) and
                            cmd==line[1]):
                            match=True
                            print('Usage: '+cmd+' '+line[3]+'\n\n'+
                                  line[2]+'\n')
                            str_list=textwrap.wrap(line[4],79)
                            for i in range (0,len(str_list)):
                                print(str_list[i])

                    # Handle the case of an acol command 
                    if match==False:
                        self.gen(o2scl_hdf,amp,cmd_name,
                                 strlist[ix+1:ix_next])

                    # If the user specified 'help set', then print
                    # the o2graph parameter documentation
                    if (cmd=='set' or cmd=='get') and (ix_next-ix)==2:
                        self.print_param_docs()

                    # If no arguments were given, then give a list of
                    # o2graph commands in addition to acol commands
                    if (ix_next-ix)==1:
                        print('O2graph command-line options:\n')
                        for line in base_list:
                            strt='  -'+line[0]
                            while len(strt)<16:
                                strt=strt+' '
                            strt+=line[1]
                            print(strt)

                elif cmd_name=='version':
                    
                    print('o2graph: A data table plotting and',
                          'processing program for O2scl.')
                    print(' Version '+version+'.')

#                elif cmd_name in acol_list:
#                    
#                    if self.verbose>2:
#                        print('Process '+cmd_name+'.')
#
#                    self.gen(o2scl_hdf,amp,cmd_name,strlist[ix+1:ix_next])

                elif cmd_name=='plot':
                    
                    if self.verbose>2:
                        print('Process plot.')

                    self.plot(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='rplot':
                    
                    if self.verbose>2:
                        print('Process rplot.')

                    self.rplot(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='plot-ser' or cmd_name=='plot_ser':
                    
                    if self.verbose>2:
                        print('Process plot-ser.')

                    self.plot_ser(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='plot1-ser' or cmd_name=='plot1_ser':
                    
                    if self.verbose>2:
                        print('Process plot1-ser.')

                    self.plot1_ser(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='scatter':
                    
                    if self.verbose>2:
                        print('Process scatter.')

                    self.scatter(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='histplot':
                    
                    if self.verbose>2:
                        print('Process histplot.')

                    self.histplot(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='errorbar':
                    
                    if self.verbose>2:
                        print('Process errorbar.')

                    self.errorbar(o2scl_hdf,amp,strlist[ix+1:ix_next])

                elif cmd_name=='hist2dplot':
                    
                    if self.verbose>2:
                        print('Process hist2dplot.')
                        
                    self.hist2dplot(o2scl_hdf,amp,strlist[ix+1:ix_next])
                            
                elif cmd_name=='den-plot':
                    
                    if self.verbose>2:
                        print('Process den-plot.')

                    self.den_plot(o2scl_hdf,amp,strlist[ix+1:ix_next])
                
                elif cmd_name=='plot1':
                    
                    if self.verbose>2:
                        print('Process plot1.')
                        
                    self.plot1(o2scl_hdf,amp,strlist[ix+1:ix_next])
                            
                elif cmd_name=='plotm':
                    
                    if self.verbose>2:
                        print('Process plotm.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for plotm option.')
                    else:
                        self.plotm(o2scl_hdf,amp,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='plot1m':
                    
                    if self.verbose>2:
                        print('Process plot1m.')
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for plot1m option.')
                    else:
                        self.plot1m(o2scl_hdf,amp,strlist[ix+1:ix_next])
                        
                elif cmd_name=='text':
                    
                    if self.verbose>2:
                        print('Process text.')
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for text option.')
                    elif ix_next-ix<5:
                        self.text(strlist[ix+1],strlist[ix+2],strlist[ix+3])
                    else:
                        self.text(strlist[ix+1],strlist[ix+2],strlist[ix+3],
                                  **string_to_dict(strlist[ix+4]))
                        
                elif cmd_name=='plot-files':
                    
                    if self.verbose>2:
                        print('Process plot-files.')
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for plot-files option.')
                    else:
                        self.plotfiles=[strlist[i+1] for i in
                                       range(ix,ix_next-1)]
                        print('File list is',self.plotfiles)
                        
                elif cmd_name=='ttext':
                    
                    if self.verbose>2:
                        print('Process ttext.')
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for ttext option.')
                    elif ix_next-ix<5:
                        self.ttext(strlist[ix+1],strlist[ix+2],strlist[ix+3])
                    else:
                        self.ttext(strlist[ix+1],strlist[ix+2],strlist[ix+3],
                                   **string_to_dict(strlist[ix+4]))
                        
                elif cmd_name=='xlimits':
                    
                    if self.verbose>2:
                        print('Process xlimits.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for xlimits option.')
                    else:
                        self.xlimits(float(strlist[ix+1]),float(strlist[ix+2]))
                        
                elif cmd_name=='ylimits':
                    
                    if self.verbose>2:
                        print('Process ylimits.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for ylimits option.')
                    else:
                        self.ylimits(float(strlist[ix+1]),float(strlist[ix+2]))
                        
                elif cmd_name=='save':
                    if self.verbose>2:
                        
                        print('Process save.')
                    if ix_next-ix<2:
                        print('Not enough parameters for save option.')
                    else:
                        plot.savefig(strlist[ix+1])
                        
                elif cmd_name=='line':
                    
                    if self.verbose>2:
                        print('Process line.')
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for line option.')
                    elif ix_next-ix<6:
                        self.line(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4])
                    else:
                        self.line(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='point':
                    
                    if self.verbose>2:
                        print('Process point.')
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for point option.')
                    elif ix_next-ix<4:
                        self.point(strlist[ix+1],strlist[ix+2])
                    else:
                        self.point(strlist[ix+1],strlist[ix+2],
                                   **string_to_dict(strlist[ix+3]))
                        
                elif cmd_name=='rect':
                    
                    if self.verbose>2:
                        print('Process rect.')
                        
                    if ix_next-ix<6:
                        print('Not enough parameters for rect option.')
                    elif ix_next-ix<7:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  strlist[ix+5])
                    else:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  strlist[ix+5],
                                  **string_to_dict(strlist[ix+6]))
                        
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
                elif cmd_name=='clf':
                    if self.verbose>2:
                        print('Process clf.')
                    plot.clf()
                    self.canvas_flag=False
                elif cmd_name=='backend':
                    if self.verbose>2:
                        print('Process backend in __init__.py.')
                elif cmd_name=='new-cmaps':
                    if self.verbose>2:
                        print('Process reds2.')
                    self.new_cmaps()
#                elif (cmd_name!='backend' and cmd_name!='o2scl-cpplib' and
#                    cmd_name!='o2scl-libdir'):
#                    print('No option named',cmd_name)
                else:
                    if self.verbose>2:
                        print('Process acol command '+cmd_name+'.')
                    self.gen(o2scl_hdf,amp,cmd_name,strlist[ix+1:ix_next])
                    
                # Increment to the next option
                ix=ix_next
                
            if self.verbose>2:
                print('Going to next.')
                
        # End of function parse_string_list()
        return
    
