from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import json

class Scraper:
    def __init__(self):
        chrome_options = Options()
        
        # --- CONFIGURAÇÃO "STEALTH" (FURTIVA) ---
        
        # 1. Definições de Janela e Cabeça
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless=new") # O modo novo é vital
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 2. O TRUQUE DO IDIOMA (Resolve o erro em espanhol)
        # Diz ao site que somos brasileiros e aceitamos português
        chrome_options.add_argument("--lang=pt-BR")
        chrome_options.add_argument("--accept-lang=pt-BR")

        # 3. Remove a barra "Chrome está sendo controlado por software de teste"
        # Isso remove bandeiras internas que sites usam para detectar robôs
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 4. User-Agent Genérico e Moderno
        # Vamos usar um bem comum para nos misturarmos na multidão
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        chrome_options.add_argument(f'user-agent={user_agent}')
        
        chrome_options.add_argument("--log-level=3")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Truque extra: altera uma propriedade interna do navegador para esconder o Selenium
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def get_price(self, url):
        try:
            self.driver.get(url)
            sleep(3) # Espera carregar o site
            
            # --- O CÉREBRO DA DECISÃO ---
            if "amazon" in url:
                return self._extract_amazon()
            elif "mercadolivre" in url:
                return self._extract_mercadolivre()
            else:
                print("❌ Loja não suportada ainda.")
                return None
            # ---------------------------

        except Exception as e:
            print(f"❌ Erro crítico no Selenium: {e}")
            return None

    def _extract_amazon(self):
        try:
            elementos = self.driver.find_elements(By.CSS_SELECTOR, '.a-price-whole')
            if not elementos:
                elementos = self.driver.find_elements(By.CSS_SELECTOR, '.a-offscreen')
            
            if not elementos: return None
            
            raw_price = elementos[0].get_attribute("textContent")
            return self._clean_price(raw_price)
        except:
            return None

    def _extract_mercadolivre(self):
        try:
            print("   -> Tentando estratégia JSON-LD (Dados Estruturados)...")
            
            # --- ESTRATÉGIA 1: JSON-LD (Blindada) ---
            # Note o 's' no final de elements. Isso impede o erro crítico.
            json_scripts = self.driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')
            
            if len(json_scripts) > 0:
                try:
                    json_text = json_scripts[0].get_attribute('innerHTML')
                    data = json.loads(json_text)
                    
                    # Lógica para caçar o preço dentro do dicionário
                    price = None
                    if 'offers' in data:
                        offers = data['offers']
                        if isinstance(offers, list):
                            price = offers[0].get('price') or offers[0].get('lowPrice')
                        else:
                            price = offers.get('price') or offers.get('lowPrice')
                    
                    if price:
                        print(f"   -> SUCESSO via JSON: {price}")
                        return float(price)
                except:
                    print("   -> JSON encontrado, mas estrutura inesperada. Indo para Plano B.")
            
            print("   -> JSON falhou. Tentando Planos Visuais...")

            # --- ESTRATÉGIA 2: Meta Tag (Plano B) ---
            meta_price = self.driver.find_elements(By.CSS_SELECTOR, "meta[itemprop='price']")
            if meta_price:
                price = meta_price[0].get_attribute("content")
                print(f"   -> SUCESSO via Meta Tag: {price}")
                return float(price)

            # --- ESTRATÉGIA 3: Visual (Plano C) ---
            selectors = [
                '.ui-pdp-price__second-line .andes-money-amount__fraction',
                '.andes-money-amount__fraction',
                '.ui-pdp-price__main-container .andes-money-amount__fraction'
            ]
            
            for selector in selectors:
                elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elementos:
                    print(f"   -> SUCESSO via Seletor CSS: {selector}")
                    return self._clean_price(elementos[0].text)
            
            # Se chegou aqui, nada funcionou
            print("❌ Esgotei todas as tentativas no ML.")
            self.driver.save_screenshot("debug_ml_final.png")
            return None

        except Exception as e:
            print(f"⚠️ Erro genérico na extração ML: {e}")
            return None

    def _clean_price(self, raw_price):
        """Função auxiliar para limpar R$ e vírgulas de qualquer loja"""
        if not raw_price: return None
        try:
            # Remove tudo que não é numero ou virgula
            numeric_string = re.sub(r'[^\d,]', '', raw_price)
            # Troca vírgula por ponto (1000,00 -> 1000.00)
            return float(numeric_string.replace(',', '.'))
        except:
            return None

    def close_browser(self):
        self.driver.quit()