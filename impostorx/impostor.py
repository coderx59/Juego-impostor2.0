import random
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones"
df = pd.read_csv("cartas_clash_royale.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cant = int(request.form["cantidad"])
        recordar = "recordar" in request.form
        session["cantidad"] = cant
        session["recordar"] = recordar
        return redirect(url_for("inicio_ronda"))
    return render_template("impos_index.html")

@app.route("/inicio_ronda", methods=["GET", "POST"])
def inicio_ronda():
    if request.method == "POST":
        cant = session.get("cantidad", 0)
        palabra = random.choice(df["nombre_carta"].tolist())
        seleccion = ["impostor"] + [palabra] * (cant - 1)
        random.shuffle(seleccion)
        session["roles"] = seleccion
        session["turno"] = 0
        return redirect(url_for("turno"))
    return render_template("inicio_ronda.html")

@app.route("/turno", methods=["GET", "POST"])
def turno():
    roles = session.get("roles", [])
    turno_actual = session.get("turno", 0)

    if turno_actual >= len(roles):
        return render_template("fin.html")

    rol = roles[turno_actual]

    if request.method == "POST":
        session["turno"] = turno_actual + 1
        return redirect(url_for("turno"))

    return render_template("turno.html", numero=turno_actual + 1, rol=rol)

@app.route("/otra_ronda", methods=["POST"])
def otra_ronda():
    if session.get("recordar", False):
        # Si el usuario marcó "recordar", usa el mismo número de participantes
        return redirect(url_for("inicio_ronda"))
    else:
        # Si no, vuelve a pedir el número de participantes
        return redirect(url_for("index"))

@app.route("/fin_juego")
def fin_juego():
    return render_template("fin_juego.html")

if __name__ == "__main__":
    app.run(debug=True)
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
