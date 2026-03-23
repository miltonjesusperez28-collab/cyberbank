from flask import Flask, render_template_string, request, redirect, session, url_for
import json, os, random, datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(name)
app.secret_key = "ultra_secret_key"

archivo = "usuarios.json"

def cargar():
    if not os.path.exists(archivo):
        return {}
    with open(archivo) as f:
        return json.load(f)

def guardar(data):
    with open(archivo, "w") as f:
        json.dump(data, f, indent=4)

def generar_tarjeta():
    return " ".join(str(random.randint(1000,9999)) for _ in range(4))

usuarios = cargar()

html = """
<!DOCTYPE html>
<html>
<head>
<title>Cyber Bank</title>

<style>
body {
    margin:0;
    background:black;
    color:white;
    font-family:sans-serif;
}

/* fondo calavera */
body::before {
    content:"";
    background:url('{{ url_for("static", filename="calavera.png") }}') no-repeat center;
    background-size:cover;
    opacity:0.1;
    position:fixed;
    width:100%;
    height:100%;
    z-index:-2;
}

.container {
    width:350px;
    margin:50px auto;
}

/* tarjeta */
.card {
    background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
    border-radius:20px;
    padding:20px;
    color:#00ffcc;
    box-shadow:0 10px 40px rgba(0,255,200,0.4);
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0% {transform:translateY(0px);}
    50% {transform:translateY(-10px);}
    100% {transform:translateY(0px);}
}

/* inputs */
input, button {
    width:100%;
    padding:10px;
    margin:5px 0;
    border:none;
    border-radius:10px;
}

button {
    background:#00ffcc;
    color:black;
    font-weight:bold;
}

/* historial */
ul {
    max-height:150px;
    overflow:auto;
}
</style>

</head>
<body>

<div class="container">

<h2>💀 Cyber Bank</h2>

{% if not session.get("user") %}

<form method="post">
<input name="user" placeholder="Usuario">
<input name="pass" type="password" placeholder="Password">
<button name="action" value="login">Entrar</button>
<button name="action" value="register">Registrar</button>
</form>

<p>{{msg}}</p>

{% else %}

<h3>Bienvenido {{session["user"]}}</h3>

<div class="card">
<p>💳 {{tarjeta}}</p>
<p>{{session["user"]}}</p>
<h2>${{saldo}}</h2>
</div>

<form method="post">
<input name="monto" placeholder="Monto">
<button name="action" value="deposit">Depositar</button>
<button name="action" value="transfer">Transferir</button>
</form>

<h4>Historial</h4>
<ul>
{% for h in historial %}
<li>{{h}}</li>
{% endfor %}
</ul>

<form method="post">
<button name="action" value="logout">Cerrar sesión</button>
</form>

{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    global usuarios
    msg = ""

    if request.method == "POST":
        action = request.form.get("action")
        u = request.form.get("user")
        p = request.form.get("pass")

        usuarios = cargar()

        if action == "register":
            if u not in usuarios:
                usuarios[u] = {
                    "password": generate_password_hash(p),
                    "saldo": 0,
                    "historial": [],
                    "tarjeta": generar_tarjeta()
                }
                guardar(usuarios)
                msg = "Usuario creado"

        elif action == "login":
            if u in usuarios and check_password_hash(usuarios[u]["password"], p):
                session["user"] = u
            else:
                msg = "Error login"

        elif action == "logout":
            session.pop("user", None)

        elif session.get("user"):
            user = session["user"]
            monto = float(request.form.get("monto", 0))
            fecha = datetime.datetime.now().strftime("%d/%m %H:%M")

            if action == "deposit":
                usuarios[user]["saldo"] += monto
                usuarios[user]["historial"].append(f"{fecha} +${monto}")elif action == "transfer":
                if monto <= usuarios[user]["saldo"]:
                    usuarios[user]["saldo"] -= monto
                    usuarios[user]["historial"].append(f"{fecha} -${monto}")
                else:
                    msg = "Saldo insuficiente"

            guardar(usuarios)

        return redirect("/")

    if session.get("user"):
        user = session["user"]
        data = usuarios[user]
        return render_template_string(html,
            saldo=data["saldo"],
            historial=data["historial"],
            tarjeta=data["tarjeta"],
            msg=msg)

    return render_template_string(html, msg=msg)


# 🔥 IMPORTANTE PARA RENDER
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)