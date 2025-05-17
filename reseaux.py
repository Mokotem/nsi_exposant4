import puissance4 as P
import socket as S

PORT = 5555
SIZE = 512

class Client:
    def __init__(self, adre: str):
        self.client = S.socket(S.AF_INET, S.SOCK_STREAM)
        self.addresse = (adre, PORT)
        self.client.connect(self.addresse)

    def recevoir(self):
        return self.client.recv(SIZE).decode()

    def send(self, data):
        self.client.send(str.encode(str(data)))

class Server:
    def __init__(self, adre: str):
        self.sock = S.socket(S.AF_INET, S.SOCK_STREAM)
        self.sock.bind(("", PORT))
        self.sock.listen()
        print("en attente d'une connection...")
        self.con, adr = self.sock.accept()
        print("connectee!")


    def send(self, data: int):
        self.con.send(str.encode(str(data)))

    def recevoir(self) -> int:
        return self.con.recv(SIZE).decode()

    def close(self):
        print("connection perdue.")
        self.con.close()