import tkinter as tk
from cmath import *
from math import *
from PIL import ImageTk, Image
from tkinter import filedialog as dial
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from Animation import *
 
class Car():
    
    def __init__(self, pos0, v0):
        self.pos = pos0
        self.v = v0

class Circuit(tk.Toplevel):
    
    def __init__(self):
        plt.gca().invert_yaxis()
        self.plotx,self.ploty = [],[]
        
        tk.Toplevel.__init__(self)
        self.resizable(width="FALSE",height="FALSE")
        
        self.ButtonFrame = tk.Frame(self) # Pour les boutons
        
        self.circuit = tk.Canvas(self, width = 500, height = 300, bg="white") # Création du canvas où sera dessiné le circuit
        self.circuit.grid(row=0,column=0)
        self.ButtonFrame.grid(row=1,column=0)
        
        self.carIm = None
        self.circuitIm = None
        self.v0 = 4
        
        self.error = 1 # pour la modif de vtesse si sortie de circuit
        
        self.normvit = 4
        self.carsize = (26,19)
        
        self.defbuttons()
        
        self.compteur = 0
        
        self.mainloop()
        
    def defbuttons(self):
        # Boutons et textes d'informations
        self.importB = tk.Button(self.ButtonFrame, text='Importer un circuit', command=self.lecture_circuit)
        self.importB.grid(row=0,column=0)
        
        self.importT = tk.Label(self.ButtonFrame)
        self.importT.grid(row=0,column=1)
        
        self.bagnoleB = tk.Button(self.ButtonFrame, text="Voiture au point de départ", command=self.bagnole, state=tk.DISABLED)
        self.bagnoleB.grid(row=1,column=0, columnspan=2)
        
        self.animB = tk.Button(self.ButtonFrame, text="Next", command=self.animation, state=tk.DISABLED)
        self.animB.grid(row=2,column=0, columnspan=2)
        
        self.stopB = tk.Button(self.ButtonFrame, text="Stop et afficher le graphe", command=self.animation)
        self.stopB.grid(row=3, column=0, columnspan=2)
        
    def motion(self,event):
        # Fonction qui permet à l'utilisateur de déplacer la voiture
        x, y = event.x, event.y
        
        self.circuit.delete("car") # On efface la voiture
        
        self.circuit.create_image(x, y, image=self.carIm, anchor=tk.CENTER, tags = "car")
        
    def placer_voiture(self,event):
        # Fonction qui permet à l'utilisateur de fixer la position de la voiture
        x, y = event.x, event.y
        
        if self.circuitPic.getpixel((x,y))[0] == 0: # On ne place la voiture que sur le circuit (pixels noirs)
            self.circuit.unbind('<Motion>') # On désensibilise le canvas des évenements
            self.circuit.unbind('<ButtonRelease-1>')
            
            self.carpos0 = complex(x,y) # On enregistre la position initiale de la voiture
            
            self.circuit.bind('<Motion>', self.droitedep) # A présent on trace le vecteur vitesse initiale
            self.circuit.bind('<ButtonRelease-1>', self.create_car)
            
    def droitedep(self, event):
        # L'utilisateur crée le vecteur vitesse intial
        x, y = event.x, event.y
        vit = complex(x-self.carpos0.real, y-self.carpos0.imag)
        self.v0 = rect(self.normvit, phase(vit)) # On crée un vecteur qui a une norme normvit et qui pointe dans la bonne direction
        
        self.circuit.delete("v0") # On affiche le vecteur
        self.circuit.create_line(self.carpos0.real, self.carpos0.imag, self.carpos0.real + self.v0.real*10, self.carpos0.imag+self.v0.imag*10, fill="red", tags = "v0", arrow = "last")
        
        self.circuit.delete("car") 
        
        # On tourne la voiture
        carPicrot = Image.new("RGBA", (self.carsize[0],self.carsize[0]))
        im = self.carPic.convert('RGBA')
        rot = im.rotate(-degrees(phase(self.v0)), expand=True)
        carPicrot.paste(rot, ((self.carsize[0]-rot.size[0])//2, (self.carsize[0]-rot.size[1])//2), rot )
        self.carIm = ImageTk.PhotoImage(carPicrot)
        
        self.circuit.create_image(self.carpos0.real, self.carpos0.imag, image=self.carIm, anchor=tk.CENTER, tags = "car")
            
    def create_car(self, event):
        # On crée la voiture
        self.circuit.unbind('<Motion>') # On désensibilise le canvas des évenements
        self.circuit.unbind('<ButtonRelease-1>')
        
        self.car = Car(self.carpos0, self.v0)
        self.bagnoleB.config(state=tk.DISABLED)
        self.animB.config(state=tk.NORMAL)
        
    def bagnole(self):
        # Importation de la voiture
        self.circuit.delete("v0") # On efface les vecteurs vitesses (si c'est pas la première fois qu'on place la voiture
        
        self.carPic = Image.open("car.gif").resize((self.carsize[0],self.carsize[1]),Image.ANTIALIAS)
        self.carIm = ImageTk.PhotoImage(self.carPic) # Importation de l'image redimensionnée
            
        self.importB.config(state=tk.DISABLED) # On ne peut plus changer de circuit
            
        self.circuit.bind('<Motion>', self.motion) # On rend le canvas 'sensible' aux déplacements de souris
        self.circuit.bind('<ButtonRelease-1>', self.placer_voiture) # On rend le canvas 'sensible' aux clicks de souris
        
        
    def lecture_circuit(self):
        # On lit l'image
        file = dial.askopenfile(mode='r',filetypes=[('images JPG', '.jpg')])
        try:
            self.circuitPic = Image.open(file.name)
            self.circuitIm = ImageTk.PhotoImage(self.circuitPic)
            self.importT.config(text="Patientez...") # On avertit l'utilisateur que ça risque de prendre du temps...
            self.update()
            self.trace_circuit()
        except AttributeError:
            pass
        else:
            self.importT.config(text=file.name) # On avertit l'utilisateur que c'est bon en affichant le nom de l'image
        
    def trace_circuit(self):
        # Trace circuit sur canvas
        self.circuit.config(width=self.circuitIm.width(), height = self.circuitIm.height()) # On redimmensionne le canvas
        
        self.circuit.create_image(0, 0, image=self.circuitIm, anchor=tk.NW, tags ="circuit")
        
        self.bagnoleB.config(state=tk.NORMAL) # On peut à présent tracer la voiture
    
    def refresh(self):
        self.circuit.delete("car") 
        
        # On tourne la voiture
        carPicrot = Image.new("RGBA", (self.carsize[0],self.carsize[0]))
        im = self.carPic.convert('RGBA')
        rot = im.rotate(-degrees(phase(self.car.v)), expand=True)
        carPicrot.paste(rot, ((self.carsize[0]-rot.size[0])//2, (self.carsize[0]-rot.size[1])//2), rot )
        self.carIm = ImageTk.PhotoImage(carPicrot)
        
        self.circuit.create_image(self.car.pos.real, self.car.pos.imag, image=self.carIm, anchor=tk.CENTER, tags = "car")
        
        
    def animation(self):
        print(self.compteur)
        if self.compteur > 300:
            plt.show()
        self.compteur +=1
        self.circuit.delete("v0")
        animer(self)
        self.animB.config(state=tk.DISABLED)
        self.after(1,self.animation)
        
if __name__=='__main__':
    fen = Circuit()
