import tkinter as tk
from tkinter import messagebox
from game.puissance4 import Puissance4

class Puissance4GUI:
    def __init__(self):
        self.jeu = Puissance4()
        self.mode = None
        self.window = None
        self.canvas = None

    def centrer_fenetre(self, fenetre, largeur, hauteur):
        fenetre.update_idletasks()
        screen_width = fenetre.winfo_screenwidth()
        screen_height = fenetre.winfo_screenheight()
        x = (screen_width // 2) - (largeur // 2)
        y = (screen_height // 2) - (hauteur // 2)
        fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

    def choisir_mode_jeu(self):
        popup = tk.Tk()
        popup.title("Choix du mode de jeu")
        self.centrer_fenetre(popup, 320, 220)

        tk.Label(popup, text="Mode de jeu :", font=("Arial", 14)).pack(pady=10)
        tk.Button(popup, text="Joueur vs Joueur", width=25, command=lambda: self.set_mode(popup, 'PVP')).pack(pady=5)
        tk.Button(popup, text="IA vs IA", width=25, command=lambda: self.set_mode(popup, 'IAvsIA')).pack(pady=5)
        tk.Button(popup, text="IA vs IA", width=25, state='disabled').pack(pady=5)
        tk.Button(popup, text="Quitter", width=25, command=popup.quit).pack(pady=15)

        popup.mainloop()

    def set_mode(self, popup, mode):
        self.mode = mode
        popup.destroy()

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
        if self.mode != 'PVP':
            messagebox.showinfo("Non disponible", "Ce mode de jeu n'est pas encore disponible.")
            return

        col = event.x // 100
        if self.jeu.jouer(col):
            self.dessiner_grille()
            if self.jeu.est_victoire():
                messagebox.showinfo("Victoire", f"Le joueur {self.jeu.joueur_actuel} a gagné !")
                self.rejouer()
            elif self.jeu.est_pleine():
                messagebox.showinfo("Match nul", "Le plateau est plein. Match nul !")
                self.rejouer()
            else:
                self.jeu.changer_joueur()

    def rejouer(self):
        self.jeu = Puissance4()
        self.dessiner_grille()

    def lancer(self):
        self.choisir_mode_jeu()

        self.window = tk.Tk()
        self.window.title("Puissance 4")
        self.centrer_fenetre(self.window, 700, 640)

        self.canvas = tk.Canvas(self.window, width=700, height=600, bg='blue')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic_souris)

        self.dessiner_grille()
        self.window.mainloop()