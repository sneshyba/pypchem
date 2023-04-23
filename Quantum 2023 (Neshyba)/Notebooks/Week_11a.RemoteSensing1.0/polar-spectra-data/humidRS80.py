# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 12:40:14 2014

@author: prowe
"""

import numpy as np

def humidRS80(wvin,Tamb_K,unitIn,unitOut,P_mb):
  #
  #
  # wvout = humidRS80(wvin,Tamb_K,iunit,ounit,P_mb)
  #
  #
  # by Penny Rowe
  # May 1, 2002
  # Nov 11, 2005: updated to include iunit=6 and ounit=4
  # Oct 20, 2009: modified so that Psat_w or Psat_i generally created.
  #
  # iunit (input units for wvin)
  #	 1/rhw:    rh_w as given by RS80 radiosonde
  #	 2:        dewpoint temp as given by RS80 radiosonde (C), using Wexler
  #	 3:        dewpoint temp as given by RS80 radiosonde (C), using Goff-Gratch
  #	 4:        frostpoint temp as given by RS80 radiosonde, using Wexler
  #	 5/rhi:    rh_i, assuming that is given by RS80 radiosonde (i.e. using Wexler)
  #	 6/pa:     Pa, as calculated by this code
  #	 7/rhi_MM: rh_i, (using Marti & Maursberger)
  #  8/mixrat: mixing ratio by weight: g/kg
  #  9:        dewpoint temp, www.wrh.noaa.gov/slc/projects/wxcalc/formulas/vaporPressure.pdf
  # 10:        dewpoint temp, using Durre and Yin, 2008 ?
  # 11/ppmv:   ppmv with respect to dry air
  #
  # ounit (output units for wvin)
  #	1/pa:     Partial pressure of wv in Pa
  #	2/rhi_MM: rh_i, using Marti & Mauersberger
  #	3:        frostpoint temp in deg C
  #	4/rhw:    rh_w (undo the conversion using this code)
  #	5/rhi:    rh_i, using hyland and wexler
  #	6:        Psat_w, Pa (note this only dep# ends on T)
  #   7/ppmv:   mixing ratio by volume: ppmv with respect to dry air
  #   8/pwv:    Precipitable Water Vapor in meters
  #   9/mixrat: mixing ratio by weight: g/kg
  #  10/moleccm3: molecules / cm^3
  
  # Notes:
  #	Since Vaisala uses Wexler's formula for the RS80, I use Wexler
  #	to undo the relative humidity wrt water.  I think that this means using
  #	Wexler's equation to calculate Psat_w(Tamb_K) and dividing by that, since
  #	(letting "w" represent liquid water):
  #
  # Updates 2010/01/07:
  #   - I converted the symbol for partial pressure of water vapor in Pa from
  #     Pwv to Ph2o to avoid confusion with precipitable water vapor (PWV)
  #     (PMR 2010/01/07)
  #   - I included output options of PWV and mixing ratio by weight
  #     (PMR 2010/01/07)
  #   - Added option of input ppmv      (PMR 2010/01/07)
  #   - Added optional string inputs that will be converted to numbers
  #     (PMR 2010/01/07)
  #   - P_mb is an optional input, but if it's needed, code will bomb
  #     (PMR 2013/09/01)
  #
  #	RH_w = 100 * (P_w / Psat_w(Tamb_K))
  #
  
  # function Ph2o = rh2PwvWexler(rh,td)
  #
  #
  # Uses Hyland and Wexler (1983) and Wexler (1976)
  #
  # Inputs: rh as reported by radisonde
  #			 td - ambient temperature in Kelvin
  #
  # Both of these can be vectors, in which case output will be a vector
  
  #*********************************************************************
  # #             function few_wexhy, t
  # #
  # #;    Saturation vapor pressure over water.  Wexler (1976) formulation.
  # #;       Input is temperature in degrees K.  e_w is in dyne/cm^2 (microbars).
  # #
  # #     td=double(t)
  # #
  # #     c0 = -2.9912729e3    &   c1 = -6.0170128e3   &   c2 = 1.887643854e1
  # #     c3 = -2.8354721e-2   &   c4 = 1.7838301e-5   &   c5 = -8.4150417e-10
  # #     c6 = 4.4412543e-13   &   D = 2.858487
  # #
  # #     term = (c0*td^(-2)) + (c1*td^(-1)) + (c2*td^0) + (c3*td^1) + (c4*td^2)+$
  # #            (c5*td^3) + (c6*td^4)
  # #     few = exp(term + (D*alog(td)))  ; Pa
  # #
  # #        return, few * 10.
  # #        # end
  
  # Note: alog in IDL = log in Matlab = natural log (ln)

  """  
  # QC: check dimensions
  if size(wvin,1) ~= size(Tamb_K,1) || size(wvin,2) ~= size(Tamb_K,2)
    if size(wvin,1)==size(Tamb_K,2)
      Tamb_K = Tamb_K';
    else
      error('w.v. and temperature vectors not same size')
    # end
  # end
  if exist('P_mb','var')
    if size(wvin,1) ~= size(P_mb,1) || size(wvin,2) ~= size(P_mb,2)
      if size(wvin,1)==size(P_mb,2)
        P_mb = P_mb';
      else
        error('w.v. and pressure vectors not same size')
      # end
    # end
  # end
  
  
  
  # ounit (output units for wvin)
  #	1/pa:     Partial pressure of wv in Pa
  #	2/rhi_MM: rh_i, using Marti & Mauersberger
  #	3:        frostpoint temp in deg C
  #	4/rhw:    rh_w (undo the conversion using this code)
  #	5/rhi:    rh_i, using hyland and wexler
  #	6:        Psat_w, Pa (note this only dep# ends on T)
  # 7/ppmv:   mixing ratio by volume: ppmv
  # 8/pwv:    Precipitable Water Vapor in meters
  # 9/mixrat: mixing ratio by weight: g/kg
  """
  
  
  
  # input is rh_w, calculate Ph2o using Wexler
  if unitIn == 'rh_w' or unitIn == 'rhw' or unitIn == 'rh' :
      
    # Warning: the following has not been checked against
    # the matlab version (or even tested)
    rh_w = wvin;
    
    c0 = -2.9912729e3;   c1 = -6.0170128e3;   c2 = 1.887643854e1;
    c3 = -2.8354721e-2;   c4 = 1.7838301e-5;   c5 = -8.4150417e-10;
    c6 = 4.4412543e-13;   D = 2.858487;
    term = (c0*Tamb_K**(-2)) + (c1*Tamb_K**(-1)) + (c2*Tamb_K**0) + \
      (c3*Tamb_K**1) + (c4*Tamb_K**2)+ (c5*Tamb_K**3) + (c6*Tamb_K**4);
    
    Psat_w = np.exp(term + D*np.log(Tamb_K))  ; 	#Pa
    
    Ph2o = 0.01 * rh_w * Psat_w 
    
    
  # dewpoint temperature, calc Ph2o, Psat_w using Wexler  
  elif unitIn == 'dewpoint' or unitIn == 'Td':
    
    # The following requires testing
    Td_K = wvin + 273.15 
    T = Td_K 
    
    c0 = -2.9912729e3;    c1 = -6.0170128e3;   c2 = 1.887643854e1
    c3 = -2.8354721e-2;   c4 = 1.7838301e-5;   c5 = -8.4150417e-10
    c6 = 4.4412543e-13;    D = 2.858487
    term = (c0*T**(-2)) + (c1*T**(-1)) + (c2*T**0) + \
      (c3*T**1) + (c4*T**2)+ (c5*T**3) + (c6*T**4)
    
    PwvWex = np.exp(term + D*np.log(T))  # Pa
    Ph2o = PwvWex 
    

    # Get Psat_w too, starting from Ph2o
    term = (c0*Tamb_K**(-2)) + (c1*Tamb_K**(-1)) + (c2*Tamb_K**0) + \
      (c3*Tamb_K**1) + (c4*Tamb_K**2)+ (c5*Tamb_K**3) + (c6*Tamb_K**4);
    
    Psat_w = np.exp(term + D*np.log(Tamb_K))  	#Pa
    
    
  elif unitIn == 'ppmv':              # ppmv with respect to dry air
    ppp  = 1e-6 * wvin 
  
    if unitOut != 'pwv':
      Ph2o = ppp * P_mb             # water vapor amount in mb
      
      Ph2o = ppp * (P_mb - Ph2o)    # was ppmv with respect to DRY air
      Ph2o = ppp * (P_mb - Ph2o)    # Repeat
      Ph2o = ppp * (P_mb - Ph2o)    # Repeat - this should be acceptable
      
      Ph2o = Ph2o*100              # convert from mb to Pa
    # end
    
  """   
  elseif iunit==3 # dewpoint temp., calc Ph2o using Goff-Gratch
    
    
    # actually, lets try assuming for some reason Goff-Gratch is used to
    # go from rh to Td, then
    #
    # #             function few_goffg, t
    # #
    # #;    Saturation vapor pressure over water.  Goff-Gratch formulation.
    # #;       Input is temperature in degrees K.  e_w is in dyne/cm^2.
    # #
    # #     ts = double(373.16)   &   sr = double(3.0057166)
    ts = 373.16 ; sr = 3.0057166;
    
    Td = wvin + 273.15 ;
    ar = ts ./ Td ;
    br  = 7.90298 * (ar - 1.0) ;
    cr  = 5.02808 * log10(ar) ;
    dw  = 1.3816e-07 * (10.0 .^ (11.344 * (1.0 - 1.0 ./ ar)) - 1.0) ;
    er  = 8.1328e-03 * (10.0 .^ (-(3.49149 * (ar - 1.0))) - 1.0) ;
    # #
    PwvGG = 100*10.0 .^ (cr - dw + er + sr - br) ;
    Ph2o = PwvGG ;
    
    ar = ts ./ Tamb_K ;
    br  = 7.90298 * (ar - 1.0) ;
    cr  = 5.02808 * log10(ar) ;
    dw  = 1.3816e-07 * (10.0 .^ (11.344 * (1.0 - 1.0 ./ ar)) - 1.0) ;
    er  = 8.1328e-03 * (10.0 .^ (-(3.49149 * (ar - 1.0))) - 1.0) ;
    Psat_w = 100*10.0 .^ (cr - dw + er + sr - br) ;
    
  elseif iunit==4    #Tf, calc Ph2o using Wexler
    
    # #;    Saturation vapor pressure over ice. Hyland and Wexler (1983) 
    # #        formulation
    # #;       Input is temperature in degrees K.  e_i is in dyne/cm^2.
    # #
    # #     td=double(t)
    # #
    c0 = -5.6745359e3 ;   c1 = 6.3925247 ;   c2 = -9.6778430e-3 ;
    c3 = 6.2215701e-7 ;   c4 = 2.0747825e-9 ;   c5 = -9.4840240e-13 ;
    D = 4.1635019 ;
    # #
    td = wvin + 273.15 ;
    term = (c0*td.^(-1)) + (c1*td.^(0)) + (c2*td.^1) + (c3*td.^2) + \
      (c4*td.^3)+ (c5*td.^4) ;
    Ph2o = exp(term + (D*log(td)))  ;  #Pa
    
    T = Tamb_K ;
    term = (c0*T.^(-1)) + (c1*T.^(0)) + (c2*T.^1) + (c3*T.^2) + (c4*T.^3)+ ...
      (c5*T.^4) ;
    Psat_w = exp(term + (D*log(T)))  ;  #Pa
    
  elseif iunit==5 # rh_i, calc Ph2o using Wexler
    
    rh_i = wvin;
    td = Tamb_K ;
    
    c0 = -5.6745359e3 ;   c1 = 6.3925247 ;   c2 = -9.6778430e-3 ;
    c3 = 6.2215701e-7 ;   c4 = 2.0747825e-9 ;   c5 = -9.4840240e-13 ;
    D = 4.1635019 ;
    # #
    term = (c0*td.^(-1)) + (c1*td.^(0)) + (c2*td.^1) + (c3*td.^2) + \
      (c4*td.^3)+ (c5*td.^4) ;
    
    Psat_i = exp(term + D*log(td))  ; 	#Pa
    
    Ph2o = 0.01 * rh_i .* Psat_i ;
    
  elseif iunit==6  # already in Pa (Ph2o)
    Ph2o = wvin ;
    
  elseif iunit==7 # rh_i, calc Ph2o using Marti & Maursberger
    
    rh_i = wvin;
    
    # constants
    A = -2663.5;  # +-.8, Kelvin
    B = 12.537;   # +- 0.11
    
    logp = A./Tamb_K + B;
    Psat_i = 10.^(logp);			# Pa
    
    Ph2o = 0.01 * rh_i .* Psat_i ;
    
  elseif iunit==8
    # g/kg
    h2o_gpkg = wvin ;
    
    # Get some constants
    [constants,units] = getConstants ;
    
    if ounit ~= 8
      ppp = h2o_gpkg / constants.MW_H2O * constants.MWdryAir/1000;
      # g H2O/kg dry air / (g H2O/mol) * g dry air/mol * 1kg/1000g = mol/mol
      Ph2o = ppp .* (P_mb*100-0)    ; # mb * 100 = Pa
      Ph2o = ppp .* (P_mb*100-Ph2o) ; # repeat - we need the partial P of dry air
      Ph2o = ppp .* (P_mb*100-Ph2o) ; # repeat - we need the partial P of dry air
      Ph2o = ppp .* (P_mb*100-Ph2o) ; # repeat - we need the partial P of dry air
      
    # end
    
  elseif iunit==9   # dewpoint temp. using NOAA
    
    Td   = wvin ;             # Celsius!
    T    = Tamb_K - 273.15 ;  # Celsius!
    Ph2o  = 6.11 * 10.^( (7.5*Td)./(237.7+Td) ) ;
    Psat_w = 6.11 * 10.^( (7.5*T)./(237.7+T) ) ;
    
  elseif iunit==10   # dewpoint temp. using
    
    Td    = wvin ;             # Celsius!
    T     = Tamb_K - 273.15 ;  # Celsius!
    f     = 1.0007+3.46.*P_mb*1e-6 ;
    
    Ph2o  = 100*f.*6.1121 .* exp( Td.*( (18.729 - Td/227.3) )  ./  (Td+257.87) ) ;
    Psat_w = 100*f.*6.1121 .* exp( T.*( (18.729 - T./227.3) )  ./  (T+257.87) ) ;
    
  """  
  
    
  """
  else:
    error('This value of unitIn is not implemented.')
  """
  # end
  
  
  # ... The outputs
  
  """
  if ounit==1			# output is Ph2o
    wvout = Ph2o ;
    
  elseif ounit==2		# output is rh_i
    
    if exist('Psat_i','var')
      warning('humidRS80:whichPsat_i','I am not sure which Psat_i I should use');
    elseif exist('Psat_w','var')
      warning('humidRS80:Psat_iVsPsat_w',...
        'I have Psat_w, will calculate Psat_i using satpressure_ice.');
    # end
    Tamb_C = Tamb_K - 273.15;
    rh_i = 100*Ph2o ./ satpressure_ice(Tamb_C) ;
    wvout = rh_i ;
    
  elseif ounit==3 # output is Tf using Marti and Mauers.
    # Ph2o=>Tf
    # Reference:
    #
    # Marti, James and Konrad Mauersberger, A Survey of New Measurements
    # of Ice Vapor Pressure at Temperatures Between 170 and 250K,
    # Geophys. Res. Let., vol. 20, No. 5, pp. 363-366, 1993.
    
    # constants
    A = -2663.5;  # +-.8, Kelvin
    B = 12.537;   # +- 0.11
    
    #logp = A./T_K + B;
    #Psat_ice = 10.^(logp);			# Pa
    Tf = A ./ ( log10(Ph2o)-B );
    wvout = Tf -273.15;
    
  elseif ounit==4  #output is rh_w (i.e. undo previous calc.)
    
    if ~exist('Psat_w','var')
      #warning('humidRS80:noPsat_w','Creating Psat_w, see code.');
      
      c0 = -2.9912729e3;   c1 = -6.0170128e3;   c2 = 1.887643854e1;
      c3 = -2.8354721e-2;   c4 = 1.7838301e-5;   c5 = -8.4150417e-10;
      c6 = 4.4412543e-13;   D = 2.858487;
      term = (c0*Tamb_K.^(-2)) + (c1*Tamb_K.^(-1)) + (c2*Tamb_K.^0) + ...
        (c3*Tamb_K.^1) + (c4*Tamb_K.^2)+ (c5*Tamb_K.^3) + (c6*Tamb_K.^4);
      
      Psat_w = exp(term + D*log(Tamb_K))  ; 	#Pa
    # end
    
    # Ph2o = 0.01 * rh_w .* Psat_w ;
    #rh_w = 100*Ph2o/.01./Psat_w ;
    rh_w = 100*Ph2o./Psat_w ;
    
    wvout = rh_w;
    
    
  elseif ounit==5  # output is rh_i
    # but use Hyland and Wexler
    # #             function fei_wexhy, t
    # #
    # #;    Saturation vapor pressure over ice. Hyland and Wexler (1983) formulation
    # #;       Input is temperature in degrees K.  e_i is in dyne/cm^2.
    # #
    # #     td=double(t)
    # #
    if exist('Psat_i','var')
    else
      warning('humidRS80:noPsat_i','I am creating Psat_i using Hyland and Wexler.');
      td = Tamb_K;
      c0 = -5.6745359e3 ;   c1 = 6.3925247;   c2 = -9.6778430e-3;
      c3 = 6.2215701e-7 ;   c4 = 2.0747825e-9;   c5 = -9.4840240e-13;
      D = 4.1635019;
      # #
      term = (c0*td.^(-1)) + (c1*td.^(0)) + (c2*td.^1) + ...
        (c3*td.^2) + (c4*td.^3)+(c5*td.^4);
      Psat_i = exp(term + (D*log(td)))  ; #Pa
      #Pwv_i = .01*rh_w .* Psat_i ;
    # end
    
    rh_i = 100*Ph2o./Psat_i ;
    
    wvout = rh_i ;
    
  elseif ounit==6  # output is Psat_wv
    
    if exist('Psat_w','var')
    else
      warning('humidRS80:noPsat_w','Creating Psat_w, see code.');
      
      c0 = -2.9912729e3;   c1 = -6.0170128e3;   c2 = 1.887643854e1;
      c3 = -2.8354721e-2;   c4 = 1.7838301e-5;   c5 = -8.4150417e-10;
      c6 = 4.4412543e-13;   D = 2.858487;
      term = (c0*Tamb_K.^(-2)) + (c1*Tamb_K.^(-1)) + (c2*Tamb_K.^0) + ...
        (c3*Tamb_K.^1) + (c4*Tamb_K.^2)+ (c5*Tamb_K.^3) + (c6*Tamb_K.^4);
      
      Psat_w = exp(term + D*log(Tamb_K))  ; 	#Pa
    # end
    
    
    wvout = Psat_w ; # Pa
    
  else
  """
  
  if unitOut == 'ppmv':                      # output is ppmv
    
    wvout = 1e6 * Ph2o / (100*P_mb-Ph2o) 
    
  """  
  elseif ounit==8  # output is Precipitable Water Vapor in m
    
    # From AMS glossary
    # PWV = (1/g) integral_P1_P2[x dp]
    # where x(p) = mixing ratio, .622e / (p-e)
    # where p=pressure, e=vapor pressure
    
    con = getConstants();                    # get constants
    
    if iunit==11
      # we already have ppp
      gpg = ppp * con.MW_H2O / con.MWdryAir ;  # grams per gram
      
    elseif iunit ~= 8
      
      # input in pascals
      ppp = Ph2o ./ (P_mb*100 - Ph2o ) ;       # parts water per part dry air
      gpg = ppp * con.MW_H2O / con.MWdryAir ;  # grams per gram
      
    elseif iunit==8
      # we have water vapor in g/kg
      gpg = h2o_gpkg * (1/1000) ;
    # end
    
    x     = gpg/ con.rho_h2o;      # g/g kg-1 m3
    wvout = -trapz(P_mb*100,x);    # m3 kg-1 Pa = m3 kg-1 kg m-1 s-2 = m2 s-2
    wvout = wvout/con.g;           # m2 s-2 * m-1 s2 = m
    
  elseif ounit==9  # output is mixing ratio as g/kg: g water / kg air
    
    constants = getConstants();  # get constants
    ppp = Ph2o ./ (P_mb*100 - Ph2o ) ;  # parts per part
    gpg = ppp*constants.MW_H2O / constants.MWdryAir ;  # grams per gram
    
    wvout = gpg *1000 ; # g/g g/kg = g/kg
    
  elseif ounit==10  # output is molecules / cm3
    
    con   = getConstants ;
    wvout = Ph2o./(con.k*Tamb_K) /100^3 ;  # molec / m3 * (1 m / 100 cm)^3
                                           # molecules / cm3
  else
    error('ounits>7 not here yet');
    
  """
  # end
  
  
  
  return wvout
  









# #*********************************************************************
# #             function fei_wexhy, t
# #
# #;    Saturation vapor pressure over ice. Hyland and Wexler (1983) formulation
# #;       Input is temperature in degrees K.  e_i is in dyne/cm^2.
# #
# #     td=double(t)
# #
# #     c0 = -5.6745359e3    &   c1 = 6.3925247   &   c2 = -9.6778430e-3
# #     c3 = 6.2215701e-7   &   c4 = 2.0747825e-9   &   c5 = -9.4840240e-13
# #     D = 4.1635019
# #
# #     term = (c0*td^(-1)) + (c1*td^(0)) + (c2*td^1) + (c3*td^2) + (c4*td^3)+$
# #            (c5*td^4)
# #     fei = exp(term + (D*alog(td)))  ; Pa
# #
# #        return, fei * 10.
# #        # end
# #*********************************************************************
# #             function few_wexhy, t
# #
# #;    Saturation vapor pressure over water.  Wexler (1976) formulation.
# #;       Input is temperature in degrees K.  e_w is in dyne/cm^2 (microbars).
# #
# #     td=double(t)
# #
# #     c0 = -2.9912729e3    &   c1 = -6.0170128e3   &   c2 = 1.887643854e1
# #     c3 = -2.8354721e-2   &   c4 = 1.7838301e-5   &   c5 = -8.4150417e-10
# #     c6 = 4.4412543e-13   &   D = 2.858487
# #
# #     term = (c0*td^(-2)) + (c1*td^(-1)) + (c2*td^0) + (c3*td^1) + (c4*td^2)+$
# #            (c5*td^3) + (c6*td^4)
# #     few = exp(term + (D*alog(td)))  ; Pa
# #
# #        return, few * 10.
# #        # end
# #*********************************************************************
# #     function rhisat_wexhy, T
# #
# #; Saturation humidity.  Input T in C.
# #; e_w from Wexler (1976); e_i from Hyland and Wexler (1983)
# #
# #     TK = double(T + 273.15)
# #     return, (fei_wexhy(TK) / few_wexhy(TK)) * 100.0
# #     # end
# #*********************************************************************
# #     function fei_goffg, t
# #
# #;       Saturation vapor pressure over ice.  Goff-Gratch formulation.
# #;       Input is temperature in degrees K.  e_i is in dyne/cm^2.
# #
# #        ai  = double(273.16) / t
# #        bi  = 9.09718 * (ai - 1.0)
# #        ci  = 3.56654 * alog10(ai)
# #        dic = 0.876793 * (1.0 - 1.0 / ai)
# #        eic = alog10(6.1071)
# #
# #        fei = 10.0 ^ (dic + eic - ci - bi)
# #     return, fei * 1000.
# #        # end
# #*********************************************************************
# #             function few_goffg, t
# #
# #;    Saturation vapor pressure over water.  Goff-Gratch formulation.
# #;       Input is temperature in degrees K.  e_w is in dyne/cm^2.
# #
# #     ts = double(373.16)   &   sr = double(3.0057166)
# #
# #        ar = ts / t
# #        br  = 7.90298 * (ar - 1.0)
# #        cr  = 5.02808 * alog10(ar)
# #        dw  = 1.3816e-07 * (10.0 ^ (11.344 * (1.0 - 1.0 / ar)) - 1.0)
# #        er  = 8.1328e-03 * (10.0 ^ (-(3.49149 * (ar - 1.0))) - 1.0)
# #
# #        few = 10.0 ^ (cr - dw + er + sr - br)
# #        return, few * 1000.
# #        # end
# #***************************************************************
# #     function rhisat_goffg, t
# #
# #; e_w and e_i from Smithsonian Met Tables (Goff-Gratch, 1940s)
# #
# #     tk = double(t + 273.16)
# #     return, (fei_goffg(tk) / few_goffg(tk)) * 100.0
# #     # end
# ##
# ## Hi Larry,
# ##
# ## We use Goff-Gratch formula  (see http://eos913c.gsfc.nasa.gov/
# gcss_wg2/projects/parcel/GG.html).  Can you s# end formulas for
# ## Wexler-Hyland so we can check more about this difference?  I did
# a quick look on web pages, and Goff-Gratch sure seems to be used a
# ## lot, so if it is wrong, there are implications elsewhere. (e.g.
# see http://www.cnrm.meteo.fr/dbfastex/datasets/moz.html,
# ## http://www.iac.ethz.ch/~dominik/idltools/idl_atmosphys.htmlo
# for examples.)
# ##
# ## Thanks,
# ##
# ## Rich
# ##
# ## On Wed, 3 Apr 2002 14:51:27 -0700 (MST), milo@ncar.ucar.edu wrote:
# ##
# ## #Brian,
# ## #
# ## #I'm not familiar with Keifer, but I was curious so I did some
# ## # quick calculations comparing the RH wrt water of ice
# ## # saturation from Wexler-Hyland and Goff-Gratch:
# ## #
# ## #IDL# T=[-50.,-60,-70,-80]
# ## #IDL# print,rhisat_wexhy(T)
# ## #       61.116723       55.450131       50.406602       45.956034
# ## #IDL# print,rhisat_goffg(T)
# ## #       61.907500       56.935199       53.155242       51.065583
# ## #IDL# print,rhisat_wexhy(T) - rhisat_goffg(T)
# ## #     -0.79077691      -1.4850672      -2.7486397      -5.1095482
# ## #
# ## #If -70C is about the coldest AFWEX temperature, then the relative
# ## #difference between the formulations is about -2.75/53.16 = -5.1#,
# ## #just what you suggested.  But that is at ice-saturation, so if the
# ## #UTH is half ice-saturation then the relative error is -10#.  I hope
# ## #that's not 10# in the wrong direction!  If -60C is a more appropriate
# ## #temperature, then it's 2.6# relative error at ice-saturation.  In any
# ## #event, these numbers are representative of one more source of
# ## #uncertainty in UT humidity measurements.
# ## #
# ## #                          Larry
# ## #
# ## ##
# ## ## You make raise a good point. I've been using a formula by Keifer, largely
# ## ## because it assympototes to zero at cold temperatures, rather than going
# ## ## haywire and producing negative values like some polynomial fits.
# ## ## I think this might affect things at the 5# level, but I really can't envision
# ## ## it havign a 30# effect.  Rich - do you know what formula your group is using?
# ## ##
# ## ## On Wednesday 03 April 2002 03:22 pm, milo@ncar.ucar.edu wrote:
# ## ## # Hi Brian,
# ## ## #
# ## ## # I'll confirm what Barry already confirmed, that the radiosonde RH is wrt
# ## ## # water, and I'll add one other comment that makes a difference at cold
# ## ## # temperatures.  If the RH is calculated from the saturation vapor
# ## ## # pressures, then it matters which formulation you use.  I use the
# ## ## # Wexler-Hyland formulations (partly because Vaisala does).  Does this
# ## ## # come into your calculations, and do you use Goff-Gratch or something
# ## ## # else?
# ## ## #                               Larry
# ## ## #
# ## ## # # I'm going back through my calculations to see why my results seem so
# ## ## # # different from Rich's. I wanted to confirm with Barry and Larry that the
# ## ## # # RH profiles in their data sets are RH wrt water (rather than RH wrt ice).
# ## ## # # Is this correct?
# ## ## # #
# ## ## # # Brian
# ## ##
# ## ## --
# ## ## _________________________________________________
# ## ##
# ## ## Brian Soden             bjs@gfdl.gov
# ## ## GFDL/NOAA
#http://www.gfdl.gov/~bjs/
# ## ## Princeton University    609-452-6575
# ## ## Post Office  Box 308    609-987-5063  [FAX]
# ## ## Princeton, NJ  08542
# ## ## _________________________________________________
# ## ##
# ## #
# ## #
# ##
# ##
# ##
# ##
# ## _____________________________________________________________
# ## Dr. Rich Ferrare
# ## Chemistry and Dynamics Branch/Atmospheric Sciences Research
# ## NASA/Langley Research Center
# ## Mail Stop 401A
# ## Building 1250/Room 135
# ## Hampton, VA 23681-0001
# ##
# ## r.ferrare@larc.nasa.gov
# ## Phone: 757-864-9443
# ## Fax: 757-864-7790
# ## Lidar Home Page: http://asd-www.larc.nasa.gov/lidar/lidar.html
# ## _____________________________________________________________
# ##
# ##
# #
# #
#
#
#
#

#  --
#
#  David Tobin
#  CIMSS/SSEC/U.Wisconsin-Madison
#  dave.tobin@ssec.wisc.edu


