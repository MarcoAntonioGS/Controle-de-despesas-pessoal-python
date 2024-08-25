-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS controle_gastos;

-- Seleciona o banco de dados
USE controle_gastos;

-- Criação da tabela despesas
CREATE TABLE IF NOT EXISTS despesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    descricao TEXT
);
