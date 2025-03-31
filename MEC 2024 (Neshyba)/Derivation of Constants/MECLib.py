import numpy as np
import h5io
import matplotlib.pyplot as plt
from copy import deepcopy as makeacopy
import pandas as pd
import sys; sys.path.append('/home'); import MECLib as CL


def GetMyScenario(filename,plotflag=True,epsdictionaryflag=True):
    """Loads the stored scheduled flow dictionary, with options to print and plot"""
    
    # Get the entire dictionary
    epsdictionary = h5io.read_hdf5(filename)

    # This extracts the dataframe from the dictionary
    epsdf = epsdictionary['dataframe']

    # This extracts the time and emissions from the dataframe
    time = np.array(epsdf['time'])
    eps = np.array(epsdf['emissions'])

    # Graph the time series (if flagged)
    if plotflag:
        plt.figure()
        plt.plot(time,eps)
        plt.grid(True)
        plt.title(filename)
        plt.xlabel('year')
        plt.ylabel('GtC/year')
        
    # Return
    return time, eps, epsdictionary 
    
def CreateClimateParams(epsdictionary,k_la=120):
    """Returns a structured dictionary containing climate parameters"""

    # Start with an empty dictionary
    ClimateParams = {}
    
   # Amount in the atmosphere (pre-industrial, and at the time of the NASA figure, 2003)
    C_atm_preind = 590
    C_atm_2003 = 780
    
    # The starting time
    epsdf = epsdictionary['dataframe']
    time_preind = np.array(epsdf['time'])[0]

    # Land-to-atmosphere flux constant and fluxes, according to NASA's figure 
    F_la_preind = k_la
    F_la_2003 = F_la_preind
    F_al_2003 = F_la_preind + 3

    # Atm-to-land flux constants (Eq. 4 of Cambio1.0, using 2003 fluxes 
    # and reservoir amounts in pre-industrial time and 2003)
    k_al1 = (F_al_2003-F_la_preind)/(C_atm_2003-C_atm_preind)
    k_al0 = F_la_preind-k_al1*C_atm_preind

    # Atmosphere-to-ocean (Eq. 6 of Cambio1.0, using 2003 flux and 
    # atmospheric reservoir amount)
    F_ao_2003 = 92
    k_ao = F_ao_2003/C_atm_2003
    F_oa_2003 = 90

    # NASA's observed ratio of net ocean sequestration to net land sequestration
    r = 2/3 

    # Ocean-to-atmosphere flux constant based on Cambio1.0 equations, constrained
    # to satisfy the ratio r
    k = epsdictionary['k']
    k_oa = k*(k_ao/(r*k_al1)-1)

    # Atmosphere-to-land feedback parameters
    k_al1_Tstar = 1.43
    k_al1_deltaT = 0.471
    fractional_k_al1_floor = 0.684
    
    # Albedo parameters
    preindustrial_albedo = 0.3
    AS = -102.8
    
    # Attach to the dictionary
    ClimateParams['k_la'] = k_la
    ClimateParams['k_al0'] = k_al0
    ClimateParams['k_al1'] = k_al1
    ClimateParams['k_oa'] = k_oa
    ClimateParams['k_ao'] = k_ao
    ClimateParams['k'] = k
    ClimateParams['DC'] = 0.0321  
    ClimateParams['climate sensitivity'] = 3/C_atm_preind
    ClimateParams['C_atm 2003'] = C_atm_2003
    ClimateParams['F_ao 2003'] = F_ao_2003
    ClimateParams['F_oa 2003'] = F_oa_2003
    ClimateParams['preindustrial C_atm'] = C_atm_preind
    ClimateParams['albedo sensitivity'] = AS
    ClimateParams['preindustrial albedo'] = preindustrial_albedo
    ClimateParams['preindustrial pH'] = 8.2
    ClimateParams['starting time'] = time_preind
    ClimateParams['k_al1_Tstar'] = k_al1_Tstar
    ClimateParams['k_al1_deltaT'] = k_al1_deltaT
    ClimateParams['fractional_k_al1_floor'] = fractional_k_al1_floor
    
    # Albedo feedback parameters (see Wunderling et al for the origin of 0.43 here)
    Delta_alpha_ASI = 0.43/AS; #print(Delta_alpha_ASI)
    fractional_albedo_floor = (preindustrial_albedo+Delta_alpha_ASI)/preindustrial_albedo
    ClimateParams['albedo_Tstar'] = 2
    ClimateParams['albedo_delta_T'] = 1
    ClimateParams['fractional_albedo_floor'] = fractional_albedo_floor

    # Return
    return ClimateParams
    
