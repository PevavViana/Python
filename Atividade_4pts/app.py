import os

from flask import Flask, redirect, url_for

from controllers import api_bp, auth_bp, tarefas_bp
from models import db

def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "banco.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"
    app.config["DEBUG"] = False

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefas_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app

app = criar_app()

if __name__ == "__main__":
    app.run(debug=False)
