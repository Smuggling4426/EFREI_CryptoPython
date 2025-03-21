from cryptography.fernet import Fernet
from flask import Flask, render_template, request
import base64

app = Flask(__name__)

# 🔑 Fonction pour générer une clé Fernet valide à partir d'une clé utilisateur
def generate_key_from_input(user_key):
    while len(user_key) < 32:
        user_key += "0"  # Remplir jusqu'à 32 caractères
    user_key = user_key[:32]  # Tronquer si trop long
    key_bytes = user_key.encode()
    return base64.urlsafe_b64encode(key_bytes)  # Convertir en clé Fernet valide

@app.route("/", methods=["GET", "POST"])
def index():
    encrypted_text = ""
    decrypted_text = ""

    if request.method == "POST":
        action = request.form.get("action")
        user_key = request.form.get("user_key")
        value = request.form.get("value")

        if not user_key or not value:
            return render_template("index.html", encrypted_text="Erreur : Remplissez tous les champs", decrypted_text="")

        key = generate_key_from_input(user_key)
        fernet = Fernet(key)

        try:
            if action == "encrypt":
                encrypted_bytes = fernet.encrypt(value.encode())
                encrypted_text = base64.urlsafe_b64encode(encrypted_bytes).decode()
            elif action == "decrypt":
                decoded_val = base64.urlsafe_b64decode(value.encode())
                decrypted_text = fernet.decrypt(decoded_val).decode()
        except Exception as e:
            return render_template("index.html", encrypted_text=f"Erreur : {str(e)}", decrypted_text="")

    return render_template("index.html", encrypted_text=encrypted_text, decrypted_text=decrypted_text)

if __name__ == "__main__":
    app.run(debug=True)
