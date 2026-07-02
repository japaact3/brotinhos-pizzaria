from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    Blueprint,
    url_for,
    session,
    flash,
    redirect
)

from werkzeug.security import check_password_hash

from dados.produtos import produtos

from database import (
    dados_dashboard,
    listar_pedidos,
    salvar_pedido,
    alterar_status,
    resetar_semana,
    conectar,
    buscar_usuario
)

from utils.auth import login_required


import json


admin_bp = Blueprint("admin", __name__)


# ============================================================
# ROTAS ADMIN
# ============================================================

@admin_bp.route("/")
def home():
    return redirect(url_for("admin.login"))

@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        user = buscar_usuario(usuario)

        if user is None:

            flash("Usuário não encontrado.", "error")
            return redirect(url_for("admin.login"))

        if user["ativo"] == 0:

            flash("Usuário desativado.", "error")
            return redirect(url_for("admin.login"))

        if not check_password_hash(user["senha"], senha):

            flash("Senha incorreta.", "error")
            return redirect(url_for("admin.login"))

        # LOGIN OK

        session["usuario_id"] = user["id"]
        session["usuario_nome"] = user["nome"]
        session["usuario"] = user["usuario"]
        session["nivel"] = user["nivel"]

        flash("Bem-vindo!", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():

    session.clear()

    flash("Sessão encerrada.", "success")

    return redirect(url_for("admin.login"))



@admin_bp.route("/admin")
@login_required
def dashboard():

    dados = dados_dashboard()

    return render_template(
        "admin/dashboard.html",
        **dados
    )




@admin_bp.route("/admin/pedidos", endpoint="lista_pedidos")
@login_required
def admin_pedidos():

    pedidos = listar_pedidos()

    return render_template("admin/pedidos.html", pedidos=pedidos)




@admin_bp.route("/admin/novo-pedido", methods=["GET", "POST"])
@login_required
def novo_pedido():

    if request.method == "POST":

        try:

            dados = request.get_json()

            salvar_pedido(dados)

            return jsonify({"status": "ok"})

        except Exception as e:

            print("ERRO:", e)

            return jsonify({
                "status": "erro",
                "erro": str(e)
            }), 500

    return render_template(
        "admin/novo_pedido.html",
        produtos=produtos
    )