def CreateClimateState(ClimateParams):
    """Creates a new climate state with default values (preindustrial)"""

    # Create an empty climate state
    ClimateState = {}

    # Fill in some default (preindustrial) values
    ClimateState['C_atm'] = ClimateParams['preindustrial C_atm']
    
    # Pre-industrial ocean carbon reservoir needed to satisfy flux ratios in 2003
    F_ao_preind = ClimateParams['k_ao'] * ClimateParams['preindustrial C_atm'] 
    F_oa_preind = F_ao_preind
    ClimateState['C_ocean'] = F_oa_preind/ClimateParams['k_oa']
    print('Computing a pre-industrial C_ocean = ', ClimateState['C_ocean'])
    
    # Other useful parameters
    ClimateState['albedo'] = ClimateParams['preindustrial albedo']

    # The temperature anomaly in preindustrial times is defined to be zero
    ClimateState['T_anomaly'] = 0

    # And the pH
    ClimateState['pH'] = ClimateParams['preindustrial pH']
    
    # Starting year
    ClimateState['time'] = ClimateParams['starting time']

    # Return the climate
    return ClimateState

def sigmafloor(x,x_trans=0,x_interval=1,sigma_floor_infinity=0):
    """Generates a sigmoid (smooth step-down) function with a floor"""
    temp = 1 - 1/(1 + np.exp(-(x-x_trans)*3/x_interval))
    return temp*(1-sigma_floor_infinity)+sigma_floor_infinity
    
def sigmoid(x,x_thresh=0,x_trans=1,sigma_x_infinity=0):
    """Generates a sigmoid (smooth step-down) function with a floor"""
    return sigmafloor(x,x_thresh,x_trans,sigma_x_infinity)
    
def sigmaup(t,transitiontime,transitiontimeinterval):
    """Generates a sigmoid (smooth step-up) function"""
    return 1 / (1 + np.exp(-(t-transitiontime)*3/transitiontimeinterval))
  
def sigmadown(t,transitiontime,transitiontimeinterval):
    """Generates a sigmoid (smooth step-down) function"""
    return 1 - sigmaup(t,transitiontime,transitiontimeinterval)

def CollectClimateTimeSeries(ClimateState_list,whatIwant):
    """Collects elements from a list of dictionaries"""
    array = np.empty(0)
    for ClimateState in ClimateState_list:
        array = np.append(array,ClimateState[whatIwant])
    return array

def Diagnose_OceanSurfacepH(C_atm,ClimateParams):
    """Returns ocean pH from the carbon amount in the atmosphere"""
    """and the ClimateParams dictionary (preindust_pH and preindust_C_atm)"""

    # Extract the preindustrial pH from ClimateParms
    preindust_pH = ClimateParams['preindustrial pH']
    
    # Extract the preindustrial carbon in the atmosphere from ClimateParams
    preindust_C_atm = ClimateParams['preindustrial C_atm']
    
    # Calculate the pH according to our algorithm
    pH = -np.log10(C_atm/preindust_C_atm)+preindust_pH

    # Return the diagnosed pH
    return(pH)

def Diagnose_T_anomaly(C_atm, alpha, ClimateParams):
    """Returns a temperature anomaly based on the C_atm, Earth's albedo,"""
    """and ClimateParams parameters related to climate_sensitivity and albedo sensitivity"""

    CS = ClimateParams['climate sensitivity']
    preindust_C_atm = ClimateParams['preindustrial C_atm']
    AS = ClimateParams['albedo sensitivity']
    preindust_alpha = ClimateParams['preindustrial albedo']
    
    # Calculate the temperature anomaly according to our algorithm
    T_anomaly = CS*(C_atm-preindust_C_atm) + AS*(alpha-preindust_alpha)

    # Return the temperature anomaly
    return(T_anomaly)

def Diagnose_ppm(C_atm):
    """Computes a temperature anomaly from the atmospheric carbon amount"""
    C_atm_ppm = C_atm*2.12
    return(C_atm_ppm)

def Diagnose_actual_temperature(T_anomaly):
    """Computes degrees C from a temperature anomaly"""
    T_C = T_anomaly+14
    return(T_C)

