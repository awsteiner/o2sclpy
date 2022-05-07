#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2022, Andrew W. Steiner
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
import sys

# For os.getenv()
import os

# For numpy.bytes_
import numpy

# To test between Linux/OSX using system()
import platform

# For CDLL loading
import ctypes
from ctypes.util import find_library

def remove_spaces(string):
    while len(string)>0 and string[0]==' ':
        string=string[1:]
    return string

def doc_replacements(s,base_list_new,ter):

    # Replace commands in base_list_new
    for i in range(0,len(base_list_new)):
        s=s.replace('``'+base_list_new[i][0]+'``',
                    ter.cyan_fg()+ter.bold()+base_list_new[i][0]+
                    ter.default_fg())

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

def reformat_python_docs(cmd,doc_str,base_list_new):

    reflist=doc_str.split('\n')
    
    for i in range(0,len(reflist)):
        reflist[i]=remove_spaces(reflist[i])
        #print(i,'x',reflist[i],'x')

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
        for i in range(0,len(reflist)):
            doc_str2=doc_str2+'\n'+reflist[i]

    reflist2=doc_str2.split('\n\n')

    if False:
        for i in range(0,len(reflist2)):
            print(i,'x',reflist2[i],'x')
    
    ter=terminal_py()
    ncols=os.get_terminal_size().columns

    short=''
    parm_desc=''
    long_help=''

    # The short description
    if len(reflist2)>=2:
        short=reflist2[1]

    # The parameter description
    if len(reflist2)>=3:
        parm_desc=reflist2[2].replace('\n',' ')

        parm_desc=parm_desc.replace('  ',' ')
        sx='Command-line arguments: ``'
        if parm_desc[0:len(sx)]==sx:
            parm_desc=parm_desc[len(sx):]
        if parm_desc[-2:]=='``':
            parm_desc=parm_desc[0:-2]
            
    print('Usage: '+ter.cyan_fg()+ter.bold()+cmd+
          ter.default_fg()+' '+parm_desc)
    print('Short description:',short)

    if len(reflist2)>=4:
        print('')
        print('Long description:')
        for j in range(3,len(reflist2)):
            if len(reflist2[j])>0:
                long_help=doc_replacements(reflist2[j].replace('\n',' '),
                                           base_list_new,ter)
                tmplist=wrap_line(long_help,ncols-1)
                if j!=3:
                    print('')
                for k in range(0,len(tmplist)):
                    print(tmplist[k])

def string_to_color(str_in):
    """
    Convert a string to a color
    """

    if str_in[0]=='(':
        temps=str_in[1:len(str_in)-1]
        temp2=temps.split(',')
        return (float(temp2[0]),float(temp2[1]),float(temp2[2]))
    elif str_in[0]=='[':
        temps=str_in[1:len(str_in)-1]
        temp2=temps.split(',')
        return [float(temp2[0]),float(temp2[1]),float(temp2[2]),
                float(temp2[3])]
    
    return str_in

def if_yt_then_Agg(backend,argv):
    # Determine if yt commands are present
            
    yt_found=False
    for i in range(1,len(argv)):
        if argv[i][0:4]=='-yt-' and yt_found==False:
            if backend!='' and backend!='agg' and backend!='Agg':
                print('Backend was not set to Agg but yt commands were found.')
            yt_found=True
            backend='Agg'
    return backend

def o2scl_get_type(o2scl,amp):
    """
    Get the type of the current object stored in the acol_manager
    pointer
    """
    # pointer types
    char_ptr=ctypes.POINTER(ctypes.c_char)
    char_ptr_ptr=ctypes.POINTER(char_ptr)
    int_ptr=ctypes.POINTER(ctypes.c_int)
    
    # Set up wrapper for type function
    type_fn=o2scl.o2scl_acol_get_type
    type_fn.argtypes=[ctypes.c_void_p,int_ptr,char_ptr_ptr]
    
    # Get current type
    it=ctypes.c_int(0)
    type_ptr=char_ptr()
    type_fn(amp,ctypes.byref(it),ctypes.byref(type_ptr))

    # Construct the type as a byte string
    curr_type=b''
    for i in range(0,it.value):
        curr_type=curr_type+type_ptr[i]
    return curr_type

