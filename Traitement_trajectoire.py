import tkinter as tk
import math
import cmath
from PIL import ImageTk, Image
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from numpy import linspace

class Segment():
    
    def __init__(self, deb, fin):
        self.deb = deb
        self.fin = fin
        self.long = abs(fin-deb)
        if (deb.real-fin.real) != 0: self.coefdir = (deb.imag-fin.imag)/(deb.real-fin.real)
        else : self.coefdir = 99e99
        self.ordorig = deb.imag-self.coefdir*deb.real
        
    def milieu(self):
        return (self.deb + self.fin)/2
    
    def mediatrice(self):
        if self.coefdir != 0 : a = -1/self.coefdir
        else : a = 99e99
        b = self.milieu().imag-self.coefdir*self.milieu().real
        
        return Segment(self.milieu(), complex(0,b))
    
def lg_arc_de_courbure(deb,mil,fin):
    pos1 = deb
    pos2 = mil
    pos3 = fin
    
    posc, R = cercle_circ(deb, mil, fin)
    
    alpha = math.atan(Segment(pos1,posc).coefdir)-math.atan(Segment(pos3,posc).coefdir)
    
    return alpha*R

def intersect(seg1,seg2):
    if (seg2.coefdir-seg1.coefdir) != 0 : x = (seg1.ordorig-seg2.ordorig)/(seg2.coefdir-seg1.coefdir)
    else : x = 99e99
    y = seg1.coefdir*x + seg1.ordorig
    
    return complex(x,y)
    
def cercle_circ(pt1, pt2, pt3):
    seg_dist1 = Segment(pt1, pt2)    
    seg_dist2 = Segment(pt2, pt3)
    
    med1 = seg_dist1.mediatrice()
    med2 = seg_dist2.mediatrice()
    
    posc = intersect(med1,med2)
    seg_rayon = Segment(med1.deb,posc)
    
    return posc, seg_rayon.long

def dist_sur_circuit(pos0,poss, circuit):
    orig = pos0
    mil, nouv = poss
    
    #orig, mil, nouv = projection(orig, mil, nouv, circuit)
    
    dist_circuit = lg_arc_de_courbure(orig, mil, nouv)

    return dist_circuit
    
"""def projection(pt1,pt2,pt3, circuit, precision = 10):
    L = []
    for pt in [pt1,pt2,pt3]:
        preclong1 = 0
        preclong2 = 0
        bestseg = 0
        for th in linspace(0,math.pi,precision,endpoint=False):
            seg = Segment(pt, pt+complex(10,10*math.tan(th)))
            cross = cross_circuit(seg, circuit)
            if preclong1 < cross  and preclong1 < preclong2:
                break
            bestseg = seg
            preclong2 = preclong1
            preclong1 = cross
        L.append(bestseg.fin)
    return L

def cross_circuit(seg, circuit):
    print(' ')
    compt = 0
    pt = seg.deb
    x = seg.deb.real
    y = seg.deb.imag
    while circuit.getpixel((pt.real,pt.imag))[0] == 0:
        print(compt)
        print(pt.real,pt.imag)
        compt +=1
        if abs(seg.coefdir) <= 1:
            print('x')
            pt = complex(x+compt,(x+compt)*seg.coefdir)
        else:
            print('y')
            pt = complex((y+compt)/seg.coefdir,y+compt)
        print(pt.real,pt.imag)
        
    return compt"""
#______________________________________###############################################____________________________________________#
    
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
    
def list_pos(v0,pos0,theta_max=20,circuit=None):
    theta=linspace(-theta_max,theta_max,20)
    L=[]
    
    for i in range(len(theta)):
        
        L.append([])
        
    for i in range(len(theta)):
        
        pos_mil,pos_fin,v1=pos_suivante(v0,pos0,theta[i])
        L[i].append(pos_mil)
        L[i].append(pos_fin)
        L[i].append(v1)
        
    return L