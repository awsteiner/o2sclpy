#  -------------------------------------------------------------------
#  
#  Copyright (C) 2022-2024, Mahamudul Hasan Anik, Satyajit Roy, and
#  Andrew W. Steiner
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
    x = numpy.array([[0,0,5.67],[1,1.19,8],[5,7.3,0],[3,5,4.2],[6.9,9,1]])
    # Note that classifiers will complain if the outputs have
    # decimals, meaning they are continuous. This is a problem 
    # with log_wgts and we have to process them differently.
    y = numpy.array([[-840],[-600],[-840],[10],[45]])
    # For float y the user can choose to use tricks like 
    # y_in*100->ftoint->train->predict->y_out/100->output
    
    if True:
        im=o2sclpy.classify_sklearn_dtc()
        im.set_data(x,y,verbose=0,random_state=0)
        exact=y[0]
        interp=im.eval(x[0])
        print('exact,interp 1:', exact,interp)
        assert numpy.allclose(exact,interp,rtol=1.0)
        
    if True:
        im2=o2sclpy.classify_sklearn_mlpc()
        im2.set_data(x,y,verbose=0,solver='lbfgs',random_state=1)
        exact=y[1]
        interp=im2.eval(x[1])
        print('exact,interp 2:', exact,interp)
        assert numpy.allclose(exact,interp,rtol=1.0)
        
    if True:
        im3=o2sclpy.classify_sklearn_gnb()
        im3.set_data(x,y,verbose=0)
        exact=y[2]
        interp=im3.eval(x[2])
        print('exact,interp 2:', exact,interp)
        assert numpy.allclose(exact,interp,rtol=1.0)
        
if __name__ == '__main__':
    test_all()
    print('All tests passed.')