import numpy as np
from ai.ArbreJeu import ArbreJeu

class RechercheMonteCarlo:
    def __init__(self, etat_initial, joueur_actuel):
        self.facteur_ucb = 1 / np.sqrt(2.0)
        self.arbre = ArbreJeu(etat_initial, joueur_actuel)

    def chercher_utc(self, iterations):
        racine = self.arbre.graphe.nodes[1]
        for _ in range(iterations):
            noeud = self.selection_politique(racine)
            recompense = self.simulation(noeud["plateau"], noeud["joueur"])
            self.retropropagation_negamax(noeud, recompense)
        meilleur = self.meilleur_enfant(racine, 0)
        return meilleur["coup"]

    def selection_politique(self, noeud):
        while not noeud["terminal"]:
            if not self.arbre.tout_explore(noeud):
                return self.expansion(noeud)
            else:
                noeud = self.meilleur_enfant(noeud, self.facteur_ucb)
        return noeud

    def expansion(self, noeud):
        coup = self.arbre.coup_suivant(noeud)
        nouvel_id = self.arbre.graphe.number_of_nodes() + 1
        self.arbre.ajouter_noeud(noeud["id_noeud"], nouvel_id, coup)
        return self.arbre.graphe.nodes[nouvel_id]

    def meilleur_enfant(self, noeud, facteur):
        scores = []
        enfants = []
        for n in self.arbre.enfants(noeud):
            n_tmp = self.arbre.graphe.nodes[n]
            exploitation = n_tmp["score"] / n_tmp["visites"]
            exploration = np.sqrt(2.0 * np.log(noeud["visites"]) / n_tmp["visites"])
            total = exploitation + facteur * exploration
            scores.append(total)
            enfants.append(n)
        idx = np.argmax(scores)
        return self.arbre.graphe.nodes[enfants[idx]]

    def simulation(self, plateau, joueur):
        return self.arbre.simuler(plateau, joueur)

    def retropropagation_negamax(self, noeud, score):
        while len(self.arbre.parent(noeud)) != 0:
            noeud["visites"] += 1
            noeud["score"] += score
            score = -score
            noeud = self.arbre.graphe.nodes[self.arbre.parent(noeud)[0]]

# --- Fonctions utilitaires pour la conversion depuis Puissance4 ---

def grille_vers_numpy(grille):
    conversion = {'.': 0, 'X': 1, 'O': 2}
    res = np.zeros((6, 7), dtype=int)
    for l in range(6):
        for c in range(7):
            res[l, c] = conversion[grille[l][c]]
    return res

def joueur_vers_int(joueur):
    return 1 if joueur == 'X' else 2

def mcts(puissance4, budget=1000):
    plateau = grille_vers_numpy(puissance4.grille)
    joueur = joueur_vers_int(puissance4.joueur_actuel)
    agent = RechercheMonteCarlo(plateau, joueur)
    col = agent.chercher_utc(budget)
    return int(col)