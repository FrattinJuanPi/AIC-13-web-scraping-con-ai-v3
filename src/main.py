import os
from src.config import STORAGE_ACCOUNT_KEY, YOUR_ENDPOINT, YOUR_API_KEY, YOUR_IA_MODEL_NAME, DEPLOYMENT
from src.scraping.downloader import download_htmls
from src.scraping.parser import parse_html
from src.azure.storage import upload_to_azure
from src.data.processing import process_data

def main():
    urls = [
        "https://www.cnbc.com/economy/",
        "https://www.elcomercio.pe/economia/",
        "https://www.larepublica.co/economia",
        "https://www.emol.com/noticias/Economia/portada.aspx",
        "https://www.clarin.com/economia",
        "https://www.infobae.com/economia",
        "https://tn.com.ar/economia/"
    ]

    # Step 1: Download HTML content
    html_dict = download_htmls(urls)

    # Step 2: Parse the downloaded HTML content
    parsed_data = parse_html(html_dict)

    # Step 3: Process the extracted data
    processed_data = process_data(parsed_data)

    # Step 4: Upload processed data to Azure
    upload_to_azure(processed_data)

if __name__ == "__main__":
    main()