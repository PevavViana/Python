from . import db
from .base import ModeloBase

class Usuario(ModeloBase):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    tarefas = db.relationship(
        "Tarefa",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
        }
