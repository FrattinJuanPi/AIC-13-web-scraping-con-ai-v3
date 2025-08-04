import os

class Config:
    STORAGE_ACCOUNT_KEY = os.getenv("STORAGE_ACCOUNT_KEY", "your_storage_account_key_here")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "https://your_azure_endpoint_here/")
    AZURE_API_KEY = os.getenv("AZURE_API_KEY", "your_azure_api_key_here")
    AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-12-01-preview")
    IA_MODEL_NAME = os.getenv("IA_MODEL_NAME", "o4-mini")
    DEPLOYMENT = os.getenv("DEPLOYMENT", "o4-mini-challengue")