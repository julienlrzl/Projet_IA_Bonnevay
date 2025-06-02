from copy import deepcopy
from ai.evaluation import evaluation


def est_feuille(n):
    return n.est_victoire() or n.est_pleine()

def generer_fils(n):
    """Génère tous les coups possibles (copie de l'état + colonne jouée)."""
    fils = []
    for col in n.get_valid_moves():
        copie = deepcopy(n)
        copie.jouer(col)
        copie.changer_joueur()
        fils.append((copie, col))
    return fils


def minimax(racine, max_profondeur):
    """Appelle JOUEURMAX comme point d’entrée de l’algo."""
    eval_finale, action = joueur_max(racine, max_profondeur)
    return action


def joueur_max(n, p):
    if est_feuille(n) or p == 0:
        if n.est_victoire():
            return -100000, get_default_action(n)  # car l'adversaire vient de jouer
        return evaluation(n), get_default_action(n)

    u = float('-inf')
    a = None

    for f, a_f in generer_fils(n):
        eval, _ = joueur_min(f, p - 1)
        if eval > u:
            u = eval
            a = a_f

    return u, a


def joueur_min(n, p):
    if est_feuille(n) or p == 0:
        if n.est_victoire():
            return 100000, get_default_action(n)  # car l'adversaire vient de jouer
        return evaluation(n), get_default_action(n)

    u = float('inf')
    a = None

    for f, a_f in generer_fils(n):
        eval, _ = joueur_max(f, p - 1)
        if eval < u:
            u = eval
            a = a_f

    return u, a

def get_default_action(n):
    """Renvoie un coup valide arbitraire pour éviter de retourner None."""
    valid_moves = n.get_valid_moves()
    return valid_moves[0] if valid_moves else 0
