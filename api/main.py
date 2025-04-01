from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg

# Configurações do banco de dados
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ans_database"
DB_USER = "postgres"
DB_PASSWORD = "password"

# Inicializa o FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Substitua pelo domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Conexão com o banco de dados
async def connect_to_db():
    """
    Cria uma conexão assíncrona com o banco de dados PostgreSQL.
    """
    return await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Modelo de resposta para os dados
class OperadoraData(BaseModel):
    data: list

@app.get("/operadoras/busca", response_model=OperadoraData)
async def buscar_operadoras(
    termo: str = Query(..., min_length=3, description="Termo de busca textual (mínimo 3 caracteres)")
):
    """
    Realiza uma busca textual na tabela 'operadoras' e retorna os registros mais relevantes.

    :param termo: Termo de busca textual.
    """
    conn = None
    try:
        # Conecta ao banco de dados
        conn = await connect_to_db()

        # Query para buscar registros que correspondam ao termo
        query = """
        SELECT 
            id,
            registro_ans,
            cnpj,
            razao_social,
            nome_fantasia,
            modalidade,
            cidade,
            uf
        FROM 
            operadoras
        WHERE 
            razao_social ILIKE $1
            OR nome_fantasia ILIKE $1
        LIMIT 10;
        """
        # Executa a query com o termo de busca
        rows = await conn.fetch(query, f"%{termo}%")

        # Converte os resultados para uma lista de dicionários
        data = [dict(row) for row in rows]

        # Retorna os dados
        return {"data": data}

    except asyncpg.exceptions.UndefinedTableError:
        raise HTTPException(status_code=404, detail="Tabela 'operadoras' não encontrada.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar a busca: {str(e)}")
    finally:
        # Fecha a conexão com o banco de dados
        if conn:
            await conn.close()