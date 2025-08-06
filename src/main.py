# import sys
# print(sys.executable)
import json
from config import (STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY,
                    AZURE_ENDPOINT, AZURE_API_KEY, AZURE_API_VERSION, IA_MODEL_NAME)
from scraping.downloader import download_htmls
from scraping.parser import dividir_html_en_bloques, reducir_htmls_por_listas, limpiar_titulares
from azureutils.storage import AzureStorage
from azureutils.openai_client import OpenAIClient
from pyspark.sql import SparkSession


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
    dict_download_htmls = download_htmls(urls)

    azure_storage = AzureStorage(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
    json_data = json.dumps(dict_download_htmls, ensure_ascii=False, indent=2)
    azure_storage.save_json(json_data, "src/data/raw/htmls.json")
    azure_storage.upload_file("src/data/raw/htmls.json",
                              "htmls.json", "scraps/raw")
    # Step 2: Parse and process HTML content
    html_dict_reducido = reducir_htmls_por_listas(dict_download_htmls)

    html_dict_dividido = {source: dividir_html_en_bloques(
        html) for source, html in html_dict_reducido.items()}
   
    # Step 3: Process the extracted data
    openai_client = OpenAIClient(
        endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
        model_name=IA_MODEL_NAME
    )
    df_titulares_azure = openai_client.extraer_todos_azure_por_bloques(
        html_dict_dividido)
        
    df_titulares_azure = limpiar_titulares(df_titulares_azure)

    # Step 4: Upload processed data to Azure
    azure_storage.save_parquet_from_df(df_titulares_azure, "src/data/clean/titulares.parquet")
    azure_storage.upload_file(
        "src/data/clean/titulares.parquet", "titulares.parquet", "scraps/clean")

if __name__ == "__main__":
    main()
