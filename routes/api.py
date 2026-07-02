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


api_bp = Blueprint("api", __name__)



# ============================================================
# API
# ============================================================


@api_bp.route("/api/pedidos", methods=["GET"])
def api_pedidos():

    pedidos = listar_pedidos()

    return jsonify(pedidos)


@api_bp.route("/api/status/<int:id>", methods=["POST"])
def atualizar_status(id):

    try:

        dados = request.get_json()

        if not dados:
            return jsonify({
                "ok": False,
                "erro": "Dados inválidos"
            }), 400

        status = dados.get("status")

        alterar_status(id, status)

        return jsonify({
            "ok": True,
            "status": status
        })

    except Exception as e:

        print("ERRO STATUS:", e)

        return jsonify({
            "ok": False,
            "erro": str(e)
        }), 500


@api_bp.route("/api/reset-semana", methods=["POST"])
def reset_semana():

    try:

        resetar_semana()

        return jsonify({
            "ok": True,
            "mensagem": "Semana resetada com sucesso"
        })

    except Exception as e:

        print("ERRO RESET:", e)

        return jsonify({
            "ok": False,
            "erro": str(e)
        }), 500
