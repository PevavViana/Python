from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .cliente_locadora import ClienteLocadora
from .locacao import Locacao
from .veiculo import Veiculo

__all__ = ["db", "ModeloBase", "ClienteLocadora", "Veiculo", "Locacao"]
