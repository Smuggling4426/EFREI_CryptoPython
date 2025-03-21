from cryptography.fernet import Fernet
from flask import Flask, render_template
import base64

app = Flask(__name__)

# 🔑 Fonction pour générer une clé à partir de la saisie utilisateur
def generate_key_from_input(user_key):
    key_bytes = user_key.encode().ljust(32, b'0')[:32]  # Pad ou tronquer à 32 bytes
    return base64.urlsafe_b64encode(key_bytes)

@app.route('/')
def index():
    return render_template('index.html')  # Assure-toi d'avoir "index.html" dans le même dossier que app.py

# 🔐 Route pour chiffrer avec une clé personnalisée
@app.route('/encrypt/<user_key>/<val>')
def encrypt(user_key, val):
    try:
        key = generate_key_from_input(user_key)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(val.encode())
        return encrypted.decode()
    except Exception as e:
        return f"Erreur d'encryption : {str(e)}"

# 🔓 Route pour déchiffrer avec une clé personnalisée
@app.route('/decrypt/<user_key>/<val>')
def decrypt(user_key, val):
    try:
        key = generate_key_from_input(user_key)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(val.encode())
        return decrypted.decode()
    except Exception as e:
        return f"Erreur de déchiffrement : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
