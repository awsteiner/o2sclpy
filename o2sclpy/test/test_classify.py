#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2024-2025, Satyajit Roy and Andrew W. Steiner
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
    
    x=numpy.array([[0.0,0.0,5.67],
                   [1.0,1.19,8.0],
                   [5.0,7.3,0.0],
                   [3.0,5.0,4.2],
                   [6.9,9.0,1.0]])

    # Note that classifiers will complain if the outputs are not integers
    y=numpy.array([[-840],
                   [-600],
                   [-840],
                   [10],
                   [45]])

    # For testing eval_list()
    xa=numpy.array([x[0],x[1],x[2]])
    ya=numpy.array([y[0][0],y[1][0],y[2][0]])
    
    if True:
        print('classify_sklearn_dtc')
        print('──────────────────────────────────────────────────────')
        print(' ')
        
        im=o2sclpy.classify_sklearn_dtc()
        im.set_data(x,y,verbose=2,random_state=0)
        im.verbose=0
        
        exact=y[0]
        result=im.eval(x[0])
        print('exact,result 1:', exact,result)
        assert numpy.allclose(exact,result,rtol=1.0e-4)
        
        im.save('test_classify.o2','dtc')
        
        im4=o2sclpy.classify_sklearn_dtc()
        im4.load('test_classify.o2','dtc')
        result=im4.eval(x[0])
        print('exact,result 4:', exact,result)
        assert numpy.allclose(exact,result,rtol=1.0e-4)

        ya_result=im4.eval_list(xa)
        print('exact,result 7:', ya,ya_result)
        assert numpy.allclose(ya,ya_result,rtol=1.0e-4)
        print(' ')
        
    if True:
        print('classify_sklearn_mlpc')
        print('──────────────────────────────────────────────────────')
        print(' ')
        
        im2=o2sclpy.classify_sklearn_mlpc()
        im2.set_data_str(x,y,"verbose=2,solver=lbfgs,"+
                         "random_state=1,hlayers=[100,100]")
        
        exact=y[1]
        result=im2.eval(x[1])
        print('exact,result 2:', exact,result)
        assert numpy.allclose(exact,result,rtol=1.0)
        
        im2.save('test_classify.o2','mlpc')

        im5=o2sclpy.classify_sklearn_mlpc()
        im5.load('test_classify.o2','mlpc')
        result=im5.eval(x[1])
        print('exact,result 5:', exact,result)
        assert numpy.allclose(exact,result,rtol=1.0e-4)

        ya_result=im5.eval_list(xa)
        print('exact,result 8:', ya,ya_result)
        assert numpy.allclose(ya,ya_result,rtol=1.0e-4)
        print(' ')
        
    if True:
        print('classify_sklearn_gnb')
        print('──────────────────────────────────────────────────────')
        print(' ')
        
        im3=o2sclpy.classify_sklearn_gnb()
        im3.set_data(x,y,verbose=2)
        exact=y[2]
        result=im3.eval(x[2])
        print('exact,result 3:', exact,result)
        assert numpy.allclose(exact,result,rtol=1.0)
        
        im3.save('test_classify.o2','gnb')
        
        im6=o2sclpy.classify_sklearn_gnb()
        im6.load('test_classify.o2','gnb')
        result=im6.eval(x[1])
        print('exact,result 6:', exact,result)
        assert numpy.allclose(exact,result,rtol=1.0)

        ya_result=im6.eval_list(xa)
        print('exact,result 9:', ya,ya_result)
        assert numpy.allclose(ya,ya_result,rtol=1.0e-4)
        print(' ')
        
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
