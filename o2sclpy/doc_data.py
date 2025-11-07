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

from o2sclpy.utils import terminal_py
from o2sclpy.link_o2scl import linker

ter=terminal_py()

#print('Linking O₂scl.')
top_linker=linker()
top_linker.link_o2scl()
#print('Done linking O₂scl.')

version='0.932'

cmaps = [('Perceptually uniform sequential', [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Cyclic', ['twilight', 'twilight_shifted', 'hsv']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar'])]
"""
List of cmaps for 'help cmaps'
"""

yt_cmaps=[('Perceptually uniform sequential (yt)',
        ['cmyt.apricity','cmyt.arbre','cmyt.dusk','cmyt.kelp',
         'cmyt.octarine']),
       ('Monochromatic sequential (yt)', 
        ['cmyt.pixel_blue','cmyt.pixel_green','cmyt.pixel_red']),
       ('Miscellaneous (yt)', 
        ['cmyt.algae','cmyt.pastel','cmyt.xray'])]
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

acol_help_topics=["functions","index-spec","mult-vector-spec","strings-spec",
                  "types","value-spec","vector-spec"]

o2graph_help_topics=["markers","markers-plot","fonts"]

