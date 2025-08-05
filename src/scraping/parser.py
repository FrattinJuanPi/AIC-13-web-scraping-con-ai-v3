from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def extract_headlines(html):
    """Extracts headlines and URLs from the provided HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    headlines = []

    for article in soup.find_all("article"):
        title_tag = article.find("h2") or article.find("h3")
        if title_tag and title_tag.a:
            title = title_tag.get_text(strip=True)
            url = title_tag.a['href']
            headlines.append({"title": title, "url": url})

    return headlines

def clean_html(html):
    """Cleans the HTML content by removing unnecessary tags."""
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    return str(soup)

def format_data(headlines, source):
    """Formats the extracted headlines into a structured JSON format."""
    formatted_data = []
    for item in headlines:
        item["source"] = source
        item["article_date"] = datetime.now().strftime('%Y-%m-%d')
        formatted_data.append(item)
    return json.dumps(formatted_data, ensure_ascii=False)

def reducir_htmls_por_listas(html_dict, max_listas=5):
    """Extrae las primeras listas UL relevantes (con links) de cada HTML en el diccionario."""
    htmls_reducidos = {}
    for source, html in html_dict.items():
        try:
            soup = BeautifulSoup(html, "html.parser")
            listas = soup.find_all("ul")

            listas_filtradas = []
            for ul in listas:
                if len(ul.find_all("li")) >= 3 and ul.find("a"):
                    listas_filtradas.append(str(ul))
                if len(listas_filtradas) >= max_listas:
                    break

            htmls_reducidos[source] = "\n".join(listas_filtradas)
        except Exception as e:
            print(f"Error procesando {source}: {e}")
            htmls_reducidos[source] = ""
    return htmls_reducidos
    
def dividir_html_en_bloques(html, max_chars=9000):
    """Divide un HTML en bloques separados si excede cierto largo (usando <ul> como unidad)."""
    soup = BeautifulSoup(html, "html.parser")
    listas = soup.find_all("ul")

    bloques = []
    bloque_actual = ""

    for ul in listas:
        ul_str = str(ul)
        if len(bloque_actual) + len(ul_str) > max_chars:
            if bloque_actual:
                bloques.append(bloque_actual)
                bloque_actual = ""
        bloque_actual += ul_str + "\n"

    if bloque_actual:
        bloques.append(bloque_actual)

    return bloques

def limpiar_titulares(df):
    """
    Limpia la columna 'source' eliminando terminaciones de dominio y sufijos '_bloque',
    y filtra las filas donde la URL tiene más de 2 palabras separadas por guiones.
    """
    import re
    # breakpoint()
    if df.empty:  
        df['source'] = df['source'].apply(lambda x: re.sub(r'\.com|\.ar|\.br|\.co|\.pe|\.cl|\.mx', '', x))
        df['source'] = df['source'].apply(lambda x: re.sub(r'_bloque\d+$', '', x))
        df['palabras_en_url'] = df['url'].str.count('-')
        df = df[df['palabras_en_url'] > 2]
    return df