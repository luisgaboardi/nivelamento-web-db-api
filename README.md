# Desafio Técnico - Arquitetura e Tecnologias

## 📌 Visão Geral
Este projeto tem como objetivo desenvolver uma solução para os testes de nivelamento, abordando web scraping, transformação de dados, banco de dados e API. A implementação será feita utilizando Python e tecnologias adequadas para cada etapa.

## 🏗 Arquitetura
A solução seguirá uma arquitetura modular, dividida em quatro principais componentes:

1. **Web Scraping**: Responsável por acessar o site da ANS e baixar os anexos necessários.
2. **Transformação de Dados**: Extração e estruturação dos dados em CSV a partir dos PDFs.
3. **Banco de Dados**: Armazenamento e consultas analíticas das informações extraídas.
4. **API e Interface Web**: Exposição dos dados via API e interface frontend para buscas.

Cada módulo será desenvolvido separadamente para garantir manutenibilidade e escalabilidade.

## 🛠 Tecnologias Utilizadas

### 🔍 Web Scraping
- **Linguagem:** Python 3.10
- **Bibliotecas:**
  - `requests` - Para requisições HTTP.
  - `BeautifulSoup` - Para extração de dados HTML.
  - `Selenium` - Para interação com páginas dinâmicas.

### 📄 Processamento de PDF e Transformação de Dados
- **Bibliotecas:**
  - `pdfplumber` - Para extração de texto dos PDFs.
  - `pandas` - Para manipulação e estruturação dos dados.
  - `csv` - Para exportação dos dados em formato estruturado.
  - `zipfile` - Para compactação dos arquivos.

### 🗄 Banco de Dados
- **Banco de Dados:** PostgreSQL 10+ (ou MySQL 8)
- **Bibliotecas:**
  - `psycopg2` - Para conexão com PostgreSQL.
  - `SQLAlchemy` - ORM para manipulação de dados.

### 🌐 API e Interface Web
- **Backend:**
  - `FastAPI` - Para criação da API RESTful.
  - `Uvicorn` - Para execução do servidor.
- **Frontend:**
  - `Vue.js` - Para desenvolvimento da interface web.
- **Ferramentas de Teste:**
  - `Postman` - Para validação das requisições da API.

## 📁 Estrutura de Diretórios
```plaintext
📂 nivelamento-web-db-api
│── 📂 scraping              # Código do web scraping
│── 📂 data_processing       # Extração e transformação dos dados
│── 📂 database              # Scripts SQL e manipulação do banco
│── 📂 api                   # API em FastAPI
│── 📂 frontend              # Interface web em Vue.js
│── 📂 tests                 # Testes unitários e de integração
│── README.md                # Documentação do projeto
```

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar o Repositório
```sh
git clone https://github.com/luisgaboardi/nivelamento-web-db-api
cd nivelamento-web-db-api
```

### 2️⃣ Criar Ambiente Virtual e Instalar Dependências
```sh
python -m venv venv
source venv/bin/activate  # No Windows use venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Executar os Módulos
- **Web Scraping:**
  ```sh
  python scraping/main.py
  ```
- **Processamento de Dados:**
  ```sh
  python data_processing/main.py
  ```
- **Configuração do Banco de Dados:**
  ```sh
  python database/setup.py
  ```
- **Execução da API:**
  ```sh
  uvicorn api.main:app --reload
  ```
- **Execução do Frontend:**
  ```sh
  cd frontend
  npm install
  npm run dev
  ```

## 🧪 Testes
Para rodar os testes:
```sh
pytest tests/
```

---

Caso tenha dúvidas ou sugestões, entre em contato! 🚀

