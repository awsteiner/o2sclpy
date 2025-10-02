#  ───────────────────────────────────────────────────────────────────
#  
#  Copyright (C) 2025, Andrew W. Steiner
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
#
import o2sclpy
import numpy
from sklearn.datasets import load_digits

def test_pca():

    digits=load_digits()['data']
    
    tab=o2sclpy.table()
    nrows=numpy.shape(digits)[0]
    ncols=numpy.shape(digits)[1]
    print('nrows,ncols',nrows,ncols)
    for i in range(0,ncols):
        tab.new_column('c_'+str(i))
    tab.set_nlines(nrows)
    for i in range(0,ncols):
        for j in range(0,nrows):
            tab.set('c_'+str(i),j,digits[j][i])
        
    pca=o2sclpy.dimred_sklearn_pca()
    out_data=pca.run(digits,n_components=4)
    print(numpy.shape(out_data),pca.pca.explained_variance_ratio_)

    pca2=o2sclpy.dimred_sklearn_pca()
    in_cols=['c_'+str(i) for i in range(0,ncols)]
    pca2.run_table(tab,in_cols,n_components=4)
    for i in range(tab.get_ncolumns()):
        print('test_pca(): column',i,tab.get_column_name(i))
    print(pca2.pca.explained_variance_ratio_)

    return

def test_tsne():

    import os
    os.environ["USE_OPENMP"] = "1"

    digits=load_digits()['data']
    
    tab=o2sclpy.table()
    nrows=numpy.shape(digits)[0]
    ncols=numpy.shape(digits)[1]
    print('test_tsne(): nrows,ncols',nrows,ncols)
    for i in range(0,ncols):
        tab.new_column('c_'+str(i))
    tab.set_nlines(nrows)
    for i in range(0,ncols):
        for j in range(0,nrows):
            tab.set('c_'+str(i),j,digits[j][i])
        
    tsne=o2sclpy.dimred_sklearn_tsne()
    out_data=tsne.run(digits,n_components=2,verbose=3)
    print(numpy.shape(out_data))

    tsne2=o2sclpy.dimred_sklearn_tsne()
    in_cols=['c_'+str(i) for i in range(0,ncols)]
    tsne2.run_table(tab,in_cols,n_components=2)
    for i in range(tab.get_ncolumns()):
        print('test_tsne(): column',i,tab.get_column_name(i))

    return

if __name__ == '__main__':
    test_pca()
    test_tsne()
    print('All tests passed.')

