#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2024, Satyajit Roy and Andrew W. Steiner
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

import o2sclpy
import numpy

def test_all():
    x = numpy.array([[0.0,0.0,5.67],
                     [1.0,1.19,8.0],
                     [5.0,7.3,0.0],
                     [3.0,5.0,4.2],
                     [6.9,9.0,1.0]])

    # Note that classifiers will complain if the outputs are not integers
    y = numpy.array([[-840],[-600],[-840],[10],[45]])
    
    if True:
        im=o2sclpy.classify_sklearn_dtc()
        im.set_data(x,y,verbose=2,random_state=0)
        exact=y[0]
        interp=im.eval(x[0])
        print('exact,interp 1:', exact,interp)
        assert numpy.allclose(exact,interp,rtol=1.0)
        
        im.save('test_classify.o2','dtc')
        
        im4=o2sclpy.classify_sklearn_dtc()
        im4.load('test_classify.o2','dtc')
        interp=im4.eval(x[0])
        print('exact,interp 4:', exact,interp)
        
    if True:
        im2=o2sclpy.classify_sklearn_mlpc()
        im2.set_data_str(x,y,"verbose=2,solver=lbfgs,"+
                         "random_state=1,hlayers=[100,100]")
        exact=y[1]
        interp=im2.eval(x[1])
        print('exact,interp 2:', exact,interp)
        assert numpy.allclose(exact,interp,rtol=1.0)
        
        im2.save('test_classify.o2','mlpc')

        im5=o2sclpy.classify_sklearn_mlpc()
        im5.load('test_classify.o2','mlpc')
        interp=im5.eval(x[1])
        print('exact,interp 5:', exact,interp)
        
    if True:
        im3=o2sclpy.classify_sklearn_gnb()
        im3.set_data(x,y,verbose=0)
        exact=y[2]
        interp=im3.eval(x[2])
        print('exact,interp 3:', exact,interp)
        assert numpy.allclose(exact,interp,rtol=1.0)
        
        im3.save('test_classify.o2','gnb')
        
        im6=o2sclpy.classify_sklearn_gnb()
        im6.load('test_classify.o2','gnb')
        interp=im6.eval(x[1])
        print('exact,interp 6:', exact,interp)
        
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
