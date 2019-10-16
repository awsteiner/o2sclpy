cmaps=[('Perceptually Uniform Sequential',
        ['viridis','plasma','inferno','magma']),
       ('Sequential', 
        ['Greys','Purples','Blues','Greens','Oranges','Reds',
         'YlOrBr','YlOrRd','OrRd','PuRd','RdPu','BuPu',
         'GnBu','PuBu','YlGnBu','PuBuGn','BuGn','YlGn']),
       ('Sequential (2)', 
        ['binary','gist_yarg','gist_gray','gray','bone','pink',
         'spring','summer','autumn','winter','cool','Wistia',
         'hot','afmhot','gist_heat','copper']),
       ('Diverging', 
        ['PiYG','PRGn','BrBG','PuOr','RdGy','RdBu',
         'RdYlBu','RdYlGn','Spectral','coolwarm','bwr','seismic']),
       ('Qualitative', 
        ['Pastel1','Pastel2','Paired','Accent',
         'Dark2','Set1','Set2','Set3',
         'tab10','tab20','tab20b','tab20c']),
       ('Miscellaneous', 
        ['flag','prism','ocean','gist_earth','terrain','gist_stern',
         'gnuplot','gnuplot2','CMRmap','cubehelix','brg','hsv',
         'gist_rainbow','rainbow','jet','nipy_spectral','gist_ncar'])]
"""
List of cmaps for 'help cmaps'
"""

new_cmaps=[('O2sclpy cmaps',
            ['jet2','pastel2','reds2','greens2','blues2'])]
"""
List of new o2sclpy cmaps
"""

