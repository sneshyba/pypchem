import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

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
    wavefunctionscale = vertical_scale/5
    for i in np.arange(n-1,-1,-1):
        color=mpl.cm.jet_r((i)/(float)(n-1),1)
        plt.plot(xvec,psi[:,i]*wavefunctionscale+Epsi[i].magnitude,c=color)
        thislabel = 'n='+str(i+1)+', E={}'.format(np.round(Epsi[i]*1000)/1000.0)
        ax.axhline(y=Epsi[i].magnitude,xmin=xmin,xmax=xmax,c=color,ls='--',label=thislabel)
        
    # Labels and legend
    plt.xlabel(label+' ('+str(xvec_in.units)+')')
    plt.ylabel('Energy (hartree)')
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