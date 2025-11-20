import sys
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# --- CONFIGURAÇÃO DE CAMINHOS BLINDADA ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
dotenv_path = os.path.join(current_dir, '..', '.env')
load_dotenv(dotenv_path)
# -----------------------------------------

from src.database import get_db_connection, get_due_products, update_last_checked
from src.scraper import Scraper
from src.whatsapp import send_whatsapp_message

MY_API_KEY = os.getenv("WHATSAPP_API_KEY")

if not MY_API_KEY:
    print("❌ ERRO: Não encontrei a WHATSAPP_API_KEY no .env")
    sys.exit(1)


def clean_url_for_whatsapp(url):
    """Limpa a URL para não quebrar o CallMeBot"""
    if "?" in url:
        url = url.split("?")[0]
    if "#" in url:
        url = url.split("#")[0]

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
        prod_id, prod_name, url, target, user_phone, user_name = task

        target_float = float(target)
        phone_clean = user_phone.replace("+", "").replace(" ", "").replace("-", "").strip()

        print(f"   👉 {prod_name}...", end='')

        try:
            current_price = bot.get_price(url)

            if current_price:
                cursor.execute(
                    "INSERT INTO price_history (product_id, price) VALUES (%s, %s)",
                    (prod_id, current_price)
                )
                conn.commit()
                update_last_checked(prod_id)

                print(f" R$ {current_price}", end='')

                # -------- PREÇO ABAIXO DO ALVO --------
                if current_price <= target_float:
                    print(" 🚨 PREÇO BAIXO! ENVIANDO...")

                    short_url = clean_url_for_whatsapp(url)
                    economia = target_float - current_price

                    msg = (
                        f"🔥 *BAIXOU! OPORTUNIDADE DETECTADA* 🔥\n\n"
                        f"📦 *{prod_name}*\n\n"
                        f"😱 Achei o seu produto por *R$ {current_price:.2f}*!!!\n"
                        f"🎯 Você queria que ele chegasse a *R$ {target_float:.2f}*...\n\n"
                        f"📉 Ou seja: *R$ {economia:.2f} DE DESCONTO* se comprar agora!!\n\n"
                        f"👉 *Garanta aqui:* {short_url}"
                    )

                    success = send_whatsapp_message(phone_clean, msg, MY_API_KEY)
                    if not success:
                        print("      ❌ Falha no envio do Zap (Verifique chave/fone)")

                # -------- PREÇO PERTO DO ALVO (15%) --------
                elif current_price <= (target_float * 1.15):
                    print(" 🤏 TÁ QUASE! ENVIANDO ALERTA SECRETO...")

                    short_url = clean_url_for_whatsapp(url)
                    diferenca = current_price - target_float

                    msg = (
                        f"👀 *PSIU! TÁ QUASE LÁ...* 👀\n\n"
                        f"📦 *{prod_name}*\n"
                        f"O preço caiu para *R$ {current_price:.2f}*.\n"
                        f"Ainda está R$ {diferenca:.2f} acima da sua meta, mas achei que você gostaria de saber!\n\n"
                        f"🔗 Espiar: {short_url}"
                    )

                    success = send_whatsapp_message(phone_clean, msg, MY_API_KEY)
                    if not success:
                        print("      ❌ Falha no envio do Zap (Verifique chave/fone)")

                else:
                    print(" 📉 (Caro)")

            else:
                print(" ❌ Erro leitura")
                update_last_checked(prod_id)

        except Exception as e:
            print(f"\n      ⚠️ Erro: {e}")
            conn.rollback()
            update_last_checked(prod_id)

    conn.close()

    try:
        bot.close_browser()
    except:
        pass


def start_saas_loop():
    try:
        while True:
            job_saas()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Parando.")


if __name__ == "__main__":
    start_saas_loop()
