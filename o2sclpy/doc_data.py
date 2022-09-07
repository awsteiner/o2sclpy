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
    ["table","plot","","",""],
    ["table","plot-color","","",""],
    ["table","rplot","","",""],
    ["table","scatter","","",""],
    ["table","errorbar","","",""],
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

