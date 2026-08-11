from flask import Blueprint, jsonify, request, session

from models import Tarefa
from services import contar_por_status, exigir_login_api
from services.tarefa_service import atualizar_tarefa, criar_tarefa, excluir_tarefa

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/tarefas/filtro", methods=["GET"])
def filtro_tarefas():
    resposta = exigir_login_api()
    if resposta:
        return resposta

    status = request.args.get("status")
    tarefas = Tarefa.listar_por_usuario(session["usuario_id"], status=status)
    return jsonify([t.para_dict() for t in tarefas])

@api_bp.route("/progresso", methods=["GET"])
def progresso_json():
    resposta = exigir_login_api()
    if resposta:
        return resposta

    return jsonify(contar_por_status(session["usuario_id"]))

@api_bp.route("/tarefas", methods=["GET"])
def rest_listar():
    resposta = exigir_login_api()
    if resposta:
        return resposta

    tarefas = Tarefa.listar_por_usuario(session["usuario_id"])
    return jsonify([t.para_dict() for t in tarefas])

@api_bp.route("/tarefas", methods=["POST"])
def rest_criar():
    resposta = exigir_login_api()
    if resposta:
        return resposta

    dados = request.get_json(silent=True) or {}
    titulo = (dados.get("titulo") or "").strip()
    if not titulo:
        return jsonify({"erro": "Campo 'titulo' é obrigatório."}), 400

    tarefa = criar_tarefa(
        usuario_id=session["usuario_id"],
        titulo=titulo,
        descricao=dados.get("descricao", ""),
        status=dados.get("status", "pendente"),
    )
    return jsonify(tarefa.para_dict()), 201

@api_bp.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def rest_atualizar(tarefa_id):
    resposta = exigir_login_api()
    if resposta:
        return resposta

    dados = request.get_json(silent=True) or {}
    titulo = (dados.get("titulo") or "").strip()
    if not titulo:
        return jsonify({"erro": "Campo 'titulo' é obrigatório."}), 400

    tarefa = atualizar_tarefa(
        tarefa_id=tarefa_id,
        usuario_id=session["usuario_id"],
        titulo=titulo,
        descricao=dados.get("descricao", ""),
        status=dados.get("status", "pendente"),
    )
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return jsonify(tarefa.para_dict())

@api_bp.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def rest_excluir(tarefa_id):
    resposta = exigir_login_api()
    if resposta:
        return resposta

    if not excluir_tarefa(tarefa_id, session["usuario_id"]):
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return "", 204