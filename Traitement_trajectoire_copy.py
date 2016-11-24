import tkinter as tk
from cmath import *
from math import *
from scipy.optimize import fsolve
from PIL import Image

class Segment():
    
    def __init__(self, deb, fin):
        self.deb = deb
        self.fin = fin
        self.long = abs(fin-deb)
        self.coefdir = (deb.imag-fin.imag)/(deb.real-fin.real)
        self.ordorig = deb.imag-self.coefdir*deb.real
        
    def milieu(self):
        return self.deb + self.coefdir*(self.long/2) + self.orig 
    
def lg_arc_de_courbure(deb,mil,fin,estimcentre):
    pos1 = deb
    pos2 = mil
    pos3 = fin
    
    def systeme(p):
        x0, y0, R = p
        c = complex(x0,y0)
        return (abs(pos1-c)-R, abs(pos2-c)-R ,abs(pos3-c)-R)
    
    xc, yc, R = fsolve(systeme, estimcentre)
    
    alpha = atan(Segment(pos1,complex(xc,yc)).coefdir)-atan(Segment(pos3,complex(xc,yc)).coefdir)
    
    return alpha*R

def intersect(seg1,seg2):
    x = (seg1.ordorig-seg2.ordorig)/(seg2.coefdir-seg1.coefdir)
    y = seg1.coefdir*x + seg1.ordorig
    
    return complex(x,y)
    
def trouve_seg(circuit,pt):
    pass

def dist_sur_circuit(circuit, posp, posmil, posn):
    orig = posp
    mil = posmil
    nouv = posn
    
    seg_dist = Segment(orig,nouv)
    seg_orig = trouve_seg(circuit,orig)
    seg_nouv = trouve_seg(circuit,nouv)
    seg_mil = trouve_seg(circuit,mil)
    estimcentrecplx = intersect(seg_orig, seg_nouv)
    estimcentre = (estimcentrecplx.real, estimcentrecplx.imag, abs(orig-estimcentrecplx))
    
    dist_circuit = lg_arc_de_courbure(seg_orig.fin, seg_mil.fin, seg_nouv.fin, estimcentre)
    return dist_circuit
    
    
    
    