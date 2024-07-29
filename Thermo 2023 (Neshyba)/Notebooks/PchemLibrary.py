import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def Statespace(xspecs,yspecs):
    if hasattr(xspecs[0],'units'): x0 = xspecs[0].magnitude
    else: x0 = xspecs[0]
    if hasattr(xspecs[1],'units'): x1 = xspecs[1].magnitude
    else: x1 = xspecs[1]
    if hasattr(yspecs[0],'units'): y0 = yspecs[0].magnitude
    else: y0 = yspecs[0]
    if hasattr(yspecs[1],'units'): y1 = yspecs[1].magnitude
    else: y1 = yspecs[1]
               
    xarray = np.linspace(x0,x1,xspecs[2])
    yarray = np.linspace(y0,y1,yspecs[2])
    ygridtemp,xgridtemp = np.meshgrid(yarray,xarray)
    xgrid = xgridtemp
    ygrid = ygridtemp
    return xgrid, ygrid

def plot_surface(Xgrid_in, Ygrid_in, Zgrid_in, color='gray', overlay=False, ax=0):
    """
    This plot_surface will be deprecated after 2023, to be replaced by plot_surface1
    """
    
    # Creates a surface plot in the handle myax
    
    if overlay==False:
        fig = plt.figure() 
        ax = plt.axes(projection='3d')
#         ax = plt.figure().gca(projection='3d') # Set up a three dimensional graphics window 

    # This strips out units if necessary
    if hasattr(Xgrid_in,'units'):
        Xgrid = Xgrid_in.magnitude
    else:
        Xgrid = Xgrid_in
        
    if hasattr(Ygrid_in,'units'):
        Ygrid = Ygrid_in.magnitude
    else:
        Ygrid = Ygrid_in
        
    if hasattr(Zgrid_in,'units'):
        Zgrid = Zgrid_in.magnitude
    else:
        Zgrid = Zgrid_in
    
    # Check to see if this is a scalar
    if np.size(Zgrid) == 1:
        Zgrid = Zgrid*np.ones(np.shape(Xgrid))
    
    # Now plot
    ax.plot_surface(Xgrid, Ygrid, Zgrid, color=color)
    
    # Now return the handle
    return ax


def plot_surface1(Xgrid_in, Ygrid_in, Zgrid_in, color='gray', labellist=[], title=''):
    
    # Initiates a surface plot 
    fig = plt.figure() 
    ax = plt.axes(projection='3d')
    
    # This strips out units if necessary
    if hasattr(Xgrid_in,'units'):
        Xgrid = Xgrid_in.magnitude
    else:
        Xgrid = Xgrid_in
        
    if hasattr(Ygrid_in,'units'):
        Ygrid = Ygrid_in.magnitude
    else:
        Ygrid = Ygrid_in
        
    if hasattr(Zgrid_in,'units'):
        Zgrid = Zgrid_in.magnitude
    else:
        Zgrid = Zgrid_in

    # Now plot
    ax.plot_surface(Xgrid, Ygrid, Zgrid, color=color)

    if len(labellist) != 0:
        ax.set_xlabel(labellist[0])
        ax.set_ylabel(labellist[1])
        ax.set_zlabel(labellist[2])
        
    if title != '':
        ax.set_title(title)
    
    # Now return the handle
    return ax

