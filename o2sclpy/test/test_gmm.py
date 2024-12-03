#  -------------------------------------------------------------------
#  
#  Copyright (C) 2023-2025, Andrew W. Steiner
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
    """
    Test the gmm_sklearn class
    """

    print('──────────────────────────────────'
          '─────────────────────────────────')
    print('Testing gmm_sklearn\n')
    
    # Create test data, a bimodal distribution with two clear peaks
    N=100
    x=numpy.zeros((N,2))
    for i in range(0,100):
        if i%2==0:
            x[i,0]=0.5+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.5+0.2*numpy.cos(i*1.0e6)
        else:
            x[i,0]=0.1+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.1+0.2*numpy.cos(i*1.0e6)

    # Perform the initial fit
    gs=o2sclpy.gmm_sklearn()
    gs.set_data_str(x,'verbose=1,n_components=2')
    print(' ')

    # Test components()
    print('components():')
    print(gs.components([0.7,0.7]))
    print(gs.components([0.0,0.0]))
    print(gs.components([[0.7,0.7],
                         [0.0,0.0]]))
    print(' ')

    # Test predict()
    print('predict():')
    print(gs.predict([0.5,0.5]))
    print(gs.predict([0.2,0.2]))
    print(gs.predict([[0.2,0.2],
                      [0.1,0.1]]))
    print(' ')
    
    # Test log_pdf()
    print('log_pdf():')
    print(gs.log_pdf([0.5,0.5]))
    print(gs.log_pdf([0.2,0.2]))
    print(gs.log_pdf([[0.2,0.2],
                      [0.1,0.1]]))
    print(' ')

    # Test score_samples()
    print('score_samples():')
    print(gs.score_samples([0.5,0.5]))
    print(gs.score_samples([0.2,0.2]))
    print(gs.score_samples([[0.2,0.2],
                            [0.1,0.1]]))
    print(' ')

    # Test sample()
    print('sample():')
    print(gs.sample())
    print(gs.sample(n_samples=3))
    print(' ')

    print('Internal data:')
    print('weights:',gs.gm.weights_)
    print('means:',gs.gm.means_)
    print('covariances:',gs.gm.covariances_)
    print('precisions:',gs.gm.precisions_)
    print(' ')

    return

def test_bgmm():

    print('──────────────────────────────────'
          '─────────────────────────────────')
    print('Testing bgmm_sklearn\n')

    # Create test data, a bimodal distribution with two clear peaks
    N=100
    x=numpy.zeros((N,2))
    for i in range(0,100):
        if i%2==0:
            x[i,0]=0.5+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.5+0.2*numpy.cos(i*1.0e6)
        else:
            x[i,0]=0.1+0.2*numpy.sin(i*1.0e6)
            x[i,1]=0.1+0.2*numpy.cos(i*1.0e6)

    # Perform the initial fit
    gs=o2sclpy.bgmm_sklearn()
    gs.set_data_str(x,'verbose=1,n_components=2')
    print(' ')
    
    # Test predict()
    print('predict():')
    print(gs.predict([0.5,0.5]))
    print(gs.predict([0.2,0.2]))
    print(gs.predict([[0.2,0.2],
                      [0.1,0.1]]))
    print(' ')
    
    # Test log_pdf()
    print('log_pdf():')
    print(gs.log_pdf([0.5,0.5]))
    print(gs.log_pdf([0.2,0.2]))
    print(gs.log_pdf([[0.2,0.2],
                      [0.1,0.1]]))
    print(' ')

    # Test score_samples()
    print('score_samples():')
    print(gs.score_samples([0.5,0.5]))
    print(gs.score_samples([0.2,0.2]))
    print(gs.score_samples([[0.2,0.2],
                            [0.1,0.1]]))
    print(' ')

    # Test sample()
    print('sample():')
    print(gs.sample())
    print(gs.sample(n_samples=3))
    print(' ')

    print('Internal data:')
    print('weights:',gs.bgm.weights_)
    print('means:',gs.bgm.means_)
    print('covariances:',gs.bgm.covariances_)
    print('precisions:',gs.bgm.precisions_)
    print(' ')

    return

if __name__ == '__main__':
    test_gmm()
    test_bgmm()
    print('All tests passed.')
