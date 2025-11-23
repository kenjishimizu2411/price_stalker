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
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--lang=pt-BR")
        chrome_options.add_argument("--accept-lang=pt-BR")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)  
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def get_price(self, url):
        try:
            self.driver.get(url)
            sleep(12) 
            price = None
            if "amazon" in url:
                price = self._extract_amazon()
            elif "mercadolivre" in url:
                price = self._extract_mercadolivre()
            else:
                print("❌ Loja não suportada.")
                return None
            
            if price is None:
                print("📸 Não achei o preço. Tirando print de diagnóstico...")
                filename = f"erro_{url.split('//')[1].split('/')[0]}.png"
                self.driver.save_screenshot(filename)
            
            return price

        except Exception as e:
            print(f"❌ Erro crítico no Selenium: {e}")
            self.driver.save_screenshot("erro_critico.png")
            return None

    def _extract_amazon(self):
        try:
            if "continuar comprando" in self.driver.page_source:
                print("🐶 Bloqueio 'Soft' da Amazon detectado. Tentando furar...")
                try:
                    botoes = self.driver.find_elements(By.TAG_NAME, "button")
                    for btn in botoes:
                        if "continuar comprando" in btn.text.lower():
                            btn.click()
                            print("   -> Botão clicado! Esperando recarregar...")
                            sleep(6)
                            break
                except Exception as e_bypass:
                    print(f"   -> Falha ao tentar clicar no botão: {e_bypass}")

            elementos = self.driver.find_elements(By.CSS_SELECTOR, '.a-price-whole')
            if not elementos:
                elementos = self.driver.find_elements(By.CSS_SELECTOR, '.a-offscreen')
            
            if not elementos: 
                elementos = self.driver.find_elements(By.ID, 'price_inside_buybox')

            if not elementos: return None
            
            raw_price = elementos[0].get_attribute("textContent")
            return self._clean_price(raw_price)
            
        except Exception as e:
            print(f"⚠️ Erro Amazon: {e}")
            return None

    def _extract_mercadolivre(self):
        try:
            print("   -> Tentando estratégia JSON-LD (Dados Estruturados)...")
            
            json_scripts = self.driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')
            
            if len(json_scripts) > 0:
                try:
                    json_text = json_scripts[0].get_attribute('innerHTML')
                    data = json.loads(json_text)
                    
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

            meta_price = self.driver.find_elements(By.CSS_SELECTOR, "meta[itemprop='price']")
            if meta_price:
                price = meta_price[0].get_attribute("content")
                print(f"   -> SUCESSO via Meta Tag: {price}")
                return float(price)

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
            numeric_string = re.sub(r'[^\d,]', '', raw_price)
            return float(numeric_string.replace(',', '.'))
        except:
            return None

    def close_browser(self):
        self.driver.quit()