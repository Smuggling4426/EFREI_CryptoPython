from cryptography.fernet import Fernet
from flask import Flask, render_template
import base64
import traceback  # Ajouté pour afficher les erreurs complètes

app = Flask(__name__)

# 🔑 Fonction pour générer une clé Fernet valide à partir d'une clé utilisateur
def generate_key_from_input(user_key):
    while len(user_key) < 32:
        user_key += "0"  # Remplir jusqu'à 32 caractères
    user_key = user_key[:32]  # Tronquer si trop long
    key_bytes = user_key.encode()
    return base64.urlsafe_b64encode(key_bytes)  # Convertir en clé Fernet valide

@app.route('/')
def index():
    return render_template('index.html')  # Assure-toi que "index.html" est bien présent

# 🔐 Route pour chiffrer avec une clé personnalisée
@app.route('/encrypt/<user_key>/<val>')
def encrypt(user_key, val):
    try:
        key = generate_key_from_input(user_key)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(val.encode())
        encrypted_safe = base64.urlsafe_b64encode(encrypted).decode()  # Encodage URL-safe
        return encrypted_safe
    except Exception as e:
        return f"Erreur d'encryption : {str(e)}\n{traceback.format_exc()}"  # Afficher l'erreur complète

# 🔓 Route pour déchiffrer avec une clé personnalisée
@app.route('/decrypt/<user_key>/<val>')
def decrypt(user_key, val):
    try:
        key = generate_key_from_input(user_key)
        fernet = Fernet(key)
        val = base64.urlsafe_b64decode(val.encode())  # Décodage URL-safe
        decrypted = fernet.decrypt(val)
        return decrypted.decode()
    except Exception as e:
        return f"Erreur de déchiffrement : {str(e)}\n{traceback.format_exc()}"  # Afficher l'erreur complète

if __name__ == "__main__":
    app.run(debug=True)  # 🔍 Active le mode debug pour voir les erreurs dans le terminal
