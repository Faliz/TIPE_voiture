import math
import cmath
import numpy as np
import matplotlib.pyplot as plt

def pos_suivante(v0,pos0,dtheta,N=5,PLOT=False):
    #N PAIR ou pas...
    #dtheta=-dtheta
    x_mil,y_mil=pos0.real,pos0.imag
    L=[]
    plotx=[pos0.real]
    ploty=[pos0.imag]
    for i in range(1,int(N/2)+1):
        x_mil+=abs(v0)*math.cos(cmath.phase(v0)-i*math.radians(dtheta))
        y_mil+=abs(v0)*math.sin(cmath.phase(v0)-i*math.radians(dtheta))
        if PLOT:
            plotx.append(x_mil)
            ploty.append(y_mil)
        
        
        
    x_mil1=x_mil+abs(v0)*math.cos(cmath.phase(v0)-(int(N/2)+1)*math.radians(dtheta))
    y_mil1=y_mil+abs(v0)*math.sin(cmath.phase(v0)-(int(N/2)+1)*math.radians(dtheta))
    
    v1=complex(x_mil1-x_mil,y_mil1-y_mil)
        
    x_fin=x_mil1
    y_fin=y_mil1
        
    for i in range(int(N/2)+2,N+1):
        x_fin+=abs(v0)*math.cos(cmath.phase(v0)-i*math.radians(dtheta))
        y_fin+=abs(v0)*math.sin(cmath.phase(v0)-i*math.radians(dtheta))
        
        if PLOT:
            plotx.append(x_fin)
            ploty.append(y_fin)

    pos_mil=complex(x_mil,y_mil)
    pos_fin=complex(x_fin,y_fin)

    if PLOT:
        plt.plot(plotx,ploty)
        plt.show()

    return pos_mil,pos_fin,v1
    
def list_pos(v0,pos0,theta_max=10,circuit=None):
    theta=np.linspace(-theta_max,theta_max,5)
    L=[]
    
    for i in range(len(theta)):
        
        L.append([])
        
    for i in range(len(theta)):
        
        pos_mil,pos_fin,v1=pos_suivante(v0,pos0,theta[i],PLOT=True)
        L[i].append(pos_mil)
        L[i].append(pos_fin)
        L[i].append(v1)
        
    return L
    
L=list_pos(complex(1,1),complex(0,0))

plt.scatter([L[-1][0].real],[L[-1][0].imag])

L1=list_pos(L[-1][-1],L[-1][0])