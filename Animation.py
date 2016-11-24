import tkinter as tk
from cmath import *
from math import *
from PIL import ImageTk, Image
from tkinter import filedialog as dial
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import copy

from Traitement_trajectoire import *
 
class Car():
    
    def __init__(self, pos0, v0):
        self.pos = pos0
        self.v = v0

def animer(parent):
    pos_nvls = list_pos(parent.car.v,parent.car.pos)
    pos_nvls = tri_sur_circuit(pos_nvls,parent.circuitPic,parent)
    
    dists = []
    for pos in pos_nvls:
        dists.append(dist_sur_circuit(parent.car.pos, pos[:-1], parent.circuitPic))
        
    bestindex = indexmax(dists)
    
    try :
        parent.car = Car(pos_nvls[bestindex][0],pos_nvls[bestindex][-1])    
        parent.plotx.append(pos_nvls[bestindex][0].real)
        parent.ploty.append(pos_nvls[bestindex][0].imag)
        parent.car.v *= parent.error
        if parent.error==1:
            c="b"
        elif parent.error==2:
            c="g"
        elif parent.error==4:
            c="y"
        elif parent.error==8:
            c="orange"
        elif parent.error>=16:
            c="r"
        plt.plot([parent.plotx[-2],parent.plotx[-1]],[parent.ploty[-2],parent.ploty[-1]],color=c)
        parent.error = 1
       # parent.refresh()
    except IndexError:
        parent.error *= 2
        parent.car.v /= 2
    parent.refresh()

        
def tri_sur_circuit(L,circuit, parent):
    
    Lc = copy.deepcopy(L)
    for l in L:
        pos = l[1]
        try:
            if circuit.getpixel((pos.real,pos.imag))[0] != 0:
                Lc.remove(l)
        except IndexError:
            return []    
    return Lc
    
def indexmax(L):
    i = 0
    for k in range(len(L)):
        if L[k] < L[i]:
            i = k
    return i