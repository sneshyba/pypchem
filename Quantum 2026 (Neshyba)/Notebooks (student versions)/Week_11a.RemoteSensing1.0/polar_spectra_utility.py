import numpy as np
import scipy.io.netcdf as netcdf
import matplotlib.pyplot as plt
import copy

# A function for simulating the downwelling radiance.  
def radtran(wnm, od, tzl):
    nnu, nlyr = od.shape                    # Better be (len(wnm), itop)
    trans_lyr = np.vstack([np.ones((nnu)).T, np.exp(-od).T]).T
    transL = 1*trans_lyr
    for i in range(1, nlyr+1):
        transL[:,i] = transL[:,i-1]*trans_lyr[:,i]        
    itop = len(tzl)-1
    tave = (tzl[:itop]+tzl[1:itop+1])/2     # Use tave as ave layer temp
    ilayers = list(range(itop))             # Downwelling radiance, surface up
    nulen  = len(wnm)
    rad    = np.zeros((nulen))
    for ilayer in ilayers:                  # get trans, rad from the bottom up
      Bb   =  plancknu(wnm, tave[ilayer])   # Clough et al. 1992 Eqn. (13)
      Bu   =  plancknu(wnm, tzl[ilayer])    # Uses low resolution layer optical depth
      atau = 0.278*od[:,ilayer]             # Pade coeff. x tau
      BL   = (Bb + atau*Bu)* (1+atau)**-1 ;                    # Eqn (15)
      rad0 = -BL * (transL[:,ilayer+1]-transL[:,ilayer]) ;     # Eqn (14)
      rad += rad0
    rad = 1e3 * np.real(rad)     
    return rad

# .. A function to get the radiance for a model atmosphere (do not modify)
def get_my_radiance(co2, h2o, ch4, other, dT):
    nlyr_h2o = 9
    # .. Load in some files we will need
    nu = np.loadtxt('polar-spectra-data/nu.txt')
    T0 = np.loadtxt('polar-spectra-data/T.txt') - 10
    od_co2 = np.loadtxt('polar-spectra-data/co2.txt')/367.71
    od_h2o = np.loadtxt('polar-spectra-data/h2o.txt')/617.44
    od_ch4 = np.loadtxt('polar-spectra-data/ch4.txt')/1.7
    od_other = np.loadtxt('polar-spectra-data/other.txt')
    od_self = np.loadtxt('polar-spectra-data/h2o_self.txt')/(617.44**2)
    
    # .. Get rid of some of the ringing in the od
    od_h2o[np.round(nu)==781,:] = .000005
    od_h2o[np.round(nu)==783,:] = .000005
    od_h2o[np.round(nu)==786,:] = .000005
    od_h2o[np.round(nu)==797,:] = .000005
    od_h2o[np.round(nu)==800,:] = .000005
    od_h2o[np.round(nu)==802,:] = .000005
    
        
# .. Create the new spectrum
    od = od_co2*co2 + od_ch4*ch4 + od_other*other
    od[:,:nlyr_h2o] = od[:,:nlyr_h2o] + od_h2o[:,:nlyr_h2o]*h2o \
      + od_self[:,:nlyr_h2o]*h2o**2
    od[od<0] = 0
    T = T0 + dT
    rad = radtran(nu, od, T)    
    my_legend = 'CO$_2$='+str(co2)+', H$_2$O='+str(h2o)+', CH$_4$='+str(ch4)+', other='+str(other)+'x'
    return nu, rad, my_legend

def plancknu(nu_icm,T):
  h    = 6.62606896e-34   # J s;  CODATA 2006
  c    = 2.99792458e8     # m/s;  NIST
  k    = 1.3806504e-23    # J K-1; CODATA 2006
  cbar = 100*c            # cm/s
  top = 2 * h * cbar**3 * nu_icm**3
  bottom = c**2 *  ( np.exp(h*cbar*nu_icm/(k*T))-1 )
  f = cbar * top/bottom
  return f

# A function for labeling your plots. 
def add_the_labels():
    # Label it
    plt.xlabel('wavenumber (cm$^{-1}$)')
    plt.ylabel('Radiance (mW / [m$^2$ sr$^{-1}$ cm$^{-1}$])')

    # Put a dotted line at zero
    plt.plot([450, 1800], [0, 0], 'k:')    

    # Zoom in on the interesting part
    plt.xlim([500, 1800])
    plt.ylim([-5, 215])          

    # Label the gases for the Oklahoma spectrum
    plt.text(900, 155, 'Mystery Gas')  
    plt.text(540, 162, 'H$_2$O')  
    plt.text(1550, 60, 'H$_2$O')    # Centered at 1595 cm-1
    plt.text(667, 158, 'CO$_2$')    # Centered at 667 cm-1
    plt.text(1030, 100, 'O$_3$')    # Centered at 1042 cm-1
    plt.text(1240, 75, 'N$_2$O')    # Centered at 1285 cm-1
    plt.text(1280, 65, 'CH$_4$')    # Centered at 1311 cm-1
    plt.plot([772, 772, 1340, 1340], [145, 150, 150, 145], 'k')
    plt.arrow(1042, 98, 0, -15, head_width=20, head_length=8, color='k') # O3 arrow
    plt.plot([1340, 1340, 1798, 1798], [53, 58, 58, 53], 'k')
