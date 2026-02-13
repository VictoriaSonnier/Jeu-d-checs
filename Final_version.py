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
        # Touche G pour forcer un Game Over (test)
        if pyxel.btnp(pyxel.KEY_G):
            self.game_over = True
        # La touche R est gérée dans Game.update pour réinitialiser les pièces

    def draw(self):
        pyxel.cls(BLACK)
        for x, y in self.damier:
            pyxel.rect(x * TILE, y * TILE, TILE, TILE, WHITE)
        
        if self.game_over:
            pyxel.rect(30, 50, 70, 30, 6)
            pyxel.rectb(30, 50, 70, 30, 7)
            pyxel.text(50, 55, "GAME OVER", 0)
            if self.winner == "BLANC":
                pyxel.text(45, 65, "WINNER BLANC", 0)
            else:
                pyxel.text(45, 65, "WINNER NOIR", 0)
            pyxel.text(35, 75, "R POUR RECOMMENCER", 0)

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

    def valid_moves(self, pieces, game):
        moves = []
        start_row = 6 if self.is_bottom_player else 1
        direction = -1 if self.is_bottom_player else 1

        nx, ny = self.x, self.y + direction
        if 0 <= ny < 8 and not any(p.x == nx and p.y == ny for p in pieces):
            moves.append((nx, ny))
            if self.y == start_row:
                ny2 = self.y + 2 * direction
                if not any(p.x == nx and p.y == ny2 for p in pieces):
                    moves.append((nx, ny2))

        for dx in (-1, 1):
            nx, ny = self.x + dx, self.y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = next((p for p in pieces if p.x == nx and p.y == ny), None)
                if target and target.is_bottom_player != self.is_bottom_player:
                    moves.append((nx, ny))
                if game.en_passant == (nx, ny):
                    moves.append((nx, ny))
        return moves

class Rook(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 16, bot)

    def valid_moves(self, pieces, game):
        moves = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x, y = self.x, self.y
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < 8 and 0 <= y < 8): break
                blocker = next((p for p in pieces if p.x == x and p.y == y), None)
                if blocker:
                    if blocker.is_bottom_player != self.is_bottom_player: moves.append((x, y))
                    break
                moves.append((x, y))
        return moves

class Knight(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 48, bot)

    def valid_moves(self, pieces, game):
        moves = []
        for dx, dy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                blocker = next((p for p in pieces if p.x == x and p.y == y), None)
                if not blocker or blocker.is_bottom_player != self.is_bottom_player:
                    moves.append((x, y))
        return moves

class Bishop(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 32, bot)
    
    def valid_moves(self, pieces, game):
        moves = []
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            x, y = self.x, self.y
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < 8 and 0 <= y < 8): break
                cible = next((p for p in pieces if p.x == x and p.y == y), None)
                if cible:
                    if cible.is_bottom_player != self.is_bottom_player: moves.append((x, y))
                    break
                moves.append((x, y))
        return moves

class Queen(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 80, bot)
    
    def valid_moves(self, pieces, game):
        return Bishop.valid_moves(self, pieces, game) + Rook.valid_moves(self, pieces, game)

class King(Piece):
    def __init__(self, x, y, bot=False):
        super().__init__(x, y, 64, bot)

    def valid_moves(self, pieces, game):
        moves = []
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                blocker = next((p for p in pieces if p.x == x and p.y == y), None)
                if not blocker or blocker.is_bottom_player != self.is_bottom_player:
                    moves.append((x, y))
        return moves

