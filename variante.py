from puissance4 import *

class PartieTetris(Partie):
    def __init__(self, dim, taille_p, p1, p2):
        super().__init__(dim, taille_p, p1, p2)
        self.pileDesTetris = PileMaisNormal()  # de bools
        self.pileDesColonnes = PileMaisNormal() # de list de int

    def jouer_coup(self, colonne):

        self.grille[colonne].empiler(self.est_j1 + 1)
        self.pileDesCoups.add(colonne)
        if self.grille[colonne].est_plein():
            self.pileDesColonnes.add(self.grille[colonne].copier())
            self.grille[colonne].vider()  # principe de la variante
            self.pileDesTetris.add(True)
        else:
            self.pileDesTetris.add(False)

        if self.alignes(Vecteur(colonne, len(self.grille[colonne]) - 1)):
            self.finito = True
        self.changer_de_joueur()

    def defaire(self):
        self.finito = False
        """
        print("----")
        if self.pileDesCoups.height > 0:
            print("coups", self.pileDesCoups.peek)
            if self.pileDesColonnes.height > 0:
                print("colon", self.pileDesColonnes.peek)
            print("tetri", self.pileDesTetris.peek)
        """
        if self.pileDesTetris.pop():
            self.grille[self.pileDesCoups.peek] = self.pileDesColonnes.pop()
            self.grille[self.pileDesCoups.pop()].retirer()
        else:
            self.grille[self.pileDesCoups.pop()].retirer()
        
        self.changer_de_joueur()
