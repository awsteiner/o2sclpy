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
import numpy
import textwrap

# For rectangles
import matplotlib.patches as patches

from o2sclpy.utils import default_plot, string_to_dict, terminal_py
from o2sclpy.doc_data import cmaps, new_cmaps

def marker_list():
    """ 
    Print a list of matplotlib markers which work in o2graph
    command-line arguments.
    """
    print('Matplotlib markers supported by O2graph:')
    ter=terminal_py()
    print(ter.horiz_line())
    outs='. point'.ljust(20)
    outs=outs+', pixel'.ljust(20)
    outs=outs+'o circle'.ljust(20)
    outs=outs+'v triangle_down'.ljust(20)+'\n'
    outs=outs+'^ triangle_up'.ljust(20)
    outs=outs+'< triangle_left'.ljust(20)
    outs=outs+'> triangle_right'.ljust(20)
    outs=outs+'1 tri_down'.ljust(20)+'\n'
    outs=outs+'2 tri_up'.ljust(20)
    outs=outs+'3 tri_left'.ljust(20)
    outs=outs+'4 tri_right'.ljust(20)
    outs=outs+'8 octagon'.ljust(20)+'\n'
    outs=outs+'s square'.ljust(20)
    outs=outs+'p pentagon'.ljust(20)
    outs=outs+'P plus (filled)'.ljust(20)
    outs=outs+'* star'.ljust(20)+'\n'
    outs=outs+'h hexagon1'.ljust(20)
    outs=outs+'H hexagon2'.ljust(20)
    outs=outs+'+ plus'.ljust(20)
    outs=outs+'x x'.ljust(20)+'\n'
    outs=outs+'X x (filled)'.ljust(20)
    outs=outs+'D diamond'.ljust(20)
    outs=outs+'d thin_diamond'.ljust(20)
    outs=outs+'| vline'.ljust(20)+'\n'
    outs=outs+'_ hline'.ljust(20)
    outs=outs+'$...$ mathtext string'.ljust(20)
    print(outs)
    print(' ')
    print("To create a plot of examples, use",
          "'o2graph -help markers-plot' or")
    print("'o2graph -help markers-plot plot_file.png'")
    return

def markers_plot(fname=''):
    """ 
    Plot the matplotlib markers which work in o2graph
    command-line arguments.
    """
    
    import matplotlib.pyplot as plot
    
    mlist=[['.',"'.'",'point'],
           [',',"','",'pixel'],
           ['o',"'o'",'circle'],
           ['v',"'v'",'down triangle'],
           ['^',"'^'",'up triangle'],
           ['<',"'<'",'left triangle'],
           ['>',"'>'",'right triangle'],
           ['1',"'1'",'down tri'],
           ['2',"'2'",'up tri'],
           ['3',"'3'",'left tri'],
           ['4',"'4'",'right tri'],
           ['8',"'8'",'octagon'],
           ['s',"'s'",'square'],
           ['p',"'p'",'pentagon'],
           ['P',"'P'",'plus (filled)'],
           ['*',"'*'",'star'],
           ['h',"'h'",'hexagon 1'],
           ['H',"'H'",'hexagon 2'],
           ['+',"'+'",'plus'],
           ['x',"'x'",'x'],
           ['X',"'X'",'filled x'],
           ['D',"'D'",'diamond'],
           ['d',"'d'",'thin diamond'],
           ['|',"'|'",'vertical line'],
           ['_',"'_'",'horizontal line'],
           [0,"0",'left tick'],
           [1,"1",'right tick'],
           [2,"2",'up tick'],
           [3,"3",'down tick'],
           [4,"4",'left caret'],
           [5,"5",'right caret'],
           [6,"6",'up caret'],
           [7,"7",'down caret'],
           [8,"8",'left shifted caret'],
           [9,"9",'right shifted caret'],
           [10,"10",'up shifted caret'],
           [11,"11",'down shifted caret'],
           ['$x^2$',"\$x^2\$",'math example']]
    nmark=len(mlist)
    ncols=2
    nrows=(nmark+(nmark%2))/ncols
    fig_dict=('left_margin=0.01,top_margin=0.01,'+
              'right_margin=0.01,'+
              'bottom_margin=0.01,'+
              'fontsize=10,ticks_in=False,'+
              'rt_ticks=False')
    dct=string_to_dict(fig_dict)
    (fig,axes)=default_plot(**dct)
    axes.set_xlim(0,1)
    axes.set_ylim(0,0.86)
    axes.set_axis_off()
    row_ctr=0
    col_ctr=0
    for entry in mlist:
        if row_ctr>2:
            plot.rc('text',usetex=False)
            axes.plot([(col_ctr+0.1)/(ncols)],
                      [float(nrows-row_ctr)/(nrows+1)],
                      marker=entry[0],color='black',markersize=10)
            axes.text((col_ctr+0.25)/(ncols),
                      float(nrows-row_ctr)/(nrows+1),
                      entry[1],family='monospace',
                      va='center',ha='center',fontsize=16)
            plot.rc('text',usetex=True)
            axes.text((col_ctr+0.37)/(ncols),
                      float(nrows-row_ctr)/(nrows+1),
                      entry[2].replace('_','\_'),
                      va='center',ha='left',fontsize=16)
        row_ctr=row_ctr+1
        if row_ctr>=nrows:
            row_ctr=0
            col_ctr=col_ctr+1
        axes.text(0.5,0.835,r'$ \mathrm{O}_2\mathrm{sc'+
                  'lpy~markers~summary} $',
                  fontsize=16,ha='center')
    if fname!='':
        plot.savefig(fname)
        print("Saved image in file",(fname+"."))
    import matplotlib
    if (matplotlib.get_backend()!='Agg' and 
        matplotlib.get_backend()!='agg'):
        if fname=='':
            plot.show()
    elif fname=='':
        print('Backend is Agg but no filename is specified',
              'so no output was created.')
    return

