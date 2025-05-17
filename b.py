import socket

host = "127.0.0.1"  # Doit correspondre à l'adresse du serveur
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    message = input("Vous: ")
    client_socket.send(message.encode())
    if message.lower() == "exit":
        break
    response = client_socket.recv(1024).decode()
    print(f"Serveur: {response}")

client_socket.close()
