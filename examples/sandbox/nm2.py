# # Multi-dimensional interpolation example for O$_2$sclpy

# See the O$_2$sclpy documentation at https://awsteiner.org/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import random
import numpy
import sys
from IPython.utils import io

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Create the data set:

# Instantiate and load the Atomic Mass Evaluation
ame=o2sclpy.nucmass_ame()
o2sclpy.ame_load(ame,'20',False)

# Print out the number of entries
print('Number of isotopes in the AME list:',ame.get_nentries())

nuc=o2sclpy.nucleus()
tab=o2sclpy.table()
tab.line_of_names('Z N mex')
for Z in range(8,200):
    for N in range(8,250):
        if ame.is_included(Z,N):
            ame.get_nucleus(Z,N,nuc)
            line=[Z,N,nuc.mex]
            tab.line_of_data(line)
            
N=tab.get_nlines()
x2=numpy.zeros((N,2))
y2=numpy.zeros((N,1))
for i in range(0,N):
    x2[i,0]=tab["Z"][i]
    x2[i,1]=tab["N"][i]
    y2[i,0]=tab["mex"][i]
print('Number of isotopes to fit:',N)

# Create the neural network interpolation object

for k in range(0,27):

    if k%3==0:
        trans='none'
    elif k%3==1:
        trans='moto'
    else:
        trans='quant'
    if (k//3)%3==0:
        act='relu'
    elif (k//3)%3==1:
        act='sigmoid'
    else:
        act='tanh'
    if (k//9)%3==0:
        M=1
    elif (k//9)%3==1:
        M=2
    else:
        M=4

    avgs=0
    
    if True:
        
        for j in range(0,5):
        
            im2=o2sclpy.interpm_tf_dnn()
            
            # Train the neural network
            
            #with io.capture_output() as cap:
            im2.set_data(x2,y2,verbose=0,epochs=800,
                         transform=trans,test_size=0.1,
                         activations=[act,act,act,act],
                         hlayers=[240*M,120*M,60*M,40*M])
            
            #v=numpy.array([x2[100,0],x2[100,1]])
            #print('%d %d %7.6e %7.6e' % (v[0],v[1],im2.eval(v)[0],y2[100,0]))
            
            with io.capture_output() as cap:
                sum=0
                for i in range(0,N):
                    v=numpy.array([x2[i,0],x2[i,1]])
                    sum+=numpy.abs(im2.eval(v)[0]-y2[i,0])
            avg=sum/N*197.33
            print('%d avg %7.6e MeV' % (j,avg))
            avgs=avgs+avg
            
        print(avgs/5.0)

    print(k,trans,act,M,avgs/5.0)
    
quit()
    


