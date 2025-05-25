from puissance4 import *
from random import choice, choices
from time import sleep

class Bot(Joueur):
    Partie = None

    def __init__(self, prenom, pion, t, prof):
        super().__init__(prenom, pion, t)
        self.PROFONDEUR = prof
        
    @staticmethod
    def set_partie_ref(partie):
        Bot.Partie = partie

    @staticmethod
    def get_min(l: list, exept):
        m = 99999999
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
        m = -99999999
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
        profon = self.PROFONDEUR + ((Bot.Partie.dimention.x - len(choix)) // 2)
        cote = Bot.Partie.est_j1
        taille = Bot.Partie.dimention.x
        scores = [0] * taille
        k = 0
        for i in choix:
            print("en attente de ordi...  |" + ("-" * k) + (" " * (len(choix) - k)) + "| "\
                + str(round(k * 100 / len(choix))) + "%", end = "\r")
            k += 1
            sc = PileMaisNormal()
            sc.add(Bot.Partie.get_pire() * 10000)
            Bot.Partie.jouer_coup(i)
            if Bot.Partie.finito:
                Bot.Partie.defaire()
                return i
            pile = PileMaisNormal()
            pile.add(Bot.Partie.coups_legaux())
            while not pile.is_empty:
                if Bot.Partie.finito or pile.height > profon or len(pile.peek) == 0:
                    if len(pile.peek) > 0:
                        a = Bot.Partie.get_score()
                        sc.edit(a * 10000)
                        #scores[i] += a
                    #print(sc)
                    pile.pop()
                    if pile.is_empty:
                        #print("to score =>",sc)
                        scores[i] += sc.peek
                    else:
                        s = sc.pop()
                        if Bot.Partie.est_j1:
                            sc.edit(min(s, sc.peek))
                        else:
                            sc.edit(max(s, sc.peek))

                    Bot.Partie.defaire()
                    #print(sc)
                else:
                    sc.add(Bot.Partie.get_pire() * 10000)
                    Bot.Partie.jouer_coup(pile.peek[0])
                    pile.peek.pop(0)
                    pile.add(Bot.Partie.coups_legaux())

        print("en attente de ordi...  |" + ("-" * len(choix)) + "| 100%")

            
        print(scores)
        #print(Bot.Partie.est_j1)
        return Bot.get_max(scores, choix) if cote else Bot.get_min(scores, choix)