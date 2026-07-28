import os
from dotenv import load_dotenv

# carrega o .env
load_dotenv()

# cria uma variável com as credenciais do banco de dados
MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

# caminho do arquivo zip
ARQUIVO_ZIP = "data/raw/arquivos.zip"

# mapeamento dos arquivos dentro do zip
ANO = 2025
ARQUIVOS = {
    "viagem": {
        "nome_csv": f"{ANO}_Viagem.csv",
        "tabela": "raw_viagem"
    },
    "pagamento": {
        "nome_csv": f"{ANO}_Pagamento.csv",
        "tabela": "raw_pagamento"
    },
    "passagem": {
        "nome_csv": f"{ANO}_Passagem.csv",
        "tabela": "raw_passagem"
    },
    "trecho": {
        "nome_csv": f"{ANO}_Trecho.csv",
        "tabela": "raw_trecho"
        }
}

#configurações do arquivo csv 
CSV_SEPARADOR = ";"
CSV_ENCODING = "latin-1"