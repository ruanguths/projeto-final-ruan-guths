CREATE DATABASE IF NOT EXISTS viagem_gov;

USE viagem_gov;

-- RAW

CREATE TABLE IF NOT EXISTS raw_viagem (
    identificador_do_processo_de_viagem VARCHAR(255),
    numero_da_proposta_PCDP VARCHAR(255),
    situacao VARCHAR(255),
    viagem_urgente VARCHAR(255),
    justificativa_urgencia_viagem VARCHAR(255),
    codigo_do_orgao_superior VARCHAR(255),
    nome_do_orgao_superior VARCHAR(255),
    codigo_orgao_solicitante VARCHAR(255),
    nome_orgao_solicitante VARCHAR(255),
    CPF_viajante VARCHAR(255),
    nome VARCHAR(255),
    cargo VARCHAR(255),
    funcao VARCHAR(255),
    descricao_funcao VARCHAR(255),
    periodo_data_de_inicio VARCHAR(255),
    periodo_data_de_fim VARCHAR(255),
    destinos VARCHAR(255),
    motivo VARCHAR(255),
    valor_diarias VARCHAR(255),
    valor_passagens VARCHAR(255),
    valor_devolucao VARCHAR(255),
    valor_outros_gastos VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS raw_pagamento (
    identificador_do_processo_de_viagem VARCHAR(255),
    numero_da_proposta_PCDP VARCHAR(255),
    codigo_do_orgao_superior VARCHAR(255),
    nome_do_orgao_superior VARCHAR(255),
    codigo_do_orgao_pagador VARCHAR(255),
    nome_do_orgao_pagador VARCHAR(255),
    codigo_da_unidade_gestora_pagadora VARCHAR(255),
    nome_da_unidade_gestora_pagadora VARCHAR(255),
    tipo_de_pagamento VARCHAR(255),
    valor VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS raw_passagem (
    identificador_do_processo_de_viagem VARCHAR(255),
    numero_da_proposta_PCDP VARCHAR(255),
    meio_de_transporte VARCHAR(255),
    pais_origem_ida VARCHAR(255),
    UF_origem_ida VARCHAR(255),
    cidade_origem_ida VARCHAR(255),
    pais_destino_ida VARCHAR(255),
    UF_destino_ida VARCHAR(255),
    cidade_destino_ida VARCHAR(255),
    pais_origem_volta VARCHAR(255),
    UF_origem_volta VARCHAR(255),
    cidade_origem_volta VARCHAR(255),
    pais_destino_volta VARCHAR(255),
    UF_destino_volta VARCHAR(255),
    cidade_destino_volta VARCHAR(255),
    valor_da_passagem VARCHAR(255),
    taxa_de_servico VARCHAR(255),
    data_da_emissao_compra VARCHAR(255),
    hora_da_emissao_compra VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS raw_trecho (
    identificador_do_processo_de_viagem VARCHAR(255),
    numero_da_Proposta_PCDP VARCHAR(255),
    sequencia_trecho VARCHAR(255),
    origem_data VARCHAR(255),
    origem_pais VARCHAR(255),
    origem_UF VARCHAR(255),
    origem_cidade VARCHAR(255),
    destino_data VARCHAR(255),
    destino_pais VARCHAR(255),
    destino_UF VARCHAR(255),
    destino_cidade VARCHAR(255),
    meio_de_transporte VARCHAR(255),
    numero_diarias VARCHAR(255),
    Missao VARCHAR(255)
);

-- SILVER

CREATE TABLE IF NOT EXISTS silver_viagem (
    id_viagem VARCHAR(20) PRIMARY KEY NOT NULL,
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    nome_viajante VARCHAR(255) NOT NULL,
    cargo VARCHAR(255),
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias DECIMAL(10,2) CHECK (valor_diarias >= 0),
    valor_passagens DECIMAL(10,2) CHECK (valor_passagens >= 0),
    valor_devolucao DECIMAL(10,2) CHECK (valor_devolucao >= 0),
    valor_outros_gastos DECIMAL(10,2) CHECK (valor_outros_gastos >= 0),
    valor_total DECIMAL(10,2) NOT NULL,
    duracao_dias INT
);

CREATE TABLE IF NOT EXISTS silver_pagamento (
    id_pagamento INT PRIMARY KEY AUTO_INCREMENT,
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) CHECK (valor >= 0),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
);

CREATE TABLE IF NOT EXISTS silver_passagem (
    id_passagem INT PRIMARY KEY AUTO_INCREMENT,
    id_viagem VARCHAR(20) NOT NULL,
    meio_transporte VARCHAR(50),
    pais_origem_ida VARCHAR(60),
    uf_origem_ida VARCHAR(40),
    cidade_origem_ida VARCHAR(80),
    pais_destino_ida VARCHAR(60),
    uf_destino_ida VARCHAR(40),
    cidade_destino_ida VARCHAR(80),
    valor_passagem DECIMAL(10,2) CHECK (valor_passagem >= 0),
    taxa_servico DECIMAL(10,2) CHECK (taxa_servico >= 0),
    data_emissao DATE,
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
);

CREATE TABLE IF NOT EXISTS silver_trecho (
    id_trecho INT PRIMARY KEY AUTO_INCREMENT, 
    id_viagem VARCHAR(20) NOT NULL, -- já é unique pq é primary key na tabela silver_viagem
    sequencia_trecho INT UNIQUE,
    origem_data DATE,
    origem_uf VARCHAR(40),
    origem_cidade VARCHAR(80),
    destino_data DATE,
    destino_uf VARCHAR(40),
    destino_cidade VARCHAR(80),
    meio_transporte VARCHAR(50),
    numero_diarias DECIMAL(10,2) CHECK (numero_diarias >= 0),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem)
);