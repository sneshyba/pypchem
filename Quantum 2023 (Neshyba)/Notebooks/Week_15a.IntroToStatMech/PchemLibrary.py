import plotly.graph_objects as go
import numpy as np

# Defining the Statespace function
def Statespace(xspecs,yspecs):
    xarray = np.linspace(xspecs[0],xspecs[1],xspecs[2])
    yarray = np.linspace(yspecs[0],yspecs[1],yspecs[2])
    ygridtemp,xgridtemp = np.meshgrid(yarray,xarray)
    xgrid = xgridtemp
    ygrid = ygridtemp
    return xgrid, ygrid

# Plotting in 3d
def plot3d(xgrid,ygrid,zgrid,xaxis_title='x',yaxis_title='y',zaxis_title='z'):
    fig = go.Figure(data=go.Surface(x=xgrid,y=ygrid,z=zgrid))
    fig.update_layout(scene = dict(
                    xaxis_title=xaxis_title,
                    yaxis_title=yaxis_title,
                    zaxis_title=zaxis_title))
    fig.show()
    
