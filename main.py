from game.puissance4 import Puissance4


def jouer_partie():
    jeu = Puissance4()

    while True:
        jeu.afficher_grille()
        try:
            col = int(input(f"Joueur {jeu.joueur_actuel}, choisissez une colonne (0-6) : "))
        except ValueError:
            print("Veuillez entrer un nombre.")
            continue

        if not jeu.jouer(col):
            continue

        if jeu.est_victoire():
            jeu.afficher_grille()
            print(f"Le joueur {jeu.joueur_actuel} a gagné ! 🎉")
            break

        if jeu.est_pleine():
            jeu.afficher_grille()
            print("Match nul ! 🤝")
            break

        jeu.changer_joueur()

if __name__ == "__main__":
    jouer_partie()
