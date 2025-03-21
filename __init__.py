from cryptography.fernet import Fernet
from flask import Flask, render_template
import os

app = Flask(__name__)

# Fonction pour charger ou générer une clé persistante
def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Assure-toi que hello.html existe

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    try:
        valeur_bytes = valeur.encode()
        token = f.encrypt(valeur_bytes)
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur d'encryptage : {str(e)}"

@app.route('/decrypt/<string:valeur>')
def decryptage(valeur):
    try:
        valeur_bytes = valeur.encode()
        decrypted = f.decrypt(valeur_bytes)
        return f"Valeur décryptée : {decrypted.decode()}"
    except Exception as e:
        return f"Erreur de déchiffrement : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
