import numpy as np
import networkx as nx

class ArbreJeu:
    """
    Structure d'arbre pour recherche MCTS sur Puissance 4 (grille numpy)
    """
    def __init__(self, plateau, joueur_courant):
        self.lignes = plateau.shape[0]
        self.colonnes = plateau.shape[1]
        self.graphe = nx.Graph()
        joueur_init = 1 + joueur_courant % 2
        coups_possibles = list(range(self.colonnes))
        self.graphe.add_node(
            1,
            id_noeud=1,
            coup=None,
            visites=1,
            score=0,
            plateau=plateau,
            coups_restants=coups_possibles,
            joueur=joueur_init,
            terminal=False
        )

    def ajouter_noeud(self, parent, enfant, coup_joue):
        etat_parent = self.graphe.nodes[parent]["plateau"].copy()
        idx_ligne = np.where(etat_parent[:, coup_joue] == 0)[0][-1]
        joueur_suivant = 1 + self.graphe.nodes[parent]["joueur"] % 2
        etat_parent[idx_ligne, coup_joue] = joueur_suivant
        nouveaux_coups = self.graphe.nodes[parent]["coups_restants"].copy()
        nouveaux_coups.remove(coup_joue)
        self.graphe.nodes[parent]["coups_restants"] = nouveaux_coups
        is_terminal = self.est_terminal(etat_parent)
        self.graphe.add_node(
            enfant,
            id_noeud=enfant,
            coup=coup_joue,
            visites=1,
            score=0,
            plateau=etat_parent,
            coups_restants=list(range(self.colonnes)),
            joueur=joueur_suivant,
            terminal=is_terminal
        )
        self.graphe.add_edge(parent, enfant)

    def coup_suivant(self, noeud):
        libres = np.where(noeud["plateau"][0, :] == 0)[0]
        restants = noeud["coups_restants"]
        possibles = np.intersect1d(restants, libres)
        return np.random.choice(possibles)

    def detecter_vainqueur(self, plateau):
        # lignes
        for l in range(self.lignes):
            for c in range(self.colonnes - 3):
                s = plateau[l, c:c+4]
                if np.all(s == s[0]) and s[0] != 0:
                    return s[0]
        # colonnes
        for c in range(self.colonnes):
            for l in range(self.lignes - 3):
                s = plateau[l:l+4, c]
                if np.all(s == s[0]) and s[0] != 0:
                    return s[0]
        # diagonale descendante
        for l in range(self.lignes - 3):
            for c in range(self.colonnes - 3):
                s = np.array([plateau[l + i, c + i] for i in range(4)])
                if np.all(s == s[0]) and s[0] != 0:
                    return s[0]
        # diagonale montante
        for l in range(3, self.lignes):
            for c in range(self.colonnes - 3):
                s = np.array([plateau[l - i, c + i] for i in range(4)])
                if np.all(s == s[0]) and s[0] != 0:
                    return s[0]
        return False

    def mettre_a_jour(self, idx, valeur):
        self.graphe.nodes[idx]["visites"] += 1
        self.graphe.nodes[idx]["score"] += valeur

    def enfants(self, noeud):
        voisins = np.array(list(self.graphe.adj[noeud["id_noeud"]]))
        return np.sort(voisins[voisins > noeud["id_noeud"]])

    def parent(self, noeud):
        voisins = np.array(list(self.graphe.adj[noeud["id_noeud"]]))
        return voisins[voisins < noeud["id_noeud"]]

    def tout_explore(self, noeud):
        libres = np.where(noeud["plateau"][0, :] == 0)[0]
        restants = noeud["coups_restants"]
        possibles = np.intersect1d(restants, libres)
        return len(self.enfants(noeud)) == self.colonnes or len(possibles) == 0

    def est_terminal(self, plateau):
        libres = np.where(plateau[0, :] == 0)[0]
        return len(libres) == 0 or (self.detecter_vainqueur(plateau) != False)

    def simuler(self, plateau, joueur):
        etat = plateau.copy()
        joueur_local = joueur
        gagnant = self.detecter_vainqueur(etat)
        while gagnant == False:
            moves = np.where(etat[0, :] == 0)[0]
            if len(moves) == 0:
                return 0
            action = np.random.choice(moves)
            joueur_local = 1 + joueur_local % 2
            pos = np.where(etat[:, action] == 0)[0][-1]
            etat[pos, action] = joueur_local
            gagnant = self.detecter_vainqueur(etat)
        if gagnant == joueur:
            return 1
        else:
            return -1