from copy import deepcopy
from ai.evaluation import evaluation


def est_feuille(etat):
    return etat.est_victoire() or etat.est_pleine()

def generer_fils(etat):
    fils = []
    for col in etat.get_valid_moves():
        copie = deepcopy(etat)
        copie.jouer(col)
        copie.changer_joueur()  
        fils.append((copie, col))
    return fils

def alpha_beta(racine, max_profondeur):
    eval, action = joueur_max(racine, max_profondeur, float('-inf'), float('inf'))
    return action


def joueur_max(n, p, alpha, beta):
    if est_feuille(n) or p == 0:
        return evaluation(n), None

    u = float('-inf')
    a = None

    for f, action_f in generer_fils(n):
        if f.est_victoire():
            return float('inf'), action_f
        
        eval, _ = joueur_min(f, p - 1, alpha, beta)
        if eval > u:
            u = eval
            a = action_f
        alpha = max(alpha, u)
        if alpha >= beta:
            return u, a

    return u, a


def joueur_min(n, p, alpha, beta):
    if est_feuille(n) or p == 0:
        return evaluation(n), None

    u = float('inf')
    a = None

    for f, action_f in generer_fils(n):
        if f.est_victoire():
            return float('-inf'), action_f
        
        eval, _ = joueur_max(f, p - 1, alpha, beta)
        if eval < u:
            u = eval
            a = action_f
        beta = min(beta, u)
        if beta <= alpha:
            return u, a

    return u, a