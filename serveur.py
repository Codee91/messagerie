from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import sqlite3
from database import register_user, verify_user, get_users

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}  # Stocke les utilisateurs connectés

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if verify_user(username, password):
            session["username"] = username
            return redirect(url_for("chat"))
        else:
            return "Identifiants incorrects"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if register_user(username, password):
            return redirect(url_for("login"))
        else:
            return "Nom d'utilisateur déjà pris"
    return render_template("register.html")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["username"])

@app.route("/get_users")
def get_users_route():
    """Renvoie la liste des utilisateurs inscrits"""
    if "username" not in session:
        return jsonify({"users": []})
    return jsonify({"users": get_users()})

@socketio.on("register_user")
def register_user(data):
    """Enregistre l'utilisateur dans la liste des connectés"""
    username = data.get("username")
    if username:
        connected_users[username] = request.sid
        emit("update_users", list(connected_users.keys()), broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    """Supprime l'utilisateur déconnecté"""
    username = None
    for user, sid in list(connected_users.items()):
        if sid == request.sid:
            username = user
            break
    if username:
        del connected_users[username]
        emit("update_users", list(connected_users.keys()), broadcast=True)

@socketio.on("message")
def handle_message(data):
    """Gère l'envoi des messages"""
    sender = None
    for user, sid in connected_users.items():
        if sid == request.sid:
            sender = user
            break
    if not sender:
        sender = "Anonyme"

    recipient = data.get("recipient", "Général")
    msg = data["message"]

    if recipient == "Général":
        send(f"{sender}: {msg}", broadcast=True)
    else:
        recipient_sid = connected_users.get(recipient)
        if recipient_sid:
            emit("private_message", {"sender": sender, "message": msg}, room=recipient_sid)
            emit("private_message", {"sender": sender, "message": msg}, room=request.sid)  # Réafficher à l'envoyeur

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
