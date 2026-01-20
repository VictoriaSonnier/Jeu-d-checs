import pyxel
from pathlib import Path
WIDTH=40
HEIGHT=40
BLACK=0
WHITE=7
#o, crée le damier
damier=[]
for i in range(8):
    for j in range(8):
        if (i+j)%2==0:
            damier.append((i,j))

def display(color,pixels=None):
    if pixels is None:
        pyxel.cls(color)

    else:
        for x,y in pixels:
            for i in range(5):
                for j in range(5):
                    pyxel.pset(x*5+i,y*5+j, color)

def draw_damier(maze):
    display(BLACK)
    display(WHITE,damier)
#on trace le damier
pyxel.init(WIDTH,HEIGHT)
draw_damier(damier)
pyxel.show()