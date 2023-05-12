#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:29:38 2023

@author: catalifo
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.patches import Polygon
import tkinter as tk

index = 0

def getEntry():
    global index   
    index += 1
    if index<=3: 
        val = e.get()
        values.append(val)
        print(values)
        e.delete(0,tk.END)    
        texte.set(variables[index])
        
    return values

R=200
alpha=m.pi/3

#  Données issuee du test
root = tk.Tk()
root.geometry('800x250')
variables = ['Entrez votre valeur de I (Interactions) : ','Entrez votre valeur de S (Structure) : ','Entrez votre valeur de P (Pouvoir) : ','CALCUL DE VOTRE PROFIL EN COURS... FERMER LA FENETRE']
values = []

texte = tk.StringVar()
texte.set(variables[0])
entry = tk.Label(root, textvariable = texte) 
entry.place(x = 30,y = 50)  
e = tk.Entry(root)
e.place(x =500, y=50)
sbmitbtn = tk.Button(root, text = "Submit",activebackground = "pink", activeforeground = "blue", command=getEntry)
sbmitbtn.place(x = 30, y = 90)

root.mainloop()

print(values)
I = float(values[0])
S = float(values[1])
P = float(values[2])
# I = float(input('Entrez votre valeur de I (Interactions) : '))
# S = float(input('Entrez votre valeur de S (Structure) : '))
# P = float(input('Entrez votre valeur de P (Pouvoir) : '))

#  Calcul de la position sur les axes
P1=(1.8265*m.log(S/P) + 4.8612)*R/10
P2=(1.8265*m.log(I/P) + 4.8612)*R/10

#  Calcul des coefficients des droites
a1=P1*m.sin(alpha)/(P1*m.cos(alpha)-R)
b1=P1*m.sin(alpha)-a1*P1*m.cos(alpha)
a2=-R*m.sin(alpha)/(P2-R*m.cos(alpha))
b2=R*P2*m.sin(alpha)/(P2-R*m.cos(alpha))

#  Coordonnées du point d'intersection
x=(b2-b1)/(a1-a2)
y=a1*x+b1
r=m.sqrt(x*x+y*y)
IM=m.sqrt((x-R)**2+y**2)
SM=m.sqrt((x-R*m.cos(alpha))**2+(y-R*m.sin(alpha))**2)
xp=(m.cos(alpha)*x+m.sin(alpha)*y)/(m.cos(alpha)+m.sin(alpha)*m.tan(alpha))
yp=m.tan(alpha)*xp
h1=m.sqrt((xp-x)**2+(yp-y)**2)
h=R*m.sqrt(3)/2
h3=h-h1-y

#  Emplacement du point dans le triangle
zone=0
if r<=R/3:
  zone=1
elif IM<=R/3:
  zone=2
elif SM<=R/3:
  zone=3


if zone==0 and y<=R/3*m.sin(alpha/2):
  zone=7
elif zone==0 and h1<=R/3*m.sin(alpha/2):
  zone =5
elif zone==0 and h3<=R/3*m.sin(alpha/2):
  zone=6
elif zone==0:
  zone=4


if zone==1:
  emplacement='Mandarinocrate'
elif zone==2:
  emplacement='Clanocrate'
elif zone==3:
  emplacement='Méritocrate'
elif zone==7:
  emplacement='Clientocrate'
elif zone==5:
  emplacement='Scientocrate'
elif zone==6:
  emplacement='Sociocrate'
else:
  emplacement='Heuristique'


#  Affichage résultat
print('Votre profil est ', emplacement)

# Figure résultat
ax1 = np.linspace(0,R,200)
ax2 = np.linspace(0,R*m.cos(alpha),100)
ax3 = np.linspace(R*m.cos(alpha),R,100)
cote1 = 0*ax1
cote2 = m.tan(alpha)*ax2
cote3 = m.sin(alpha)/(m.cos(alpha)-1)*ax3-R*m.sin(alpha)/(m.cos(alpha)-1)
fig=plt.figure()
geo = fig.add_subplot()

plt.plot(ax1,cote1,'k', linewidth=3.0)
plt.plot(ax2,cote2,'k', linewidth=3.0)
plt.plot(ax3,cote3,'k', linewidth=3.0)

sec1 = Wedge((0,0), R/3, 0, alpha*180/m.pi, color="gray")
sec2 = Wedge((R*m.cos(alpha),R*m.sin(alpha)), R/3, -2*alpha*180/m.pi, -alpha*180/m.pi, color="gray")
sec3 = Wedge((R,0), R/3, (m.pi-alpha)*180/m.pi, 180, color="gray")
geo.add_patch(sec1)
geo.add_patch(sec2)
geo.add_patch(sec3)

A=(R/3*m.cos(alpha/2),R/3*m.sin(alpha/2))
B=(R-R/3*m.cos(alpha/2),R/3*m.sin(alpha/2))
C=(R/2,h-R/3)
triangle = Polygon([A, B, C], color="0.8")
geo.add_patch(triangle)
plt.plot(x,y,'r.',markersize=20)
plt.title('Votre profile est '+emplacement,fontsize=20, color= 'red')
plt.grid(False)
plt.axis('off')
plt.show()