class Game:
    def __init__(self):
        pyxel.init(SIDE * TILE, SIDE * TILE, title="Echecs")
        try: pyxel.load("res.pyxres")
        except: pass
        self.reset_game()
        pyxel.mouse(visible=True)
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.turn = 1 
        self.chessboard = Chessboard()
        self.pieces = []
        self.valid = Valid()
        self.p = None
        self.en_passant = None
        # Setup pieces
        self.pieces += [Pawn(i, 1) for i in range(SIDE)]
        self.pieces += [Rook(0,0), Knight(1,0), Bishop(2,0), Queen(3,0), King(4,0), Bishop(5,0), Knight(6,0), Rook(7,0)]
        self.pieces += [Pawn(i, 6, True) for i in range(SIDE)]
        self.pieces += [Rook(0,7, True), Knight(1,7, True), Bishop(2,7, True), Queen(3,7, True), King(4,7, True), Bishop(5,7, True), Knight(6,7, True), Rook(7,7, True)]

    def is_occupied(self, x, y):
        return next((p for p in self.pieces if p.x == x and p.y == y), None)

    def attaque(self, p, pieces):
        for p1 in pieces:
            if p1.is_bottom_player != p.is_bottom_player:
                if (p.x, p.y) in p1.valid_moves(pieces, self):
                    return True
        return False

    def is_square_attacked(self, x, y, attacker_is_bottom):
        for p in self.pieces:
            if p.is_bottom_player == attacker_is_bottom:
                if (x, y) in p.valid_moves(self.pieces, self):
                    return True
        return False

    def echec_et_mat(self, joueur_is_bottom):
        pieces_joueur = [p for p in self.pieces if p.is_bottom_player == joueur_is_bottom]
        for p in pieces_joueur:
            moves = p.valid_moves(self.pieces, self)
            old_x, old_y = p.x, p.y
            for dx, dy in moves:
                target = self.is_occupied(dx, dy)
                if target: self.pieces.remove(target)
                p.x, p.y = dx, dy
                
                roi = next(p1 for p1 in self.pieces if isinstance(p1, King) and p1.is_bottom_player == joueur_is_bottom)
                en_danger = self.attaque(roi, self.pieces)
                
                p.x, p.y = old_x, old_y
                if target: self.pieces.append(target)
                if not en_danger: return False
        return True

    def execute_move(self, p, x, y):
        old_x, old_y = p.x, p.y
        target = self.is_occupied(x, y)
        
        # En passant capture
        if isinstance(p, Pawn) and self.en_passant == (x, y):
            cap_y = y + 1 if p.is_bottom_player else -1
            victim = self.is_occupied(x, cap_y)
            if victim: self.pieces.remove(victim)

        if target: self.pieces.remove(target)
        p.x, p.y = x, y

        # En passant update
        if isinstance(p, Pawn) and abs(p.y - old_y) == 2:
            self.en_passant = (p.x, (p.y + old_y) // 2)
        else:
            self.en_passant = None

        # Promotion
        promo_row = 0 if p.is_bottom_player else 7
        if isinstance(p, Pawn) and p.y == promo_row:
            self.pieces.remove(p)
            self.pieces.append(Queen(p.x, p.y, p.is_bottom_player))

        # Check if move leaves king in check
        roi_local = next(k for k in self.pieces if isinstance(k, King) and k.is_bottom_player == p.is_bottom_player)
        if self.attaque(roi_local, self.pieces):
            p.x, p.y = old_x, old_y
            if target: self.pieces.append(target)
            return False

        self.turn = 1 - self.turn
        if self.echec_et_mat(self.turn == 1):
            self.chessboard.game_over = True
            self.chessboard.winner = "BLANC" if self.turn == 0 else "NOIR"
        return True

    def update(self):
        self.chessboard.update()
        if self.chessboard.game_over:
            if pyxel.btnp(pyxel.KEY_R): self.reset_game()
            return

        if self.turn == 1: # Joueur
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                x, y = pyxel.mouse_x // TILE, pyxel.mouse_y // TILE
                if self.p is None:
                    temp = self.is_occupied(x, y)
                    if temp and temp.is_bottom_player:
                        self.p = temp
                        self.valid.moves = self.p.valid_moves(self.pieces, self)
                else:
                    if (x, y) in self.valid.moves:
                        self.execute_move(self.p, x, y)
                    self.p, self.valid.moves = None, []
        else: # IA
            self.ia_move()

    def ia_move(self):
        ia_pieces = [p for p in self.pieces if not p.is_bottom_player]
        valid_actions = []
        for p in ia_pieces:
            for m in p.valid_moves(self.pieces, self):
                valid_actions.append((p, m))
        
        if valid_actions:
            # On cherche un coup qui ne met pas le roi en danger (simplifié)
            random.shuffle(valid_actions)
            for p, (nx, ny) in valid_actions:
                if self.execute_move(p, nx, ny):
                    return
        self.chessboard.game_over = True # Pat ou Mat

    def draw(self):
        self.chessboard.draw()
        texte = "TOUR: BLANC" if self.turn == 1 else "TOUR: IA (NOIR)"
        pyxel.text(5, 3, texte, 7 if self.turn == 1 else 13)
        for mx, my in self.valid.moves:
            pyxel.circ(mx * TILE + 8, my * TILE + 8, 2, 11)
        for piece in self.pieces:
            piece.draw()

Game()