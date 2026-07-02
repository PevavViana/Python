from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from models import ClienteLocadora, Locacao, Veiculo, db

locadora_bp = Blueprint("locadora", __name__, url_prefix="/locadora")


@locadora_bp.route("/")
def index():
    locacoes = Locacao.listar_com_detalhes()
    return render_template("locadora/lista.html", locacoes=locacoes)


@locadora_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    clientes = ClienteLocadora.listar()
    veiculos = Veiculo.listar()

    if request.method == "POST":
        loc = Locacao(
            cliente_id=int(request.form["cliente_id"]),
            veiculo_id=int(request.form["veiculo_id"]),
            data_inicio=datetime.strptime(
                request.form["data_inicio"], "%Y-%m-%d"
            ).date(),
            data_fim=datetime.strptime(request.form["data_fim"], "%Y-%m-%d").date(),
            valor_total=float(request.form["valor_total"]),
        )
        db.session.add(loc)
        db.session.commit()
        return redirect(url_for("locadora.index"))

    return render_template(
        "locadora/formulario.html",
        clientes=clientes,
        veiculos=veiculos,
    )
