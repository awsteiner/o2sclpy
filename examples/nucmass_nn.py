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

vary_nn_parms=False

# Create the data set:

# Instantiate and load the Atomic Mass Evaluation. The third parameter
# is False, to indicate that we include masses which are not solely
# determined by experiment
ame=o2sclpy.nucmass_ame()
o2sclpy.ame_load(ame,'20',False)
print('Number of isotopes in the AME list:',ame.get_nentries())

dist_exp=o2sclpy.std_vector_nucleus()
o2sclpy.nucdist_set(dist_exp,ame,'')
print('Number of nuclei in dist_exp:',len(dist_exp))

msis=o2sclpy.nucmass_mnmsk()
o2sclpy.mnmsk_load(msis,'msis16')

dist_msis=o2sclpy.std_vector_nucleus()
o2sclpy.nucdist_set(dist_msis,msis)
print('Number of nuclei in dist_msis:',len(dist_msis))

# Instantiate the Duflo-Zuker fit and set parameters from a recent fit
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

# Instantiate the FRDM-shell fit and set parameters from a recent fit
frdm_shell=o2sclpy.nucmass_frdm_shell()
p.resize(14)
p[0]=2.657399203505667e+00
p[1]=1.136316849511381e+00
p[2]=3.548541967676024e+01
p[3]=1.649009712939987e+01
p[4]=2.331520244072635e+01
p[5]=3.437294342444157e+01
p[6]=2.660294896136239e+01
p[7]=4.409661805078772e-01
p[8]=2.501490274580595e+01
p[9]=1.897879047364143e+00
p[10]=-1.460475719478483e+00
p[11]=1.928679183044334e-02
p[12]=1.901033655300475e-03
p[13]=8.970261351311239e-02
frdm_shell.fit_fun(14,p)

# Instantiate the ldrop_shell fit and set parameters from a recent fit
ldrop_shell=o2sclpy.nucmass_ldrop_shell()
sk=o2sclpy.eos_had_skyrme()
o2sclpy.skyrme_load(sk,'SLy4')
ldrop_shell.set_eos_had_temp_base(sk)
p.resize(11)
p[0]=8.994776301007761e-01
p[1]=9.679865078598426e-01
p[2]=8.751369188587536e-01
p[3]=9.710432146736609e-01
p[4]=-9.041294789462331e-03
p[5]=1.390547985659261e-01
p[6]=1.246579548574642e+01
p[7]=-1.493972115439528e+00
p[8]=1.419539065031770e-02
p[9]=1.659654542326672e-03
p[10]=1.136613448382515e-01
ldrop_shell.fit_fun(11,p)

# Instantiate tables
wlw=o2sclpy.nucmass_wlw()
wlw.load("WS4_RBF")

# Create the initial table from which the neural network fit is based
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

# Write the table to a file
hf=o2sclpy.hdf_file()
hf.open_or_create('nm2.o2')
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

# Create the neural network interpolation object

for k in range(0,27):

    if vary_nn_parms==True or k==19:

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
        
        # Try each configuration five times, and take the
        # average of the 5 at the end
        n_fits=0
        
        for j in range(0,5):

            if vary_nn_parms==True or j==0:
            
                im2=o2sclpy.interpm_tf_dnn()
                
                # Train the neural network
                
                im2.set_data(x2,y2,verbose=1,epochs=800,
                             transform_in=trans,test_size=0.1,
                             activations=[act,act,act,act],
                             hlayers=[240*M,120*M,60*M,40*M])
                im2.save('nm2.keras')
                
                sum=0
                for i in range(0,N):
                    v=numpy.array([x2[i,0],x2[i,1]])
                    sum+=numpy.abs(im2.eval(v)[0]-y2[i,0])
                    
                avg=sum/N
                print('%d avg %7.6e MeV' % (j,avg))
                avgs=avgs+avg
                n_fits=n_fits+1
                
        print(avgs/n_fits)
    
    print(k,trans,act,M,avgs/n_fits)

# Plot Tin isotopes    


