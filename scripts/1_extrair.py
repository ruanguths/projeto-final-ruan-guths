import zipfile
import pandas as pd

import config
import banco

# função para carregar um arquivo csv dentro de um zip
def carregar_raw(conexao, arquivo_zip, arquivo_csv, tabela):
    print(f"Carregando {tabela} ..." )

    print(f"limpando tabela...")
    banco.executar(conexao, f"TRUNCATE TABLE {tabela};") # esvazia a tabela antes de carregar

    print("tabela limpa")
    total = 0

    print("abrindo csv...")
    with arquivo_zip.open(arquivo_csv) as arquivo:
        print("csv aberto")
        pedacos = pd.read_csv(
            arquivo,
            sep=config.CSV_SEPARADOR, # separador ;
            encoding=config.CSV_ENCODING, # codificação latin-1
            dtype=str, # Tudo string - raw
            keep_default_na=False, #vazio continua vazio e nao NaN
            chunksize=config.TAMANHO_BLOCO # 50000 linhas por bloco
        )

        print("csv preparado para leitura")
        for pedaco in pedacos:
            linhas = pedaco.values.tolist()
            marcadores = ", ".join(["%s"] * len(pedaco.columns))
            comando = f"INSERT INTO {tabela} VALUES ({marcadores})"
            banco.inserir_em_lote(conexao, comando, linhas)
            total += len(linhas)
            print(f"  {total} linhas carregadas...")

    print(f"Total de linhas: {total}")

def main():
    print("Extração + camada raw")

    try:
        conexao = banco.conectar()

        caminho_zip = config.ARQUIVO_ZIP

        with zipfile.ZipFile(caminho_zip) as arquivo_zip:
            for arquivo in config.ARQUIVOS.values():
                carregar_raw(conexao, arquivo_zip, arquivo["nome_csv"], arquivo["tabela"])

        banco.fechar_conexao(conexao)
        print("RAW concluido!")
    except Exception as erro:
        print(f"Erro: {erro}")
        raise

if __name__ == "__main__":
    main()