def Diagnose_degreesF(T_C):
    """Converts temperature from C to F"""

    # Do the conversion to F
    T_F = T_C*9/5+32### END SOLUTION

    # Return the diagnosed temperature in F
    return(T_F)

def Diagnose_albedo_with_constraint(T_anomaly, ClimateParams, previousalbedo=0, dtime=0):
    """
    Returns the albedo as a function of temperature, constrained so the change can't 
    exceed a certain amount per year, if so flagged
    """
        
    # Find the albedo without constraint
    albedo = Diagnose_albedo(T_anomaly, ClimateParams)
    
    # Applying a constraint, if called for
    if (previousalbedo !=0) & (dtime != 0):
        albedo_change = albedo-previousalbedo
        max_albedo_change = ClimateParams['max_albedo_change_rate']*dtime
        if np.abs(albedo_change) > max_albedo_change:
            this_albedo_change = np.sign(albedo_change)*max_albedo_change
            albedo = previousalbedo + this_albedo_change

    # Return the albedo
    return albedo

def Diagnose_albedo(T_anomaly, ClimateParams):
    """
    Returns the albedo as a function of temperature anomaly
    """

    # Extract the fractional albedo floor from ClimateParams
    fractional_albedo_floor = ClimateParams['fractional_albedo_floor']

    # Extract the transition temperature
    try:
        transitionT = ClimateParams['albedo_transition_temperature'] 
    except:
        transitionT = ClimateParams['albedo_Tstar']
        
    # Extract the transition temperature interval
    try:
        transitionTinterval = ClimateParams['albedo_transition_interval'] 
    except:
        transitionTinterval = ClimateParams['albedo_delta_T']
    
    # Extract the preindustrial albedo
    try:
        preindust_albedo = ClimateParams['preindust_albedo']
    except:
        preindust_albedo = ClimateParams['preindustrial albedo']
    
    # Compute the albedo
    albedo = sigmafloor(T_anomaly,transitionT,transitionTinterval,fractional_albedo_floor)*preindust_albedo
                
    # Return the diagnosed albedo
    return albedo


def Diagnose_Delta_T_from_albedo(albedo,ClimateParams):
    """
    Computes additional planetary temperature increase resulting from a lower albedo
    Based on the idea of radiative balance, ASR = OLR
    """
    
    # Extract parameters we need and make the diagnosis
    AS = ClimateParams['albedo_sensitivity']    
    preindust_albedo = ClimateParams['preindust_albedo']
    Delta_T_from_albedo = (albedo-preindust_albedo)*AS
    return Delta_T_from_albedo

# def Diagnose_indirect_T_anomaly(T_anomaly, albedo,ClimateParams):
#     """Computes a temperature anomaly resulting from a lower albedo"""
#     """Based on the idea of radiative balance, ASR = OLR"""
    
#     # Get the delta-T diagnostic
#     Delta_T_from_albedo = Diagnose_Delta_T_from_albedo(albedo,ClimateParams)
    
#     # Update our temperature anomaly
#     T_anomaly += Delta_T_from_albedo
#     return T_anomaly

def Diagnose_Stochastic_C_atm(C_atm,ClimateParams):
    """Returns a noisy version of T"""
    
    # Extract parameters we need and make the diagnosis
    Stochastic_C_atm_std_dev = ClimateParams['Stochastic_C_atm_std_dev']
    C_atm_new = np.random.normal(C_atm, Stochastic_C_atm_std_dev)
    return C_atm_new 

def MakeEmissionsScenario(t_start,t_stop,nsteps,k,eps_0,t_0,t_peak,t_decarb):
    """Returns an emissions scenario"""
    t = np.linspace(t_start,t_stop,nsteps)
    tp1 = t_peak + (t_decarb/3)*np.log(3/(k*t_decarb)-1)
    myeps = np.exp(k*t) * eps_0*np.exp(-k*t_0) * np.exp(3/t_decarb*(tp1-t)) / (1+np.exp(3/t_decarb*(tp1-t)))
    return t, myeps

def MakeEmissionsScenarioLTE(t_start,t_stop,nsteps,k,eps_0,t_0,t_peak,t_decarb,epslongterm):
    """Returns an emissions scenario that has a long-term, post-peak emission"""
    t = np.linspace(t_start,t_stop,nsteps)
    time, eps = MakeEmissionsScenario(t_start,t_stop,nsteps,k,eps_0,t_0,t_peak,t_decarb)
    neweps = PostPeakFlattener(time,eps,t_decarb,epslongterm)
    return time, neweps

