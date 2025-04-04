# # nstar rot example for O$_2$sclpy

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

# Get a copy (a pointer to) the O$_2$scl unit conversion object,
# which also allows access to the constant library

o2scl_settings=o2sclpy.lib_settings_class()
cu=o2scl_settings.get_convert_units()

if len(sys.argv)<2:

    # Set up the EOS
    
    eC=o2sclpy.eos_nstar_rot_C()
    eC.set(True)
    
    # Construct a configuration with a specified central energy density
    # and axis ratio
    
    nr=o2sclpy.nstar_rot()
    nr.verbose=1
    nr.set_eos(eC)
    nr.fix_cent_eden_axis_rat(2.0e15,0.59)
    
    # Obtain the output table3d object
    
    t3d=o2sclpy.table3d()
    nr.output_table(t3d)
    
    # Output the slice names: ed, pr, h, vsq, rho, gamma, omega, alpha
    
    for i in range(0,t3d.get_nslices()):
        print(i,t3d.get_slice_name(i))
    
    # Print out the gravitational mass
        
    print('%7.6e' % (nr.Mass/nr.MSUN))

    # The the log carefully so we can plot
    
    t3d.function_slice('if(pr>1.0e-12,log10(pr),-12.0)','log10_pr')
    
    # Plot the pressure output
    
    if plots:
        pb=o2sclpy.plot_base()
        pb.colbar=True
        pb.den_plot([t3d,'log10_pr'])
        pb.save('nr1.png')
        plot.close()
    
    # Create a new table for the output in Cartesian coordinates

    t3db=o2sclpy.table3d()
    t3db.set_interp_type(o2sclpy.itp_linear)
    rad_eq=nr.R_e/1.0e5
    coord_grid=o2sclpy.uniform_grid_end.init(0.01,rad_eq*1.1,100)
    t3db.set_xy_grid('x',coord_grid,'z',coord_grid)
    t3db.line_of_names('ed pr')

    # Interpolate into the Cartesian coordinates
    
    for i in range(0,t3db.get_nx()):
        for j in range(0,t3db.get_ny()):
            r=numpy.sqrt(coord_grid[i]**2+coord_grid[j]**2)
            theta=numpy.atan(-coord_grid[j]/coord_grid[i])+numpy.pi/2.0
            t3db.set(i,j,'ed',t3d.interp(r/(r+rad_eq),
                                         numpy.cos(theta),'ed'))
            t3db.set(i,j,'pr',t3d.interp(r/(r+rad_eq),
                                         numpy.cos(theta),'pr'))
    
    # The the log carefully so we can plot
    
    t3db.function_slice('if(pr>1.0e-5,log10(pr),-5.0)','log10_pr')
        
    # Plot the rotating star
    
    if plots:
        pb=o2sclpy.plot_base()
        pb.fig_dict='dpi=250'
        pb.colbar=True
        pb.den_plot([t3db,'log10_pr'])
        pb.save('nr2.png')
        plot.close()

elif sys.argv[1]=='p':
    
