from puissance4 import *
from time import sleep
import server as S
from bot import *
import graphismes as G
from threading import Thread
from os import system
from variante import PartieTetris

def clearconsole(): system("cls")

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
        result += "(" + str(i + 1) + ")" + choix[i] + ", "
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


def demanderProfondeur() -> tuple:
    match demanderL("difficulte", "force 1", "force 2", "force 3", "max (lent!)"):
        case 0:
            return (2, "ordi force 1")
        case 1:
            return (4, "ordi force 2")
        case 2:
            return (5, "ordi force 3")
        case 3:
            return (6, "ordi max")

def JouerEnLocal():
    clearconsole()
    txt_demander_temps = "limite de temps (sec) {0: pas de limite} = "
    global j1
    global j2
    global tetris
    if demander("jouer", "multijoueur", "contre l'ordinateur"):
        tetris = not demander("variante", "classique", "tetris")
        tmps = int(input(txt_demander_temps))
        j1 = Joueur("player 1", "O", tmps)
        j2 = Joueur("player 2", "X", tmps)
    else:
        tetris = not demander("variante", "classique", "tetris")
        if demander("qui joue en premier ?", "moi", "bot"):
            tmps = int(input(txt_demander_temps))
            j1 = Joueur("player", "O", tmps)
            pr = demanderProfondeur()
            j2 = Bot(pr[1], "X", -1, pr[0])
        else:
            tmps = int(input(txt_demander_temps))
            pr = demanderProfondeur()
            j1 = Bot(pr[1], "O", -1, pr[0])
            j2 = Joueur("player", "X", tmps)
    Jouer(False)


def JouerEnReseau():
    clearconsole()
    global j1
    global j2
    global tetris
    hotepartie = None
    en_ligne = True
    name = input("pseudonyme > ")
    while len(name) < 3 or len(name) > 16 or name == "b":
        print("ce nom n'est pas autorise.")
        name = input("pseudonyme > ")
    error = True
    print("Connection au serveur ...")
    while error:
        try:
            hotepartie = S.Machine()
            error = False
        except Exception as e:
            print(e)
            input("ok. retour au menu principale")
            G.StartMenu()
    if (hotepartie.sock.recv(S.Client.SIZE) == S.Server.CONNECTION_REUSSI):
        print("Connection reussi avec le serveur !!! un coca ?")
    hotepartie.Envoyer(name)
    h = 2
    while h == 2:
        serv = S.Server.Decode(hotepartie.sock.recv(S.Client.SIZE).decode())
        S.Server.AfficherParties(serv[0], serv[1], serv[2])
        h = demanderL("", "etre hote", "rejoindre", "rafraichir")
        if h == 0:
            rep = "hh"
        elif h == 1:
            rep = 0
            while rep < 1 or rep > len(serv[0]):
                rep = int(input("numero de partie > "))
            rep = str(rep)
            if len(rep) < 2:
                rep = "0" + rep
        else:
            hotepartie.Envoyer("ra")

        if (h < 2):
            adversaire = ""
            hotepartie.Envoyer(rep)
            if (h == 0):
                # HOTE
                print(hotepartie.Recevoir())
                adversaire = hotepartie.Recevoir()
                print(adversaire, "a rejoin la partie.")
                hotepartie.Envoyer(input("message de bienvenue > "))
                print(adversaire + ":", '"'+hotepartie.Recevoir()+'"')
                joueprems = demander("qui joue en premier ?", "moi", adversaire)
                hotepartie.Envoyer("d" if joueprems else "p")
                if (joueprems):
                    print("Vous jouez en premier.")
                    j1 = JoueurHote(name, "X", -1, hotepartie)
                    j2 = JoueurReseaux(adversaire, "O", -1, hotepartie)
                else:
                    print("Vous jouez en deuxieme.")
                    j1 = JoueurReseaux(adversaire, "X", -1, hotepartie)
                    j2 = JoueurHote(name, "O", -1, hotepartie)
            else:
                # INVITEE
                adversaire = hotepartie.Recevoir()
                if (adversaire == "b"):
                    print("cette partie est en jeu.")
                    h = 2
                else:
                    print("tu as rejoin la partie de",adversaire)
                    print(adversaire + ":", '"'+hotepartie.Recevoir()+'"')
                    hotepartie.Envoyer(input("message de presentation > "))
                    if (hotepartie.Recevoir() == "d"):
                        print("Vous jouez en deuxieme.")
                        j1 = JoueurReseaux(adversaire, "X", -1, hotepartie)
                        j2 = JoueurHote(name, "O", -1, hotepartie)
                    else:
                        print("Vous jouez en premier.")
                        j1 = JoueurHote(name, "X", -1, hotepartie)
                        j2 = JoueurReseaux(adversaire, "O", -1, hotepartie)
    Jouer(True, hote=hotepartie)


def Jouer(en_ligne: bool, hote = None):
    global j1
    global j2
    global tetris
    partie = None
    if tetris:
        partie = PartieTetris(Vecteur(7, 6), 4, j1, j2)
    else:
        partie = Partie(Vecteur(7, 6), 4, j1, j2)
    Bot.Partie = partie
    clearconsole()
    partie.afficher()
    print("")
    
    while not partie.finito:
        coup = partie.joueur.choisir(partie.coups_legaux())
        if not partie.joueur.reste_du_temps():
            print(partie.joueur.nom, "a perdu au temps !")
            partie.finir()
        else:
            partie.jouer_coup(coup)
            clearconsole()
            partie.afficher()
            print("")
    if en_ligne:
        hote.Envoyer("exit")
    sleep(1)
    partie.changer_de_joueur()
    print(partie.joueur.nom, "a gagnee !!!!!!")
    input("ok. retour au menu principale")
    G.StartMenu()

j1 = None
j2 = None
tetris = False
G.OnLocalSelected = JouerEnLocal
G.OnOnlineSelected = JouerEnReseau

if __name__ == "__main__":
    G.StartMenu()