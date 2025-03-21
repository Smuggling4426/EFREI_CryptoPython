from cryptography.fernet import Fernet
from flask import Flask, render_template
import sqlite3
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Clé générée à chaque exécution → non persistante !
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

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
