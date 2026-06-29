import sqlite3

def conectar():
    return sqlite3.connect("brotinhosGalego.db")


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        endereco TEXT,
        itens TEXT,
        total REAL,
        status TEXT,
        pagamento TEXT,
        data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    cursor.execute("""
        UPDATE pedidos SET status = '🟡 Em preparo' WHERE status = 'preparo'
        """)

    cursor.execute("""
        UPDATE pedidos SET status = '🟢 Pronto' WHERE status = 'pronto'
        """)

    cursor.execute("""
        UPDATE pedidos SET status = '🚚 Saiu para entrega' WHERE status = 'saida'
        """)

    cursor.execute("""
        UPDATE pedidos SET status = '✅ Entregue' WHERE status = 'entregue'
        """)

    cursor.execute("""
        UPDATE pedidos SET status = '🔴 Cancelado' WHERE status = 'cancelado'
        """)

    conn.commit()
    conn.close()


criar_tabela()