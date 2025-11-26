from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def dashboard():
    try:
        capteurs = requests.get("http://127.0.0.1:6000/last6").json()
    except:
        capteurs = []
    return render_template("index.html", capteurs=capteurs)

if __name__ == "__main__":
    app.run(debug=True)