base_list=[
    ["arrow","Plot an arrow.",
     "<x1> <y1> <x2> <y2> <arrow properties> [kwargs]",
     "Plot an arrow from (x1,y1) to (x2,y2). This command uses "+
     "axes.annotate() to generate an arrow with an empty string "+
     "as the first argument to annotate(). The o2graph argument <arrow "+
     "properties> is the python dictionary for the 'arrowprops' "+
     "argument to annotate(). The arrowstyle and connectionstyle "+
     "attributes should be listed along with other arrowprops attributes.\n"+
     " \nExamples for arrowprops are:\n"+
     "\"arrowstyle=->,connectionstyle=arc3\"\n"+
     "\"arrowstyle=-|>,connectionstyle=arc,fc=red,ec=blue\"\n"+
     "\"arrowstyle=-|>,connectionstyle=arc,head_length=4.0,"+
     "head_width=1.0\"\n"+
     "\"arrowstyle=->,connectionstyle=arc3,head_length=4.0,"+
     "head_width=1.0,rad=-0.1\"\n"+
     "\"arrowstyle=fancy,connectionstyle=arc3,head_length=4.0,"+
     "head_width=1.0,rad=-0.1\"\n \n"+
     "Summary for arrowstyle argument (angleB is renamed to as_angleB):\n"+
     "Name    Attributes\n"+
     "-       None\n"+
     "->      head_length=0.4,head_width=0.2\n"+
     "-[      widthB=1.0,lengthB=0.2,as_angleB=None\n"+
     "|-      widthA=1.0,widthB=1.0\n"+
     "-|      head_length=0.4,head_width=0.2\n"+
     "<-      head_length=0.4,head_width=0.2\n"+
     "<-      head_length=0.4,head_width=0.2\n"+
     "<|      head_length=0.4,head_width=0.2\n"+
     "<|      head_length=0.4,head_width=0.2\n"+
     "fancy   head_length=0.4,head_width=0.4,tail_width=0.4\n"+
     "simple  head_length=0.5,head_width=0.5,tail_width=0.2\n"+
     "wedge   tail_width=0.3,shrink_factor=0.5\n \n"+
     "(note that fancy, simple or wedge require arc3 or angle3 connection "+
     "styles)\n \n"+
     "Summary for connectionstyle argument (angleB is renamed to "+
     "cs_angleB):\n"+
     "Name    Attributes\n"+
     "angle   angleA=90,cs_angleB=0,rad=0.0\n"+
     "angle3  angleA=90,cs_angleB=0\n"+
     "arc     angleA=0,cs_angleB=0,armA=None,armB=None,rad=0.0\n"+
     "arc3    rad=0.0\n"+
     "bar     armA=0.0,armB=0.0,fraction=0.3,angle=None\n \n"+
     "See https://matplotlib.org/2.0.2/users/annotations.html for more."],
    ["backend","Select the matplotlib backend to use.","<backend>",
     "This selects the matplotlib backend. "+
     "Typical values are 'Agg', 'TkAgg', 'WX', 'QTAgg', 'QT4Agg'. "+
     "Use -backend Agg to save the plot to a file without "+
     "opening a window. The backend can only be changed once, i.e. "+
     "if the \"backend\" command is invoked "+
     "more than once, then only the last invocation will have any "+
     "effect."],
    ["canvas","Create a plotting canvas.","",
     "Create an empty plotting canvas. For example 'o2graph "+
     "-canvas -show'."],
    ["clf","Clear the current figure.","",
     "Clear the current figure."],
    ["eval","Run the python eval() function.","<source code>",
     "Long desc."],
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
    ["plotv","Plot several vector-like data sets.",
     "[multiple vector spec. for x] <multiple vector spec. for y>",
     "The 'plotv' command plots one or several pairs of vectors for x "+
     "and y. The total number of curves plotted will be the number "+
     "of vector data sets from the first argument times the number "+
     "of vector data sets from the second argument. If the x and y "+
     "vector lengths are not equal, then the longer vector is "+
     "truncated. Any kwargs are applied to all curves plotted. For "+
     "details on multiple vector specifications, use "+
     "'o2graph -help mult-vector-spec'. Note that 'plotv' uses "+
     "the vector<contour_line> object as temporary storage, so if "+
     "the current object has type vector<contour_line> then you "+
     "will need to save that object to a file and use 'clear' first."],
    ["point","Plot a single point.","",""],
    ["python","Begin an interactive python session.","",""],
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
    ["text","Plot text in the data coordinates.",
     "<x> <y> <text> [kwargs]","The 'text' command plots text in the "+
     "data coordinates defined by the current axes with the font size "+
     "determined by the value of the parameter 'font'."],
    ["textbox",
     "Plot a box with text.","<x1> <y1> <text> <bbox properties> [kwargs]",
     "Plot text <text> and a box at location <x1> <y1>. For example, "+
     "textbox 0.5 0.5 \"$ f(x) $\" \"alpha=0.8,facecolor=white\" ."],
    ["ttext","Plot text in window coordinates [(0,0) to (1,1)].",
     "<x> <y> <text> [kwargs]","The 'text' command plots text in the "+
     "window coordinates [typically (0,0) to (1,1)] with the font size "+
     "determined by the value of the parameter 'font'."],
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
    ["yt-render","Render the yt visualization.",
     "<filename or pattern> [movie output filename]","Long desc."],
    ["yt-source-list","Source list.","","Long desc."],
    ["zlimits","Set the z-azis limits.","<low> <high>",
     "Set 'zlo' and 'zhi' to the specified limits, "+
     "and set 'zset' to true. If a plotting canvas is currently "+
     "open, then "+
     "the z-limits on that plot are modified. Future plots are also "+
     "set with the specified z-limits."],
    ["yt-tf","Edit the yt transfer function.","","Long desc."],
    ["subplots","Create subplots.","<nrows> <ncols> [kwargs]",
     "Create a grid of <nrows> by <ncols> subplots. "+
     "The kwargs currently supported are 'sharex', 'sharey', "+
     "and 'squeeze'."],
    ["selax","Select axis.","<index>",
     "Select which axis to use for subsequent plotting commands. "+
     "If a two-dimesional grid is made with 'subplots', then the "+
     "index starts at zero and goes to the right before proceeding "+
     "to the next row."],
    ["addcbar","Add color bar.","<left> <bottom> <width> <height> [kwargs]",
     "Add axis"],
    ["xtitle","Add x title to plot (or subplot).","",""],
    ["ytitle","Add y title to plot (or subplot).","",""],
    ["ztitle","Add z title to plot (yt only).","",""],
    ["inset","Add an inset (unfinished).","",""],
    ["subadj","Adjust subplots.","<kwargs>",
     "The kwargs for 'subadj' are left, right, bottom, top, "+
     "wspace, and hspace."]
]
"""
This is a list of 4-element entries:
1: command name
2: short description
3: argument list
4: full help text
"""

# Types which appear in extra_list below (not a list of all acol types)
extra_types=["table","table3d","hist_2d","hist","double[]","int[]",
             "size_t[]","tensor","tensor<int>","tensor<size_t>",
             "tensor_grid"]
