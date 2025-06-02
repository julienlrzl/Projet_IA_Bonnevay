import tkinter as tk
from tkinter import messagebox
from game.puissance4 import Puissance4
from ai.minimax import minimax
from ai.alphabeta import alpha_beta
# from ai.mcts import mcts  # si tu veux le rajouter

class Puissance4GUI:
    def __init__(self):
        self.jeu = Puissance4()
        self.mode = None
        self.ia1 = None
        self.ia2 = None
        self.window = None
        self.canvas = None
        self.label_infos = None
        self.profondeur_ia1 = 4
        self.profondeur_ia2 = 4

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
        self.centrer_fenetre(popup, 320, 300)

        tk.Label(popup, text="Mode de jeu :", font=("Arial", 14)).pack(pady=10)
        tk.Button(popup, text="Joueur vs Joueur", width=25, command=lambda: self.set_mode(popup, 'PVP')).pack(pady=5)
        tk.Button(popup, text="Joueur vs IA", width=25, command=lambda: self.set_mode(popup, 'PvIA')).pack(pady=5)
        tk.Button(popup, text="IA vs IA", width=25, command=lambda: self.set_mode(popup, 'IAvsIA')).pack(pady=5)
        tk.Button(popup, text="Quitter", width=25, command=popup.quit).pack(pady=15)

        popup.mainloop()

    def choisir_profondeur(self, titre):
        popup = tk.Tk()
        popup.title(titre)
        self.centrer_fenetre(popup, 300, 200)

        val = tk.IntVar()
        val.set(4)  # par défaut

        tk.Label(popup, text="Choisissez la profondeur :", font=("Arial", 14)).pack(pady=10)
        tk.Scale(popup, from_=1, to=8, orient='horizontal', variable=val).pack(pady=10)

        tk.Button(popup, text="Valider", command=popup.quit).pack(pady=10)

        popup.mainloop()
        popup.destroy()

        return val.get()

    def set_mode(self, popup, mode):
        self.mode = mode
        popup.destroy()

    def dessiner_grille(self):
        self.canvas.delete("all")
        for row in range(self.jeu.rows):
            for col in range(self.jeu.cols):
                x1 = col * 100
                y1 = row * 100 + 50  # Décaler vers le bas à cause du label
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
        if self.mode not in ['PVP', 'PvIA']:
            messagebox.showinfo("Non disponible", "Ce mode de jeu n'est pas encore disponible.")
            return

        col = event.x // 100
        if self.jeu.jouer(col):
            self.dessiner_grille()
            if self.jeu.est_victoire():
                messagebox.showinfo("Victoire", f"Le joueur {self.jeu.joueur_actuel} a gagné !")
                self.window.destroy()
                self.lancer()
                return
            elif self.jeu.est_pleine():
                messagebox.showinfo("Match nul", "Le plateau est plein. Match nul !")
                self.window.destroy()
                self.lancer()
                return
            else:
                self.jeu.changer_joueur()

        if self.mode == 'PvIA' and self.jeu.joueur_actuel == 'O':
            self.window.after(500, self.tour_ia)

    def tour_ia(self):
        if self.ia2 == "1":
            col = minimax(self.jeu, max_profondeur=self.profondeur_ia2)
        elif self.ia2 == "2":
            col = alpha_beta(self.jeu, max_profondeur=self.profondeur_ia2)
        elif self.ia2 == "3":
            print("MCTS non implémenté")
            col = 0
        else:
            col = 0

        if self.jeu.jouer(col):
            self.dessiner_grille()
            if self.jeu.est_victoire():
                messagebox.showinfo("Victoire", f"L'IA a gagné !")
                self.window.destroy()
                self.lancer()
                return
            elif self.jeu.est_pleine():
                messagebox.showinfo("Match nul", "Le plateau est plein. Match nul !")
                self.window.destroy()
                self.lancer()
                return
            else:
                self.jeu.changer_joueur()

    def tour_ia_vs_ia(self):
        if self.jeu.joueur_actuel == 'X':
            choix_ia = self.ia1
            profondeur = self.profondeur_ia1
        else:
            choix_ia = self.ia2
            profondeur = self.profondeur_ia2

        if choix_ia == "1":
            col = minimax(self.jeu, max_profondeur=profondeur)
        elif choix_ia == "2":
            col = alpha_beta(self.jeu, max_profondeur=profondeur)
        elif choix_ia == "3":
            print("MCTS non implémenté")
            col = 0
        else:
            col = 0

        if self.jeu.jouer(col):
            self.dessiner_grille()
            if self.jeu.est_victoire():
                messagebox.showinfo("Victoire", f"L'IA {self.jeu.joueur_actuel} a gagné !")
                self.window.destroy()
                self.lancer()
                return
            elif self.jeu.est_pleine():
                messagebox.showinfo("Match nul", "Le plateau est plein. Match nul !")
                self.window.destroy()
                self.lancer()
                return
            else:
                self.jeu.changer_joueur()
                self.window.after(500, self.tour_ia_vs_ia)

    def choisir_ia(self, titre):
        popup = tk.Tk()
        popup.title(titre)
        self.centrer_fenetre(popup, 320, 250)

        choix = tk.StringVar()
        choix.set("1")  # par défaut Minimax

        tk.Label(popup, text="Choisissez l'IA :", font=("Arial", 14)).pack(pady=10)
        tk.Radiobutton(popup, text="Minimax", variable=choix, value="1").pack(anchor='w', padx=20)
        tk.Radiobutton(popup, text="Alpha-Beta", variable=choix, value="2").pack(anchor='w', padx=20)
        tk.Radiobutton(popup, text="MCTS (non implémenté)", variable=choix, value="3").pack(anchor='w', padx=20)

        tk.Button(popup, text="Valider", command=popup.quit).pack(pady=15)

        popup.mainloop()
        popup.destroy()

        return choix.get()

    def afficher_infos_joueurs(self):
        infos = ""
        if self.mode == 'PVP':
            infos = "🔴 Joueur X : Humain      🟡 Joueur O : Humain"
        elif self.mode == 'PvIA':
            ia2_name = "Minimax" if self.ia2 == "1" else "AlphaBeta" if self.ia2 == "2" else "MCTS"
            infos = f"🔴 Joueur X : Humain      🟡 Joueur O : IA ({ia2_name}, prof {self.profondeur_ia2})"
        elif self.mode == 'IAvsIA':
            ia1_name = "Minimax" if self.ia1 == "1" else "AlphaBeta" if self.ia1 == "2" else "MCTS"
            ia2_name = "Minimax" if self.ia2 == "1" else "AlphaBeta" if self.ia2 == "2" else "MCTS"
            infos = f"🔴 Joueur X : IA ({ia1_name}, prof {self.profondeur_ia1})      🟡 Joueur O : IA ({ia2_name}, prof {self.profondeur_ia2})"

        self.label_infos.config(text=infos)

    def lancer(self):
        self.jeu = Puissance4()
        self.choisir_mode_jeu()

        if self.mode is None:
            return  # si on a cliqué sur "Quitter"

        if self.mode == 'PvIA':
            self.ia2 = self.choisir_ia("Choix de l'IA (joueur O)")
            self.profondeur_ia2 = self.choisir_profondeur("Profondeur IA (joueur O)")

        elif self.mode == 'IAvsIA':
            self.ia1 = self.choisir_ia("Choix IA 1 (joueur X)")
            self.profondeur_ia1 = self.choisir_profondeur("Profondeur IA 1 (joueur X)")

            self.ia2 = self.choisir_ia("Choix IA 2 (joueur O)")
            self.profondeur_ia2 = self.choisir_profondeur("Profondeur IA 2 (joueur O)")

        self.window = tk.Tk()
        self.window.title("Puissance 4")
        self.centrer_fenetre(self.window, 700, 700)

        self.label_infos = tk.Label(self.window, text="", font=("Arial", 14))
        self.label_infos.pack(pady=5)
        self.afficher_infos_joueurs()

        self.canvas = tk.Canvas(self.window, width=700, height=650, bg='blue')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic_souris)

        self.dessiner_grille()

        if self.mode == 'IAvsIA':
            self.window.after(1000, self.tour_ia_vs_ia)

        self.window.mainloop()
