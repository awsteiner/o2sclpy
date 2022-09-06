from o2sclpy.utils import terminal_py

ter=terminal_py()

version='0.928a1'

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

# When entries are blank, it's because they are taken from the
# python docstring in o2graph_plotter.help_func()
base_list=[
    ["addcbar","","",""],
    ["arrow","","",""],
    ["backend","","",""],
    ["cmap","","",""],
    ["cmap2","","",""],
    ["canvas","","",""],
    ["clf","","",""],
    ["ellipse","","",""],
    ["eval","","",""],
    ["exec","","",""],
    ["image","","",""],
    ["inset","","",""],
    ["line","","",""],
    ["modax","","",""],
    ["o2scl-addl-libs","","",""],
    ["o2scl-cpp-lib","","",""],
    ["o2scl-lib-dir","","",""],
    ["plotv","","",""],
    ["point","","",""],
    ["python","","",""],
    ["rect","","",""],
    ["save","","",""],
    ["selax","","",""],
    ["show","","",""],
    ["subadj","","",""],
    ["subplots","",""],
    ["text","","",""],
    ["textbox","","",""],
    ["ttext","","",""],
    ["xlimits","","",""],
    ["xtitle","","",""],
    ["ylimits","","",""],
    ["ytitle","","",""],
    ["yt-ann","Annotate a yt rendering (experimental).","",
     "The 'yt-ann' command adds a list of o2graph commands that can "+
     "be used to annotate a yt rendering. Annotations are normal "+
     "o2graph 2D plotting commands built upon a coordinate system with "+
     "(0,0) as the lower-left corner of the image and (1,1) as the "+
     "upper-right corner. "+
     "yt-ann command arguments may include dashes but must end with the "+
     "word 'end'.\n\n"+
     "Examples are:\n  -yt-ann -text 0.1 0.95 \"Ann. example\" "+
     "color=w,ha=left end"],
    ["yt-xtitle","Add a x title to a yt render.","",""],
    ["yt-ytitle","Add a y title to a yt render.","",""],
    ["yt-ztitle","Add a z title to a yt render.","",""],
    ["yt-arrow","Draw an arrow in the yt volume.",
     "<[x1,y1,z1]> <[x2,y2,z2]> [kwargs]",
     "Draw an arrow from the tail at (x1,y1,z1) to the head at "+
     "(x2,y2,z2). Relevant kwargs are "+
     "color=[r,g,b,a] where r,g,b,a are all from 0 to 1 and "+
     "keyname='o2sclpy_line' for the key name in the list yt sources, "+
     "n_lines=40 for the number of lines around the azimuthal angle, "+
     "frac_length=0.05 for the fractional length of the head relative "+
     "to the full arrow length, radius=0.0125 for the radius of the "+
     "largest part of the arrow head, coords=user to use either the "+
     "internal or user-based coordinate system. "+
     "If the x, y, and z limits have not yet been set, then the "+
     "lower limit for the x coordinate will be set by the minimum "+
     "of x1 and x2, and the upper limit for the x coordinate will be "+
     "set to the maximum of x1 and x2. Similarly for y and z. If "+
     "a yt volume has not yet been constructed, then the default "+
     "volume will be created."],
    ["yt-axis","Add an axis to the yt volume.",
     "[x] [y] [z] [kwargs]",
     "Plot an axis using a point at the origin and then "+
     "three arrows pointing to "+
     "[0,0,xval], [0,yval,0], and [0,0,zval]. "+
     "Relevant kwargs are color=[1,1,1,0.5], and coords='user' "+
     "coords=user to use the "+
     "user-based coordinate system or 'internal' to use the internal "+
     "coordinates"],
    ["yt-box","Draw a box in the yt volume.",
     "<[x1,y1,z1]> <[x2,y2,z2]> [kwargs]",
     "Draw a box with diagonally opposed corners "+
     "(x1,y1,z1) to (x2,y2,z2). Relevant kwargs are "+
     "color=[r,g,b,a] where r,g,b,a are all from 0 to 1, "+
     "coords=user to use the "+
     "user-based coordinate system or 'internal' to use the internal "+
     "coordinates, and "+
     "keyname='o2sclpy_line' for the key name in the list yt sources. "+
     "If the x, y, and z limits have not yet been set, then the "+
     "lower limit for the x coordinate will be set by the minimum "+
     "of x1 and x2, and the upper limit for the x coordinate will be "+
     "set to the maximum of x1 and x2. Similarly for y and z. If "+
     "a yt volume has not yet been constructed, then the default "+
     "volume will be created."],
    ["yt-line","Draw a line in the yt volume.",
     "<x1> <y1> <z1> <x2> <y2> <z2> [kwargs]",
     "Draw a line from (x1,y1,z1) to (x2,y2,z2). Relevant kwargs are "+
     "color=[r,g,b,a] where r,g,b,a are all from 0 to 1, "+
     "coords=user to use the "+
     "user-based coordinate system or 'internal' to use the internal "+
     "coordinates. and "+
     "keyname='o2sclpy_line' for the key name in the list yt sources. "+
     "If the x, y, and z limits have not yet been set, then the "+
     "lower limit for the x coordinate will be set by the minimum "+
     "of x1 and x2, and the upper limit for the x coordinate will be "+
     "set to the maximum of x1 and x2. Similarly for y and z. If "+
     "a yt volume has not yet been constructed, then the default "+
     "volume will be created."],
    ["yt-path","Add a path to the yt animation.",
     "<type> <number of frames> <other parameters>",
     "This adds a path to the yt animation. To rotate the camera around "+
     "the z-axis, use 'yaw' <n_frames> "+
     "<angle>, where angle is a fraction of a full rotation. To zoom "+
     "the camera, use 'zoom' "+
     "<n_frames> <factor> ,where factor is the total zoom factor to "+
     "apply over all n_frames. To move the camera along a line, "+
     "use 'move' <n_frames> "+
     "<[dest_x,dest_y,dest_z]> <'internal' or 'user'>, where the third "+
     "argument is the destination in either the internal or user-specified "+
     "coordinate system. To turn the camera without moving it, use "+
     "'turn' <n_frames> <[foc_x,foc_y,foc_z]> <'internal' or 'user'>. "+
     "Executing 'yt-path reset' resets the yt "+
     "animation path to an empty list (for no animation)."],
    ["yt-render","","",""],
    ["yt-source-list","List all current yt sources.","",
     "For each source output the index, keyname, and source type."],
    ["yt-text","Add text to the yt volume.",
     "<x> <y> <z> <text>","reorient=False"],
    ["yt-tf","Edit the yt transfer function.","<mode> <args>",
     "To create a new transfer function, use 'new' for <mode> "+
     "and the remaining <args> are <min> <max> [nbins] "+
     ".To add a Gaussian, use 'gauss' for <mode> "+
     "and <args> are <loc> <width> <red> <green> <blue>, and <alpha>. "+
     "To add a step function, use 'step' "+
     "<low> <high> <red> <green> <blue>, and <alpha> "+
     "To plot the transfer function, use 'plot' "+
     "<filename>."],
    ["zlimits","Set the z-axis limits.","<low> <high>",
     "Set 'zlo' and 'zhi' to the specified limits, "+
     "and set 'zset' to true. The z-axis limits are principally used "+
     "for yt volume visualizations. If <low> and <high> are identical "+
     "then "+ter.red_fg()+
     ter.bold()+"zset"+ter.default_fgbg()+" is set to false."]
]
"""
This is a list of 4-element entries:
1: command name
2: short description
3: argument list
4: full help text
"""

