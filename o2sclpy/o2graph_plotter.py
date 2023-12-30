#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2023, Andrew W. Steiner
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
import math
import sys
import ctypes
import numpy
import os
import readline

# For wrapping help text
import textwrap

# For code.interact() in 'python' command
import code 

from o2sclpy.doc_data import cmaps, new_cmaps, extra_types
from o2sclpy.doc_data import acol_help_topics, version
from o2sclpy.doc_data import o2graph_help_topics, acol_types
from o2sclpy.utils import parse_arguments, string_to_dict, terminal_py
from o2sclpy.utils import force_bytes, default_plot, cross
from o2sclpy.utils import is_number, arrow, icosahedron
from o2sclpy.utils import length_without_colors, wrap_line, screenify_py
from o2sclpy.utils import string_equal_dash, latex_to_png
from o2sclpy.utils import force_string, remove_spaces
from o2sclpy.plot_base import plot_base
from o2sclpy.yt_plot_base import yt_plot_base
from o2sclpy.plot_info import marker_list, markers_plot, colors_near
from o2sclpy.plot_info import cmap_list_func, cmaps_plot, xkcd_colors_list
from o2sclpy.plot_info import colors_plot, color_list
from o2sclpy.doc_data import version
from o2sclpy.hdf import *
from o2sclpy.base import *
from o2sclpy.kde import *
from yt.visualization._commons import get_canvas

base_list=[
    ["addcbar",plot_base.addcbar.__doc__],
    ["arrow",plot_base.arrow.__doc__],
    ["backend",
     ("Documentation for backend\n\n"+
      "Select the matplotlib backend to use.\n\n"+
      "<backend>\n\n"+
      "This commend selects the matplotlib backend. "+
      "Typical values are 'Agg', 'TkAgg', 'WX', 'QTAgg', "+
      "and 'QT4Agg'. Use backend Agg to save the plot to a "+
      "file without opening a window. The backend can only "+
      "be changed once, i.e. if the backend command is "+
      "invoked more than once, then only the last invocation "+
      "will have any effect.")],
    ["canvas",plot_base.canvas.__doc__],
    ["clf","Documentation for clf\n\n"+
     "Clear the current figure.\n\n"+
     "(No arguments.)\n\n"+
     "Clear the current figure."],
    ["cmap",plot_base.cmap.__doc__],
    ["colors",plot_base.colors.__doc__],
    ["ellipse",plot_base.ellipse.__doc__],
    ["error-point",plot_base.error_point.__doc__],
    ["eval","Documentation for eval\n\n"+
     "Run the python eval() function.\n\n"+
     "<python code>\n\n"+
     "Take the python code given and execute it using eval(). "+
     "For example::\n\no2graph -eval \"print(numpy.pi)\""],
    ["exec","Documentation for exec\n\n"+
     "Run the python code specified in a file.\n\n"+
     "<filename>\n\n"+
     "Take the python code given and execute it using execfile()."],
    ["image","Documentation for image\n\n"+
     "Plot a png file in a matplotlib window.\n\n"+
     "<png file>\n\n"+
     "This command reads a png file, fills a plotting canvas "+
     "and then calls matplotlib.pyplot.show()."],
    ["inset",plot_base.inset.__doc__],
    ["kde-plot",0],
    ["kde-2d-plot",0],
    ["line",plot_base.line.__doc__],
    ["modax",plot_base.modax.__doc__],
    ["mp4",0],
    ["obj",0],
    ["gltf",0],
    ["o2scl-addl-libs",
     "Specify a list of list of additional libraries to load."],
    ["o2scl-cpp-lib",
     "Specify the location of the standard C++ library."],
    ["o2scl-lib-dir",
     "Specify the directory for the libo2scl shared library."],
    ["plotv",0],
    ["point",plot_base.point.__doc__],
    ["python","Begin an interactive python session."],
    ["rect",plot_base.rect.__doc__],
    ["save",
     "Documentation for save\n\n"+
     "Save the current plot in a file.\n\n"+
     "<filename>\n\n",
     "Save the current plot in a file similar "+
     "to plot.savefig(). The action of this command depends on "+
     "which backend was selected. File type depends on the "+
     "extension, typically either .png, .pdf, .eps, .jpg, .raw, "+
     ".svg, and .tif."],
    ["selax",plot_base.selax.__doc__],
    ["show",plot_base.show.__doc__],
    ["subadj","Documentation for subadj\n\n"+
     "Adjust spacing of subplots\n\n"+
     "<kwargs>\n\n"+
     "Adjust the spacing for subplots after using the 'subplots' "+
     "command. All arguments are keyword arguments. The kwargs "+
     "for 'subadj' are left, right, bottom, top, "+
     "wspace, and hspace. This command is a wrapper to the "+
     "pyplot.subplots_adjust() function. Note that, unlike the "+
     "margin settings for the fig_dict parameter, the values "+
     "'right' and 'top' are defined relative to the lower-left "+
     "corner, so a small right margin is 'right=0.99'. The "+
     "subplots_adjust() function requires right>left and "+
     "top>bottom."],
    ["subplots",plot_base.subplots.__doc__],
    ["td-axis","Documentation for td-axis\n\n"+
     "Create a 3D axis label (experimental).\n\n"+
     "<x label> <y label> <z label> [kwargs]\n\n"+
     "Full desc."],
    ["td-arrow","Documentation for td-arrow\n\n"+
     "Create a 3D arrow (experimental).\n\n"+
     "<x1> <y1> <z1> <x2> <y2> <z2> [kwargs]\n\n"+
     "Full desc."],
    ["td-den-plot","Documentation for td-den-plot\n\n"+
     "Create a 3D density plot (experimental).\n\n"+
     "<x label> <y label> <z label> [kwargs]\n\n"+
     "Full desc."],
    ["text",plot_base.text.__doc__],
    ["textbox",plot_base.textbox.__doc__],
    ["ttext",plot_base.ttext.__doc__],
    ["xlimits",plot_base.xlimits.__doc__],
    ["xtitle",plot_base.xtitle.__doc__],
    ["ylimits",plot_base.ylimits.__doc__],
    ["ytitle",plot_base.ytitle.__doc__],
    ["yt-ann",0],
    ["yt-arrow",yt_plot_base.yt_arrow.__doc__],
    ["yt-axis",yt_plot_base.yt_plot_axis.__doc__],
    ["yt-box",yt_plot_base.yt_box.__doc__],
    ["yt-line",yt_plot_base.yt_line.__doc__],
    ["yt-path",0],
    ["yt-render",0],
    ["yt-source-list","List yt sources"],
    ["yt-text",0],
    ["yt-tf",0],
    ["yt-xtitle",yt_plot_base.yt_xtitle.__doc__],
    ["yt-ytitle",yt_plot_base.yt_ytitle.__doc__],
    ["yt-ztitle",yt_plot_base.yt_ztitle.__doc__],
    ["zlimits",plot_base.zlimits.__doc__]
]

extra_list=[
    ["double[]","plot1",0],
    ["hist","hist-plot",0],
    ["hist","plot",0],
    ["hist_2d","den-plot",0],
    ["int[]","plot1",0],
    ["prob_dens_mdim_amr","plot",0],
    ["size_t[]","plot1",0],
    ["table","errorbar",0],
    ["table","hist-plot",0],
    ["table","hist2d-plot",0],
    ["table","plot",0],
    ["table","to-kde",0],
    ["table","plot1",0],
    ["table","plot-color",0],
    ["table","rplot",0],
    ["table","scatter",0],
    ["table","yt-scatter",0],
    ["table","yt-vertex-list",0],
    ["table3d","den-plot",0],
    ["table3d","den-plot-rgb",0],
    ["table3d","make-png",0],
    ["tensor","den-plot",0],
    ["tensor<int>","den-plot",0],
    ["tensor<size_t>","den-plot",0],
    ["tensor_grid","den-plot",0],
    ["tensor_grid","den-plot-anim",0],
    ["tensor_grid","yt-add-vol",0],
    ["vector<contour_line>","plot",0],
    ["vec_vec_double","plot",0],
]

param_list=[
    ["colbar","If true, den-plot adds a color legend (default False)."],
    ["editor","If true, open the plot editor."],
    ["fig_dict",("Dictionary for figure properties. The default value is "+
                 "blank and implies ('fig_size_x=6.0, fig_size_y=6.0, "+
                 "ticks_in=False, "+
                 "rt_ticks=False, left_margin=0.14, right_margin=0.04, "+
                 "bottom_margin=0.12, top_margin=0.04, fontsize=16'). "+
                 "The x and y sizes of the figure object are in "+
                 "fig_size_x and fig_size_y. The value ticks_in refers "+
                 "to whether or not the ticks are inside or outside the "+
                 "plot. The value of rt_ticks refers to whether or not "+
                 "tick marks are plotted on the right and top sides of "+
                 "the plot. If the font size is unspecified, then "+
                 "the 'font' setting is used. "+
                 "The font size parameter is multiplied by 0.8 "+
                 "and then used for the axis labels. Note that this "+
                 "value must be set before the plotting canvas is"+
                 "created (which is done by 'subplots' or automatically "+
                 "when the first object is added to the plot) in order "+
                 "to have any effect.")],
    ["font","Font scaling for text objects (default 16)."],
    ["logx","If true, use a logarithmic x-axis (default False)."],
    ["logy","If true, use a logarithmic y-axis (default False)."],
    ["logz","If true, use a logarithmic z-axis (default False)."],
    ["usetex","If true, use LaTeX for text rendering (default True)."],
    ["verbose","Verbosity parameter (default 1)."],
    ["xhi","Upper limit for x-axis (function if starts with '(')."],
    ["xlo","Lower limit for x-axis (function if starts with '(')."],
    ["xset","If true, x-axis limits have been set (default False)."],
    ["yhi","Upper limit for y-axis (function if starts with '(')."],
    ["ylo","Lower limit for y-axis (function if starts with '(')."],
    ["yset","If true, y-axis limits have been set (default False)."],
    ["zlo","Lower limit for z-axis (function if starts with '(')."],
    ["zhi","Upper limit for z-axis (function if starts with '(')."],
    ["zset","If true, z-axis limits have been set (default False)."]
]
"""
List of o2sclpy parameters

A list of 2-element entries, name and description
"""

yt_param_list=[
    ["yt_filter",("Filter for yt-generated images (default '')"+
                  "\n\nIf non-empty, must contain the "+
                  "strings '%i' for input file and '%o' for "+
                  "output file. A typical example is something like\n\n"+
                  "convert -contrast-stretch 0 %i %o\n\n"+
                  "which uses imagemagick to adjust the color curve.")],
    ["yt_focus",("The yt camera focus as a string. "+
                 "The string 'default' is equivalent "+
                 "to '[0.5,0.5,0.5] internal'. This string can be "+
                 "either in the "+
                 "'internal' or 'user' unit system.")],
    ["yt_path",("The yt animation path (default []), as list of "+
                "lists. The list contains instructions such as\n\n"+
                "['yaw',100,0.01]\n['zoom',100,2.0]\n...\n\n"+
                "where the first entry in each sublist is always a type "+
                "move, and the second entry in each sublist is always the "+
                "number of frames over which to complete the move.\n\n"+
                "Note that this variable is not set using -set or -get but "+
                "by the 'yt-path' command.")],
    ["yt_position",("The yt camera position as a string "+
                    "The string 'default' is equivalent "+
                    "to '[1.5,0.6,0.7] internal'. This string can be "+
                    "either in the 'internal' or 'user' unit system.")],
    ["yt_north",("The yt camera north vector string. "+
                 "The string 'default' is equivalent to "
                 "'[1.0,0.0,0.0]'. Always in the internal "+
                 "unit system.")],
    ["yt_width",("The yt camera width relative to the domain volume "+
                 "as a string. The string 'default' is equivalent to "+
                 "'[1.5,1.5,1.5]'. Always in the internal unit system.")],
    ["yt_resolution","The rendering resolution (default (512,512))."],
    ["yt_sigma_clip","Sigma clipping parameter (default 4.0)."]
]
"""
List of yt parameters for o2sclpy

A list of 2-element entries, name and description
"""

def doc_replacements(s,ter,amp,link,script=False):
    """
    Make some replacements from RST formatting to the terminal screen.

    This function is in ``o2graph_plotter.py``.
    """

    amt=acol_manager(link,amp)

    if script:
        s=(force_string(amt.get_exec_color())+s+
           force_string(amt.get_default_color()))
        return s
    
    # Replace commands in base_list
    for i in range(0,len(base_list)):
        s=s.replace('``'+base_list[i][0]+'``',
                    force_string(amt.get_command_color())+
                    base_list[i][0]+
                    force_string(amt.get_default_color()))
        
    # Replace commands in extra_list
    for i in range(0,len(extra_list)):
        s=s.replace('``'+extra_list[i][1]+'``',
                    force_string(amt.get_command_color())+
                    extra_list[i][1]+
                    force_string(amt.get_default_color()))
        
    s=s.replace('o2graph',
                (force_string(amt.get_exec_color())+'o2graph'+
                 force_string(amt.get_default_color())))
    s=s.replace('O2scl',
                (force_string(amt.get_exec_color())+'O₂scl'+
                 force_string(amt.get_default_color())))
        
    # Replace parameters in param_list
    for i in range(0,len(param_list)):
        s=s.replace('``'+param_list[i][0]+'``',
                    force_string(amt.get_param_color())+
                    param_list[i][0]+
                    force_string(amt.get_default_color()))

    # Replace yt_parameters in yt_param_list
    for i in range(0,len(yt_param_list)):
        s=s.replace('``'+yt_param_list[i][0]+'``',
                    force_string(amt.get_param_color())+
                    yt_param_list[i][0]+
                    force_string(amt.get_default_color()))

    # Replace yt_parameters in acol_types
    for i in range(0,len(acol_types)):
        s=s.replace('``'+acol_types[i]+'``',
                    force_string(amt.get_type_color())+
                    acol_types[i]+
                    force_string(amt.get_default_color()))

    # Decorate URLs
    if s.find('https://')!=-1:
        ix=s.find('https://')
        found=False
        j=ix
        while j!=len(s) and found==False:
            if s[j]==' ':
                found=True
            else:
                j=j+1
        if j==len(s):
            s=(s[0:ix]+force_string(amt.get_url_color())+
               s[ix:len(s)]+force_string(amt.get_default_color()))
        else:
            s=(s[0:ix]+force_string(amt.get_url_color())+
               s[ix:j]+force_string(amt.get_default_color())+
               s[j:len(s)])

    # For ``code`` formatting
    s=s.replace(' ``',' ')
    s=s.replace('`` ',' ')
    s=s.replace('``, ',', ')
    s=s.replace('``. ','. ')

    # Combine two spaces to one
    s=s.replace('  ',' ')

    # For :math:`` equations
    s=s.replace(' :math:`',' ')
    s=s.replace('` ',' ')
    s=s.replace('`.','.')
    s=s.replace('`',',')
                    
    return s

def o2scl_get_type(o2scl,amp,link):
    """
    Get the type of the current object stored in the acol_manager
    pointer and return as a bytes object.
    """

    amt=acol_manager(link,amp)
    return amt.get_type()

def reformat_python_docs(cmd,doc_str,amp,link,
                         return_short=False,verbose=0):
    """
    Reformat a python documentation string
    """
    
    amt=acol_manager(link,amp)
    
    reflist=doc_str.split('\n')
    
    for i in range(0,len(reflist)):
        reflist[i]=remove_spaces(reflist[i])
        if verbose>1:
            print(i,'x',reflist[i],'x')

    if len(reflist)<1:
        return

    if reflist[0]=='':
        if len(reflist)<2:
            return
        doc_str2=reflist[1]
        for i in range(2,len(reflist)):
            doc_str2=doc_str2+'\n'+reflist[i]
    else:
        doc_str2=reflist[0]
        for i in range(1,len(reflist)):
            doc_str2=doc_str2+'\n'+reflist[i]

    reflist2=doc_str2.split('\n\n')

    if False:
        for i in range(0,len(reflist2)):
            print(i,'x',reflist2[i],'x')
    
    ter=terminal_py()
    try:
        ncols=os.get_terminal_size().columns
    except:
        ncols=80

    short=''
    parm_desc=''
    long_help=''

    # The short description
    if len(reflist2)==1:
        short=reflist2[0].split('\n')[0]
    elif len(reflist2)>=2:
        short=reflist2[1]

    if return_short:
        return short

    # The parameter description
    if len(reflist2)>=3:
        parm_desc=reflist2[2].replace('\n',' ')

        parm_desc=parm_desc.replace('  ',' ')
        sx='Command-line arguments: ``'
        if parm_desc[0:len(sx)]==sx:
            parm_desc=parm_desc[len(sx):]
        if parm_desc[-2:]=='``':
            parm_desc=parm_desc[0:-2]
            
    print('Usage: '+force_string(amt.get_command_color())+cmd+
          force_string(amt.get_default_color())+' '+parm_desc)
    
    print('Short description:',short)

    if len(reflist2)>=4:
        print('')
        print('Long description:')
        last_pgh_colons=False
        for j in range(3,len(reflist2)):
            if len(reflist2[j])>0:
                if last_pgh_colons:
                    long_help=doc_replacements(reflist2[j].replace('\n',' '),
                                               ter,amp,link,script=True)
                    tmplist=long_help.split(' \\ ')
                else:
                    long_help=doc_replacements(reflist2[j].replace('\n',' '),
                                               ter,amp,link)
                    tmplist=wrap_line(long_help,ncols-1)
                if j!=3:
                    print('')
                for k in range(0,len(tmplist)):
                    if last_pgh_colons:
                        if k!=len(tmplist)-1:
                            print(' ',tmplist[k],'\\')
                        else:
                            print(' ',tmplist[k])
                    else:
                        print(tmplist[k])
                if long_help[-2:]=='::':
                    last_pgh_colons=True
                else:
                    last_pgh_colons=False
                    
    return

def reformat_python_docs_type(curr_type,cmd,doc_str,amp,link,
                              return_short=False,verbose=0):
    """
    Reformat a python documentation string
    """
    
    amt=acol_manager(link,amp)

    reflist=doc_str.split('\n')
    
    for i in range(0,len(reflist)):
        reflist[i]=remove_spaces(reflist[i])
        if verbose>1:
            print(i,'x',reflist[i],'x')

    if len(reflist)<1:
        return

    if reflist[0]=='':
        if len(reflist)<2:
            return
        doc_str2=reflist[1]
        for i in range(2,len(reflist)):
            doc_str2=doc_str2+'\n'+reflist[i]
    else:
        doc_str2=reflist[0]
        for i in range(1,len(reflist)):
            doc_str2=doc_str2+'\n'+reflist[i]

    reflist2=doc_str2.split('\n\n')

    sect_found=False
    jfound=0
    for j in range(0,len(reflist2)):
        if reflist2[j]==("For objects of type ``"+
                         force_string(curr_type)+"``:"):
            sect_found=True
            jfound=j+1

    if sect_found==False:
        print('Could not find documentation for type',curr_type,
              'and command',cmd)
        return

    strt="For objects of type"
    reflist3=[]
    jlast=len(reflist2)
    loop_done=False
    for j in range(jfound,jlast):
        if reflist2[j][0:len(strt)]==strt:
            jlast=j
            loop_done=True
        elif loop_done==False:
            reflist3.append(reflist2[j])

    if False:
        for j in range(0,len(reflist3)):
            print(j,'y',reflist3[j],'y')
            
    ter=terminal_py()
    ncols=os.get_terminal_size().columns

    short=''
    parm_desc=''
    long_help=''

    if len(reflist3)>0:
        short=reflist3[0]

    if return_short:
        return short

    if len(reflist3)>1:
        parm_desc=reflist3[1].replace('\n',' ')

        parm_desc=parm_desc.replace('  ',' ')
        sx='Command-line arguments: ``'
        if parm_desc[0:len(sx)]==sx:
            parm_desc=parm_desc[len(sx):]
        if parm_desc[-2:]=='``':
            parm_desc=parm_desc[0:-2]
            
    print('Usage for type '+
          force_string(amt.get_type_color())+curr_type+
          force_string(amt.get_default_color())+': '+
          force_string(amt.get_command_color())+cmd+
          force_string(amt.get_default_color())+' '+parm_desc)
    
    print('Short description:',short)

    if len(reflist3)>2:
        print('')
        print('Long description:')
        last_pgh_colons=False
        for j in range(2,len(reflist3)):
            if len(reflist3[j])>0:
                if last_pgh_colons:
                    long_help=doc_replacements(reflist3[j].replace('\n',' '),
                                               ter,amp,link,script=True)
                    tmplist=long_help.split(' \ ')
                else:
                    long_help=doc_replacements(reflist3[j].replace('\n',' '),
                                               ter,amp,link)
                    tmplist=wrap_line(long_help,ncols-1)
                if j!=2:
                    print('')
                for k in range(0,len(tmplist)):
                    if last_pgh_colons:
                        if k!=len(tmplist)-1:
                            print(' ',tmplist[k],'\\')
                        else:
                            print(' ',tmplist[k])
                    else:
                        print(tmplist[k])
                if long_help[-2:]=='::':
                    last_pgh_colons=True
                else:
                    last_pgh_colons=False
                    
    return

def table_get_column(o2scl,amp,link,name,return_pointer=False):
    """
    Return a column from the current table object stored
    in the acol_manager object 'amp'
    """

    amt=acol_manager(link,amp)
    tab=amt.get_table_obj()
    col=tab[force_bytes(name)]

    return col

class material:
    """
    A simple material for a 3-d visualization
    """
    name: str
    """
    The name of the visualization
    """
    Ka: list[float]
    """
    The ambient color
    """
    Kd: list[float]
    """
    The diffuse color
    """
    Ks: list[float]
    """
    The specular color
    """
    Ns: float
    """
    The specular exponent
    """
    txt: str
    """
    The texture filename, including extension
    """

    def __init__(self, name: str, Ka: list[float]=[1,1,1], txt: str=''):
        """Create a new material with color in ``Ka`` and texture file in
        ``txt``.
        """
        self.name=name
        self.Ka=Ka
        self.Kd=Ka
        self.Ks=[0,0,0]
        self.Ns=0
        self.txt=txt
        return
    
class group_of_faces:
    """
    A group of (triangular) faces

    Right now, the faces either have 3, 4, 6, or 7 elements, corresponding
    to the cases
    * faces
    * faces plus material
    * faces plus texture coordinates
    * faces plus texture coordinates plus material
    """
    vert_list: list[list[float]]=[]
    """
    List of vertices
    """
    vn_list: list[list[float]]=[]
    """
    List of vertex normals
    """
    vt_list: list[list[float]]=[]
    """
    List of texture coordinates
    """
    faces: list[list[int | str]]
    """
    The list of faces
    """
    name: str=''
    """
    The name of the group.

    This string is used for the ``g `` commands in ``obj`` files. It 
    may be empty, in which case no ``g `` command is given. 
    """
    mat: str=''
    """The name of the material (blank for none, or for different material for
    each face)

    Note that this string might be nonempty even when some of the
    faces explicitly specify a material. In this case, this string
    specifies the default material to be used for those faces which do
    not specify their own material.

    If this string is non-empty, but all of the faces specify a 
    material, then the ``sort_by_mat()`` function will 
    """

    def __init__(self, name: str, faces: list[list[int | str]],
                 mat: str = ''):
        """
        Create a group given the specfied list of faces, name, and 
        material.
        """
        self.name=name
        self.faces=faces
        self.mat=mat
        return

    def sort_by_mat(self):
        """Sort the faces by material name, ensuring that the group and
        material commands do not have to be issued for each face.

        """

        # If no materials are specified in faces, there is nothing to do
        found_four=False
        for i in range(0,len(self.faces)):
            if len(self.faces[i])==4 or len(self.faces[i])==7:
                found_four=True
        print('group_of_faces::sort_by_mat(): found_four',found_four)
        if found_four==False:
            return

        # Find if there at least two distinct materials 
        two_mats=False
        for i in range(0,len(self.faces)):
            if (len(self.faces[i])==4 and
                self.faces[i][3]!=self.mat):
                two_mats=True
            if (i>0 and len(self.faces[i])==4 and
                len(self.faces[i-1])==4 and
                self.faces[i][3]!=self.faces[i-1][3]):
                two_mats=True

        # If there are not two distinct materials, there's nothing to do
        print('group_of_faces::sort_by_mat(): two_mats',two_mats)
        if two_mats==False:
            return

        # Reorganize faces by material name
        mat_list=[]
        faces2=[]

        # First, if a global material is specified, add all faces
        # which don't have a material and assume that they'll use the
        # global material.
        if self.mat!='':

            # This is true if self.mat has been added to 'mat_list'
            base_name_added=False
            for i in range(0,len(self.faces)):
                if len(self.faces[i])==3:
                    if base_name_added==False:
                        mat_list.append(self.mat)
                        base_name_added=True
                    faces2.append(self.faces[i])
                    
            if base_name_added==False:
                raise ValueError('In function sort_by_mat(): '+
                                 '  A material named '+self.mat+
                                 ' was specified in "mat", but no face '+
                                 'uses that material.')

        # Now go through the list and find faces not already added to
        # mat_list
        face_copies=[False for i in range(0,len(self.faces))]
        for i in range(0,len(self.faces)):
            if len(self.faces[i])==4:
                mat_name=self.faces[i][3]
                if mat_name not in mat_list:
                    print('group_of_faces::sort_by_mat():',
                          'At index',i,'adding faces for',mat_name)
                    mat_list.append(mat_name)
                    # If it's not found, then add the current face,
                    # and loop over the remaining faces which match
                    faces2.append(self.faces[i])
                    face_copies[i]=True
                    for j in range(i+1,len(self.faces)):
                        if self.faces[j][3]==mat_name:
                            faces2.append(self.faces[j])
                            face_copies[j]=True

        if len(self.faces)!=len(faces2):
            print('sort_by_mat():',len(self.faces),len(faces2))
            raise SyntaxError('The lists of faces do not match up in '+
                              'sort_by_mat().')
                 
        self.faces=faces2
        return

