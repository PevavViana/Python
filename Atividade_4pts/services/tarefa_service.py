from models import Tarefa, db
from models.tarefa import status_validos

def criar_tarefa(usuario_id, titulo, descricao, status="pendente"):
    if status not in status_validos:
        status = "pendente"
    tarefa = Tarefa(titulo=titulo, descricao=descricao, status=status, usuario_id=usuario_id)
    db.session.add(tarefa)
    db.session.commit()
    return tarefa

def buscar_tarefa(tarefa_id, usuario_id):
    return Tarefa.query.filter_by(id=tarefa_id, usuario_id=usuario_id).first()

def atualizar_tarefa(tarefa_id, usuario_id, titulo, descricao, status):
    tarefa = buscar_tarefa(tarefa_id, usuario_id)
    if not tarefa:
        return None
    tarefa.titulo = titulo
    tarefa.descricao = descricao
    if status in status_validos:
        tarefa.status = status
    db.session.commit()
    return tarefa

def excluir_tarefa(tarefa_id, usuario_id):
    tarefa = buscar_tarefa(tarefa_id, usuario_id)
    if not tarefa:
        return False
    db.session.delete(tarefa)
    db.session.commit()
    return True

def contar_por_status(usuario_id):
    contagem = {}
    for status in status_validos:
        contagem[status] = 0
    for tarefa in Tarefa.query.filter_by(usuario_id=usuario_id).all():
        contagem[tarefa.status] = contagem.get(tarefa.status, 0) + 1
    return contagem
