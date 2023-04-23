import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from sympy import lambdify
from sympy import Symbol
from sympy.physics.hydrogen import Psi_nlm
import plotly.graph_objects as go
from sympy import pprint as pprint


def plotter(Epsi,psi,xvec_in,V,n, label='x'):

    # Extracting W
    xvec = xvec_in.magnitude
    xmin = xvec[0]
    xmax = xvec[-1]
    
    # Offsetting and scaling for the wave functions
    ytop = Epsi[n].magnitude
    ybot = np.min(np.diag(V.magnitude))
    vertical_scale = ytop-ybot
    extra_space = vertical_scale*.1
    ybot -= extra_space

    # Create the figure
    f=plt.figure()
    ax=f.add_subplot(111)
   
    # Set limits
    plt.xlim(xvec[0],xvec[-1])
    plt.ylim(ybot,ytop)
    
    # Plot the wave functions
    wavefunctionscale = vertical_scale/4
    for i in np.arange(n-1,-1,-1):
        color=mpl.cm.jet_r((i)/(float)(n-1),1)
        plt.plot(xvec,psi[:,i]*wavefunctionscale+Epsi[i].magnitude,c=color)
        thislabel = 'n='+str(i+1)+', E={}'.format(np.round(Epsi[i].magnitude*10000)/10000.0)
        plt.plot([xmin,xmax],[Epsi[i].magnitude, Epsi[i].magnitude],c=color,ls='--',label=thislabel)
        #ax.axhline(y=Epsi[i].magnitude,xmin=xmin,xmax=1,c=color,ls='--',label=thislabel)
        
    # Labels and legend
    plt.xlabel(label+' ('+str(xvec_in.units)+')')
    plt.ylabel('Energy ('+str(Epsi[i].units)+')')
    L=plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)
    box=ax.get_position()
    ax.set_position([box.x0,box.y0,0.7*box.width,box.height])
    
    # Potential too
    Varray = np.diag(V.magnitude)
    plt.plot(xvec,Varray,color='gray',linewidth=4)
    plt.grid(True)

def flat_potential(xvec, V0=0, graphit=False):
    """Creates a flat surface with value V0
    The surface is returned in the form of a diagonal matrix whose dimensions match xvec""" 
    nsteps = len(xvec)
    Varray = np.ones(nsteps)*V0
    if graphit:
        f = plt.figure()
        ax=f.add_subplot(111)
        plt.plot(xvec,Varray,label='Potential',color='gray',linewidth=4)
        plt.xlabel('x')
        plt.ylabel('potential energy')
        L=plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)
        box=ax.get_position()
        ax.set_position([box.x0,box.y0,0.7*box.width,box.height])
        plt.grid(True)
    V = np.diag(Varray)
    return V

def sloped_potential(xvec, V1=0, V2=1, graphit=False):
    """Creates a sloped surface with values ranging from V1 to V2
    The surface is returned in the form of a diagonal matrix whose dimensions match xvec""" 
    nsteps = len(xvec)
    xarray = (xvec-xvec[0])/(xvec[-1]-xvec[0])
    xarray = xarray.magnitude
    Varray = V1 + (V2-V1)*xarray
    if graphit:
        f = plt.figure()
        ax=f.add_subplot(111)
        plt.plot(xvec,Varray,label='Potential',color='gray',linewidth=4)
        plt.xlabel('x')
        plt.ylabel('potential energy')
        L=plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)
        box=ax.get_position()
        ax.set_position([box.x0,box.y0,0.7*box.width,box.height])
        plt.grid(True)
    V = np.diag(Varray)
    return V

def step_potential(xvec, xbump, Vleft, Vright, graphit=False):
    """Creates a surface that jumps from Vleft to Vright, at position xbump
    The surface is returned in the form of a diagonal matrix whose dimensions match xvec""" 
    nsteps = len(xvec)
    Varray = np.ones(nsteps)
    for i in range(nsteps):
        if xvec[i].magnitude < xbump:
            Varray[i] = Varray[i]*Vleft
        else:
            Varray[i] = Varray[i]*Vright
    if graphit:
        f = plt.figure()
        ax=f.add_subplot(111)
        plt.plot(xvec,Varray,label='Potential',color='gray',linewidth=4)
        plt.xlabel('x')
        plt.ylabel('potential energy')
        L=plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)
        box=ax.get_position()
        ax.set_position([box.x0,box.y0,0.7*box.width,box.height])
        plt.grid(True)
    V = np.diag(Varray)
    return V

def kron3(X,Y,Z):
    """Kronecker delta function for three spatial dimensions"""
    return np.kron(X,np.kron(Y,Z))

