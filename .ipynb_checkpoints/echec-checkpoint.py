import pyxel
from pathlib import Path
WIDTH=8
HEIGHT=8
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
            pyxel.pset(x,y, color)
def draw_damier(maze):
    display(BLACK)
    display(WHITE,damier)
#on trace le damier
pyxel.init(WIDTH,HEIGHT)
draw_damier(damier)
pyxel.show()