# Controle de Despesas Pessoal

## Descrição

Este é um aplicativo de controle de despesas pessoais desenvolvido em Python utilizando a biblioteca `tkinter` para a interface gráfica e `mysql-connector-python` para a conexão com o banco de dados MySQL. O aplicativo permite adicionar, atualizar, excluir e visualizar despesas, além de gerar relatórios de despesas por categoria.

## Funcionalidades

- **Adicionar Despesa**: Permite adicionar uma nova despesa com data, valor, categoria e descrição.
- **Atualizar Despesa**: Permite atualizar uma despesa existente.
- **Excluir Despesa**: Permite excluir uma despesa selecionada.
- **Visualizar Despesas**: Exibe todas as despesas cadastradas em uma tabela.
- **Gerar Relatório**: Gera um relatório de despesas agrupado por categoria, mostrando o total de despesas por categoria.

## Pré-requisitos

- Python 3.x
- MySQL Server
- Biblioteca `mysql-connector-python`

  ## Configure o banco de dados MySQL:

Crie um banco de dados chamado controle_gastos e execute o script SQL para criar a tabela de despesas.

CREATE DATABASE controle_gastos;
USE controle_gastos;

CREATE TABLE despesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    valor DECIMAL(10, 2),
    categoria VARCHAR(50),
    descricao TEXT
);

## Instale as dependências:

Certifique-se de que você tem a biblioteca mysql-connector-python instalada:
pip install mysql-connector-python

## Configure a conexão com o banco de dados:

No código Python, substitua user, password e host com as suas credenciais de conexão MySQL.

conn = mysql.connector.connect(
    host='localhost',
    user='root',  # Substitua pelo seu nome de usuário do MySQL
    password='sua-senha',  # Substitua pela sua senha do MySQL
    database='controle_gastos'
)



