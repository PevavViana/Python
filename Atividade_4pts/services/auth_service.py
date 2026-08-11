from flask import jsonify, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import Usuario, db

def registrar_usuario(nome, email, senha):
    usuario = Usuario(nome=nome, email=email, senha=generate_password_hash(senha))
    db.session.add(usuario)
    db.session.commit()
    return usuario

def autenticar(email, senha):
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and check_password_hash(usuario.senha, senha):
        return usuario
    return None

def exigir_login():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    return None

def exigir_login_api():
    if "usuario_id" not in session:
        return jsonify({"erro": "Não autenticado."}), 401
    return None
