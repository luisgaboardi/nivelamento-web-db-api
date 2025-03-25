import os
import csv
import pandas as pd
import pdfplumber


def extract_table_from_pdf(pdf_path, output_csv):
    """
    Extrai o conteúdo da tabela do PDF e salva em um arquivo CSV, ignorando cabeçalhos repetidos.
    
    :param pdf_path: Caminho do PDF de entrada.
    :param output_csv: Caminho do arquivo CSV de saída.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"O arquivo PDF não foi encontrado: {pdf_path}")
    
    # Lê o PDF
    data_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            print(f"Extraindo tabela da página {page.page_number}/{len(pdf.pages)}...")
            tables = page.extract_tables()
            for table in tables:
                data_tables.append(table)

    # Salva os dados em CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        header_written = False
        for table in data_tables:
            for row in table:
                row = [cell.replace("\n", " ") for cell in row]
                # Ignora cabeçalhos repetidos
                if not header_written and "VIGÊNCIA" in row:
                    writer.writerow(row)  # Escreve o cabeçalho
                    header_written = True
                    continue
            
                # Ignora cabeçalhos repetidos
                if "VIGÊNCIA" in row:
                    continue

                writer.writerow(row)  # Escreve cada linha da tabela no CSV
    
    print(f"\nTabela extraída com sucesso para:\n{output_csv}")

def replace_abbreviations(csv_path, output_csv):
    """
    Substitui abreviações nas colunas OD e AMB pelas descrições completas.
    
    :param csv_path: Caminho do CSV de entrada.
    :param output_csv: Caminho do CSV de saída com as abreviações substituídas.
    """
    # Legenda para substituição
    legend = {
        "OD": "Odontologia",
        "AMB": "Ambulatorial"
    }

    # Lê o CSV em um DataFrame
    df = pd.read_csv(csv_path, header=None)

    # Substitui as abreviações
    df.replace(legend, inplace=True)

    # Salva o CSV atualizado
    df.to_csv(output_csv, index=False, header=False, encoding="utf-8")
    print(f"\nAbreviações substituídas com sucesso e CSV atualizado em:\n{output_csv}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    # Caminhos dos arquivos
    pdf_path = "downloads/Anexo_1.pdf"  # PDF do Anexo I
    raw_csv = "data_processing/rol_procedimentos_raw.csv"
    processed_csv = "data_processing/rol_procedimentos.csv"

    # 2.1 e 2.2 Extrai a tabela do PDF e salva em CSV
    extract_table_from_pdf(pdf_path, raw_csv)

    # 2.4. Substitui abreviações nas colunas OD e AMB
    replace_abbreviations(raw_csv, processed_csv)