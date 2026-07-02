import sqlite3
import json

from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash


DB = "brotinhosGalego.db"


def conectar():
    conn = sqlite3.connect(DB, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


# ============================================================
# DASHBOARD
# ============================================================

def dados_dashboard():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT IFNULL(SUM(total),0)
        FROM pedidos
        WHERE status='entregue'
    """)
    total_vendas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status='preparo'
    """)
    em_preparo = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status='saida'
    """)
    na_entrega = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status='entregue'
    """)
    entregues = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM pedidos
        WHERE status='cancelado'
    """)
    cancelados = cursor.fetchone()[0]

    conn.close()

    ticket = 0

    if entregues:
        ticket = total_vendas / entregues

    return {

        "total_pedidos": total_pedidos,
        "total_vendas": round(total_vendas, 2),
        "em_preparo": em_preparo,
        "na_entrega": na_entrega,
        "entregues": entregues,
        "cancelados": cancelados,
        "ticket": round(ticket, 2)

    }


# ============================================================
# PEDIDOS
# ============================================================

def listar_pedidos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()


    pedidos = []

    for r in rows:

        try:
            itens = json.loads(r[4]) if r[4] else []
        except:
            itens = []
    
        pedidos.append({
            "id": r[0],
            "nome": r[1],
            "telefone": r[2],
            "endereco": r[3],
            "itens": itens,
            "total": r[5],
            "status": r[6]
        })

    return pedidos


# ============================================================
# NOVO PEDIDO
# ============================================================

def salvar_pedido(dados):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO pedidos
        (
            nome,
            telefone,
            endereco,
            itens,
            total,
            status
        )

        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        dados.get("nome"),
        dados.get("telefone"),
        dados.get("endereco"),

        json.dumps(
            dados.get("itens", [])
        ),

        dados.get("total"),

        "preparo"

    ))

    conn.commit()
    conn.close()


# ============================================================
# STATUS
# ============================================================

def alterar_status(id, status):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE pedidos

        SET status=?

        WHERE id=?

    """, (

        status,
        id

    ))

    conn.commit()
    conn.close()


# ============================================================
# RESET
# ============================================================

def resetar_semana():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM pedidos

    """)

    conn.commit()

    conn.close()



# ============================================================
# USUÁRIOS
# ============================================================

def criar_tabela_usuarios():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            usuario TEXT UNIQUE NOT NULL,

            senha TEXT NOT NULL,

            nivel TEXT NOT NULL DEFAULT 'atendente',

            ativo INTEGER DEFAULT 1

        )
    """)

    conn.commit()
    conn.close()


def criar_admin():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE usuario=?",
        ("admin",)
    )

    existe = cursor.fetchone()

    if not existe:

        senha = generate_password_hash("123456")

        cursor.execute("""

            INSERT INTO usuarios
            (
                nome,
                usuario,
                senha,
                nivel
            )

            VALUES
            (?, ?, ?, ?)

        """, (

            "Administrador",

            "admin",

            senha,

            "administrador"

        ))

        conn.commit()

    conn.close()


# ============================================================
# LOGIN
# ============================================================

def buscar_usuario(usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            id,
            nome,
            usuario,
            senha,
            nivel,
            ativo

        FROM usuarios

        WHERE usuario=?

    """, (usuario,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "nome": row[1],
        "usuario": row[2],
        "senha": row[3],
        "nivel": row[4],
        "ativo": row[5]
    }


def criar_admin_padrao():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ("admin",))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO usuarios (nome, usuario, senha, nivel, ativo)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Administrador",
            "admin",
            generate_password_hash("123456"),
            "admin",
            1
        ))

        conn.commit()

    conn.close()