def latex_prism(x1,y1,z1,x2,y2,z2,latex,png_file,mat_name,
                dir='x',end_mat='white'):
    """
    Create a rectangular prism with textures from a png created by a
    LaTeX string on four sides.

    This function returns four objects: the vertices, the faces,
    the texture uv coordinates, and the material object

    The variable dir is either 'x', 'y', or 'z', depending
    on the orientation of the prism. For the 'x' direction,
    the xy and xz faces have textures from the LaTeX object,
    and the yz faces are set to the end material specified
    in ``end_mat``. The normal vectors for all six faces point
    outside the prism. 
    """

    w,h,w_new,h_new=latex_to_png(latex,png_file,power_two=True)
    face=[]
    vert=[]
    facet=[]
    text_uv=[]

    if dir=='x':
        xcent=(x1+x2)/2.0
        height=abs(y2-y1)
        width=w_new/h_new*height
        x1=xcent-width/2.0
        x2=xcent+width/2.0
    elif dir=='y':
        ycent=(y1+y2)/2.0
        height=abs(z2-z1)
        width=w_new/h_new*height
        y1=ycent-width/2.0
        y2=ycent+width/2.0
    else:
        zcent=(z1+z2)/2.0
        height=abs(x2-x1)
        width=w_new/h_new*height
        z1=zcent-width/2.0
        z2=zcent+width/2.0
        print(x1,y1,z1,x2,y2,z2)

    m=material(mat_name,txt=png_file)

    # Add the 8 vertices
    vert.append([x1,y1,z1])
    vert.append([x2,y1,z1])
    vert.append([x1,y2,z1])
    vert.append([x2,y2,z1])
    vert.append([x1,y1,z2])
    vert.append([x2,y1,z2])
    vert.append([x1,y2,z2])
    vert.append([x2,y2,z2])
    
    text_uv.append([0.0,float(h)/float(h_new)])
    text_uv.append([0.0,0.0])
    text_uv.append([float(w)/float(w_new),float(h)/float(h_new)])
    text_uv.append([float(w)/float(w_new),0.0])

    if dir=='x':
        
        # The four sides with labels
        face.append([1,5,2,2,1,4,mat_name])
        face.append([2,5,6,4,1,3,mat_name])
        face.append([8,7,4,4,2,3,mat_name])
        face.append([4,7,3,3,2,1,mat_name])
        face.append([1,2,3,1,3,2,mat_name])
        face.append([3,2,4,2,3,4,mat_name])
        face.append([5,7,6,2,1,4,mat_name])
        face.append([6,7,8,4,1,3,mat_name])
        
        # The two sides without labels
        face.append([2,6,4,end_mat])
        face.append([4,6,8,end_mat])
        face.append([1,3,5,end_mat])
        face.append([5,3,7,end_mat])
        
    elif dir=='y':
        
        # The four sides with labels
        face.append([3,1,4,4,2,3,mat_name])
        face.append([4,1,2,3,2,1,mat_name])
        face.append([6,5,8,2,1,4,mat_name])
        face.append([8,5,7,4,1,3,mat_name])
        face.append([4,2,8,4,2,3,mat_name])
        face.append([8,2,6,3,2,1,mat_name])
        face.append([5,1,7,2,1,4,mat_name])
        face.append([7,1,3,4,1,3,mat_name])
        
        # The two sides without labels
        face.append([3,4,7,end_mat])
        face.append([7,4,8,end_mat])
        face.append([1,5,2,end_mat])
        face.append([2,5,6,end_mat])
        
    else:
        
        # The four sides with labels
        face.append([4,8,3,1,3,2,mat_name])
        face.append([3,8,7,2,3,4,mat_name])
        face.append([2,1,6,2,1,4,mat_name])
        face.append([6,1,5,4,1,3,mat_name])
        
        face.append([8,4,6,4,2,3,mat_name])
        face.append([6,4,2,3,2,1,mat_name])
        face.append([1,3,5,2,1,4,mat_name])
        face.append([5,3,7,4,1,3,mat_name])
        
        # The two sides without labels
        face.append([1,2,3,end_mat])
        face.append([3,2,4,end_mat])
        face.append([5,7,6,end_mat])
        face.append([6,7,8,end_mat])
        
    # Rearrange for GLTF. to compute normals, we use the cross
    # products.

    norms=[[1.0,0.0,0.0],
           [-1.0,0.0,0.0],
           [0.0,1.0,0.0],
           [0.0,-1.0,0.0],
           [0.0,0.0,1.0],
           [0.0,0.0,-1.0]]
        
    vert2=[]
    txts=[]
    norms2=[]
    
    for i in range(0,len(face)):

        # Add the vertices to the new vertex array
        vert2.append(vert[face[i][0]-1])
        vert2.append(vert[face[i][1]-1])
        vert2.append(vert[face[i][2]-1])

        # Compute the norm
        p1=vert[face[i][0]-1]
        p2=vert[face[i][1]-1]
        p3=vert[face[i][2]-1]
        v1=[1]*3
        v2=[1]*3
        for j in range(0,3):
            v1[j]=p2[j]-p1[j]
            v2[j]=p3[j]-p2[j]
        norm=cross(v1,v2,norm=True)
        for k in range(0,3):
            norms2.append([norm[0],norm[1],norm[2]])

        if len(face[i])>=7:
            # Texture coordinates in the case of a image
            txts.append([text_uv[face[i][3]-1][0],
                         text_uv[face[i][3]-1][1]])
            txts.append([text_uv[face[i][4]-1][0],
                         text_uv[face[i][4]-1][1]])
            txts.append([text_uv[face[i][5]-1][0],
                         text_uv[face[i][5]-1][1]])
            face[i]=[i*3,i*3+1,i*3+2,face[i][6]]
        else:
            # Default texture coordinates for no image
            txts.append([text_uv[3][0],
                         text_uv[3][1]])
            txts.append([text_uv[0][0],
                         text_uv[0][1]])
            txts.append([text_uv[1][0],
                         text_uv[1][1]])
            face[i]=[i*3,i*3+1,i*3+2,face[i][3]]

    # Print out results
    if True:
        for ki in range(0,len(vert2),3):
            print('%d [%d,%d,%d] mat: %s' % (int(ki/3),face[int(ki/3)][0],
                                             face[int(ki/3)][1],
                                             face[int(ki/3)][2],
                                             face[int(ki/3)][3]))
            print(('0 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki][0],vert2[ki][1],
                                             vert2[ki][2],txts[ki][0],
                                             txts[ki][1],norms2[ki][0],
                                             norms2[ki][1],norms2[ki][2]))
            print(('1 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+1][0],vert2[ki+1][1],
                                             vert2[ki+1][2],txts[ki+1][0],
                                             txts[ki+1][1],norms2[ki+1][0],
                                             norms2[ki+1][1],norms2[ki+1][2]))
            print(('2 [%7.6e,%7.6e,%7.6e] [%7.6e,%7.6e] '+
                   '[%7.6e,%7.6e,%7.6e]') % (vert2[ki+2][0],vert2[ki+2][1],
                                             vert2[ki+2][2],txts[ki+2][0],
                                             txts[ki+2][1],norms2[ki+2][0],
                                             norms2[ki+2][1],norms2[ki+2][2]))
            print('')
            
        #quit()

    return vert2,face,txts,norms2,m
            
class threed_objects:
    """A set of three-dimensional objects
    """
    
    gf_list: list[group_of_faces]=[]
    """
    List of groups of faces
    """
    mat_list: list[material]=[]
    """
    List of materials
    """

    def add_object(self, gf: group_of_faces):
        """Add an object given 'lv', a list of vertices, and 'gf', a group of
        triangular faces among those vertices.

        Optionally, also specify the vertex normals in ``normals``.
        """
        #normals : list[list[float]] = [],
        #texcoords : list[list[float]] = []):

        if len(gf.vn_list)>0 and len(gf.vn_list)!=len(gf.vert_list):
            raise ValueError('List of normals has size',len(normals),
                             'and list of vertices is of size',len(lv))
        
        if len(gf.vt_list)>0 and len(gf.vt_list)!=len(gf.vert_list):
            raise ValueError('List of texture coordinates has size',
                             len(gf.vt_list),
                             'and list of vertices is of size',
                             len(gf.vert_list))

        # Find the first empty vertex index
        len_lv=len(gf.vert_list)
        len_lvt=len(gf.vt_list)
        len_lvn=len(gf.vn_list)

        # Iterate over each face
        print('threed_object::add_object():',
              'Adjust faces for group',gf.name,'and check.')
        
        for i in range(0,len(gf.faces)):

            # Check to make sure we don't have OBJ indices in
            # GLTF mode
            if len(gf.faces[i])>4:
                raise ValueError('Face '+str(i)+' has more than 4 '+
                                 'elements.')
            
            # Check if there is an undefined material in this face
            if len(gf.faces[i])==4:
                mat_found=False
                mat_tmp=gf.faces[i][3]
                for k in range(0,len(self.mat_list)):
                    if self.mat_list[k].name==mat_tmp:
                        mat_found=True
                if mat_found==False:
                    raise ValueError('Face '+str(i)+' refers to a '+
                                     'material "'+mat_tmp+
                                     '" which is not in the list of '+
                                     'materials.')
                    
        # Check if there is an undefined material in the
        # group_of_faces data member 'mat'
        if gf.mat!='':
            mat_found=False
            for k in range(0,len(self.mat_list)):
                if self.mat_list[k].name==gf.mat:
                    mat_found=True
            if mat_found==False:
                raise ValueError('The group of faces names a material '+
                                 gf.mat+' which is not in the list of '+
                                 'materials.')

        # Sort the group of vertices by material for output later
        print('threed_object::add_object(): Sort group named',
              gf.name,'by material.')
        gf.sort_by_mat()
                
        # Add the group of faces to the list
        self.gf_list.append(gf)
        
        return

    def add_mat(self, m: material):
        # Add the material if not found
        mat_found=False
        for i in range(0,len(self.mat_list)):
            if self.mat_list[i].name==m.name:
                mat_found=True
        if mat_found==False:
            self.mat_list.append(m)
        return
    
    def add_object_mat(self, gf: group_of_faces, m: material):
        """Add an object given 'lv', a list of vertices, and 'gf', a group of
        triangular faces among those vertices, and 'm', the material
        for all of the faces.

        """
        self.add_mat(m)
        if gf.mat=='':
            gf.mat=m.name
        self.add_object(gf)
        return

    def is_mat(self, m: str):
        """Return true if a a material named ``m`` has been added
        """
        for i in range(0,len(self.mat_list)):
            if self.mat_list[i].name==m:
                return True
        return False
    
    def add_object_mat_list(self, gf: group_of_faces, lm: list[material]):
        """Add an object given 'lv', a list of vertices, and 'gf', a group of
        triangular faces among those vertices, and 'm', the material
        for all of the faces.
        """
        
        for k in range(0,len(lm)):
            self.add_mat(lm[k])
        self.add_object(gf)
        return

    def write_obj_old(self, prefix: str):
        """Write all objects to an '.obj' file, creating a '.mtl' file if
        necessary

        (This function doesn't work anymore.)
        """
        quit()

        # Remove suffix if it is present
        if prefix[-4:]=='.obj':
            prefix=prefix[:-4]
        obj_file=prefix+'.obj'
        mtl_file=prefix+'.mtl'
        
        f=open(obj_file,'w')
        if len(self.mat_list)>0:
            f.write('mtllib '+mtl_file+'\n')

        # Add vertices
        for k in range(0,len(self.vert_list)):
            f.write('v '+
                    ('%7.6e' % self.vert_list[k][0])+' '+
                    ('%7.6e' % self.vert_list[k][1])+' '+
                    ('%7.6e' % self.vert_list[k][2])+'\n')

        # Add vertices
        for k in range(0,len(self.vt_list)):
            print(k,self.vt_list[k])
            f.write('vt '+
                    ('%7.6e' % self.vt_list[k][0])+' '+
                    ('%7.6e' % self.vt_list[k][1])+'\n')

        # Add each set of faces as a group
        for i in range(0,len(self.gf_list)):
            if self.gf_list[i].name!='':
                f.write('g '+self.gf_list[i].name+'\n')
            # If the base material is used, output that first
            if (self.gf_list[i].mat!='' and
                len(self.gf_list[i].faces[0])==3):
                f.write('usemtl '+self.gf_list[i].mat+'\n')
            if (self.gf_list[i].mat!='' and
                len(self.gf_list[i].faces[0])==6):
                f.write('usemtl '+self.gf_list[i].mat+'\n')
            for k in range(0,len(self.gf_list[i].faces)):
                # Take care of the cases when we need to change materials
                if k==0 and len(self.gf_list[i].faces[k])==4:
                    f.write('usemtl '+self.gf_list[i].faces[k][3]+'\n')
                elif k==0 and len(self.gf_list[i].faces[k])==7:
                    f.write('usemtl '+self.gf_list[i].faces[k][6]+'\n')
                elif (len(self.gf_list[i].faces[k-1])==3 and 
                      len(self.gf_list[i].faces[k])==4):
                    f.write('usemtl '+self.gf_list[i].faces[k][3]+'\n')
                elif (len(self.gf_list[i].faces[k-1])==3 and 
                      len(self.gf_list[i].faces[k])==7):
                    f.write('usemtl '+self.gf_list[i].faces[k][6]+'\n')
                elif (len(self.gf_list[i].faces[k-1])==4 and 
                    len(self.gf_list[i].faces[k])>=4 and
                    self.gf_list[i].faces[k-1][3]!=
                    self.gf_list[i].faces[k][3]):
                    f.write('usemtl '+self.gf_list[i].faces[k][3]+'\n')
                if len(self.gf_list[i].faces[k])>=6:
                    # Write the face with vertex texture indices
                    f.write('f '+
                            ('%i' % self.gf_list[i].faces[k][0])+'/'+
                            ('%i' % self.gf_list[i].faces[k][3])+' '+
                            ('%i' % self.gf_list[i].faces[k][1])+'/'+
                            ('%i' % self.gf_list[i].faces[k][4])+' '+
                            ('%i' % self.gf_list[i].faces[k][2])+'/'+
                            ('%i' % self.gf_list[i].faces[k][5])+'\n')
                    # Check that the texture index
                    # refers to a valid texture coordinate
                    for j in range(3,6):
                        if self.gf_list[i].faces[k][j]-1>=len(self.vt_list):
                            print('Problem with vertex',j,'of face',k+1,
                                  'in group',i)
                else:
                    # Write the face
                    f.write('f '+
                            ('%i' % self.gf_list[i].faces[k][0])+' '+
                            ('%i' % self.gf_list[i].faces[k][1])+' '+
                            ('%i' % self.gf_list[i].faces[k][2])+'\n')
                # Check that the face refers to a valid vertex
                for j in range(0,3):
                    if self.gf_list[i].faces[k][j]-1>=len(self.vert_list):
                        print('Problem with vertex',j,'of face',k+1,
                              'in group',i)
        f.close()

        # Create the materials file
        if len(self.mat_list)>0:
            f=open(mtl_file,'w')
            for i in range(0,len(self.mat_list)):
                f.write('newmtl '+self.mat_list[i].name+'\n')
                f.write('Ka '+str(self.mat_list[i].Ka[0])+' '+
                        str(self.mat_list[i].Ka[1])+' '+
                        str(self.mat_list[i].Ka[2])+'\n')
                f.write('Kd '+str(self.mat_list[i].Kd[0])+' '+
                        str(self.mat_list[i].Kd[1])+' '+
                        str(self.mat_list[i].Kd[2])+'\n')
                f.write('Ks '+str(self.mat_list[i].Ks[0])+' '+
                        str(self.mat_list[i].Kd[1])+' '+
                        str(self.mat_list[i].Kd[2])+'\n')
                f.write('Ns '+str(self.mat_list[i].Ns)+'\n')
                if self.mat_list[i].txt!='':
                    f.write('map_Ka '+self.mat_list[i].txt+'\n')
                    f.write('map_Kd '+self.mat_list[i].txt+'\n')
            f.close()
                        
        return
        
    def write_gltf(self, prefix: str):
        """Write all objects to an '.gltf' file, creating a '.bin' file
        """

        import json
        from struct import pack
        
        # Remove suffix if it is present
        if prefix[-5:]=='.gltf':
            prefix=prefix[:-5]
        gltf_file=prefix+'.gltf'
        bin_file=prefix+'.bin'
        
        nodes_list=[]
            
        for k in range(0,len(self.gf_list)):
            nodes_list.append(k)
                
        jdat={"asset": {"generator": "o2sclpy v"+version,
                        "version": "2.0"},
              "scene": 0,
              "scenes": [{ "name": "Scene",
                           "nodes": nodes_list
                          }]
              }
            
        nodes_list=[]
        for k in range(0,len(self.gf_list)):
            nodes_list.append({"mesh" : k,
                               "name" : self.gf_list[k].name})
            #"rotation" : [0,0,0,0]})
        jdat["nodes"]=nodes_list
    
        mesh_list=[]
        acc_list=[]
        buf_list=[]
        mat_json=[]
        txt_list=[]
        img_list=[]
            
        f2=open(bin_file,'wb')
            
        texture_map=[-1]*len(self.mat_list)
        texture_index=0
        
        for i in range(0,len(self.mat_list)):

            this_mat=self.mat_list[i]

            if this_mat.txt!='':
                mat_json.append({"doubleSided": True,
                                 "name": this_mat.name,
                                 "pbrMetallicRoughness": {
                                     "baseColorTexture": {
                                         "index":
                                         texture_index
                                         },
                                     "metallicFactor": 0
                                 }
                                 })
                txt_list.append({"source": texture_index})
                img_list.append({"mimeType": "image/png",
                                 "name": this_mat.name,
                                 "uri": this_mat.txt})
                texture_map[i]=texture_index
                texture_index=texture_index+1
            else:
                mat_json.append({"doubleSided": True,
                                 "name": this_mat.name,
                                 "pbrMetallicRoughness": {
                                     "baseColorFactor": [
                                         this_mat.Ka[0],
                                         this_mat.Ka[1],
                                         this_mat.Ka[2],
                                         1],
                                     "metallicFactor": 0
                                 }
                                 })
        
        # Add each set of faces as a group
        acc_index=0
        offset=0

        for i in range(0,len(self.gf_list)):
                
            normals=False
            if len(self.gf_list[i].vn_list)==len(self.gf_list[i].vert_list):
                normals=True
            texcoords=False
            if len(self.gf_list[i].vt_list)==len(self.gf_list[i].vert_list):
                texcoords=True
    
            att={}
            face_bin=[]
            norm_bin=[]
            txts_bin=[]
            vert_bin=[]
            vert_map = [-1] * len(self.gf_list[i].vert_list)
            prim_list=[]
            mat_index=-1
                
            for j in range(0,len(self.gf_list[i].faces)):

                # Determine the material for this face
                mat1=''
                mat_index=-1
                
                lf1=len(self.gf_list[i].faces[j])
                if lf1==4:
                    mat1=self.gf_list[i].faces[j][lf1-1]

                    mat_found=False
                    for ik in range(0,len(self.mat_list)):
                        if (mat_found==False and
                            self.mat_list[ik].name==mat1):
                            mat_index=ik
                            mat_found=True
                    if mat_found==False:
                        print('Could not find mat "'+mat2+
                              '" in mat_list.')
                        quit()
                    
                #print(i,j,'mat1:',mat1)
                    
                # Map the first vertex
                ix=self.gf_list[i].faces[j][0]
                if vert_map[ix]==-1:
                    # Converting the vertices to "float()"
                    # helps ensure single precision and then
                    # validators don't complain that max and
                    # min are wrong.
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][0]))
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][1]))
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][2]))
                    if normals:
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][0]))
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][1]))
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][2]))
                    if texcoords and self.mat_list[mat_index].txt!='':
                        txts_bin.append(float(self.gf_list[i].vt_list[ix][0]))
                        txts_bin.append(float(self.gf_list[i].vt_list[ix][1]))
                    vert_map[ix]=int(len(vert_bin)/3)
                    # We have to subtract one here because
                    # the point has already been added to 'vert_bin'
                    face_bin.append(int(len(vert_bin)/3)-1)
                else:
                    face_bin.append(vert_map[ix])
                # Map the second vertex
                ix=self.gf_list[i].faces[j][1]
                if vert_map[ix]==-1:
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][0]))
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][1]))
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][2]))
                    if normals:
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][0]))
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][1]))
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][2]))
                    if texcoords and self.mat_list[mat_index].txt!='':
                        txts_bin.append(float(self.gf_list[i].vt_list[ix][0]))
                        txts_bin.append(float(self.gf_list[i].vt_list[ix][1]))
                    vert_map[ix]=int(len(vert_bin)/3)
                    # We have to subtract one here because
                    # the point has already been added to 'vert_bin'
                    face_bin.append(int(len(vert_bin)/3)-1)
                else:
                    face_bin.append(vert_map[ix])
                # Map the third vertex
                ix=self.gf_list[i].faces[j][2]
                if vert_map[ix]==-1:
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][0]))
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][1]))
                    vert_bin.append(float(self.gf_list[i].vert_list[ix][2]))
                    if normals:
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][0]))
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][1]))
                        norm_bin.append(float(self.gf_list[i].vn_list[ix][2]))
                    if texcoords and self.mat_list[mat_index].txt!='':
                        txts_bin.append(float(self.gf_list[i].vt_list[ix][0]))
                        txts_bin.append(float(self.gf_list[i].vt_list[ix][1]))
                    vert_map[ix]=int(len(vert_bin)/3)
                    # We have to subtract one here because
                    # the point has already been added to 'vert_bin'
                    face_bin.append(int(len(vert_bin)/3)-1)
                else:
                    face_bin.append(vert_map[ix])

                # Determine if the next face is composed of a
                # different material, if so, set mat2 and
                # flip next_face_different_mat to True
                next_face_different_mat=False
                if j<len(self.gf_list[i].faces)-1:
                    mat2=''
                    lf2=len(self.gf_list[i].faces[j+1])
                    if lf2==4:
                        mat2=self.gf_list[i].faces[j+1][lf2-1]
                    if mat1!=mat2:
                        next_face_different_mat=True

                # If we're at the end, or we're switching materials,
                # then add the primitive to the mesh and update
                # the binary data file accordingly
                if (j==len(self.gf_list[i].faces)-1 or
                    next_face_different_mat==True):

                    dat1=pack('<'+'f'*len(vert_bin),*vert_bin)
                    f2.write(dat1)
                    if normals:
                        dat3=pack('<'+'f'*len(norm_bin),*norm_bin)
                        f2.write(dat3)
                    # If the object provides texture coordinates, but
                    # there's no texture, then there's no need to
                    # output them
                    if texcoords and self.mat_list[mat_index].txt!='':
                        dat4=pack('<'+'f'*len(txts_bin),*txts_bin)
                        f2.write(dat4)
                    dat2=pack('<'+'h'*len(face_bin),*face_bin)
                    f2.write(dat2)
        
                    max_v=[0,0,0]
                    min_v=[0,0,0]
                    for ii in range(0,len(vert_bin),3):
                        for jj in range(0,3):
                            if ii==0 or vert_bin[ii+jj]<min_v[jj]:
                                min_v[jj]=vert_bin[ii+jj]
                            if ii==0 or vert_bin[ii+jj]>max_v[jj]:
                                max_v[jj]=vert_bin[ii+jj]
                    
                    # 5120 is signed byte
                    # 5121 is unsigned byte
                    # 5122 is signed short
                    # 5123 is unsigned short
                    # 5125 is unsigned int
                    # 5126 is signed float
                    
                    acc_list.append({"bufferView": acc_index,
                                     "componentType": 5126,
                                     "count": int(len(vert_bin)/3),
                                     "max": max_v,
                                     "min": min_v,
                                     "type": "VEC3"})
                    att["POSITION"]=acc_index
                    acc_index=acc_index+1
                    if normals:
                        acc_list.append({"bufferView": acc_index,
                                         "componentType": 5126,
                                         "count": int(len(vert_bin)/3),
                                         "type": "VEC3"})
                        att["NORMAL"]=acc_index
                        acc_index=acc_index+1
                    # If the object provides texture coordinates, but
                    # there's no texture, then there's no need to
                    # output them
                    if texcoords and self.mat_list[mat_index].txt!='':
                        acc_list.append({"bufferView": acc_index,
                                         "componentType": 5126,
                                         "count": int(len(vert_bin)/3),
                                         "type": "VEC2"})
                        att["TEXCOORD_0"]=acc_index
                        acc_index=acc_index+1
                    acc_list.append({"bufferView": acc_index,
                                     "componentType": 5123,
                                     "count": int(len(face_bin)/1),
                                     "type": "SCALAR"})
                    if mat1=='':
                        prim_list.append({"attributes": att,
                                          "indices": acc_index})
                    else:
                        prim_list.append({"attributes": att,
                                          "indices": acc_index,
                                          "material": mat_index})
                    if j==len(self.gf_list[i].faces)-1:
                        mesh_list.append({"name": self.gf_list[i].name,
                                          "primitives": prim_list})
                        
                    acc_index=acc_index+1
        
                    # 34962 is "ARRAY_BUFFER"
                    # 34963 is "ELEMENT_ARRAY_BUFFER"
                    
                    buf_list.append({"buffer": 0,
                                     "byteLength": 4*len(vert_bin),
                                     "byteOffset": offset,
                                     "target": 34962})
                    offset+=4*len(vert_bin)
                    if normals:
                        buf_list.append({"buffer": 0,
                                         "byteLength": 4*len(norm_bin),
                                         "byteOffset": offset,
                                         "target": 34962})
                        offset+=4*len(norm_bin)
                    # If the object provides texture coordinates, but
                    # there's no texture, then there's no need to
                    # output them
                    if texcoords and self.mat_list[mat_index].txt!='':
                        buf_list.append({"buffer": 0,
                                         "byteLength": 4*len(txts_bin),
                                         "byteOffset": offset,
                                         "target": 34962})
                        offset+=4*len(txts_bin)
                    buf_list.append({"buffer": 0,
                                     "byteLength": 2*len(face_bin),
                                     "byteOffset": offset,
                                     "target": 34963})
                    offset+=2*len(face_bin)
                    print('offset:',offset)

                    print('len(face_bin):',self.gf_list[i].name,
                          len(face_bin))
                    print('min,max:',min_v,max_v)
                    print('')
                    
                    # Reset the primitive objects so that
                    # we can start a new one
                    att={}
                    face_bin=[]
                    vert_bin=[]
                    vert_map = [-1] * len(self.gf_list[i].vert_list)

        # Add the top-level data to the json object
        jdat["meshes"]=mesh_list
        if len(mat_json)>0:
            jdat["materials"]=mat_json
        jdat["accessors"]=acc_list
        jdat["bufferViews"]=buf_list
        jdat["buffers"]=[{"byteLength": offset,
                          "uri": prefix+'.bin'}]
        if len(txt_list)>0:
            jdat["textures"]=txt_list
            jdat["images"]=img_list

        # write the json file
        f=open(gltf_file,'w',encoding='utf-8')
        json.dump(jdat,f,ensure_ascii=False,indent=2)
        f.close()

        f2.close()
            
        return
        
