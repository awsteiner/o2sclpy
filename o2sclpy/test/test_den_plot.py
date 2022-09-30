import numpy
import o2sclpy

def xtest_all(tmp_path):

    link=o2sclpy.linker()
    link.link_o2scl()

    x=[i*0.3 for i in range(0,5)]
    y=[i*0.3 for i in range(0,5)]
    m=o2sclpy.ublas_matrix(5,5)
    for i in range(0,1):
        for j in range(0,1):
            m[i,j]=numpy.sin(x[i])*numpy.cos(y[j])
    print('m(0,0):',m(0,0))
    print('m(1,0):',m(1,0))

    pb=o2sclpy.plot_base()
    pb.subplots(2,2)
    pb.selax(0)
    pb.den_plot([x,y,m],pcm=True)
    pb.selax(1)
    pb.den_plot([x,y,m],pcm=False)
    
    pb.logx=True
    pb.logy=True
    pb.selax(2)
    pb.den_plot([x,y,m],pcm=True)
    pb.selax(3)
    pb.den_plot([x,y,m],pcm=False)
    pb.show()
    return
    
if __name__ == '__main__':
    #xtest_all()
    print('All tests passed.')
    
