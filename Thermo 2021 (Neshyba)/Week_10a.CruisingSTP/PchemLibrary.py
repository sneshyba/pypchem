import numpy as np

def Statespace(xspecs,yspecs):
    xarray = np.linspace(xspecs[0],xspecs[1],xspecs[2])
    yarray = np.linspace(yspecs[0],yspecs[1],yspecs[2])
    ygridtemp,xgridtemp = np.meshgrid(yarray,xarray)
    xgrid = xgridtemp
    ygrid = ygridtemp
    return xgrid, ygrid

def dF_dx(statespace,Fgrid):
    # Returns the partial of F with respect to x (axis 0) holding y (axis 1) constant
    xgrid = statespace[0]
    ygrid = statespace[1]
    dF = np.diff(Fgrid,axis=0)
    dx = np.diff(xgrid,axis=0)
    dF_dx = dF/dx
    print('Shape of partial derivative =', np.shape(dF_dx))
    try:
        print('Units of partial derivative =', dF_dx.units)
#         dF_dx *= Fgrid.units/xgrid.units
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
        print('Units of partial derivative =', dF_dy.units)
#         dF_dy *= Fgrid.units/ygrid.units
    except:
        print('No units')
    xgridnew = xgrid[:,1:]
    ygridnew = ygrid[:,1:]
    return xgridnew, ygridnew, dF_dy

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
    """ webbook.nist.gov """
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
    