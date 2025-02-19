import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configuration du serveur
SERVER_IP = "127.0.0.1"
PORT = 12345

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Messagerie - Deux Clients")

        # Zone d'affichage des messages
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", height=15)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Séparation des deux clients
        self.frame_user1 = tk.Frame(root)
        self.frame_user1.pack(fill=tk.X, padx=10, pady=5)
        self.label_user1 = tk.Label(self.frame_user1, text="Utilisateur 1 :")
        self.label_user1.pack(side=tk.LEFT)
        self.entry_user1 = tk.Entry(self.frame_user1)
        self.entry_user1.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_user1.bind("<Return>", lambda event: self.send_message(1))  # Envoi avec Entrée
        self.button_user1 = tk.Button(self.frame_user1, text="Envoyer", command=lambda: self.send_message(1))
        self.button_user1.pack(side=tk.RIGHT)

        self.frame_user2 = tk.Frame(root)
        self.frame_user2.pack(fill=tk.X, padx=10, pady=5)
        self.label_user2 = tk.Label(self.frame_user2, text="Utilisateur 2 :")
        self.label_user2.pack(side=tk.LEFT)
        self.entry_user2 = tk.Entry(self.frame_user2)
        self.entry_user2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_user2.bind("<Return>", lambda event: self.send_message(2))  # Envoi avec Entrée
        self.button_user2 = tk.Button(self.frame_user2, text="Envoyer", command=lambda: self.send_message(2))
        self.button_user2.pack(side=tk.RIGHT)

        # Connexions des deux clients
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket1.connect((SERVER_IP, PORT))

        self.client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket2.connect((SERVER_IP, PORT))

        # Threads pour recevoir les messages
        self.receive_thread1 = threading.Thread(target=self.receive_messages, args=(self.client_socket1, "Utilisateur 1"), daemon=True)
        self.receive_thread1.start()

        self.receive_thread2 = threading.Thread(target=self.receive_messages, args=(self.client_socket2, "Utilisateur 2"), daemon=True)
        self.receive_thread2.start()

    def receive_messages(self, client_socket, username):
        """Réception des messages du serveur et affichage"""
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.display_message(f"{username}: {message}")
            except:
                break

    def display_message(self, message):
        """Affiche un message dans la zone de texte"""
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state="disabled")
        self.text_area.yview(tk.END)

    def send_message(self, user):
        """Envoie un message depuis un des deux utilisateurs"""
        if user == 1:
            message = self.entry_user1.get()
            socket_client = self.client_socket1
            username = "Utilisateur 1"
            self.entry_user1.delete(0, tk.END)
        else:
            message = self.entry_user2.get()
            socket_client = self.client_socket2
            username = "Utilisateur 2"
            self.entry_user2.delete(0, tk.END)

        if message:
            socket_client.send(message.encode())
            self.display_message(f"{username} (Moi): {message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()
