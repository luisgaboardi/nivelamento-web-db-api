import os
from zipfile import ZipFile
import requests
from bs4 import BeautifulSoup
import os

def download_pdfs() -> list:
    """
    Baixa arquivos PDF da ANS.
    """

    # 1.1
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "Anexo" in href and href.endswith(".pdf"):
            pdf_links.append(href)
    
    if len(pdf_links) < 2:
        raise ValueError("Não foi possível encontrar os PDFs necessários.")
    
    # 1.2
    pdf_files = []
    os.makedirs("downloads", exist_ok=True)
    
    for i, pdf_url in enumerate(pdf_links[:2]):
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()
        
        pdf_filename = f"downloads/Anexo_{i+1}.pdf"
        with open(pdf_filename, "wb") as file:
            file.write(pdf_response.content)
        
        if not os.path.exists(pdf_filename) or os.path.getsize(pdf_filename) == 0:
            raise ValueError(f"Falha ao baixar o arquivo PDF: {pdf_filename}")
            
        pdf_files.append(pdf_filename)

    print("Arquivos baixados com sucesso:")
    for pdf_file in pdf_files:
        print(pdf_file)
    
    return pdf_files

# 1.3
def zip_pdfs(pdf_files, zip_filename="downloads/Anexos.zip") -> str:
    """
    Compacta arquivos PDF para um arquivo ZIP.

    :param pdf_files: Arquivos PDFs a serem compactados.
    :param zip_filename: Arquivo ZIP resultante.
    """
    with ZipFile(zip_filename, "w") as zipf:
        for pdf in pdf_files:
            zipf.write(pdf, os.path.basename(pdf))

    if not os.path.exists(zip_filename) or os.path.getsize(zip_filename) == 0:
        raise ValueError(f"Falha ao criar o arquivo ZIP: {zip_filename}")

    print(f"Arquivos compactados com sucesso em:\n{zip_filename}")
    return zip_filename

def extract_zip(zip_filename, extract_to="downloads/extracted") -> str:
    """
    Extrai os arquivos de um arquivo ZIP para o diretório especificado e verifica a integridade dos arquivos extraídos.

    :param zip_filename: Caminho do arquivo ZIP a ser extraído.
    :param extract_to: Diretório onde os arquivos serão extraídos.
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
    
    print(f"Arquivos extraídos com sucesso para:\n{extract_to}")
    return extract_to


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    print('Web Scraping - ANS')
    print('--------------------')
    print('Baixando arquivos PDFs...\n')
    pdf_files = download_pdfs()

    print('\nCompactando arquivos PDFs...\n')
    zip_file = zip_pdfs(pdf_files)

    print('\nExtraindo arquivos do ZIP...\n')
    extract_zip(zip_file)