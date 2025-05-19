from game.puissance4 import Puissance4
from ai.alphabeta import alpha_beta
import sys

def jouer_joueur_vs_joueur():
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
            print(f"Le joueur {jeu.joueur_actuel} a gagné !")
            break

        if jeu.est_pleine():
            jeu.afficher_grille()
            print("Match nul !")
            break

        jeu.changer_joueur()

def jouer_joueur_vs_ia():
    jeu = Puissance4()
    while True:
        jeu.afficher_grille()
        if jeu.joueur_actuel == 'X':
            try:
                col = int(input("Votre coup (0-6) : "))
            except ValueError:
                print("Nombre invalide.")
                continue
        else:  # IA joue avec O
            print("IA réfléchit...")
            col = alpha_beta(jeu, max_profondeur=8)  # profondeur ajustable

        if not jeu.jouer(col):
            print("Coup invalide.")
            continue

        if jeu.est_victoire():
            jeu.afficher_grille()
            print(f"Le joueur {jeu.joueur_actuel} a gagné !")
            break

        if jeu.est_pleine():
            jeu.afficher_grille()
            print("Match nul.")
            break

        jeu.changer_joueur()

def afficher_menu():
    print("\n--- Menu Puissance 4 ---")
    print("1. Joueur contre Joueur")
    print("2. Joueur contre IA")
    print("3. IA contre IA (à venir)")
    print("0. Quitter")

def jouer_partie_console():
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == "1":
            jouer_joueur_vs_joueur()
        elif choix == "2":
            jouer_joueur_vs_ia()
        elif choix == "3":
            print("Mode IA contre IA en cours de développement.")
        elif choix == "0":
            print("Au revoir !")
            sys.exit(0)
        else:
            print("Option invalide.")