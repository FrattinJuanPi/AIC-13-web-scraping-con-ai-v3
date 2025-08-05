# import sys
# print(sys.executable)
import json
from config import (STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY, AZURE_ENDPOINT,AZURE_API_KEY,AZURE_API_VERSION,IA_MODEL_NAME)
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
    # print(dict_download_htmls)
    print('holaaaaaaaaaaaaaaaaaaa')
    json_data = json.dumps(dict_download_htmls, ensure_ascii=False, indent=2)
    # Save the downloaded HTML content to Azure Blob Storage
    AzureStorage.save_json_to_abfss(
        "abfss://scraps@scrapingiastorage.dfs.core.windows.net/raw/htmls.json",
        json_data,
        overwrite=True
    )
    # spark = SparkSession.builder.getOrCreate()
    print('2holaaaaaaaaaaaaaa')
    # data = [(k, v) for k, v in dict_download_htmls.items()]
    # df_news = spark.createDataFrame(data, schema=["source", "html"])

    # df_news_pd = df_news.toPandas()

    # Step 2: Parse the downloaded HTML content
    # print('-'*60)
    # for dominio, html in dict_download_htmls.items():
    #     print(f"Dominio: {dominio}, longitud HTML: {len(html)}")
    # print('-'*60)
    html_dict_reducido = reducir_htmls_por_listas(dict_download_htmls)
    # breakpoint()
    # parsed_data = parse_html(html_dict)
    # print("-" * 60)
    # for dominio, html in html_dict_reducido.items():
    #     print(f"Dominio: {dominio}, longitud HTML: {len(html)}")
    # print("-" * 60)
    
    html_dict_dividido = {source: dividir_html_en_bloques(html) for source, html in html_dict_reducido.items()}
    # breakpoint()
    # Step 3: Process the extracted data
    # processed_data = process_data(parsed_data)
    openai_client = OpenAIClient(
        endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
        model_name=IA_MODEL_NAME
    )
    df_titulares_azure = openai_client.extraer_todos_azure_por_bloques(html_dict_dividido)
    # breakpoint()
    df_titulares_azure = limpiar_titulares(df_titulares_azure)
    
    # Step 4: Upload processed data to Azure
    # spark = SparkSession.builder.getOrCreate()
    # df_titulares_azure_spark = spark.createDataFrame(df_titulares_azure)
    # Supón que ya tienes tu SparkSession y tu DataFrame
    azure_storage = AzureStorage(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
    # import pandas as pd

    # Supón que tienes un DataFrame llamado df
    df_titulares_azure.to_parquet("output.parquet", engine="pyarrow", index=False)
    azure_storage.upload_file("output.parquet", "clean/output.parquet", "scraps")
    # azure_storage.save_spark_df_as_parquet(df_titulares_azure_spark, "abfss://scraps@scrapingiastorage.dfs.core.windows.net/clean/")
    # upload_to_azure(processed_data)


if __name__ == "__main__":
    main()
