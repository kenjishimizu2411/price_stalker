import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(message):
    """
    Envia uma mensagem de texto para o seu Telegram.
    """
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️ Erro: Token ou Chat ID do Telegram não configurados no .env")
        return

    # URL Mágica da API do Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown" # Permite usar negrito, itálico, etc.
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Notificação enviada para o Telegram!")
        else:
            print(f"❌ Erro ao enviar Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão com Telegram: {e}")

# Teste rápido (só roda se executar esse arquivo)
if __name__ == "__main__":
    send_telegram_message("🚀 Teste do PriceStalker: Olá, Mestre Kenji!")