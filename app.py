from flask import Flask, render_template_string, request, redirect, session
import json, os

app = Flask(__name__)
app.secret_key = "secret123"

archivo = "usuarios.json"

def cargar():
    if not os.path.exists(archivo):
        return {}
    with open(archivo) as f:
        return json.load(f)

def guardar(data):
    with open(archivo, "w") as f:
        json.dump(data, f, indent=4)

usuarios = cargar()

html = """
<!DOCTYPE html>
<html>
<head>
<title>Cyber Bank Premium</title>

<style>
body {
    margin:0;
    background:black;
    color:#00ff00;
    font-family:Courier;
}

/* 💀 fondo */
body::before {
    content:"";
    background:url('/static/calavera.png') no-repeat center center;
    background-size:cover;
    opacity:0.12;
    position:fixed;
    width:100%;
    height:100%;
    z-index:-2;
}

body::after {
    content:"";
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.8);
    z-index:-1;
}

/* contenedor */
.container {
    width:350px;
    margin:80px auto;
    text-align:center;
}

/* inputs */
input, button {
    width:90%;
    padding:10px;
    margin:8px;
    background:#111;
    color:#00ff00;
    border:1px solid #00ff00;
}

button:hover {
    background:#00ff00;
    color:black;
}

/* tarjeta */
.card {
    margin-top:20px;
    padding:20px;
    border-radius:15px;
    background:#0a0a0a;
    box-shadow:0 0 20px #00ff00;
}

/* dashboard */
.stats {
    display:flex;
    justify-content:space-between;
    margin-top:10px;
}

.stat {
    border:1px solid #00ff00;
    padding:10px;
    width:45%;
}

/* historial */
ul {
    text-align:left;
    max-height:150px;
    overflow:auto;
}
</style>

</head>
<body>

<div class="container">

<h2>💀 CYBER BANK PREMIUM</h2>

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

<div class="stats">
<div class="stat">💰 ${{saldo}}</div>
<div class="stat">📊 {{historial|length}} mov</div>
</div>

<div class="card">
<h3>💳 TARJETA DIGITAL</h3>
<p>{{session["user"]}}</p>
<p>${{saldo}}</p>
<p>**** **** **** {{saldo|string|length}}123</p>
</div>

<form method="post">
<input name="monto" placeholder="Monto">
<button name="action" value="deposit">Depositar</button>
<button name="action" value="transfer">Transferir</button>
</form>

<h4>📜 Historial</h4>
<ul>
{% for h in historial %}
<li>{{h}}</li>
{% endfor %}
</ul>

<form method="post">
<button name="action" value="logout">Cerrar sesión</button>
</form>

<p>{{msg}}</p>

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

        # REGISTRO
        if action == "register":
            if u not in usuarios:
                usuarios[u] = {"password": p, "saldo": 0, "historial": []}
                guardar(usuarios)
                msg = "✔ Usuario creado"
            else:
                msg = "Ya existe"

        # LOGIN
        elif action == "login":
            if u in usuarios and usuarios[u]["password"] == p:
                session["user"] = u
            else:
                msg = "❌ Error login"

        # LOGOUT
        elif action == "logout":
            session.pop("user", None)

        # ACCIONES YA LOGUEADO
        elif session.get("user"):
            user = session["user"]

            try:
                monto = float(request.form.get("monto"))
            except:
                msg = "Monto inválido"
                return redirect("/")

            if action == "deposit":
                usuarios[user]["saldo"] += monto
                usuarios[user]["historial"].append(f"💸 Depósito ${monto}")

            elif action == "transfer":
                if monto <= usuarios[user]["saldo"]:
                    usuarios[user]["saldo"] -= monto
                    usuarios[user]["historial"].append(f"🏦 Transferencia ${monto}")
                else:
                    msg = "❌ Saldo insuficiente"

            guardar(usuarios)

        return redirect("/")

    if session.get("user"):
        user = session["user"]
        data = usuarios[user]
        return render_template_string(html,
            saldo=data["saldo"],
            historial=data["historial"],
            msg=msg)

    return render_template_string(html, msg=msg)

app.run(debug=True)