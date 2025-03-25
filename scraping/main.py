import os
import requests
from bs4 import BeautifulSoup

def download_pdfs():

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
        
        # Verificar se o arquivo foi baixado corretamente
        if os.path.getsize(pdf_filename) == 0:
            raise ValueError(f"Falha ao baixar o arquivo PDF: {pdf_filename}")
            
        pdf_files.append(pdf_filename)
    
    return pdf_files

if __name__ == "__main__":
    pdf_files = download_pdfs()
    print("Arquivos baixados com sucesso:")
    for pdf_file in pdf_files:
        print(pdf_file)