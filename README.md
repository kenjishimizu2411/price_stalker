# 🕵️ PriceStalker - Monitorador de Preços Inteligente (SaaS)

O **PriceStalker** é uma aplicação Full-Stack projetada para monitorar preços de produtos em grandes e-commerces (Amazon, Mercado Livre) e notificar o usuário via WhatsApp apenas quando o preço atingir uma meta pré-estabelecida.

Diferente de comparadores comuns, o PriceStalker funciona com **Inteligência de Dados**, gerando gráficos de histórico e calculando a economia real.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 🚀 Funcionalidades

* **Multi-Tenant SaaS:** Sistema de Login e Cadastro de usuários seguros (Hash de senha).
* **Scraping Híbrido:** Suporte para Amazon e Mercado Livre (bypassing anti-bots).
* **Agente Autônomo:** Script em background que checa preços 24/7.
* **Dashboard Interativo:** Interface visual para gestão de produtos e análise de gráficos.
* **Notificações Smart:** Envia alertas no WhatsApp com cálculo de desconto ("Você economizou R$ 50,00!").

## 🛠️ Tecnologias Utilizadas

* **Backend/Core:** Python 3.11
* **Frontend:** Streamlit (Interface Web)
* **Banco de Dados:** PostgreSQL (Driver psycopg2)
* **Automação Web:** Selenium WebDriver & Beautiful Soup
* **Análise de Dados:** Pandas & Plotly (Gráficos Interativos)
* **Notificações:** API CallMeBot (Gateway WhatsApp)

## ⚙️ Como Rodar Localmente

1.  **Clone o repositório**
    ```bash
    git clone [https://github.com/kenjishimizu2411/price_stalker.git](https://github.com/kenjishimizu2411/price_stalker.git)
    cd price_stalker
    ```

2.  **Configure o Ambiente Virtual**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente (.env)**
    Crie um arquivo `.env` na raiz e adicione:
    ```ini
    DB_NAME=pricestalker
    DB_USER=postgres
    DB_PASS=sua_senha
    DB_HOST=localhost
    DB_PORT=5432
    WHATSAPP_API_KEY=sua_chave_callmebot
    ```

5.  **Execute a Aplicação**
    * **Terminal 1 (Interface):** `streamlit run src/dashboard.py`
    * **Terminal 2 (Robô):** `python src/main.py`

## 👨‍💻 Desenvolvedor

Desenvolvido por **Kenji Shimizu** como projeto de Engenharia de Software Full-Stack.