def plot_surfaces(Xgrid_in, Ygrid_in, Zgridlist_in, colorlist=[], labellist=[], titlelist=[]):
    
    if len(colorlist) == 0:
        colorlist = ['greys','blues','greens','mint','reds']
    else:
        for i in range(len(colorlist)):
            if colorlist[i] == 'blue': colorlist[i]='blues'
            if colorlist[i] == 'green': colorlist[i]='greens'
            if colorlist[i] == 'red': colorlist[i]='reds'

    # This strips out units if necessary
    if hasattr(Xgrid_in,'units'):
        Xgrid = Xgrid_in.magnitude
    else:
        Xgrid = Xgrid_in
        
    if hasattr(Ygrid_in,'units'):
        Ygrid = Ygrid_in.magnitude
    else:
        Ygrid = Ygrid_in
        
    if hasattr(Zgridlist_in[0],'units'):
        Zgridlist = Zgridlist_in
        for i in range(len(Zgridlist)):
            Zgridlist[i] = Zgridlist_in[i].magnitude
    else:
        Zgridlist = Zgridlist_in
                
    # Moving on
    if len(Zgridlist) == 1:
        fig = go.Figure(data=[
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[0], colorscale=colorlist[0], showscale=False)])
                                             
    elif len(Zgridlist) == 2:
        fig = go.Figure(data=[
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[1], colorscale=colorlist[1], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[0], colorscale=colorlist[0], showscale=False)])
                                                 
    elif len(Zgridlist) == 3:
        fig = go.Figure(data=[
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[2], colorscale=colorlist[2], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[1], colorscale=colorlist[1], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[0], colorscale=colorlist[0], showscale=False)])
                                                 
    elif len(Zgridlist) == 4:
        fig = go.Figure(data=[
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[3], colorscale=colorlist[3], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[2], colorscale=colorlist[2], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[1], colorscale=colorlist[1], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[0], colorscale=colorlist[0], showscale=False)])
                                                 
    elif len(Zgridlist) == 5:
        fig = go.Figure(data=[
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[4], colorscale=colorlist[4], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[3], colorscale=colorlist[3], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[2], colorscale=colorlist[2], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[1], colorscale=colorlist[1], showscale=False),
            go.Surface(x=Xgrid,y=Ygrid,z=Zgridlist[0], colorscale=colorlist[0], showscale=False)])
                                                 
    else:
        print('From plot_multiple_surfaces: too many surfaces to overlap, sorry')
        return
    
    mytitlestring = ''
    if len(titlelist) != 0:
        for i in range(len(titlelist)):
            mytitlestring += titlelist[i]+'='+str(colorlist[i])+' '       
            
    if len(labellist) != 0 and len(titlelist) == 0:
        fig.update_layout(scene = dict(
                    xaxis_title=labellist[0],
                    yaxis_title=labellist[1],
                    zaxis_title=labellist[2]))
        
    elif len(labellist) != 0 and len(titlelist) != 0:
        fig.update_layout(scene = dict(
                    xaxis_title=labellist[0],
                    yaxis_title=labellist[1],
                    zaxis_title=labellist[2]),
                    title=mytitlestring)   
        
    elif len(labellist) == 0 and len(titlelist) != 0:
        fig.update_layout(
                    title=mytitlestring)   
     
    return fig

def dF_dx(statespace,Fgrid):
    # Returns the partial of F with respect to x (axis 0) holding y (axis 1) constant
    xgrid = statespace[0]
    ygrid = statespace[1]
    dF = np.diff(Fgrid.magnitude,axis=0)
    dx = np.diff(xgrid.magnitude,axis=0)
    dF_dx = dF/dx
    print('Shape of partial derivative =', np.shape(dF_dx))
    try:
        dF_dx *= Fgrid.units/xgrid.units
        # print('Units of partial derivative =', dF_dx.units)
    except:
        print('No units')
    xgridnew = xgrid[1:,:]
    ygridnew = ygrid[1:,:]
    return xgridnew, ygridnew, dF_dx

def dF_dy(statespace,Fgrid):
    # Returns the partial of F with respect to y (axis 1) holding x (axis 0) constant
    xgrid = statespace[0]
    ygrid = statespace[1]
    dF = np.diff(Fgrid.magnitude,axis=1)
    dy = np.diff(ygrid.magnitude,axis=1)
    dF_dy = dF/dy
    print('Shape of partial derivative =', np.shape(dF_dy))
    try:
        dF_dy *= Fgrid.units/ygrid.units
        #print('Units of partial derivative =', dF_dy.units)
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
    """
    Integrates a differential equation of state to produce F(x,y)
    Assumes quantities have units
    """
