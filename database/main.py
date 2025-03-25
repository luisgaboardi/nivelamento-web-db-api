import os
from zipfile import ZipFile
import requests


def download_zips(download_dir="downloads") -> list:
    """
    Baixa arquivos ZIP da ANS a partir de uma lista de URLs.

    :param download_dir: Diretório onde os arquivos ZIP serão salvos.
    :return: Lista de caminhos dos arquivos ZIP baixados.
    """
    # URLs dos arquivos ZIP
    urls = [
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/1T2024.zip",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/2T2024.zip",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/3T2024.zip",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/4T2024.zip",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/1T2023.zip",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/2T2023.zip",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/3T2023.zip",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/4T2023.zip",
    ]
    
    zip_files = []

    os.makedirs(download_dir, exist_ok=True)

    for i, url in enumerate(urls):
        print(f"Baixando arquivo {i + 1}/{len(urls)}: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        zip_filename = os.path.join(download_dir, f"DemCon_{i + 1}.zip")
        
        with open(zip_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  # Baixa em blocos
                file.write(chunk)
        
        if not os.path.exists(zip_filename) or os.path.getsize(zip_filename) == 0:
            raise ValueError(f"Falha ao baixar o arquivo ZIP: {zip_filename}")
        
        zip_files.append(zip_filename)

    print("\nArquivos baixados com sucesso:")
    for zip_file in zip_files:
        print(zip_file)
    
    return zip_files

def extract_zip(zip_filename, extract_to="downloads/DemCon") -> str:
    """
    Extrai os arquivos de um arquivo ZIP para o diretório especificado e verifica a integridade dos arquivos extraídos.

    :param zip_filename: Caminho do arquivo ZIP a ser extraído.
    :param extract_to: Diretório onde os arquivos serão extraídos.
    :return: Caminho do diretório onde os arquivos foram extraídos.
    """
    if not os.path.exists(zip_filename):
        raise FileNotFoundError(f"O arquivo ZIP não foi encontrado: {zip_filename}")
    
    os.makedirs(extract_to, exist_ok=True)
    
    with ZipFile(zip_filename, "r") as zipf:
        zipf.extractall(extract_to)
        extracted_files = zipf.namelist()
    
    for file in extracted_files:
        file_path = os.path.join(extract_to, file)
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            raise ValueError(f"Arquivo extraído está corrompido ou vazio: {file_path}")
    
    return extract_to

def download_csv(csv_url, output_path="downloads/DemCon/OPSA.csv"):
    """
    Baixa um arquivo CSV de uma URL e salva no caminho especificado.

    :param csv_url: URL do arquivo CSV a ser baixado.
    :param output_path: Caminho onde o arquivo CSV será salvo.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Baixando arquivo: {csv_url}")
    response = requests.get(csv_url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        raise ValueError(f"Falha ao baixar o arquivo CSV: {output_path}")

    print(f"Arquivo CSV baixado com sucesso em: {output_path}")
    return output_path

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    downloaded_files = download_zips()
    for zip_file in downloaded_files:
        extract_zip(zip_file)
    print(f"\nArquivos extraídos com sucesso em: downloads/DemCon\n")
    
    csv_url = 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv'
    csv_path = "downloads/DemCon/OPSA.csv"
    download_csv(csv_url, output_path=csv_path)
 