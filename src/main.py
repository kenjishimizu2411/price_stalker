import sys
import os
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
dotenv_path = os.path.join(current_dir, '..', '.env')
load_dotenv(dotenv_path)

from src.database import get_db_connection, get_due_products, update_last_checked, update_last_notified
from src.scraper import Scraper
from src.whatsapp import send_whatsapp_message

def clean_url_for_whatsapp(url):
    """Limpa a URL para não quebrar o CallMeBot"""
    if "?" in url: url = url.split("?")[0]
    if "#" in url: url = url.split("#")[0]

    if "amazon" in url and "/dp/" in url:
        try:
            base_part = url.split("/dp/")[1]
            asin = base_part.split("/")[0]
            return f"https://www.amazon.com.br/dp/{asin}"
        except:
            return url
    return url

def job_saas():
    print(f"\n🔄 [SaaS] PriceStalker: {datetime.now().strftime('%H:%M:%S')}")
    tasks = get_due_products()
    
    if not tasks:
        print("💤 Nada pendente.")
        return

    print(f"🔥 Processando {len(tasks)} produtos...")
    bot = Scraper()
    conn = get_db_connection()
    cursor = conn.cursor()

    for task in tasks:
        prod_id, prod_name, url, target, user_phone, user_name, user_apikey, notify_daily, last_notified = task
        
        target_float = float(target)
        phone_clean = user_phone.replace("+", "").replace(" ", "").replace("-", "").strip() if user_phone else ""

        print(f"   👉 {prod_name} ({user_name})...", end='')
        
        try:
            current_price = bot.get_price(url)
            
            if current_price:
                cursor.execute("INSERT INTO price_history (product_id, price) VALUES (%s, %s)", (prod_id, current_price))
                conn.commit()
                update_last_checked(prod_id)
                
                print(f" R$ {current_price}", end='')
                
                should_notify = True
                if notify_daily and last_notified:
                    if last_notified.date() == datetime.now(timezone.utc).date():
                        print(" 🔕 (Spam Block)", end='')   
                        should_notify = False

                
                if current_price <= target_float:
                    if should_notify:
                        if user_apikey:
                            print(" 🚨 BAIXOU!", end='')
                            short_url = clean_url_for_whatsapp(url)
                            economia = target_float - current_price
                            msg = (
                                f"🔥 *BAIXOU! OPORTUNIDADE* 🔥\n\n"
                                f"📦 *{prod_name}*\n"
                                f"😱 Achei o seu produto por *R$ {current_price:.2f}*!!!\n"
                                f"🎯 Você queria que ele chegasse a *R$ {target_float:.2f}*\n\n"
                                f"📉 Ou seja: *R$ {economia:.2f} DE DESCONTO* se comprar *AGORA*!!\n\n" 
                                f"👉 *Garanta aqui:* {short_url}"
                            )
                            if send_whatsapp_message(phone_clean, msg, user_apikey):
                                update_last_notified(prod_id)
                            else:
                                print(" ❌ Falha Zap", end='')
                        else:
                            print(" ⚠️ Sem Key", end='')
                
                elif current_price <= (target_float * 1.10):
                    if should_notify:
                        if user_apikey:
                            print(" 🤏 QUASE!", end='')
                            short_url = clean_url_for_whatsapp(url)
                            diferenca = current_price - target_float
                            msg = (
                                f"👀 *PSIU! TÁ QUASE LÁ...* 👀\n\n"
                                f"📦 *{prod_name}*\n"
                                f"O preço caiu para *R$ {current_price:.2f}*.\n"
                                f"Ainda está *R$ {diferenca:.2f}* acima da sua meta, mas, achei que você gostaria de saber!\n"
                                f"🔗 Espiar: {short_url}"
                            )
                            if send_whatsapp_message(phone_clean, msg, user_apikey):
                                update_last_notified(prod_id)
                            else:
                                print(" ❌ Falha Zap", end='')
                        else:
                            print(" ⚠️ Sem Key", end='')
                
                else:
                    print(" 📉 (Caro)", end='')

            else:
                print(" ❌ Erro leitura", end='')
                update_last_checked(prod_id)
        
        except Exception as e:
            print(f"\n      ⚠️ Erro tarefa: {e}")
            conn.rollback()
            update_last_checked(prod_id)
            
        print("")

    conn.close()
    try: bot.close_browser()
    except: pass

def run_once():
    """Roda uma única vez (Para Cloud/Cron Jobs)"""
    print(f"🚀 [Cloud Run] Iniciando verificação única: {datetime.now()}")
    job_saas()
    print("🏁 [Cloud Run] Finalizado com sucesso.")

def start_saas_loop():
    """Roda em loop (Para PC Local)"""
    print(f"🚀 [Local Mode] Rodando em Loop...")
    try:
        while True:
            job_saas()
            print("💤 Dormindo 60s...")
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Parando.")

if __name__ == "__main__":
    # Para o GitHub Actions, usamos run_once()
    # Se quiser testar looping no PC, troque para start_saas_loop()
    run_once()