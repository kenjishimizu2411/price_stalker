# 📉 PriceStalker V2.0 (SaaS Cloud Native)

> **Plataforma Inteligente de Monitoramento de Preços** | 100% em Nuvem, Arquitetura Distribuída & Notificações via WhatsApp.

![Status](https://img.shields.io/badge/Status-Online-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Neon](https://img.shields.io/badge/Database-Neon_(Serverless_Postgres)-00E599?style=for-the-badge&logo=postgresql&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

---

## 🚀 Live Demo
Acesse a aplicação em produção agora mesmo:
### [🔗 CLIQUE AQUI PARA ACESSAR O PRICESTALKER](https://pricestalker.streamlit.app)

---

## 💡 Sobre o Projeto

O **PriceStalker** evoluiu de um script local simples para uma solução completa **SaaS (Software as a Service)**. Ele resolve o problema de monitorar preços em grandes e-commerces (Amazon & Mercado Livre) de forma autônoma.

**Diferenciais da Versão 2.0:**
1. **100% Cloud Native:** Sem dependência de manter a máquina local ligada.
2. **Multi-Tenant:** Cada usuário tem sua própria conta, lista de produtos e chave de API privada para notificações.
3. **Worker Autônomo:** Um robô na nuvem verifica os preços de hora em hora e dispara notificações apenas quando uma oportunidade real é detectada.

---

## 🏗️ Arquitetura da Solução (Custo Zero & Serverless)

O projeto emprega uma arquitetura moderna e desacoplada para garantir alta disponibilidade com custo zero de infraestrutura:

```mermaid
graph TD
    User["Usuário"] -->|Acessa| Frontend["Streamlit Cloud"]
    Frontend -->|"Leitura/Escrita"| DB[("Neon Serverless Postgres")]
     
    GitHub["GitHub Actions"] -->|"Cron Job (1h)"| Scraper["Worker Python"]
    Scraper -->|Consulta| DB
    Scraper -->|Scraping| ECommerce["Amazon / Mercado Livre"]
    Scraper -->|Notifica| WhatsApp["CallMeBot API"]
    WhatsApp -->|Envia Msg| UserPhone["Celular do Usuário"]
```

---

### 🛠️ Tech Stack

* **Frontend:** Streamlit hospedado no **Streamlit Community Cloud**.
* **Database:** PostgreSQL Serverless hospedado na **Neon.tech** (AWS Region).
* **Backend/Worker:** Python + Selenium rodando em containers Linux via **GitHub Actions** (CI/CD).
* **DevOps:**
    * Deploy Automático do Frontend via Git Push na branch `main`.
    * Automação do Scraper via Cron Job (`hourly_check.yml`).

---

## 📸 Screenshots

### Painel de Controle (Dashboard)
![Dashboard](https://github.com/kenjishimizu2411/price_stalker/blob/main/docs/tela_atual.PNG?raw=true)
*Interface responsiva com gestão de produtos, gráficos históricos e modo noturno.*

---

## ⚙️ Funcionalidades Chave

* **Autenticação Segura:** Sistema de Login/Cadastro com hash de senha (`bcrypt`).
* **Motor de Scraping Híbrido:**
    * *Amazon:* Tratamento de seletores CSS e Headers Anti-bot.
    * *Mercado Livre:* Estratégia prioritária usando JSON-LD (Dados Estruturados) para precisão máxima.
* **Alertas Inteligentes:** O sistema calcula a economia real ("R$ 50,00 abaixo da meta") e envia links diretos e limpos via WhatsApp.
* **Visualização de Dados:** Gráficos interativos (Plotly) monitorando Preço vs. Meta ao longo do tempo.

---

## 💻 Configuração de Desenvolvimento Local

Se você deseja clonar e modificar o projeto:

### 1. Clone o Repositório
'''bash
git clone [https://github.com/kenjishimizu2411/price_stalker.git](https://github.com/kenjishimizu2411/price_stalker.git)
cd price_stalker
'''

### 2. Configure o Ambiente
'''bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
'''

### 3. Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz do diretório com a string de conexão do seu banco (Local ou Neon):
'''ini
DATABASE_URL="postgres://usuario:senha@host:porta/banco"
'''

### 4. Executar Aplicação
'''bash
# Rodar o Dashboard
streamlit run src/dashboard.py

# Rodar o Scraper (uma vez)
python src/main.py
'''

---

## ⚖️ Aviso Legal

Este projeto é uma demonstração de engenharia de software e habilidades de automação.
* O **PriceStalker** não possui afiliação com as lojas monitoradas.
* O Web Scraping deve ser realizado de forma ética e responsável.
* As notificações dependem da disponibilidade de APIs de terceiros (CallMeBot).

---

<p align="center">
Desenvolvido por <strong>Kenji Shimizu</strong>
</p>
