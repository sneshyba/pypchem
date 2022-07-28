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