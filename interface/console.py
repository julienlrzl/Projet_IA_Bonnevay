from game.puissance4 import Puissance4
from ai.minimax import minimax
# from ai.alphabeta import alpha_beta
# from ai.mcts import mcts
import sys

def afficher_grille_et_resultat(jeu):
    jeu.afficher_grille()
    if jeu.est_victoire():
        print(f"Victoire du joueur {jeu.joueur_actuel} !")
        return True
    elif jeu.est_pleine():
        print("Match nul !")
        return True
    return False

def jouer_joueur_vs_joueur():
    jeu = Puissance4()
    print("\n--- Joueur vs Joueur ---")
    while True:
        jeu.afficher_grille()
        try:
            col = int(input(f"Joueur {jeu.joueur_actuel}, choisissez une colonne (0-6) : "))
        except ValueError:
            print("Veuillez entrer un nombre.")
            continue

        if not jeu.jouer(col):
            print("Coup invalide. Réessayez.")
            continue

        if afficher_grille_et_resultat(jeu):
            break

        jeu.changer_joueur()

def jouer_joueur_vs_ia(choix_ia):
    jeu = Puissance4()
    print("\n--- Joueur vs IA ---")
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
            if choix_ia == "1":
                col = minimax(jeu, max_profondeur=4)
            # elif choix_ia == "2":
            #     col = alpha_beta(jeu, max_profondeur=4)
            # elif choix_ia == "3":
            #     col = mcts(jeu, simulations=1000)
            else:
                print("IA non reconnue.")
                break

        if not jeu.jouer(col):
            print("Coup invalide.")
            continue

        if afficher_grille_et_resultat(jeu):
            break

        jeu.changer_joueur()

def jouer_ia_vs_ia():
    jeu = Puissance4()
    profondeur = 4  # même profondeur pour X et O

    print("\n--- IA vs IA ---")

    while True:
        jeu.afficher_grille()
        print(f"[IA {jeu.joueur_actuel}] réfléchit...")

        # Choix d'algorithme par symbole (on peut différencier plus tard si besoin)
        col = minimax(jeu, max_profondeur=profondeur)
        # col = alpha_beta(jeu, max_profondeur=profondeur)
        # col = mcts(jeu, simulations=1000)

        if not jeu.jouer(col):
            print(f"[ERREUR] IA {jeu.joueur_actuel} a choisi une colonne invalide. Abandon.")
            break

        if afficher_grille_et_resultat(jeu):
            break

        jeu.changer_joueur()

def afficher_menu():
    print("\n--- Menu Puissance 4 ---")
    print("1. Joueur contre Joueur")
    print("2. Joueur contre IA")
    print("3. IA contre IA")
    print("0. Quitter")

def afficher_choix_ia():
    print("\n--- Choix de l'IA ---")
    print("1. Minimax")
    print("2. Alpha-Beta")
    print("3. MCTS")
    print("0. Retour")

def jouer_partie_console():
    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == "1":
            jouer_joueur_vs_joueur()

        elif choix == "2":
            afficher_choix_ia()
            choix_ia = input("Choisissez une IA : ")
            if choix_ia == "0":
                continue
            elif choix_ia not in ["1", "2", "3"]:
                print("Choix invalide.")
                continue
            jouer_joueur_vs_ia(choix_ia)

        elif choix == "3":
            jouer_ia_vs_ia()

        elif choix == "0":
            print("Au revoir !")
            sys.exit(0)

        else:
            print("Option invalide.")
