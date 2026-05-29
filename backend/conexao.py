# conexao.py
import mysql.connector

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # coloque sua senha aqui
        database="voltiq"
    )
    return conn
