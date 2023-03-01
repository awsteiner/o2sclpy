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

def test_all():

    N=1000
    
    x=numpy.zeros((N,2))
    for i in range(0,N):
        for j in range(0,2):
            x[i,0]=numpy.sin(i)
            x[i,1]=numpy.cos(i)
            
    y=numpy.zeros((N,1))
    for i in range(0,N):
        for j in range(0,1):
            y[i,j]=x[i,0]**3+3.0*(x[i,1]**2)
            if abs(x[i,0]-0.2)<0.17 and abs(x[i,1]-0.1)<0.17:
                print(x[i,0],x[i,1],y[i,0])

    im=o2sclpy.interpm_sklearn_gp()
    im.set_data_str(x,y,'verbose=2')
    print(im.eval([0.2,0.1]),0.2**3+3*(0.1**2))
            
    return

if __name__ == '__main__':
    test_all()
    print('All tests passed.')
