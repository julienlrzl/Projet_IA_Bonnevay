import tkinter as tk
from tkinter import messagebox
from game.puissance4 import Puissance4

class Puissance4GUI:
    def __init__(self):
        self.jeu = Puissance4()  # <-- on utilise la classe logique ici
        self.window = tk.Tk()
        self.window.title("Puissance 4")
        self.canvas = tk.Canvas(self.window, width=700, height=600, bg='blue')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic_souris)
        self.dessiner_grille()

    def dessiner_grille(self):
        self.canvas.delete("all")
        for row in range(self.jeu.rows):
            for col in range(self.jeu.cols):
                x1 = col * 100
                y1 = row * 100
                x2 = x1 + 100
                y2 = y1 + 100
                couleur = 'white'
                case = self.jeu.grille[row][col]
                if case == 'X':
                    couleur = 'red'
                elif case == 'O':
                    couleur = 'yellow'
                self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill=couleur, outline='black')

    def clic_souris(self, event):
        col = event.x // 100
        if self.jeu.jouer(col):
            self.dessiner_grille()
            if self.jeu.est_victoire():
                messagebox.showinfo("Victoire", f"Le joueur {self.jeu.joueur_actuel} a gagné !")
                self.window.quit()
            elif self.jeu.est_pleine():
                messagebox.showinfo("Match nul", "Le plateau est plein. Match nul !")
                self.window.quit()
            else:
                self.jeu.changer_joueur()

    def lancer(self):
        self.window.mainloop()
