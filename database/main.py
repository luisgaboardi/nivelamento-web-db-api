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


def prepare_csv_files():
    """
    Prepara os arquivos CSV para importação no banco de dados PostgreSQL.
    """
    csv_files = [f for f in os.listdir("downloads/DemCon") if f.endswith(".csv")]
    for csv_file in csv_files:
        csv_path = os.path.join("downloads/DemCon", csv_file)
        df = pd.read_csv(csv_path, delimiter=";", encoding="utf-8")
        print('\nPreparando arquivo:', csv_file)
        
        if "VL_SALDO_INICIAL" in df.columns or "VL_SALDO_FINAL" in df.columns:
            df.fillna({"VL_SALDO_INICIAL": 0, "VL_SALDO_FINAL": 0}, inplace=True)
            df["VL_SALDO_INICIAL"] = df["VL_SALDO_INICIAL"].astype(str).str.replace(",", ".").astype(float)
            df["VL_SALDO_FINAL"] = df["VL_SALDO_FINAL"].astype(str).str.replace(",", ".").astype(float)

        if ('DDD' in df.columns):
            # Pegar somente os dois primeiros números do DDD e se NaN, transofmrar para 0
            df['DDD'] = df['DDD'].apply(lambda x: str(x).replace('.', '')[:2] if str(x) != 'nan' else '0')

        # Substitui os telefones com mais de 15 caracteres por 000000000
        if "Telefone" in df.columns:
            df["Telefone"] = df["Telefone"].apply(lambda x: x if len(str(x)) <= 15 else "000000000")

        df.to_csv(csv_path, index=False, sep=";", encoding="utf-8")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    create_tables()