def MakeEmissionsScenario1(t_start,t_stop,nsteps,k,eps_0,t_0,t_trans,delta_t_trans):
    """Returns an emissions scenario"""
    time = np.linspace(t_start,t_stop,nsteps)
    myexp = np.exp(k*time)
    myN = eps_0/(np.exp(k*t_0)*sigmadown(t_0,t_trans,delta_t_trans))
    mysigmadown = sigmadown(time,t_trans,delta_t_trans)
    eps = myN*myexp*mysigmadown
    return time, eps

def MakeEmissionsScenario2(t_start,t_stop,nsteps,k,eps_0,t_0,t_peak,delta_t_trans):
    """Returns an emissions scenario parameterized by the year of peak emissions"""
    t_trans = t_peak + delta_t_trans/3*np.log(3/(k*delta_t_trans)-1)
    return MakeEmissionsScenario(t_start,t_stop,nsteps,k,eps_0,t_0,t_trans,delta_t_trans)

def PostPeakFlattener(time,eps,transitiontimeinterval,epslongterm):
    ipeak = np.where(eps==np.max(eps))[0][0]; print('peak',eps[ipeak],ipeak)
    b = eps[ipeak]
    a = epslongterm
    neweps = makeacopy(eps)
    for i in range(ipeak,len(eps)):
        ipostpeak = i-ipeak
        neweps[i] = a + np.exp(-(time[i]-time[ipeak])**2/transitiontimeinterval**2)*(b-a)
    return neweps
 
def MakeEmissionsScenario1LTE(t_start,t_stop,nsteps,k,eps_0,t_0,t_trans,delta_t_trans,epslongterm):
    time, eps = MakeEmissionsScenario(t_start,t_stop,nsteps,k,eps_0,t_0,t_trans,delta_t_trans)
    neweps = PostPeakFlattener(time,eps,delta_t_trans,epslongterm)
    return time, neweps

def MakeEmissionsScenario2LTE(t_start,t_stop,nsteps,k,eps_0,t_0,t_peak,delta_t_trans,epslongterm):
    time, eps = MakeEmissionsScenario2(t_start,t_stop,nsteps,k,eps_0,t_0,t_peak,delta_t_trans)
    neweps = PostPeakFlattener(time,eps,delta_t_trans,epslongterm)
    return time, neweps

def MakeHybridEmissionScenario(\
    t_start,t_stop,EnROADS_time,EnROADS_eps,filename,k=0.0166, nsteps=1000,reportflag=False,plotflag=False):
    
    # Extracting the first emission entry of the baseline scenario, for pegging the cambio scenario
    eps_0=EnROADS_eps[0]; print(eps_0)
    time_0=EnROADS_time[0]; print(time_0)

    # Creating a new cambio scenario compatible pegged to the baseline scenario
    delta_t_trans = 20
    t_peak = time_0+1
    epslongterm = 0
    intermediate_filename = 'ignore_this_file.txt'
    time_cambio, eps_cambio = MakeEmissionsScenario2LTE(t_start,t_stop,nsteps,k,eps_0,time_0,t_peak,delta_t_trans,epslongterm)

    # Loading in that Cambio scenario
#     time_cambio, eps_cambio = GetMyScenario(intermediate_filename,reportflag=False,plotflag=False)

    # Create a set of emissions equal to EnROADS, but interpolated to the cambio times
    dt = time_cambio[1]-time_cambio[0]
    times_to_interpolate = np.arange(time_0+dt,t_stop,dt)
    eps_interpolated = np.interp(times_to_interpolate,EnROADS_time,EnROADS_eps)

    # Create the hybrid emission scenario
    i_pegged,val = min(enumerate(time_cambio), key=lambda x: abs(x[1]-(time_0+dt))); print(i_pegged,val)
    eps_hybrid = np.append(eps_cambio[0:i_pegged],eps_interpolated); print(len(eps_hybrid))

    # Create an empty dictionary
    epsdictionary = dict()

    # Create an empty dataframe
    epsdf = pd.DataFrame()

    # Insert the time and emissions columns into the dataframe
    epsdf.insert(loc=0, column='time', value=time_cambio)
    epsdf.insert(loc=1, column='emissions', value=eps_hybrid)

    # Add the dataframe to the dictionary
    epsdictionary['dataframe'] = epsdf

    # This saves it, if we change the flag to True
    h5io.write_hdf5(filename, epsdictionary, overwrite=True)
    
    return

