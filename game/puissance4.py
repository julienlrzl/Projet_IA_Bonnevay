class Puissance4:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.grille = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        self.joueur_actuel = 'X'

    def afficher_grille(self):
        for ligne in self.grille:
            print(' '.join(ligne))
        print(' '.join([str(i) for i in range(self.cols)]))

    def jouer(self, col):
        if col < 0 or col >= self.cols:
            print("Colonne invalide.")
            return False
        for row in reversed(range(self.rows)):
            if self.grille[row][col] == '.':
                self.grille[row][col] = self.joueur_actuel
                return True
        print("Colonne pleine.")
        return False

    def changer_joueur(self):
        self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'

    def est_pleine(self):
        return all(self.grille[0][col] != '.' for col in range(self.cols))

    def est_victoire(self):
        def check4(a, b, c, d):
            return a == b == c == d != '.'

        for r in range(self.rows):
            for c in range(self.cols - 3):
                if check4(self.grille[r][c], self.grille[r][c+1], self.grille[r][c+2], self.grille[r][c+3]):
                    return True

        for r in range(self.rows - 3):
            for c in range(self.cols):
                if check4(self.grille[r][c], self.grille[r+1][c], self.grille[r+2][c], self.grille[r+3][c]):
                    return True

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if check4(self.grille[r][c], self.grille[r+1][c+1], self.grille[r+2][c+2], self.grille[r+3][c+3]):
                    return True

        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if check4(self.grille[r][c], self.grille[r-1][c+1], self.grille[r-2][c+2], self.grille[r-3][c+3]):
                    return True

        return False
    
    def get_valid_moves(self):
        return [c for c in range(self.cols) if self.grille[0][c] == '.']