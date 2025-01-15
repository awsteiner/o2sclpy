#  ───────────────────────────────────────────────────────────────────
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
#  ───────────────────────────────────────────────────────────────────
#
import o2sclpy
import numpy
import random
import sys

plots=True
if 'pytest' in sys.modules:
    plots=False

def test_all():

    N=2000
    x=numpy.zeros((N,2))
    for i in range(0,N):
        if i%2==0:
            x[i,0]=0.7+0.1*random.random()
            x[i,1]=0.5+0.1*random.random()
        else:
            x[i,0]=-0.7+0.1*random.random()
            x[i,1]=0.2+0.1*random.random()

    if plots:
        pb=o2sclpy.plot_base()
        pb.xlimits(-1,1)
        pb.ylimits(0,1)
        pb.scatter([x[:,0],x[:,1]])
        pb.show()

    nsf=o2sclpy.nflows_nsf()
    nsf.set_data_str(x,'max_iter=200,verbose=2,outformat=list')

    print('Sampling')
    out=[]
    for i in range(0,300):
        out.append(nsf.sample(1))

    if plots:
        pb=o2sclpy.plot_base()
        pb.xlimits(-1,1)
        pb.ylimits(0,1)
        pb.scatter([[out[i][0] for i in range(0,100)],
                    [out[i][1] for i in range(0,100)]])
        pb.show()

    xgrid=[]
    ygrid=[]
    for i in range(0,21):
        xgrid.append(float(i)/10.0-1.0)
    for j in range(0,21):
        ygrid.append(float(j)/20.0)

    nx=len(xgrid)
    ny=len(ygrid)
    ymat=numpy.zeros((nx,ny))
    for i in range(0,nx):
        for j in range(0,ny):
            x=[xgrid[i],ygrid[j]]
            y=nsf.log_pdf(x)
            ymat[i,j]=numpy.exp(y)

    print('Plotting density')
    if plots:
        pb=o2sclpy.plot_base()
        pb.colbar=True
        pb.xlimits(xgrid[0],xgrid[-1])
        pb.ylimits(ygrid[0],ygrid[-1])
        pb.den_plot([xgrid,ygrid,ymat])
        pb.show()
            
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