def run_Cambio(PropagateClimateState, ClimateParams, epstime, eps):

    # Make the starting state the preindustrial
    ClimateState = CreateClimateState(ClimateParams)

    # Initialize our list of climate states 
    ClimateState_list = []

    # The time interval
    dt = epstime[1]-epstime[0]

    # Loop over all the times after the initial one in the scheduled flow
    for i in range(1,len(epstime)):

        # Propagate
        ClimateState = PropagateClimateState(ClimateState,ClimateParams,dt,eps[i])

        # Add to our list of climate states
        ClimateState_list.append(ClimateState)
        
    return ClimateState_list


def PropagateClimateState_Cambio4(previousClimateState, ClimateParams, dt, F_ha):
    """Propagates the state of the climate, with a specified anthropogenic carbon flux"""
    """Returns a new climate state"""

    # Extract constants from ClimateParams
    k_la = ClimateParams['k_la']
    k_al0 = ClimateParams['k_al0']
    k_al1 = ClimateParams['k_al1']
    k_oa = ClimateParams['k_oa']
    k_ao = ClimateParams['k_ao']
    DC = ClimateParams['DC']
    preindustrial_albedo = ClimateParams['preindustrial albedo']
    fractional_albedo_floor = ClimateParams['fractional_albedo_floor']
    albedo_Tstar = ClimateParams['albedo_Tstar']
    albedo_delta_T = ClimateParams['albedo_delta_T']
    k_al1_Tstar = ClimateParams['k_al1_Tstar']
    k_al1_deltaT = ClimateParams['k_al1_deltaT']
    fractional_k_al1_floor = ClimateParams['fractional_k_al1_floor']
    
    # Extract concentrations, albedo, etc, from the previous climate state
    C_atm = previousClimateState['C_atm']
    C_ocean = previousClimateState['C_ocean']
    albedo = previousClimateState['albedo']
    time = previousClimateState['time']
    
    # Get the temperature anomaly implied by the carbon in the atmosphere and the albedo
    T_anomaly = Diagnose_T_anomaly(C_atm, albedo, ClimateParams)

    # Get albedo from the temperature anomaly
    albedo = Diagnose_albedo(T_anomaly, ClimateParams)

    # Get new fluxes (including the effect of temperature anomaly on the ocean-to-atmosphere flux)
    F_la = k_la    
    F_al = k_al0 + k_al1*C_atm*sigmafloor(T_anomaly,k_al1_Tstar,k_al1_deltaT,fractional_k_al1_floor)
    F_oa = k_oa*C_ocean*(1+DC*T_anomaly)
    F_ao = k_ao*C_atm

    # Get new concentrations of carbon that depend on the fluxes
    C_atm += (F_la + F_oa - F_ao - F_al + F_ha)*dt
    C_ocean += (F_ao - F_oa)*dt
    time += dt

    # Ocean surface diagnostic
    OceanSurfacepH = Diagnose_OceanSurfacepH(C_atm,ClimateParams)

    # Create a new climate state with these updates
    ClimateState = makeacopy(previousClimateState)
    ClimateState['C_atm'] = C_atm
    ClimateState['C_ocean'] = C_ocean
    ClimateState['F_al'] = F_al
    ClimateState['F_la'] = F_la
    ClimateState['F_ao'] = F_ao
    ClimateState['F_oa'] = F_oa
    ClimateState['F_ha'] = F_ha
    ClimateState['F_ocean_net'] = F_oa-F_ao
    ClimateState['F_land_net'] = F_la-F_al
    ClimateState['time'] = time
    ClimateState['T_anomaly'] = T_anomaly
    ClimateState['OceanSurfacepH'] = OceanSurfacepH
    ClimateState['albedo'] = albedo

    # Return the new climate state
    return ClimateState