def table3d_get_slice(o2scl,amp,name):
    """
    Return a slice from the current table3d object stored
    in the acol_manager object 'amp'
    """
    get_fn=o2scl.o2scl_acol_get_slice
    get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                     int_ptr,double_ptr_ptr,
                     int_ptr,double_ptr_ptr,double_ptr_ptr]
    
    slice=ctypes.c_char_p(force_bytes(slice_name))
    nx=ctypes.c_int(0)
    ptrx=double_ptr()
    ny=ctypes.c_int(0)
    ptry=double_ptr()
    ptrs=double_ptr()
    get_fn(amp,slice,ctypes.byref(nx),ctypes.byref(ptrx),
           ctypes.byref(ny),ctypes.byref(ptry),
           ctypes.byref(ptrs))
    return (nx,ptrx,ny,ptry,ptrs)

def table_get_column(o2scl,amp,name,return_pointer=False):
    """
    Return a column from the current table object stored
    in the acol_manager object 'amp'
    """

    # C types
    int_ptr=ctypes.POINTER(ctypes.c_int)
    double_ptr=ctypes.POINTER(ctypes.c_double)
    double_ptr_ptr=ctypes.POINTER(double_ptr)

    # Function interface
    get_fn=o2scl.o2scl_acol_get_column
    get_fn.argtypes=[ctypes.c_void_p,ctypes.c_char_p,
                     int_ptr,double_ptr_ptr]
    get_fn.restype=ctypes.c_int

    # Arguments
    col=ctypes.c_char_p(force_bytes(name))
    size=ctypes.c_int(0)
    pointer=double_ptr()

    # Function call
    get_ret=get_fn(amp,col,ctypes.byref(size),ctypes.byref(pointer))
    if get_ret!=0:
        print('Failed to get column named "'+name+'".')
        return None

    if return_pointer:
        return pointer
        
    col=[pointer[i] for i in range(0,size.value)]
    return col

def is_number(s):
    """
    Return true if 's' is likely a number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def force_bytes(obj):
    """
    This function returns the bytes object corresponding to ``obj``
    in case it is a string using UTF-8. 
    """
    if isinstance(obj,numpy.bytes_)==False and isinstance(obj,bytes)==False:
        return bytes(obj,'utf-8')
    return obj

def force_string(obj):
    """
    This function returns the bytes object corresponding to ``obj``
    in case it is a string using UTF-8. 
    """
    if isinstance(obj,numpy.bytes_)==True or isinstance(obj,bytes)==True:
        return obj.decode('utf-8')
    return obj

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
                 right_margin=0.04,top_margin=0.04,fontsize=16,
                 fig_size_x=6.0,fig_size_y=6.0,ticks_in=False,
                 rt_ticks=False,editor=False):
    
    import matplotlib.pyplot as plot

    """
    This function sets up the O\ :sub:`2`\ sclpy ``matplotlib``
    defaults. It returns a pair of objects, the figure object and axes
    object. The fontsize argument times 0.8 is used 
    for the size of the font labels. Setting the ``ticks_in`` argument
    to ``True`` makes the ticks point inwards instead of outwards
    and setting ``rt_ticks`` to ``True`` puts ticks (but not labels)
    on the right and top edges of the plot. 
    
    This function is in ``utils.py``.
    """
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')
    plot.rcParams['lines.linewidth']=0.5
    
    if editor:
        
        fig=plot.figure(1,figsize=(fig_size_x*2,fig_size_y))
        fig.set_facecolor('white')
        
        ax_left_panel=plot.axes([0,0,0.5,1],facecolor=(1,1,1,0),
                                autoscale_on=False)
        ax_left_panel.margins(x=0,y=0)
        ax_left_panel.axis('off')
        
        ax_right_panel=plot.axes([0.5,0,0.5,1],facecolor=(0.9,0.9,0.9,1),
                                 autoscale_on=False)
        ax_right_panel.margins(x=0,y=0)
        ax_right_panel.get_xaxis().set_visible(False)
        ax_right_panel.get_yaxis().set_visible(False)
        ax=plot.axes([left_margin/2.0,bottom_margin,
                           (1.0-left_margin-right_margin)/2,
                           1.0-top_margin-bottom_margin])
    else:
        
        fig=plot.figure(1,figsize=(fig_size_x,fig_size_y))
        fig.set_facecolor('white')
        
        ax=plot.axes([left_margin,bottom_margin,
                      1.0-left_margin-right_margin,
                      1.0-top_margin-bottom_margin])
        
    ax.minorticks_on()
    # Make the ticks longer than default
    ax.tick_params('both',length=12,width=1,which='major')
    ax.tick_params('both',length=5,width=1,which='minor')
    ax.tick_params(labelsize=fontsize*0.8)
    plot.grid(False)

    if editor:
        return (fig,ax,ax_left_panel,ax_right_panel)
    
    return (fig,ax)
    
def get_str_array(dset):
    """
    Extract a string array from O\ :sub:`2`\ scl HDF5 dataset ``dset``
    as a python list

    This function is in ``utils.py``.
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

