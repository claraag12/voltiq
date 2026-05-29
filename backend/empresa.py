# empresa.py
from conexao import conectar

def listar_empresas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresa ORDER BY nome")
    lista = cursor.fetchall()
    conn.close()
    return lista

def buscar_empresa(id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresa WHERE id_empresa = %s", (id_empresa,))
    emp = cursor.fetchone()
    conn.close()
    return emp

def cadastrar_empresa(nome, cnpj, cidade, tarifa):
    conn = conectar()
    cursor = conn.cursor()
    # verifica se cnpj ja existe
    cursor.execute("SELECT id_empresa FROM empresa WHERE cnpj = %s", (cnpj,))
    if cursor.fetchone():
        conn.close()
        return {"erro": "CNPJ ja cadastrado!"}
    cursor.execute(
        "INSERT INTO empresa (nome, cnpj, cidade, tarifa_reais) VALUES (%s, %s, %s, %s)",
        (nome, cnpj, cidade, tarifa)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return {"id": novo_id, "mensagem": "Empresa cadastrada!"}

def editar_empresa(id_empresa, nome, cidade, tarifa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE empresa SET nome = %s, cidade = %s, tarifa_reais = %s WHERE id_empresa = %s",
        (nome, cidade, tarifa, id_empresa)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Empresa atualizada!"}

def excluir_empresa(id_empresa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empresa WHERE id_empresa = %s", (id_empresa,))
    conn.commit()
    conn.close()
    return {"mensagem": "Empresa excluida!"}
