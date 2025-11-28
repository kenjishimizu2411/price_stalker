import requests
import urllib.parse

def send_whatsapp_message(phone_number, message, api_key):
    
    try:
        encoded_msg = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={encoded_msg}&apikey={api_key}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ WhatsApp enviado para {phone_number}!")
            return True
        else:
            print(f"❌ Erro CallMeBot: {response.text}")
            return False
            
    except Exception as e:
        print(f"⚠️ Erro de conexão Zap: {e}")
        return False