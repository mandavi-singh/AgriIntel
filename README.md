# 🌾 AgriIntel — Global Agriculture Intelligence Platform

A full-stack AI-powered agriculture web application built with Streamlit. It combines machine learning, real-time social signals, live weather data, and generative AI to help farmers, researchers, and agricultural enthusiasts make better decisions.

---

## 🚀 Features

| Tab | Feature | Description |
|-----|---------|-------------|
| 🗺️ World Map | Interactive Map | Click any country marker to explore crops, seasons, and regions |
| 📊 Intelligence | Country Dashboard | Live weather, Reddit signals, news sentiment, and risk score |
| 🌤️ Forecast | 7-Day Weather | Temperature trends, precipitation chart, and farming tips |
| 🌾 Yield Predict | ML Prediction | Predict crop yield from farm inputs + historical yield trends |
| 📸 Disease AI | Disease Detection | Upload crop photo → Gemini AI diagnoses the disease instantly |
| 📅 Crop Calendar | Farming Schedule | Sowing, fertilizing, irrigation, and harvesting dates by crop & season |
| 💰 Mandi Prices | Price Tracker | 30-day Indian mandi price trends for 14 major crops |
| 🗺️ India Map | State-wise Map | India state-level crop data, yield, soil type, and agriculture facts |
| 🤖 AgriBot | AI Chatbot | Gemini-powered agriculture assistant — ask anything |

---

## 🛠️ Setup Instructions

### Step 1 — Extract and navigate to the folder
```bash
cd agri_app
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Add API keys

Create the secrets file at `.streamlit/secrets.toml`:

```
agri_app/
└── .streamlit/
    └── secrets.toml   ← create this file
```

Add your keys in this format:
```toml
GEMINI_API_KEY = "your_gemini_key_here"
REDDIT_CLIENT_ID = "your_reddit_client_id"
REDDIT_CLIENT_SECRET = "your_reddit_client_secret"
NEWS_API_KEY = "your_newsapi_key"
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

---

## 🔑 How to Get API Keys

| API | Link | Cost |
|-----|------|------|
| **Gemini API** | https://aistudio.google.com/app/apikey | ✅ Free |
| **Reddit API** | https://www.reddit.com/prefs/apps → Create App → Script | ✅ Free |
| **NewsAPI** | https://newsapi.org/register | ✅ Free (100 req/day) |
| **Weather** | Open-Meteo — no key needed | ✅ Free |

> ⚠️ The app works without Reddit and NewsAPI keys — only those sections will show a message. Weather and Gemini features require their respective keys.

---

## 📁 Project Structure

```
agri_app/
├── app.py              ← Main Streamlit application (all 9 tabs)
├── utils.py            ← Weather, Reddit, News, Disease detection, Price, Chatbot
├── ml_model.py         ← Crop yield prediction ML model (Random Forest)
├── country_data.py     ← Agriculture data for 12 countries
├── crop_calendar.py    ← Crop calendar data (sowing, harvesting, etc.)
├── india_states.py     ← India state-wise crop and yield data (15 states)
├── yield_history.py    ← Historical yield data 2015–2024 (FAO-based)
├── requirements.txt    ← Python dependencies
└── .streamlit/
    └── secrets.toml    ← API keys (you create this)
```

---

## 🌱 Supported Countries

India, USA, China, Brazil, Australia, Russia, France, Argentina, Nigeria, Indonesia, Canada, Ukraine

---

## 🌾 Supported Crops

**Yield Prediction:** Rice, Wheat, Maize, Cotton, Sugarcane, Barley, Soybean, Tomato, Potato, Carrot

**Mandi Prices:** Wheat, Rice, Maize, Cotton, Sugarcane, Soybean, Barley, Potato, Tomato, Carrot, Onion, Mustard, Groundnut, Chickpea

**Crop Calendar:** Rice, Wheat, Cotton, Maize, Sugarcane, Soybean, Barley, Potato, Tomato, Carrot (India) + Corn, Soybeans, Wheat, Canola (USA, Brazil, Australia, China)

---

## 🤖 AI Features

- **Crop Disease Detection** — Upload any crop leaf photo and Gemini Vision AI will identify the disease, severity, cause, treatment, and prevention steps
- **AgriBot Chatbot** — Ask agriculture-related questions in natural language. The bot only answers agriculture topics and uses country context automatically

---

## 📊 Data Sources

| Data | Source |
|------|--------|
| Weather (current + forecast) | Open-Meteo API (free, no key) |
| Social signals | Reddit via PRAW |
| News articles | NewsAPI |
| Historical yield data | FAO-based approximate values (2015–2024) |
| Mandi prices | Simulated based on realistic MSP ranges |
| ML model | Trained on synthetic farm data (Random Forest) |

---

## ⚠️ Important Notes

- **Never put API keys directly in code** — always use `.streamlit/secrets.toml`
- The `.streamlit/secrets.toml` file should never be uploaded to GitHub
- The ML model (`model.pkl`) is auto-generated on first run — this may take a few seconds
- Mandi prices are simulated for demonstration — for real prices, integrate Agmarknet API

---

## 👩‍💻 Built By

**Mandavi Singh**
BSc (Hons.) Data Science & Artificial Intelligence
Indian Institute of Technology (IIT) Guwahati — 2023–2027
Roll No: 23035010823
Email: s.mandavi@op.iitg.ac.in
GitHub: github.com/mandavi-singh
