import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt

def Statespace(xspecs,yspecs):
    xarray = np.linspace(xspecs[0],xspecs[1],xspecs[2])
    yarray = np.linspace(yspecs[0],yspecs[1],yspecs[2])
    ygridtemp,xgridtemp = np.meshgrid(yarray,xarray)
    xgrid = xgridtemp
    ygrid = ygridtemp
    return xgrid, ygrid

def plot_surface(Xgrid, Ygrid, Zgrid, color='purple', overlay=False, ax=0):
    # Creates a surface plot in the handle myax
    
    if overlay==False:
        fig = plt.figure() 
        ax = plt.axes(projection='3d')
#         ax = plt.figure().gca(projection='3d') # Set up a three dimensional graphics window 

    # This strips out units if necessary
    if hasattr(Xgrid,'units'):
        Xgridplot = Xgrid.magnitude
    else:
        Xgridplot = Xgrid
        
    if hasattr(Ygrid,'units'):
        Ygridplot = Ygrid.magnitude
    else:
        Ygridplot = Ygrid
        
    if hasattr(Zgrid,'units'):
        Zgridplot = Zgrid.magnitude
    else:
        Zgridplot = Zgrid
        
    # Now plot
    ax.plot_surface(Xgridplot, Ygridplot, Zgridplot, color=color)
    
    # Now return the handle
    return ax

def dF_dx(statespace,Fgrid):
    # Returns the partial of F with respect to x (axis 0) holding y (axis 1) constant
    xgrid = statespace[0]
    ygrid = statespace[1]
    dF = np.diff(Fgrid,axis=0)
    dx = np.diff(xgrid,axis=0)
    dF_dx = dF/dx
    print('Shape of partial derivative =', np.shape(dF_dx))
    try:
        dF_dx *= Fgrid.units/xgrid.units
        print('Units of partial derivative =', dF_dx.units)
    except:
        print('No units')
    xgridnew = xgrid[1:,:]
    ygridnew = ygrid[1:,:]
    return xgridnew, ygridnew, dF_dx

def dF_dy(statespace,Fgrid):
    # Returns the partial of F with respect to y (axis 1) holding x (axis 0) constant
    xgrid = statespace[0]
    ygrid = statespace[1]
    dF = np.diff(Fgrid,axis=1)
    dy = np.diff(ygrid,axis=1)
    dF_dy = dF/dy
    print('Shape of partial derivative =', np.shape(dF_dy))
    try:
        dF_dy *= Fgrid.units/ygrid.units
        print('Units of partial derivative =', dF_dy.units)
    except:
        print('No units')
    xgridnew = xgrid[:,1:]
    ygridnew = ygrid[:,1:]
    return xgridnew, ygridnew, dF_dy

def func_P_isotherm(V1,V2,n,R,T,AssignQuantity,P_units):
    # Defines an isothermal expansion/contraction function
    Varray = np.linspace(V1,V2)
    Varray = AssignQuantity(Varray,V1.units)
    Parray = n*R*T/Varray
    Parray.ito(P_units)
    return Varray, Parray

def func_P_adiabat(V1,V2,n,R,T1,C_V,AssignQuantity,P_units):
    # Defines an adiabatic expansion/contraction function
    V2array = np.linspace(V1,V2)
    V2array = AssignQuantity(V2array,V2.units)
    P1 = n*R*T1/V1
    nR_over_C_V = n*R/C_V
    P2array = P1*(V2array/V1)**(-nR_over_C_V-1)
    P2array.ito(P_units)
    return V2array, P2array

def CP_H2Ogas(T,AssignQuantity):
    """ www.engineeringtoolbox.com/water-vapor-d_979.html """
    m = AssignQuantity(0.0067,'J/mol/K^2')
    CP0 = AssignQuantity(33.58,'J/mol/K')
    T0 = AssignQuantity(300,'K')
    CP = CP0 + m*(T-T0)
    return CP

