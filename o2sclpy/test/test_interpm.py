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

    im=o2sclpy.interpm_sklearn_gpr()
    im.set_data_str(x,y,'verbose=2')
    print(im.eval([0.2,0.1]),0.2**3+3*(0.1**2))
            
    return

if __name__ == '__main__':
    test_all()
    print('All tests passed.')