def get_ic_ptrs_to_list(size,lengths,chars):
    """
    """
    tlist=[]
    count=0
    for i in range(0,size.value):
        strt=b''
        for j in range(0,lengths[i]):
            strt=strt+chars[count]
            count+=1
        tlist.append(strt)
    return tlist

def parse_arguments(argv,verbose=0):
    """
    Old command-line parser (this is currently unused and
    it's not clear if it will be useful in the future).

    This function is in ``utils.py``.
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
    Convert a string to a dictionary, with extra processing for
    colors, subdictionaries, and matplotlib keyword arguments which
    are expected to have integer or floating point values.

    This function is in ``utils.py``.
    """

    # First split into keyword = value pairs
    arr=s.split(',')
    # Create empty dictionary
    dct={}
    # If we need to skip arguments
    skip=0

    if len(s)==0:
        return dct
    
    for i in range(0,len(arr)):

        if skip>0:
            skip=skip-1
        else:
            # For each pair, split keyword and value.
            arr2=arr[i].split('=')

            # Remove preceeding and trailing whitespace from the
            # keywords (not for the values)
            while arr2[0][0].isspace():
                arr2[0]=arr2[0][1:]
            while arr2[0][len(arr2[0])-1].isspace():
                arr2[0]=arr2[0][:-1]

            # Remove quotes if necessary
            if len(arr2)>1 and len(arr2[1])>2:
                if arr2[1][0]=='\'' and arr2[1][len(arr2[1])-1]=='\'':
                    arr2[1]=arr2[1][1:len(arr2[1])-1]
                if arr2[1][0]=='"' and arr2[1][len(arr2[1])-1]=='"':
                    arr2[1]=arr2[1][1:len(arr2[1])-1]

            # If one of the entries is arrowstyle, then combine
            # it with the head_width, head_length, and tail_width
            # options if they are present
            if arr2[0]=='arrowstyle':
                for j in range(0,len(arr)):
                    if arr[j].split('=')[0]=='head_width':
                        arr2[1]=arr2[1]+',head_width='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='head_length':
                        arr2[1]=arr2[1]+',head_length='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='tail_width':
                        arr2[1]=arr2[1]+',tail_width='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='shrink_factor':
                        arr2[1]=arr2[1]+',shrink_factor='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='widthA':
                        arr2[1]=arr2[1]+',widthA='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='widthB':
                        arr2[1]=arr2[1]+',widthB='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='lengthB':
                        arr2[1]=arr2[1]+',lengthB='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='as_angleB':
                        arr2[1]=arr2[1]+',angleB='+arr[j].split('=')[1]
                print('Found arrowstyle option, reprocessed:',arr2[1])

            # If one of the entries is connection style, then process
            # accordingly
            if arr2[0]=='connectionstyle':
                for j in range(0,len(arr)):
                    if arr[j].split('=')[0]=='angleA':
                        arr2[1]=arr2[1]+',angleA='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='cs_angleB':
                        arr2[1]=arr2[1]+',angleB='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='armA':
                        arr2[1]=arr2[1]+',armA='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='armB':
                        arr2[1]=arr2[1]+',armB='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='rad':
                        arr2[1]=arr2[1]+',rad='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='fraction':
                        arr2[1]=arr2[1]+',fraction='+arr[j].split('=')[1]
                    if arr[j].split('=')[0]=='angle':
                        arr2[1]=arr2[1]+',angle='+arr[j].split('=')[1]
                print('Found connectionstyle option, reprocessed:',arr2[1])
                
            # convert strings to numbers if necessary
            if arr2[0]=='zorder':
                arr2[1]=float(arr2[1])
            if arr2[0]=='lw':
                arr2[1]=float(arr2[1])
            if arr2[0]=='linewidth':
                arr2[1]=float(arr2[1])
            if arr2[0]=='elinewidth':
                arr2[1]=float(arr2[1])
            if arr2[0]=='alpha':
                arr2[1]=float(arr2[1])
            if arr2[0]=='shrinkA':
                arr2[1]=int(arr2[1])
            if arr2[0]=='shrinkB':
                arr2[1]=int(arr2[1])
            if arr2[0]=='bins':
                arr2[1]=int(arr2[1])
            if arr2[0]=='fig_size_x':
                arr2[1]=float(arr2[1])
            if arr2[0]=='fig_size_y':
                arr2[1]=float(arr2[1])
            if arr2[0]=='left_margin':
                arr2[1]=float(arr2[1])
            if arr2[0]=='right_margin':
                arr2[1]=float(arr2[1])
            if arr2[0]=='top_margin':
                arr2[1]=float(arr2[1])
            if arr2[0]=='bottom_margin':
                arr2[1]=float(arr2[1])
            if arr2[0]=='left':
                arr2[1]=float(arr2[1])
            if arr2[0]=='right':
                arr2[1]=float(arr2[1])
            if arr2[0]=='top':
                arr2[1]=float(arr2[1])
            if arr2[0]=='bottom':
                arr2[1]=float(arr2[1])
            if arr2[0]=='wspace':
                arr2[1]=float(arr2[1])
            if arr2[0]=='hspace':
                arr2[1]=float(arr2[1])
            if arr2[0]=='fontsize':
                arr2[1]=float(arr2[1])
            if arr2[0]=='font':
                arr2[1]=float(arr2[1])
            if arr2[0]=='scale':
                arr2[1]=float(arr2[1])
            if arr2[0]=='dpi':
                arr2[1]=float(arr2[1])
            if arr2[0]=='pad':
                arr2[1]=float(arr2[1])
            if arr2[0]=='capsize':
                arr2[1]=float(arr2[1])
            if arr2[0]=='capthick':
                arr2[1]=float(arr2[1])

            # Convert strings to bool values
            if arr2[0]=='sharex':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='lolims':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='uplims':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='xlolims':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='xuplims':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='reorient':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='sharey':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='squeeze':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='fill':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='ticks_in':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='rt_ticks':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
            if arr2[0]=='pcm':
                if arr2[1]=='True':
                    arr2[1]=True
                else:
                    arr2[1]=False
                    
            # Process color entries. The challenge here is that
            # dictionary entries are separated by commas, but there
            # are also commas inside color specifications. If color
            # contains a left parenthesis or a left bracket, then we
            # have to convert the string to an array. However, this
            # algorithm has a limitation: it can only handle (rgb) or
            # [rgba], but not [rgb] or (rgba).

            if (arr2[0]=='color' and
                arr[i][5]=='=' and arr[i][6]=='('):
                arr2[1]=arr2[1]+','+arr[i+1]+','+arr[i+2]
                skip=2
                arr2[1]=arr2[1][1:len(arr2[1])-1]
                arr3=arr2[1].split(',')
                arr2[1]=(float(arr3[0]),float(arr3[1]),float(arr3[2]))
                print('Found color:',arr2[1])
            elif (arr2[0]=='color' and
                  arr[i][5]=='=' and arr[i][6]=='['):
                arr2[1]=arr2[1]+','+arr[i+1]+','+arr[i+2]+','+arr[i+3]
                skip=3
                arr2[1]=arr2[1][1:len(arr2[1])-1]
                arr3=arr2[1].split(',')
                arr2[1]=[float(arr3[0]),float(arr3[1]),float(arr3[2]),
                         float(arr3[3])]
                print('Found color:',arr2[1])
            elif (arr2[0]=='textcolor' and
                arr[i][9]=='=' and arr[i][10]=='('):
                arr2[1]=arr2[1]+','+arr[i+1]+','+arr[i+2]
                skip=2
                arr2[1]=arr2[1][1:len(arr2[1])-1]
                arr3=arr2[1].split(',')
                arr2[1]=(float(arr3[0]),float(arr3[1]),float(arr3[2]))
                print('Found color:',arr2[1])
            elif (arr2[0]=='textcolor' and
                  arr[i][9]=='=' and arr[i][10]=='['):
                arr2[1]=arr2[1]+','+arr[i+1]+','+arr[i+2]+','+arr[i+3]
                skip=3
                arr2[1]=arr2[1][1:len(arr2[1])-1]
                arr3=arr2[1].split(',')
                arr2[1]=[float(arr3[0]),float(arr3[1]),float(arr3[2]),
                         float(arr3[3])]
                print('Found color:',arr2[1])

            if ((arr2[0]=='ls' or arr2[0]=='linestyle')
                and len(arr2)>=2 and len(arr2[1])>1
                and arr2[1][0]=='('):
                lstemp=arr[i]
                skip=0
                while (lstemp[-1]!=')' and lstemp[-2]!=')' and
                       i+1<len(arr)):
                    lstemp=lstemp+','+arr[i+1]
                    skip=skip+1
                    i=i+1
                if lstemp[-2]!=')' or lstemp[-1]!=')':
                    print('Failed to parse line style from',s)
                    quit()
                arr2[1]=eval(lstemp[3:])

            # if (arr2[0]=='color' and (arr2[1].find('(')!=-1 or
            #                           arr2[1].find('[')!=-1)):
            #     print('here',arr2[0],arr2[1])
            #     if arr2[1].find('(')==-1:
            #         loc1=arr2[1].find('[')
            #         loc2=arr2[1].find(']')
            #     else:
            #         loc1=arr2[1].find('(')
            #         loc2=arr2[1].find(')')
            #     print('here2',loc1,loc2)
            #     arr2[1]=arr2[1][loc1:loc2-loc1+1]
            #     print('here3',arr2[1])
            #     temp=arr2[1].split(',')
            #     if len(temp)==3:
            #         arr2[1]=[float(temp[0]),float(temp[1]),
            #                  float(temp[2])]
            #     else:
            #         arr2[1]=[float(temp[0]),float(temp[1]),
            #                  float(temp[2]),float(temp[3])]
            #     print('here4',arr2[1])

            # assign to dictionary (except for arrowstyle and
            # connectionstyle options which are handled separately
            # above)
            if (arr2[0]!='head_width' and arr2[0]!='head_length' and
                arr2[0]!='tail_width' and arr2[0]!='rad' and
                arr2[0]!='angleA' and arr2[0]!='as_angleB' and
                arr2[0]!='armA' and arr2[0]!='armB' and
                arr2[0]!='angle' and arr2[0]!='fraction' and
                arr2[0]!='shrink_factor' and arr2[0]!='widthA' and
                arr2[0]!='lengthB' and arr2[0]!='widthB' and
                arr2[0]!='cs_angleB'):
                if len(arr2)<2:
                    print('Original string:',s)
                    print('Current entry:',arr2)
                    print('Current dictionary:',dct)
                    raise Exception('Failed to parse string "'+s+
                                    '" as dictionary.')
                dct[arr2[0]]=arr2[1]
        
    return dct

