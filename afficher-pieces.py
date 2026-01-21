import pyxel

TILE = 16
SIDE = 8
BLACK = 0
WHITE = 7
CREME = 15

class Chessboard:
    def __init__(self):
        self.damier = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.damier.append((i, j))
        self.game_over = False
        self.winner = "BLANC"

    def update(self):
        if pyxel.btnp(pyxel.KEY_G):
            self.game_over = True
        if self.game_over and pyxel.btnp(pyxel.KEY_R):
            self.game_over = False

    def draw(self):
        pyxel.cls(BLACK)
        for x, y in self.damier:
            pyxel.rect(x * TILE, y * TILE, TILE, TILE, WHITE)
        if self.game_over:
            pyxel.rect(30, 50, 70, 30, 6)
            pyxel.rectb(30, 50, 70, 30, 7)
            pyxel.text(50, 55, "GAME OVER", 0)

class Piece:
    def __init__(self, x, y, u, bot=False):
        self.x = x
        self.y = y
        self.u = u
        self.v = 16 if bot else 0
        self.is_bottom_player = bot

    def draw(self):
        pyxel.blt(self.x * TILE, self.y * TILE, 0, self.u, self.v, 16, 16, 0)

class Pawn(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 0, bot)

class Rook(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 16, bot)

class Knight(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 32, bot)

class Bishop(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 48, bot)

class Queen(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 64, bot)

class King(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 80, bot)

class Game:
    def __init__(self):
        pyxel.init(SIDE * TILE, SIDE * TILE, title="Echecs")
        try:
            pyxel.load("res.pyxres")
        except:
            pass

        self.chessboard = Chessboard()
        self.pieces = []

        self.pieces += [Pawn(i, 1) for i in range(SIDE)]
        self.pieces += [
            Rook(0, 0), Knight(1, 0), Bishop(2, 0), Queen(3, 0),
            King(4, 0), Bishop(5, 0), Knight(6, 0), Rook(7, 0)
        ]

        self.pieces += [Pawn(i, 6, True) for i in range(SIDE)]
        self.pieces += [
            Rook(0, 7, True), Knight(1, 7, True), Bishop(2, 7, True), Queen(3, 7, True),
            King(4, 7, True), Bishop(5, 7, True), Knight(6, 7, True), Rook(7, 7, True)
        ]

    def start(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        self.chessboard.update()

    def draw(self):
        self.chessboard.draw()
        for piece in self.pieces:
            piece.draw()

game = Game()
game.start()