class td_plot_base(yt_plot_base):
    """
    A class for managing plots of three-dimensional data
    """

    def __init__(self):
        super().__init__()
        self.to=threed_objects()
        return

    def td_den_plot(self,o2scl,amp,args,cmap='',mat_name='white'):
        """
        Desc
        """
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        slice_name=''
        slice=args[0]

        if curr_type==b'table3d':
            slice_name=args[0]
            if len(args)>=2:
                kwstring=args[1]
        else:
            print("Command 'td-den-plot' not supported for type",
                  curr_type,".")
            return

        table3d=amt.get_table3d_obj()
        nxt=table3d.get_nx()
        nyt=table3d.get_ny()
        sl=table3d.get_slice(slice).to_numpy()
        xgrid=[table3d.get_grid_x(i) for i in range(0,nxt)]
        ygrid=[table3d.get_grid_y(i) for i in range(0,nyt)]
        
        if self.xset==False:
            self.xlo=numpy.min(xgrid)
            self.xhi=numpy.max(xgrid)
            if self.verbose>2:
                print('td_den_plot(): x limits not set, so setting to',
                      self.xlo,',',self.xhi)
        if self.yset==False:
            self.ylo=numpy.min(ygrid)
            self.yhi=numpy.max(ygrid)
            if self.verbose>2:
                print('td_den_plot(): y limits not set, so setting to',
                      self.ylo,',',self.yhi)
        if self.zset==False:
            self.zlo=numpy.min(sl)
            self.zhi=numpy.max(sl)
            if self.verbose>2:
                print('td_den_plot(): z limits not set, so setting to',
                      self.zlo,',',self.zhi)
        
        # If true, then a color map has been specified and we need
        # to add materials
        colors=False
        
        # The list of 256 materials defined by the color map
        # (not all will be needed for the 3d object
        cmap_mats=[]
        
        if cmap!='':
            
            import matplotlib.cm as cm
            from matplotlib.colors import Normalize
            import matplotlib.pyplot as plot
            
            color_map=cm.get_cmap(cmap)
            norm=plot.Normalize(0,255)
            
            for i in range(0,256):
                rgb=color_map(norm(float(i)))[:3]
                cmap_mats.append(material('cmap_'+str(i),[rgb[0],rgb[1],
                                                       rgb[2]]))
                
            colors=True
            if self.verbose>2:
                print('td_den_plot(): Using colors from cmap',cmap)
            
        # Vertices for the density plot
        den_vert=[]
        # Faces for the density plot
        den_face=[]
        # Materials for the density plot
        den_ml=[]
        
        # Vertex index for faces
        k=0
        for i in range(0,nxt):
            for j in range(0,nyt):
                arr=[(xgrid[i]-self.xlo)/(self.xhi-self.xlo),
                     (ygrid[j]-self.ylo)/(self.yhi-self.ylo),
                     (sl[i,j]-self.zlo)/(self.zhi-self.zlo)]
                den_vert.append(arr)
                if i<nxt-1 and j<nyt-1:
                    if colors==True:
                        # Construct the colormap index
                        cmap_ix=int(arr[2]*256)
                        if cmap_ix>255:
                            cmap_ix=255
                        cmap_name='cmap_'+str(cmap_ix)
                        # See if the corresponding material is already
                        # in the list named 'den_ml'
                        mat_found=False
                        for ell in range(0,len(den_ml)):
                            if den_ml[ell].name==cmap_name:
                                mat_found=True
                        # If it was not found, find it in the list
                        # named 'cmap_mats'
                        if mat_found==False:
                            for ell in range(0,len(cmap_mats)):
                                if cmap_mats[ell].name==cmap_name:
                                    print('Adding material',cmap_name)
                                    den_ml.append(cmap_mats[ell])
                                    ell=len(cmap_mats)
                         # Add the two triangles 
                        arr2=[k+1,k+nyt+1,k+2,cmap_name]
                        den_face.append(arr2)
                        arr3=[k+1+nyt,k+2,k+2+nyt,cmap_name]
                        den_face.append(arr3)
                        
                    else:
                        
                        arr2=[k,k+nyt,k+1]
                        den_face.append(arr2)
                        arr3=[k+nyt,k+1+nyt,k+1]
                        den_face.append(arr3)
                        
                k=k+1

        #for k in range(0,41):
        #print(k,den_vert[k])
                
        # Convert to GLTF
                
        vert2=[]
        norms2=[]
        
        for i in range(0,len(den_face)):

            #print('old faces:',den_face[i])
            
            # Add the vertices to the new vertex array
            vert2.append(den_vert[den_face[i][0]-1])
            vert2.append(den_vert[den_face[i][1]-1])
            vert2.append(den_vert[den_face[i][2]-1])
    
            # Compute the norm
            p1=den_vert[den_face[i][0]-1]
            p2=den_vert[den_face[i][1]-1]
            p3=den_vert[den_face[i][2]-1]
            v1=[1]*3
            v2=[1]*3
            for j in range(0,3):
                v1[j]=p2[j]-p1[j]
                v2[j]=p3[j]-p2[j]
            norm=cross(v1,v2,norm=True)
            for k in range(0,3):
                norms2.append([norm[0],norm[1],norm[2]])
    
            den_face[i]=[i*3,i*3+1,i*3+2,den_face[i][3]]

            #print('new faces:',den_face[i])
            #print('face:',den_face[i])
            #print('verts:',vert2[den_face[i][0]],
            #      vert2[den_face[i][1]],vert2[den_face[i][2]])
            #temp=input('Press a key to continue. ')

        if self.verbose>2:
            print('td_den_plot(): adding',len(den_face),'faces.')
        if colors==True:
            gf=group_of_faces('plot',den_face)
            gf.vert_list=vert2
            gf.vn_list=norms2
            self.to.add_object_mat_list(gf,den_ml)
            for i in range(0,len(self.to.mat_list)):
                print('to.mat_list',i,self.to.mat_list[i].name)
        else:
            
            if self.to.is_mat(mat_name)==False:
                
                if mat_name=='white':
                    white=material(mat_name,[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('Material '+mat_name+' not found in td-den-plot.')
                    return
            
            gf=group_of_faces('plot',den_face)
            gf.vert_list=vert2
            gf.vn_list=norms2
            self.to.add_object_mat(gf,white)

        return
        
    def td_arrow(self,x1,y1,z1,x2,y2,z2,name,
                 mat : str | material = 'white'):
        """Documentation for o2graph command ``td-arrow``:

        Plot an axis in a 3d visualization

        Command-line arguments: ``x1 y1 z1 x2 y2 z2 group_name [kwargs]``
        """
        arr_vert,arr_norm,arr_face=arrow(x1,y1,z1,x2,y2,z2)

        if type(mat)==str:
            if not self.to.is_mat(mat):
                if mat=='white':
                    white=material('white',[1,1,1])
                    self.to.add_mat(white)
                else:
                    print('No material named',mat,'in td-arrow')
                    return
            if self.verbose>2:
                print('td_arrow() creating group named',name,'with material',
                      mat+'.')
            gf=group_of_faces(name,arr_face,mat)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)
                               
        else:
            if self.verbose>2:
                print('td_arrow() creating group named',name,'with material',
                      mat.name+'.')
            if not self.to.is_mat(mat.name):
                self.to.add_mat(mat)
            gf=group_of_faces(name,arr_face,mat.name)
            gf.vert_list=arr_vert
            gf.vn_list=arr_norm
            self.to.add_object(gf)

        return

    def td_axis_label(self, ldir : str, tex_label : str,
                      mat_name : str = '', png_file : str = '',
                      group_name : str = '', offset : float = 0.1,
                      height : float = 0.1):
        """Create an axis label in the direction ``ldir`` with label
        ``tex_label``.
        """

        white_found=False
        for i in range(0,len(self.to.mat_list)):
            if self.to.mat_list[i].name=='white':
                white_found=True
        if white_found==False:
            white=material('white',[1,1,1])
            self.to.add_mat(white)
        
        if ldir=='x':
            
            if png_file=='':
                png_file='xtitle.png'
            if mat_name=='':
                mat_name='mat_xtitle'
            if group_name=='':
                group_name='x_title'

            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)

            x_v,x_f,x_t,x_n,x_m=latex_prism(0.5,-offset-height/2.0,
                                            -offset+height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset-height/2.0,
                                            tex_label,png_file,mat_name,
                                            dir=ldir)

            self.to.add_mat(x_m)
            gf=group_of_faces(group_name,x_f)
            gf.vert_list=x_v
            gf.vn_list=x_n
            gf.vt_list=x_t
            self.to.add_object(gf)

        elif ldir=='y':
            
            if png_file=='':
                png_file='ytitle.png'
            if mat_name=='':
                mat_name='mat_ytitle'
            if group_name=='':
                group_name='y_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)
                
            y_v,y_f,y_t,y_n,y_m=latex_prism(-offset-height/2.0,0.5,
                                            -offset+height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset-height/2.0,
                                            tex_label,png_file,mat_name,
                                            dir=ldir)
            
            self.to.add_mat(y_m)
            gf=group_of_faces(group_name,y_f)
            gf.vert_list=y_v
            gf.vn_list=y_n
            gf.vt_list=y_t
            self.to.add_object(gf)

        elif ldir=='z':
            
            if png_file=='':
                png_file='ztitle.png'
            if mat_name=='':
                mat_name='mat_ztitle'
            if group_name=='':
                group_name='z_title'
                
            if self.verbose>2:
                print('td_axis_label(): png_file:',png_file,'mat_name:',
                      mat_name,'group_name:',group_name)
                
            z_v,z_f,z_t,z_n,z_m=latex_prism(-offset-height/2.0,
                                            -offset+height/2.0,
                                            0.5,-offset+height/2.0,
                                            -offset-height/2.0,0.5,
                                            tex_label,png_file,mat_name,
                                            dir=ldir)
            
            self.to.add_mat(z_m)
            gf=group_of_faces(group_name,z_f)
            gf.vert_list=z_v
            gf.vn_list=z_n
            gf.vt_list=z_t
            self.to.add_object(gf)

        else:
            if type(ldir)==str:
                raise ValueError('Direction '+ldir+' is not one of "x", "y",'+
                                 ' or "z" in function td_axis_label().')
            else:
                raise ValueError('Direction is not one of "x", "y",'+
                                 ' or "z" in function td_axis_label().')
            
        return
    
