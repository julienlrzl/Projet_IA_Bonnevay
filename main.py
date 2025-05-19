# main.py

from interface.console import jouer_partie_console
from interface.gui import Puissance4GUI

def menu_choix_interface():
    print("\n--- Choix de l'interface ---")
    print("1. Interface Console")
    print("2. Interface Graphique (GUI)")
    print("0. Quitter")
    choix = input("Entrez votre choix : ")
    return choix

if __name__ == "__main__":
    choix = menu_choix_interface()

    if choix == "1":
        jouer_partie_console()
    elif choix == "2":
        gui = Puissance4GUI()
        gui.lancer()
    elif choix == "0":
        print("À bientôt !")
    else:
        print("Choix invalide.")

