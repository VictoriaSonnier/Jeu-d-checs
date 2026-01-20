import pyxel
from pathlib import Path
WIDTH=30
HEIGHT=30
BLACK=0
WHITE=7
def display(color,pixels=None):
    if pixels is None:
        pyxel.cls(color)

    else:
        for x,y in pixels:
            pyxel.pset(x,y, color)
def draw_maze(maze):
    display(BLACK)
    display(WHITE,random_maze)
pyxel.init(WIDTH,HEIGHT)
draw_maze(random_maze)
pyxel.show()