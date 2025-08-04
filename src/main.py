import os
import json
from src.config import STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY, YOUR_ENDPOINT, YOUR_API_KEY, YOUR_IA_MODEL_NAME, DEPLOYMENT
from src.scraping.downloader import download_htmls
from src.scraping.parser import dividir_html_en_bloques, reducir_htmls_por_listas, limpiar_titulares
from src.azure.storage import AzureStorage
from src.azure.openai_client import OpenAIClient
from src.data.processing import process_data
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
    json_data = json.dumps(dict_download_htmls, ensure_ascii=False, indent=2)
    AzureStorage.save_json_to_abfss(
        "abfss://scraps@scrapingiastorage.dfs.core.windows.net/raw/htmls.json",
        json_data,
        overwrite=True
    )
    # spark = SparkSession.builder.getOrCreate()

    # data = [(k, v) for k, v in dict_download_htmls.items()]
    # df_news = spark.createDataFrame(data, schema=["source", "html"])

    # df_news_pd = df_news.toPandas()

    # Step 2: Parse the downloaded HTML content
    # print('-'*60)
    # for dominio, html in dict_download_htmls.items():
    #     print(f"Dominio: {dominio}, longitud HTML: {len(html)}")
    # print('-'*60)
    html_dict_reducido = reducir_htmls_por_listas(dict_download_htmls)
    # parsed_data = parse_html(html_dict)
    # print("-" * 60)
    # for dominio, html in html_dict_reducido.items():
    #     print(f"Dominio: {dominio}, longitud HTML: {len(html)}")
    # print("-" * 60)
    
    html_dict_dividido = {source: dividir_html_en_bloques(html) for source, html in html_dict_reducido.items()}
    
    # Step 3: Process the extracted data
    # processed_data = process_data(parsed_data)
    openai_client = OpenAIClient(
        endpoint=YOUR_ENDPOINT,
        api_key=YOUR_API_KEY,
        api_version=DEPLOYMENT,
        model_name=YOUR_IA_MODEL_NAME
    )
    df_titulares_azure = openai_client.extraer_todos_azure_por_bloques(html_dict_dividido)
    
    df_titulares_azure = limpiar_titulares(df_titulares_azure)
    
    # Step 4: Upload processed data to Azure
    spark = SparkSession.builder.getOrCreate()
    df_titulares_azure_spark = spark.createDataFrame(df_titulares_azure)
    # Supón que ya tienes tu SparkSession y tu DataFrame
    azure_storage = AzureStorage(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
    azure_storage.save_spark_df_as_parquet(df_titulares_azure_spark, "abfss://scraps@scrapingiastorage.dfs.core.windows.net/clean/")
    # upload_to_azure(processed_data)


if __name__ == "__main__":
    main()