class o2graph_plotter(td_plot_base):
    """
    A plotting class for the o2graph script. This class is a child of the
    :py:class:`o2sclpy.plot_base` class.

    This class is not necessarily intended to be instantiated by the 
    end user. 

    The function parameter `o2scl` must always be a ctypes DLL 
    object which points to the libo2scl shared library (.so on
    linux and .dylib on OSX). The function parameter `amp` must
    always be a pointer to the 
    :ref:`o2scl_acol::acol_manager<o2scl:acol_manager>` object.
    """

    cbar=0
    """ 
    Colorbar object
    """

    def __init__(self):
        """
        Desc
        """
        for line in base_list:
            if line[0]=="plotv":
                line[1]=o2graph_plotter.plotv.__doc__
            elif line[0]=="yt-ann":
                line[1]=o2graph_plotter.yt_ann_func.__doc__
            elif line[0]=="yt-path":
                line[1]=o2graph_plotter.yt_path_func.__doc__
            elif line[0]=="yt-render":
                line[1]=o2graph_plotter.yt_render.__doc__
            elif line[0]=="yt-text":
                line[1]=o2graph_plotter.yt_text.__doc__
            elif line[0]=="mp4":
                line[1]=o2graph_plotter.mp4.__doc__
            elif line[0]=="obj":
                line[1]=o2graph_plotter.obj_o2graph.__doc__
            elif line[0]=="gltf":
                line[1]=o2graph_plotter.gltf_o2graph.__doc__
            elif line[0]=="kde-plot":
                line[1]=o2graph_plotter.kde_plot.__doc__
            elif line[0]=="kde-2d-plot":
                line[1]=o2graph_plotter.kde_2d_plot.__doc__
            elif line[0]=="yt-tf":
                line[1]=o2graph_plotter.yt_tf_func.__doc__
        for line in extra_list:
            if line[1]=="to-kde":
                line[2]=o2graph_plotter.to_kde.__doc__
            if line[1]=="den-plot":
                line[2]=o2graph_plotter.den_plot_o2graph.__doc__
            if line[1]=="den-plot-rgb":
                line[2]=o2graph_plotter.den_plot_rgb_o2graph.__doc__
            if line[1]=="den-plot-anim":
                line[2]=o2graph_plotter.den_plot_anim.__doc__
            if line[1]=="errorbar":
                line[2]=o2graph_plotter.errorbar.__doc__
            elif line[1]=="hist-plot":
                line[2]=o2graph_plotter.hist_plot.__doc__
            elif line[1]=="hist2d-plot":
                line[2]=o2graph_plotter.hist2d_plot.__doc__
            elif line[1]=="plot":
                line[2]=o2graph_plotter.plot_o2graph.__doc__
            elif line[1]=="plot1":
                line[2]=o2graph_plotter.plot1.__doc__
            elif line[1]=="plot-color":
                line[2]=o2graph_plotter.plot_color.__doc__
            elif line[1]=="rplot":
                line[2]=o2graph_plotter.rplot.__doc__
            elif line[1]=="scatter":
                line[2]=o2graph_plotter.scatter.__doc__
            elif line[1]=="yt-add-vol":
                line[2]=o2graph_plotter.yt_add_vol.__doc__
            elif line[1]=="yt-anim":
                line[2]=o2graph_plotter.yt_anim.__doc__
            elif line[1]=="yt-scatter":
                line[2]=o2graph_plotter.yt_scatter.__doc__
            elif line[1]=="yt-vertex-list":
                line[2]=o2graph_plotter.yt_vertex_list.__doc__

        super().__init__()
        return

    def set_wrapper(self,o2scl,amp,link,args):
        """
        Wrapper around :py:func:`o2sclpy.plot_base.set` which sets
        plot-related parameters and sends other parameters to
        ``acol_manager``.
        """

        # First determine if it's an o2graph or yt parameter
        match=False
        for line in param_list:
            if args[0]==line[0]:
                match=True
                if self.verbose>2:
                    print('Parameter',args[0],'is o2graph parameter.')
                
        for line in yt_param_list:
            if args[0]==line[0]:
                match=True
                if self.verbose>2:
                    print('Parameter',args[0],'is a yt parameter.')

        # If it's an o2graph or yt parameter, then call the parent
        # set() function
        if match==True:
            self.set(args[0],args[1])

        # If we're modifying the verbose parameter, then make sure
        # both the o2graph and the acol version match. Otherwise, if
        # it's only an o2graph or yt parameter, then just return.
        if (match==True and 
            force_bytes(args[0])!=b'verbose'):
            return

        # Call the acol 'set' function
        vs=std_vector_string(self.link2)
        vs.resize(len(args)+1)
        vs[0]=b'-set'
        for i in range(0,len(args)):
            vs[i+1]=force_bytes(args[i])

        amt=acol_manager(self.link2,amp)
            
        if self.verbose>2:
            print('Calling acol set function for parameter '+args[0]+'.')
            
        amt.parse_vec_string(vs)

        # End of function o2graph_plotter::set_wrapper()
        return

    def get_wrapper(self,o2scl,amp,args):
        """
        Wrapper around :py:func:`o2sclpy.plot_base.get` which
        gets plot-related parameters and gets other parameters
        from ``acol_manager``.
        """
        match=False
        for line in param_list:
            if args[0]==line[0]:
                match=True

        for line in yt_param_list:
            if args[0]==line[0]:
                match=True
                
        if match==True:
            
            self.get(args[0])
                            
        else:

            vs=std_vector_string(self.link2)
            vs.resize(len(args)+1)
            vs[0]=b'-get'
            for i in range(0,len(args)):
                vs[i+1]=force_bytes(args[i])

            amt=acol_manager(self.link2,amp)

            if self.verbose>2:
                print('Calling acol get function for parameter '+
                      args[0]+'.')

            amt.parse_vec_string(vs)

        # End of function o2graph_plotter::get_wrapper()
        return
            
    def ell_max(self,amp,link,args):
        """
        Desc
        """
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)

        # Handle tensor and table3d types
        if curr_type!=b'prob_dens_mdim_gaussian':
            print("Command 'ell-max' not supported for type",
                  curr_type,".")
            return

        amt=acol_manager(self.link2,amp)
        pdmg=amt.get_pdmg_obj()
        
        if self.canvas_flag==False:
            self.canvas()
            
        fx=float(eval(x))
        fy=float(eval(y))
        fw=float(eval(w))
        fh=float(eval(h))
        fangle=float(eval(angle))
        if self.canvas_flag==False:
            self.canvas()
        r=patches.Ellipse((fx,fy),fw,fh,fangle,**kwargs)
        self.axes.add_patch(r)
        # End of function plot_base::ellipse()
        
        return
        
    def gen_acol(self,o2scl,amp,link,cmd_name,args):
        """
        Run a general ``acol`` command named ``cmd_name`` with arguments
        stored in ``args``. This function uses the O2scl function
        ``o2scl_acol_parse()``.
        """

        vs=std_vector_string(self.link2)
        vs.resize(len(args)+1)
        
        vs[0]=b'-'+force_bytes(cmd_name)
        for i in range(0,len(args)):
            vs[i+1]=force_bytes(args[i])
            
        amt=acol_manager(self.link2,amp)
        amt.parse_vec_string(vs)
        
        # End of function o2graph_plotter::gen_acol()
        return

    def to_kde(self,o2scl,amp,link,args):
        """Documentation for o2graph command ``to-kde``:

        For objects of type ``table``:

        Convert columns in a table to a KDE

        Command-line arguments: ``<options or 'none'> 
        <column 1> [column 2] ...``

        Desc.
        """
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)
        print('Command to-kde is not yet finished.')
        quit()
        #if curr_type==b'table':
        #else:

    def mp4(self,args,loop=False,vf=''):
        """Documentation for o2graph command ``mp4``:

        Create an mp4 file from a series of images.

        Command-line arguments: ``<pattern> <output>``

        Typical patterns are "prefix%02dsuffix" and outputs are
        "out.mp4". If the "mp4" suffix is omitted, it is automatically
        added.

        Typical video filter is e.g. vf='eq=brightness=0.5:contrast=10'.
        """
        if len(args)<2:
            print('Command mp4 needs more arguments.')
            return
        pattern=args[0]
        output=args[1]
        if output[-4:]!='.mp4':
            output=output+'.mp4'

        # -y means overwrite output without asking
        # -r 10 means set the framerate to 10 frames per second
        # -vcodec sets the video codec
        # -pix_fmt sets the pixel format
            
        cmd=('ffmpeg -y -r 10 -f image2 -i '+pattern+
             ' -vcodec libx264')
        if vf!='':
            cmd=cmd+' -vf '+vf
        if loop==True:
            cmd=cmd+' -stream_loop -1'
            
        cmd=cmd+' -crf 25 -pix_fmt yuv420p '+output
        
        print('o2graph_plottter::mp4(): Executing "'+cmd+'".')
        os.system(cmd)
        
        return
        
    def den_plot_o2graph(self,o2scl,amp,link,args):
        """Documentation for o2graph command ``den-plot``:

        For objects of type ``table3d``:

        Create a density plot from a slice of a table3d

        Command-line arguments: ``<slice> [kwargs]``

        Creates a density plot from the specified slice. A z-axis
        density legend is displayed on the RHS if ``colbar`` is set to
        True before plotting. If z-axis limits are specified, then
        values larger than the upper limit are set equal to the upper
        limit and values smaller than the lower limit are set equal to
        the lower limit before plotting. 

        The python function imshow() is used, unless 'pcm=True' is
        specified, in which case the pcolormesh() function is used
        instead. When 'pcm=False', logarithmic scales are handled by
        taking the base 10 log of the x- or y-grids specified in the
        table3d object before plotting. When 'pcm=True', logarithmic
        axes can be handled automatically. The imshow() function
        presumes a uniform linear or logarithmic x- and y-axis grid,
        and the den-plot function will output a warning if this is not
        the case. The pcolormesh() function can handle arbitrary x and
        y-axis grids. If ``logz`` is set to true, then the base 10
        logarithm is taken of the data before the density plot is
        constructed. 

        Some useful kwargs are cmap, interpolation (for
        imshow), alpha, vmin, and vmax. 

        See 
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
        and
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pcolormesh.html
        for more information and keyword arguments.

        For objects of type ``hist_2d``:

        Create a density plot from a hist_2d object

        Command-line arguments: ``[kwargs]``

        Creates a density plot from the current two-dimensional
        histogram. A z-axis density legend is displayed on the RHS if
        ``colbar`` is set to True before plotting. If z-axis limits
        are specified, then values larger than the upper limit are set
        equal to the upper limit and values smaller than the lower
        limit are set equal to the lower limit before plotting.

        The python function imshow() is used, unless 'pcm=True' is
        specified, in which case the pcolormesh() function is used
        instead. When 'pcm=False', logarithmic scales are handled by
        taking the base 10 log of the x- or y-grids specified in the
        table3d object before plotting. When 'pcm=True', logarithmic
        axes can be handled automatically. The imshow() function
        presumes a uniform linear or logarithmic x- and y-axis grid,
        and the den-plot function will output a warning if this is not
        the case. The pcolormesh() function can handle arbitrary x and
        y-axis grids. If ``logz`` is set to true, then the base 10
        logarithm is taken of the data before the density plot is
        constructed. 

        Some useful kwargs are cmap, interpolation (for
        imshow), alpha, vmin, and vmax.

        See 
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
        and
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pcolormesh.html
        for more information and keyword arguments.

        For objects of type ``tensor``:

        Create a density plot from a tensor object.

        Command-line arguments: ``[index_1 index_2] [kwargs]``

        If the tensor has rank 2 and the indices are not specified,
        then plot the first index along the x-axis and the second
        index along the y-axis. A z-axis density legend is print on
        the RHS if ``colbar`` is set to 1 before plotting. If z-axis
        limits are specified, then values larger than the upper limit
        are set equal to the upper limit and values smaller than the
        lower limit are set equal to the lower limit before plotting.

        For objects of type ``tensor<int>``:

        Create a density plot from a tensor<int> object.

        Command-line arguments: ``[index_1 index_2] [kwargs]``

        If the tensor has rank 2 and the indices are not specified,
        then plot the first index along the x-axis and the second
        index along the y-axis. A z-axis density legend is print on
        the RHS if ``colbar`` is set to 1 before plotting. If z-axis
        limits are specified, then values larger than the upper limit
        are set equal to the upper limit and values smaller than the
        lower limit are set equal to the lower limit before plotting.

        For objects of type ``tensor<size_t>``:

        Create a density plot from a tensor<size_t> object.

        Command-line arguments: ``[index_1 index_2] [kwargs]``

        If the tensor has rank 2 and the indices are not specified,
        then plot the first index along the x-axis and the second
        index along the y-axis. A z-axis density legend is print on
        the RHS if ``colbar`` is set to 1 before plotting. If z-axis
        limits are specified, then values larger than the upper limit
        are set equal to the upper limit and values smaller than the
        lower limit are set equal to the lower limit before plotting.

        For objects of type ``tensor_grid``:

        Create a density plot from a tensor_grid object.

        Command-line arguments: ``[index_1 index_2] [kwargs]``

        If the tensor has rank 2 and the indices are not specified,
        then plot the first index along the x-axis and the second
        index along the y-axis. A z-axis density legend is print on
        the RHS if ``colbar`` is set to 1 before plotting. If z-axis
        limits are specified, then values larger than the upper limit
        are set equal to the upper limit and values smaller than the
        lower limit are set equal to the lower limit before plotting.

        """
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        kwstring=''
        slice_name=''
        if curr_type==b'tensor':
            if len(args)>=2:
                amt.get_tensor_obj().copy_table3d(args[0],args[1],
                                                  amt.get_table3d_obj())
            else:
                amt.get_tensor_obj().copy_table3d(0,1,amt.get_table3d_obj())
            slice_name='z'
            if len(args)>=3:
                kwstring=args[2]
            elif len(args)==1:
                kwstring=args[0]
        elif curr_type==b'tensor<size_t>':
            if len(args)>=2:
                amt.get_tensor_size_t_obj().copy_table3d(args[0],args[1],
                                                         amt.get_table3d_obj())
            else:
                amt.get_tensor_size_t_obj().copy_table3d(0,1,
                                                         amt.get_table3d_obj())
            slice_name='z'
            if len(args)>=3:
                kwstring=args[2]
            elif len(args)==1:
                kwstring=args[0]
        elif curr_type==b'tensor<int>':
            if len(args)>=2:
                amt.get_tensor_int_obj().copy_table3d(args[0],args[1],
                                                      amt.get_table3d_obj())
            else:
                amt.get_tensor_int_obj().copy_table3d(0,1,
                                                      amt.get_table3d_obj())
            slice_name='z'
            if len(args)>=3:
                kwstring=args[2]
            elif len(args)==1:
                kwstring=args[0]
        elif curr_type==b'tensor_grid':
            svst=std_vector_size_t(self.link2)
            tg=amt.get_tensor_grid_obj()
            svst.resize(tg.get_rank())
            func=tg.copy_table3d_align_setxy
            t3d=amt.get_table3d_obj()
            if len(args)>=2:
                func(args[0],args[1],svst,t3d)
            else:
                func(0,1,svst,t3d)
            slice_name='z'
            if len(args)>=3:
                kwstring=args[2]
            elif len(args)==1:
                kwstring=args[0]
        elif curr_type==b'hist_2d':
            
            if len(args)>=1:
                kwstring=args[0]
                
            dctt=string_to_dict(kwstring)
            self.den_plot([amt.get_hist_2d_obj(),self.link2],**dctt)
            return
        
        elif curr_type==b'table3d':
            slice_name=args[0]
            if len(args)>=2:
                kwstring=args[1]
        else:
            print("Command 'den-plot' not supported for type",
                  curr_type,".")
            return

        dctt=string_to_dict(kwstring)
        self.den_plot([amt.get_table3d_obj(),slice_name],**dctt)

        return

    def den_plot_rgb_o2graph(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``den-plot-rgb``:

        For objects of type ``table3d``:

        Create a density plot from a specified slice

        Command-line arguments: ``<slice r> <slice g> <slice b> [kwargs]``

        Create a density plot from the three specified slices. This
        command uses imshow(). To directly create a .png file with no
        axes, use make-png instead. For example::

            o2graph -create table3d x "grid:0,1,0.01" y "grid:0,1,0.01" \\
            r "x" -function "y" g -function 0 b -den-plot-rgb r g b -show
        """

        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        kwstring=''
        if curr_type!=b'table3d':
            print("Command 'den-plot-rgb' not supported for type",
                  curr_type,".")
            return
            
        slice_r=args[0]
        slice_g=args[1]
        slice_b=args[2]
        if len(args)>=4:
            kwstring=args[3]

        dctt=string_to_dict2(kwstring,list_of_bools=['renorm'])
        self.den_plot_rgb(amt.get_table3d_obj(),slice_r,slice_g,slice_b,
                          **dctt)

        return

    def gltf_o2graph(self,o2scl,amp,link,args):
        """
        """

        prefix=args[0]
        if len(args)>=2:
            kwstring=args[1]

        if self.verbose>2:
            print('Writing gltf to file',prefix)
        self.to.write_gltf(prefix)

        return
    
    def obj_o2graph(self,o2scl,amp,link,args):
        """Produce an obj file
        """

        prefix=args[0]
        if len(args)>=2:
            kwstring=args[1]

        if self.verbose>2:
            print('Writing obj to file',prefix)
        self.to.write_obj(prefix)

        return

    def make_png_o2graph(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``make-png``:
        
        For objects of type ``table3d``:

        Command-line arguments: ``<slice r> <slice g> <slice b> [kwargs]``

        Create a .png file from the three specified table3d slices.
        This command requires pillow. To create a density-plot with
        axes instead, use den-plot-rgb.
        """

        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)

        kwstring=''
        if curr_type!=b'table3d':
            print("Command 'make-png' not supported for type",
                  curr_type,".")
            return
            
        slice_r=args[0]
        slice_g=args[1]
        slice_b=args[2]
        fname=args[3]
        if len(args)>=5:
            kwstring=args[4]

        dctt=string_to_dict(kwstring)
        renorm=dctt.pop('renorm',False)

        try:
            self.den_plot_rgb(amt.get_table3d_obj(),slice_r,slice_g,slice_b,
                              make_png=fname,renorm=renorm,**dctt)
        except Exception as e:
            print('Exception in make_png_o2graph()',e)
            raise
            
        return

    def kde_plot(self,o2scl,amp,args,link):
        """Documentation for o2graph command ``kde-plot``:

        For objects of type ``table``:

        Plot a KDE of one column

        Command-line arguments: ``<column> [plot kwargs] [kde kwargs]``

        Useful plot kwargs are all the usual plotting kwargs, plus
        x_min=0, x_max=0, y_mult=1, and n_points=201.

        Useful KDE kwargs are kernel='gaussian', metric='euclidean',
        transform='unit', and bandwidth='none'.
        """
        curr_type=o2scl_get_type(o2scl,amp,link)

        if curr_type==b'table':
            
            amt=acol_manager(link,amp)
            tab=amt.get_table_obj()

            # Copy the table data to a 2D numpy array
            x=numpy.zeros((tab.get_nlines(),1))
            for i in range(0,tab.get_nlines()):
                x[i,0]=tab.get(args[0],i)

            # Set defaults
            x_min=0
            x_max=0
            n_points=201
            y_mult=1
            
            # Convert kwargs to string so we can extract
            # n_points, x_min, and x_max
            dct_plot={}
            if len(args)>=2:
                dct_plot=string_to_dict2(args[1],
                                         list_of_ints=['n_points'],
                                         list_of_floats=['x_min','x_max',
                                                         'y_mult'])
                x_min=dct_plot.pop('x_min',0)
                x_max=dct_plot.pop('x_max',0)
                y_mult=dct_plot.pop('y_mult',1)
                n_points=dct_plot.pop('n_points',201)

            # If x_min and x_max are not set, then determine them,
            # either from the plot limits or from the minimum
            # and maximum of the data
            if x_min>=x_max:
                if self.xset==False:
                    # Determine min and max of data
                    x_min=x[0,0]
                    x_max=x[0,0]
                    for i in range(1,tab.get_nlines()):
                        if x[i,0]<x_min:
                            x_min=x[i,0]
                        if x[i,0]>x_max:
                            x_max=x[i,0]
                else:
                    x_min=self.xlo
                    x_max=self.xhi
            print('x_min,x_max,n_points,y_mult:',x_min,x_max,n_points,y_mult)

            # Use sklearn and a reasonable guess for the bandwidth,
            # between 1.0e-2 and 1.0e+2. Note that the KDE is
            # rescaled by default. 
            k=kde_sklearn()
            bw_array=[10**(float(i)/4.0-2.0) for i in range(0,17)]

            # Set the KDE
            if len(args)>=3:
                k.set_data_str(x,bw_array,args[2])
            else:
                k.set_data_str(x,bw_array,'')

            # Use the new KDE to create x and y-arrays
            xa=[]
            ya=[]
            xp=x_min
            for i in range(0,n_points):
                xa.append(xp)
                ya.append(k.pdf([xp])*y_mult)
                xp=xp+(x_max-x_min)/float(n_points-1)

            # Plot
            if len(args)<2:
                self.plot([xa,ya])
            else:
                self.plot([xa,ya],**dct_plot)
                
        else:
            print("Command 'kde-plot' not supported for type",
                  curr_type,".")
            return
        
        # End of function o2graph_plotter::kde_plot()
        return

    def kde_2d_plot(self,o2scl,amp,args,link):
        """Documentation for o2graph command ``kde-2d-plot``:

        For objects of type ``table``:

        Plot a KDE of two columns

        Command-line arguments: ``<column x> <column y> [options]``

        Desc.
        """
        curr_type=o2scl_get_type(o2scl,amp,link)

        if curr_type==b'table':
            
            amt=acol_manager(link,amp)
            tab=amt.get_table_obj()

            # Copy the table data to a numpy array
            x=numpy.zeros((tab.get_nlines(),2))
            for i in range(0,tab.get_nlines()):
                x[i,0]=tab.get(args[0],i)
                x[i,1]=tab.get(args[1],i)

            x0_min=x[0,0]
            x0_max=x[0,0]
            x1_min=x[0,1]
            x1_max=x[0,1]
            for i in range(1,tab.get_nlines()):
                if x[i,0]<x0_min:
                    x0_min=x[i,0]
                if x[i,0]>x0_max:
                    x0_max=x[i,0]
                if x[i,1]<x1_min:
                    x1_min=x[i,1]
                if x[i,1]>x1_max:
                    x1_max=x[i,1]
                
            k=kde_sklearn()
            bw_array=[10**(float(i)/4.0-2.0) for i in range(0,17)]

            if len(args)>2:
                k.set_data_str(x,bw_array,args[1])
            else:
                k.set_data_str(x,bw_array,'')

            x0a=[]
            x0p=x0_min
            for i in range(0,201):
                x0a.append(x0p)
                x0p=x0p+(x0_max-x0_min)/200.0
            x1a=[]
            x1p=x1_min
            for i in range(0,201):
                x1a.append(x1p)
                x1p=x1p+(x1_max-x1_min)/200.0
            z=numpy.zeros((200,200))
            for i in range(0,201):
                for j in range(0,201):
                    z[i,j]=k.pdf([x0a[i],x1a[j]])

            if len(args)<3:
                self.den_plot([x0a,x1a,z])
            else:
                self.den_plot([x0a,x1a,z],**string_to_dict(args[2]))
                
        else:
            print("Command 'kde-2d-plot' not supported for type",
                  curr_type,".")
            return
        
        # End of function o2graph_plotter::kde_2d_plot()
        return

    def plot_o2graph(self,o2scl,amp,args,link):
        """Documentation for o2graph command ``plot``:

        For objects of type ``table``:

        Plot two columns.

        Command-line arguments: ``<x> <y> [kwargs]``

        Plot column <y> versus
        column <x>. Some useful kwargs are color (c), dashes,
        linestyle (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms). For example::

            o2graph -create table x grid:0,10,0.2 -function "sin(x)" y \\
            -plot x y "lw=0,marker=+" -show 

        This command uses the matplotlib plot() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        For objects of type ``vec_vec_double``:

        Plot one or two columns.

        Command-line arguments: ``<x index> [y index or 'none'] [kwargs]``

        Plot vector with index [index y] versus vector with index
        <index x>. Alternatively, if the second argument is the
        string 'none', plot the vector with index <index x>.
        Some useful kwargs are color (c), dashes, linestyle
        (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms). For example::
        
            o2graph -create vec_vec_double grid:0,10,0.2 "func:51:sin(i)" \\
            -plot 0 1 "lw=0,marker=+" -show

        This command uses the matplotlib plot() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        For objects of type ``hist``:

        Plot the histogram

        Command-line arguments: ``[kwargs]``

        Plot the histogram weights as a function of the bin
        representative values. Some useful kwargs (which apply for all
        three object types) are color (c), dashes, linestyle (ls),
        linewidth (lw), marker, markeredgecolor (mec), markeredgewidth
        (mew), markerfacecolor (mfc), markerfacecoloralt (mfcalt),
        markersize (ms). For example::

            o2graph -create table x grid:0,10,0.01 \\
            -function "abs(sin(x))" y -to-hist y 20 \\
            -plot "lw=0,marker=+" -show

        This command uses the matplotlib plot() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        For objects of type ``vector<contour_line>``:

        Plot the contour lines.

        Command-line arguments: ``[kwargs]``

        Plot the set of contour lines. Some useful kwargs (which apply
        for all three object types) are color (c), dashes, linestyle
        (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms). For example::
        
            o2graph -create table3d x grid:0,1,0.02 y grid:0,1,0.02 z \\
            "(exp(-(x-0.2)^2/0.1)+exp(-(x-0.9)^2/0.1))*exp(-(y-0.4)^2/0.1)" \\
            -contours 0.5 z -plot "lw=2" -show 

        This command uses the matplotlib plot() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        For objects of type ``prob_dens_mdim_amr``:

        Plot the probability distribution.

        Command-line arguments: ``[kwargs]``

        Plot the set of contour lines. Some useful kwargs (which apply
        for all three object types) are color (c), dashes, linestyle
        (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms). This command
        uses the matplotlib plot() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        """

        curr_type=o2scl_get_type(o2scl,amp,self.link2)
                        
        if curr_type==b'table':
            
            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            
            if len(args)<3:
                self.plot([tab,args[0],args[1]])
            else:
                self.plot([tab,args[0],args[1]],**string_to_dict(args[2]))

            failed=False

            # End of section for 'table' type
            
        elif curr_type==b'vec_vec_double':
            
            amt=acol_manager(self.link2,amp)
            vvd=amt.get_vvdouble_obj()

            if len(args)<2:
                self.plot([vvd,int(args[0])])
            elif len(args)<3:
                self.plot([vvd,int(args[0]),int(args[1])])
            else:
                if args[1]=='none':
                    self.plot([vvd,int(args[0])],
                              **string_to_dict(args[2]))
                else:
                    self.plot([vvd,int(args[0]),int(args[1])],
                              **string_to_dict(args[2]))

            failed=False

            # End of section for 'vec_vec_double' type
            
        elif curr_type==b'hist':

            amt=acol_manager(self.link2,amp)
            hist=amt.get_hist_obj()
            
            if len(args)<3:
                self.plot([hist,self.link2])
            else:
                self.plot([hist,self.link2],**string_to_dict(args[0]))

            failed=False
            
            # End of section for 'hist' type
        elif curr_type==b'prob_dens_mdim_amr':

            amt=acol_manager(self.link2,amp)
            pdma=amt.get_pdma_obj()
            ndimx=pdma.n_dim
            mesh=pdma.get_mesh()
            nx=mesh.size()
            lowx=pdma.get_low()
            highx=pdma.get_high()

            if len(args)<2:
                print('Not enough arguments to plot for an object',
                      'of type prob_dens_mdim_amr.')
            
            dimx=int(args[0])
            dimy=int(args[1])

            self.xlo=lowx[dimx]
            self.ylo=lowx[dimy]
            self.xset=True
            self.xhi=highx[dimx]
            self.yhi=highx[dimy]
            self.yset=True
            print('%7.6e %7.6e %7.6e %7.6e' %
                  (self.xlo,self.ylo,self.xhi,self.yhi))

            if self.canvas_flag==False:
                self.canvas()

            # Need to figure out here how to convert fill function
            # to a value, keeping in mind it can depend on
            # fvy.value (fractional volume) or wy.value (weight)
                
            fill_fn='None'
            if len(args)>=3:
                fill_fn=args[2]
                
            print('Fill function',fill_fn)
                
            import matplotlib.patches as patches

            for i in range(0,nx):

                m2=mesh[i]
                low2=m2.get_low()
                high2=m2.get_high()
                left=low2[dimx]
                lower=low2[dimy]
                right=high2[dimx]
                upper=high2[dimy]
                fvy=m2.frac_vol
                wy=m2.weight
                w=right-left
                h=upper-lower
                print('%d %7.6e %7.6e %7.6e %7.6e %7.6e %7.6e' %
                      (i,left,lower,w,h,fvy,wy))

                if len(args)<4:
                    r=patches.Rectangle((left,lower),w,h,angle=0.0,
                                        alpha=1,fill=None,lw=1)
                    self.axes.add_patch(r)
                else:
                    strtemp='alpha='+str(fvy.value)+','+args[3]
                    r=patches.Rectangle((left,lower),w,h,angle=0.0,
                                        **string_to_dict(strtemp))
                    self.axes.add_patch(r)
                            
            # End of section for 'prob_dens_mdim_amr' type
        elif curr_type==b'vector<contour_line>':

            amt=acol_manager(self.link2,amp)
            vcl=amt.get_cont_obj()
            nconts=vcl.size()

            if self.canvas_flag==False:
                self.canvas()

            # Loop over all contour lines
            for k in range(0,nconts):

                cl=vcl[k]
                xv=cl.get_x().to_numpy()
                yv=cl.get_y().to_numpy()
                
                if self.logx==True:
                    if self.logy==True:
                        if len(args)<2:
                            self.axes.loglog(xv,yv)
                        else:
                            self.axes.loglog(xv,yv,**string_to_dict(args[0]))
                    else:
                        if len(args)<1:
                            self.axes.semilogx(xv,yv)
                        else:
                            self.axes.semilogx(xv,yv,**string_to_dict(args[0]))
                else:
                    if self.logy==True:
                        if len(args)<1:
                            self.axes.semilogy(xv,yv)
                        else:
                            self.axes.semilogy(xv,yv,**string_to_dict(args[0]))
                    else:
                        if len(args)<1:
                            self.axes.plot(xv,yv)
                        else:
                            self.axes.plot(xv,yv,**string_to_dict(args[0]))
                            
            # End of section for 'vector<contour_line>' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return

        # AWS, Commented out on 5/3/23
        #if self.xset==True:
        #self.axes.set_xlim(self.xlo,self.xhi)
        #if self.yset==True:
        #    self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::plot_o2graph()
        return
                                 
    def plot_color(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``plot-color``:

        For objects of type ``table``:

        Plot three columns, using the third for the color

        Command-line arguments: ``<x> <y> <c> <cmap> [kwargs]``

        Plot column <y> versus
        column <x> using column <c> to specify the line color.
        Some useful kwargs are color (c), dashes,
        linestyle (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms). For example:
        \"o2graph -create x 0 10 0.2 -function sin(x) y -plot x y
        lw=0,marker='+' -show\". This command uses the matplotlib
        plot() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.
        """
        
        if len(args)<4:
            raise ValueError('Function plot_color() requires four values '+
                             'for the args list.')
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
                        
        if curr_type==b'table':
                            
            failed=False

            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            xv=tab[force_bytes(args[0])]
            yv=tab[force_bytes(args[1])]
            zv=tab[force_bytes(args[2])]
            
            cmap=args[3]
            if args[3][0:5]=='cmyt.':
                import cmyt

            if failed==False:

                if self.logx:
                    for i in range(0,len(xv)):
                        xv[i]=math.log10(xv)
                if self.logy:
                    for i in range(0,len(yv)):
                        yv[i]=math.log10(yv)
                if self.logz:
                    for i in range(0,len(zv)):
                        zv[i]=math.log10(zv)
                
                if self.canvas_flag==False:
                    self.canvas()

                import matplotlib
                import matplotlib.cm as cm
                
                norm=matplotlib.colors.Normalize(vmin=min(zv),
                                                 vmax=max(zv),
                                                 clip=True)
                mapper=cm.ScalarMappable(norm=norm,cmap=cmap)
                    
                for i in range(0,len(xv)-1):

                    col=mapper.to_rgba(zv[i])
                    if len(args)<5:
                        self.axes.plot([xv[i],xv[i+1]],
                                       [yv[i],yv[i+1]],
                                       color=col)
                    else:
                        self.axes.plot([xv[i],xv[i+1]],
                                       [yv[i],yv[i+1]],
                                       color=col,
                                       **string_to_dict(args[4]))

                if self.colbar==True:
                    cbar=self.fig.colorbar(mapper,ax=self.axes)
                    cbar.ax.tick_params('both',length=6,width=1,which='major')
                    cbar.ax.tick_params(labelsize=self.font*0.8)
                    
            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::plot_color()
        return
                                 
    def rplot(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``rplot``:

        For objects of type ``table``:

        Plot a region inside a column or in between two columns.

        Command-line arguments: ``<x1> <y1> [x2 y2] [kwargs]``

        If either 2 or 3 arguments are specified, this command plots
        the region inside the curve defined by the specified set of x
        and y values. The first point is copied at the end to ensure a
        closed region. If 4 or 5 arguments are specified, then this
        command plots the region in between two sets of x and y
        values, again adding the first point from (x1,y1) to the end
        to ensure a closed region.
        """

        curr_type=o2scl_get_type(o2scl,amp,self.link2)
                        
        if curr_type==b'table':
                            
            failed=False

            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            xv=tab[force_bytes(args[0])]
            yv=tab[force_bytes(args[1])]
                
            if len(args)>3:
                zv=tab[force_bytes(args[2])]
                wv=tab[force_bytes(args[3])]

                for i in range(0,len(zv)):
                    xv=numpy.append(xv,zv[len(zv)-1-i])
                    yv=numpy.append(yv,wv[len(wv)-1-i])

                # Make sure the loop is closed
                xv=numpy.append(xv,zv[0])
                yv=numpy.append(yv,wv[0])
        
            if self.canvas_flag==False:
                self.canvas()
            if len(args)==3:
                self.axes.fill(xv,yv,**string_to_dict(args[2]))
            elif len(args)==5:
                self.axes.fill(xv,yv,**string_to_dict(args[4]))
            else:
                self.axes.fill(xv,yv)

            if self.logx==True:
                self.axes.set_xscale('log')
            if self.logy==True:
                self.axes.set_yscale('log')
                    
            if self.xset==True:
                self.axes.set_xlim(self.xlo,self.xhi)
            if self.yset==True:
                self.axes.set_ylim(self.ylo,self.yhi)
                                 
            # End of section for 'table' type
        else:
            print("Command 'rplot' not supported for type",
                  curr_type,".")
            return
        
        # End of function o2graph_plotter::rplot()
        return
                                 
    def scatter(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``scatter``:

        For objects of type ``table``:

        Create a scatter plot from 2-4 columns.

        Command-line arguments: ``<x> <y> [s] [c] [kwargs]``

        This command creates a scatter plot form columns <x> and <y>,
        optionally using column [s] to choose the marker size and
        optionally using column [c] to choose the marker color. To
        vary the marker colors while choosing the default marker size
        just specify 'None' as the argument for [s]. Or, to specify
        keyword arguments while using the default size and color,
        specify 'None' as the argument for both [s] and [c].

        """

        if self.verbose>1:
            print('In o2graph_plotter::scatter().')
        
        import matplotlib.pyplot as plot
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
                        
        if curr_type==b'table':
                            
            failed=False

            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            xv=tab[force_bytes(args[0])]
            yv=tab[force_bytes(args[1])]

            sv=[]
            cv=[]

            if (len(args)>2 and force_bytes(args[2])!=b'None' and
                force_bytes(args[2])!=b'none'):
                sv=tab[force_bytes(args[2])]

            if (len(args)>3 and force_bytes(args[3])!=b'None' and
                force_bytes(args[3])!=b'none'):
                cv=tab[force_bytes(args[3])]

            if failed==False:
                
                if self.canvas_flag==False:
                    self.canvas()
                ft=self.axes.scatter
                if len(sv)>0:
                    if len(cv)>0:
                        if len(args)>4:
                            self.last_image=ft(xv,yv,s=sv,c=cv,
                                         **string_to_dict(args[4]))
                        else:
                            self.last_image=ft(xv,yv,s=sv,c=cv)
                    else:
                        if len(args)>4:
                            self.last_image=ft(xv,yv,s=sv,
                                         **string_to_dict(args[4]))
                        else:
                            self.last_image=ft(xv,yv,s=sv)
                else:
                    if len(cv)>0:
                        if len(args)>4:
                            self.last_image=ft(xv,yv,c=cv,
                                         **string_to_dict(args[4]))
                        else:
                            self.last_image=ft(xv,yv,c=cv)
                    else:
                        if len(args)>4:
                            self.last_image=ft(xv,yv,**string_to_dict(args[4]))
                        else:
                            self.last_image=ft(xv,yv)

                if self.logx==True:
                    self.axes.set_xscale('log')
                if self.logy==True:
                    self.axes.set_yscale('log')
                    
                if self.xset==True:
                    self.axes.set_xlim(self.xlo,self.xhi)
                if self.yset==True:
                    self.axes.set_ylim(self.ylo,self.yhi)
                if self.colbar==True and len(cv)>0:
                    cbar=plot.colorbar(self.last_image,ax=self.axes)
                    cbar.ax.tick_params('both',length=6,width=1,
                                        which='major')
                    cbar.ax.tick_params(labelsize=self.font*0.8)
                    
            # End of section for 'table' type
        else:
            print("Command 'scatter' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::scatter()
        return
                                 
    def hist_plot(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``hist-plot``:

        For objects of type ``table``:

        Create a histogram plot from a column in a table

        Command-line arguments: ``<col> [kwargs]``

        For a table, create a histogram plot from the specified
        column. This command uses matplotlib to construct the
        histogram rather than using O2scl to create a histogram
        object. This command uses the matplotlib hist() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
        for information and keyword arguments.

        For objects of type ``hist``:

        Create a histogram plot from the current histogram.
        
        Command-line arguments: ``[kwargs]``

        Create a histogram plot from the current histogram. This
        command uses the matplotlib hist() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
        for information and keyword arguments.
        """

        curr_type=o2scl_get_type(o2scl,amp,self.link2)
                        
        if curr_type==b'table':

            failed=False
                
            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            xv=tab[force_bytes(args[0])]

            if failed==False:
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)<2:
                    self.axes.hist(xv)
                else:
                    self.axes.hist(xv,**string_to_dict(args[1]))

        elif curr_type==b'hist':
                    
            amt=acol_manager(self.link2,amp)
            hist=amt.get_hist_obj()
            wgts=hist.get_wgts()
            reps=std_vector(self.link2)
            hist.create_rep_vec(reps)
            bins=hist.get_bins()

            xv=reps.to_numpy()
            yv=wgts.to_numpy()
            zv=bins.to_numpy()
            
            if self.canvas_flag==False:
                self.canvas()
            if len(args)<1:
                self.axes.hist(xv,weights=yv,bins=zv)
            else:
                self.axes.hist(xv,weights=yv,bins=zv,
                               **string_to_dict(args[0]))
            
            # End of section for 'table' type
        else:
            print("Command 'hist_plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::hist_plot()
        return
                                 
    def hist2d_plot(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``hist2d-plot``:

        For objects of type ``table``:

        Create a 2D histogram plot from two columns in a table

        Command-line arguments: ``<col x> <col y> [kwargs]``

        Create a 2D histogram plot from the specified columns. This
        command uses matplotlib to construct the histogram rather than
        using O2scl to create a hist object.
        """

        import matplotlib.pyplot as plot
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
                        
        if curr_type==b'table':
                            
            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            xv=tab[force_bytes(args[0])]
            yv=tab[force_bytes(args[1])]

            failed=False

            if failed==False:
        
                if self.canvas_flag==False:
                    self.canvas()
                if len(args)<3:
                    c,x,y,self.last_image=self.axes.hist2d(xv,yv)
                else:
                    c,x,y,self.last_image=self.axes.hist2d(xv,yv,
                                                           **string_to_dict(args[2]))
                
                if self.colbar==True:
                    cbar=plot.colorbar(self.last_image,ax=self.axes)
                    cbar.ax.tick_params('both',length=6,width=1,
                                        which='major')
                    cbar.ax.tick_params(labelsize=self.font*0.8)
                    
            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::hist2d_plot()
        return
                                 
    def errorbar(self,o2scl,amp,link,args):
        """Documentation for o2graph command ``errorbar``:

        For objects of type ``table``:

        Plot the specified columns with errorbars.

        Command-line arguments: ``<x> <y> <xerr> <yerr> [kwargs]``

        Plot column <y> versus column <x> with symmetric error bars
        given in column <xerr> and <yerr>. For no uncertainty in
        either the x or y direction, just use 0 for <xerr> or <yerr>,
        respectively.

        Some useful kwargs for the errorbar command are:

        ========== ================================= =============
        keyword    description                       default value
        ========== ================================= =============
        ecolor     error bar color                   None
        elinewidth error bar line width              None
        capsize    cap size in points                None
        barsabove  plot error bars on top of points  False
        lolims     y value is lower limit            False
        uplims     y value is upper limit            False
        xlolims    x value is lower limit            False
        xuplims    x value is upper limit            False
        errorevery draw error bars on subset of data 1
        capthick   thickness of error bar cap        None
        ========== ================================= =============

        For error points with no lines use, e.g. lw=0,elinewidth=1.
        See also ``error-point`` for plotting a single point with
        errorbars.

        """

        curr_type=o2scl_get_type(o2scl,amp,self.link2)
                        
        if curr_type==b'table':

            xv=table_get_column(o2scl,amp,self.link2,args[0])
            yv=table_get_column(o2scl,amp,self.link2,args[1])

            if len(args)>=6 and args[2]=='None' or args[2]=='none':
                if is_number(args[3]):
                    xerrv=float(args[3]);
                else:
                    xerrv=table_get_column(o2scl,amp,self.link2,args[3])
            if len(args)>=6 and args[3]=='None' or args[3]=='none':
                if is_number(args[2]):
                    xerrv=float(args[2]);
                else:
                    xerrv=table_get_column(o2scl,amp,self.link2,args[2])
            elif len(args)>=6:
                if is_number(args[2]):
                    if is_number(args[3]):
                        xerrv=[[float(args[2]),float(args[3])]
                               for i in range(0,idxerr.value)]
                    else:
                        ptrxerr=table_get_column(o2scl,amp,self.link2,args[3])
                        xerrv=[[float(args[2]),ptrxerr[i]] for i in
                               range(0,idxerr.value)]
                else:
                    if is_number(args[3]):
                        ptrxerr=table_get_column(o2scl,amp,self.link2,args[2])
                        xerrv=[[ptrxerr[i],float(args[3])] for i in
                               range(0,idxerr.value)]
                    else:
                        ptrxerr=table_get_column(o2scl,amp,self.link2,args[2])
                        ptrxerr2=table_get_column(o2scl,amp,self.link2,args[3])
                        xerrv=[[ptrxerr[i],ptrxerr2[i]] for i in
                               range(0,idxerr.value)]
            else:
                if args[2]=='None' or args[2]=='none':
                    xerrv=0.0
                elif is_number(args[2]):
                    xerrv=float(args[2])
                else:
                    xerrv=table_get_column(o2scl,amp,self.link2,args[2])
    
            if args[3]=='None' or args[3]=='none':
                yerrv=0.0
            elif is_number(args[3]):
                yerrv=float(args[3])
            else:
                yerrv=table_get_column(o2scl,amp,self.link2,args[3])

            if self.canvas_flag==False:
                self.canvas()
            if len(args)<5:
                self.axes.errorbar(xv,yv,yerr=yerrv,xerr=xerrv)
            else:
                self.axes.errorbar(xv,yv,yerr=yerrv,xerr=xerrv,
                                   **string_to_dict(args[4]))
                
            # End of section for 'table' type
        else:
            print("Command 'plot' not supported for type",
                  curr_type,".")
            return
        
        if self.xset==True:
            self.axes.set_xlim(self.xlo,self.xhi)
        if self.yset==True:
            self.axes.set_ylim(self.ylo,self.yhi)
                                 
        # End of function o2graph_plotter::errorbar()
        return
                                 
    def plot1(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``plot1``:
        
        For objects of type ``table``:

        Plot the specified column

        Command-line arguments: ``<y> [kwargs]``

        Plot column <y> versus row number. Some useful kwargs are
        color (c), dashes, linestyle (ls), linewidth (lw), marker,
        markeredgecolor (mec), markeredgewidth (mew), markerfacecolor
        (mfc), markerfacecoloralt (mfcalt), markersize (ms). For
        example: \"o2graph -create x 0 10 0.2 -function sin(x) y
        -plot1 y ls='--',marker='o' -show\". This command uses the
        matplotlib plot() function, see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        For objects of type ``double[]``:

        Plot the array.

        Command-line arguments: ``[kwargs]``

        Plot the array. Some useful kwargs are color (c), dashes,
        linestyle (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms).
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        For objects of type ``int[]``:

        Plot the array.

        Command-line arguments: ``[kwargs]``

        Plot the array. Some useful kwargs are color (c), dashes,
        linestyle (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms).
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        For objects of type ``size_t[]``:

        Plot the array.

        Command-line arguments: ``[kwargs]``

        Plot the array. Some useful kwargs are color (c), dashes,
        linestyle (ls), linewidth (lw), marker, markeredgecolor (mec),
        markeredgewidth (mew), markerfacecolor (mfc),
        markerfacecoloralt (mfcalt), markersize (ms).
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        for information and keyword arguments. This command does not
        yet support the matplotlib format parameter.

        """
        curr_type=o2scl_get_type(o2scl,amp,self.link2)
        amt=acol_manager(self.link2,amp)
                        
        failed=False
            
        if curr_type==b'table':

            tab=amt.get_table_obj()
            yv=tab[force_bytes(args[0])][0:tab.get_nlines()]
            args=args[1:]

        elif curr_type==b'double[]':
            
            yv=amt.get_doublev_obj().to_numpy()
            
        elif curr_type==b'int[]':

            yv=amt.get_intv_obj().to_numpy()
            
        elif curr_type==b'size_t[]':
            
            yv=amt.get_size_tv_obj().to_numpy()
            
        else:
            
            print("Command 'plot1' not supported for type",
                  curr_type,".")
            return
            
        if failed==False:
            
            xv=[i for i in range(0,len(yv))]
        
            if self.canvas_flag==False:
                self.canvas()
            if self.logx==True:
                if self.logy==True:
                    if len(args)<1:
                        self.axes.loglog(xv,yv)
                    else:
                        self.axes.loglog(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        self.axes.semilogx(xv,yv)
                    else:
                        self.axes.semilogx(xv,yv,**string_to_dict(args[0]))
            else:
                if self.logy==True:
                    if len(args)<1:
                        self.axes.semilogy(xv,yv)
                    else:
                        self.axes.semilogy(xv,yv,**string_to_dict(args[0]))
                else:
                    if len(args)<1:
                        self.axes.plot(xv,yv)
                    else:
                        self.axes.plot(xv,yv,**string_to_dict(args[0]))
                                
            if self.xset==True:
                self.axes.set_xlim(self.xlo,self.xhi)
            if self.yset==True:
                self.axes.set_ylim(self.ylo,self.yhi)
                    
        # End of function o2graph_plotter::plot1()
        return
            
    def plotv(self,o2scl,amp,link,args):
        """Documentation for o2graph command ``plotv``:

        Plot several vector-like data sets.

        Command-line arguments: ``[multiple vector spec. for x] 
        <multiple vector spec. for y>``

        The plotv command plots one or several pairs of vectors for x
        and y. The total number of curves plotted will be the number
        of vector data sets from the first argument times the number
        of vector data sets from the second argument. If the x and y
        vector lengths are not equal, then the longer vector is
        truncated. Any kwargs are applied to all curves plotted. For
        details on multiple vector specifications, use o2graph -help
        mult-vector-spec.

        There is an additional keyword argument ``filter``. The filter
        is parsed through the python eval() function and all pairs of
        points for which the function evaluates to False are omitted
        from the plot. Local variables of interest are ``x`` and
        ``y``, corresponding to the x and y value at each point, and
        ``k``, the current array index.
        """

        amt=acol_manager(self.link2,amp)
        curr_type=o2scl_get_type(o2scl,amp,self.link2)

        filt=''
        if len(args)>=3:
            kwargs=string_to_dict(args[2])
            filt=kwargs.pop('filter','')
        
        if self.canvas_flag==False:
            self.canvas()

        if (len(args)>=2 and force_bytes(args[1])!=b'none' and
            force_bytes(args[1])!=b'None'):
            
            if self.verbose>1 or True:
                print('Calling mult_vectors_to_conts() with',
                      args[0],'and',args[1])
                
            vvdx=std_vector_vector(self.link2)
            retx=mult_vector_spec(self.link2,args[0],vvdx,False,self.verbose,
                                  False)
            vvdy=std_vector_vector(self.link2)
            rety=mult_vector_spec(self.link2,args[1],vvdy,False,self.verbose,
                                  False)

            for i in range(0,vvdx.size()):
                for j in range(0,vvdy.size()):

                    xarr=vvdx[i]
                    yarr=vvdy[j]
                    
                    if len(xarr)!=len(yarr):
                        print('o2graph command plotv warning: x vector',
                              i,'and y vector',j,'dont have the same',
                              'size.')
                        print('  Length of x:',len(xarr),'y:',len(yarr))
                    if len(filt)>0:
                        xarr2=[]
                        yarr2=[]
                        for k in range(0,len(xarr)):
                            if k<len(xarr):
                                x=xarr[k]
                                y=yarr[k]
                                if eval(filt)==True:
                                    xarr2.append(xarr[k])
                                    yarr2.append(yarr[k])
                    else:
                        xarr2=xarr
                        yarr2=yarr
                    if self.logx==True:
                        if self.logy==True:
                            if len(args)>=3:
                                self.axes.loglog(xarr2,yarr2,
                                                 **kwargs)
                            else:
                                self.axes.loglog(xarr2,yarr2)
                        else:
                            if len(args)>=3:
                                self.axes.semilogx(xarr2,yarr2,
                                                 **kwargs)
                            else:
                                self.axes.semilogx(xarr2,yarr2)
                    else:
                        if self.logy==True:
                            if len(args)>=3:
                                self.axes.semilogy(xarr2,yarr2,
                                                 **kwargs)
                            else:
                                self.axes.semilogy(xarr2,yarr2)
                        else:
                            if len(args)>=3:
                                self.axes.plot(xarr2,yarr2,
                                               **kwargs)
                            else:
                                self.axes.plot(xarr2,yarr2)
            
        else:
            
            if self.verbose>1:
                print('Calling mult_vectors_to_conts() with',
                      args[0])
                
            vvdy=std_vector_vector(self.link2)
            mult_vector_spec(self.link2,args[0],vvdy,False,self.verbose,False)
            
            kwstring=''
            if (len(args)>=3 and (force_bytes(args[1])==b'none' or
                                  force_bytes(args[1])==b'None')):
                kwstring=args[2]
            elif len(args)>=2:
                kwstring=args[1]
            
            for j in range(0,vvdy.size()):

                yarr=vvdy[j]
                xarr=[i for i in range(0,len(vvdy[j]))]

                if len(filt)>0:
                    xarr2=[]
                    yarr2=[]
                    for k in range(0,len(xarr)):
                        if k<len(xarr):
                            x=xarr[k]
                            y=yarr[k]
                            if eval(filt)==True:
                                xarr2.append(xarr[k])
                                yarr2.append(yarr[k])
                else:
                    xarr2=xarr
                    yarr2=yarr
                
                if self.logx==True:
                    if self.logy==True:
                        if kwstring!='':                            
                            self.axes.loglog(xarr2,yarr2,
                                             **string_to_dict(kwstring))
                        else:
                            self.axes.loglog(xarr2,yarr2)
                    else:
                        if kwstring!='':
                            self.axes.semilogx(xarr2,yarr2,
                                             **string_to_dict(kwstring))
                        else:
                            self.axes.semilogx(xarr2,yarr2)
                else:
                    if self.logy==True:
                        if kwstring!='':
                            self.axes.semilogy(xarr2,yarr2,
                                             **string_to_dict(kwstring))
                        else:
                            self.axes.semilogy(xarr2,yarr2)
                    else:
                        if kwstring!='':
                            self.axes.plot(xarr2,yarr2,
                                             **string_to_dict(kwstring))
                        else:
                            self.axes.plot(xarr2,yarr2)
                    
        # End of function o2graph_plotter::plotv()
        return
        
    def print_param_docs(self,amt):
        """
        Print parameter documentation.

        Called by help_func().
        """

        ter=terminal_py()
        str_line=ter.horiz_line()
        print('\n'+str_line)
        print('\nO2graph parameter list:')
        print(' ')
        for line in param_list:
            if line[0]!='verbose':
                if line[0]=='colbar':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.colbar))
                elif line[0]=='fig-dict':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.fig_dict))
                elif line[0]=='font':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.font))
                elif line[0]=='logx':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.logx))
                elif line[0]=='logy':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.logy))
                elif line[0]=='logz':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.logz))
                elif line[0]=='xhi':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.xhi))
                elif line[0]=='xlo':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.xlo))
                elif line[0]=='xset':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.xset))
                elif line[0]=='yhi':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.yhi))
                elif line[0]=='ylo':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.ylo))
                elif line[0]=='yset':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.yset))
                elif line[0]=='zhi':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.zhi))
                elif line[0]=='zlo':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.zlo))
                elif line[0]=='zset':
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color())+' '+
                          str(self.zset))
                else:
                    print(force_string(amt.get_param_color())+line[0]+
                          force_string(amt.get_default_color()))
                print(' '+line[1])
                print(' ')
        print(str_line)
        print('\nyt-related settings:')
        print(' ')
        for line in yt_param_list:
            if line[0]=='yt_filter':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_filter))
            if line[0]=='yt_focus':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_focus))
            if line[0]=='yt_position':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_position))
            if line[0]=='yt_width':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_width))
            if line[0]=='yt_north':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_north))
            if line[0]=='yt_path':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_path))
            if line[0]=='yt_resolution':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_resolution))
            if line[0]=='yt_sigma_clip':
                print(force_string(amt.get_param_color())+line[0]+
                      force_string(amt.get_default_color())+' '+
                      str(self.yt_sigma_clip))
            print(' '+line[1])
            print(' ')

        # End of function o2graph_plotter::print_param_docs()
        return
            
    def parse_argv(self,argv,o2scl,link):
        """
        Parse command-line arguments.

        This is the main function used by the :ref:`o2graph_script` .
        Once it has created a list of strings from argv, it calls
        parse_string_list() to call the proper functions. It 
        creates the pointer to the o2scl acol_manager object 
        called `amp`.
        """

        # Set the o2scl library pointer in the plot_base parent
        self.link2=link
        
        # Create an acol_manager object and get the pointer
        am=acol_manager(self.link2)
        amp=am._ptr

        s=std_string(self.link2)
        s.init_bytes(b'O2GRAPH_DEFAULTS')
        am.set_env_var_name(s)
        
        am.run_empty()
        cl=am.get_cl()

        # Get current type
        ter=terminal_py()
        cmd_desc=(b'o2graph: A data viewing and '+
                  b'processing program for '+force_bytes(ter.bold())+
                  b'O2scl'+force_bytes(ter.default_fgbg())+
                  b'.\n  Version: '+force_bytes(version)+b'\n')

        s.init_bytes(b'o2graph')
        cl.set_cmd_name(s)
        
        s.init_bytes(cmd_desc)
        cl.set_desc(s)

        # 12/9 The problem here is that o2graph appears to be
        # using acol to process the aliases. I think everything
        # may be fixed now with aliases.
        
        #if 'O2GRAPH_DEFAULTS' in os.environ:
        #    am.def_args=os.environ['O2GRAPH_DEFAULTS']
        #    vs_da=am.def_args.split()
        #    print('parsing default args')
        #    print('vs_da:',vs_da);
        #    vs_da2=std_vector_string(link)
        #    vs_da2.set_list(vs_da)
        #    print('here, going to pfa')
        #    cl.parse_for_aliases(vs_da2,True)
        #    print('vs2:',vs_da);
        #    self.parse_string_list(vs_da,o2scl,amp,link)
        #    print('done.')
        #else:
        #    am.def_args=''

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
                    self.parse_string_list(strlist,o2scl,amp,self.link2)
        else:
            
            vs=std_vector_string(self.link2)
            vs.set_list(argv)
            cl.apply_aliases(vs,0,True)
            strlist=[]
            for i in range(0,len(vs)):
                strlist.append(force_string(vs[i]))
            
            if self.verbose>2:
                print('Number of arguments:',len(strlist),'arguments.')
                print('Argument List:',strlist)
            self.parse_string_list(strlist,o2scl,amp,self.link2)

        # End of function o2graph_plotter::parse_argv()
        return

    def yt_add_vol(self,o2scl,amp,link,args,keyname='o2graph_vol'):
        """
        Documentation for o2graph command ``yt-add-vol``:

        For objects of type ``tensor_grid``:

        Add a tensor_grid object as a yt volume source

        Command-line arguments: ``[kwargs]``

        This command adds the volumetric data specified in the
        ``tensor_grid`` object as a yt volume source. The transfer
        function previously specified by ``yt-tf`` is used, or if
        unspecified, then yt's transfer_function_helper is used to
        create a 3 layer default transfer function.

        """

        curr_type=o2scl_get_type(o2scl,amp,self.link2)

        if curr_type==b'tensor_grid':
            
            self.yt_check_backend()
            import yt
            from yt.visualization.volume_rendering.api \
                import create_volume_source
            from yt.visualization.volume_rendering.transfer_function_helper \
                import TransferFunctionHelper

            amt=acol_manager(self.link2,amp)
            tg3=amt.get_tensor_grid_obj()
            rk=tg3.get_rank()
            if rk!=3:
                print("Object of type 'tensor_grid' does not have rank 3.")
                return
            sza=tg3.get_size_arr()
            nx=sza[0]
            ny=sza[1]
            nz=sza[2]
            grid_packed=tg3.get_grid_packed()
            gridx=[grid_packed[i] for i in range(0,nx)]
            gridy=[grid_packed[i+nx] for i in range(0,ny)]
            gridz=[grid_packed[i+nx+ny] for i in range(0,nz)]
            
            data=tg3.get_data()
            total_size=nx*ny*nz

            if self.xset==False:
                self.xlo=gridx[0]
                self.xhi=gridx[nx-1]
                self.xset=True
            if self.yset==False:
                self.ylo=gridy[0]
                self.yhi=gridy[ny-1]
                self.yset=True
            if self.zset==False:
                self.zlo=gridz[0]
                self.zhi=gridz[nz-1]
                self.zset=True
                print('o2graph_plotter:yt-add-vol: axis limits:\n ',
                      '%7.6e %7.6e %7.6e %7.6e %7.6e %7.6e' % (
                          self.xlo,self.xhi,
                          self.ylo,self.yhi,self.zlo,self.zhi))

            arr=numpy.ctypeslib.as_array(data,shape=(nx,ny,nz))
            arr3=arr.reshape((nx,ny,nz))
            
            self.yt_volume_data.append(numpy.copy(arr))
            # Rescale to the internal coordinate system
            bbox=numpy.array([[(gridx[0]-self.xlo)/(self.xhi-self.xlo),
                               (gridx[nx-1]-self.xlo)/(self.xhi-self.xlo)],
                              [(gridy[0]-self.ylo)/(self.yhi-self.ylo),
                               (gridy[ny-1]-self.ylo)/(self.yhi-self.ylo)],
                              [(gridz[0]-self.zlo)/(self.zhi-self.zlo),
                               (gridz[nz-1]-self.zlo)/(self.zhi-self.zlo)]])
            self.yt_volume_bbox.append(numpy.copy(bbox))
            bbox2=self.yt_volume_bbox[len(self.yt_volume_bbox)-1]

            func=yt.load_uniform_grid
            self.yt_data_sources.append(func(dict(density=arr3),
                                             (nx,ny,nz),bbox=bbox2))
            ds=self.yt_data_sources[len(self.yt_data_sources)-1]

            cvs=create_volume_source
            self.yt_vols.append(cvs(ds,field=('gas','density')))
                                              
            vol=self.yt_vols[len(self.yt_vols)-1]
            vol.log_field=False

            # Setup the transfer function
            if self.yt_tf!=0:
                vol.set_transfer_function(self.yt_tf)
                print(self.yt_tf)
            else:
                tfh=TransferFunctionHelper(ds)
                tfh.set_field('density')
                tfh.set_log(False)
                tfh.set_bounds()
                tfh.build_transfer_function()
                tfh.tf.add_layers(3)
                #tfh.plot('tf.png')
                vol.set_transfer_function(tfh.tf)
                print(tfh.tf)

            if self.yt_created_scene==False:
                self.yt_create_scene()

            kname=self.yt_unique_keyname(keyname)
            self.yt_vol_keynames.append(kname)
            self.yt_scene.add_source(vol,keyname=kname)
                            
            if self.yt_created_camera==False:
                self.yt_create_camera(ds)
                
        elif curr_type==b'table3d':
            
            self.yt_check_backend()
            
            import yt
            from yt.visualization.volume_rendering.api \
                import create_volume_source
            from yt.visualization.volume_rendering.transfer_function_helper \
                import TransferFunctionHelper

            tg=tensor_grid(self.link2)
            amt=acol_manager(self.link2,amp)
            t3d=amt.get_table3d_obj()
            tg.from_table3d_fermi(args[0])

            grid=std_vector(self.link2)
            grid=tg.get_grid_packed()
            nx=tg.get_size(0)
            ny=tg.get_size(1)
            nz=tg.get_size(2)
            gridx=[grid[i] for i in range(0,nx)]
            gridy=[grid[i] for i in range(nx,nx+ny)]
            gridz=[grid[i] for i in range(nx+ny,nx+ny+nz)]
            
            total_size=nx*ny*nz

            if self.xset==False:
                self.xlo=gridx[0]
                self.xhi=gridx[nx-1]
                self.xset=True
            if self.yset==False:
                self.ylo=gridy[0]
                self.yhi=gridy[ny-1]
                self.yset=True
            if self.zset==False:
                self.zlo=gridz[0]
                self.zhi=gridz[nz-1]
                self.zset=True
            print('o2graph_plotter:yt-add-vol: axis limits:',
                  self.xlo,self.xhi,
                  self.ylo,self.yhi,self.zlo,self.zhi)
            
            arr=numpy.ctypeslib.as_array(data,shape=(nx,ny,nz))
            self.yt_volume_data.append(numpy.copy(arr))
            # Rescale to the internal coordinate system
            bbox=numpy.array([[(gridx[0]-self.xlo)/(self.xhi-self.xlo),
                               (gridx[nx-1]-self.xlo)/(self.xhi-self.xlo)],
                              [(gridy[0]-self.ylo)/(self.yhi-self.ylo),
                               (gridy[ny-1]-self.ylo)/(self.yhi-self.ylo)],
                              [(gridz[0]-self.zlo)/(self.zhi-self.zlo),
                               (gridz[nz-1]-self.zlo)/(self.zhi-self.zlo)]])
            self.yt_volume_bbox.append(numpy.copy(bbox))
            arr2=self.yt_volume_data[len(self.yt_volume_data)-1]
            bbox2=self.yt_volume_bbox[len(self.yt_volume_bbox)-1]

            func=yt.load_uniform_grid
            self.yt_data_sources.append(func(dict(density=arr2),
                                             arr2.shape,bbox=bbox2))
            ds=self.yt_data_sources[len(self.yt_data_sources)-1]

            self.yt_vols.append(create_volume_source(ds,field='density'))
            vol=self.yt_vols[len(self.yt_vols)-1]
            vol.log_field=False

            # Setup the transfer function
            if self.yt_tf!=0:
                vol.set_transfer_function(self.yt_tf)
                print(self.yt_tf)
            else:
                tfh=TransferFunctionHelper(ds)
                tfh.set_field('density')
                tfh.set_log(False)
                tfh.set_bounds()
                tfh.build_transfer_function()
                tfh.tf.add_layers(3)
                #tfh.plot('tf.png')
                vol.set_transfer_function(tfh.tf)
                print(tfh.tf)
                        
            if self.yt_created_scene==False:
                self.yt_create_scene()

            kname=self.yt_unique_keyname(keyname)
            self.yt_vol_keynames.append(kname)
            self.yt_scene.add_source(vol,keyname=kname)
                            
            if self.yt_created_camera==False:
                self.yt_create_camera(ds)
                
        # End of function o2graph_plotter::yt_add_vol()
        return
        
    def den_plot_anim(self,o2scl,amp,link,args):
        """Documentation for o2graph command ``den-plot-anim``:

        Create an animated density plot from a rank 3 tensor_grid
        object

        Command-line arguments: ``<x index> <y index> <z index [+'r']>
        <mp4 filename> [kwargs for imshow()]``

        Create an mp4 animation of a density plot from a
        ``tensor_grid`` object with rank 3. The first argument
        specifies which tensor index is along the x axis (either
        ``0``, ``1`` or ``2``), the second argument is the tensor
        index is along the y axis (either ``0``, ``1`` or ``2``), and
        the third argument is the tensor index which will be animated.
        If the third argument has an additional ``r`` suffix, then the
        animation will be reversed, so that the first frame
        corresponds to the largest value of the grid for the
        associated index.

        Experimental.

        """

        import matplotlib.pyplot as plot
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)

        if curr_type==b'tensor_grid':

            # Set up wrapper for get function
            amt=acol_manager(self.link2,amp)
            tg3=amt.get_tensor_grid_obj()
            rk=tg3.get_rank()
            if rk!=3:
                print("Object of type 'tensor_grid' does not have rank 3.")
                return
            sza=tg3.get_size_arr()
            nx=sza[0]
            ny=sza[1]
            nz=sza[2]
            grid_packed=tg3.get_grid_packed()
            gridx=[grid_packed[i] for i in range(0,nx)]
            gridy=[grid_packed[i+nx] for i in range(0,ny)]
            gridz=[grid_packed[i+nx+ny] for i in range(0,nz)]
            
            data=tg3.get_data()
            total_size=nx*ny*nz

            if args[0]=='0':
                xgrid=[gridx[i] for i in range(0,nx)]
                nx2=nx
            elif args[0]=='1':
                xgrid=[gridy[i] for i in range(0,ny)]
                nx2=ny
            else:
                xgrid=[gridz[i] for i in range(0,nz)]
                nx2=nz
            
            if args[1]=='0':
                ygrid=[gridx[i] for i in range(0,nx)]
                ny2=nx
            elif args[1]=='1':
                ygrid=[gridy[i] for i in range(0,ny)]
                ny2=ny
            else:
                ygrid=[gridz[i] for i in range(0,nz)]
                ny2=nz

            if args[2]=='0':
                n_frames=nx
            elif args[2]=='0r':
                n_frames=nx
            elif args[2]=='1':
                n_frames=ny
            elif args[2]=='1r':
                n_frames=ny
            elif args[2]=='2':
                n_frames=nz
            elif args[2]=='2r':
                n_frames=nz

            kwstring=''
            if len(args)>=5:
                kwstring=args[4]
            dctt=string_to_dict(kwstring)
                
            if n_frames>9999:
                print('Large number of frames (',n_frames,') not',
                      'supported in den-plot-anim.')
                return

            arr=data.reshape((nx,ny,nz))

            if self.colbar==True:
                # The animation of the colorbar messes up the
                # automatic colorbar placement, so this is a hack to
                # attempt make sure the colorbar is placed correctly
                # in all frames.
                dct=string_to_dict(self.fig_dict)
                if ('right_margin' not in dct.keys() or
                    dct['right_margin']<0.1):
                    print('xxx')
                    dct['right_margin']=0.15
                if 'top_margin' not in dct.keys():
                    dct['top_margin']=0.06
                if 'left_margin' not in dct.keys():
                    dct['left_margin']=0.14
                if 'bottom_margin' not in dct.keys():
                    dct['bottom_margin']=0.12
                rm=dct['right_margin']
                lm=dct['left_margin']
                tm=dct['top_margin']
                bm=dct['bottom_margin']
                if self.verbose>1:
                    print('o2graph_plotter.den_plot_anim(): margins',
                          rm,lm,tm,bm)
                if self.canvas_flag==False:
                    if 'fontsize' not in dct.keys():
                        dct['fontsize']=self.font
                    (self.fig,self.axes)=default_plot(**dct)
                    # Plot limits
                    if self.xset==True:
                        self.axes.set_xlim(self.xlo,self.xhi)
                    if self.yset==True:
                        self.axes.set_ylim(self.ylo,self.yhi)
                    # Set log mode for x and y axes if requested
                    if self.logx==True:
                        self.axes.set_xscale('log')
                    if self.logy==True:
                       self.axes.set_yscale('log')
                    self.canvas_flag=True
            else:
                # If there's no colorbar, then we can use
                # the standard approach
                if self.canvas_flag==False:
                    self.canvas()
                
            if self.logx==True:
                for i in range(0,len(xgrid)):
                    xgrid[i]=math.log(xgrid[i],10)
                    
            if self.logy==True:
                for i in range(0,len(ygrid)):
                    ygrid[i]=math.log(ygrid[i],10)

            for k in range(0,n_frames):
                if args[2]=='0':
                    sl=arr[k,:,:]
                elif args[2]=='0r':
                    sl=arr[n_frames-1-k,:,:]
                elif args[2]=='1':
                    sl=arr[:,k,:]
                elif args[2]=='0r':
                    sl=arr[:,n_frames-1-k,:]
                elif args[2]=='2':
                    sl=arr[:,:,k]
                elif args[2]=='2r':
                    sl=arr[:,:,n_frames-1-k]
                sl=sl.transpose()
 
                if self.logz==True:
                    fail_found=False
                    for i in range(0,len(ygrid)):
                        for j in range(0,len(xgrid)):
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
                                
                # If the z range was specified, truncate all values
                # outside that range (this truncation is done after
                # the application of the log above)
                if self.zset==True:
                    for i in range(0,ny2):
                        for j in range(0,nx2):
                            if sl[i][j]>self.zhi:
                                sl[i][j]=self.zhi
                            elif sl[i][j]<self.zlo:
                                sl[i][j]=self.zlo
                            
                diffs_x=[xgrid[i+1]-xgrid[i] for i in range(0,len(xgrid)-1)]
                mean_x=numpy.mean(diffs_x)
                std_x=numpy.std(diffs_x)
                diffs_y=[ygrid[i+1]-ygrid[i] for i in range(0,len(ygrid)-1)]
                mean_y=numpy.mean(diffs_y)
                std_y=numpy.std(diffs_y)
            
                if std_x/mean_x>1.0e-4 or std_x/mean_x>1.0e-4:
                    print('Warning in o2graph::o2graph_plotter::'+
                          'den_plot_anim():')
                    print('  Nonlinearity of x or y grid is greater than '+
                          '10^{-4}.')
                    print('  Value of std(diff_x)/mean(diff_x): %7.6e .' %
                          (std_x/mean_x))
                    print('  Value of std(diff_y)/mean(diff_y): %7.6e .' %
                          (std_y/mean_y))
                    print('  The density plot may not be properly scaled.')
                
                tmp1=xgrid[0]-(xgrid[1]-xgrid[0])/2
                tmp2=xgrid[nx2-1]+(xgrid[nx2-1]-xgrid[nx2-2])/2
                tmp3=ygrid[0]-(ygrid[1]-ygrid[0])/2
                tmp4=ygrid[ny2-1]+(ygrid[ny2-1]-ygrid[ny2-2])/2
                
                if k>0:
                    # It's important to remove the last image and
                    # colorbar to free up the space. We have to
                    # remmove the colorbar first, then the image.
                    if self.colbar==True:
                        self.cbar.remove()
                        del self.cbar
                    self.last_image.remove()
                    del self.last_image
                        
                self.last_image=self.axes.imshow(sl,interpolation='nearest',
                                                 origin='lower',
                                                 extent=[tmp1,tmp2,
                                                         tmp3,tmp4],
                                                 aspect='auto',**dctt)
                
                if self.colbar==True:
                    dpa_cax2=self.fig.add_axes([1.0-rm*0.9,
                                                bm,rm*0.3,
                                                1.0-bm-tm])
                    self.cbar=self.fig.colorbar(self.last_image,
                                                cax=dpa_cax2)
                    self.cbar.ax.tick_params('both',length=6,width=1,
                                             which='major')
                    self.cbar.ax.tick_params(labelsize=self.font*0.8)
                    
                if n_frames<10:
                    fname='/tmp/dpa_'+str(k)+'.png'
                elif n_frames<100:
                    if k<10:
                        fname='/tmp/dpa_0'+str(k)+'.png'
                    else:
                        fname='/tmp/dpa_'+str(k)+'.png'
                elif n_frames<1000:
                    if k<10:
                        fname='/tmp/dpa_00'+str(k)+'.png'
                    elif k<100:
                        fname='/tmp/dpa_0'+str(k)+'.png'
                    else:
                        fname='/tmp/dpa_'+str(k)+'.png'
                elif n_frames<10000:
                    if k<10:
                        fname='/tmp/dpa_000'+str(k)+'.png'
                    elif k<100:
                        fname='/tmp/dpa_00'+str(k)+'.png'
                    elif k<1000:
                        fname='/tmp/dpa_0'+str(k)+'.png'
                    else:
                        fname='/tmp/dpa_'+str(k)+'.png'
                print('Saving to',fname)
                plot.savefig(fname)

                # End of loop, continue to next frame

            # Now after loop, compile frames into a movie
            prefix='/tmp/dpa_'
            suffix='.png'
            mov_fname=args[3]
            if n_frames>=1000:
                self.mp4([prefix+'%04d'+suffix,mov_fname])
            elif n_frames>=100:
                self.mp4([prefix+'%03d'+suffix,mov_fname])
            elif n_frames>=10:
                self.mp4([prefix+'%02d'+suffix,mov_fname])
            else:
                self.mp4([prefix+'%01d'+suffix,mov_fname])

            # End of "if curr_type==b'tensor_grid':"
                
        # End of function o2graph_plotter::den_plot_anim()
        return
        
    def help_func(self,o2scl,amp,link,args):
        """
        Function to process the help command.
        """

        amt=acol_manager(self.link2,amp)
        cl=amt.get_cl()
        
        # The command we're looking for help on (if specified)
        cmd=''

        # vt100 inits
        ter=terminal_py()
        str_line=ter.horiz_line()

        # Get current type
        curr_type=o2scl_get_type(o2scl,amp,self.link2)

        if len(args)==1:
            # If just a command is specified
            
            cmd=args[0]
            
        elif len(args)==2:
            # If both a type and command are specified
                        
            curr_type=args[0]
            cmd=args[1]

        # True if the user-specified arguments were matched
        match=False

        # Handle the case of an o2graph command from the base list
        for line in base_list:
            if cmd==line[0]:
                match=True
                reformat_python_docs(cmd,line[1],amp,self.link2)
        
        # Handle the case of an o2graph command from the
        # extra list
        if match==False:
            for line in extra_list:
                if ((curr_type==line[0] or
                     curr_type==force_bytes(line[0])) and
                    cmd==line[1]):
                    match=True
                    reformat_python_docs_type(curr_type,cmd,line[2],amp,
                                              self.link2)

        # Handle the case of an o2graph command from the
        # extra list without a matching type
        if match==False:
            for line in extra_list:
                if cmd==line[1]:
                    match=True
                    print('\n'+str_line)
                    #print('here2')
                    reformat_python_docs_type(line[0],cmd,line[2],amp,
                                              self.link2)
                    
        # If we haven't matched yet, check for get/set parameters
        if match==False:
            for line in param_list:
                if cmd==line[0]:
                    match=True
                    print('O2graph parameter modified by the get and set',
                          'commands: '+line[0]+'\n')
                    
                    tempx_arr=line[1].split('\n')
                    for j in range(0,len(tempx_arr)):
                        if len(tempx_arr[j])<79:
                            print(tempx_arr[j])
                        else:
                            str_list=textwrap.wrap(tempx_arr[j],79)
                            for i in range (0,len(str_list)):
                                print(str_list[i])

        # If we haven't matched yet, check for get/set parameters
        # from yt
        if match==False:
            for line in yt_param_list:
                if cmd==line[0]:
                    match=True
                    print('yt parameter modified by the get and',
                          'set commands: '+line[0]+'\n')
                    
                    tempx_arr=line[1].split('\n')
                    for j in range(0,len(tempx_arr)):
                        if len(tempx_arr[j])<79:
                            print(tempx_arr[j])
                        else:
                            str_list=textwrap.wrap(tempx_arr[j],79)
                            for i in range (0,len(str_list)):
                                print(str_list[i])

        # Handle o2graph topics
        if (cmd=='markers') and len(args)==1:
            marker_list()
            match=True
            
        if (len(args)==1 or len(args)==2) and args[0]=='markers-plot':
            if len(args)==2:
                markers_plot(args[1])
            else:
                markers_plot()
            match=True

        # Handle acol topics and types
        if match==False:
            if len(args)==1:
                if amt.help_found(args[0],'')==True:
                    self.gen_acol(o2scl,amp,self.link2,'help',args)
                    match=True
            elif len(args)==2 and amt.help_found(args[0],args[1])==True:
                self.gen_acol(o2scl,amp,self.link2,'help',args)
                match=True

        # If there was no match, do a command list
        if match==False:
            
            print('o2graph: A data viewing and '+
                  'processing program for '+ter.bold()+
                  'O2scl'+ter.default_fgbg()+
                  '.\n  Version: '+version)
            print(' ')
            if curr_type==b'':
                print('List of command-line options which',
                      'do not require a current object:\n')
            else:
                # AWS removed decode on 10/27/2020
                # and converted to force_string() on 5/6/22
                print('List of command-line options',
                      '(current object type is',
                      force_string(amt.get_type_color())+
                      force_string(curr_type)+
                      force_string(amt.get_default_color())+'):\n')
            full_list=[]

            tlist=cl.get_option_list()
            for j in range(0,len(tlist)):
                desc=cl.option_short_desc(tlist[j])
                full_list.append([tlist[j],desc])

            for line2 in base_list:
                short=reformat_python_docs(line2[0],line2[1],amp,
                                           self.link2,True)
                full_list.append([force_bytes(line2[0]),
                                  force_bytes(short)])

            if curr_type!='':
                for line in extra_list:
                    if force_bytes(line[0])==curr_type:
                        #print('here3')
                        short=reformat_python_docs_type(curr_type,line[1],
                                                        line[2],amp,
                                                        self.link2,True)
                        full_list.append([force_bytes(line[1]),
                                          force_bytes(short)])

            full_list2=sorted(full_list,key=lambda x: x[0])
            max_len=0
            for k in range(0,len(full_list2)):
                full_list2[k][0]=(force_string(amt.get_command_color())+
                                  full_list2[k][0].decode('utf-8')+
                                  force_string(amt.get_default_color()))
                full_list2[k][1]=full_list2[k][1].decode('utf-8')
                if length_without_colors(full_list2[k][0])>max_len:
                    max_len=length_without_colors(full_list2[k][0])
            for k in range(0,len(full_list2)):
                strt='  '
                extra=max_len-length_without_colors(full_list2[k][0])
                strt+='-'+full_list2[k][0]
                for ij in range(0,extra):
                    strt+=' '
                strt+=' '+full_list2[k][1]
                print(strt)
            print('\n'+str_line)
            help_topics=sorted(acol_help_topics+o2graph_help_topics)
                
            strt='Additional help topics: '
            for j in range(0,len(help_topics)):
                if j<len(help_topics)-1:
                    strt+=(force_string(amt.get_help_color())+
                           help_topics[j]+
                           force_string(amt.get_default_color())+', ')
                else:
                    strt+=('and '+force_string(amt.get_help_color())+
                           help_topics[j]+
                           force_string(amt.get_default_color())+'.')
                        
            tlist=wrap_line(strt)
            for j in range(0,len(tlist)):
                print(tlist[j])
            
        # If the user specified 'help set', then print
        # the o2graph parameter documentation
        if (cmd=='set' or cmd=='get') and len(args)==1:
            self.print_param_docs(amt)

        # End of function o2graph_plotter::help_func()
        return
        
    def yt_tf_func(self,args):
        """
        Documentation for o2graph command ``yt-tf``:

        Edit the yt transfer function.

        Command-line arguments: ``<mode> <args>``

        To create a new transfer function, use 'new' for <mode> and
        the remaining <args> are <min> <max> [nbins] .To add a
        Gaussian, use 'gauss' for <mode> and <args> are <loc> <width>
        <red> <green> <blue>, and <alpha>. To add a step function, use
        'step' <low> <high> <red> <green> <blue>, and <alpha>. To plot
        the transfer function, use 'plot' <filename>.
        """

        if len(args)==0:
            print('Function yt_tf_func() requires arguments.')
            print('  For a new transfer function, args should be '+
                  "('new','min','max') or ('new','min','max','nbins')")
            print('  To add a Gaussian, args should be '+
                  "('gauss','loc','width','red','green','blue','alpha')")
            print('  To add a step function, args should be '+
                  "('step','low','high','red','green','blue','alpha')")
            print('  To plot the transfer function, args should be '+
                  "('plot','filename')")
            return

        if args[0]=='new':
            if len(args)<3:
                print('yt-tf new requires 3 arguments.')
                return
            import yt
            print('o2graph:yt-tf: New transfer function.')
            print('o2graph:yt-tf: min:',args[1],
                  'max:',args[2])
            if len(args)>=4:
                self.yt_tf=yt.ColorTransferFunction((float(eval(args[1])),
                                                     float(eval(args[2]))),
                                                    nbins=int(eval(args[3])),
                                                    grey_opacity=False)
            else:
                self.yt_tf=yt.ColorTransferFunction((float(eval(args[1])),
                                                     float(eval(args[2]))),
                                                    grey_opacity=False)
                
        elif args[0]=='gauss':
            if len(args)<7:
                print('yt-tf gauss requires 6 arguments.')
                return
            print('o2graph:yt-tf: Adding Gaussian to',
                  'transfer function.')
            print('o2graph:yt-tf: location:',args[1],
                  'width:',args[2])
            print('o2graph:yt-tf: r,g,b,a:',
                  args[3],args[4],
                  args[5],args[6])
            self.yt_tf.add_gaussian(float(eval(args[1])),
                                    float(eval(args[2])),
                                    [float(eval(args[3])),
                                     float(eval(args[4])),
                                     float(eval(args[5])),
                                     float(eval(args[6]))])
            
        elif args[0]=='plot':
            if len(args)<2:
                print('yt-tf plot requires 1 argument.')
                return
            print('o2graph:yt-tf: Storing',
                  'transfer function in file',args[1])
            self.yt_tf.plot(args[1])

        elif args[0]=='step':
            if len(args)<7:
                print('yt-tf step requires 6 arguments.')
                return
            print('o2graph:yt-tf: Adding step to',
                  'transfer function.')
            print('o2graph:yt-tf: start:',args[1],
                  'stop:',args[2])
            print('o2graph:yt-tf: r,g,b,a:',
                  args[3],args[4],
                  args[5],args[6])
            self.yt_tf.add_step(float(eval(args[1])),
                                float(eval(args[2])),
                                [float(eval(args[3])),
                                 float(eval(args[4])),
                                 float(eval(args[5])),
                                 float(eval(args[6]))])

        # End of function o2graph_plotter::yt_tf_func()
        return

    def yt_path_func(self,o2scl,amp,args):
        """
        Documentation for o2graph command ``yt-path``:

        Add a path to the yt animation.

        Command-line arguments: ``<type> <number of frames> 
        <other parameters>``

        The ``yt-path`` adds a path to a yt animation. To rotate the
        camera around the z-axis, use 'yaw' <n_frames> <angle>, where
        angle is a fraction of a full rotation to perform by the end
        of the animation. To zoom the camera, use 'zoom' <n_frames>
        <factor> ,where factor is the total zoom factor to apply over
        all n_frames. To move the camera along a line, use 'move'
        <n_frames> <[dest_x,dest_y,dest_z]> <'internal' or 'user'>,
        where the third argument is the destination in either the
        internal or user-specified coordinate system. To turn the
        camera without moving it, use 'turn' <n_frames>
        <[foc_x,foc_y,foc_z]> <'internal' or 'user'>. Executing
        'yt-path reset' resets the yt animation path to an empty list
        (for no animation).

        """

        self.yt_path.append(args)
        print('yt_path is',self.yt_path)
        
        return

    def yt_ann_func(self,o2scl,amp,args):
        """Documentation for o2graph command ``yt-ann``:

        Annotate a yt rendering (experimental).

        Command-line arguments: ``[args]``
        
        The ``yt-ann`` command adds a list of o2graph commands that
        can be used to annotate a yt rendering. Annotations are normal
        o2graph 2D plotting commands built upon a coordinate system
        with (0,0) as the lower-left corner of the image and (1,1) as
        the upper-right corner. Arguments for ``yt-ann`` may include
        dashes but must end with the word 'end'.
        
        For example::

          -yt-ann -text 0.1 0.95 \"Ann. example\" color=w,ha=left end
        
        The list or arguments in `args` must end with 'end'. 
        If `args` contains only one entry ('end'), then the
        list of annotations is cleared.

        """

        if len(args)==1 and force_bytes(args[0])==b'end':
            print('Clearing all yt annotations.')
        else:
            for i in range(0,len(args)):
                if force_bytes(args[i])!=b'end':
                    self.yt_ann.append(args[i])
            print('yt_ann is',self.yt_ann)
        
        return

    def yt_scatter(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``yt-scatter``:

        For objects of type ``table``:

        Add scattered points to a yt scene
        
        Command-line arguments: ``<x column> <y column> <z column> 
        [size column] [red column] [green column] [blue column] 
        [alpha column]``

        Add a series of points to a yt scene. If a volume has not yet
        been added, then a default volume is added. If the x, y-, or
        z-axis limits have not yet been set, then they are set by the
        limits of the data. If the size column is unspecified, 'none',
        or 'None', then the default value of 3 is used. If the color
        columns are unspecified, 'none' or 'None', then [1,1,1] is
        used, and finally the default for the alpha column is 0.5. If
        any of the values for the color columns are less than zero or
        greater than 1, then that color column is rescaled to [0,1].
        """

        if len(args)<3:
            print('Function yt_scatter() requires three ',
                  'column arguments.')
            return

        column_x=args[0]
        column_y=args[1]
        column_z=args[2]
        size_column=''
        red_column=''
        green_column=''
        blue_column=''
        alpha_column=''
        if len(args)>=4:
            size_column=args[3]
        if len(args)>=5:
            red_column=args[4]
        if len(args)>=6:
            green_column=args[5]
        if len(args)>=7:
            blue_column=args[6]
        if len(args)>=8:
            alpha_column=args[7]
        
        curr_type=o2scl_get_type(o2scl,amp,self.link2)

        if curr_type==b'table':
            if self.yt_check_backend()==1:
                return

            import yt
            from yt.visualization.volume_rendering.api \
                import PointSource

            failed=False
            
            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            ptrx=tab[force_bytes(column_x)]
            ptry=tab[force_bytes(column_y)]
            ptrz=tab[force_bytes(column_z)]

            if (force_bytes(size_column)==b'None' or
                force_bytes(size_column)==b'none'):
                size_column=''
            if (force_bytes(red_column)==b'None' or
                force_bytes(red_column)==b'none'):
                red_column=''
            if (force_bytes(green_column)==b'None' or
                force_bytes(green_column)==b'none'):
                green_column=''
            if (force_bytes(blue_column)==b'None' or
                force_bytes(blue_column)==b'none'):
                blue_column=''
            if (force_bytes(alpha_column)==b'None' or
                force_bytes(alpha_column)==b'none'):
                alpha_column=''

            print('size,red,green,blue,alpha:',size_column,red_column,
                  green_column,blue_column,alpha_column)
            
            if size_column!='':
                ptrs=tab[force_bytes(size_column)]
                
            if red_column!='':
                ptrr=tab[force_bytes(red_column)]
                
            if green_column!='':
                ptrg=tab[force_bytes(green_column)]
                
            if blue_column!='':
                ptrb=tab[force_bytes(blue_column)]
                
            if alpha_column!='':
                ptra=tab[force_bytes(alpha_column)]

            if red_column!='' and blue_column!='' and green_column!='':
                rescale_r=False
                rescale_g=False
                rescale_b=False
                for i in range(0,len(ptrr)):
                    if ptrr[i]<0.0 or ptrr[i]>1.0:
                        rescale_r=True
                    if ptrg[i]<0.0 or ptrg[i]>1.0:
                        rescale_g=True
                    if ptrb[i]<0.0 or ptrb[i]>1.0:
                        rescale_b=True
                if rescale_r:
                    min_r=ptrr[0]
                    max_r=ptrr[0]
                    for i in range(0,len(ptrr)):
                        if ptrr[i]<min_r:
                            min_r=ptrr[i]
                        if ptrr[i]>max_r:
                            max_r=ptrr[i]
                if rescale_g:
                    min_g=ptrg[0]
                    max_g=ptrg[0]
                    for i in range(0,len(ptrg)):
                        if ptrg[i]<min_g:
                            min_g=ptrg[i]
                        if ptrg[i]>max_g:
                            max_g=ptrg[i]
                if rescale_b:
                    min_b=ptrb[0]
                    max_b=ptrb[0]
                    for i in range(0,len(ptrb)):
                        if ptrb[i]<min_b:
                            min_b=ptrb[i]
                        if ptrb[i]>max_b:
                            max_b=ptrb[i]
                if rescale_r:
                    print('Rescaling red range   (%0.6e,%0.6e) to (0,1)' %
                          (min_r,max_r))
                    for i in range(0,len(ptrr)):
                        ptrr[i]=(ptrr[i]-min_r)/(max_r-min_r)
                if rescale_g:
                    print('Rescaling green range (%0.6e,%0.6e) to (0,1)' %
                          (min_g,max_g))
                    for i in range(0,len(ptrg)):
                        ptrg[i]=(ptrg[i]-min_g)/(max_g-min_g)
                if rescale_b:
                    print('Rescaling blue range  (%0.6e,%0.6e) to (0,1)' %
                          (min_b,max_b))
                    for i in range(0,len(ptrb)):
                        ptrb[i]=(ptrb[i]-min_b)/(max_b-min_b)
                
            if self.xset==False:
                self.xlo=ptrx[0]
                self.xhi=ptrx[0]
                for i in range(0,len(ptrx)):
                    if ptrx[i]<self.xlo:
                        self.xlo=ptrx[i]
                    if ptrx[i]>self.xhi:
                        self.xhi=ptrx[i]
                print('Set xlimits to (%0.6e,%0.6e)' % (self.xlo,self.xhi))
                self.xset=True
            if self.yset==False:
                self.ylo=ptry[0]
                self.yhi=ptry[0]
                for i in range(0,len(ptry)):
                    if ptry[i]<self.ylo:
                        self.ylo=ptry[i]
                    if ptry[i]>self.yhi:
                        self.yhi=ptry[i]
                print('Set ylimits to (%0.6e,%0.6e)' % (self.ylo,self.yhi))
                self.yset=True
            if self.zset==False:
                self.zlo=ptrz[0]
                self.zhi=ptrz[0]
                for i in range(0,len(ptrz)):
                    if ptrz[i]<self.zlo:
                        self.zlo=ptrz[i]
                    if ptrz[i]>self.zhi:
                        self.zhi=ptrz[i]
                print('Set zlimits to (%0.6e,%0.6e)' % (self.zlo,self.zhi))
                self.zset=True
            x_range=self.xhi-self.xlo
            y_range=self.yhi-self.ylo
            z_range=self.zhi-self.zlo

            icnt=0
            if self.yt_scene!=0:
                for key, value in self.yt_scene.sources.items():
                    print('yt-source-list',icnt,key,type(value))
                    icnt=icnt+1
            if icnt==0:
                self.yt_def_vol()
            
            pts=[]
            cols=[]
            sizes=[]
            for i in range(0,len(ptrx)):
                pts.append([(ptrx[i]-self.xlo)/x_range,
                            (ptry[i]-self.ylo)/y_range,
                            (ptrz[i]-self.zlo)/z_range])
                if red_column=='' or blue_column=='' or green_column=='':
                    cols.append([1.0,1.0,1.0,0.5])
                else:
                    if alpha_column=='':
                        cols.append([ptrr[i],ptrg[i],ptrb[i],1.0])
                    else:
                        cols.append([ptrr[i],ptrg[i],ptrb[i],ptra[i]])
                if size_column=='':
                    sizes.append(3)
                else:
                    sizes.append(int(ptrs[i]))
            pts2=numpy.array(pts)
            cols2=numpy.array(cols)
            sizes2=numpy.array(sizes)
            #print('cols2:',cols2[0],cols2[1],cols2[len(cols2)-1])
            #print('sizes2:',sizes2[0],sizes2[1],sizes2[len(sizes2)-1])

            if len(args)>=9:
                ps=PointSource(pts2,colors=cols2,radii=sizes2,
                               **string_to_dict(args[8]))
            else:
                ps=PointSource(pts2,colors=cols2,radii=sizes2)

            #if self.yt_created_scene==False:
            #self.yt_create_scene()

            print('o2graph:yt-scatter: Adding point source.')
            kname=self.yt_unique_keyname('o2graph_scatter')
            self.yt_scene.add_source(ps,keyname=kname)
                        
            #if self.yt_created_camera==False:
            #self.yt_create_camera(ps)

        else:
            # The object curr_type is a bytes object, so we just use
            # commas and avoid trying to add the strings together
            print('Command yt-scatter does not work with type',
                  curr_type,'.')
            
        # End of function o2graph_plotter::yt_scatter()
        return
        
    def yt_vertex_list(self,o2scl,amp,link,args):
        """
        Documentation for o2graph command ``yt-vertex-list``:
        
        For objects of type ``table``:

        Draw a line from a series of vertices in a table.

        Command-line arguments: ``<x column> <y column> <z column> 
        [kwargs]``
        
        Create a series of yt LineSource objects in a visualization
        using the three specified columns as vertices. One line segment
        will be drawn from the values in the first row to the values in
        the second row, one line segment from the second row to the
        third row, and so on.
        """

        if len(args)<3:
            print('Function yt_vertex_list() requires three ',
                  'column arguments.')
            return

        column_x=args[0]
        column_y=args[1]
        column_z=args[2]
        
        icnt=0
        if self.yt_scene!=0:
            for key, value in self.yt_scene.sources.items():
                print('yt-source-list',icnt,key,type(value))
                icnt=icnt+1
        # If there are no yt sources yet, then create a
        # default volume object
        if icnt==0:
            self.yt_def_vol()

        curr_type=o2scl_get_type(o2scl,amp,self.link2)

        if curr_type==b'table':
            if self.yt_check_backend()==1:
                return

            import yt
            from yt.visualization.volume_rendering.api \
                import LineSource

            failed=False
            
            amt=acol_manager(self.link2,amp)
            tab=amt.get_table_obj()
            ptrx=tab[force_bytes(column_x)]
            ptry=tab[force_bytes(column_y)]
            ptrz=tab[force_bytes(column_z)]

            if self.xset==False:
                self.xlo=ptrx[0]
                self.xhi=ptrx[0]
                for i in range(0,idx.value):
                    if ptrx[i]<self.xlo:
                        self.xlo=ptrx[i]
                    if ptrx[i]>self.xhi:
                        self.xhi=ptrx[i]
                print('Set xlimits to (%0.6e,%0.6e)' % (self.xlo,self.xhi))
                self.xset=True
            if self.yset==False:
                self.ylo=ptry[0]
                self.yhi=ptry[0]
                for i in range(0,idy.value):
                    if ptry[i]<self.ylo:
                        self.ylo=ptry[i]
                    if ptry[i]>self.yhi:
                        self.yhi=ptry[i]
                print('Set ylimits to (%0.6e,%0.6e)' % (self.ylo,self.yhi))
                self.yset=True
            if self.zset==False:
                self.zlo=ptrz[0]
                self.zhi=ptrz[0]
                for i in range(0,idz.value):
                    if ptrz[i]<self.zlo:
                        self.zlo=ptrz[i]
                    if ptrz[i]>self.zhi:
                        self.zhi=ptrz[i]
                print('Set zlimits to (%0.6e,%0.6e)' % (self.zlo,self.zhi))
                self.zset=True
            x_range=self.xhi-self.xlo
            y_range=self.yhi-self.ylo
            z_range=self.zhi-self.zlo

            pts=[]
            cols=[]
            sizes=[]
            for i in range(0,idx.value-1):
                pts.append([[(ptrx[i]-self.xlo)/x_range,
                             (ptry[i]-self.ylo)/y_range,
                             (ptrz[i]-self.zlo)/z_range],
                            [(ptrx[i+1]-self.xlo)/x_range,
                             (ptry[i+1]-self.ylo)/y_range,
                             (ptrz[i+1]-self.zlo)/z_range]])
                cols.append([1.0,1.0,1.0,1.0])
            pts2=numpy.array(pts)
            cols2=numpy.array(cols)

            ls=LineSource(pts2,cols2)

            #if self.yt_created_scene==False:
            #self.yt_create_scene()

            print('o2graph:yt-vertex-list: Adding point source.')
            kname=self.yt_unique_keyname('o2graph_vertex_list')
            self.yt_scene.add_source(ls,keyname=kname)
                        
            #if self.yt_created_camera==False:
            #self.yt_create_camera(ps)

        else:
            print('Command yt-vertex-list does not work with type',
                  curr_type+'.')
            
        # End of function o2graph_plotter::yt_vertex_list()
        return
        
    def yt_mesh(self,o2scl,amp,link,args):
        """
        Plot a mesh from vertices specified by a slice of O2scl
        table3d object.
        """

        if len(args)<1:
            print('Function yt_mesh() requires a slice ',
                  'column arguments.')
            return

        slc=args[0]

        amt=acol_manager(self.link2,amp)
        curr_type=amt.get_type()
            
        if curr_type==b'table3d':
            if self.yt_check_backend()==1:
                return

            import yt
            from yt.visualization.volume_rendering.api \
                import LineSource

            t3d=amt.get_table3d_obj()
            sl=t3d.get_slice(slc).to_numpy()
            xv=[t3d.get_grid_x(i) for i in
                range(0,t3d.get_nx())]
            yv=[t3d.get_grid_y(i) for i in
                range(0,t3d.get_ny())]
            
            if self.xset==False:
                self.xlo=min(xv)
                self.xhi=max(xv)
                print('Function yt-mesh set xlimits to (%0.6e,%0.6e)' %
                      (self.xlo,self.xhi))
                self.xset=True
            if self.yset==False:
                self.ylo=min(yv)
                self.yhi=max(yv)
                print('Function yt-mesh set ylimits to (%0.6e,%0.6e)' %
                      (self.ylo,self.yhi))
                self.yset=True
            if self.zset==False:
                self.zlo=numpy.min(sl)
                self.zhi=numpy.max(sl)
                print('Function yt-mesh set zlimits to (%0.6e,%0.6e)' %
                      (self.zlo,self.zhi))
                self.zset=True
            x_range=self.xhi-self.xlo
            y_range=self.yhi-self.ylo
            z_range=self.zhi-self.zlo

            icnt=0
            if self.yt_scene!=0:
                for key, value in self.yt_scene.sources.items():
                    print('yt-source-list',icnt,key,type(value))
                    icnt=icnt+1
            # If there are no yt sources yet, then create a
            # default volume object
            if icnt==0:
                self.yt_def_vol()

            
            pts=[]
            cols=[]
            sizes=[]
            for i in range(0,len(xv)-1):
                for j in range(0,len(yv)):
                    pts.append([[(xv[i]-self.xlo)/x_range,
                                       (yv[j]-self.ylo)/y_range,
                                       (sl[i][j]-self.zlo)/z_range],
                                      [(xv[i+1]-self.xlo)/x_range,
                                       (yv[j]-self.ylo)/y_range,
                                       (sl[i+1][j]-self.zlo)/z_range]])
                    cols.append([1.0,1.0,1.0,1.0])
                    
            for i in range(0,len(xv)):
                for j in range(0,len(yv)-1):
                    pts.append([[(xv[i]-self.xlo)/x_range,
                                       (yv[j]-self.ylo)/y_range,
                                       (sl[i][j]-self.zlo)/z_range],
                                      [(xv[i]-self.xlo)/x_range,
                                       (yv[j+1]-self.ylo)/y_range,
                                       (sl[i][j+1]-self.zlo)/z_range]])
                    cols.append([1.0,1.0,1.0,1.0])
                    
            pts2=numpy.array(pts)
            cols2=numpy.array(cols)
            #print(pts2,cols2)

            ls=LineSource(pts2,cols2)

            if self.yt_created_scene==False:
                self.yt_create_scene()

            kname=self.yt_unique_keyname('o2graph_mesh')
            print('o2graph:yt-mesh: Adding line source '+kname+'.')
            self.yt_scene.add_source(ls,keyname=kname)
                        
        else:
            print('Command yt-mesh does not work with type',
                  curr_type+'.')
            
        # End of function o2graph_plotter::yt_mesh()
        return
        
    def commands(self,o2scl,amp,link,args):
        """
        Output the currently available commands.
        """

        amt=acol_manager(self.link2,amp)
        ter=terminal_py()
        cl=amt.get_cl()
        
        if len(args)>0 and args[0]=='all':

            print('Commands from acol which do not require a current',
                  'object:\n')

            old_type=amt.get_type()
            amt.command_del(old_type)
            amt.command_add(b'')
            list_temp=cl.get_option_list()
            base_acol_comm_list=[]
            for i in range(0,len(list_temp)):
                base_acol_comm_list.append(list_temp[i])
            amt.command_del(b'')
            amt.command_add(old_type)
            
            base_acol_comm_list=sorted(base_acol_comm_list)
            comm_list=[]
            for i in range(0,len(base_acol_comm_list)):
                st=force_string(base_acol_comm_list[i])
                comm_list.append(ter.cmd_str(st,amt))
            
            comm_rows=screenify_py(comm_list)
            for i in range(0,len(comm_rows)):
                print(comm_rows[i])

            print(' ')
            
            print('O2graph commands which do not require a current',
                  'object:\n')

            comm_list=[]
            for line in base_list:
                comm_list.append(force_bytes(line[0]))
            comm_list_dec=sorted(comm_list)
            for i in range(0,len(comm_list_dec)):
                comm_list_dec[i]=ter.cmd_str(comm_list_dec[i].decode('utf-8'),
                                             amt)
            comm_rows=screenify_py(comm_list_dec)
            for i in range(0,len(comm_rows)):
                print(comm_rows[i])
                
            print(' ')

            for this_type in acol_types:
                
                print('Acol and o2graph commands for an object of type '+
                      ter.type_str(force_string(this_type),amt)+':\n')
                
                old_type=amt.get_type()
                amt.command_del(old_type)
                amt.command_add(force_bytes(this_type))
                temp_list=cl.get_option_list()
                comm_list=[]
                for i in range(0,len(temp_list)):
                    comm_list.append(temp_list[i])
                amt.command_del(force_bytes(this_type))
                amt.command_add(old_type)
                
                for line in extra_list:
                    if (this_type==line[0] or
                        this_type==force_bytes(line[0])):
                        comm_list.append(force_bytes(line[1]))

                comm_list2=sorted(comm_list)
                for comm_entry in base_acol_comm_list:
                    if comm_entry in comm_list:
                        comm_list2.remove(comm_entry)

                if len(comm_list2)>0:
                    for i in range(0,len(comm_list2)):
                        comm_list2[i]=ter.cmd_str(comm_list2[i].decode('utf-8'),
                                                  amt)
                    comm_rows=screenify_py(comm_list2)
                    for i in range(0,len(comm_rows)):
                        print(comm_rows[i])
                else:
                    print('<none>')
                    
                print(' ')
            
        elif len(args)>0:
            
            curr_type=args[0]

            if curr_type not in acol_types:
                print("Command 'commands' cannot find type ",curr_type+'.')
                print('List of valid types:')
                print('')
                print(acol_types)
                return

            old_type=amt.get_type()
            amt.command_del(old_type)
            amt.command_add(force_bytes(curr_type))
            temp_list=cl.get_option_list()
            comm_list=[]
            for i in range(0,len(temp_list)):
                comm_list.append(temp_list[i])
            amt.command_del(force_bytes(curr_type))
            amt.command_add(old_type)
                
            # comm_list is the list of acol commands for this type
            print('Commands from acol for objects of type',
                  ter.type_str(curr_type,amt)+':')
            print('')
            
            comm_list2=sorted(comm_list)
            for i in range(0,len(comm_list2)):
                comm_list2[i]=ter.cmd_str(comm_list2[i].decode('utf-8'),
                                          amt)
            comm_rows=screenify_py(comm_list2)
            for i in range(0,len(comm_rows)):
                print(comm_rows[i])
            print('')

            print('Commands from o2graph which do not require a current',
                  'object.')
            print('')
            comm_list=[]
            for line in base_list:
                comm_list.append(force_bytes(line[0]))

            comm_list2=sorted(comm_list)
            for i in range(0,len(comm_list2)):
                comm_list2[i]=ter.cmd_str(comm_list2[i].decode('utf-8'),
                                          amt)
            comm_rows=screenify_py(comm_list2)
            for i in range(0,len(comm_rows)):
                print(comm_rows[i])
            print('')
                
            print('Commands from o2graph for objects of type',
                  ter.type_str(curr_type,amt)+':')
            print('')
            comm_list=[]
            for line in extra_list:
                if (curr_type==line[0] or
                    curr_type==force_bytes(line[0])):
                    comm_list.append(force_bytes(line[1]))

            comm_list2=sorted(comm_list)
            for i in range(0,len(comm_list2)):
                comm_list2[i]=ter.cmd_str(comm_list2[i].decode('utf-8'),
                                          amt)
            comm_rows=screenify_py(comm_list2)
            for i in range(0,len(comm_rows)):
                print(comm_rows[i])
                        
        else:

            curr_type=o2scl_get_type(o2scl,amp,self.link2)

            if curr_type==b'':
                print('O2graph commands which do not require a '+
                      'current object.')
            else:
                print('O2graph commands for an object of type '+
                      ter.type_str(curr_type.decode('utf-8'),amt)+':\n')
            
            comm_list=cl.get_option_list().to_list()
            
            for line in base_list:
                comm_list.append(force_bytes(line[0]))
            for line in extra_list:
                if (curr_type==line[0] or
                    curr_type==force_bytes(line[0])):
                    comm_list.append(force_bytes(line[1]))

            comm_list2=sorted(comm_list)
            for i in range(0,len(comm_list2)):
                comm_list2[i]=ter.cmd_str(comm_list2[i].decode('utf-8'),
                                          amt)
            comm_rows=screenify_py(comm_list2)
            for i in range(0,len(comm_rows)):
                print(comm_rows[i])
                        
        # End of function o2graph_plotter::commands()
        return

    def yt_save_annotate(self,o2scl,amp,link,fname):
        """
        Create a .png image, then add 2D annotations, 
        save to file named 'fname', and then apply any filters
        
        """
        
        import matplotlib.pyplot as plot
        
        if len(self.yt_ann)==0:
            
            # No annotation, so just call scene.save()
            print('o2graph:yt_save_annotate: Calling yt_scene.save()',
                  'with filename',fname,self.yt_sigma_clip)
            self.yt_scene.save(fname,sigma_clip=self.yt_sigma_clip)
            
        else:

            # This segment of code is based off of yt's save_annotate()
            # function.
            self.yt_scene.render()
            fa=self.yt_scene._show_mpl
            axt=fa(self.yt_scene._last_render.swapaxes(0,1),
                   sigma_clip=self.yt_sigma_clip,dpi=100)
            self.yt_trans=self.yt_scene._render_figure.transFigure
            self.axes=axt.axes
            self.fig=self.yt_scene._render_figure
            self.canvas_flag=True
            if self.verbose>1:
                print('Adding annotations:')
            self.parse_string_list(self.yt_ann,o2scl,amp,self.link2)
            if self.verbose>1:
                print('Done adding annotations:')
            #self.text(0.1,0.9,'x',color='w',fontsize=self.font*1.25,
                #transform=tf)
            self.canvas_flag=False
            #axt.axes.text(0.1,0.9,'test',color='w',transform=tf,
            #fontsize=self.font*1.25)
            canvast=get_canvas(self.yt_scene._render_figure,
                               fname)
            self.yt_scene._render_figure.canvas=canvast
            #self.yt_scene._render_figure.tight_layout(pad=0.0)
            plot.subplots_adjust(left=0.0,bottom=0.0,
                                 right=1.0,top=1.0)
            if self.verbose>0:
                print('o2graph:yt-render: Calling',
                      'savefig() with annotations and file',fname,'.')
            self.yt_scene._render_figure.savefig(fname,facecolor='black',
                                                 pad_inches=0)

        # After having saved the image, filter it
        self.filter_image(fname)
            
        return

    def _make_fname(self,prefix,suffix,i_frame,n_frames):
        """
        Construct the animation filename from frame index and frame 
        total, padding with zeros when necessary. 
        """
        if n_frames>=1000:
            if i_frame<10:
                fname2=prefix+'000'+str(i_frame)+suffix
            elif i_frame<100:
                fname2=prefix+'00'+str(i_frame)+suffix
            elif i_frame<1000:
                fname2=prefix+'0'+str(i_frame)+suffix
            else:
                fname2=prefix+str(i_frame)+suffix
        elif n_frames>=100:
            if i_frame<10:
                fname2=prefix+'00'+str(i_frame)+suffix
            elif i_frame<100:
                fname2=prefix+'0'+str(i_frame)+suffix
            else:
                fname2=prefix+str(i_frame)+suffix
        elif n_frames>=10:
            if i_frame<10:
                fname2=prefix+'0'+str(i_frame)+suffix
            else:
                fname2=prefix+str(i_frame)+suffix
        else:
            fname2=prefix+str(i_frame)+suffix
        return fname2

    def restore_position(self,pos):
        """
        Restore the value of self.yt_position from the array 'pos'
        which is ...
        """
        
        if self.yt_position=='default':
            self.yt_position=str([pos[0]*(self.xhi-self.xlo)+
                                  self.xlo,
                                  pos[1]*(self.yhi-self.ylo)+
                                  self.ylo,
                                  pos[2]*(self.zhi-self.zlo)+
                                  self.zlo])
        elif len(self.yt_position.split(' '))==2:
            splittemp=self.yt_position.split(' ')
            if splittemp[1]=='internal':
                self.yt_position=(str([pos[0],pos[1],pos[2]])+
                                  ' internal')
            else:
                self.yt_position=str([pos[0]*(self.xhi-self.xlo)+
                                      self.xlo,
                                      pos[1]*(self.yhi-self.ylo)+
                                      self.ylo,
                                      pos[2]*(self.zhi-self.zlo)+
                                      self.zlo])
        else:
            self.yt_position=str([pos[0]*(self.xhi-self.xlo)+
                                  self.xlo,
                                  pos[1]*(self.yhi-self.ylo)+
                                  self.ylo,
                                  pos[2]*(self.zhi-self.zlo)+
                                  self.zlo])
        print('restored self.yt_position:',
              self.yt_position)
        return

    def restore_focus(self,foc):
        """
        Restore the value of self.yt_focus from the array 'foc'.
        """
        
        if (len(self.yt_focus.split(' '))==2 and
            self.yt_focus.split(' ')[1]=='internal'):
            self.yt_focus=(str([foc[0],foc[1],foc[2]])+
                           ' internal')
        else:
            self.yt_focus=str([foc[0]*(self.xhi-self.xlo)+self.xlo,
                               foc[1]*(self.yhi-self.ylo)+self.ylo,
                               foc[2]*(self.zhi-self.zlo)+self.zlo])
        print('restored self.yt_focus:',
              self.yt_focus)

    def restore_north(self,nor):
        """
        Restore the value of self.yt_north from the array 'nor'.
        """
        self.yt_north=[nor[0],nor[1],nor[2]]
        return
        
    def restore_width(self,wid):
        """
        Restore the value of self.yt_width from the array 'wid'.
        """
        self.yt_width=[wid[0],wid[1],wid[2]]
        return
        
    def create_camera_vecs(self):
        """
        Create vectors (pos,foc,nor,wid) from the user settings in
        yt_position, yt_focus, yt_north and yt_width. This function is
        used in yt_render to keep track of the camera properties.
        The output vectors are always created in the internal 
        coordinate system.
        """
        
        # Create position array
        if self.yt_position=='default':
            pos=[1.5,0.6,0.7]
        elif len(self.yt_position.split(' '))==2:
            splittemp=self.yt_position.split(' ')
            if splittemp[1]=='internal':
                pos=[float(splittemp[0][0]),
                     float(splittemp[0][1]),
                     float(splittemp[0][2])]
            else:
                pos=[(float(splittemp[0][0])-self.xlo)/
                     (self.xhi-self.xlo),
                     (float(splittemp[0][1])-self.ylo)/
                     (self.yhi-self.ylo),
                     (float(splittemp[0][2])-self.zlo)/
                     (self.zhi-self.zlo)]
        else:
            pos=[(eval(self.yt_position)[0]-self.xlo)/
                 (self.xhi-self.xlo),
                 (eval(self.yt_position)[1]-self.ylo)/
                 (self.yhi-self.ylo),
                 (eval(self.yt_position)[2]-self.zlo)/
                 (self.zhi-self.zlo)]

        # Create focus array
        if self.yt_focus=='default':
            foc=[0.5,0.5,0.5]
        elif len(self.yt_focus.split(' '))==2:
            splittemp=self.yt_focus.split(' ')
            if splittemp[1]=='internal':
                foc=[float(splittemp[0][0]),
                     float(splittemp[0][1]),
                     float(splittemp[0][2])]
            else:
                foc=[(float(splittemp[0][0])-self.xlo)/
                     (self.xhi-self.xlo),
                     (float(splittemp[0][1])-self.ylo)/
                     (self.yhi-self.ylo),
                     (float(splittemp[0][2])-self.zlo)/
                     (self.zhi-self.zlo)]
        else:
            foc=[(eval(self.yt_focus)[0]-self.xlo)/
                 (self.xhi-self.xlo),
                 (eval(self.yt_focus)[1]-self.ylo)/
                 (self.yhi-self.ylo),
                 (eval(self.yt_focus)[2]-self.zlo)/
                 (self.zhi-self.zlo)]

        if self.yt_north=='default':
            nor=[0.0,0.0,1.0]
        else:
            nor=[float(eval(self.yt_north))[0],
                 float(eval(self.yt_north))[1],
                 float(eval(self.yt_north))[2]]
            
        if self.yt_width=='default':
            wid=[1.5,1.5,1.5]
        else:
            wid=[self.yt_width[0],
                 self.yt_width[1],
                 self.yt_width[2]]
            
        return (pos,foc,nor,wid)

    def filter_image(self,fname):
        """
        If a filter has been defined, apply that filter to the image
        stored in file ``fname``. This function is used in
        yt_save_annotate() to filter the images after saving them to a
        file.
        """
        if self.yt_filter!='':
            print('Found filter')
            cmd=self.yt_filter
            cmd=cmd.replace('%i',fname)
            cmd=cmd.replace('%o','/tmp/yt_filtered.png')
            print('Running filter command:\n  ',cmd)
            os.system(cmd)
            print('Moving file back:',
                  'mv /tmp/yt_filtered.png '+fname)
            os.system('mv /tmp/yt_filtered.png '+fname)
        return
    
    def yt_render(self,o2scl,amp,link,fname,mov_fname='',loop=False):
        """
        Documentation for o2graph command ``yt-render``:

        Render the yt volume visualization.

        Command-line arguments: ``<filename or pattern> [kwargs]``

        Perform the volume rendering. If yt_path is empty, then the
        first argument is the filename. If yt_path is not empty then
        the first argument is a filename pattern containing * where
        each frame will be stored. If yt_path is not empty and a movie
        filename is given, then ffmpeg will be used to combine the
        frames into an mp4 file.

        The keyword argument ``mov_fname`` specifies the output
        movie file (if an animation is specified with ``yt-path``).
        If empty, the filename ``o2graph.mp4`` is used. 
        """

        if self.yt_scene==0:
            print('Cannot perform a yt render without a scene.')
            return
        
        # AWS 10/14/19 the call to save() below does
        # the render() so I don't think I need this
        #self.yt_scene.render()

        if len(self.yt_path)==0:

            # No path, so just call save and finish
            self.yt_save_annotate(o2scl,amp,self.link2,fname);

        else:

            # Setup destination filename
            if mov_fname=='':
                print('No movie filename specified so using',
                      'o2graph.mp4')
                mov_fname='o2graph.mp4'

            # Parse image file pattern
            asterisk=fname.find('*')
            prefix=fname[0:asterisk]
            suffix=fname[asterisk+1:len(fname)]
            print('o2graph:yt-render:',
                  'fname,prefix,suffix,mov_fname:\n  ',
                  fname,prefix,suffix,mov_fname)
                            
            # Count total frames
            n_frames=0
            for ip in range(0,len(self.yt_path)):
                n_frames=n_frames+int(self.yt_path[ip][1])
            print(n_frames,'total frames')

            # Render initial frame
            i_frame=0
            fname2=self._make_fname(prefix,suffix,i_frame,n_frames)
            self.yt_save_annotate(o2scl,amp,self.link2,fname2);

            # Loop over all movements
            for ip in range(0,len(self.yt_path)):

                # Number of frames for this movement
                n_frames_move=int(self.yt_path[ip][1])
            
                if self.yt_path[ip][0]=='yaw':

                    angle=(float(self.yt_path[ip][2])*numpy.pi*2.0/
                           n_frames_move)

                    # Create arrays
                    (pos,foc,nor,wid)=self.create_camera_vecs()
                    print('yaw: camera pos, foc:',pos,foc)
                    print('yaw: camera nor, wid:',nor,wid)
                    
                    for ifr in range(0,n_frames_move):
                        
                        i_frame=i_frame+1
                        
                        if self.verbose>=2:
                            print(self.yt_camera)
                            print('normal_vector:',
                                  self.yt_camera.normal_vector)
                            print('north_vector:',
                                  self.yt_camera.north_vector)
                            print('origin:',
                                  self.yt_camera.lens.origin)

                        # We can't use the yt yaw() function because
                        # it modifies the camera properties in an
                        # undocumented way. 
                        
                        from yt.units.yt_array import YTArray
                        rv=YTArray([0,0,1])
                        #rc=YTArray([0.5,0.5,0.5])
                        self.yt_camera.rotate(angle,rot_vector=rv)
                        
                        xt=pos[0]-foc[0]
                        yt=pos[1]-foc[1]
                        zt=pos[2]-foc[2]
                        r=math.sqrt(xt**2+yt**2+zt**2)
                        theta=math.acos(zt/r)
                        phi=math.atan2(yt,xt)
                        phi+=angle
                        xt=r*math.sin(theta)*math.cos(phi)
                        yt=r*math.sin(theta)*math.sin(phi)
                        zt=r*math.cos(theta)
                        
                        pos[0]=foc[0]+xt
                        pos[1]=foc[1]+yt
                        pos[2]=foc[2]+zt
                        #print('yaw: new position:',pos)

                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.switch_orientation()
                            
                        if self.verbose>=2:
                            print('Camera width [%0.6e,%0.6e,%0.6e]' %
                                  (self.yt_camera.width[0],
                                   self.yt_camera.width[1],
                                   self.yt_camera.width[2]))
                            
                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl,amp,self.link2,fname2);
                    
                        # End of 'for ifr in range(0,n_frames_move)'
                    
                    # Restore position array
                    self.restore_position(pos)
                    
                    # End of loop 'if self.yt_path[ip][0]=='yaw''
                    
                elif self.yt_path[ip][0]=='zoom':
                    
                    factor=float(self.yt_path[ip][2])

                    for ifr in range(0,n_frames_move):
                        
                        i_frame=i_frame+1
                        
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)
                        
                        # Move camera
                        ifactor=factor**(1.0/float(n_frames_move-1))
                        print('ifactor',ifactor)
                        self.yt_camera.zoom(ifactor)

                        print('Camera width [%0.6e,%0.6e,%0.6e]' %
                              (self.yt_camera.width[0],
                               self.yt_camera.width[1],
                               self.yt_camera.width[2]))
                        
                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl,amp,self.link2,fname2);
                        
                        # End of 'for ifr in range(0,n_frames_move)'

                    # Width
                    self.restore_width(self.yt_camera.width)
                        
                    # End of loop 'if self.yt_path[ip][0]=='zoom''
                    
                elif self.yt_path[ip][0]=='move':

                    # Move the camera without changing the focus

                    dest=eval(self.yt_path[ip][2])
                    unit_system=self.yt_path[ip][3]
                    if unit_system=='user':
                        dest=[(float(dest[0])-self.xlo)/
                              (self.xhi-self.xlo),
                              (float(dest[1])-self.ylo)/
                              (self.yhi-self.ylo),
                              (float(dest[2])-self.zlo)/
                        (self.zhi-self.zlo)]
                    
                    # Create arrays
                    (source,foc,nor,wid)=self.create_camera_vecs()
                    print('move: camera pos, foc:',source,foc)
                    print('move: camera nor, wid:',nor,wid)
                    print('move: camera dest:',dest)

                    for ifr in range(0,n_frames_move):
                        
                        i_frame=i_frame+1
                    
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)

                        # Create the new position array
                        pos[0]=(source[0]+(dest[0]-source[0])*ifr/
                                (float(n_frames_move-1)))
                        pos[1]=(source[1]+(dest[1]-source[1])*ifr/
                                (float(n_frames_move-1)))
                        pos[2]=(source[2]+(dest[2]-source[2])*ifr/
                                (float(n_frames_move-1)))
                        
                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.switch_orientation()

                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl,amp,self.link2,fname2);

                        # End of 'for ifr in range(0,n_frames_move)'
                        
                    # Restore position array
                    self.restore_position(pos)

                    # End of loop 'if self.yt_path[ip][0]=='move''
                    
                elif self.yt_path[ip][0]=='turn':

                    # Modify the focus without moving
                    
                    new_focus=eval(self.yt_path[ip][2])
                    unit_system=self.yt_path[ip][3]
                    if unit_system=='user':
                        new_focus=[(float(dest[0])-self.xlo)/
                                   (self.xhi-self.xlo),
                                   (float(dest[1])-self.ylo)/
                                   (self.yhi-self.ylo),
                                   (float(dest[2])-self.zlo)/
                                   (self.zhi-self.zlo)]
                    
                    # Create arrays
                    (pos,old_focus,nor,wid)=self.create_camera_vecs()
                    print('move: camera pos, foc:',pos,old_focus)
                    print('move: camera nor, wid:',nor,wid)
                    print('move: camera new focus:',new_focus)

                    for ifr in range(0,int(self.yt_path[ip][1])):
                        
                        i_frame=i_frame+1
                    
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)

                        # Create the new focus array
                        foc[0]=(old_focus[0]+(new_focus[0]-old_focus[0])*ifr/
                                (float(n_frames_move-1)))
                        foc[1]=(old_focus[1]+(new_focus[1]-old_focus[1])*ifr/
                                (float(n_frames_move-1)))
                        foc[2]=(old_focus[2]+(new_focus[2]-old_focus[2])*ifr/
                                (float(n_frames_move-1)))
                        
                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.switch_orientation()

                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl,amp,self.link2,fname2);

                        # End of 'for ifr in range(0,n_frames_move)'
                        
                elif self.yt_path[ip][0]=='moveauto':

                    # Move the camera, automatically changing the
                    # focus to lie along the direction of motion
                    #
                    # The idea here is to do the turn at the beginning
                    # of the movement so that the initial frames turn
                    # toward the new focus while moving and the final
                    # frames just move to the final camera position.

                    print('unfinished')
                    quit()

                    # This is just a copy of the 'move' code from
                    # above
                    dest=eval(self.yt_path[ip][2])
                    unit_system=self.yt_path[ip][3]
                    if unit_system=='user':
                        dest=[(float(dest[0])-self.xlo)/
                              (self.xhi-self.xlo),
                              (float(dest[1])-self.ylo)/
                              (self.yhi-self.ylo),
                              (float(dest[2])-self.zlo)/
                        (self.zhi-self.zlo)]
                        
                    # Create arrays
                    (source,old_focus,nor,wid)=self.create_camera_vecs()

                    # The new focus is just beyond the destination,
                    # we arbitrarily choose 0.1
                    new_focus=[dest[0]-source[0]*0.1+dest[0],
                               dest[1]-source[1]*0.1+dest[1],
                               dest[2]-source[2]*0.1+dest[2]]
                    
                    print('move: camera old position, old focus:',source,
                          old_focus)
                    print('move: camera nor, wid:',nor,wid)
                    print('move: camera dest:',dest)
                    print('move: camera new focus:',new_focus)

                    for ifr in range(0,self.yt_path[ip][1]):
                        
                        i_frame=i_frame+1
                    
                        print(self.yt_camera)
                        print('unit_vectors:',self.yt_camera.unit_vectors)
                        print('normal_vector:',self.yt_camera.normal_vector)
                        print('north_vector:',self.yt_camera.north_vector)
                        print('origin:',self.yt_camera.lens.origin)
                        print('num_threads:',self.yt_camera.lens.num_threads)

                        frame_ratio=(float(ifr)/
                                     (float(self.yt_path[ip][1])-1))
                        
                        # Create the new position array
                        pos[0]=source[0]+(dest[0]-source[0])*frame_ratio
                        pos[1]=source[1]+(dest[1]-source[1])*frame_ratio
                        pos[2]=source[2]+(dest[2]-source[2])*frame_ratio

                        # This function makes the focus change quickly
                        # at first and then slowly at the end
                        foc_factor=0.11/(frame_ratio+0.1)-0.1

                        # Create the new focus array
                        foc[0]=(old_focus[0]+
                                (new_focus[0]-old_focus[0])*foc_factor)
                        foc[1]=(old_focus[1]+
                                (new_focus[1]-old_focus[1])*foc_factor)
                        foc[2]=(old_focus[2]+
                                (new_focus[2]-old_focus[2])*foc_factor)
                                
                        # Move camera
                        self.yt_camera.position=[pos[0],pos[1],pos[2]]
                        self.yt_camera.focus=[foc[0],foc[1],foc[2]]
                        self.yt_camera.width=[wid[0],wid[1],wid[2]]
                        self.yt_camera.north_vector=[nor[0],nor[1],nor[2]]
                        self.yt_camera.switch_orientation()

                        # Update text objects
                        self.yt_update_text()

                        # Save new frame
                        fname2=self._make_fname(prefix,suffix,
                                                i_frame,n_frames)
                        self.yt_save_annotate(o2scl,amp,self.link2,fname2);

                        # End of 'for ifr in range(0,n_frames_move)'
                        
                # End of 'for ip in range(0,len(self.yt_path)):'

            # -r is rate (in frames/sec), -f is format, -vcodec is
            # video codec (apparently 420p works well with quicktime),
            # -pix_fmt sepcifies the pixel format, -crf is the quality
            # (15-25 recommended) -y forces overwrite of the movie
            # file if it already exists
            
            if n_frames>=1000:
                self.mp4([prefix+'%04d'+suffix,mov_fname],loop=loop)
            elif n_frames>=100:
                self.mp4([prefix+'%03d'+suffix,mov_fname],loop=loop)
            elif n_frames>=10:
                self.mp4([prefix+'%02d'+suffix,mov_fname],loop=loop)
            else:
                self.mp4([prefix+'%01d'+suffix,mov_fname],loop=loop)

            # End of else for 'if len(self.yt_path)==0:'
            
        # End of function o2graph_plotter::yt_render()
        return

    def parse_string_list(self,strlist,o2scl,amp,link):
        """
        Parse a list of strings.

        This function is called by parse_argv().
        """

        if self.verbose>2:
            print('In parse_string_list()',strlist)
        
        ix=0
        while ix<len(strlist):
            
            if self.verbose>2:
                print('Processing index',ix,'with value',strlist[ix],'.')
                
            # Find first option, at index ix
            initial_ix_done=False
            while initial_ix_done==False:
                if ix==len(strlist):
                    initial_ix_done=True
                elif strlist[ix][0]=='-':
                    initial_ix_done=True
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
                ix_next_done=False
                while ix_next_done==False:

                    # Normally, o2graph and acol commands are ended by
                    # the next command-line argument which begins with
                    # a dash. We make an exception for yt-ann, which
                    # annotates a yt plot. yt-ann commands require
                    # the keyword "end" and the end to indicate that
                    # they are complete.
                    
                    if ix_next==len(strlist):
                        ix_next_done=True
                    elif (cmd_name!='yt-ann' and
                    len(strlist[ix_next])>0 and strlist[ix_next][0]=='-'):
                        ix_next_done=True
                    elif (cmd_name=='yt-ann' and ix_next>0 and
                    strlist[ix_next-1]=='end'):
                        ix_next_done=True
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
                           'set-data','set_data','set-unit','set',
                           'set_unit','show-units','show_units','slice',
                           'sort','stats','sum','to-hist','to_hist',
                           'to-hist-2d' 'to_hist_2d',
                           'to_table3d','to-table','to_table','to-table3d',
                           'type','v','warranty']
                
                # Now process the option
                if cmd_name=='set':

                    if self.verbose>2:
                        print('Process set.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for set option.')
                    else:
                        self.set_wrapper(o2scl,amp,self.link2,strlist[ix+1:ix_next])
                        
                elif cmd_name=='ell-max':

                    if self.verbose>2:
                        print('Process ell-max.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<1:
                        print('Not enough parameters for ell-max option.')
                    else:
                        self.ell_max(strlist[ix+1],strlist[ix+2:ix_next])
                        
                elif cmd_name=='colors':

                    if self.verbose>2:
                        print('Process colors.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<1:
                        print('Not enough parameters for ell-max option.')
                    else:
                        self.colors(strlist[ix+1:ix_next])
                        
                elif cmd_name=='cmap':

                    if self.verbose>2:
                        print('Process cmap.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for cmap option.')
                    elif ix_next-ix<3:
                        self.cmap(strlist[ix+1])
                    else:
                        self.cmap(strlist[ix+1],strlist[ix+2:ix_next])
                        
                elif cmd_name=='make-png':

                    if self.verbose>2:
                        print('Process make-png.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for make-png option.')
                    else:
                        self.make_png_o2graph(o2scl,amp,self.link2,
                                              strlist[ix+1:ix_next])
                        
                elif cmd_name=='get':
                    
                    if self.verbose>2:
                        print('Process get.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        self.get('No parameter specified to get.')
                    else:
                        self.get_wrapper(o2scl,amp,strlist[ix+1:ix_next])

                elif cmd_name=='commands':
                    
                    if self.verbose>2:
                        print('Process commands.')
                        print('args:',strlist[ix:ix_next])

                    self.commands(o2scl,amp,self.link2,
                                  strlist[ix+1:ix_next])
                    
                elif cmd_name=='yt-add-vol':

                    if self.verbose>2:
                        print('Process yt-add-vol.')
                        print('args:',strlist[ix:ix_next])
                        
                    self.yt_add_vol(o2scl,amp,self.link2,
                                    strlist[ix+1:ix_next])
                    
                elif cmd_name=='yt-scatter':

                    if self.verbose>2:
                        print('Process yt-scatter.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<4:
                        print('Not enough parameters for yt-scatter.')
                    else:
                        self.yt_scatter(o2scl,amp,
                                        self.link2,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-path':

                    if self.verbose>2:
                        print('Process yt-path.')
                        print('args:',strlist[ix:ix_next])

                    if strlist[ix+1]=='reset':
                        print('Resetting yt-path.')
                        self.yt_path=[]
                    elif ix_next-ix<4:
                        print('Not enough parameters for yt-path.')
                    else:
                        self.yt_path_func(o2scl,amp,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-ann':

                    if self.verbose>2:
                        print('Process yt-ann.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<4:
                        print('Not enough parameters for yt-ann.')
                    else:
                        self.yt_ann_func(o2scl,amp,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-text':

                    if self.verbose>2:
                        print('Process yt-text.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<5:
                        print('Not enough parameters for yt-text.')
                    elif ix_next-ix>5:
                        self.yt_text(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     strlist[ix+4],
                                     **string_to_dict(strlist[ix+5]))
                    else:
                        self.yt_text(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     strlist[ix+4])
                                                    
                elif cmd_name=='yt-xtitle':

                    if self.verbose>2:
                        print('Process yt-text.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for yt-text.')
                    elif ix_next-ix==3:
                        self.yt_xtitle(strlist[ix+1],
                                       **string_to_dict(strlist[ix+2]))
                    else:
                        self.yt_xtitle(strlist[ix+1])
                                                    
                elif cmd_name=='yt-ytitle':

                    if self.verbose>2:
                        print('Process yt-text.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for yt-text.')
                    elif ix_next-ix==3:
                        self.yt_ytitle(strlist[ix+1],
                                       **string_to_dict(strlist[ix+2]))
                    else:
                        self.yt_ytitle(strlist[ix+1])
                                                    
                elif cmd_name=='yt-ztitle':

                    if self.verbose>2:
                        print('Process yt-text.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for yt-text.')
                    elif ix_next-ix==3:
                        self.yt_ztitle(strlist[ix+1],
                                       **string_to_dict(strlist[ix+2]))
                    else:
                        self.yt_ztitle(strlist[ix+1])
                                                    
                elif cmd_name=='yt-line':

                    if self.verbose>2:
                        print('Process yt-line.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<7:
                        print('Not enough parameters for yt-line.')
                    elif ix_next-ix>7:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_line([x1,y1,z1],[x2,y2,z2],
                                      **string_to_dict(strlist[ix+7]))
                    else:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_line([x1,y1,z1],[x2,y2,z2])
                                                    
                elif cmd_name=='yt-point':

                    if self.verbose>2:
                        print('Process yt-point.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<5:
                        print('Not enough parameters for yt-point.')
                    elif ix_next-ix>5:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        rad=float(eval(strlist[ix+4]))
                        self.yt_point([x1,y1,z1],rad,
                                      **string_to_dict(strlist[ix+5]))
                    else:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        rad=float(eval(strlist[ix+4]))
                        self.yt_point([x1,y1,z1],rad)
                                                    
                elif cmd_name=='yt-box':

                    if self.verbose>2:
                        print('Process yt-box.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<7:
                        print('Not enough parameters for yt-box.')
                    elif ix_next-ix>=8:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_box([x1,y1,z1],[x2,y2,z2],
                                      **string_to_dict(strlist[ix+7]))
                    else:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_box([x1,y1,z1],[x2,y2,z2])
                                                    
                elif cmd_name=='yt-arrow':

                    if self.verbose>2:
                        print('Process yt-arrow.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<6:
                        print('Not enough parameters for yt-arrow.')
                    elif ix_next-ix>=7:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_arrow([x1,y1,z1],[x2,y2,z2],
                                      **string_to_dict(strlist[ix+7]))
                    else:
                        x1=float(eval(strlist[ix+1]))
                        y1=float(eval(strlist[ix+2]))
                        z1=float(eval(strlist[ix+3]))
                        x2=float(eval(strlist[ix+4]))
                        y2=float(eval(strlist[ix+5]))
                        z2=float(eval(strlist[ix+6]))
                        self.yt_arrow([x1,y1,z1],[x2,y2,z2])
                                                    
                elif cmd_name=='yt-vertex-list':

                    if self.verbose>2:
                        print('Process yt-vertex-list.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<4:
                        print('Not enough parameters for yt-vertex-list.')
                    else:
                        self.yt_vertex_list(o2scl,amp,self.link2,
                                            strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-mesh':

                    if self.verbose>2:
                        print('Process yt-mesh.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for yt-mesh.')
                    else:
                        self.yt_mesh(o2scl,amp,self.link2,
                                     strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='yt-source-list':

                    if self.verbose>2:
                        print('Process yt-source-list.')
                        print('args:',strlist[ix:ix_next])
                        
                    icnt=0
                    if self.yt_scene==0:
                        print('No yt sources.')
                    else:
                        for key, value in self.yt_scene.sources.items():
                            tstr=("<class 'yt.visualization.volume_"+
                                  "rendering.render_source.")
                            print('yt-source-list',icnt,key,
                                  str(type(value)).replace(tstr,"<class '..."))
                            icnt=icnt+1
                        if icnt==0:
                            print('No yt sources.')

                elif cmd_name=='td-arrow':

                    if self.verbose>2:
                        print('Process td-arrow.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix>=8:
                        self.td_arrow(float(strlist[ix+1]),
                                      float(strlist[ix+2]),
                                      float(strlist[ix+3]),
                                      float(strlist[ix+4]),
                                      float(strlist[ix+5]),
                                      float(strlist[ix+6]),
                                      strlist[ix+7])
                    else:
                        print('Not enough arguments for td-arrow.')

                elif cmd_name=='td-axis':

                    if self.verbose>2:
                        print('Process td-axis.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix>=4:
                        self.td_arrow(0,0,0,1,0,0,'x_axis')
                        self.td_arrow(0,0,0,0,1,0,'y_axis')
                        self.td_arrow(0,0,0,0,0,1,'z_axis')
                        self.td_axis_label('x',strlist[ix+1])
                        self.td_axis_label('y',strlist[ix+2])
                        self.td_axis_label('z',strlist[ix+3])
                    else:
                        print('Not enough arguments for td-axis.')
                        
                elif cmd_name=='td-den-plot':

                    if self.verbose>2:
                        print('Process td-den-plot.')
                        print('args:',strlist[ix:ix_next])

                    print('here0',ix_next-ix,strlist[ix+2])
                    if ix_next-ix==2:
                        self.td_den_plot(o2scl,amp,[strlist[ix+1]])
                    elif ix_next-ix>=3:
                        self.td_den_plot(o2scl,amp,[strlist[ix+1]],
                                         **string_to_dict(strlist[ix+2]))
                    else:
                        print('Not enough arguments for td-den-plot.')

                elif cmd_name=='yt-axis':

                    if self.verbose>2:
                        print('Process yt-axis.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        self.yt_plot_axis()
                    else:
                        self.yt_plot_axis(**string_to_dict(strlist[ix+1]))

                elif cmd_name=='yt-render':

                    if self.verbose>2:
                        print('Process render.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for yt-render.')
                    elif ix_next-ix<3:
                        self.yt_render(o2scl,amp,self.link2,strlist[ix+1])
                    else:
                        self.yt_render(o2scl,amp,self.link2,strlist[ix+1],
                                       **string_to_dict(strlist[ix+2]))

                elif cmd_name=='yt-tf':

                    if self.verbose>2:
                        print('Process yt-tf.')
                        print('args:',strlist[ix:ix_next])

                    self.yt_tf_func(strlist[ix+1:ix_next])
                    
                elif cmd_name=='help' or cmd_name=='h':
                    
                    if self.verbose>2:
                        print('Process help.')
                        print('args:',strlist[ix:ix_next])

                    self.help_func(o2scl,amp,self.link2,strlist[ix+1:ix_next])

                elif cmd_name=='plot':
                    
                    if self.verbose>2:
                        print('Process plot.')
                        print('args:',strlist[ix:ix_next])

                    self.plot_o2graph(o2scl,amp,strlist[ix+1:ix_next],
                                      self.link2)

                elif cmd_name=='plot-color':
                    
                    if self.verbose>2:
                        print('Process plot-color.')
                        print('args:',strlist[ix:ix_next])

                    self.plot_color(o2scl,amp,self.link2,strlist[ix+1:ix_next])

                elif cmd_name=='rplot':
                    
                    if self.verbose>2:
                        print('Process rplot.')
                        print('args:',strlist[ix:ix_next])

                    self.rplot(o2scl,amp,self.link2,strlist[ix+1:ix_next])

                elif cmd_name=='scatter':
                    
                    if self.verbose>2:
                        print('Process scatter.')
                        print('args:',strlist[ix:ix_next])

                    self.scatter(o2scl,amp,self.link2,strlist[ix+1:ix_next])

                elif cmd_name=='hist-plot':
                    
                    if self.verbose>2:
                        print('Process hist-plot.')
                        print('args:',strlist[ix:ix_next])

                    self.hist_plot(o2scl,amp,self.link2,strlist[ix+1:ix_next])

                elif cmd_name=='errorbar':
                    
                    if self.verbose>2:
                        print('Process errorbar.')
                        print('args:',strlist[ix:ix_next])

                    self.errorbar(o2scl,amp,self.link2,strlist[ix+1:ix_next])

                elif cmd_name=='hist2d-plot':
                    
                    if self.verbose>2:
                        print('Process hist2d-plot.')
                        print('args:',strlist[ix:ix_next])
                        
                    self.hist2d_plot(o2scl,amp,self.link2,
                                     strlist[ix+1:ix_next])
                            
                elif cmd_name=='den-plot':
                    
                    if self.verbose>2:
                        print('Process den-plot.')
                        print('args:',strlist[ix:ix_next])

                    self.den_plot_o2graph(o2scl,amp,self.link2,
                                          strlist[ix+1:ix_next])
                
                elif cmd_name=='mp4':
                    
                    if self.verbose>2:
                        print('Process mp4.')
                        print('args:',strlist[ix:ix_next])

                    self.mp4(strlist[ix+1:ix_next])
                
                elif cmd_name=='kde-plot':
                    
                    if self.verbose>2:
                        print('Process kde-plot.')
                        print('args:',strlist[ix:ix_next])

                    self.kde_plot(o2scl,amp,strlist[ix+1:ix_next],
                                  self.link2)
                
                elif cmd_name=='kde-2d-plot':
                    
                    if self.verbose>2:
                        print('Process kde-2d-plot.')
                        print('args:',strlist[ix:ix_next])

                    self.kde_2d_plot(o2scl,amp,strlist[ix+1:ix_next],
                                  self.link2)
                
                elif cmd_name=='to-kde':
                    
                    if self.verbose>2:
                        print('Process to-kde.')
                        print('args:',strlist[ix:ix_next])

                    self.to_kde(o2scl,amp,self.link2,
                                strlist[ix+1:ix_next])
                
                elif cmd_name=='den-plot-rgb':
                    
                    if self.verbose>2:
                        print('Process den-plot-rgb.')
                        print('args:',strlist[ix:ix_next])

                    self.den_plot_rgb_o2graph(o2scl,amp,self.link2,
                                              strlist[ix+1:ix_next])
                
                elif cmd_name=='obj':

                    if self.verbose>2:
                        print('Process obj.')
                        print('args:',strlist[ix:ix_next])

                    print('going to obj_o2graph.')
                    self.obj_o2graph(o2scl,amp,self.link2,
                                              strlist[ix+1:ix_next])
                
                elif cmd_name=='gltf':

                    if self.verbose>2:
                        print('Process gltf.')
                        print('args:',strlist[ix:ix_next])

                    print('going to gltf_o2graph.')
                    self.gltf_o2graph(o2scl,amp,self.link2,
                                              strlist[ix+1:ix_next])
                
                elif cmd_name=='den-plot-anim':
                    
                    if self.verbose>2:
                        print('Process den-plot-anim.')
                        print('args:',strlist[ix:ix_next])

                    self.den_plot_anim(o2scl,amp,self.link2,
                                       strlist[ix+1:ix_next])
                
                elif cmd_name=='plot1':
                    
                    if self.verbose>2:
                        print('Process plot1.')
                        print('args:',strlist[ix:ix_next])
                        
                    self.plot1(o2scl,amp,self.link2,strlist[ix+1:ix_next])
                            
                elif cmd_name=='plotv':
                    
                    if self.verbose>2:
                        print('Process plotv.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for plotv option.')
                    else:
                        self.plotv(o2scl,amp,self.link2,strlist[ix+1:ix_next])
                                                    
                elif cmd_name=='text':
                    
                    if self.verbose>2:
                        print('Process text.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for text option.')
                    elif ix_next-ix<5:
                        self.text2(strlist[ix+1],strlist[ix+2],strlist[ix+3])
                    else:
                        self.text2(strlist[ix+1],strlist[ix+2],strlist[ix+3],
                                  **string_to_dict(strlist[ix+4]))
                        
                elif cmd_name=='ttext':
                    
                    if self.verbose>2:
                        print('Process ttext.')
                        print('args:',strlist[ix:ix_next])
                        
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
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for xlimits option.')
                    else:
                        self.xlimits(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])))
                        
                elif cmd_name=='ylimits':
                    
                    if self.verbose>2:
                        print('Process ylimits.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for ylimits option.')
                    else:
                        self.ylimits(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])))
                        
                elif cmd_name=='save':
                    
                    if self.verbose>2:
                        print('Process save.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for save option.')
                    else:
                        import matplotlib.pyplot as plot
                        plot.savefig(strlist[ix+1])
                        
                elif cmd_name=='subplots':
                    
                    if self.verbose>2:
                        print('Process subplots.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for subplots option.')
                    elif ix_next-ix<3:
                        self.subplots(int(strlist[ix+1]))
                    elif ix_next-ix<4:
                        self.subplots(int(strlist[ix+1]),int(strlist[ix+2]))
                    else:
                        self.subplots(int(strlist[ix+1]),int(strlist[ix+2]),
                                      **string_to_dict(strlist[ix+3]))
                        
                elif cmd_name=='selax':
                    
                    if self.verbose>2:
                        print('Process selax.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        self.selax()
                    else:
                        self.selax(strlist[ix+1])
                        
                elif cmd_name=='addcbar':
                    
                    if self.verbose>5:
                        print('Process addcbar.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for addcbar option.')
                    elif ix_next-ix<6:
                        self.addcbar(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     float(eval(strlist[ix+4])))
                    else:
                        self.addcbar(float(eval(strlist[ix+1])),
                                     float(eval(strlist[ix+2])),
                                     float(eval(strlist[ix+3])),
                                     float(eval(strlist[ix+4])),
                                     **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='inset':
                    
                    if self.verbose>5:
                        print('Process inset.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for inset option.')
                    elif ix_next-ix<6:
                        self.inset(float(eval(strlist[ix+1])),
                                   float(eval(strlist[ix+2])),
                                   float(eval(strlist[ix+3])),
                                   float(eval(strlist[ix+4])))
                    else:
                        self.inset(float(eval(strlist[ix+1])),
                                   float(eval(strlist[ix+2])),
                                   float(eval(strlist[ix+3])),
                                   float(eval(strlist[ix+4])),
                                   **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='modax':
                    
                    if self.verbose>1:
                        print('Process modax.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<2:
                        print('Not enough parameters for inset option.')
                    else:
                        self.modax(**string_to_dict(strlist[ix+1]))
                        
                elif cmd_name=='subadj':
                    
                    if self.verbose>2:
                        print('Process subadj.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for subadj option.')
                    else:
                        import matplotlib.pyplot as plot
                        plot.subplots_adjust(**string_to_dict(strlist[ix+1]))
                        
                elif cmd_name=='xtitle':

                    if self.verbose>2:
                        print('Process xtitle.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for xtitle option.')
                    elif ix_next-ix==2:
                        self.xtitle(strlist[ix+1])
                    elif ix_next-ix>2 and ix_next-ix<5:
                        print('All three location parameters (xtitle).')
                    elif ix_next-ix==5:
                        self.xtitle(strlist[ix+1],
                                    loc=[float(eval(strlist[ix+2])),
                                         float(eval(strlist[ix+3])),
                                         float(eval(strlist[ix+4]))])
                        
                elif cmd_name=='ytitle':
                    
                    if self.verbose>2:
                        print('Process ytitle.')
                        print('args:',strlist[ix:ix_next])

                    if ix_next-ix<2:
                        print('Not enough parameters for ytitle option.')
                    elif ix_next-ix==2:
                        self.ytitle(strlist[ix+1])
                    elif ix_next-ix>2 and ix_next-ix<5:
                        print('All three location parameters needed (ytitle).')
                    elif ix_next-ix==5:
                        self.ytitle(strlist[ix+1],
                                    loc=[float(eval(strlist[ix+2])),
                                         float(eval(strlist[ix+3])),
                                         float(eval(strlist[ix+4]))])
                        
                # elif cmd_name=='ztitle':
                    
                #     if self.verbose>2:
                #         print('Process ztitle.')

                #     if ix_next-ix<2:
                #         print('Not enough parameters for ztitle option.')
                #     elif ix_next-ix==2:
                #         self.ztitle(strlist[ix+1])
                #     elif ix_next-ix>2 and ix_next-ix<5:
                #         print('All three location parameters needed.')
                #     elif ix_next-ix==5:
                #         self.ztitle(strlist[ix+1],
                #                     loc=[float(eval(strlist[ix+2])),
                #                          float(eval(strlist[ix+3])),
                #                          float(eval(strlist[ix+4]))])
                        
                elif cmd_name=='line':
                    
                    if self.verbose>2:
                        print('Process line.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for line option.')
                    elif ix_next-ix<6:
                        self.line(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4])
                    else:
                        self.line(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='o2scl-cpp-lib':
                    
                    if self.verbose>2:
                        print('Process o2scl-cpp-lib.')
                        print('args:',strlist[ix:ix_next])
                        
                elif cmd_name=='o2scl-lib-dir':
                    
                    if self.verbose>2:
                        print('Process o2scl-lib-dir.')
                        print('args:',strlist[ix:ix_next])
                    
                elif cmd_name=='o2scl-addl-libs':
                    
                    if self.verbose>2:
                        print('Process o2scl-addl-libs.')
                        print('args:',strlist[ix:ix_next])
                    
                elif cmd_name=='debug-first-pass':
                    
                    if self.verbose>2:
                        print('Process debug-first-pass.')
                        print('args:',strlist[ix:ix_next])
                    
                elif cmd_name=='textbox':
                    
                    if self.verbose>2:
                        print('Process textbox.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<4:
                        print('Not enough parameters for textbox option.')
                    elif ix_next-ix<5:
                        self.textbox(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3])
                    elif ix_next-ix<6:
                        self.textbox(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4])
                    else:
                        self.textbox(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4],
                                     **string_to_dict(strlist[ix+5]))
                        
                elif cmd_name=='arrow':
                    
                    if self.verbose>2:
                        print('Process arrow.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<6:
                        print('Not enough parameters for arrow option.')
                    elif ix_next-ix<7:
                        self.arrow(strlist[ix+1],strlist[ix+2],
                                   strlist[ix+3],strlist[ix+4],
                                   strlist[ix+5])
                    else:
                        self.arrow(strlist[ix+1],strlist[ix+2],
                                   strlist[ix+3],strlist[ix+4],
                                   strlist[ix+5],
                                   **string_to_dict(strlist[ix+6]))
                        
                elif cmd_name=='point':
                    
                    if self.verbose>2:
                        print('Process point.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<3:
                        print('Not enough parameters for point option.')
                    elif ix_next-ix<4:
                        self.point(strlist[ix+1],strlist[ix+2])
                    else:
                        self.point(strlist[ix+1],strlist[ix+2],
                                   **string_to_dict(strlist[ix+3]))
                        
                elif cmd_name=='error-point':
                    
                    if self.verbose>2:
                        print('Process point.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for point option.')
                    elif ix_next-ix>=8:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4],
                                         strlist[ix+5],strlist[ix+6],
                                         **string_to_dict(strlist[ix+7]))
                    elif ix_next-ix>=7:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4],
                                         strlist[ix+5],strlist[ix+6])
                    elif ix_next-ix>=6:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4],
                                         **string_to_dict(strlist[ix+5]))
                    else:
                        self.error_point(strlist[ix+1],strlist[ix+2],
                                         strlist[ix+3],strlist[ix+4])
                        
                elif cmd_name=='python':
                    
                    if self.verbose>2:
                        print('Process python.')
                        print('args:',strlist[ix:ix_next])

                    print("The o2graph_plotter() object is named 'self'.")
                    print("Use 'import o2sclpy' and 'help(o2sclpy)' +"
                          "for more help on o2sclpy "+
                          "classes and functions.")
                    code.interact(local=locals())
                    
                elif cmd_name=='eval':
                    
                    if self.verbose>2:
                        print('Process eval.')
                        print('args:',strlist[ix:ix_next])

                    eval(strlist[ix+1],None,locals())
                    
                elif cmd_name=='exec':
                    
                    if self.verbose>2:
                        print('Process exec.')
                        print('args:',strlist[ix:ix_next])

                    exec(open(strlist[ix+1]).read(),None,locals())
                    
                elif cmd_name=='image':
                    
                    if self.verbose>2:
                        print('Process image.')
                        print('args:',strlist[ix:ix_next])

                    import matplotlib.image as img
                    im=img.imread(strlist[ix+1])
                    
                    # Rescale the figure to insure the correct
                    # aspect ratio
                    height=im.shape[0]
                    width=im.shape[1]
                    fig_size_x=6
                    fig_size_y=height*fig_size_x/width
                    if fig_size_y>10:
                        fig_size_y=10
                        fig_size_x=fig_size_y*width/height
                        
                    default_plot(0.0,0.0,0.0,0.0,fig_size_x=fig_size_x,
                                 fig_size_y=fig_size_y)
                    
                    import matplotlib.pyplot as plot
                    plot.imshow(im)
                    plot.show()
                    
                elif cmd_name=='rect':
                    
                    if self.verbose>2:
                        print('Process rect.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for rect option.')
                    elif ix_next-ix<6:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4])
                    elif ix_next-ix<7:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  strlist[ix+5])
                    else:
                        self.rect(strlist[ix+1],strlist[ix+2],
                                  strlist[ix+3],strlist[ix+4],
                                  strlist[ix+5],
                                  **string_to_dict(strlist[ix+6]))
                        
                elif cmd_name=='ellipse':
                    
                    if self.verbose>2:
                        print('Process ellipse.')
                        print('args:',strlist[ix:ix_next])
                        
                    if ix_next-ix<5:
                        print('Not enough parameters for ellipse option.')
                    elif ix_next-ix<6:
                        self.ellipse(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4])
                    elif ix_next-ix<7:
                        self.ellipse(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4],
                                     strlist[ix+5])
                    else:
                        self.ellipse(strlist[ix+1],strlist[ix+2],
                                     strlist[ix+3],strlist[ix+4],
                                     strlist[ix+5],
                                     **string_to_dict(strlist[ix+6]))
                        
                elif cmd_name=='show':
                    if self.verbose>2:
                        print('Process show.')
                        print('args:',strlist[ix:ix_next])
                    self.show()
                elif cmd_name=='move-labels':
                    if self.verbose>2:
                        print('Process move-labels.')
                        print('args:',strlist[ix:ix_next])
                    self.move_labels()
                elif cmd_name=='canvas':
                    if self.verbose>2:
                        print('Process canvas.')
                        print('args:',strlist[ix:ix_next])
                    self.canvas()
                elif cmd_name=='clf':
                    if self.verbose>2:
                        print('Process clf.')
                        print('args:',strlist[ix:ix_next])
                    import matplotlib.pyplot as plot
                    plot.clf()
                    self.canvas_flag=False
                elif cmd_name=='backend':
                    if self.verbose>2:
                        print('Process backend in __init__.py.')
                        print('args:',strlist[ix:ix_next])
                else:
                    if self.verbose>2:
                        print('Process acol command '+cmd_name+'.')
                        print('args:',strlist[ix:ix_next])
                    self.gen_acol(o2scl,amp,self.link2,cmd_name,
                                  strlist[ix+1:ix_next])
                    # AWS, 3/9/23: I had to take this out, I think
                    # because it's not supported in the older version
                    # of HDF5 which is used in Ubuntu, but at some
                    # point I can put it back.
                    #
                    # if (cmd_name=='v' or cmd_name=='version'):
                    #     try:
                    #         import h5py
                    #     except:
                    #         print('\n(Import h5py failed.)')
                    #     else:
                    #         vv=h5py.h5.get_libversion()
                    #         print('\nHDF5 version from h5py:',
                    #               vv[0],vv[1],vv[2])
                    
                # Increment to the next option
                ix=ix_next
                
            if self.verbose>2:
                print('Going to next argument in parse_string_list().')
                
        # End of function o2graph_plotter::parse_string_list()
        return
    
