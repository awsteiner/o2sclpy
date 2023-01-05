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

yt_param_list=[
    ["yt_filter","Filter for yt-generated images (default '')"],
    ["yt_focus","The camera focus (default is the center of the volume)."],
    ["yt_path","The animation path (typically set using 'yt-path')."],
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

o2graph_help_topics=["markers","markers-plot"]

