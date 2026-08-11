from flask import Blueprint, redirect, render_template, request, session, url_for

from models import Tarefa
from models.tarefa import status_validos
from services import buscar_frase_motivacional, excluir_tarefa, exigir_login
from services.tarefa_service import atualizar_tarefa, buscar_tarefa, criar_tarefa

tarefas_bp = Blueprint("tarefas", __name__)

@tarefas_bp.route("/dashboard")
def dashboard():
    resposta = exigir_login()
    if resposta:
        return resposta

    usuario_id = session["usuario_id"]
    status_filtro = request.args.get("status")

    tarefas = Tarefa.listar_por_usuario(usuario_id, status=status_filtro)
    frase = buscar_frase_motivacional()

    return render_template(
        "dashboard.html",
        tarefas=tarefas,
        frase=frase,
        status_filtro=status_filtro or "todos",
        status_validos=status_validos,
    )

@tarefas_bp.route("/nova_tarefa", methods=["GET", "POST"])
def nova_tarefa():
    resposta = exigir_login()
    if resposta:
        return resposta

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            return render_template(
                "nova_tarefa.html",
                status_validos=status_validos,
                erro="Informe um título para a tarefa.",
            )

        criar_tarefa(session["usuario_id"], titulo, descricao, status)
        return redirect(url_for("tarefas.dashboard"))

    return render_template("nova_tarefa.html", status_validos=status_validos)

@tarefas_bp.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
def editar(tarefa_id):
    resposta = exigir_login()
    if resposta:
        return resposta

    usuario_id = session["usuario_id"]
    tarefa = buscar_tarefa(tarefa_id, usuario_id)
    if not tarefa:
        return redirect(url_for("tarefas.dashboard"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", tarefa.status)

        if not titulo:
            return render_template(
                "editar_tarefa.html",
                tarefa=tarefa,
                status_validos=status_validos,
                erro="Informe um título para a tarefa.",
            )

        atualizar_tarefa(tarefa_id, usuario_id, titulo, descricao, status)
        return redirect(url_for("tarefas.dashboard"))

    return render_template("editar_tarefa.html", tarefa=tarefa, status_validos=status_validos)

@tarefas_bp.route("/excluir/<int:tarefa_id>", methods=["POST"])
def excluir(tarefa_id):
    resposta = exigir_login()
    if resposta:
        return resposta

    excluir_tarefa(tarefa_id, session["usuario_id"])
    return redirect(url_for("tarefas.dashboard"))

@tarefas_bp.route("/progresso")
def progresso():
    resposta = exigir_login()
    if resposta:
        return resposta

    return render_template("progresso.html")