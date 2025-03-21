from cryptography.fernet import Fernet
from flask import Flask, render_template
import os

app = Flask(__name__)

# 📌 Fonction pour charger ou générer une clé persistante
KEY_FILE = "secret.key"

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

# Charger la clé une seule fois au démarrage
key = load_key()
fernet = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Assure-toi que hello.html existe

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    try:
        token = fernet.encrypt(valeur.encode())
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur d'encryptage : {str(e)}"

@app.route('/decrypt/<string:valeur>')
def decryptage(valeur):
    try:
        decrypted = fernet.decrypt(valeur.encode())
        return f"Valeur décryptée : {decrypted.decode()}"
    except Exception as e:
        return f"Erreur de déchiffrement : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
