# 📉 PriceStalker V2.0 (SaaS Cloud Native)

> **Plataforma de Monitoramento de Preços Inteligente** totalmente baseada em nuvem, com arquitetura distribuída e notificações via WhatsApp.

![Status](https://img.shields.io/badge/Status-Online-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Neon](https://img.shields.io/badge/Database-Neon_(Serverless_Postgres)-00E599?style=for-the-badge&logo=postgresql&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

---

## 🚀 Live Demo
Acesse a aplicação rodando em produção agora mesmo:
### [🔗 CLIQUE AQUI PARA ACESSAR O PRICESTALKER](https://pricestalker.streamlit.app)

---

## 💡 Sobre o Projeto

O **PriceStalker** evoluiu de um script local para um **SaaS (Software as a Service)** completo. Ele resolve o problema de monitorar preços em grandes e-commerces (Amazon & Mercado Livre) de forma autônoma.

**Diferenciais da Versão 2.0:**
1.  **100% Cloud:** Não depende mais da máquina do usuário ligada.
2.  **Multi-Tenant:** Cada usuário tem sua conta, seus produtos e sua própria chave de API para notificações.
3.  **Autônomo:** Um robô na nuvem verifica os preços de hora em hora e notifica apenas se houver oportunidade real.

---

## 🏗️ Arquitetura de Solução (Cloud Native)

O projeto utiliza uma arquitetura moderna e desacoplada para garantir custo zero e alta disponibilidade:

```mermaid
graph TD
    User["Usuário"] -->|Acessa| Frontend["Streamlit Cloud"]
    Frontend -->|"Lê/Escreve"| DB[("Neon Serverless Postgres")]
    
    GitHub["GitHub Actions"] -->|"Cron Job (1h)"| Scraper["Robô Python"]
    Scraper -->|Consulta| DB
    Scraper -->|Scraping| ECommerce["Amazon / Mercado Livre"]
    Scraper -->|Notifica| WhatsApp["CallMeBot API"]
    WhatsApp -->|Envia| UserPhone["Celular do Usuário"]
```

### 🛠️ Tech Stack

* **Frontend:** Streamlit hospedado no **Streamlit Community Cloud**.
* **Database:** PostgreSQL Serverless hospedado na **Neon.tech** (AWS Region).
* **Backend/Worker:** Python + Selenium rodando em containers Linux via **GitHub Actions** (CI/CD).
* **DevOps:**
    * Deploy automático do Frontend via Git Push na branch `main`.
    * Automação do Scraper via Cron Job (`hourly_check.yml`).

---

## 📸 Screenshots

### Painel de Controle (Dashboard)
![Dashboard](https://github.com/kenjishimizu2411/price_stalker/blob/main/docs/tela_atual.PNG?raw=true)
*Interface responsiva com gestão de produtos, gráficos históricos e modo noturno.*

---

## ⚙️ Funcionalidades Chave

* **Autenticação Segura:** Sistema de Login/Cadastro com hash de senha (`bcrypt`).
* **Scraping Híbrido:**
    * *Amazon:* Tratamento de seletores CSS e Headers anti-bot.
    * *Mercado Livre:* Estratégia prioritária via JSON-LD (Dados estruturados) para precisão máxima.
* **Smart Alerts:** O sistema calcula a economia real ("R$ 50,00 abaixo da meta") e envia links limpos e diretos no WhatsApp.
* **Análise Gráfica:** Gráficos interativos (Plotly) mostram a evolução do preço x meta ao longo do tempo.

---

## 💻 Como Rodar Localmente (Para Desenvolvedores)

Se você deseja clonar e modificar o projeto:

### 1. Clone o Repositório
```bash
git clone [https://github.com/kenjishimizu2411/price_stalker.git](https://github.com/kenjishimizu2411/price_stalker.git)
cd price_stalker
```

### 2. Configure o Ambiente
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto com a conexão do seu banco (Local ou Neon):
```ini
DATABASE_URL="postgres://usuario:senha@host:porta/banco"
```

### 4. Execute
```bash
# Rodar o Dashboard
streamlit run src/dashboard.py

# Rodar o Robô (uma vez)
python src/main.py
```

---

## ⚖️ Aviso Legal

Este projeto é uma demonstração de engenharia de software e automação. 
* O **PriceStalker** não possui vínculo com as lojas monitoradas.
* O uso de Web Scraping deve ser feito de forma ética e responsável.
* As notificações dependem da disponibilidade da API de terceiros (CallMeBot).

---

<p align="center">
Developed by <strong>Kenji Shimizu</strong>
</p>