from openai import AzureOpenAI
import time
import re
import json
from datetime import datetime
import pandas as pd
from config import DEPLOYMENT


class OpenAIClient:
    def __init__(self, endpoint, api_key, api_version, model_name):
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        self.model_name = model_name

    def get_completion(self, prompt, max_retries=5):
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model= DEPLOYMENT,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e):
                    time.sleep(60)  # Wait before retrying
                else:
                    raise e
        return None

    def extraer_titulares_azure(self, html, source, max_retries=5):
        """Extrae titulares y URLs usando Azure OpenAI, con retry en caso de error 429."""
        for intento in range(max_retries):
            try:
                prompt = (
                    "You are a data analyst. Your task is to read this reduced HTML fragment "
                    "(usually containing article links) and extract a list of main news headlines.\n\n"
                    "Do NOT include links to sections, categories, tags, or general pages.\n"
                    "Only include individual news article headlines with their corresponding URLs.\n\n"
                    "Output a valid JSON list with this exact format:\n"
                    "[{\"title\": \"...\", \"url\": \"...\"}]\n\n"
                    "Use double quotes for all JSON keys and values.\n"
                    "Make sure the title is complete and informative. If the title seems too short, "
                    "try to infer or complete it using the last part of the URL (where words are separated by hyphens).\n\n"
                    "Example:\n"
                    "[{\"title\": \"Man arrested for fraud in government bidding\", \"url\": \"https://example.com/news1\"}]\n\n"
                    f"HTML:\n{html}"
                )

                response = self.client.chat.completions.create(
                    model=DEPLOYMENT,
                    messages=[{"role": "user", "content": prompt}]
                )

                response_text = response.choices[0].message.content
                match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if not match:
                    raise ValueError("No se encontró JSON en la respuesta")

                data = json.loads(match.group(0))
                for item in data:
                    item["source"] = source
                    item["article_date"] = datetime.now().strftime('%Y-%m-%d')
                return data

            except Exception as e:
                if "429" in str(e):
                    print(f"Intento {intento + 1}/{max_retries} - Error 429 para {source}, esperando 60 segundos...")
                    time.sleep(60)
                else:
                    print(f"Error extrayendo con Azure para {source}: {e}")
                    break

        return []

    def extraer_todos_azure_por_bloques(self, html_dict_dividido, max_retries=5):
        """Procesa bloques de HTML por cada dominio y extrae titulares con Azure."""
        todas_filas = []

        for source, bloques in html_dict_dividido.items():
            print(f"Procesando {source} ({len(bloques)} bloque(s))")

            for i, bloque in enumerate(bloques):
                print(f"  → Bloque {i+1}/{len(bloques)}")
                try:
                    filas = self.extraer_titulares_azure(bloque, source=f"{source}_bloque{i+1}", max_retries=max_retries)
                    todas_filas.extend(filas)
                except Exception as e:
                    print(f" Error en {source} bloque {i+1}: {e}")

        return pd.DataFrame(todas_filas)

