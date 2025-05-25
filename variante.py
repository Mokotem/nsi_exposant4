from puissance4 import *

class PartieTetris(Partie):
    def __init__(self, dim, taille_p, p1, p2):
        super().__init__(dim, taille_p, p1, p2)
        self.pileDesTetris = PileMaisNormal()  # de bools
        self.pileDesColonnes = PileMaisNormal() # de list de int

    def jouer_coup(self, colonne):
        super().jouer_coup(colonne)
        if self.grille[colonne].est_plein():
            self.pileDesColonnes.add(self.grille[colonne])
            print(self.pileDesColonnes.peek)
            self.grille[colonne].vider()  # principe de la variante
            self.pileDesTetris.add(True)
        else:
            self.pileDesTetris.add(False)

    def defaire(self):
        self.__finito = False
        if self.pileDesTetris.pop():
            self.grille[self.pileDesCoups.pop()] = self.pileDesColonnes.pop()
        else:
            self.grille[self.pileDesCoups.pop()].retirer()
        
        self.changer_de_joueur()
