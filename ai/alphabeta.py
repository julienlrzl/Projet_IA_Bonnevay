# --- alphabeta.py ---
from copy import deepcopy
from ai.evaluation import evaluation

# Le joueur “référentiel” (celui pour lequel on maximise au niveau de la racine)
# sera passé en paramètre dès l'appel initial.
# On ne modifie jamais “jeu.joueur_actuel” dans evaluation ni dans utilité.

def est_terminal(etat):
    # Si l'un des deux a aligné 4, ou si la grille est pleine ⇒ terminal
    # Rappel : est_victoire(s) avec argument s teste si 's' a une ligne gagnante.
    return any(etat.est_victoire(s) for s in ('X', 'O')) or etat.est_pleine()

def generer_fils(etat):
    fils = []
    for col in etat.get_valid_moves():
        copie = deepcopy(etat)
        copie.jouer(col)
        copie.changer_joueur()  # ← C’EST ESSENTIEL !
        fils.append((copie, col))
    return fils



def alpha_beta(racine, max_profondeur):
    """
    Appelé depuis console/gui. On considère que racine.joueur_actuel est
    le joueur que l'on veut faire jouer ici (X ou O). 
    On prendra “joueur_ref = racine.joueur_actuel”.
    """
    joueur_ref = racine.joueur_actuel
    valeur, action = max_value(racine, max_profondeur, float('-inf'), float('inf'), joueur_ref)

    # --- Ajoute cette ligne ---
    if action is None:
        valid_moves = racine.get_valid_moves()
        if valid_moves:
            action = valid_moves[0]
        else:
            print("[ERREUR] Aucun coup valide trouvé dans alpha_beta.")
            action = 0  # fallback sûr

    print(f"[AlphaBeta depth {max_profondeur}] Best move for {joueur_ref}: {action}, Eval = {valeur}")
    if valeur == float('inf') or valeur == float('-inf'):
        print("[!WARNING] Évaluation infinie détectée. Est-ce justifié ?")
        racine.afficher_grille()

    return action



def max_value(noeud, profondeur, alpha, beta, joueur_ref):
    """
    Noeud ⟶ c'est le moment où c'est au tour de noeud.joueur_actuel de jouer.
    On cherche à MAXIMISER le score pour joueur_ref.
    """
    if profondeur == 0 or noeud.est_pleine():
        return utilite(noeud, joueur_ref), None

    adversaire = 'O' if noeud.joueur_actuel == 'X' else 'X'
    if noeud.est_victoire(adversaire):
        return float('-inf'), None


    valeur = float('-inf')
    meilleur_coup = None

    # Pour chaque coup possible :
    for (fils, action_f) in generer_fils(noeud):
        # On descend dans la mesure où c'est au tour du joueur adverse
        val_min, _ = min_value(fils, profondeur - 1, alpha, beta, joueur_ref)
        if val_min > valeur:
            valeur = val_min
            meilleur_coup = action_f
        # Actualisation alpha puis test de coupe
        alpha = max(alpha, valeur)
        if alpha >= beta:
            break  # coupe bêta
    return valeur, meilleur_coup


def min_value(noeud, profondeur, alpha, beta, joueur_ref):
    """
    Noeud ⟶ c'est le tour de noeud.joueur_actuel de jouer, mais ici on veut MINIMISER
    le score pour joueur_ref, car c'est l'adversaire dans l'arbre minimax.
    """
    if profondeur == 0 or noeud.est_pleine():
        return utilite(noeud, joueur_ref), None

    adversaire = 'O' if noeud.joueur_actuel == 'X' else 'X'
    if noeud.est_victoire(adversaire):
        return float('inf'), None


    valeur = float('inf')
    meilleur_coup = None

    for (fils, action_f) in generer_fils(noeud):
        val_max, _ = max_value(fils, profondeur - 1, alpha, beta, joueur_ref)
        if val_max < valeur:
            valeur = val_max
            meilleur_coup = action_f
        beta = min(beta, valeur)
        if beta <= alpha:
            break  # coupe alpha
    return valeur, meilleur_coup

def utilite(noeud, joueur_ref):
    """
    Évalue une position pour Alpha-Beta.
    +∞ si victoire de joueur_ref
    –∞ si victoire de l’adversaire
    0 si match nul
    sinon : heuristique
    """
    adversaire = 'O' if joueur_ref == 'X' else 'X'

    
    if noeud.est_victoire(joueur_ref):
        return float('inf')
    if noeud.est_victoire(adversaire):
        return float('-inf')
    if noeud.est_pleine():
        return 0

    if evaluation(noeud, joueur_ref) >= 1e6:
        print("[DEBUG] Heuristique très élevée sans victoire réelle.")

    return evaluation(noeud, joueur_ref)


