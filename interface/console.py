# interface/console.py

from game.puissance4 import Puissance4
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

def afficher_menu():
    print("\n--- Menu Puissance 4 ---")
    print("1. Joueur contre Joueur")
    print("2. Joueur contre IA (à venir)")
    print("3. IA contre IA (à venir)")
    print("0. Quitter")

def jouer_partie_console():
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == "1":
            jouer_joueur_vs_joueur()
        elif choix == "2":
            print("Mode Joueur contre IA en cours de développement.")
        elif choix == "3":
            print("Mode IA contre IA en cours de développement.")
        elif choix == "0":
            print("Au revoir !")
            sys.exit(0)
        else:
            print("Option invalide.")