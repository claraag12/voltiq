# meta.py
from conexao import conectar

def listar_metas(id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM meta WHERE id_empresa = %s ORDER BY mes_referencia",
        (id_empresa,)
    )
    lista = cursor.fetchall()
    conn.close()
    return lista

def cadastrar_meta(id_empresa, mes, limite):
    if limite <= 0:
        return {"erro": "Limite deve ser maior que zero!"}
    conn = conectar()
    cursor = conn.cursor()
    # verifica se ja existe meta para esse mes
    cursor.execute(
        "SELECT id_meta FROM meta WHERE id_empresa = %s AND mes_referencia = %s",
        (id_empresa, mes)
    )
    if cursor.fetchone():
        conn.close()
        return {"erro": "Meta ja existe para esse mes!"}
    cursor.execute(
        "INSERT INTO meta (id_empresa, mes_referencia, limite_kwh) VALUES (%s, %s, %s)",
        (id_empresa, mes, limite)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return {"id": novo_id, "mensagem": "Meta cadastrada!"}

def excluir_meta(id_meta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meta WHERE id_meta = %s", (id_meta,))
    conn.commit()
    conn.close()
    return {"mensagem": "Meta excluida!"}
