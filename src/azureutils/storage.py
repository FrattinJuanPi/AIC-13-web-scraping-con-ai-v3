from azure.storage.filedatalake import DataLakeServiceClient
import json
import os
import pandas as pd


class AzureStorage:
    def __init__(self, account_name, account_key):
        self.account_name = account_name
        self.account_key = account_key
        self.service_client = self._initialize_storage_account()

    def _initialize_storage_account(self):
        try:
            service_client = DataLakeServiceClient(
                account_url=f"https://{self.account_name}.dfs.core.windows.net",
                credential=self.account_key
            )
            return service_client
        except Exception as e:
            print(f"[ERROR] Inicializando cuenta de Azure: {e}")
            return None

    def upload_file(self, file_path, file_name, file_system_name):
        try:
            file_system_client = self.service_client.get_file_system_client(
                file_system_name)
            file_client = file_system_client.get_file_client(file_name)

            with open(file_path, "rb") as data:
                file_client.upload_data(data, overwrite=True)
            print(f"[OK] Archivo subido: {file_name}")
        except Exception as e:
            print(f"[ERROR] Subiendo archivo a Azure: {e}")

    def download_file(self, file_name, file_system_name, download_path):
        try:
            file_system_client = self.service_client.get_file_system_client(
                file_system_name)
            file_client = file_system_client.get_file_client(file_name)

            with open(download_path, "wb") as download_file:
                download_file.write(file_client.download_file().readall())
            print(f"[OK] Archivo descargado: {download_path}")
        except Exception as e:
            print(f"[ERROR] Descargando archivo de Azure: {e}")

    def save_json(self, json_data: dict, local_path: str):
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] JSON guardado localmente: {local_path}")
        except Exception as e:
            print(f"[ERROR] Guardando JSON local: {e}")

    def save_parquet_from_df(self, df: pd.DataFrame, local_path: str):
        try:
            df.to_parquet(local_path, index=False)
            print(f"[OK] Parquet guardado localmente: {local_path}")
        except Exception as e:
            print(f"[ERROR] Guardando Parquet local: {e}")
