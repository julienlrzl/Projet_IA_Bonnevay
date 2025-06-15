# --- evaluation.py ---
def eval_ligne(ligne, joueur):
    adversaire = 'X' if joueur == 'O' else 'O'
    count = ligne.count(joueur)
    empty = ligne.count('.')
    if ligne.count(adversaire) > 0:
        return 0
    if count == 4:
        return 100000
    elif count == 3 and empty == 1:
        return 1000
    elif count == 2 and empty == 2:
        return 100
    elif count == 1 and empty == 3:
        return 10
    return 0

def evaluation(jeu, joueur_ref):
    """
    Retourne un score >0 si la position est favorable à joueur_ref,
    <0 si elle est favorable à l'adversaire de joueur_ref,
    0 si neutre.
    """
    def total_pour(joueur):
        score = 0
        for r in range(jeu.rows):
            for c in range(jeu.cols - 3):
                ligne = [jeu.grille[r][c+i] for i in range(4)]
                score += eval_ligne(ligne, joueur)
        for r in range(jeu.rows - 3):
            for c in range(jeu.cols):
                colonne = [jeu.grille[r+i][c] for i in range(4)]
                score += eval_ligne(colonne, joueur)
        for r in range(jeu.rows - 3):
            for c in range(jeu.cols - 3):
                diag1 = [jeu.grille[r+i][c+i] for i in range(4)]
                diag2 = [jeu.grille[r+3-i][c+i] for i in range(4)]
                score += eval_ligne(diag1, joueur)
                score += eval_ligne(diag2, joueur)
        return score

    adversaire = 'X' if joueur_ref == 'O' else 'O'
    return total_pour(joueur_ref) - total_pour(adversaire)