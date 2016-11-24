import tkinter as tk
import math
import cmath
from PIL import ImageTk, Image, ImageDraw
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from numpy import linspace
import copy

##CODE A MODIFIER POUR OPTI
def liste_bordure(liste1):
    point_bord = []
    liste=peinture_Lapin_malin(liste1)
    while liste != peinture_Lapin_malin(liste):
        liste = peinture_Lapin_malin(liste)
    for i in range(len(liste)):
        for j in range(len(liste[0])):
            if type(liste[i][j])==int:
                if liste[i][j]>=240:
                    liste[i][j] = "int"
    for i in range(1,len(liste)-1):
        for j in range(1,len(liste[0])-1):
            if type(liste[i][j])==int:
                voisinnage=voisin(liste,i,j)
                if "ext" in voisinnage:
                    b_ext.append((i,j))
                elif "int" in voisinnage:
                    point_bord.append((i,j))
    #for i in point_bord:
    #    plt.scatter(i[0],i[1],c="b")
    #print(point_bord)
    ext,inte,test=difference(point_bord)
    test = list(set(test))
    
    for i in test:
        plt.scatter(i[0],i[1],c="k")
    plt.show()
    return ext,inte
   
def difference(liste):
    inte, ext, test = [], [], []
    bool = True
    ext.append(liste[0])
    while bool:
        new_ext,test = cherche_voisin(ext,liste,test)
        if new_ext == ext:
            bool = False
        else:
            ext = new_ext
    for i in range(len(liste)):
        if liste[i] not in ext:
            inte.append(liste[i])
    return ext, inte, test
        
def cherche_voisin(ext,liste,bord_testes):
    for i in range(len(ext)):
        if ext[i] in bord_testes:
            pass
        else:
            #print(ext[i])
            bord_testes.append(ext[i])
            nord, sud, est, ouest = (ext[i][0]+1,ext[i][1]),(ext[i][0]-1,ext[i][1]),(ext[i][0],ext[i][1]+1),(ext[i][0],ext[i][1]-1)
            if nord in liste:
                ext.append(nord)
            if est in liste:
                ext.append(est)
            if sud in liste:
                ext.append(sud)
            if ouest in liste:
                ext.append(sud)
    ext_ordo = set(ext)
    ext_ordo = list(ext_ordo)
    return ext_ordo,bord_testes
    

def tracer_bordure(ext,inte):
    for pts in ext:
        plt.scatter(pts[0],pts[1],c="g")
    for pts in inte:
        plt.scatter(pts[0],pts[1],c="r")
    plt.show()
    
def voisin(l,x,y):
    return [l[x-1][y-1],l[x-1][y],l[x-1][y+1],l[x][y-1],l[x][y+1],l[x+1][y-1],l[x+1][y],l[x+1][y+1]]
    
def peinture_Lapin_malin(liste_ok):
    '''Fonction inspirée de la peinture de Lapin Malin niveau CP. https://www.youtube.com/watch?v=7ynFs8jDoqg&feature=youtu.be&t=1h37m24s
    Pour voir si on est à l'intérieur du circuit, ou à l'extérieur, on contamine la première case, et on regarde si dans ses voisins il y a une case contaminée "ext", si c'est le cas, elle devient aussi contaminée. Sinon deux cas de figure : soit la case est un morceau du circuit (comprendre un pixel "noir", alors dans ce cas pas touche; soit la case est "saine", alors elle devient une case "int". '''
    liste=copy.deepcopy(liste_ok)
    pos_ext_non_testees = [(1,1)]
    pos_ext_testees = []
    while len(pos_ext_non_testees) !=0:
        print(len(pos_ext_non_testees), len(pos_ext_testees))
        Pos_a_test = pos_ext_non_testees.pop(0)
        #print(pos_ext_non_testees,Pos_a_test)
        if not (Pos_a_test in pos_ext_testees):
            if Pos_a_test[0] == 0 or Pos_a_test[1] == 0 or Pos_a_test[0] == len(liste_ok[0]) or Pos_a_test[1] == len(liste_ok):
                pos_ext_testees.append(Pos_a_test)
            else:
                for i in range(-1,2):
                    for j in range(-1,2):
                        Pos_voisin = (Pos_a_test[0]+i,Pos_a_test[1]+j)
                        if Pos_voisin[0] == len(liste) or Pos_voisin[1] == len(liste[0]):
                            pos_ext_testees.append(Pos_voisin)
                        elif liste[Pos_voisin[0]][Pos_voisin[1]] > 0:
                            #A CHANGER POUR LES PIXELS
                            pos_ext_non_testees.append(Pos_voisin)
        pos_ext_testees.append(Pos_a_test)
        pos_ext_non_testees = list(set(pos_ext_non_testees))
    plt.show()
    return list(set(pos_ext_testees))


def inte_exte(circuit):
    ext = peinture_Lapin_malin(circuit)
    print(ext)
    for i in range(1,len(circuit)-1):
        for j in range(1,len(circuit[0])-1):
            if circuit[i][j] < 0:
                bool_ext = False
                vois = voisin(circuit,i,j)
                for V in vois:
                    if V in ext:
                        plt.scatter(i,j,c="g")
    plt.show()

    
    
def contour(liste):
    liste_m = copy.deepcopy(liste)
    L_indice, EXT, INT = [], [], []

    LENL,LENL0 = len(liste_m),len(liste_m[0])    
    print(LENL,LENL0)
    for i in range(LENL):
        L_indice.append([])
        for j in range(LENL0):
            L_indice[-1].append([])
    
    # Lecture horizontale d'abord
    
    for i in range(1,LENL-1):
        compteur = 0
        for j in range(1,LENL0-1):
            if liste_m[i][j] == 0:
                if (liste[i][j-1] > 0) or (liste[i][j+1] > 0):
                    if compteur%4==0 or compteur%4==3:
                        L_indice[i][j].append("ext")
                        compteur+=1
                    elif compteur%4 == 2 or compteur%4 == 1:
                        L_indice[i][j].append("int")
                        compteur+=1
            
    # Lecture verticale ensuite
    
    # for i in range(1,LENL0-1):
    #     compteur_V = 0
    #     for j in range(1,LENL-1):
    #         if liste[j][i] < 0:
    #             pass
    #         else:
    #             if compteur_V%4 == 0 or compteur_V%4 == 3:
    #                 if liste_m[j][i-1] < 0 or liste[j][i+1] < 0:
    #                     L_indice[j][i].append("ext")
    #                     compteur_V += 1
    #                 else:
    #                     L_indice[j][i].append("ext")
    #             else:
    #                 if liste_m[j][i-1] < 0 or liste[j][i+1] < 0:
    #                     L_indice[j][i].append("int")
    #                     compteur_V += 1
    #                 else:
    #                     L_indice[j][i].append("int")
                        
    img = Image.new('RGB',(LENL,LENL0),(255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(LENL):
        for j in range(LENL0):
            if "ext" in L_indice[i][j]:
                draw.point((i,j),fill="red")
            elif L_indice[i][j] == ["int"]:
                draw.point((i,j),fill="green")
    title = "Circuit_bords.png"
    img.save(title,"PNG")
    
    
    
    
        
if __name__ == '__main__':
   pass
    #plt.show()
    #print(L)
    
    
    
    