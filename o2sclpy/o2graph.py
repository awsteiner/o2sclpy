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

# For sys.argv
import sys
import os

def o2graph():

    from o2sclpy.link_o2scl import linker

    l=linker()
    backend=l.get_library_settings(sys.argv)
    l.link_o2scl()
    
    if backend!='':
        import matplotlib
        matplotlib.use(backend)
        print('o2graph: Set matplotlib backend to',backend,'.')
        
    import o2sclpy
    gc=o2sclpy.o2graph_plotter()
    gc.parse_argv(sys.argv,l.o2scl,l)

    return

