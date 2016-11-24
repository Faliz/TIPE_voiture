from PIL import Image, ImageDraw
import time

test = 0 #Numéro du testeur, pour garder les autres tests sous la main.


def chercher_premier_pixel(liste,pixel=0):
    
    '''Cherche le premier pixel d'une liste rectangulaire composée de pixel "noirs" et "blancs" donc la couleur est proche du noir. On part du haut gauche de la liste.
    Revoie (NaN,Nan) s'il n'y a pas de pixel noir dans la liste.'''
    
    I,J = len(liste), len(liste[0])
    
    for i in range(I):
        for j in range(J):
            if (liste[i][j]==0):
                return [i,j]
    return [float('NaN'),float('NaN')]
    
def chercher_premier_pixel_deux(liste,ext,pixel=0):
    
    I,J = len(liste), len(liste[0])
    
    for i in range(I):
        for j in range(J):
            if (liste[i][j]==0):
                if ([i,j] in ext):
                    a=1
                else:
                    noir, blanc = False, False
                    V = voisin(liste,[i,j])
                    for k in range(len(V)):
                        if liste[V[k][0]][V[k][1]] == 0:
                            noir = True
                        if liste[V[k][0]][V[k][1]] == 255:
                            blanc = True
                    if noir and blanc:
                        return [i,j]
    return [float('NaN'),float('NaN')]    
    
    
if __name__ == "__main__" and test ==1 :
    l = [[255,255,255,255],[255,255,200,255],[255,220,220,255],[255,255,255,255]]
    print(chercher_premier_pixel(l))
    
    
def voisin(liste,coord):
    ''' Rend la liste du voisinage de liste[x][x]'''
    x,y=coord[0],coord[1]
    X,Y = len(liste)-1,len(liste[0])-1
    voisins = []
    for i in range(-1,2):
        if i==-1 and x>0:
            for j in range(-1,2):
                if j==-1 and y>0:
                    voisins.append([x+i,y+j])
                elif j==0:
                    voisins.append([x+i,y+j])
                elif j==1 and y<Y:
                    voisins.append([x+i,y+j])
        elif i==0:
            for j in range(-1,2,2):
                if j==-1 and y>0:
                    voisins.append([x+i,y+j])
                elif j==1 and y<Y:
                    voisins.append([x+i,y+j])
        elif i==1 and x<X:
            for j in range(-1,2):
                if j==-1 and y>0:
                    voisins.append([x+i,y+j])
                elif j==0:
                    voisins.append([x+i,y+j])
                elif j==1 and y<Y:
                    voisins.append([x+i,y+j])
    return voisins
    
if __name__ == "__main__" and test == 4:
    
    l = [[255,255,255,255,255,255],[255,255,0,0,0,255],[255,255,0,0,0,255],[255,255,0,0,0,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255]]
    print(voisin(l,[0,0]))
    print(voisin(l,[2,3]))
    print(voisin(l,[8,3]))
    
def regarde_voisin(liste,coord,pixel=0):
    
    '''On regarde le voisinnage d'un pixel et on rend ceux qui sont proches en couleur de la couleur cherchée.'''
    
    bons_voisins = []
    vois = voisin(liste,coord)
    #print(vois)
    for i in range(len(vois)):
        blanc,noir = False, False
        vois_vois = voisin(liste,[vois[i][0],vois[i][1]])
        
        for j in range(len(vois_vois)):
            if liste[vois_vois[j][0]][vois_vois[j][1]] < 25:
                noir = True
            if liste[vois_vois[j][0]][vois_vois[j][1]] > 225:
                blanc = True
        if blanc and noir:
            bons_voisins.append(vois[i])
    
    return bons_voisins
    
if __name__ == "__main__" and test == 2:
    
    l = [[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,2,2,2,255],[255,255,24,255,24,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255]]
    
    print(regarde_voisin(l,[2,2]))
    print(regarde_voisin(l,[0,0]))
    print(regarde_voisin([[0]],[1,1]))
        
        
def contour(liste):
    x,y = len(liste), len(liste[0])
    t1 = time.clock()
    img = Image.new('RGB',(x,y),(255,255,255))
    draw = ImageDraw.Draw(img)
    
    '''Donne la liste des points du contour extérieur de l'image.'''
    compteur = 0
    liste_points, points_deja_testes = [chercher_premier_pixel(liste)], []
    while len(liste_points)!=0:
        #print(len(liste_points),"|","1")
        point_a_test = liste_points.pop(0)
        if not(point_a_test in points_deja_testes):
            points_deja_testes.append(point_a_test)
            nouveaux_points = regarde_voisin(liste,point_a_test)            
            for PT in nouveaux_points:
                if not(PT in points_deja_testes):
                    liste_points.append(PT)
    for i in range(len(points_deja_testes)):
        draw.point((points_deja_testes[i][0],points_deja_testes[i][1]),fill = (255,0,0))
        #plt.scatter(points_deja_testes[i][0],points_deja_testes[i][1], c = "r")
    
    liste_points_deux, points_deja_testes_deux = [chercher_premier_pixel_deux(liste,points_deja_testes)], []
    while len(liste_points_deux)!=0:
        #print(len(liste_points_deux),"|","2")
        point_a_test2 = liste_points_deux.pop(0)
        if not(point_a_test2 in points_deja_testes_deux):
            points_deja_testes_deux.append(point_a_test2)
            nouveaux_points = regarde_voisin(liste,point_a_test2)            
            for PT in nouveaux_points:
                if not(PT in points_deja_testes):
                    liste_points_deux.append(PT)
                    
    for i in range(len(points_deja_testes_deux)):
        #print(points_deja_testes_deux)
        draw.point((points_deja_testes_deux[i][0],points_deja_testes_deux[i][1]),fill = (0,255,0))
        #plt.scatter(points_deja_testes_deux[i][0],points_deja_testes_deux[i][1], c = "g")
    img.show()
    img.save("bordures_circuit.png")
    t2 = time.clock()
    print("Le temps de calcul total est :",t2-t1)
    print("J'attends ton lapin magique, enculé!")
    #plt.show()
    
if __name__ == "__main__" and test == 3:
    
    l = [[255,255,255,255,255,255],[255,255,0,0,0,255],[255,255,0,0,0,255],[255,255,0,0,0,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255],[255,255,255,255,255,255]]
    print(contour(l))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    