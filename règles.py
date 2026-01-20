import pyxel
from pathlib import Path

TILE=16
SIDE = 8
PLACE=[k*16 for k in range(8)]

class Chessboard:
    def __init__(self):
        pyxel.cls(0)
        for y in range(SIDE):
            for x in range(SIDE):
                if (x + y) % 2 == 0:
                    color = 7 
                else:
                    color = 5  
        px = x * TILE
        py = y * TILE
        pyxel.rect(px, py, TILE, TILE, color)
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
        pyxel.init(TILE*SIDE,TILE*SIDE,title='Echiquier')
        pyxel.load('res.pyxres')
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