def meshgrid3d(x,y,z,reporting=False):
    """This is a more intuitive version of numpy's meshgrid in 3d)"""
    ygrid,xgrid,zgrid = np.meshgrid(y,x,z)
    
    if reporting:
        # Print slices
        print('Slicing through x:')
        print(xgrid[:,0,0])
        print(ygrid[:,0,0])
        print(zgrid[:,0,0])

        print('Slicing through y:')
        print(xgrid[0,:,0])
        print(ygrid[0,:,0])
        print(zgrid[0,:,0])

        print('Slicing through z:')
        print(xgrid[0,0,:])
        print(ygrid[0,0,:])
        print(zgrid[0,0,:])

    return xgrid,ygrid,zgrid

def getpsi(n,l,m,xgrid,ygrid,zgrid,Zeff,xshift=0):
    
    #print('xshift =', xshift)
    xgrid_shifted = xgrid-xshift
    rgrid = ((xgrid_shifted)**2+ygrid**2+zgrid**2)**.5; #print(np.shape(rgrid),np.size(rgrid))
    thetagrid = np.arccos(zgrid/rgrid); #print(np.shape(thetagrid),np.size(thetagrid))
    phigrid = np.arctan2(ygrid,xgrid-xshift); #print(np.shape(phigrid),np.size(phigrid))

    r=Symbol("r", positive=True)
    phi=Symbol("phi", real=True)
    theta=Symbol("theta", real=True)
    Z=Symbol("Z", positive=True, nonzero=True)

    psi_analytical = Psi_nlm(n,l,m, r, phi, theta, Z)
    pprint(psi_analytical)
    psi_numerical = lambdify([r,theta,phi,Z], psi_analytical, 'numpy')
    psi = psi_numerical(rgrid,thetagrid,phigrid,Zeff)
    return psi

def getnormalizedpsi(n,l,m,xgrid,ygrid,zgrid,Zeff,xshift=0):
    tolerance=0.01
    psi = getpsi(n,l,m,xgrid,ygrid,zgrid,Zeff,xshift)
    dv = (xgrid[1,0,0]-xgrid[0,0,0])*(ygrid[0,1,0]-ygrid[0,0,0])*(zgrid[0,0,1]-zgrid[0,0,0])
    psi2 = abs(psi)**2
    N = np.sum(psi2)*dv
    psi /= N
    return psi
    
def normalizer(psi,dv,tolerance=0.01):
    psi2 = abs(psi)**2
    N = (np.sum(psi2)*dv)**.5
    if (abs(N-1)<tolerance):
        print('Congratulations, that wave function was already normalized')
    else:
        print('Normalizing by ', N)
        psi /= N
    return psi

def visualize_in_3d(xgrid,ygrid,zgrid,psi,scale=0.12,method='go',symbolsize=10):

    if method == 'go':
        values = np.real(psi).flatten()
        isovalfactor = 0.4
        maxposval = np.max(values)*isovalfactor
        maxnegval = -np.max(-values)*isovalfactor
        fig = go.Figure(data=go.Isosurface(
        x=xgrid.flatten(),
        y=ygrid.flatten(),
        z=zgrid.flatten(),
        value=values,
        isomin=maxnegval,
        isomax=maxposval,
        caps=dict(x_show=False, y_show=False, z_show=False)
        ))
        fig.show()
    
    elif method == 'matplotlib':
        fig = plt.figure('2,1,1')
        ax = fig.add_subplot(projection='3d')
        ax.set_box_aspect(aspect = (aspect_ratio,1,1))
        ax.scatter(xgrid,ygrid,zgrid, s=np.abs(psi)*symbolsize, c=np.real(psi), vmin=-scale, vmax=scale, cmap="bwr_r")
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

# # Getting the grid in spherical polar coordinates
# rgrid = (xgrid**2+ygrid**2+zgrid**2)**.5; print(np.shape(rgrid),np.size(rgrid))
# thetagrid = np.arccos(zgrid/rgrid); print(np.shape(thetagrid),np.size(thetagrid))
# phigrid = np.arctan2(ygrid,xgrid); print(np.shape(phigrid),np.size(phigrid))

# # The code below is for testing purposes
# # Construct an LMO
# psi = psi_DMO1+psi_DMO2
# fig = plt.figure('LMO1')
# ax = fig.add_subplot(projection='3d')
# ax.set_box_aspect(aspect = (aspect_ratio,1,1))
# ax.scatter(xgrid,ygrid,zgrid, s=np.abs(psi)*symbolsize, c=np.real(psi), vmin=-scale, vmax=scale, cmap="bwr_r")
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# psi = normalizer(x,y,z,psi)
# psi_LMO1 = psi

# # Construct another LMO
# psi = psi_DMO1-psi_DMO2
# fig = plt.figure('LMO2')
# ax = fig.add_subplot(projection='3d')
# ax.set_box_aspect(aspect = (aspect_ratio,1,1))
# ax.scatter(xgrid,ygrid,zgrid, s=np.abs(psi)*symbolsize, c=np.real(psi), vmin=-scale, vmax=scale, cmap="bwr_r")
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# psi = normalizer(x,y,z,psi)
# psi_LMO1 = psi