"""
List of types which have additional plotting commands
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
    ["table","yt-scatter","Add scattered points to a yt scene",
     "<x column> <y column> <z column> [color column] [size column]",
     "Long desc."],
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
     "the base 10 log of the x- or y-grids specified in the hist_2d object "+
     "before plotting. A z-axis density legend is print on the RHS if colbar "+
     "is set to 1 before plotting. If z-axis limits are specified, then "+
     "values larger than the upper limit are set equal to the upper limit "+
     "and values smaller than the lower limit are set equal to the lower "+
     "limit before plotting."],
    ["tensor","den-plot","Create a density plot from a tensor object",
     "[index_1 index_2] [kwargs]",
     "Create a density plot from the current tensor. "+
     "If the tensor has rank 2 and the indices are not specifed, then "+
     "plot the first index along the x-axis and the second index along "+
     "the y-axis. "+
     "A z-axis density legend is print on the RHS if colbar "+
     "is set to 1 before plotting. If z-axis limits are specified, then "+
     "values larger than the upper limit are set equal to the upper limit "+
     "and values smaller than the lower limit are set equal to the lower "+
     "limit before plotting."],
    ["tensor<int>","den-plot","Create a density plot from a tensor object",
     "[index_1 index_2] [kwargs]",
     "Create a density plot from the current tensor. "+
     "If the tensor has rank 2 and the indices are not specifed, then "+
     "plot the first index along the x-axis and the second index along "+
     "the y-axis. "+
     "A z-axis density legend is print on the RHS if colbar "+
     "is set to 1 before plotting. If z-axis limits are specified, then "+
     "values larger than the upper limit are set equal to the upper limit "+
     "and values smaller than the lower limit are set equal to the lower "+
     "limit before plotting."],
    ["tensor<size_t>","den-plot","Create a density plot from a tensor object",
     "[index_1 index_2] [kwargs]",
     "Create a density plot from the current tensor. "+
     "If the tensor has rank 2 and the indices are not specifed, then "+
     "plot the first index along the x-axis and the second index along "+
     "the y-axis. "+
     "A z-axis density legend is print on the RHS if colbar "+
     "is set to 1 before plotting. If z-axis limits are specified, then "+
     "values larger than the upper limit are set equal to the upper limit "+
     "and values smaller than the lower limit are set equal to the lower "+
     "limit before plotting."],
    ["tensor_grid","den-plot","Create a density plot from a tensor object",
     "[index_1 index_2] [kwargs]",
     "Create a density plot from the current tensor. "+
     "If the tensor has rank 2 and the indices are not specifed, then "+
     "plot the first index along the x-axis and the second index along "+
     "the y-axis. "+
     "A z-axis density legend is print on the RHS if colbar "+
     "is set to 1 before plotting. If z-axis limits are specified, then "+
     "values larger than the upper limit are set equal to the upper limit "+
     "and values smaller than the lower limit are set equal to the lower "+
     "limit before plotting."],
    ["tensor_grid","yt-add-vol",
     "Add a tensor_grid object as a yt volume source",
     "","Long desc."]
]
"""
This is a list of 5-element entries:
1: object type
2: command name
3: short description
4: argument list
5: full help text
"""

param_list=[
    ["colbar","If true, den-plot adds a color legend (default False)."],
    ["fig_dict",("Dictionary for figure properties. The default value is "+
                 "blank and implies ('fig_size_x=6.0, fig_size_y=6.0, "+
                 "ticks_in=False, "+
                 "rt_ticks=False, left_margin=0.14, right_margin=0.04, "+
                 "bottom_margin=0.12, top_margin=0.04, fontsize=16') ."+
                 "The x and y sizes of the figure object are in "+
                 "fig_size_x and fig_size_y. The value ticks_in refers "+
                 "to whether or not the ticks are inside or outside the "+
                 "plot. The value of rt_ticks refers to whether or not "+
                 "tick marks are plotted on the right and top sides of "+
                 "the plot. The font size parameter is multiplied by 0.8 "+
                 "and then used for the axis labels.")],
    ["font","Font scaling for text objects (default 16)."],
    ["logx","If true, use a logarithmic x-axis (default False)."],
    ["logy","If true, use a logarithmic y-axis (default False)."],
    ["logz","If true, use a logarithmic z-axis (default False)."],
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
    ["yt_axis","If true, plot a 3D axis."],
    ["yt_axis_color","Color for the 3D axis."],
    ["yt_axis_labels_flat",
     "If true, force the axis labels to be parallel to the camera."],
    ["yt_focus","The camera focus (default [0.5,0.5,0.5])."],
    ["yt_position","The camera position."],
    ["yt_path","The animation path."],
    ["yt_resolution","The rendering resolution (default (512,512))."]
]
"""
List of yt parameters for o2sclpy

A list of 2-element entries, name and description
"""

