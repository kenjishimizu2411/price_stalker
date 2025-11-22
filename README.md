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
    User[Usuário] -->|Acessa| Frontend[Streamlit Cloud]
    Frontend -->|Lê/Escreve| DB[(Neon Serverless Postgres)]
    
    GitHub[GitHub Actions] -->|Cron Job (1h)| Scraper[Robô Python]
    Scraper -->|Consulta| DB
    Scraper -->|Scraping| ECommerce[Amazon / Mercado Livre]
    Scraper -->|Notifica| WhatsApp[CallMeBot API]
    WhatsApp -->|Envia| UserPhone[Celular do Usuário]