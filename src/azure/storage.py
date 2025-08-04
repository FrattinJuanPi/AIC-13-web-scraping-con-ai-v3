from azure.storage.filedatalake import DataLakeServiceClient
import os

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
            print(f"Error initializing Azure Storage Account: {e}")
            return None

    def upload_file(self, file_path, file_name, file_system_name):
        file_system_client = self.service_client.get_file_system_client(file_system_name)
        file_client = file_system_client.get_file_client(file_name)

        with open(file_path, "rb") as data:
            file_client.upload_data(data, overwrite=True)

    def download_file(self, file_name, file_system_name, download_path):
        file_system_client = self.service_client.get_file_system_client(file_system_name)
        file_client = file_system_client.get_file_client(file_name)

        with open(download_path, "wb") as download_file:
            download_file.write(file_client.download_file().readall())