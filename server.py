import socket as Sock
import threading as Thread
from time import sleep

class Machine:  # client chez la machine de l'utilisateur
    SERVER_ADRESS = "192.168.142.168"
    
    def __init__(self):
        self.sock = Sock.socket(Sock.AF_INET, Sock.SOCK_STREAM)
        self.sock.connect((Machine.SERVER_ADRESS, Server.PORT))
        
    def Deco(self):
        self.sock.send(Server.ADVERSAIRE_DECONNECTE)
        
    def Envoyer(self, message: str):
        self.sock.send(str(message).encode())

    def Recevoir(self):
        return self.sock.recvfrom(Client.SIZE)[0].decode()

class Client:  # client chez le serveur
    SIZE = 512
    def __init__(self, conn: Sock.socket, adress: str, name: str):
        self.CONNECTION = conn
        self.ADRESS = adress
        self.NAME = name
        
    def Envoyer(self, message: str):
        self.CONNECTION.send(message.encode())
        
    def Recevoir(self):
        return self.CONNECTION.recv(Client.SIZE).decode()
    
class Partie:
    def __init__(self, host: Client, code = ""):
        self.bloque = False
        self.host = host
        self.invitee =  None
        host.Envoyer("Tu as cree une partie. En attente d'un adversaire ...")
        self.running = True
        if len(code) == 4:
            self.code = code.lower()
            self.hasCode = True
        else:
            self.code = ""
            self.hasCode = False
        self.hostISFirst = True
        
    def Rejoindre(self, invitee: Client):
        self.bloque = True
        self.invitee = invitee

        # messages de presentations
        try:
            self.host.Envoyer(invitee.NAME)
            invitee.Envoyer(self.host.NAME)
            data = self.host.CONNECTION.recv(Client.SIZE)
            self.invitee.CONNECTION.send(data)
            data = self.invitee.CONNECTION.recv(Client.SIZE)
            self.host.CONNECTION.send(data)
        
            data = self.host.CONNECTION.recv(Client.SIZE)
            self.invitee.CONNECTION.send(data)
            if data.decode() == "p":
                data = self.invitee.CONNECTION.recv(Client.SIZE)
                self.host.CONNECTION.send(data)
                tache = Thread.Thread(target=self.Tache_Communication)
                tache.start()
        except:
            self.bloque = True
            self.running = False
        
    def Tache_Communication(self):
        while self.running:
            try:
                data = self.host.CONNECTION.recv(Client.SIZE)
                if data.decode() == "exit":
                    self.running = False
                    self.invitee.Envoyer("deco")
                else:
                    self.invitee.CONNECTION.send(data)
                    data = self.invitee.CONNECTION.recv(Client.SIZE)
                    if data.decode() == "exit":
                        self.host.Envoyer("deco")
                        self.invitee = None
                        self.bloque = False
                    else:
                        self.host.CONNECTION.send(data)
            except:
                self.bloque = True
                self.running = False

class Server:
    PORT = 8080
    PARTIE_LIMIT = 8
    PARTIE_BLOQUEE = "b".encode()
    CODE_REQUI = "c".encode()
    ADVERSAIRE_DECONNECTE = "d".encode()
    CREER_PARTIE = "h".encode()
    CONNECTION_REUSSI = "r".encode()
    
    def __init__(self):
        self.socket = Sock.socket(Sock.AF_INET, Sock.SOCK_STREAM)
        self.socket.bind((Machine.SERVER_ADRESS, Server.PORT))
        self.nombreDeConnec = 0
        self.running = True
        self.parties = list()  # liste de 'Partie'
        self.socket.listen()
        tache1 = Thread.Thread(target=self.Tache_Connections)
        tache1.start()
        tache2 = Thread.Thread(target=self.Tache_Nettoyage)
        tache2.start()
        
    def Tache_Nettoyage(self):
        while self.running:
            sleep(1)
            i = 0
            while i < len(self.parties):
                if (not self.parties[i].running):
                    self.parties.pop(i)

    def Tache_Connections(self):
        while self.running:
            print("en attente d'une connection")
            ar = self.socket.accept()
            tache = Thread.Thread(\
            target=self.Tache_Accueillir,\
            args=ar)
            tache.start()
            
    def Tache_Accueillir(self, conn: Sock.socket, adre: str):
        conn.send(Server.CONNECTION_REUSSI)
        requete = conn.recv(Client.SIZE).decode()
        c = Client(conn, adre, requete)
        self.nombreDeConnec += 1
        requete = "ra"
        while requete == "ra":
            conn.send(self.Encode().encode())
            requete = conn.recv(Client.SIZE).decode()
            if (requete == "hh"):
                p = Partie(c)
                self.parties.append(p)
                data = Server.Decode(self.Encode())
                self.AfficherParties(data[0], data[1], data[2])
            elif requete[0] != "r":
                id_partie = int(requete) - 1
                if self.parties[id_partie].bloque:
                    conn.send(Server.PARTIE_BLOQUEE)
                    requete = "ra"
                elif self.parties[id_partie].hasCode:
                    conn.send(Server.CODE_REQUI)
                else:
                    self.parties[id_partie].Rejoindre(c)
           
    @staticmethod
    def AfficherParties(names: list, codes: list, nombre_bloque: int):
        t = len(names)
        if t > Server.PARTIE_LIMIT or t != len(codes):
            raise Exception("parties depassent la limite de "\
                + str(Server.PARTIE_LIMIT) + " parties")
        print("SERVEUR:")
        print("Parties:", str(t) + "/" + str(Server.PARTIE_LIMIT))
        i = 0
        while i < Server.PARTIE_LIMIT:
            if i < t - int(nombre_bloque):
                if not codes[i]:
                    print("    ("+str(i + 1)+") {mdp requis}  hote:", names[i])
                else:
                    print("    ("+str(i + 1)+")  hote:", names[i])
            elif i < t + int(nombre_bloque) - 1:
                print("    En jeu.  hote:", names[i])
            else:
                print("    ... vide")
            i += 1
    
    def Encode(self) -> str:
        names = ""
        codes = ""
        nombrebloque = 0
        i = 0
        while i < len(self.parties):
            names += self.parties[i].host.NAME + ","
            codes += ("1" if self.parties[i].hasCode else "0")
            if self.parties[i].bloque: nombrebloque += 1
            i += 1
        names.removesuffix(",")
        return names + "/" + codes + "/" + str(nombrebloque)
    
    @staticmethod
    def Decode(serv: str) -> tuple:
        lst = serv.split("/")
        fnames = lst[0].split(",")
        fnames.pop(fnames.__len__() - 1)
        return fnames, [bool(b) for b in lst[1]], int(lst[2])
    
if __name__ == "__main__":
    serv = Server()
    while True:
        input("rafraichir")
        d = serv.Encode()
        print(d)
        data = Server.Decode(d)
        print(data)
        serv.AfficherParties(data[0], data[1], data[2])
        