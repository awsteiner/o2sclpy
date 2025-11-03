# See the O$_2$sclpy documentation at https://awsteiner.org/code/o2sclpy for more information.

# +
import o2sclpy
import matplotlib.pyplot as plot
import numpy
import sys

plots=True
if 'pytest' in sys.modules:
    plots=False
# -

# Load the data sets of nuclei

# Instantiate and load the Atomic Mass Evaluation. The third parameter
# is False, to indicate that we include masses which are not solely
# determined by experiment

ame=o2sclpy.nucmass_ame()
ame.load('20',False)
print('Number of isotopes in the AME list:',ame.get_nentries())

dist_exp=o2sclpy.std_vector_nucleus()
o2sclpy.nucdist_set(dist_exp,ame)
print('Number of nuclei in dist_exp:',len(dist_exp))

msis=o2sclpy.nucmass_mnmsk()
o2sclpy.mnmsk_load(msis,'msis16')

dist_msis=o2sclpy.std_vector_nucleus()
o2sclpy.nucdist_set(dist_msis,msis)
print('Number of nuclei in dist_msis:',len(dist_msis))

# Instantiate the Duflo-Zuker (DZ) fit and set parameters from a
# recent fit. Note that this isn't the original DZ table, but rather a
# new fit of the 33-parameter DZ model to the 2020 AME.

dz=o2sclpy.nucmass_dz_fit_33()
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

# Instantiate the FRDM fit and set parameters from a recent fit

frdm=o2sclpy.nucmass_frdm()
p.resize(10)
p[0]=1.470521168091704e+00
p[1]=1.110599542324431e+00
p[2]=4.233650770523403e+01
p[3]=1.677705218132046e+01
p[4]=2.646289872432062e+01
p[5]=3.443846328788821e+01
p[6]=2.585455547917483e+01
p[7]=7.138147608954237e-01
p[8]=1.284100176024626e+00
p[9]=2.660955290904157e-01
frdm.fit_fun(10,p)

# Instantiate tables

wlw=o2sclpy.nucmass_wlw()
wlw.load("WS4_RBF")

# Create the initial table from which the neural network fit is based
# We fit the deviation in the mass excess. We also remove the
# most neutron-rich isotopes of Sn by hand, so we can see how good
# the neural network is doing later.

nuc=o2sclpy.nucleus()
tab=o2sclpy.table()
tab.line_of_names('Z N mex mex_th diff')
for Z in range(8,200):
    for N in range(8,250):
        line=[Z,N,0,0,0]
        if (ame.is_included(Z,N) and dz.is_included(Z,N) and
            (Z!=50 or N<=80)):
            ame.get_nucleus(Z,N,nuc)
            line[2]=nuc.mex*197.33
            dz.get_nucleus(Z,N,nuc)
            line[3]=nuc.mex*197.33
            line[4]=line[2]-line[3]
            if Z==50:
                print(line)
            tab.line_of_data(line)

# Write the table to a file

hf=o2sclpy.hdf_file()
if 'pytest' in sys.modules:
    filename='examples/data/nucmass_nn.o2'
else:
    filename='data/nucmass_nn.o2'
hf.open_or_create(filename)
o2sclpy.hdf_output_table(hf,tab,b'table')
hf.close()

# Reformat the table into a numpy array for the interpm class

N=tab.get_nlines()
x2=numpy.zeros((N,2))
y2=numpy.zeros((N,1))
for i in range(0,N):
    x2[i,0]=tab["Z"][i]
    x2[i,1]=tab["N"][i]
    y2[i,0]=tab["diff"][i]
print('Number of isotopes to fit:',N)

# The input transformation

trans='moto'

# The activation function

act='relu'

# The neural network size parameter

M=4

# Create the neural network interpolation object

im2=o2sclpy.interpm_tf_dnn()

# Train the neural network or load a previous training

if True:
    im2.set_data(x2,y2,verbose=1,epochs=800,
                 transform_in=trans,test_size=0.1,
                 activations=[act,act,act,act],
                 hlayers=[240*M,120*M,60*M,40*M])
else:
    im2.load('data/nucmass_nn2')

# Print the absolute deviation

sum=0
for i in range(0,N):
    v=numpy.array([x2[i,0],x2[i,1]])
    sum+=numpy.abs(im2.eval(v)[0]-y2[i,0])
qual=sum/N
print('Quality: %7.6e' %(qual))

# Save the result in a file

if 'pytest' in sys.modules:
    im2.save('examples/data/nucmass_nn2')
else:
    im2.save('data/nucmass_nn2')

# Plot the loss and the validation loss

if plots:
    index=[i for i in range(0,len(im2.loss))]
    pb=o2sclpy.plot_base()
    pb.fig_dict='fig_size_x=6,fig_size_y=6,dpi=250'
    pb.plot([index,im2.loss])
    pb.plot([index,im2.val_loss])
    pb.show()
    plot.close()
    
# Compute Tin isotopes

Z=50
sn=o2sclpy.table()
sn.line_of_names('N ame dz msis dz_nn dz_ame dz_nn_ame')
for N in range(50,100):
    if ame.is_included(Z,N):
        ame.get_nucleus(Z,N,nuc)
        ame_mex=nuc.mex
    else:
        ame_mex=0.0
    dz.get_nucleus(Z,N,nuc)
    dz_mex=nuc.mex
    msis.get_nucleus(Z,N,nuc)
    msis_mex=nuc.mex
    # diff is ame-dz, so ame is diff+dz
    ii=numpy.array([50,N])
    if ame.is_included(Z,N):
        line=[N,ame_mex*197.33,dz_mex*197.33,msis_mex*197.33,
              dz_mex*197.33+im2.eval(ii)[0],
              (dz_mex-ame_mex)*197.33,
              dz_mex*197.33+im2.eval(ii)[0]-ame_mex*197.33]
              
    else:
        line=[N,ame_mex*197.33,dz_mex*197.33,msis_mex*197.33,
              dz_mex*197.33+im2.eval(ii)[0],1.0,1.0]
    sn.line_of_data(line)

# Plot Sn isotopes

if plots:
    pb=o2sclpy.plot_base()
    pb.fig_dict='fig_size_x=6,fig_size_y=6,dpi=250'
    pb.plot([sn,'N','ame'])
    pb.plot([sn,'N','dz'])
    pb.plot([sn,'N','msis'])
    pb.plot([sn,'N','dz_nn'])
    pb.show()
    plot.close()

# Plot theory minus experiment
    
if plots:
    pb=o2sclpy.plot_base()
    pb.fig_dict='fig_size_x=6,fig_size_y=6,dpi=250'
    pb.plot([sn,'N','dz_ame'])
    pb.plot([sn,'N','dz_nn_ame'])
    pb.show()
    plot.close()
    
    