def CP_H2Oice(T,AssignQuantity):
    """ www.liquisearch.com/heat_capacity/table_of_specific_heat_capacities """
    CP = AssignQuantity(38.0,'J/mol/K')
    return CP

def CP_H2Oliq(T,AssignQuantity):
    """ https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Units=SI&Mask=2#Thermo-Condensed """
    A = AssignQuantity(-203.606,'J/mol/K')
    B = AssignQuantity(1523.290,'J/mol/K^2')
    C = AssignQuantity(-3196.413,'J/mol/K^3')
    D = AssignQuantity(2474.455,'J/mol/K^4')
    E = AssignQuantity(3.855326,'J/mol K')
    t = T/1000
    CP = A + B*t + C*t**2 + D*t**3 + E/t**2
    return CP



def Integrator(statespace,dF_dx,dF_dy,AssignQuantity,SState=[],Units=[],axis=0):
    """Integrates a differential equation of state to produce F(x,y)"""
    from scipy.interpolate import RectBivariateSpline
    xgrid = statespace[0]
    ygrid = statespace[1]
    xarray = xgrid[:,0]; dx = (xarray[1]-xarray[0]); #print('dx=',dx)
    yarray = ygrid[0,:]; dy = (yarray[1]-yarray[0]); #print('dy=',dy)
    Fgrid = np.zeros(np.shape(xgrid))
    
    # Branch according to which axis to integrate along first
    if axis==0:
        integral_along_x = np.cumsum(dF_dx[:,0])*dx
        for i in range(len(xarray)):
            integral_along_y = np.cumsum(dF_dy[i,:])*dy 
            integral_along_y += integral_along_x[i]
            Fgrid[i,:] = integral_along_y
    else:
        integral_along_y = np.cumsum(dF_dy[0,:])*dy
        for i in range(len(yarray)):
            integral_along_x = np.cumsum(dF_dx[:,i])*dx
            #print('!',integral_along_x.units)
            #print('!',integral_along_y.units)
            
            integral_along_x += integral_along_y[i]
            Fgrid[:,i] = integral_along_x
            
    # Assign units if desired
    if len(Units) != 0:
        print('Assigning units:', Units)
        Fgrid = AssignQuantity(Fgrid,Units)
    else:
        Fgrid = AssignQuantity(Fgrid,integral_along_y.units)
    
    # Apply an offset if desired
    if len(SState) != 0:
        SState_x = SState[0]
        SState_y = SState[1]
        SState_F = SState[2]
        Fgrid_interpolater = RectBivariateSpline(xgrid[:,0], ygrid[0,:], Fgrid)
        Fgrid_at_standard_state = Fgrid_interpolater(SState_x,SState_y)
        Fgrid_at_standard_state = AssignQuantity(Fgrid_at_standard_state,SState_F.units)
        Fgrid -= Fgrid_at_standard_state
        Fgrid += SState_F

    return(Fgrid)
   
def StateSpaceInterpolator(statespace,nxarray,nyarray,Fgrid,AssignQuantity=0):
    if type(AssignQuantity) == type:
        #print('I think it is a function')
        useAssignQuantity = True
    else:
        useAssignQuantity = False
    xgrid = statespace[0]
    ygrid = statespace[1]
    Fgrid_interpolater = RectBivariateSpline(xgrid[:,0], ygrid[0,:], Fgrid)
    if np.size(nxarray) == 1:
        nxarray = [nxarray]
        nyarray = [nyarray]
    result = []
    for i in range(len(nxarray)):
        result.append(Fgrid_interpolater(nxarray[i],nyarray[i]))
    result = np.squeeze(result)
    if useAssignQuantity:
        result = AssignQuantity(result,Fgrid.units)
    return np.squeeze(result)

def trapz(integrand,x,AssignQuantity=0):
    # Uses numpy's trapz, but with units
    try:
        integrand.units
        result = np.trapz(integrand.magnitude,x.magnitude)
        result = AssignQuantity(result,integrand.units*x.units)
        return result
    except:
        print('Integrating without units')
        result = np.trapz(integrand,x)
        return result
