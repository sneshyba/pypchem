def plancknu(nu_icm,T):

  # function f = plancknu(nu_icm,T);
  #
  # spectral Planck function as function of wavenumbers (cm-1)
  #
  # [h]    = J*s
  # [c]    = m/s
  # [cbar] = cm/s
  # [k]    = J*K-1
  #
  #
  #    Note: LBLRTM uses ...
  #c    Constants from NIST 01/11/2002
  #
  #      DATA PLANCK / 6.62606876E-27 /, BOLTZ  / 1.3806503E-16 /,
  #     *     CLIGHT / 2.99792458E+10 /, 
  # 
 
  import numpy as np
   
  h    = 6.62606896e-34				# J s;  CODATA 2006
  c    = 2.99792458e8				# m/s;  NIST
  k    = 1.3806504e-23				# J K-1; CODATA 2006
  cbar = 100*c			  		# cm/s
  
  nu = nu_icm+0.
  
  # Ignore the possibility of input nu == 0 for now
  #if np.isscalar(nu):
  #  if nu==0:
  #    f = 0
  #else
  #  i0 = np.where(nu==0)[0]
  #  if len(i0) > 0:
  #    nu[i0] = 1e-6


  top    = 2 * h * cbar**3 * nu**3
  bottom =  c**2 *  ( np.exp(h*cbar*nu/(k*T))-1 )
  
  f      = cbar*top/bottom
 

  # now set f to zero for wavenumbers less than or equal to 0
  #if len(i0)>0:
  #  f[i0] = 0


  #[B]= cm*s-1*J*s*cm3*s-3*cm-3*m-2*s2
  #[B]= W m-2 cm

  return f

	