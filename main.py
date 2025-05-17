from puissance4 import *
from time import sleep
import server as S
from bot import *

def demander(quest: str, rep1, rep2) -> bool:
    print(quest, "{(1)" + rep1, "(2)" + rep2 + "}")
    re = ""
    while re != "1" and re != "2":
        re = input(">>>")
    return re == "1"

def demanderL(quest: str, *choix) -> bool:
    result = ""
    c = list()
    i = 0
    while i < len(choix):
        result += "(" + str(i + 1) + ") " + choix[i] + ", "
        c.append(str(i + 1))
        i += 1
    result.removesuffix(", ")
    print(quest, result)
    re = ""
    while not re in c:
        re = input(">>>")
    return int(re) - 1

class JoueurReseaux(Joueur):
    def __init__(self, nom, char, t, connec: S.Machine):
        super().__init__(nom, char, t)
        self.con = connec

    def choisir(self, choix):
        print("En attente de", self.nom, "...")
        return int(self.con.sock.recvfrom(S.Client.SIZE)[0].decode())

class JoueurHote(Joueur):
    def __init__(self, nom, char, t, connec: S.Machine):
        super().__init__(nom, char, t)
        self.con = connec

    def choisir(self, choix):
        c = super().choisir(choix)
        self.con.Envoyer(c)
        return c


if __name__ == "__main__":
    if demander("jouer", "local", "en ligne"):
        if demander("jouer", "multijoueur", "contre l'ordinateur"):
            j1 = Joueur("player1", "O", 60 * 5)
            j2 = Joueur("player2", "X", 60 * 5)
        else:
            if demander("qui joue en premier ?", "moi", "bot"):
                j1 = Joueur("player1", "O", 60 * 5)
                j2 = Bot("player2", "X", 60 * 5)
            else:
                j1 = Bot("player1", "O", 60 * 5)
                j2 = Joueur("player2", "X", 60 * 5)
    else:
        name = input("pseudonyme > ")
        error = True
        print("Connection au serveur ...")
        while error:
            try:
                hote = S.Machine()
                error = False
            except Exception as e:
                print(e)
        if (hote.sock.recv(S.Client.SIZE) == S.Server.CONNECTION_REUSSI):
            print("Connection reussi avec le serveur !!! un coca ?")
        hote.Envoyer(name)
        h = 2
        while h == 2:
            serv = S.Server.Decode(hote.sock.recv(S.Client.SIZE).decode())
            S.Server.AfficherParties(serv[0], serv[1], serv[2])
            h = demanderL("", "etre hote", "rejoindre", "rafraichir")
            if h == 0:
                rep = "hh"
            elif h == 1:
                print(" rejoindre une partie ...")
                rep = 0
                while rep < 1 or rep > len(serv[0]):
                    rep = int(input(">>>"))
                rep = str(rep)
                if len(rep) < 2:
                    rep = "0" + rep
            else:
                hote.Envoyer("ra")
        
        adversaire = ""
        hote.Envoyer(rep)
        if (h == 0):
            # HOTE
            print(hote.Recevoir())
            adversaire = hote.Recevoir()
            print(adversaire, "a rejoin la partie.")
            hote.Envoyer(input("message de bienvenue > "))
            print(adversaire + ":", '"'+hote.Recevoir()+'"')
            joueprems = demander("qui joue en premier ?", "moi", adversaire)
            hote.Envoyer("d" if joueprems else "p")
            if (joueprems):
                print("Vous jouez en premier.")
                j1 = JoueurHote(name, "X", 60, hote)
                j2 = JoueurReseaux(adversaire, "O", 60, hote)
            else:
                print("Vous jouez en deuxieme.")
                j1 = JoueurReseaux(adversaire, "X", 60, hote)
                j2 = JoueurHote(name, "O", 60, hote)
        else:
            # INVITEE
            adversaire = hote.Recevoir()
            print("tu as rejoin la partie de",adversaire)
            print(adversaire + ":", '"'+hote.Recevoir()+'"')
            hote.Envoyer(input("message de presentation > "))
            if (hote.Recevoir() == "d"):
                print("Vous jouez en deuxieme.")
                j1 = JoueurReseaux(adversaire, "X", 60, hote)
                j2 = JoueurHote(name, "O", 60, hote)
            else:
                print("Vous jouez en premier.")
                j1 = JoueurHote(name, "X", 60, hote)
                j2 = JoueurReseaux(adversaire, "O", 60, hote)


    partie = Partie(Vecteur(7, 6), 4, j1, j2)
    Bot.Partie = partie
    partie.afficher()
    
    while not partie.finito:
        coup = partie.joueur.choisir(partie.coups_legaux())
        partie.jouer_coup(coup)
        partie.afficher()

    sleep(1)
    print(partie.joueur.nom, "a gagnee !!!!!!")
            
input("finito!")