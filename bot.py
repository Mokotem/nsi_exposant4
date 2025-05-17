from puissance4 import *
from random import choice, choices
from time import sleep

class Bot(Joueur):
    PROFONDEUR = 6
    Partie = None

    def __init__(self, prenom, pion, t):
        super().__init__(prenom, pion, t)
        
    @staticmethod
    def set_partie_ref(partie: Partie):
        Bot.Partie = partie

    @staticmethod
    def get_min(l: list, exept):
        m = 9999999
        i = 0
        while i < len(l):
            if l[i] < m and i in exept:
                m = l[i]
            i += 1
        k = list()
        i = 0
        while i < len(l):
            if l[i] == m and (i in exept):
                k.append(i)
            i += 1
        return choice(k)

    @staticmethod
    def get_max(l: list, exept):
        m = -9999999
        i = 0
        while i < len(l):
            if l[i] > m and i in exept:
                m = l[i]
            i += 1
        k = list()
        i = 0
        while i < len(l):
            if l[i] == m and (i in exept):
                k.append(i)
            i += 1
        return choice(k)

    def choisir(self, choix: list) -> int:
        cote = Bot.Partie.est_j1
        taille = Bot.Partie.dimention.x
        scores = [0] * taille
        i = 0
        for i in choix:
            sc = PileMaisNormal()
            Bot.Partie.jouer_coup(i)
            pile = PileMaisNormal()
            pile.add(Bot.Partie.coups_legaux())
            sc.add(10000 if Bot.Partie.est_j1 else -10000)
            while not pile.is_empty:
                if Bot.Partie.finito or len(pile.peek) == 0 or pile.height > Bot.PROFONDEUR:
                    scores[i] += Bot.Partie.get_score()
                    pile.pop()
                    if not pile.is_empty:
                        #print(" <- ",sc)
                        s = sc.pop()
                        if (s != 0):
                            pass
                        if Bot.Partie.est_j1:
                            sc.edit(max(sc.peek, s))
                        else:
                            sc.edit(min(sc.peek, s))
                        #print(sc)
                        if len(pile.peek) > 0:
                            pile.peek.pop(0)
                        Bot.Partie.defaire()
                else:
                    Bot.Partie.jouer_coup(pile.peek[0])
                    pile.add(Bot.Partie.coups_legaux())
                    sc.add(10000 if Bot.Partie.est_j1 else -10000)
            #print(sc)
            scores[i] += sc.peek
            Bot.Partie.defaire()
            i += 1
        #print(scores)
        return Bot.get_min(scores, choix) if cote else Bot.get_max(scores, choix)