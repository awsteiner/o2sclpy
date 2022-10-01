import numpy
import o2sclpy
import matplotlib.pyplot as plot

def test_all(tmp_path):

    link=o2sclpy.linker()
    link.link_o2scl()

    for k in range(0,2):

        if k>0:
            plot.clf()

        if k==0:
            
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

            args=[x,y,m.to_numpy()]
            
        elif k==1:

            t=o2sclpy.table3d(link)
            x=o2sclpy.std_vector(link)
            y=o2sclpy.std_vector(link)
            x.from_list([i*0.3+0.3 for i in range(0,5)])
            y.from_list([i*0.3+0.3 for i in range(0,5)])
            t.set_xy('x',len(x),x,'y',len(y),y)
            t.new_slice('z')
            for i in range(0,5):
                for j in range(0,5):
                    t.set(i,j,'z',numpy.sin(x[i])*numpy.cos(y[j]))

            args=[t,'z']
                    
        elif k==2:

            h=o2sclpy.hist_2d(link)
            x=[i*0.3+0.15 for i in range(0,6)]
            y=[i*0.3+0.15 for i in range(0,6)]
            h.set_xy(x,y)
            for i in range(0,5):
                for j in range(0,5):
                    h.set_wgt_i(i,j,'z',numpy.sin(x[i])*numpy.cos(y[j]))

            args=[h]
                    
        pb=o2sclpy.plot_base()
        pb.subplots(2,2)
    
        pb.selax(0)
        pb.den_plot(args,pcm=False)
        pb.ttext(0.5,1.06,'no log, pcm=False')
    
        pb.selax(1)
        pb.den_plot(args,pcm=True)
        pb.ttext(0.5,1.06,'no log, pcm=True')
        
        pb.logx=True
        pb.logy=True
    
        pb.selax(2)
        pb.den_plot(args,pcm=False)
        pb.ttext(0.5,1.06,'with log, pcm=False')
    
        pb.selax(3)
        pb.den_plot(args,pcm=True)
        pb.ttext(0.5,1.06,'with log, pcm=True')
    
        plot.subplots_adjust(left=0.11,right=0.99,bottom=0.08,top=0.95,
                             hspace=0.30,wspace=0.27)

        if False:
            if k==0:
                pb.save('test_den_plot0.png')
            elif k==1:
                pb.save('test_den_plot1.png')
            elif k==2:
                pb.save('test_den_plot2.png')
            
        pb.show()
        
    return
    
if __name__ == '__main__':
    test_all()
    print('All tests passed.')
    
