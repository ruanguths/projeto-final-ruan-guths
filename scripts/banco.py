import mysql.connector
from mysql.connector import Error
from config import MYSQL_CONFIG # importando do arquivo config.py

# função para conectar ao banco de dados
def conectar():
    try:
        return mysql.connector.connect(**MYSQL_CONFIG) # **MYSQL_CONFIG é um dicionário sendo desempacotado (chave e valor separados)
    except Error as erro:
        raise RuntimeError(f"""Erro ao conectar ao banco de dados: {erro}
Execute o arquivo 0_criar_banco.sql primeiro.""")

# função para executar um sql
def executar(conexao, sql):
    cursor = conexao.cursor()
    cursor.execute(sql)

    if sql.strip().upper().startswith("SELECT"):
        resultado = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description] # list comprehension coletando o nome das colunas (.description) em um select
        cursor.close()
        return resultado, colunas

    conexao.commit()
    cursor.close()

# função para inserir varias linhas em uma tabela
def inserir_em_lote(conexao, sql_insert, linhas):
    if not linhas:
        return
    cursor = conexao.cursor()
    cursor.executemany(sql_insert, linhas)
    conexao.commit()
    cursor.close()

# função para fechar a conexão se estiver aberta
def fechar_conexao(conexao):
    if conexao and conexao.is_connected():
        conexao.close()