def colors_near(col='',fname=''):
    """
    Create a plot of all colors near a specified colors, and
    optionally, store the plot in file named 'fname'.
    Possible values of 'col' are red, orange, yellow, green,
    cyan, blue, purple, magenta, pink, grey, and gray.
    """
    
    import matplotlib.pyplot as plot
    
    if col=='all':
        
        from matplotlib import colors as mc
        colors=dict(**mc.CSS4_COLORS,**mc.XKCD_COLORS)
        by_hsv=sorted((tuple(mc.rgb_to_hsv(mc.to_rgba(color)[:3])),name)
                      for name, color in colors.items())
        sorted_names=[(hsv, name) for hsv, name in by_hsv]
        selected=[]
        
        print('Hue          Saturation',
              '  Value        name')
        for i in range(0,len(sorted_names)):
            print('%7.6e %7.6e %7.6e %s' %
                  (sorted_names[i][0][0],
                   sorted_names[i][0][1],
                   sorted_names[i][0][2],
                   sorted_names[i][1]))
    elif col=='':

        docstr=('o2graph -help colors-near <color> shows a '+
                'plot of colors near <color>, where <color> can be '+
                'either a named color like black or \"xkcd:pea green\", '+
                'an rgb array of the form (r,g,b) where r, g, and b are '+
                'all between 0 and 1, or a hexadecimalcolor like '+
                '\"ff8200\". o2graph -help colors-near <color> <filename> '+
                'shows a plot of '+
                'colors near <color> and stores the plot in <filename>. '+
                'o2graph -help colors-near all gives a list of all CSS4 '+
                'and XKCD colors')
        str_list=textwrap.wrap(docstr,79)
        for i in range (0,len(str_list)):
            print(str_list[i])
        
    else:

        from matplotlib.colors import to_rgba
        from matplotlib import colors as mc

        # Obtain a list of CSS4 and XKCD colors
        colors=dict(**mc.CSS4_COLORS,**mc.XKCD_COLORS)

        # Remove leading space
        while col[0].isspace():
            col=col[1:]

        # Convert from string to [r,g,b] if necessary
        if col[0]=='(' or col[0]=='[':
            col=col.replace('(',' ')
            col=col.replace(')',' ')
            col=col.replace('[',' ')
            col=col.replace(']',' ')
            col=col.split(',')
            col=[float(col[0]),float(col[1]),float(col[2])]
        
        # Convert the specified color to [r,g,b,a] where
        # all four entries are between 0 and 1
        
        colt=to_rgba(col)
        print('converted',col,'to',colt)
        ir=colt[0]
        ig=colt[1]
        ib=colt[2]
        
        selected=[]
        
        crange=0.100
        while len(selected)<80:
            selected=[]
            for key in colors:
                hexc=colors[key]
                jr=float(int(hexc[1]+hexc[2],16))/255.0
                jg=float(int(hexc[3]+hexc[4],16))/255.0
                jb=float(int(hexc[5]+hexc[6],16))/255.0
                diff=abs(jr-ir)+abs(jg-ig)+abs(jb-ib)
                if diff<crange:
                    selected.append((key,diff))
            if len(selected)<80:
                crange=crange+0.002
                
        if len(selected)>=80:
            def sort_first(val):
                return val[0]
            selected2=sorted(selected,key=lambda x: x[1])
            #print(selected2)
            #print('Found list with range ',crange)

        # If col was converted to (r,g,b), then convert back to a
        # string.
        col_fixpound=str(col).replace('#','\\#')
        title=(r'$ \mathrm{O}_2\mathrm{sc'+
               'lpy~list~of~colors~near~'+col_fixpound+'}: $')
        #print('title',title)

        if len(selected)>80:
            selected=selected[0:80]
    
        if len(selected)>0:
            #print('selected',selected)
            n=len(selected)
            header=1
            ncols=4
            nrows=n//ncols
            #print('ncols,nrows',ncols,nrows)
            plot.rc('text',usetex=True)
            plot.rc('font',family='serif')
            fig,axes=plot.subplots(figsize=(9.5,6.4))
            # Get height and width
            X,Y=fig.get_size_inches()*100
            h=Y/(nrows+header+1)
            w=X/ncols
        
            for i in range(0,n):
                row=i%nrows
                column=i//nrows
                y=Y-((row+header)*h)-h
                xi_line=w*(column+0.05)
                xf_line=w*(column+0.25)
                xi_text=w*(column+0.3)
                
                axes.text(xi_text,y,selected[i][0],
                          fontsize=(h*0.4),
                          ha='left',va='center')
    
                axes.hlines(y+h*0.1,xi_line,xf_line,
                            color=selected[i][0],
                            linewidth=(h*0.8))

            column=2.4
            row=-1.2
            y=Y-((row+header)*h)-h
            xi_line=w*(column+0.05)
            xf_line=w*(column+0.25)
            xi_text=w*(column+0.3)
            axes.text(w*(column),y,title,
                      fontsize=(h*0.5),ha='right',va='center')
            axes.hlines(y+h*0.1,xi_line,xf_line,
                        color=col,linewidth=(h*0.8))
            
            axes.set_xlim(0,X)
            axes.set_ylim(0,Y+header)
            axes.set_axis_off()
                                    
            fig.subplots_adjust(left=0,right=1,top=1,bottom=0,
                                hspace=0,wspace=0)
            if fname!='':
                plot.savefig(fname)
                print('Created file '+fname+'.')
            import matplotlib
            if (matplotlib.get_backend()!='Agg' and 
                matplotlib.get_backend()!='agg'):
                if fname=='':
                    plot.show()
            elif fname=='':
                print('Backend is Agg but no filename is specified',
                      'so no output was created.')
        else:
            print('Error. Not enough colors selected in colors_near().')
            
    return

