# ============================================================
# IMPORTAÇÕES
# ============================================================

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
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


from flask import Flask

from routes.cliente import cliente_bp
from routes.admin import admin_bp
from routes.api import api_bp

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("admin.login"))

from database import criar_tabela_usuarios
from database import criar_admin

criar_tabela_usuarios()
criar_admin()

app.register_blueprint(cliente_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run(debug=False)