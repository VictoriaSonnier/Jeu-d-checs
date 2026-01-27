import pyxel
import random
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
class Valid:
    def __init__(self):
        self.moves = [] 

    def clear(self):
        self.moves = []

    def add(self, x, y):
        self.moves.append((x, y))

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
        
    def valid_moves(self, pieces):
        moves = []
        direction = -1 if self.is_bottom_player else 1
        nx, ny = self.x, self.y + direction

    
        if 0 <= ny <= 7:
            # Avancer
            if not any(p.x == nx and p.y == ny for p in pieces):
                moves.append((nx, ny))
            # Captures
            for dx in [-1, 1]:
                if 0 <= nx + dx <= 7:
                    target = next((p for p in pieces if p.x == nx + dx and p.y == ny), None)
                    if target and target.is_bottom_player != self.is_bottom_player:
                        moves.append((nx + dx, ny))
        return moves
    
class Rook(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 16, bot)

    def valid_moves(self, pieces):
        moves = []

        dirs = [(1,0), (-1,0), (0,1), (0,-1)]

        for dx, dy in dirs:
            x, y = self.x, self.y
            while True:
                x += dx
                y += dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                blocker = next((p for p in pieces if p.x == x and p.y == y), None)
                if blocker:
                    if blocker.is_bottom_player != self.is_bottom_player:
                        moves.append((x, y)) 
                    break
                moves.append((x, y))

        return moves

    

class Knight(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 48, bot)

    def valid_moves(self, pieces):
        moves = []
        jumps = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]

        for dx, dy in jumps:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                blocker = next((p for p in pieces if p.x == x and p.y == y), None)
                if not blocker or blocker.is_bottom_player != self.is_bottom_player:
                    moves.append((x, y))

        return moves

    
class Bishop(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 32, bot)
    
    def valid_moves(self, pieces):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            x, y = self.x, self.y
            while True:
                x += dx
                y += dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                cible = next((p for p in pieces if p.x == x and p.y == y), None)
                if cible:
                    if cible.is_bottom_player != self.is_bottom_player:
                        moves.append((x, y))
                    break
                moves.append((x, y))

        return moves

class Queen(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 80, bot)
    
    def valid_moves(self, pieces):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            x, y = self.x, self.y
            while True:
                x += dx
                y += dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                cible = next((p for p in pieces if p.x == x and p.y == y), None)
                if cible:
                    if cible.is_bottom_player != self.is_bottom_player:
                        moves.append((x, y))
                    break
                moves.append((x, y))

        return moves

class King(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 64, bot)

    def valid_moves(self, pieces):
        moves = []
        dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

        for dx, dy in dirs:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                blocker = next((p for p in pieces if p.x == x and p.y == y), None)
                if not blocker or blocker.is_bottom_player != self.is_bottom_player:
                    moves.append((x, y))

        return moves



class Game:
    def __init__(self):
        self.turn=1 # Ajout de la gestion du tour
        pyxel.init(SIDE * TILE, SIDE * TILE, title="Echecs")
        try:
            pyxel.load("res.pyxres")
        except:
            pass

        self.chessboard = Chessboard()
        self.pieces = []
        self.valid = Valid()
        self.selected_piece = None

        self.pieces += [Pawn(i, 1) for i in range(SIDE)]
        self.pieces += [
            Rook(0, 0), Knight(1, 0), Bishop(2, 0), Queen(3, 0),
            King(4, 0), Bishop(5, 0), Knight(6, 0), Rook(7, 0)
        ]

        self.pieces += [Pawn(i, 6, True) for i in range(SIDE)]
        self.pieces += [
            Rook(0, 7, True), Knight(2, 7, True), Bishop(1, 7, True), Queen(3, 7, True),
            King(4, 7, True), Bishop(6, 7, True), Knight(5, 7, True), Rook(7, 7, True)
        ]
        pyxel.mouse(visible=True)
        self.p=None

    def start(self):
        pyxel.run(self.update, self.draw)
    
    def is_occupied(self,x,y):
        for p in self.pieces:
            if p.x==x and p.y==y:
                return p
        return None
    def attaque(self,piece,pieces):
        for p in pieces:
            if p.is_bottom_player!=piece.is_bottom_player:
                if (piece.x,piece.y) in  p.valid_moves(pieces):
                    return True
        return False
    def echec_et_mat(self,pieces,bot):
        for p in pieces:
            if p.is_bottom_player==bot:
                old_x=p.x
                old_y=p.y
                for dx,dy in p.valid_moves(pieces):
                    p.x=dx
                    p.y=dy
                    for p1 in pieces:
                        if isinstance(p1, King) and p1.is_bottom_player == bot:
                            roi=p1
                    if not self.attaque(roi, pieces):
                        return False       
                    else:
                        p.x=old_x
                        p.y=old_y
        print("Perdu")
        return True                   

                    



    def update(self):
        if self.turn == 1:
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                x = pyxel.mouse_x // TILE
                y = pyxel.mouse_y // TILE

                if self.p is None:
                    temp_p = self.is_occupied(x, y)
                    if temp_p and temp_p.is_bottom_player:
                        self.p = temp_p
                        self.valid.moves = self.p.valid_moves(self.pieces)
                else:
                    if (x, y) in self.valid.moves:
                        self.execute_move(self.p, x, y)
                    self.p = None
                    self.valid.clear()

       #IA
        elif self.turn == 0:
            
            self.ia_move()

    def execute_move(self, piece, x, y):
    
        old_x, old_y = piece.x, piece.y
        target = self.is_occupied(x, y)
        
        
        if target:
            self.pieces.remove(target)
        piece.x = x
        piece.y = y
        

        en_echec = False
        
        for p in self.pieces:
            if isinstance(p, King) and p.is_bottom_player == piece.is_bottom_player:
                if self.attaque(p, self.pieces):
                    en_echec = True
                    break
        
       
        if en_echec:
            
            piece.x, piece.y = old_x, old_y
            if target:
                self.pieces.append(target)
            return 
        else:
           
            self.turn = 1 - self.turn
            return True 

    def ia_move(self):
    
        ia_pieces = [p for p in self.pieces if not p.is_bottom_player]
        random.shuffle(ia_pieces) # Mélange pour ne pas toujours tester les mêmes

        for p in ia_pieces:
            moves = p.valid_moves(self.pieces)
            if moves:
                # Si la pièce a des coups possibles on en choisit un au hasard
                dest_x, dest_y = random.choice(moves)
                self.execute_move(p, dest_x, dest_y)
                return 

    def draw(self):
        self.chessboard.draw()
        
       
        pyxel.rect(0, 0, 50, 10, 0) 
        pyxel.rectb(0, 0, 50, 10, 7) 

   
        texte = "TOUR: BLANC" if self.turn == 1 else "TOUR: NOIR"
        couleur = 7 if self.turn == 1 else 13
        pyxel.text(5, 3, texte, couleur)

        for mx, my in self.valid.moves:
            pyxel.circ(mx * TILE + 8, my * TILE + 8, 2, 11)

        for piece in self.pieces:
            piece.draw()


game = Game()
game.start()