import o2sclpy
import matplotlib.pyplot as plot
import numpy
import sys
import random
import math
from mpi4py import MPI

class bayes_nstar_rot:
    """
    Perform a Bayesian inference with rotating neutron stars
    """
    
    def __init__(self):
        """
        Initialize class data members 
        """

        # Get a copy (a pointer to) the O$_2$scl unit conversion object,
        # which also allows access to the constant library
        self.o2scl_settings=o2sclpy.lib_settings_class()
        self.cu=self.o2scl_settings.get_convert_units()
        self.hc=self.cu.find_unique('hbarc','MeV*fm')

        # Verbosity parameter
        self.verbose=0

        # Output file handle
        self.f=0

        # Total runtime
        self.runtime=0.0

    def initial_point(self):
        """
        Compute the likelihood function with a single initial point.
        """
        
        # Initial guess
        n1=0.8
        nbtrans=0.64
        n2=0.7

        self.one_point(n1,nbtrans,n2)

        return

    def one_point(self,n1,nbtrans,n2,output,
                  a=13,alpha=0.49,S=32,L=44):
        """
        Compute the likelihood function from the three parameters,
        ``n1``, ``nbtrans``, and ``n2`` and place output in file
        handle ``output``.
        """

        # Set up numerical parameters for low-density equation of state
        b=S-16-a
        beta=(L-3*a*alpha)/b/3
        n0=0.16
        if self.verbose>0:
            output.write('params: %7.6e %7.6e %7.6e\n' %
                         (n1,nbtrans,n2))

        # Create the table to store the equation of state. The column
        # ``nb`` is the baryon number density, ``ed`` is the energy
        # density, and ``pr`` is the pressure.
        tab=o2sclpy.table_units()
        tab.line_of_names('nb ed pr')
        tab.line_of_units('1/fm^3 1/fm^4 1/fm^4')

        # Add the low-density part based on quantum Monte Carlo from
        # Gandolfi et al. (2014) from baryon densities of 0.08 fm^{-3}
        # to 0.32 fm^{-3}.
        tab.set_nlines(25)
        for i in range(0,25):
            nb=0.08+i*0.01
            tab.set('nb',i,nb)
            tab.set('ed',i,939.0/self.hc*nb+(nb*a*(nb/n0)**alpha+
                                            nb*b*(nb/n0)**beta)/self.hc)
            tab.set('pr',i,(n0*a*alpha*(nb/n0)**(1.0+alpha)+
                            n0*b*beta*(nb/n0)**(1.0+beta))/self.hc)
            if self.verbose>1:
                output.write('1: %7.6e %7.6e %7.6e\n' %
                             (tab.get('nb',i),tab.get('ed',i),
                              tab.get('pr',i)))
        if self.verbose>1:
            output.flush()

        # The energy density and pressure at a baryon density of 0.32
        # fm^{-3}
        ed32=tab.get('ed',tab.get_nlines()-1)
        pr32=tab.get('pr',tab.get_nlines()-1)

        # Construct the first polytrope object
        coeff1=pr32/ed32**(1.0+1.0/n1)
        p1=o2sclpy.eos_tov_polytrope()
        p1.set_coeff_index(coeff1,n1)
        p1.set_baryon_density(0.32,ed32)

        # Add the first polytrope object to the table
        for i in range(1,33):
            nb=0.32+i*(nbtrans-0.32)/32
            if not math.isfinite(p1.ed_from_nb(nb)):
                output.write(('nb,n1,coeff1,edlast,prlast: '+
                              '%7.6e %7.6e %7.6e %7.6e %7.6e\n') % 
                             (nb,n1,coeff1,ed32,pr32))
                return (1,0)
            tab.line_of_data([nb,p1.ed_from_nb(nb),p1.pr_from_nb(nb)])
            if self.verbose>1:
                output.write('2: %7.6e %7.6e %7.6e\n' %
                             (nb,p1.ed_from_nb(nb),p1.pr_from_nb(nb)))
        if self.verbose>1:
            output.flush()

        # The energy density and pressure at density ``nbtrans``
        edlast=tab.get('ed',tab.get_nlines()-1)
        prlast=tab.get('pr',tab.get_nlines()-1)

        # Construct the second polytrope object
        coeff2=prlast/edlast**(1.0+1.0/n2)
        p2=o2sclpy.eos_tov_polytrope()
        p2.set_coeff_index(coeff2,n2)
        p2.set_baryon_density(nbtrans,edlast)

        # Add the second polytrope object to the table
        for i in range(1,33):
            nb=nbtrans+i*(1.5-nbtrans)/32
            if not math.isfinite(p2.ed_from_nb(nb)):
                output.write(('nb,n2,coeff2,edlast,prlast: '+
                              '%7.6e %7.6e %7.6e %7.6e %7.6e\n') % 
                             (nb,n2,coeff2,edlast,prlast))
                return (2,0)
            tab.line_of_data([nb,p2.ed_from_nb(nb),p2.pr_from_nb(nb)])
            if self.verbose>1:
                output.write('3: %7.6e %7.6e %7.6e\n' %
                             (nb,p2.ed_from_nb(nb),p2.pr_from_nb(nb)))
        if self.verbose>1:
            output.flush()

        # Output the entire table if verbose is larger than 1
        if self.verbose>0:
            for i in range(0,tab.get_nlines()):
                output.write('4: %7.6e %7.6e %7.6e\n' %
                             (tab.get('nb',i),tab.get('ed',i),
                              tab.get('pr',i)))
            output.flush()

        # For comparison, construct the nonrotating mass-radius
        # relation
        eti=o2sclpy.eos_tov_interp()
        eti.default_low_dens_eos()
        eti.read_table(tab,'ed','pr','nb')
        ts=o2sclpy.tov_solve()
        ts.set_eos(eti)
        #ts.verbose=self.verbose
        ts.verbose=0
        ts.mvsr()

        # Delete table rows beyond the maximum mass configuration
        nonrot=ts.get_results()
        prmax=nonrot.get('pr',nonrot.lookup('gm',nonrot.max('gm')))
        nonrot.delete_rows_func('pr>'+str(prmax))

        # Compute the maximum speed of sound only below
        # the maximum energy density

        edmax=nonrot.max('ed')
        if self.verbose>0:
            output.write('edmax %7.6e %s\n' %
                         (edmax,o2sclpy.force_string(nonrot.get_unit('ed'))))
        edmax2=self.cu.convert('Msun/km^3','1/fm^4',edmax)
        if self.verbose>0:
            output.write('edmax2 %s 1/fm^4\n' % (edmax2))
        tab.deriv_col('ed','pr','cs2')
        cs2_max=0
        for i in range(0,tab.get_nlines()):
            if self.verbose>1:
                output.write('%d %7.6e %7.6e %7.6e\n' %
                             (i,tab.get('ed',i),edmax2,tab.get('cs2',i)))
            if tab.get('ed',i)<edmax2 and tab.get('cs2',i)>cs2_max:
                cs2_max=tab.get('cs2',i)
        if self.verbose>0:
            output.write('cs2_max: %7.6e\n' % (cs2_max))

        # The radius of a 1.4 solar mass neutron star
        rad14=nonrot.interp('gm',1.4,'r')

        if self.verbose>0:
            output.write('rad14: %7.6e\n' % (rad14))

        # Construct the EOS object for the rotating neutron star class
        enri=o2sclpy.eos_nstar_rot_interp()
        edv=o2sclpy.std_vector()    
        prv=o2sclpy.std_vector()    
        nbv=o2sclpy.std_vector()
        for i in range(0,tab.get_nlines()):
            edv.push_back(tab.get('ed',i))
            prv.push_back(tab.get('pr',i))
            nbv.push_back(tab.get('nb',i))
        enri.set_eos_fm(tab.get_nlines(),edv,prv,nbv)
    
        # Create the rotating neutron star object and set the EOS
        nr=o2sclpy.nstar_rot()
        nr.err_nonconv=False
        nr.verbose=1
        nr.set_eos(enri)

        # Create a series of configurations with increasing energy
        # density at the Keplerian rotation limit
        last_mass=0
        i=0
        done=False
        while i<30 and done==False:
            rho_cent=4.0e14*(10**float(i/29))
            ret=nr.fix_cent_eden_with_kepler(rho_cent)

            output.write('%d %d %7.6e %7.6e %7.6e %7.6e %7.6e %7.6e\n' %
                  (i,ret,rho_cent,nr.Mass/nr.MSUN,nr.R_e/1.0e5,
                   nr.r_p/nr.r_e,nr.Omega,nr.r_ratio))
            output.flush()

            # If the gravitational mass drops, stop early
            if i>0 and nr.Mass/nr.MSUN<last_mass:
                output.write('rank %d stopping early\n' % (rank))
                done=True
            last_mass=nr.Mass/nr.MSUN
            i=i+1

        return (0,0)

    def loop_time(self,rank,size,rtime):
        """
        Randomly select parameters until the elapsed time
        is greater than the runtime specified in ``rtime``. 
        """

        with open(('nstar_rot2_'+str(rank))+'.txt','w') as f:
            print('Starting run on rank',rank,'of',size,'with time',
                  rtime)

            start_time=MPI.Wtime()

            N=100
            i=0
            done=False
            while done==False and i<N:

                # Randomize the parameters
                n1=random.random()*4.0+0.01
                n2=random.random()*4.0+0.01
                nbtrans=random.random()*0.66+0.33

                # Evaluate the point
                print('Going to one_point(): %d %7.6e %7.6e %7.6e' %
                      (rank,n1,nbtrans,n2))
                b.verbose=2
                b.one_point(n1,nbtrans,n2,f)

                # Check to see if the elapsed time is greater
                # than the request runtime
                elapsed=MPI.Wtime()-start_time
                if elapsed>rtime:
                    print('Rank',rank,'elapsed',elapsed,
                          'greater than rtime',rtime,'.')
                    done=True

                # Increase the iteration number
                i=i+1
                
        f.close()

        return
    
if __name__ == '__main__':

    if len(sys.argv)<2:
        
        print("Argument required, either 'test' or 'production'.")
        quit()
        
    if sys.argv[1]=='test':
        
        b=bayes_nstar_rot()
        b.initial_point()
        
    if sys.argv[1]=='production':
        
        if len(sys.argv)<3:
            print('Production mode requires additional runtime argument.')
            quit()
            
        comm=MPI.COMM_WORLD
        rank=comm.Get_rank()
        size=comm.Get_size()

        if rank==0:
            print('Beginning production run.')
        
        b=bayes_nstar_rot()
        b.loop_time(rank,size,float(sys.argv[2]))

        

    