def PropagateClimateState_Cambio3(previousClimateState, ClimateParams, dt, F_ha):
    """Propagates the state of the climate including Henry feedback and ice-albedo feedback"""

    # Extract constants from ClimateParams
    k_la = ClimateParams['k_la']
    k_al0 = ClimateParams['k_al0']
    k_al1 = ClimateParams['k_al1']
    k_oa = ClimateParams['k_oa']
    k_ao = ClimateParams['k_ao']
    DC = ClimateParams['DC']
    preindustrial_albedo = ClimateParams['preindustrial albedo']
    fractional_albedo_floor = ClimateParams['fractional_albedo_floor']
    albedo_Tstar = ClimateParams['albedo_Tstar']
    albedo_delta_T = ClimateParams['albedo_delta_T']
    
    # Extract concentrations, albedo, etc, from the previous climate state
    C_atm = previousClimateState['C_atm']
    C_ocean = previousClimateState['C_ocean']
    albedo = previousClimateState['albedo']
    time = previousClimateState['time']
    
    # Get the temperature anomaly implied by the carbon in the atmosphere and the albedo
    T_anomaly = Diagnose_T_anomaly(C_atm, albedo, ClimateParams)

    # Get albedo from the temperature anomaly
    albedo = Diagnose_albedo(T_anomaly, ClimateParams)

    # Get new fluxes (including the effect of temperature anomaly on the ocean-to-atmosphere flux)
    F_la = k_la    
    F_al = k_al0 + k_al1*C_atm
    F_oa = k_oa*C_ocean*(1+DC*T_anomaly)
    F_ao = k_ao*C_atm

    # Get new concentrations of carbon that depend on the fluxes
    C_atm += (F_la + F_oa - F_ao - F_al + F_ha)*dt
    C_ocean += (F_ao - F_oa)*dt
    time += dt

    # Ocean surface diagnostic
    OceanSurfacepH = Diagnose_OceanSurfacepH(C_atm,ClimateParams)

    # Create a new climate state with these updates
    ClimateState = makeacopy(previousClimateState)
    ClimateState['C_atm'] = C_atm
    ClimateState['C_ocean'] = C_ocean
    ClimateState['F_al'] = F_al
    ClimateState['F_la'] = F_la
    ClimateState['F_ao'] = F_ao
    ClimateState['F_oa'] = F_oa
    ClimateState['F_ha'] = F_ha
    ClimateState['F_ocean_net'] = F_oa-F_ao
    ClimateState['F_land_net'] = F_la-F_al
    ClimateState['time'] = time
    ClimateState['T_anomaly'] = T_anomaly
    ClimateState['OceanSurfacepH'] = OceanSurfacepH
    ClimateState['albedo'] = albedo

    # Return the new climate state
    return ClimateState

def PropagateClimateState_Cambio2(previousClimateState, ClimateParams, dt, F_ha):
    """Propagates the state of the climate including Henry feedback"""

    # Extract constants from ClimateParams
    k_la = ClimateParams['k_la']
    k_al0 = ClimateParams['k_al0']
    k_al1 = ClimateParams['k_al1']
    k_oa = ClimateParams['k_oa']
    k_ao = ClimateParams['k_ao']
    DC = ClimateParams['DC']
    
    # Extract concentrations, albedo, etc, from the previous climate state
    C_atm = previousClimateState['C_atm']
    C_ocean = previousClimateState['C_ocean']
    albedo = previousClimateState['albedo']
    time = previousClimateState['time']
    
    # Get the temperature anomaly implied by the carbon in the atmosphere and the albedo
    T_anomaly = Diagnose_T_anomaly(C_atm, albedo, ClimateParams)
    actual_temperature = Diagnose_actual_temperature(T_anomaly)
    OceanSurfacepH = Diagnose_OceanSurfacepH(C_atm,ClimateParams)
    
    # Get new fluxes (including the effect of temperature anomaly on the ocean-to-atmosphere flux)
    F_la = k_la    
    F_al = k_al0 + k_al1*C_atm
    F_oa = k_oa*C_ocean*(1+DC*T_anomaly)
    F_ao = k_ao*C_atm

    # Get new concentrations of carbon that depend on the fluxes
    C_atm += (F_la + F_oa - F_ao - F_al + F_ha)*dt
    C_ocean += (F_ao - F_oa)*dt
    time += dt
    
    # Create a new climate state with these updates
    ClimateState = makeacopy(previousClimateState)
    ClimateState['C_atm'] = C_atm
    ClimateState['C_ocean'] = C_ocean
    ClimateState['F_al'] = F_al
    ClimateState['F_la'] = F_la
    ClimateState['F_ao'] = F_ao
    ClimateState['F_oa'] = F_oa
    ClimateState['F_ha'] = F_ha
    ClimateState['F_ocean_net'] = F_oa-F_ao
    ClimateState['F_land_net'] = F_la-F_al
    ClimateState['time'] = time
    ClimateState['T_anomaly'] = T_anomaly
    ClimateState['actual temperature'] = actual_temperature
    ClimateState['OceanSurfacepH'] = OceanSurfacepH
    ClimateState['albedo'] = albedo

    # Return the new climate state
    return ClimateState

