import psycopg2

# Configurações do banco de dados
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ans_database"
DB_USER = "postgres"
DB_PASSWORD = "password"


def clear_database():
    """
    Remove todas as tabelas do banco de dados PostgreSQL.
    """
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

        # Script para excluir todas as tabelas no esquema 'public'
        cursor.execute("""
        DO $$ DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END $$;
        """)

        # Confirma as alterações
        conn.commit()
        print("Banco de dados limpo com sucesso!")

    except Exception as e:
        print(f"Erro ao limpar o banco de dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    clear_database()