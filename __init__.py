from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import base64, hashlib

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    encrypted_text = ""
    decrypted_text = ""

    if request.method == "POST":
        user_key = request.form.get("user_key")   # Clé personnelle saisie
        value = request.form.get("value")         # Texte à chiffrer/déchiffrer
        action = request.form.get("action")       # "encrypt" ou "decrypt"

        if user_key and value and action:
            try:
                # On dérive la clé Fernet depuis la clé utilisateur (pour la démo)
                derived_key = base64.urlsafe_b64encode(hashlib.sha256(user_key.encode()).digest())
                f = Fernet(derived_key)

                if action == "encrypt":
                    encrypted_text = f.encrypt(value.encode()).decode()
                elif action == "decrypt":
                    decrypted_text = f.decrypt(value.encode()).decode()

            except Exception as e:
                # En cas d'erreur (mauvaise clé, etc.)
                if action == "encrypt":
                    encrypted_text = f"Erreur : {e}"
                else:
                    decrypted_text = f"Erreur : {e}"

    # On renvoie les valeurs calculées au template
    return render_template("index.html",
                           encrypted_text=encrypted_text,
                           decrypted_text=decrypted_text)

if __name__ == "__main__":
    app.run(debug=True)