acol_types=["char","double","double[]","hist","hist_2d","int",
            "int[]","prob_dens_mdim_amr","prob_dens_mdim_gaussian",
            "size_t","size_t[]","string",
            "string[]","table","table3d","tensor","tensor<int>",
            "tensor<size_t>","tensor_grid",
            "uniform_grid<double>","vec_vec_double",
            "vec_vec_string","vector<contour_line>"]

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
     "<x>. Some useful kwargs are color (c), dashes, "+
     "linestyle (ls), linewidth (lw), marker, markeredgecolor (mec), "+
     "markeredgewidth (mew), markerfacecolor (mfc), markerfacecoloralt "+
     "(mfcalt), markersize (ms). For example: \"o2graph -create x 0 10 0.2 "+
     "-function sin(x) y -plot x y lw=0,marker='+' -show\". "+
     "This command uses the matplotlib plot() function, see "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html "+
     "for information and keyword arguments. This command does not yet "+
     "support the matplotlib format parameter."],
    ["table","plot-color",
     "Plot three columns from the table.",
     "<x> <y> <z> <cmap> [kwargs]",
     "If the current object is a table, then plot "+
     "column <y> versus column "+
     "<x> using line segments colored by column <z> which are rescaled "+
     "to colormap <cmap>. "+
     "Some useful kwargs are color (c), dashes, "+
     "linestyle (ls), linewidth (lw), marker, markeredgecolor (mec), "+
     "markeredgewidth (mew), markerfacecolor (mfc), markerfacecoloralt "+
     "(mfcalt), markersize (ms). For example: o2graph -create x 0 10 0.2 "+
     "-function sin(x) y -function cos(x) z -plot-color x y z "+
     "Purples lw=0,marker='+' -show"],
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
     "direction, just use 0 for <xerr> or <yerr>, respectively. Some "+
     "useful kwargs "+
     "for the errorbar command are:\n\n"+
     "keyword    description                      default value\n"+
     "---------------------------------------------------------\n"+
     "ecolor     error bar color                   None\n"+
     "elinewidth error bar line width              None\n"+
     "capsize    cap size in points                None\n"+
     "barsabove  plot error bars on top of points  False\n"+
     "lolims     y value is lower limit            False\n"+
     "uplims     y value is upper limit            False\n"+
     "xlolims    x value is lower limit            False\n"+
     "xuplims    x value is upper limit            False\n"+
     "errorevery draw error bars on subset of data 1\n"+
     "capthick   thickness of error bar cap        None\n\n"+
     "For error points with no lines use, e.g. lw=0,elinewidth=1 . "+
     "See also 'error-point' for plotting a single point with errorbars."],
    ["table","yt-scatter","Add scattered points to a yt scene",
     ("<x column> <y column> <z column> [size column] [red column] "+
      "[green column] [blue column] [alpha column]"),
     ("This adds a series of points to a yt scene. If a volume "+
      "has not yet been added, then a default volume is added. "+
      "If the x, y-, or z-axis limits have not yet been set, then "+
      "they are set by the limits of the data. If the size column "+
      "is unspecified, 'none', or 'None', then the default value of 3 is "+
      "used. If the color columns are unspecified, 'none' or "+
      "'None', then [1,1,1] is used, and finally the default "+
      "for the alpha column is 0.5. If any of the values for the color "+
      "columns are less than zero or greater than 1, then that color "+
      "column is rescaled to [0,1].")],
    ["table","yt-vertex-list",
     "Draw a line from a series of vertices in a table.",
     "<x column> <y column> <z column> [kwargs]",
     "Create a series of yt LineSource objects in a visualization "+
     "using the three specified columns as vertices. One line segment "+
     "will be drawn from the values in the first row to the values in "+
     "the second row, one line segment from the second row to the "+
     "third row, and so on"],
    ["table","plot1","Plot the specified column.","<y> [kwargs]",
     "Plot column <y> versus row number. Some "+
     "useful kwargs are color (c), "+
     "dashes, linestyle (ls), linewidth (lw), marker, markeredgecolor (mec), "+
     "markeredgewidth (mew), markerfacecolor (mfc), markerfacecoloralt "+
     "(mfcalt), markersize (ms). For example: \"o2graph -create x 0 10 0.2 "+
     "-function sin(x) y -plot1 y ls='--',marker='o' -show\". "+
     "This command uses the matplotlib plot() function, see "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html "+
     "for information and keyword arguments. This command does not yet "+
     "support the matplotlib format parameter."],
    ["table","hist-plot","Create a histogram plot from column in a table.",
     "<col> [kwargs]","For a table, create a histogram plot from the "+
     "specified column. This command uses matplotlib to construct the "+
     "histogram rather than using O2scl to create a histogram object. "+
     "This command uses the matplotlib hist() function, see "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html "+
     "for information and keyword arguments."],
    ["table","hist2d-plot",
     "Create a 2-D histogram plot from two columns in a table.",
     "<col x> <col y>","For a table, create a 2D histogram plot from "+
     "the specified columns. This command uses matplotlib to construct the "+
     "histogram rather than using O2scl to create a hist object."],
    ["table3d","den-plot","Create a density plot from a table3d object.",
     "<slice> [kwargs]",
     "Creates a density plot from the specified "+
     "slice. A z-axis density legend "+
     "is print on the RHS if colbar is set to True before plotting. "+
     "If z-axis limits are specified, then values larger than the upper "+
     "limit "+
     "are set equal to the upper limit and values smaller than the lower "+
     "limit are set equal to the lower limit before plotting. The x- "+
     "and y-axis limits (xlo,xhi,ylo,yhi) are ignored. The python "+
     "function imshow() is used, unless 'pcm=True' is specified, in "+
     "which case the pcolormesh() function is used instead. When "+
     "'pcm=False', logarithmic scales are handled by "+
     "taking the base 10 log of the x- or y-grids "+
     "specified in the table3d object before plotting. When 'pcm=True', "
     "logarithmic axes can be handled automatically. The imshow() "+
     "function presumes a uniform linear or logarithmic x- and y-axis "+
     "grid, and the den-plot function will output a warning if this "+
     "is not the case. The pcolormesh() function can handle arbitrary "+
     "x and y-axis grids. If ``logz`` is set to true, then the base 10 "+
     "logarithm is taken of the data before the density plot is "+
     "constructed. Some useful kwargs are cmap, interpolation "+
     "(for imshow), alpha, vmin, and vmax. See more information at "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html "+
     "and "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pcolormesh.html "+
     "for more information and keyword arguments."],
    ["table3d","den-plot-rgb","Create a (R,G,B) density plot from a table3d.",
     "<slice_r> <slice_g> <slice_b>","Create a density plot from "+
     "the three specified slices. This command uses imshow(). "+
     "To directly create a .png file with no axes, use make-png instead."],
    ["table3d","yt-mesh","","",""],
    ["table3d","make-png","Create a png file from a table3d object.",
     "<slice_r> <slice_g> <slice_b> <filename>",
     "Create a .png file from "+
     "the three specified table3d slices. This command requires pillow. "+
     "To create a density-plot with axes instead, use den-plot-rgb."],
    ["hist","hist-plot",
     "Create a histogram plot from the current histogram.",
     "[kwargs]","Create a histogram plot from the "+
     "current histogram. "+
     "This command uses the matplotlib hist() function, see "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html "+
     "for information and keyword arguments."],
    ["hist","plot","Plot the histogram.","[kwargs]",
     "Plot the histogram weights as a function "+
     "of the bin representative values. "+
     "Some useful kwargs (which apply for all three object types) are "+
     "color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms). For example: \"o2graph "+
     "-create x 0 10 0.2 -function sin(x) y "+
     "-plot x y lw=0,marker='+' -show\". "+
     "This command uses the matplotlib plot() function, see "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html "+
     "for information and keyword arguments. This command does not yet "+
     "support the matplotlib format parameter."],
    ["double[]","plot1","Plot the array.","[kwargs]",
     "Plot the array. Some useful kwargs "+
     "are color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms). "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html "+
     "for information and keyword arguments. This command does not yet "+
     "support the matplotlib format parameter."],
    ["int[]","plot1","Plot the array.","[kwargs]",
     "Plot the array. Some useful kwargs "+
     "are color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms). "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html "+
     "for information and keyword arguments. This command does not yet "+
     "support the matplotlib format parameter."],
    ["size_t[]","plot1","Plot the array.","[kwargs]",
     "Plot the array. Some useful kwargs "+
     "are color (c), dashes, linestyle (ls), linewidth (lw), marker, "+
     "markeredgecolor (mec), markeredgewidth (mew), markerfacecolor (mfc), "+
     "markerfacecoloralt (mfcalt), markersize (ms). "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html "+
     "for information and keyword arguments. This command does not yet "+
     "support the matplotlib format parameter."],
    ["vector<contour_line>","plot","Plot the contour lines.","[kwargs]",
     "Plot the set of contour lines. Some "+
     "useful kwargs (which apply for all three "+
     "object types) are color (c), dashes, linestyle (ls), linewidth (lw), "+
     "marker, markeredgecolor (mec), markeredgewidth (mew), markerfacecolor "+
     "(mfc), markerfacecoloralt (mfcalt), markersize (ms). For example: "+
     "\"o2graph -create x 0 10 0.2 -function sin(x) y -plot x y "+
     "lw=0,marker='+' -show\". "+
     "This command uses the matplotlib plot() function, see "+
     "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html "+
     "for information and keyword arguments. This command does not yet "+
     "support the matplotlib format parameter."],
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
     "[kwargs]","This adds the volumetric data specified in the "+
     "tensor_grid object as a yt volume source. The transfer "+
     "function previously specified by 'yt-tf' is used, or if "+
     "unspecified, then yt's transfer_function_helper is used "+
     "to create a 3 layer default transfer function."],
    ["tensor_grid","den-plot-anim",
     "Create an animated density plot from a tensor_grid object. ",
     "<x index> <y index> <z index [+'r']> <mp4 filename>",
     "(Requires ffmpeg.)"],
    ["prob_dens_mdim_gaussian","max-ell",
     "Create an ellipse around the peak.",
     "<frac> [kwargs]",""]
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
    ["yt_filter","Filter for yt-generated images (default '')"],
    ["yt_focus","The camera focus (default is the center of the volume)."],
    ["yt_position","The camera position "+
     "(default is '[1.5,0.6,0.7] internal')."],
    ["yt_north","The camera north vector (default [0.0,0.0,1.0])."],
    ["yt_width","The camera width relative to the domain volume< "+
     "(default [1.5,1.5,1.5])."],
    ["yt_resolution","The rendering resolution (default (512,512))."],
    ["yt_sigma_clip","Sigma clipping parameter (default 4.0)."]
]
"""
List of yt parameters for o2sclpy

A list of 2-element entries, name and description
"""

acol_help_topics=["functions","index-spec","mult-vector-spec","strings-spec",
                  "types","value-spec","vector-spec"]

o2graph_help_topics=["cmaps","cmaps-plot","colors","colors-plot",
                     "colors-near","markers","markers-plot",
                     "xkcd-colors"]