#     from scipy.interpolate import RectBivariateSpline
#     from scipy import interpolate
#     This used to be called Integrator_pint
    
    dF_dx_local = dF_dx.to_base_units(); #print('dF_dx.units', dF_dx_local.units)
    dF_dy_local = dF_dy.to_base_units(); #print('dF_dy.units', dF_dy_local.units)
    
    xgrid = statespace[0]
    xgrid_local = xgrid.to_base_units()    
    ygrid = statespace[1]
    ygrid_local = ygrid.to_base_units()
  
    dx = xgrid_local[1,0]-xgrid_local[0,0]
    dy = ygrid_local[0,1]-ygrid_local[0,0]
    
    nx,ny = np.shape(xgrid)
    Fgrid = np.zeros(np.shape(xgrid))
    
    # If we're getting scalars, convert them
    if np.size(dF_dx_local) == 1:
        dF_dx_local = dF_dx_local*np.ones(np.shape(xgrid_local))
    if np.size(dF_dy) == 1:
        dF_dy_local = dF_dy_local*np.ones(np.shape(xgrid_local))
    
    # Branch according to which axis to integrate along first
    if axis==0:
        integral_along_x = np.cumsum(dF_dx_local[:,0])*dx
        for i in range(nx):
            integral_along_y = np.cumsum(dF_dy_local[i,:])*dy 
            integral_along_y += integral_along_x[i]
            Fgrid[i,:] = integral_along_y.magnitude
    else:
        integral_along_y = np.cumsum(dF_dy_local[0,:])*dy
        for i in range(ny):
            integral_along_x = np.cumsum(dF_dx_local[:,i])*dx
            integral_along_x += integral_along_y[i]
            Fgrid[:,i] = integral_along_x.magnitude
            
    # Apply an offset if desired
    debugging = False
    Fgrid = AssignQuantity(Fgrid,dF_dx_local.units*dx.units)
    if debugging: print('Fgrid.units:', Fgrid.units)
    if len(SState) != 0:
        SState_x = SState[0]; SState_x.ito_base_units()
        if debugging: print('SState_x:', SState_x)
        SState_y = SState[1]; SState_y.ito_base_units()
        if debugging: print('SState_y:', SState_y)
        SState_F = SState[2]; SState_F.ito_base_units()
        if debugging: print('SState_F:', SState_F)
        if debugging: print('Origin', xgrid[0,0],ygrid[0,0])
        if debugging: print('Standard states', SState_x,SState_y)
        
        # This shouldn't have to be done, but I can't get the interpolator to work properly
        ix_SS = nx-1 # Just a starting guess, it'll get over-ridden below
        last_deviation = (xgrid[ix_SS,0] - SState_x)**2
        for ix in range(nx):
            deviation = (xgrid[ix,0] - SState_x)**2
            if (deviation < last_deviation):
                last_deviation = deviation
                ix_SS = ix
        iy_SS = ny-1 # Just a starting guess, it'll get over-ridden below
        last_deviation = (ygrid[0,iy_SS] - SState_y)**2
        for iy in range(ny):
            deviation = (ygrid[0,iy] - SState_y)**2
            if (deviation < last_deviation):
                last_deviation = deviation
                iy_SS = iy

        # Find the value to be subtracted away
        Original_Fgrid_at_standard_state = np.squeeze(Fgrid[ix_SS,iy_SS])
        if debugging: print('Indices closest to standard state', ix_SS, iy_SS)
        if debugging: print('Original Fgrid at standard state', Original_Fgrid_at_standard_state)
 
        # Create the new Fgrid
        new_Fgrid = Fgrid -Original_Fgrid_at_standard_state +SState_F

    if len(Units) != 0:
        new_Fgrid.ito(Units)
    
    return(new_Fgrid)


def Integrator_old(statespace,dF_dx,dF_dy,AssignQuantity,SState=[],Units=[],axis=0):
    """
    Integrates a differential equation of state to produce F(x,y)
    """
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

# These (drawbox_xx and plot3d) are from Chem 341; plot3d should be replaced by plot_surface1
    
# Draw the box (clumsily)
from itertools import product, combinations
def drawbox_xx(xinit,xfinal,y,z,fig=[]):
    if np.size(fig) == 0:
        fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_box_aspect(aspect = (xinit,y,z))
    rext = xfinal/xinit
    r = [0, 1]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            ax.plot3D(*zip(s, e), color="b")
    ax.plot3D([1.0, rext],[0, 0],[0, 0],color='g')
    ax.plot3D([1.0, rext],[1, 1],[1, 1],color='g')
    ax.plot3D([1.0, rext],[0, 0],[1, 1],color='g')
    ax.plot3D([1.0, rext],[1, 1],[0, 0],color='g')
    ax.plot3D([rext, rext],[0, 1],[0, 0],color='g')
    ax.plot3D([rext, rext],[0, 0],[0, 1],color='g')
    ax.plot3D([rext, rext],[0, 1],[1, 1],color='g')
    ax.plot3D([rext, rext],[1, 1],[0, 1],color='g')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    return fig

# Plotting in 3d
def plot3d(xgrid,ygrid,zgrid,xaxis_title='x',yaxis_title='y',zaxis_title='z'):
    fig = go.Figure(data=go.Surface(x=xgrid,y=ygrid,z=zgrid))
    fig.update_layout(scene = dict(
                    xaxis_title=xaxis_title,
                    yaxis_title=yaxis_title,
                    zaxis_title=zaxis_title))
    fig.show()
    
def f_sigmoid(f1, f2, T, AssignQuantity, T_interval_magnitude=3, T_transition_magnitude=0):
    if T_transition_magnitude == 0:
        T1 = np.max(T)
        T2 = np.min(T)
        Tmid = (T2+T1)/2
        T_transition = AssignQuantity(Tmid,'K')
    else:
        T_transition = AssignQuantity(T_transition_magnitude,'K')
    T_interval = AssignQuantity(T_interval_magnitude,'K')
    sigmoid_arg = (T-T_transition)/T_interval
    sigmoid = 1 - 1.0/(1.0 + np.exp(-sigmoid_arg))
    sigmoid_min = sigmoid[0,0]; #print(sigmoid_min)
    sigmoid_max = sigmoid[-1,0]; #print(sigmoid_max)
    f = (sigmoid-sigmoid_min)*(f2-f1)/(sigmoid_max-sigmoid_min)+f1
    return f