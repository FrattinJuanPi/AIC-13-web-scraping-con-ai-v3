# 🧠 Scraper con IA para sitios web de noticias económicas

Este proyecto implementa un scraper generalizado potenciado por inteligencia artificial, diseñado para extraer información útil desde páginas web dinámicas, incluso cuando los datos no están estructurados de forma clara. Utiliza **Selenium** para la captura dinámica de HTML y modelos de lenguaje de **Azure OpenAI** (como GPT o Gemini) para procesar y estructurar la información de forma flexible.

---

## 🚀 Descripción general

El scraper accede a sitios web de noticias económicas, descarga el HTML completo con Selenium, y lo divide en bloques analizables. Luego, utiliza modelos de lenguaje IA para interpretar esos bloques y extraer contenido relevante como títulos, fechas, enlaces y fuentes.

Este enfoque híbrido combina la confiabilidad del scraping tradicional con la adaptabilidad de los modelos LLM.

---

## 🧠 Scraping asistido por Inteligencia Artificial

En ciertos escenarios, especialmente cuando se requiere procesar grandes volúmenes de HTML sin estructura clara, o cuando los datos se presentan de forma inconsistente, las técnicas tradicionales de scraping pueden no ser suficientes.

Además, muchos modelos de lenguaje actuales, como **Gemini**, **GPT** o los modelos de **Azure OpenAI**, **no permiten navegación web directa vía API**, lo que plantea desafíos adicionales si se desea automatizar tareas de extracción con ayuda de IA.

### ✅ Solución propuesta: combinación de scraping + IA

Este proyecto implementa un enfoque mixto que:

- Accede a sitios web (estáticos o dinámicos) mediante **Selenium**.
- Maneja bloqueos utilizando headers aleatorios, tiempo de espera y rotación de agente de usuario.
- Extrae el HTML completo de las páginas indicadas.
- Filtra los elementos correspondientes a **listas o bloques de noticias**.
- Divide los HTMLs en **bloques más pequeños** para ajustarse a los límites de tokens de los LLM.
- Envía estos bloques a un modelo IA (como GPT-4 o Gemini 1.5 Flash) para su interpretación.
- El modelo responde con **contenido estructurado**, facilitando su posterior análisis o almacenamiento.

⚠️ Este enfoque **no reemplaza** al scraping tradicional, sino que lo **complementa** cuando la lógica de extracción es compleja o inconsistente.

---

## ⚙️ Procesamiento paso a paso

1. **Descarga HTML**: Se utiliza `selenium` para abrir sitios, esperar contenido dinámico y capturar el HTML completo.
2. **Reducción de HTML**: Se filtran listas de interés desde el HTML crudo.
3. **División en bloques**: Se fragmenta el contenido para cumplir con los límites del modelo IA.
4. **Extracción con IA**: Cada bloque es enviado a un modelo LLM que responde con contenido estructurado en JSON.
5. **Almacenamiento**: Los resultados se guardan localmente como `.json`, `.csv` o `.parquet` y se pueden subir a **Azure Data Lake**.

---

## ▶️ Uso

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```
### 2. Configurar credenciales
Crear un archivo .env con las siguientes variables:

```STORAGE_ACCOUNT_NAME = ""
STORAGE_ACCOUNT_KEY = ""
AZURE_ENDPOINT = ""
AZURE_API_KEY = ""
AZURE_API_VERSION =  ""
IA_MODEL_NAME = ""
DEPLOYMENT = ""
```

### 3. Ejecutar el scraper
```
python main.py
```