class terminal_py:
    """
    Handle vt100 formatting sequences
    """
    
    redirected=False
    """
    If true, then the output is being redirected to a file, so 
    don't use the formatting sequences
    """
    
    def __init__(self):
        """
        Determine if the output is being redirected or not
        """
        if sys.stdout.isatty()==False:
            self.redirected=True
        return
    
    def cyan_fg(self):
        """
        Set the foreground color to cyan
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[36m'
        return strt
    
    def red_fg(self):
        """
        Set the foreground color to red
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[31m'
        return strt
    
    def magenta_fg(self):
        """
        Set the foreground color to magenta
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[35m'
        return strt
    
    def green_fg(self):
        """
        Set the foreground color to green
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[32m'
        return strt
    
    def bold(self):
        """
        Set the face to bold
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[1m'
        return strt
    
    def default_fg(self):
        """
        Set the foreground color to the default
        """
        strt=''
        if self.redirected:
            return strt
        strt=strt+chr(27)+'[m'
        return strt
    
    def horiz_line(self):
        """
        Return a string which represents a horizontal line. If possible,
        vt100-like terminal sequences are used to create a line.
        Otherwise, dashes are used.
        """
        str_line=''
        if self.redirected:
            for jj in range(0,78):
                str_line+='-'
        else:
            str_line=str_line+chr(27)+'(0'
            for jj in range(0,78):
                str_line+='q'
            str_line=str_line+chr(27)+'(B'
        return str_line

    def type_str(self,strt):
        return self.magenta_fg()+self.bold()+strt+self.default_fg()
    
    def cmd_str(self,strt):
        return self.cyan_fg()+self.bold()+strt+self.default_fg()
    
    def topic_str(self,strt):
        return self.green_fg()+self.bold()+strt+self.default_fg()
    
    def var_str(self,strt):
        return self.red_fg()+self.bold()+strt+self.default_fg()

def length_without_colors(strt):
    """
    Compute the length of strt, ignoring characters which correspond
    to VT100 formatting sequences
    """
    count=0
    index=0
    while index<len(strt):
        if strt[index]!=chr(27):
            count=count+1
        elif index+2<len(strt) and strt[index+1]=='[' and strt[index+2]=='m':
            index=index+2
        elif index+3<len(strt) and strt[index+1]=='[' and strt[index+3]=='m':
            index=index+3
        elif index+4<len(strt) and strt[index+1]=='[' and strt[index+4]=='m':
            index=index+4
        elif index+2<len(strt) and strt[index+1]=='(' and strt[index+2]=='0':
            index=index+2
        elif index+2<len(strt) and strt[index+1]=='(' and strt[index+2]=='B':
            index=index+2
        index=index+1
    return count
            
def wrap_line(line,ncols=79):
    """
    From a string 'line', create a list of strings which adds return
    characters in order to attempt to ensure each line is less than
    or equal to ncols characters long. This function also respects
    explicit carriage returns, ensuring they force a new line 
    independent of the line length. This function uses the
    'length_without_colors()' function above, to ensure VT100 formatting
    sequences aren't included in the count.
    """
    list=[]
    # First, just split by carriage returns
    post_list=line.split('\n')
    for i in range(0,len(post_list)):
        # If this line is already short enough, then just handle
        # it directly below
        if length_without_colors(post_list[i])>ncols:
            # A temporary string which will hold the current line
            strt=''
            # Now split by spaces
            post_word=post_list[i].split(' ')
            # Proceed word by word
            for j in range(0,len(post_word)):
                # If the current word is longer than ncols, then
                # clear the temporary string and add it to the list
                if length_without_colors(post_word[j])>ncols:
                    if length_without_colors(strt)>0:
                        list.append(strt)
                    list.append(post_word[j])
                    strt=''
                elif (length_without_colors(strt)+
                      length_without_colors(post_word[j])+1)>ncols:
                    # Otherwise if the next word will take us over the
                    # limit
                    list.append(strt)
                    strt=post_word[j]
                elif len(strt)==0:
                    strt=post_word[j]
                else:
                    strt=strt+' '+post_word[j]
            # If after the last word we still have anything in the
            # temporary string, then add it to the list
            if length_without_colors(strt)>0:
                list.append(strt)
        else:
            # Now if the line was already short enough, add it
            # to the list
            list.append(post_list[i])
                
    return list
            
def string_equal_dash(str1,str2):
    b1=force_bytes(str1)
    b2=force_bytes(str2)
    for i in range(0,len(b1)):
        if b1[i]==b'-':
            b1[i]=b'-'
    for i in range(0,len(b2)):
        if b2[i]==b'-':
            b2[i]=b'-'
    if b1==b2:
        return True
    return False

def screenify_py(tlist,ncols=79):
    maxlen=0
    for i in range(0,len(tlist)):
        if length_without_colors(tlist[i])>maxlen:
            maxlen=length_without_colors(tlist[i])
    # Add to ensure there is at least one space between columns
    maxlen=maxlen+1
    ncolumns=int(ncols/maxlen)
    nrows=int(len(tlist)/ncolumns)
    while nrows*ncolumns<len(tlist):
        nrows=nrows+1
    output_list=[]
    for i in range(0,nrows):
        row=''
        for j in range(0,ncolumns):
            if i+j*nrows<len(tlist):
                colt=tlist[i+j*nrows]
                while length_without_colors(colt)<maxlen:
                    colt=colt+' '
                row=row+colt
        output_list.append(row)
    return output_list
