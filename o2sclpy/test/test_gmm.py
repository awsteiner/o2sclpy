#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023, Andrew W. Steiner
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
import o2sclpy
import numpy

def test_gmm():

    N=100
    x=numpy.zeros((N,2))
    for i in range(0,100):
        if i%2==0:
            x[i,0]=0.5+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.5+0.2*numpy.cos(i*1.0e6)
        else:
            x[i,0]=0.1+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.1+0.2*numpy.cos(i*1.0e6)
    
    gs=o2sclpy.gmm_sklearn()
    gs.set_data_str(x,'verbose=2,n_components=2')
    print(gs.components([0.7,0.7]))
    print(gs.components([0.0,0.0]))
    print('w',gs.gm.weights_)
    print('m',gs.gm.means_)
    print('c',gs.gm.covariances_)
    print('p',gs.gm.precisions_)
    print(gs.get_data())

    return

def test_bgmm():

    N=100
    x=numpy.zeros((N,2))
    for i in range(0,100):
        if i%2==0:
            x[i,0]=0.5+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.5+0.2*numpy.cos(i*1.0e6)
        else:
            x[i,0]=0.1+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.1+0.2*numpy.cos(i*1.0e6)
    
    gs=o2sclpy.bgmm_sklearn()
    gs.set_data_str(x,'verbose=2,n_components=2')
    print(gs.components([0.7,0.7]))
    print(gs.components([0.0,0.0]))
    print('w',gs.bgm.weights_)
    print('m',gs.bgm.means_)
    print('c',gs.bgm.covariances_)
    print('p',gs.bgm.precisions_)
    print(gs.get_data())

    return

if __name__ == '__main__':
    test_gmm()
    test_bgmm()
    print('All tests passed.')