def PropagateClimateState_Cambio1(previousClimateState, ClimateParams, dt, F_ha):
    """Propagates the state of the climate with no feedback"""

    # Extract constants from ClimateParams
    k_la = ClimateParams['k_la']
    k_al0 = ClimateParams['k_al0']
    k_al1 = ClimateParams['k_al1']
    k_oa = ClimateParams['k_oa']
    k_ao = ClimateParams['k_ao']
    DC = ClimateParams['DC']
    
    # Extract concentrations, albedo, etc, from the previous climate state
    C_atm = previousClimateState['C_atm']
    C_ocean = previousClimateState['C_ocean']
    albedo = previousClimateState['albedo']
    time = previousClimateState['time']
    
    # Get the temperature anomaly implied by the carbon in the atmosphere and the albedo
    T_anomaly = Diagnose_T_anomaly(C_atm, albedo, ClimateParams)
    actual_temperature = Diagnose_actual_temperature(T_anomaly)
    OceanSurfacepH = Diagnose_OceanSurfacepH(C_atm,ClimateParams)
    
    # Get new fluxes (including the effect of temperature anomaly on the ocean-to-atmosphere flux)
    F_la = k_la    
    F_al = k_al0 + k_al1*C_atm
    F_oa = k_oa*C_ocean
    F_ao = k_ao*C_atm

    # Get new concentrations of carbon that depend on the fluxes
    C_atm += (F_la + F_oa - F_ao - F_al + F_ha)*dt
    C_ocean += (F_ao - F_oa)*dt
    time += dt
    
    # Create a new climate state with these updates
    ClimateState = makeacopy(previousClimateState)
    ClimateState['C_atm'] = C_atm
    ClimateState['C_ocean'] = C_ocean
    ClimateState['F_al'] = F_al
    ClimateState['F_la'] = F_la
    ClimateState['F_ao'] = F_ao
    ClimateState['F_oa'] = F_oa
    ClimateState['F_ha'] = F_ha
    ClimateState['F_ocean_net'] = F_oa-F_ao
    ClimateState['F_land_net'] = F_la-F_al
    ClimateState['time'] = time
    ClimateState['T_anomaly'] = T_anomaly
    ClimateState['actual temperature'] = actual_temperature
    ClimateState['OceanSurfacepH'] = OceanSurfacepH
    ClimateState['albedo'] = albedo

    # Return the new climate state
    return ClimateState

def printmaxmin(t,y,label=''):
    imax = np.argmax(y)
    print('Max of '+label+' = ',y[imax], 'at time ', t[imax])
    imin = np.argmin(y)
    print('Min of '+label+' = ',y[imin], 'at time ', t[imin])

def Climatestate_list_plots(ClimateState_list,items_to_plot,plot_title):
    time_array = CollectClimateTimeSeries(ClimateState_list,'time')
    for item in items_to_plot:
        plt.figure()
        plt.title(plot_title)
        plt.grid(True)
        plt.xlabel('time (years)')

        if np.size(item) == 1:
            item_array = CollectClimateTimeSeries(ClimateState_list,item)
            if len(plot_title) != 0:
                plotlabel = plot_title+' ('+item+')'
            else:
                plotlabel = item
            printmaxmin(time_array,item_array,label=plotlabel)
            plt.plot(time_array,item_array,label=item)
        else:
            for subitem in item:
                subitem_array = CollectClimateTimeSeries(ClimateState_list,subitem)
                printmaxmin(time_array,subitem_array,label=plot_title+' ('+subitem+')')
                if len(plot_title) != 0:
                    plotlabel = plot_title+' ('+subitem+')'
                else:
                    plotlabel = subitem
                plt.plot(time_array,subitem_array,label=plotlabel)
        plt.legend()          
        plt.show()
    return

