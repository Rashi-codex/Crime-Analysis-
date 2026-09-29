# 🛡️ Crime Against Women in India (2001–2021) | Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Pandas](https://img.shields.io/badge/Data-Pandas%20%7C%20NumPy-150458?logo=pandas)](https://pandas.pydata.org/)
[![Plotly & Folium](https://img.shields.io/badge/Visuals-Folium%20%7C%20Matplotlib-orange)](https://plotly.com/)

> An end-to-end exploratory data analytics and geospatial intelligence dashboard examining 21 years of reported crimes against women across Indian states and Union Territories.

---

## 📌 Executive Summary

Gender-based violence remains one of the most critical socio-legal challenges in India. This dashboard provides researchers, policy analysts, legal scholars, journalists, and citizens with an interactive platform to analyze historical trends, geographic concentration, and crime type distributions from **2001 to 2021**.

The underlying data is curated from official records published by the **National Crime Records Bureau (NCRB)**, Ministry of Home Affairs, Government of India.

---

## 🚀 Key Features

* **Dynamic Multi-Dimensional Exploration**: Filter across **Year** (2001–2021), **State/UT**, and **Crime Offense** across 8 distinct dynamic view scenarios.
* **Geospatial Choropleth Mapping**: Interactive India state choropleth powered by Leaflet and Folium displaying cumulative offense density with interactive hover tooltips.
* **KPI Metrics & Risk Callouts**: Instant summary cards displaying total reported cases, predominant crime categories, and contextual insights.
* **Time-Series Analysis**: Multi-line and area charts depicting national and state-specific trajectories over two decades.
* **Category Distribution**: Breakdown of specific Indian Penal Code (IPC) and Special & Local Laws (SLL) crime heads.

---

## 📊 Crime Indicators & Legal Glossary

| Metric Code | Full Legal Classification | Indian Penal Code / Act Reference |
| :--- | :--- | :--- |
| **Rape** | Rape | IPC Section 376 |
| **K&A** | Kidnapping & Abduction of Women | IPC Sections 363–373 |
| **DD** | Dowry Deaths | IPC Section 304B |
| **AoW** | Assault on Women with Intent to Outrage Modesty | IPC Section 354 |
| **AoM** | Insult to the Modesty of Women | IPC Section 509 |
| **DV** | Cruelty by Husband or his Relatives (Domestic Violence) | IPC Section 498A |
| **WT** | Women Trafficking / Immoral Traffic | Immoral Traffic (Prevention) Act |

---

## 🏗️ Tech Stack & Architecture

* **Frontend & Web Framework**: [Streamlit](https://streamlit.io/)
* **Data Processing & Analytics**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Geospatial & Visualization**: [Folium](https://python-visualization.github.io/folium/), [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium), [Matplotlib](https://matplotlib.org/)
* **Asset & Image Handling**: [Pillow (PIL)](https://python-pillow.org/)

---

## ☁️ Deployment Guide

### Option 1: Deploy on Streamlit Community Cloud (Recommended ⭐)
1. Fork or push this repository to your **GitHub** account.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
3. Click **"New app"**.
4. Select:
   * **Repository**: `your-username/crime-against-women-analytics`
   * **Branch**: `main`
   * **Main file path**: `app.py`
5. Click **"Deploy!"**. Your dashboard will be live within 2–3 minutes at `https://<your-app-name>.streamlit.app`.

### Option 2: Deploy on Hugging Face Spaces (Top Alternative 🚀)
1. Log in to [Hugging Face](https://huggingface.co/) and click **New Space**.
2. Select **Streamlit** as the Space SDK and choose the **Free (2 vCPU · 16 GB RAM)** hardware tier.
3. Push your repository code to the Hugging Face Git remote repository.
4. Hugging Face automatically detects `requirements.txt` and starts your dashboard.

### Option 3: Deploy on Render
1. Connect your GitHub repository to [Render](https://render.com/).
2. Create a new **Web Service**.
3. Select **Python 3** environment.
4. The repo contains `render.yaml` and `Procfile` configured automatically:
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

### Option 4: Run via Docker
```bash
# Build the Docker image
docker build -t crime-analytics-dashboard .

# Run the container
docker run -p 8501:8501 crime-analytics-dashboard
```
Open `http://localhost:8501` in your browser.

---

## 💻 Local Installation & Setup

### Prerequisites
* Python 3.9, 3.10, or 3.11 installed.
* Git installed.

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/crime-against-women-analytics.git
cd crime-against-women-analytics
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch the Dashboard
```bash
streamlit run app.py
```

---

## 📁 Project Directory Structure

```text
├── .streamlit/
│   └── config.toml                 # Streamlit UI theme and server settings
├── CrimesOnWomenData.csv           # Raw NCRB historical records (2001–2021)
├── india_states.geojson            # India state GeoJSON boundaries
├── crime.jpg                       # Dashboard banner artwork
├── app.py                          # Streamlit web application
├── requirements.txt                # Pinned production dependencies
├── Procfile                        # Process file for Render / Heroku
├── render.yaml                     # Service specification for Render
├── Dockerfile                      # Containerization instructions
├── .dockerignore                   # Docker build exclusions
├── .gitignore                      # Git ignored files and cache
└── README.md                       # Comprehensive documentation
```

---

## 🔍 Key Analytical Insights

1. **Predominance of Domestic Violence (IPC 498A)**: Cruelty by Husband or his Relatives represents the single highest volume of reported cases across all tracked years.
2. **Post-2012 Reporting Surge**: Following legal reforms and the 2013 Criminal Law Amendment, reported incidents of assault (IPC 354) and kidnapping exhibited a sharp upward trend, reflecting enhanced reporting mechanisms and institutional mandates.
3. **Geographic Distribution**: Populous states including Uttar Pradesh, West Bengal, Rajasthan, and Maharashtra record the largest total reported cases in absolute terms.

---

## 🤝 Contributing & License

Contributions, feedback, and issue reports are welcome.  
This project is open-source under the [MIT License](LICENSE).
