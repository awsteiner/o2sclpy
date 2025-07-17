#  -------------------------------------------------------------------
#  
#  Copyright (C) 2024-2025, Andrew W. Steiner
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
import random
import numpy

def subtest_acor():

    # This dataset has an approximate correlation length
    # of 100
    data=[]
    for i in range(0,10):
        for j in range(0,100):
            data.append(float(i)/20.0+random.random())

    vec=o2sclpy.std_vector()
    vec.from_list(data)

    m=o2sclpy.vector_mean(len(vec),vec)
    print('mean:',m)
    assert numpy.allclose(m,0.72,rtol=4.0e-2)
    s=o2sclpy.vector_stddev(len(vec),vec)
    print('stddev:',s)
    assert numpy.allclose(s,0.33,rtol=0.1)

    assert numpy.allclose(o2sclpy.vector_lagk_autocorr(len(vec),
                                                       vec,100),0.1,
                          rtol=2.0)

    ac=o2sclpy.std_vector()
    o2sclpy.vector_autocorr_vector(len(vec),vec,ac)
    ftom=o2sclpy.std_vector()
    assert numpy.allclose(o2sclpy.vector_autocorr_tau(ac,ftom),
                          100,atol=100)

    ac2=o2sclpy.std_vector()
    o2sclpy.vector_autocorr_vector_fftw(vec,ac2,m,s)
    ftom2=o2sclpy.std_vector()
    assert numpy.allclose(o2sclpy.vector_autocorr_tau(ac2,ftom2),
                          100,atol=100)

    # This doesn't work yet
    #tau=0.0
    #o2sclpy.vector_acor(len(vec),vec,m,s,tau)
    #print(tau)
    
    return

def test_all():
    subtest_acor()
    return
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
