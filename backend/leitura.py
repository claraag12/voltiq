# leitura.py
from conexao import conectar
from datetime import date

def listar_leituras(id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM leitura WHERE id_empresa = %s ORDER BY mes_referencia",
        (id_empresa,)
    )
    lista = cursor.fetchall()
    conn.close()
    return lista

def registrar_leitura(id_empresa, mes, kwh):
    if kwh <= 0:
        return {"erro": "kWh deve ser maior que zero!"}
    conn = conectar()
    cursor = conn.cursor()
    # verifica se mes ja foi registrado
    cursor.execute(
        "SELECT id_leitura FROM leitura WHERE id_empresa = %s AND mes_referencia = %s",
        (id_empresa, mes)
    )
    if cursor.fetchone():
        conn.close()
        return {"erro": "Leitura ja existe para esse mes!"}
    cursor.execute(
        "INSERT INTO leitura (id_empresa, mes_referencia, kwh_consumido, data_registro) VALUES (%s, %s, %s, %s)",
        (id_empresa, mes, kwh, date.today())
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return {"id": novo_id, "mensagem": "Leitura registrada!"}

def editar_leitura(id_leitura, kwh):
    if kwh <= 0:
        return {"erro": "kWh deve ser maior que zero!"}
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE leitura SET kwh_consumido = %s WHERE id_leitura = %s",
        (kwh, id_leitura)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Leitura atualizada!"}

def excluir_leitura(id_leitura):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leitura WHERE id_leitura = %s", (id_leitura,))
    conn.commit()
    conn.close()
    return {"mensagem": "Leitura excluida!"}
