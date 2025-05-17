from bot import Bot
from puissance4 import *
import reseaux as R
from time import sleep
from os import system

def demander(quest: str, rep1, rep2) -> bool:
    global reset
    print(quest, "{(1)" + rep1, "(2)" + rep2 + "}")
    re = ""
    while re != "1" and re != "2":
        re = input(">>>")
    return re == "1"

class JoueurRecoie(Joueur):
    def __init__(self, nom, char, t, connec: R.Client):
        super().__init__(nom, char, t)
        self.con = connec

    def choisir(self, choix):
        return int(self.con.recevoir())

class JoueurEnvoie(Joueur):
    def __init__(self, nom, char, t, connec: R.Server):
        super().__init__(nom, char, t)
        self.con = connec

    def choisir(self, choix):
        c = super().choisir(choix)
        self.con.send(c)
        return c

if __name__ == "__main__":
    reset = True
    while reset:
        system('cls')
        if demander("jouer", "local", "en ligne"):
            if demander("jouer", "multijoueur", "contre l'ordinateur"):
                j1 = Joueur("player1", "X", 60 * 5)
                j2 = Joueur("player2", "O", 60 * 5)
            else:
                if demander("qui joue en premier ?", "moi", "ordi"):
                    j1 = Joueur("player", "X", 60 * 5)
                    j2 = Bot("ordi", "O", 60 * 5)
                else:
                    j1 = Bot("ordi", "X", 60 * 5)
                    j2 = Joueur("player", "O", 60 * 5)
        else:
            if demander("", "etre hote", "rejoindre"):
                error = True
                while error:
                    try:
                        hote = R.Server("127.0.0.1")
                        error = False
                    except:
                        print("erreur")
                hote.send(input("message de bienvenue > "))
                print("adversaire:", '"'+hote.recevoir()+'"')
                joueprems = demander("qui joue en premier ?", "moi", "adversaire")
                hote.send("d" if joueprems else "p")
                if (joueprems):
                    print("Vous jouez en premier.")
                    j1 = JoueurEnvoie("vous", "X", 60, hote)
                    j2 = JoueurRecoie("adversaire", "O", 60, hote)
                else:
                    print("Vous jouez en deuxieme.")
                    j1 = JoueurRecoie("adversaire", "X", 60, hote)
                    j2 = JoueurEnvoie("vous", "O", 60, hote)
            else:
                error = True
                while error:
                    try:
                        cli = R.Client(input("Adresse IPv4 de votre adversiare > "))
                        error = False
                    except:
                        print("erreur")
                print("adversaire:", '"'+cli.recevoir()+'"')
                cli.send(input("message de presentation > "))
                if (cli.recevoir() == "d"):
                    print("Vous jouez en deuxieme.")
                    j1 = JoueurRecoie("adversaire", "X", 60, cli)
                    j2 = JoueurEnvoie("vous", "O", 60, cli)
                else:
                    print("Vous jouez en premier.")
                    j1 = JoueurEnvoie("vous", "X", 60, cli)
                    j2 = JoueurRecoie("adversaire", "O", 60, cli)

        partie = Partie(Vecteur(7, 6), 4, j1, j2)
        Bot.set_partie_ref(partie)
        partie.afficher()
    
        print(partie.j1, partie.j2)
        while not partie.finito:
            coup = partie.joueur.choisir(partie.coups_legaux())
            partie.jouer_coup(coup)
            partie.afficher()

        sleep(1)
        print(partie.j1.nom if partie.est_j1 else partie.j2.nom, "a ganee !!!!!!")
        sleep(1)
        input("ok.")
            
input("finito!")