import numpy
import o2sclpy
import matplotlib.pyplot as plot

def test_all(tmp_path):

    link=o2sclpy.linker()
    link.verbose=2
    link.link_o2scl()

    x=[i*0.3+0.3 for i in range(0,5)]
    y=[i*0.3+0.3 for i in range(0,5)]
    m=o2sclpy.ublas_matrix(link)
    m.resize(5,5)
    for i in range(0,5):
        for j in range(0,5):
            m[i,j]=numpy.sin(x[i])*numpy.cos(y[j])
            
    print('m(0,0):',m[0,0])
    print('m(1,0):',m[1,0])
    print('m(0,1):',m[0,1])

    pb=o2sclpy.plot_base()
    pb.subplots(2,2)

    pb.selax(0)
    pb.den_plot([x,y,m.to_numpy()],pcm=False)
    pb.ttext(0.5,1.06,'no log, pcm=False')

    pb.selax(1)
    pb.den_plot([x,y,m.to_numpy()],pcm=True)
    pb.ttext(0.5,1.06,'no log, pcm=True')
    
    pb.logx=True
    pb.logy=True

    pb.selax(2)
    pb.den_plot([x,y,m.to_numpy()],pcm=False)
    pb.ttext(0.5,1.06,'with log, pcm=False')

    pb.selax(3)
    pb.den_plot([x,y,m.to_numpy()],pcm=True)
    pb.ttext(0.5,1.06,'with log, pcm=True')

    plot.subplots_adjust(left=0.11,right=0.99,bottom=0.08,top=0.95,
                         hspace=0.30,wspace=0.27)
    pb.save('test_den_plot.png')
    pb.show()
    return
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
    
