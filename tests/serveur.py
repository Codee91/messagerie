import socket
import threading

import socket
import threading

# Configuration du serveur
HOST = '0.0.0.0'  # Accepte toutes les connexions entrantes
PORT = 12345       # Port d'écoute
clients = []

def broadcast(message, sender_socket):
    """Envoie un message à tous les clients sauf l'expéditeur"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    """Gère la communication avec un client spécifique"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Message reçu: {message.decode()}")
            broadcast(message, client_socket)
        except:
            break
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    """Lance le serveur de chat"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Serveur démarré sur {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Nouvelle connexion: {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()