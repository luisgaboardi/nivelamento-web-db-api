import os
import psycopg2
from tabulate import tabulate
import pandas as pd


# Configurações do banco de dados
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ans_database"
DB_USER = "postgres"
DB_PASSWORD = "password"

def create_tables():
    """
    Conecta ao banco de dados PostgreSQL e cria as tabelas demonstracoes_contabeis e operadoras.
    """
    cursor = None
    conn = None
    try:
        # Conecta ao banco de dados
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Query para criar a tabela demonstracoes_contabeis
        create_demonstracoes_contabeis = """
        CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
            data DATE,
            reg_ans VARCHAR(255),
            cd_conta_contabil VARCHAR(255),
            descricao TEXT,
            vl_saldo_inicial NUMERIC(20, 2),
            vl_saldo_final NUMERIC(20, 2)
        );
        """

        # Query para criar a tabela operadoras
        create_operadoras = """
        CREATE TABLE IF NOT EXISTS operadoras (
            id SERIAL PRIMARY KEY,
            registro_ans VARCHAR(255),
            cnpj VARCHAR(18),
            razao_social VARCHAR(255),
            nome_fantasia VARCHAR(255),
            modalidade VARCHAR(255),
            logradouro VARCHAR(255),
            numero VARCHAR(20),
            complemento VARCHAR(255),
            bairro VARCHAR(255),
            cidade VARCHAR(255),
            uf VARCHAR(2),
            cep VARCHAR(10),
            ddd VARCHAR(3),
            telefone VARCHAR(15),
            fax VARCHAR(15),
            endereco_eletronico VARCHAR(255),
            representante VARCHAR(255),
            cargo_representante VARCHAR(255),
            regiao_comercializacao VARCHAR(255),
            data_registro_ans DATE
        );
        """

        # Executa as queries para criar as tabelas
        cursor.execute(create_demonstracoes_contabeis)
        cursor.execute(create_operadoras)

        # Confirma as alterações no banco de dados
        conn.commit()
        print("Tabelas criadas com sucesso!")

    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")
    finally:
        # Fecha a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    create_tables()
