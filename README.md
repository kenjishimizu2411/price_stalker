# 📉 PriceStalker V2.0 (SaaS Cloud Native)

> **Intelligent Price Monitoring Platform** | 100% Cloud-based, Distributed Architecture & WhatsApp Notifications.

![Status](https://img.shields.io/badge/Status-Online-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Neon](https://img.shields.io/badge/Database-Neon_(Serverless_Postgres)-00E599?style=for-the-badge&logo=postgresql&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/Automation-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

---

## 🚀 Live Demo
Access the production application right now:
### [🔗 CLICK HERE TO ACCESS PRICESTALKER](https://pricestalker.streamlit.app)

---

## 💡 About the Project

**PriceStalker** has evolved from a simple local script into a full **SaaS (Software as a Service)** solution. It solves the problem of monitoring prices on major e-commerce platforms (Amazon & Mercado Livre) autonomously.

**V2.0 Key Differentiators:**
1. **100% Cloud Native:** No dependency on local machines being turned on.
2. **Multi-Tenant:** Each user has their own account, product list, and private API key for notifications.
3. **Autonomous Worker:** A cloud robot checks prices hourly and triggers notifications only when a real opportunity is detected.

---

## 🏗️ Solution Architecture (Zero-Cost & Serverless)

The project employs a modern, decoupled architecture to ensure high availability with zero infrastructure cost:

```mermaid
graph TD
    User["User"] -->|Access| Frontend["Streamlit Cloud"]
    Frontend -->|"Read/Write"| DB[("Neon Serverless Postgres")]
    GitHub["GitHub Actions"] -->|"Cron Job (1h)"| Scraper["Python Worker"]
    Scraper -->|Query| DB
    Scraper -->|Scraping| ECommerce["Amazon / Mercado Livre"]
    Scraper -->|Notify| WhatsApp["CallMeBot API"]
    WhatsApp -->|Send Message| UserPhone["User's Mobile"]
```

### 🛠️ Tech Stack

* **Frontend:** Streamlit hosted on **Streamlit Community Cloud**.
* **Database:** PostgreSQL Serverless hosted on **Neon.tech** (AWS Region).
* **Backend/Worker:** Python + Selenium running on Linux containers via **GitHub Actions** (CI/CD).
* **DevOps:**
    * Automatic Frontend Deploy via Git Push to `main`.
    * Scraper Automation via Cron Job (`hourly_check.yml`).

---

## 📸 Screenshots

### Control Panel (Dashboard)
![Dashboard](https://github.com/kenjishimizu2411/price_stalker/blob/main/docs/tela_atual.PNG?raw=true)
*Responsive interface with product management, historical charts, and dark mode.*

---

## ⚙️ Key Features

* **Secure Authentication:** Login/Registration system with password hashing (`bcrypt`).
* **Hybrid Scraping Engine:**
    * *Amazon:* Handling of CSS selectors and Anti-bot Headers.
    * *Mercado Livre:* Priority strategy using JSON-LD (Structured Data) for maximum precision.
* **Smart Alerts:** The system calculates real savings ("$50.00 below target") and sends clean, direct links via WhatsApp.
* **Data Visualization:** Interactive charts (Plotly) tracking Price vs. Target over time.

---

## 💻 Local Development Setup

If you wish to clone and modify the project:

### 1. Clone the Repository
'''bash
git clone [https://github.com/kenjishimizu2411/price_stalker.git](https://github.com/kenjishimizu2411/price_stalker.git)
cd price_stalker
'''

### 2. Configure Environment
'''bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
'''

### 3. Environment Variables (.env)
Create a `.env` file in the root directory with your database connection string (Local or Neon):
'''ini
DATABASE_URL="postgres://user:password@host:port/database"
'''

### 4. Run Application
'''bash
# Run the Dashboard
streamlit run src/dashboard.py

# Run the Scraper (once)
python src/main.py
'''

---

## ⚖️ Legal Disclaimer

This project is a demonstration of software engineering and automation skills.
* **PriceStalker** has no affiliation with the monitored stores.
* Web Scraping must be performed ethically and responsibly.
* Notifications depend on third-party API availability (CallMeBot).

---

<p align="center">
Developed by <strong>Kenji Shimizu</strong>
</p>
