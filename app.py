from flask import Flask, render_template, request, redirect, url_for, jsonify

import sqlite3

import json



from dados.produtos import produtos

app = Flask(__name__)

# memória temporária (depois vira banco de dados)
pedidos = []

def conectar():
    return sqlite3.connect(
        "brotinhosGalego.db",
        timeout=10
    )


@app.route("/novo-pedido", methods=["GET", "POST"])
def novo_pedido():

    if request.method == "POST":

        try:
            dados = request.get_json()

            print("DEBUG PEDIDO:", dados)

            conn = conectar()
            conn.execute("PRAGMA journal_mode=WAL;")
            cursor = conn.cursor()
        

            cursor.execute("""
                INSERT INTO pedidos (nome, telefone, endereco, itens, total, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                dados.get("nome"),
                dados.get("telefone"),
                dados.get("endereco"),
                json.dumps(dados.get("itens", [])),
                dados.get("total"),
                "🟡 Em preparo"
            ))

            conn.commit()
            conn.close()

            return jsonify({"status": "ok"})

        except Exception as e:
            print("ERRO NO BACKEND:", e)
            return jsonify({"status": "error", "erro": str(e)}), 500

    return render_template("novo_pedido.html", produtos=produtos)





@app.route("/pedidos")
def lista_pedidos():

    conn = conectar()
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    pedidos = []

    for row in rows:
        pedidos.append({
            "id": row[0],
            "nome": row[1],
            "telefone": row[2],
            "endereco": row[3],
            "itens": json.loads(row[4]),
            "total": row[5],
            "status": row[6]
        })

    return render_template("pedidos.html", pedidos=pedidos)




@app.route("/atualizar-status/<int:id>", methods=["POST"])
def atualizar_status(id):

    try:
        dados = request.get_json()

        if not dados or "status" not in dados:
            return jsonify({"erro": "status inválido"}), 400

        novo_status = dados["status"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pedidos SET status = ? WHERE id = ?
        """, (novo_status, id))

        conn.commit()
        conn.close()

        return jsonify({"ok": True})

    except Exception as e:
        print("ERRO STATUS:", e)
        return jsonify({"erro": str(e)}), 500



@app.route("/")
@app.route("/dashboard")
def dashboard():

    conn = conectar()
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()

    # Total de pedidos
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    # Total vendido (somente entregues)
    cursor.execute("""
        SELECT IFNULL(SUM(total),0)
        FROM pedidos
        WHERE TRIM(status) = 'entregue'
    """)
    total_vendas = cursor.fetchone()[0]

    # Em preparo
    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status='preparo'
    """)
    em_preparo = cursor.fetchone()[0]

    # Na entrega
    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status='saiu'
    """)
    na_entrega = cursor.fetchone()[0]

    # Entregues
    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE TRIM(status) = 'entregue'
    """)
    entregues = cursor.fetchone()[0]

    # Cancelados
    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status='cancelado'
    """)
    cancelados = cursor.fetchone()[0]


    conn.close()

    ticket = total_vendas / entregues if entregues else 0

    return render_template(
        "dashboard.html",
        total_pedidos=total_pedidos,
        total_vendas=round(total_vendas, 2),
        em_preparo=em_preparo,
        na_entrega=na_entrega,
        entregues=entregues,
        cancelados=cancelados,
        ticket=round(ticket, 2)
    )






STATUS = {
    "preparo": "🟡 Em preparo",
    "pronto": "🟢 Pronto",
    "saida": "🚚 Saiu para entrega",
    "entregue": "✅ Entregue",
    "cancelado": "🔴 Cancelado"
}


if __name__ == "__main__":
    app.run()