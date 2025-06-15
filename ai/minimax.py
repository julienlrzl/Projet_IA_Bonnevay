from copy import deepcopy
from ai.evaluation import evaluation

joueur_ref = None  # <-- ajouté

def est_feuille(n):
    j_adv = 'O' if n.joueur_actuel == 'X' else 'X'
    return n.est_victoire(j_adv) or n.est_pleine()

def generer_fils(n):
    fils = []
    for col in n.get_valid_moves():
        copie = deepcopy(n)
        copie.jouer(col)
        copie.changer_joueur()
        fils.append((copie, col))
    return fils

def minimax(racine, max_profondeur):
    global joueur_ref
    joueur_ref = racine.joueur_actuel
    eval_finale, action = joueur_max(racine, max_profondeur)
    return action

def joueur_max(n, p):
    if est_feuille(n) or p == 0:
        adversaire = 'O' if n.joueur_actuel == 'X' else 'X'
        if n.est_victoire(adversaire):
            return -100000, get_default_action(n)
        return evaluation(n, joueur_ref), get_default_action(n)

    u = float('-inf')
    a = None

    for f, a_f in generer_fils(n):
        eval_min, _ = joueur_min(f, p - 1)
        if eval_min > u:
            u = eval_min
            a = a_f

    return u, a

def joueur_min(n, p):
    if est_feuille(n) or p == 0:
        adversaire = 'O' if n.joueur_actuel == 'X' else 'X'
        if n.est_victoire(adversaire):
            return 100000, get_default_action(n)
        return evaluation(n, joueur_ref), get_default_action(n)

    u = float('inf')
    a = None

    for f, a_f in generer_fils(n):
        eval_max, _ = joueur_max(f, p - 1)
        if eval_max < u:
            u = eval_max
            a = a_f

    return u, a

def get_default_action(n):
    valid_moves = n.get_valid_moves()
    return valid_moves[0] if valid_moves else 0