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


def import_csv_with_copy(csv_files):
    """
    Importa múltiplos arquivos CSV para uma tabela no banco de dados PostgreSQL usando o comando COPY.

    :param csv_files: Lista de caminhos dos arquivos CSV.
    """
    print('\n-----------------------------\n')
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

        for csv_file in csv_files:
            csv_path = os.path.join("downloads/DemCon", csv_file)
            print(f"\nImportando arquivo: {csv_file}")
            if 'OPSA' in csv_file:
                table_name = "operadoras"
                columns = """
                    registro_ans,
                    cnpj,
                    razao_social,
                    nome_fantasia,
                    modalidade,
                    logradouro,
                    numero,
                    complemento,
                    bairro,
                    cidade,
                    uf,
                    cep,
                    ddd,
                    telefone,
                    fax,
                    endereco_eletronico,
                    representante,
                    cargo_representante,
                    regiao_comercializacao,
                    data_registro_ans
                """
            else:
                table_name = "demonstracoes_contabeis"
                columns = """
                    data,
                    reg_ans,
                    cd_conta_contabil,
                    descricao,
                    vl_saldo_inicial,
                    vl_saldo_final
                """

            # Usa o comando COPY para importar os dados
            with open(csv_path, 'r', encoding='utf-8') as file:
                cursor.copy_expert(f"""
                    COPY {table_name} ({columns}) 
                    FROM STDIN
                    DELIMITER ';'
                    CSV HEADER;
                """, file)

        # Confirma as alterações
        conn.commit()
        print(f"\nTodos os arquivos foram importados com sucesso!")

    except Exception as e:
        print(f"Erro ao importar arquivos CSV: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def check_inserted_data(table_name):
    """
    Conecta ao banco de dados PostgreSQL e verifica a quantidade de tuplas na tabela especificada.

    :param table_name: Nome da tabela no banco de dados.
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

        # Query para contar a quantidade de tuplas na tabela
        count_data = f"SELECT COUNT(*) FROM {table_name};"

        # Executa a query
        cursor.execute(count_data)
        count = cursor.fetchone()[0]
        print(f"\nA tabela '{table_name}' contém {count} tuplas.")

    except Exception as e:
        print(f"\nErro ao verificar os dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def top_10_operadoras_trimestre():
    """
    Conecta ao banco de dados PostgreSQL e retorna as 10 operadoras com maiores despesas em 
    "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre.
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

        # Query para retornar as 10 operadoras com maiores despesas
        top_10_query = """
        SELECT 
            o.razao_social AS operadora,
            o.cnpj,
            o.uf,
            d.reg_ans,
            SUM(d.vl_saldo_final) AS total_despesas
        FROM 
            demonstracoes_contabeis d
        JOIN 
            operadoras o
        ON 
            d.reg_ans = o.registro_ans
        WHERE 
            d.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
            AND d.data >= (date_trunc('quarter', CURRENT_DATE) - INTERVAL '3 months')
            AND d.data < date_trunc('quarter', CURRENT_DATE)
        GROUP BY 
            o.razao_social, o.cnpj, o.uf, d.reg_ans
        ORDER BY 
            total_despesas DESC
        LIMIT 10;
        """

        print("\nConsultando: Top 10 Operadoras com maiores despesas em 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR' no último trimestre:")

        # Executa a query
        cursor.execute(top_10_query)
        results = cursor.fetchall()

        # Define os cabeçalhos da tabela
        headers = ["Operadora", "CNPJ", "UF", "Registro ANS", "Total Despesas"]

        # Exibe os resultados em formato de tabela
        print(tabulate(results, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"Erro ao realizar consulta: {e}")
    finally:
        # Fecha a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def top_10_operadoras_ano():
    """
    Conecta ao banco de dados PostgreSQL e retorna as 10 operadoras com maiores despesas em 
    "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último ano.
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

        # Query para retornar as 10 operadoras com maiores despesas
        top_10_query = """
        SELECT 
            o.razao_social AS operadora,
            o.cnpj,
            o.uf,
            d.reg_ans,
            SUM(d.vl_saldo_final) AS total_despesas
        FROM 
            demonstracoes_contabeis d
        JOIN 
            operadoras o
        ON 
            d.reg_ans = o.registro_ans
        WHERE 
            d.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
            AND d.data >= '2024-01-01'
            AND d.data <= '2024-12-31'
        GROUP BY 
            o.razao_social, o.cnpj, o.uf, d.reg_ans
        ORDER BY 
            total_despesas DESC
        LIMIT 10;
        """

        print("\nConsultando: Top 10 Operadoras com maiores despesas em na categoria no último ANO:")

        # Executa a query
        cursor.execute(top_10_query)
        results = cursor.fetchall()

        # Define os cabeçalhos da tabela
        headers = ["Operadora", "CNPJ", "UF", "Registro ANS", "Total Despesas"]

        # Exibe os resultados em formato de tabela
        print(tabulate(results, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"Erro ao realizar consulta: {e}")
    finally:
        # Fecha a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()



if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    create_tables()

    prepare_csv_files()

    csv_files = [f for f in os.listdir("downloads/DemCon") if f.endswith(".csv")]

    import_csv_with_copy(csv_files)
    
    check_inserted_data("demonstracoes_contabeis")
    check_inserted_data("operadoras")

    top_10_operadoras_trimestre()

    top_10_operadoras_ano()
