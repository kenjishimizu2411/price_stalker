# 📉 Price Stalker: Monitoramento Inteligente de Preços

> Aplicação Full Stack para rastreamento de preços em e-commerces (Amazon & Mercado Livre) com notificações automáticas via WhatsApp.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Selenium](https://img.shields.io/badge/Scraping-Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![WhatsApp](https://img.shields.io/badge/Notify-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)

---

## 📸 Dashboard
![Price Stalker Dashboard](https://github.com/kenjishimizu2411/price_stalker/blob/main/docs/dashboard_preview.png?raw=true)
*(Nota: Substitua o link acima pelo caminho real da sua imagem)*

---

## 💡 O Projeto (MVP)

O **Price Stalker** resolve a dor de quem precisa monitorar produtos voláteis na internet. Diferente de extensões de navegador simples, ele funciona como um sistema centralizado que:

1.  **Gerencia Usuários:** Permite cadastro e login seguro.
2.  **Monitora 24/7:** Utiliza *bots* (Selenium) para varrer sites de e-commerce periodicamente.
3.  **Analisa Oportunidades:** Compara o preço atual com a "Meta" definida pelo usuário.
4.  **Notifica:** Envia alerta no WhatsApp quando o preço atinge a meta ou chega a uma margem de oportunidade (15%).

---

## 🏗️ Arquitetura e Tecnologias

O sistema foi construído seguindo padrões de arquitetura modular:

* **Frontend (UI):** Desenvolvido em **Streamlit**, oferecendo um dashboard interativo e responsivo para gestão dos monitoramentos.
* **Backend (Core):** Python puro gerenciando a lógica de negócios.
* **Web Scraping:** **Selenium Webdriver** configurado para navegação em marketplaces complexos (Amazon e Mercado Livre), simulando comportamento humano para evitar bloqueios.
* **Banco de Dados:** **PostgreSQL**. Modelagem relacional robusta com tabelas para `Users`, `Products` e `Price_History` (Histórico de variação de preços).
* **Notificações:** Integração com API **CallMeBot** para envio de mensagens via WhatsApp.

---

## 📂 Estrutura do Banco de Dados

O projeto utiliza um banco relacional para garantir integridade dos dados:

* `users`: Credenciais e dados de contato (telefone para WhatsApp).
* `products`: Links, metas de preço e status do monitoramento.
* `price_history`: Log temporal de todas as flutuações de preço para análise futura.

---

## 🚀 Como Rodar Localmente

### 1. Pré-requisitos
* Python 3.10+
* PostgreSQL instalado e rodando.
* Google Chrome (para o Selenium).

### 2. Instalação
```bash
# Clone o repositório
git clone [https://github.com/kenjishimizu2411/price_stalker.git](https://github.com/kenjishimizu2411/price_stalker.git)
cd price_stalker

# Crie o ambiente virtual
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração (.env)
Crie um arquivo `.env` na raiz e configure suas credenciais:

```ini
# Banco de Dados PostgreSQL
DB_HOST=localhost
DB_NAME=price_stalker
DB_USER=postgres
DB_PASS=sua_senha_aqui

# API CallMeBot (WhatsApp)
WHATSAPP_API_KEY=sua_chave_aqui
```

### 4. Execução

**Para iniciar a Interface (Dashboard):**
```bash
streamlit run src/dashboard.py
```

**Para iniciar o Robô de Monitoramento:**
```bash
python src/main.py
```

---

## ⚠️ Aviso Legal
Este projeto é para fins educacionais e de portfólio. O uso de Web Scraping deve respeitar os termos de serviço (`robots.txt`) dos sites alvo.

---

<p align="center">
<strong>Price Stalker</strong> — Desenvolvido por Kenji Shimizu
</p>