def cmap_list_func():
    """ 
    List the matplotlib and o2sclpy colormaps.
    """
    print('Matplotlib colormaps:')
    ter=terminal_py()
    print(ter.horiz_line())
    for category, cmap_list in cmaps:
        list2=''
        for name in cmap_list:
            list2+=name+' '
        str_list=textwrap.wrap(category+': '+list2,79)
        for i in range (0,len(str_list)):
            print(str_list[i])
        print(' ')
    for category, cmap_list in new_cmaps:
        list2=''
        for name in cmap_list:
            list2+=name+' '
        str_list=textwrap.wrap(category+': '+list2,79)
        for i in range (0,len(str_list)):
            print(str_list[i])
        print(' ')
    print('Remember that colormaps can all be',
          'reversed by using a "_r" suffix.')
    print(' ')
    print("To create a plot of the colormaps, use",
          "'o2graph -help cmaps-plot' or")
    print("'o2graph -help cmaps-plot plot_file.png'")
    return

def cmaps_plot(fname=''):
    """ 
    Create a plot of matplotlib and o2sclpy colormaps.
    """
    print('Generating colormap summary figure.')
                        
    import matplotlib.pyplot as plot
    
    # An internal implementation of
    # https://matplotlib.org/3.1.0/gallery/
    # color/colormap_reference.html
                        
    #self.left_margin=0.01
    #self.right_margin=0.01
    #self.top_margin=0.01
    #self.bottom_margin=0.01
    gradient=numpy.linspace(0,1,256)
    gradient=numpy.vstack((gradient,gradient))
                        
    nrows=0
    for category, cmap_list in cmaps:
        for name in cmap_list:
            nrows=nrows+1
    for category, cmap_list in new_cmaps:
        for name in cmap_list:
            nrows=nrows+1
    ncols=3
    while nrows%ncols!=0:
        nrows=nrows+1
    nrows=int((nrows)/ncols)

    # Manually create figure and axes 
    fig_x=7.0
    fig_y=0.95*(0.35+0.15+(nrows+(nrows-1)*0.1)*0.22)
    (fig,axes)=plot.subplots(nrows=nrows,
                                       ncols=ncols,
                                       figsize=(fig_x,
                                                fig_y))
    fig.subplots_adjust(top=1.0-0.35/fig_y,
                             bottom=0.15/fig_y,
                             left=0.01,right=0.99,
                             wspace=0.01)
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')

    for i in range(0,nrows):
        for j in range(0,ncols):
            axes[i][j].set_axis_off()
                        
    row_ctr=0
    col_ctr=0
    for category, cmap_list in cmaps:
        for name in cmap_list:
            name2=name.replace('_','\_')
            ax=axes[row_ctr][col_ctr]
            ax.imshow(gradient,aspect='auto',
                             cmap=plot.get_cmap(name))
            r=patches.Rectangle((0.32,0.1),0.36,0.8,0,
                                fc=(1,1,1,0.7),lw=0,
                                fill=True,
                                transform=ax.transAxes)
            ax.add_patch(r)
            ax.text(0.5,0.45,name2,
                                va='center',ha='center',
                                fontsize=8,color=(0,0,0),
                                transform=ax.transAxes)
            row_ctr=row_ctr+1
            if row_ctr>=nrows:
                row_ctr=0
                col_ctr=col_ctr+1
    for category, cmap_list in new_cmaps:
        for name in cmap_list:
            name2=name.replace('_','\_')
            ax=axes[row_ctr][col_ctr]
            ax.imshow(gradient,aspect='auto',
                      cmap=plot.get_cmap(name))
            r=patches.Rectangle((0.32,0.1),0.36,0.8,0,fc=(1,1,1,0.7),lw=0,
                                fill=True,transform=ax.transAxes)
            ax.add_patch(r)
            ax.text(0.5,0.45,name2,va='center',ha='center',
                    fontsize=8,color=(0,0,0),transform=ax.transAxes)
            row_ctr=row_ctr+1
            if row_ctr>=nrows:
                row_ctr=0
                col_ctr=col_ctr+1

    ax=axes[0][0]
    ax.text(1.5,1.7,
            (r'$ \mathrm{O}_2\mathrm{sc'+
             'lpy~colormap~summary} $'),
            ha='center',va='center',fontsize=16,
            transform=ax.transAxes)
    if fname!='':
        plot.savefig(fname)
        print('Created image file '+fname+'.')
    print('Remember that colormaps can all be',
          'reversed by using a "_r" suffix.')
    import matplotlib
    if (matplotlib.get_backend()!='Agg' and 
        matplotlib.get_backend()!='agg'):
        if fname=='':
            plot.show()
    elif fname=='':
        print('Backend is Agg but no filename is specified',
              'so no output was created.')
    return

