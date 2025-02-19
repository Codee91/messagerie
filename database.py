import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "chat.db"

def init_db():
    """Crée la base de données et la table users si elles n'existent pas"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("[✔] Base de données initialisée avec succès !")
    except Exception as e:
        print(f"[❌] Erreur lors de l'initialisation de la base de données : {e}")

def register_user(username, password):
    """Enregistre un utilisateur avec un mot de passe haché"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False

        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[❌] Erreur lors de l'inscription : {e}")
        return False

def verify_user(username, password):
    """Vérifie si un utilisateur existe et si son mot de passe est correct"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        return row and check_password_hash(row[0], password)
    except Exception as e:
        print(f"[❌] Erreur lors de la vérification de l'utilisateur : {e}")
        return False

def get_users():
    """Récupère la liste des utilisateurs inscrits"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
    except Exception as e:
        print(f"[❌] Erreur lors de la récupération des utilisateurs : {e}")
        return []
