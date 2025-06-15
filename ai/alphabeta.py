from copy import deepcopy
from ai.evaluation import evaluation


def est_feuille(etat):
    joueur_precedent = 'O' if etat.joueur_actuel == 'X' else 'X'
    return etat.est_victoire(joueur_precedent) or etat.est_pleine()


def generer_fils(etat):
    fils = []
    for col in etat.get_valid_moves():
        copie = deepcopy(etat)
        copie.jouer(col)
        copie.changer_joueur()  
        fils.append((copie, col))
    return fils

def alpha_beta(racine, max_profondeur):
    global joueur_ref
    joueur_ref = racine.joueur_actuel  # <-- ligne importante
    eval, action = joueur_max(racine, max_profondeur, float('-inf'), float('inf'))
    return action



def joueur_max(n, p, alpha, beta):
    if est_feuille(n) or p == 0:
        return evaluation(n, joueur_ref), get_default_action(n)

    u = float('-inf')
    a = get_default_action(n)  

    for f, action_f in generer_fils(n):
        if f.est_victoire(n.joueur_actuel):  # car 'n' est le parent de 'f'
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
        return evaluation(n, joueur_ref), get_default_action(n)


    u = float('inf')
    a = get_default_action(n) 

    for f, action_f in generer_fils(n):
        if f.est_victoire(n.joueur_actuel):  # car 'n' est le parent de 'f'
            return float('-inf'), action_f
        
        eval, _ = joueur_max(f, p - 1, alpha, beta)
        if eval < u:
            u = eval
            a = action_f
        beta = min(beta, u)
        if beta <= alpha:
            return u, a  

    return u, a


def get_default_action(n):
    """Renvoie un coup valide arbitraire pour éviter de retourner None."""
    valid_moves = n.get_valid_moves()
    return valid_moves[0] if valid_moves else 0