def colors_plot(fname='',dpi=10):
    """
    Create a plot of the matplotlib CSS4 colors and, optionally,
    store the plot in file named 'fname'.
    """
    from matplotlib import colors as mc
    import matplotlib.pyplot as plot

    colors=dict(**mc.CSS4_COLORS)
    by_hsv=sorted((tuple(mc.rgb_to_hsv(mc.to_rgba(color)[:3])),name)
                    for name, color in colors.items())
    sorted_names=[name for hsv, name in by_hsv]
    n=len(sorted_names)
    header=1
    ncols=4
    nrows=n//ncols
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')
    fig,axes=plot.subplots(figsize=(8,6.6))
    # Get height and width
    fig.set_dpi(dpi)
    X,Y=fig.get_dpi()*fig.get_size_inches()
    h=Y/(nrows+1+header)
    w=X/ncols

    for i, name in enumerate(sorted_names):
        row=i%nrows
        col=i//nrows
        y=Y-((row+header)*h)-h
        xi_line=w*(col+0.05)
        xf_line=w*(col+0.25)
        xi_text=w*(col+0.3)
        axes.text(xi_text,y,name,fontsize=(h*0.6),
                ha='left',va='center')

        axes.hlines(y+h*0.1,xi_line,xf_line,
                  color=colors[name],linewidth=(h*0.8))

        axes.set_xlim(0,X)
        axes.set_ylim(0,Y+header)
        axes.set_axis_off()
                            
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0,
                        hspace=0,wspace=0)
    axes.text(X*0.5,(Y+header)*0.965,r'$ \mathrm{O}_2\mathrm{sc'+
              'lpy~colors~summary} $',fontsize=16,ha='center')
    if fname!='':
        plot.savefig(fname)
        print('Created image file '+fname+'.')
    import matplotlib
    if (matplotlib.get_backend()!='Agg' and 
        matplotlib.get_backend()!='agg'):
        if fname=='':
            plot.show()
    elif fname=='':
        print('Backend is Agg but no filename is specified',
              'so no output was created.')
    return

