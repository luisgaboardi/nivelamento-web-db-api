import os
import csv
import zipfile
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
            if (page.page_number % 10 == 0 or page.page_number == len(pdf.pages)):
                print(f"Extraindo dados da tabela (página {page.page_number}/{len(pdf.pages)})...")
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
    
    if not os.path.exists(output_csv) or os.path.getsize(output_csv) == 0:
        raise ValueError(f"Falha ao gerar o arquivo CSV: {output_csv}")

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

def compress_csv_to_zip(csv_path, zip_path):
    """
    Compacta o arquivo CSV em um arquivo ZIP.
    
    :param csv_path: Caminho do CSV a ser compactado.
    :param zip_path: Caminho do arquivo ZIP de saída.
    """
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))

    if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
        raise ValueError(f"Falha ao criar o arquivo ZIP: {zip_path}")
    
    print(f"\nArquivo CSV compactado com sucesso em:\n{zip_path}")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    # Caminhos dos arquivos
    pdf_path = "downloads/Anexo_1.pdf"  # PDF do Anexo I
    raw_csv = "data_processing/rol_procedimentos_raw.csv"
    processed_csv = "data_processing/rol_procedimentos.csv"
    zip_file = f"data_processing/Teste_Luis_Queiroz.zip"

    # 2.1 e 2.2 Extrai a tabela do PDF e salva em CSV
    extract_table_from_pdf(pdf_path, raw_csv)

    # 2.4. Substitui abreviações nas colunas OD e AMB
    replace_abbreviations(raw_csv, processed_csv)

    # 2.3. Compacta o CSV em um arquivo ZIP
    compress_csv_to_zip(processed_csv, zip_file)