from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import tempfile
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

def get_random_headers():
    """ Esta función setea los parámetros de conexión 
    con headers aleatorios 
    """
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com"
    }

# Descarga de  HTMLs 
def download_htmls(urls, tiempo_espera=5):
    """ Esta función descarga los HTMLs completos 
    utilizando scraping dinámico con beatufoulsoup 
    """
    
    html_dict = {}

    for url in urls:
        headers = get_random_headers()
        user_data_dir = tempfile.mkdtemp()

        opciones = Options()
        opciones.add_argument("--headless") 
        opciones.add_argument("--disable-gpu")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument(f"--user-data-dir={user_data_dir}")
        opciones.add_argument(f"user-agent={headers['User-Agent']}")

        try:
            driver = webdriver.Chrome(options=opciones)
            driver.get(url)

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article, h2, h3, .headline, a[href]"))
            )

            # Scroll para cargar contenido dinámico, sirve para evitar bloqueos a bots
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            time.sleep(tiempo_espera)

            html_completo = driver.page_source
            dominio = url.split("//")[-1].split("/")[0].replace("www.", "")
            html_dict[dominio] = html_completo

            driver.save_screenshot(f"src/screen/screenshot_{dominio}.png")
            driver.quit()

        except Exception as e:
            print(f"Error procesando {url}: {e}")
            continue

    return html_dict
 
    