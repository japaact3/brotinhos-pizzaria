from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    Blueprint
)

from dados.produtos import produtos

from database import (
    dados_dashboard,
    listar_pedidos,
    salvar_pedido,
    alterar_status,
    resetar_semana,
    conectar
)

import json

cliente_bp = Blueprint("cliente", __name__)

# ============================================================
# ROTAS DO CLIENTE
# ============================================================

@cliente_bp.route("/home")
def home():
    return render_template("cliente/home.html")

@cliente_bp.route("/cardapio")
def cardapio():
    return render_template(
        "cliente/cardapio.html",
        produtos=produtos
    )


@cliente_bp.route("/acompanhar")
def acompanhar():
    return render_template("cliente/acompanhar.html")


@cliente_bp.route("/contato")
def contato():
    return render_template("cliente/contato.html")

@cliente_bp.route("/pedido")
def pedido():
    return render_template(
        "cliente/pedido_cliente.html",
        produtos=produtos
    )


@cliente_bp.route("/novo-pedido", methods=["POST"])
def novo_pedido():

    dados = request.get_json()

    salvar_pedido(dados)

    return jsonify({"status": "ok"})
