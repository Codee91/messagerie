import socket
import threading

SERVER_IP = "127.0.0.1"
PORT = 12345

def receive_messages(client_socket):
    """Réception des messages du serveur"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\nMessage reçu : {message.decode()}")
        except:
            break

def start_client():
    """Connexion au serveur et interaction"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input("Vous : ")
        client_socket.send(message.encode())

if __name__ == "__main__":
    start_client()