def color_list():
    """
    List matplotlib base and CSS4 colors along with their
    values in #RRGGBB hexadecimal format.
    """
    from matplotlib import colors as mcolors
    print('Matplotlib colors:')
    ter=terminal_py()
    print(ter.horiz_line())
    base_dict=dict(mcolors.BASE_COLORS)
    css4_dict=dict(**mcolors.CSS4_COLORS)
    print(len(base_dict),'base colors:')
    outs=''
    ctr=0
    for col in base_dict:
        outs=outs+(col+' '+str(base_dict[col])).ljust(20)
        if ctr%4==3:
            outs=outs+'\n'
        ctr=ctr+1
    print(outs)
    print(len(css4_dict),'CSS4 colors:')
    outs=''
    ctr=0
    for col in css4_dict:
        if ctr%3==0:
            outs=outs+(col+' '+str(css4_dict[col])).ljust(26)
        elif ctr%3==1:
            outs=outs+(col+' '+str(css4_dict[col])).ljust(28)
        else:
            outs=outs+(col+' '+str(css4_dict[col])).ljust(26)
            outs=outs+'\n'
        ctr=ctr+1
    print(outs)
    print(' ')
    outs=("o2sclpy also supports the (r,g,b) format, the [r,g,b,a] format, "+
          "the HTML format, the grayscale single-value format, "+
          "and the XKCD colors (see '-help xkcd-colors' for a list). "+
          "For (r,g,b) colors, parentheses must be used, and the r, g,"+
          " and b numbers should be from 0.0 to 1.0. For [r,g,b,a] "+
          "colors, square brackets must be used and the r, g, b, "+
          "and a numbers should be from 0.0 to 1.0. The HTML "+
          "format is #RRGGBB where RR, GG, and BB are two-digit "+
          "hexadecimal values.")
    str_list=textwrap.wrap(outs,79)
    for i in range (0,len(str_list)):
        print(str_list[i])
    print(' ')
    print("To create a plot of colors, use",
          "'o2graph -help colors-plot' or")
    print("'o2graph -help colors-plot plot_file.png'")
    return

def xkcd_colors_list():
    """
    List all of the XKCD colors along with their 
    values in #RRGGBB hexadecimal format.
    """
    from matplotlib import colors as mcolors
    xkcd_dict=dict(**mcolors.XKCD_COLORS)
    print('XKCD colors:')
    ter=terminal_py()
    print(ter.horiz_line())
    # These are commented out for now because
    # o2graph has a hard time with spaces in
    # color names
    print(len(xkcd_dict),'XKCD colors:')
    outs=''
    ctr=0
    for col in xkcd_dict:
        if ctr%2==0:
            outs=outs+(col+' '+str(xkcd_dict[col])).ljust(40)
        else:
            outs=outs+(col+' '+str(xkcd_dict[col])).ljust(39)
            outs=outs+'\n'
        ctr=ctr+1
    print(outs)
    return
