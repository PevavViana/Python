from flask import Blueprint, redirect, render_template, request, session, url_for

from models import Usuario
from services import autenticar, registrar_usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            return render_template("registro.html", erro="Preencha nome, email e senha.")

        if Usuario.query.filter_by(email=email).first():
            return render_template("registro.html", erro="Esse email já está cadastrado.")

        registrar_usuario(nome, email, senha)
        return redirect(url_for("auth.login"))

    return render_template("registro.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = autenticar(email, senha)
        if not usuario:
            return render_template("login.html", erro="Email ou senha inválidos.")

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        return redirect(url_for("tarefas.dashboard"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))