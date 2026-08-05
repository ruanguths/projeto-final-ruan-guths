import banco

# raw_viagem para silver_viagem
def transformar_viagem(conexao):

    query = """
    INSERT INTO silver_viagem(
        id_viagem,
        num_proposta,
        situacao,
        viagem_urgente,
        cod_orgao_superior,
        nome_orgao_superior,
        nome_viajante,
        cargo,
        data_inicio,
        data_fim,
        destinos,
        motivo,
        valor_diarias,
        valor_passagens,
        valor_devolucao,
        valor_outros_gastos,
        valor_total,
        duracao_dias,
        custo_medio_diario
    )
    SELECT 
        identificador_do_processo_de_viagem,
        numero_da_proposta_PCDP,
        situacao,
        viagem_urgente, 
        codigo_do_orgao_superior,
        nome_do_orgao_superior,
        nome,
        cargo,
        STR_TO_DATE(
            periodo_data_de_inicio, '%d/%m/%Y'
            ),
        STR_TO_DATE(
            periodo_data_de_fim, '%d/%m/%Y'
            ),
        destinos,
        motivo, 
        CAST(
            REPLACE(valor_diarias, ',', '.') AS DECIMAL(10,2)
            ),
        CAST(
            REPLACE(valor_passagens, ',', '.') AS DECIMAL(10,2)
            ),
        CAST(
            REPLACE(valor_devolucao, ',', '.') AS DECIMAL(10,2)
            ),
        CAST(
            REPLACE(valor_outros_gastos, ',', '.') AS DECIMAL(10,2)
            ),
        CAST(
            REPLACE(valor_diarias, ',', '.') +
            REPLACE(valor_passagens, ',', '.') +
            REPLACE(valor_devolucao, ',', '.') +
            REPLACE(valor_outros_gastos, ',', '.')
            AS DECIMAL(10,2)
            ),
        DATEDIFF(
            STR_TO_DATE(periodo_data_de_fim, '%d/%m/%Y'),
            STR_TO_DATE(periodo_data_de_inicio, '%d/%m/%Y')
            ) +1,
        NULL

    FROM raw_viagem;
    """
    # NULL para custo_medio_diario para primeiro criar as colunas que serão utilizadas na sua fórmula e então só dar udpdate
    # com custo_medio_diario = valor_total / duracao_dias.


    query_update = """
        UPDATE silver_viagem
        SET custo_medio_diario = valor_total / duracao_dias;
"""

    banco.executar(conexao, query)
    banco.executar(conexao, query_update)

# raw_pagamento para silver_pagamento

def transformar_pagamento(conexao):

    query = """
    INSERT INTO silver_pagamento(
        id_viagem,
        num_proposta,
        nome_orgao_pagador,
        nome_ug_pagadora,
        tipo_pagamento,
        valor
    )
    SELECT 
        identificador_do_processo_de_viagem,
        numero_da_proposta_PCDP,
        nome_do_orgao_pagador,
        nome_da_unidade_gestora_pagadora,
        tipo_de_pagamento,
        CAST(
            REPLACE(valor, ',', '.') AS DECIMAL(10,2)
            )
    FROM raw_pagamento;
"""

    banco.executar(conexao, query)

# raw_passagem para silver_passagem
def transformar_passagem(conexao):

    query = """
    INSERT INTO silver_passagem(
        id_viagem,
        meio_transporte,
        pais_origem_ida,
        uf_origem_ida,
        cidade_origem_ida,
        pais_destino_ida,
        uf_destino_ida,
        cidade_destino_ida,
        valor_passagem,
        taxa_servico,
        data_emissao
    )
    SELECT 
        identificador_do_processo_de_viagem,
        meio_de_transporte,
        pais_origem_ida,
        UF_origem_ida,
        cidade_origem_ida,
        pais_destino_ida,
        UF_destino_ida,
        cidade_destino_ida,
        CAST(
            REPLACE(valor_da_passagem, ',', '.') AS DECIMAL(10,2)
            ),
        CAST(
            REPLACE(taxa_de_servico, ',', '.') AS DECIMAL(10,2)
            ),
        STR_TO_DATE(
            NULLIF(data_da_emissao_compra, ''), '%d/%m/%Y'
            )
    FROM raw_passagem;
"""

    banco.executar(conexao, query)

# raw_trecho para silver_trecho
def transformar_trecho(conexao):

    query = """
    INSERT INTO silver_trecho(
        id_viagem,
        sequencia_trecho,
        origem_data,
        origem_uf,
        origem_cidade,
        destino_data,
        destino_uf,
        destino_cidade,
        meio_transporte,
        numero_diarias
    )
    SELECT 
        identificador_do_processo_de_viagem,
        cast(
            sequencia_trecho AS UNSIGNED
            ),
        STR_TO_DATE(
            origem_data, '%d/%m/%Y'
            ),        
        origem_UF,
        origem_cidade,
        STR_TO_DATE(
            destino_data, '%d/%m/%Y'
            ),
        destino_UF,
        destino_cidade,
        meio_de_transporte,
        CAST(
            REPLACE(numero_diarias, ',', '.') AS DECIMAL(10,2)
            )
    FROM raw_trecho;
"""

    banco.executar(conexao, query)

# roda todas as funções anteriores
def main():

    try:
        print("Conectando ao banco...")
        conexao = banco.conectar()
        print("Conexão estabelecida!")

        # limpa tabelas antes de transformar
        banco.executar(conexao, "SET FOREIGN_KEY_CHECKS = 0;") # desabilita foreign key checks para evitar erro ao limpar a tabela silver_viagem
        banco.executar(conexao, "TRUNCATE TABLE silver_pagamento;")
        banco.executar(conexao, "TRUNCATE TABLE silver_passagem;")
        banco.executar(conexao, "TRUNCATE TABLE silver_trecho;")
        banco.executar(conexao, "TRUNCATE TABLE silver_viagem;")
        banco.executar(conexao, "SET FOREIGN_KEY_CHECKS = 1;") # reabilita foreign key checks

        print("Transformando tabelas...")
        transformar_viagem(conexao)
        print("tabela viagem transformada!")
        
        transformar_pagamento(conexao)
        print("tabela pagamento transformada!")

        transformar_passagem(conexao)
        print("tabela passagem transformada!")

        transformar_trecho(conexao)
        print("tabela trecho transformada!")

    finally:
        print("Transformação concluída!")
        banco.fechar_conexao(conexao)
        print("Conexão fechada!")

if __name__ == "__main__":
    main()