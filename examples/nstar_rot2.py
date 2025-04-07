# # nstar rot example for O$_2$sclpy

import o2sclpy
import matplotlib.pyplot as plot
import numpy
import sys
import random
from mpi4py import MPI

class bayes_nstar_rot:
    """
    Desc
    """
    
    def __init__(self):
        """
        Desc
        """

        # Get a copy (a pointer to) the O$_2$scl unit conversion object,
        # which also allows access to the constant library

        self.o2scl_settings=o2sclpy.lib_settings_class()
        self.cu=self.o2scl_settings.get_convert_units()
        self.hc=self.cu.find_unique('hbarc','MeV*fm')
        self.verbose=0
        self.low=[-2.0,0.33,-2.0]
        self.high=[4.0,0.8,4.0]

        # Output file handle
        self.f=0

        # Total runtime
        self.runtime=0.0

    def initial_point(self):
        """
        Desc
        """
        
        # Initial guess
        a=13
        alpha=0.49
        S=32
        L=44
        n1=0.8
        nbtrans=0.64
        n2=0.7

        self.one_point(n1,nbtrans,n2)

        return

    def one_point(self,n1,nbtrans,n2,output,
                  a=13,alpha=0.49,S=32,L=44,verbose=1):
        """
        Desc
        """
        
        b=S-16-a
        beta=(L-3*a*alpha)/b/3
        n0=0.16
        if verbose>0:
            output.write('b,beta: %7.6e %7.6e' % (b,beta))

        tab=o2sclpy.table_units()
        tab.line_of_names('nb ed pr')
        tab.line_of_units('1/fm^3 1/fm^4 1/fm^4')
        tab.set_nlines(25)
        for i in range(0,25):
            if self.verbose>1:
                output.write('i',i)
            nb=0.08+i*0.01
            tab.set('nb',i,nb)
            tab.set('ed',i,939.0/197.33*nb+(nb*a*(nb/n0)**alpha+
                                            nb*b*(nb/n0)**beta)/197.33)
            tab.set('pr',i,(n0*a*alpha*(nb/n0)**(1.0+alpha)+
                            n0*b*beta*(nb/n0)**(1.0+beta))/197.33)
            
        ed32=tab.get('ed',tab.get_nlines()-1)
        pr32=tab.get('pr',tab.get_nlines()-1)
        
        coeff1=pr32/ed32**(1.0+1.0/n1)
        p1=o2sclpy.eos_tov_polytrope()
        p1.set_coeff_index(coeff1,n1)
        p1.set_baryon_density(0.32,ed32)
        
        for i in range(1,33):
            nb=0.32+i*(nbtrans-0.32)/32
            tab.line_of_data([nb,p1.ed_from_nb(nb),p1.pr_from_nb(nb)])

        edlast=tab.get('ed',tab.get_nlines()-1)
        prlast=tab.get('pr',tab.get_nlines()-1)

        coeff2=prlast/edlast**(1.0+1.0/n2)
        p2=o2sclpy.eos_tov_polytrope()
        p2.set_coeff_index(coeff2,n2)
        p2.set_baryon_density(nbtrans,edlast)
    
        for i in range(1,33):
            nb=nbtrans+i*(1.5-nbtrans)/32
            tab.line_of_data([nb,p2.ed_from_nb(nb),p2.pr_from_nb(nb)])

        if self.verbose>1:
            for i in range(0,tab.get_nlines()):
                output.write('%7.6e %7.6e %7.6e' %
                             (tab.get('nb',i),tab.get('ed',i),
                              tab.get('pr',i)))

        eti=o2sclpy.eos_tov_interp()
        eti.default_low_dens_eos()
        eti.read_table(tab,'ed','pr','nb')
        ts=o2sclpy.tov_solve()
        ts.set_eos(eti)
        ts.verbose=self.verbose
        ts.mvsr()

        # Delete table rows larger than the maximum mass
        nonrot=ts.get_results()
        prmax=nonrot.get('pr',nonrot.lookup('gm',nonrot.max('gm')))
        nonrot.delete_rows_func('pr>'+str(prmax))

        # Compute the maximum speed of sound only below
        # the maximum energy density

        edmax=nonrot.max('ed')
        if self.verbose>0:
            output.write('edmax %7.6e %s' % (edmax,nonrot.get_unit('ed')))
        edmax2=self.cu.convert('Msun/km^3','1/fm^4',edmax)
        if self.verbose>0:
            output.write('edmax2 %s 1/fm^4' % (edmax2))
        tab.deriv_col('ed','pr','cs2')
        cs2_max=0
        for i in range(0,tab.get_nlines()):
            if verbose>1:
                output.write(i,tab.get('ed',i),edmax2,tab.get('cs2',i))
            if tab.get('ed',i)<edmax2 and tab.get('cs2',i)>cs2_max:
                cs2_max=tab.get('cs2',i)
        if verbose>0:
            output.write('cs2_max: %7.6e' % (cs2_max))

        # The radius of a 1.4 solar mass neutron star
        rad14=nonrot.interp('gm',1.4,'r')

        if verbose>0:
            output.write('rad14: %7.6e' % (rad14))

        enri=o2sclpy.eos_nstar_rot_interp()
        edv=o2sclpy.std_vector()    
        prv=o2sclpy.std_vector()    
        nbv=o2sclpy.std_vector()
        for i in range(0,tab.get_nlines()):
            edv.push_back(tab.get('ed',i))
            prv.push_back(tab.get('pr',i))
            nbv.push_back(tab.get('nb',i))
        enri.set_eos_fm(tab.get_nlines(),edv,prv,nbv)
    
        # Construct a configuration with a specified central energy density
        # and axis ratio
        
        nr=o2sclpy.nstar_rot()
        nr.err_nonconv=False
        nr.verbose=1
        nr.set_eos(enri)
        last_mass=0
        for i in range(0,30):
            rho_cent=4.0e14*(10**float(i/29))
            ret=nr.fix_cent_eden_with_kepler(rho_cent)

            output.write('ret',ret)

            output.write('%d %7.6e %7.6e %7.6e %7.6e %7.6e %7.6e' %
                  (i,rho_cent,nr.Mass/nr.MSUN,nr.R_e/1.0e5,
                   nr.r_p/nr.r_e,nr.Omega,nr.r_ratio))
            
            if i>0 and nr.Mass/nr.MSUN<last_mass:
                i=30
                output.write('stopping early')
            last_mass=nr.Mass/nr.MSUN

        return

    def loop_time(self,rank,size,rtime):
        """
        Desc
        """

        with open(('nstar_rot2_'+str(rank))+'.txt','w') as f:
            print('Starting run on rank',rank,'of',size,'with time',
                  rtime)

            start_time=MPI.Wtime()

            N=100
            for i in range(0,N):
                n1=random.random()*4.0+0.01
                n2=random.random()*4.0+0.01
                nbtrans=random.random()*0.66+0.33
                b.one_point(n1,nbtrans,n2,f)
                elapsed=MPI.Wtime()

                if elapsed-start_time>rtime:
                    i=N:
                
        f.close()

        return
    
if __name__ == '__main__':

    if len(sys.argv)<2:
        print('Argument required.')
        quit()
    if sys.argv[1]=='test':
        b=bayes_nstar_rot()
        b.initial_point()
    if sys.argv[1]=='production':
        if len(sys.argv)<3:
            print('Production needs time')
            quit()
            
        comm=MPI.COMM_WORLD
        rank=comm.Get_rank()
        size=comm.Get_size()

        if rank==0:
            print('Beginning production run.')
        
        b=bayes_nstar_rot()
        b.loop_time(rank,size,float(sys.argv[2]))

        

    
