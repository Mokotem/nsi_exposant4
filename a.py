import socket

host = "127.0.0.1"  # Adresse locale
port = 12345        # Port d'écoute

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Serveur en attente de connexion sur {host}:{port}...")
client_socket, client_address = server_socket.accept()
print(f"Connexion acceptée de {client_address}")

while True:
    message = client_socket.recv(1024).decode()
    if message.lower() == "exit":
        break
    print(f"Client: {message}")
    response = input("Vous: ")
    client_socket.send(response.encode())

client_socket.close()
server_socket.close()
