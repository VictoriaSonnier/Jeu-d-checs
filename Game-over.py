import pyxel

WIDTH = 40
HEIGHT = 40
BLACK = 0
WHITE = 7

class JeuEchecs:
    def __init__(self): # constructeur
        pyxel.init(WIDTH, HEIGHT, title="Echecs") #allume l'écran de jeu
        
        
        self.damier = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.damier.append((i, j))
        
        self.game_over = False
        self.winner = "BLANC" 
        
        pyxel.run(self.update, self.draw) #dtecte echec et mat

    def display(self, color, pixels=None): #self indique que la fonction appartient la classe JeuEchecs.
        if pixels is None:
            pyxel.cls(color)
        else:
            for x, y in pixels:
                pyxel.rect(x * 5, y * 5, 5, 5, color)

    def update(self):
        # g=ame over pour test
        if pyxel.btnp(pyxel.KEY_G):
            self.game_over = True
        
        # R pour rejouer
        if self.game_over and pyxel.btnp(pyxel.KEY_R):
            self.game_over = False
            

    def draw(self):
        self.display(BLACK) #trace d'abord le fond noir
        self.display(WHITE, self.damier) #damier blanc
        
        if self.game_over:


            if self.game_over:

                pyxel.rect(1, 10, 38, 26, 6)
                pyxel.rectb(1, 10, 38, 26, 7)

                pyxel.text(12, 13, "GAME", 5) 
                pyxel.text(12, 20, "OVER", 5) 


                pyxel.text(2, 27, f"GAGNANT:{self.winner[0]}", 5)
             

JeuEchecs()








