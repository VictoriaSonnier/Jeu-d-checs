import pyxel
from pathlib import Path

TILE=16
SIDE = 8
BLACK=0
WHITE=7
PLACE=[k*16 for k in range(8)]

class Chessboard:
    def __init__(self): # constructeur
        pyxel.init(SIDE*TILE, SIDE*TILE, title="Echecs") #allume l'écran de jeu
        
        
        self.damier = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.damier.append((i, j))
        
        self.game_over = False
        self.winner = "BLANC" 
        
        pyxel.run(self.update, self.draw) #détecte echec et mat

    def display(self, color, pixels=None): #self indique que la fonction appartient la classe Chessboard().
        if pixels is None:
            pyxel.cls(color)
        else:
            for x, y in pixels:
                pyxel.rect(x * TILE, y * TILE, TILE, TILE, color)

    def update(self):
        # game over pour test
        if pyxel.btnp(pyxel.KEY_G):
            self.game_over = True
        
        # R pour rejouer
        if self.game_over and pyxel.btnp(pyxel.KEY_R):
            self.game_over = False
            

    def draw(self):
        self.display(BLACK) #trace d'abord le fond noir
        self.display(WHITE, self.damier) #damier blanc
        
        if self.game_over:
            pyxel.rect(1, 10, 38, 26, 6)
            pyxel.rectb(1, 10, 38, 26, 7)

            pyxel.text(12, 13, "GAME", 5) 
            pyxel.text(12, 20, "OVER", 5) 

            pyxel.text(2, 27, f"GAGNANT:{self.winner[0]}", 5)
Chessboard()


class Piece:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Pawn(Piece):
    def draw(self):
        pyxel.blt(self.x*SIDE,self.y*SIDE,0,0,0,16,16,0,0)

class Rook(Piece):
    def draw(self):
        pyxel.blt(self.x*SIDE,self.y*SIDE,0,16,0,16,16,0,0)

class Bishop(Piece):
    def draw(self):
        pyxel.blt(self.x*SIDE,self.y*SIDE,0,32,0,16,16,0,0)

class Knight(Piece):
    def draw(self):
        pyxel.blt(self.x*SIDE,self.y*SIDE,0,48,0,16,16,0,0)

class King(Piece):
    def draw(self):
        pyxel.blt(self.x*SIDE,self.y*SIDE,0,64,0,16,16,0,0)

class Queen(Piece):
    def draw(self):
        pyxel.blt(self.x*SIDE,self.y*SIDE,0,80,0,16,16,0,0)

class Game:
    def __init__(self):
        self.chessboard=Chessboard()
        self.pieces = [
            ( Pawn(1*TILE, k*TILE) for k in range(SIDE)),
            ( Pawn(7*TILE, k*TILE) for k in range(SIDE))
        ]

    def start(self):
        pyxel.run(self.update,self.draw)

    def update(self):
        pass

    def draw(self):
        self.chessboard.draw()
        for piece in self.pieces:
            piece.draw()


game = Game()
game.start()
pyxel.show()







