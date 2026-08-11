from . import db
from .base import ModeloBase

status_validos = ["pendente", "em_andamento", "concluida"]

class Tarefa(ModeloBase):
    __tablename__ = "tarefas"

    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="tarefas")

    @classmethod
    def listar_por_usuario(cls, usuario_id, status=None):
        query = cls.query.filter_by(usuario_id=usuario_id)
        if status and status in status_validos:
            query = query.filter_by(status=status)
        return query.order_by(cls.data_criacao.desc()).all()

    def para_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "usuario_id": self.usuario_id,
            "data_criacao": str(self.data_criacao),
            "data_atualizacao": str(self.data_atualizacao),
        }
