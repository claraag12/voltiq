-- =============================================
-- VoltIQ -- Banco de Dados
-- =============================================

CREATE DATABASE IF NOT EXISTS voltiq;
USE voltiq;

CREATE TABLE empresa (
    id_empresa   INT           AUTO_INCREMENT PRIMARY KEY,
    nome         VARCHAR(100)  NOT NULL,
    cnpj         VARCHAR(18)   NOT NULL UNIQUE,
    cidade       VARCHAR(100)  NOT NULL,
    tarifa_reais DECIMAL(10,2) NOT NULL,
    CHECK (tarifa_reais > 0)
);

CREATE TABLE leitura (
    id_leitura     INT           AUTO_INCREMENT PRIMARY KEY,
    id_empresa     INT           NOT NULL,
    mes_referencia VARCHAR(7)    NOT NULL,
    kwh_consumido  DECIMAL(10,2) NOT NULL,
    data_registro  DATE          NOT NULL,
    CHECK (kwh_consumido > 0),
    UNIQUE (id_empresa, mes_referencia),
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa) ON DELETE CASCADE
);

CREATE TABLE meta (
    id_meta        INT           AUTO_INCREMENT PRIMARY KEY,
    id_empresa     INT           NOT NULL,
    mes_referencia VARCHAR(7)    NOT NULL,
    limite_kwh     DECIMAL(10,2) NOT NULL,
    CHECK (limite_kwh > 0),
    UNIQUE (id_empresa, mes_referencia),
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa) ON DELETE CASCADE
);
