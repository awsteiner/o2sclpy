# # Multi-dimensional interpolation example for O$_2$sclpy

# 0 avg 1.064573e+00 MeV
#1 avg 1.382027e+00 MeV
#2 avg 9.551093e-01 MeV
#3 avg 1.587466e+00 MeV
#4 avg 9.933744e-01 MeV
#1.1965099779501946
#10 moto relu 2 1.1965099779501946

#0 avg 1.192039e+00 MeV
#1 avg 8.977399e-01 MeV
#2 avg 8.968433e-01 MeV
#3 avg 1.378074e+00 MeV
#4 avg 1.645730e+00 MeV
#1.202085270806319
#19 moto relu 4 1.202085270806319

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

# Instantiate and load the Atomic Mass Evaluation. The third parameter
# is False, to indicate that we include masses which are not solely
# determined by experiment
ame=o2sclpy.nucmass_ame()
o2sclpy.ame_load(ame,'20',False)

# Print out the number of entries
print('Number of isotopes in the AME list:',ame.get_nentries())

dz=o2sclpy.nucmass_dz_fit_33()
dist=o2sclpy.std_vector_nucleus()

o2sclpy.nucdist_set(dist,ame)
print(len(dist))

p=o2sclpy.ublas_vector()
p.resize(33)
p[0]=9.089056134746128e+00
p[1]=6.503243633083565e+00
p[2]=4.508165895514288e+00
p[3]=2.078535386636489e+01
p[4]=1.725739163595326e+00
p[5]=7.535149383516492e+00
p[6]=-4.506924382606631e+00
p[7]=-3.412765813834761e+01
p[8]=-3.585539147281765e-01
p[9]=7.344223304154160e-01
p[10]=-7.511052798991504e-01
p[11]=-3.761406531766877e+00
p[12]=-1.776599459045521e-01
p[13]=-8.995089717699093e-01
p[14]=3.973338204326113e-01
p[15]=1.807250910019584e+00
p[16]=2.413813645058122e-01
p[17]=1.066620521567073e+00
p[18]=8.518733677001322e+00
p[19]=5.373696129291158e+01
p[20]=1.824339588062157e+01
p[21]=7.270593853877729e+01
p[22]=-2.714335458881215e+01
p[23]=-1.284192451766697e+02
p[24]=-5.001066637985519e+00
p[25]=-3.299700362463194e+01
p[26]=-3.794286672329046e+01
p[27]=-5.392723600204433e+01
p[28]=1.559715229007208e+00
p[29]=5.448044100904870e+00
p[30]=7.054620573104972e-01
p[31]=6.182687849301996e+00
p[32]=2.076508980189957e+01

dz.fit_fun(33,p)

nuc=o2sclpy.nucleus()
tab=o2sclpy.table()
tab.line_of_names('Z N mex mex_th diff')
for Z in range(8,200):
    for N in range(8,250):
        line=[Z,N,0,0,0]
        if ame.is_included(Z,N) and dz.is_included(Z,N):
            ame.get_nucleus(Z,N,nuc)
            line[2]=nuc.mex*197.33
            dz.get_nucleus(Z,N,nuc)
            line[3]=nuc.mex*197.33
            line[4]=line[2]-line[3]
            if Z==82 and N==126:
                print(line)
            tab.line_of_data(line)

hf=o2sclpy.hdf_file()
hf.open_or_create('nm2.o2')
o2sclpy.hdf_output_table(hf,tab,b'table')
hf.close()
                
N=tab.get_nlines()
x2=numpy.zeros((N,2))
y2=numpy.zeros((N,1))
for i in range(0,N):
    x2[i,0]=tab["Z"][i]
    x2[i,1]=tab["N"][i]
    y2[i,0]=tab["diff"][i]
print('Number of isotopes to fit:',N)

# Create the neural network interpolation object

#for k in range(0,27):
for k in range(19,20):

    # Different transformations
    if k%3==0:
        trans='none'
    elif k%3==1:
        trans='moto'
    else:
        trans='quant'

    # Different activation functions
    if (k//3)%3==0:
        act='relu'
    elif (k//3)%3==1:
        act='sigmoid'
    else:
        act='tanh'

    # Different network sizes
    if (k//9)%3==0:
        M=1
    elif (k//9)%3==1:
        M=2
    else:
        M=4

    avgs=0
    
    if True:

        # Try each configuration five times, and take the
        # average of the 5 at the end
        #for j in range(0,5):
        for j in range(0,1):
        
            im2=o2sclpy.interpm_tf_dnn()
            
            # Train the neural network
            
            #with io.capture_output() as cap:
            im2.set_data(x2,y2,verbose=1,epochs=800,
                         transform_in=trans,test_size=0.1,
                         activations=[act,act,act,act],
                         hlayers=[240*M,120*M,60*M,40*M])
            
            #v=numpy.array([x2[100,0],x2[100,1]])
            #print('%d %d %7.6e %7.6e' % (v[0],v[1],im2.eval(v)[0],y2[100,0]))
            
            #with io.capture_output() as cap:
            sum=0
            for i in range(0,N):
                v=numpy.array([x2[i,0],x2[i,1]])
                sum+=numpy.abs(im2.eval(v)[0]-y2[i,0])
                
            avg=sum/N
            print('%d avg %7.6e MeV' % (j,avg))
            avgs=avgs+avg
            
        print(avgs/5.0)

    print(k,trans,act,M,avgs/5.0)
    


