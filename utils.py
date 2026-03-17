import os
import requests
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ─── Load secrets ─────────────────────────────────────────────
def get_secret(key):
    try:
        import streamlit as st
        return st.secrets.get(key, "")
    except Exception:
        return os.getenv(key, "")

analyzer = SentimentIntensityAnalyzer()

AGRI_KEYWORDS = [
    "crop", "harvest", "yield", "farm", "soil", "irrigation",
    "fertilizer", "pesticide", "drought", "flood", "sowing",
    "cultivation", "agriculture", "planting", "wheat", "rice",
    "maize", "cotton", "sugarcane", "kharif", "rabi", "pest",
    "crop disease", "organic farming", "seed", "tractor",
    "greenhouse", "livestock", "cattle", "poultry", "compost",
    "herbicide", "fungicide", "barley", "soybean", "millet",
    "groundwater", "crop rotation", "agri", "farmer"
]

AGRI_SUBREDDITS = [
    "agriculture", "farming", "IndianAgriculture", "crops",
    "homesteading", "permaculture", "organicfarming", "soil",
    "vegetablegardening", "AgriculturePro"
]

WEATHER_DESC = {
    0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅",
    3: "Overcast ☁️", 45: "Foggy 🌫️", 48: "Icy fog 🌫️",
    51: "Light drizzle 🌦️", 61: "Slight rain 🌧️", 63: "Moderate rain 🌧️",
    65: "Heavy rain 🌧️", 71: "Slight snow 🌨️", 80: "Rain showers 🌦️",
    95: "Thunderstorm ⛈️", 99: "Heavy thunderstorm ⛈️"
}


# ─── CURRENT WEATHER ─────────────────────────────────────────
def get_weather(lat, lon):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,windspeed_10m,weathercode"
            f"&timezone=auto"
        )
        r = requests.get(url, timeout=8)
        data = r.json()
        current = data.get("current", {})
        code = current.get("weathercode", 0)
        return {
            "temperature":  current.get("temperature_2m", "N/A"),
            "humidity":     current.get("relative_humidity_2m", "N/A"),
            "precipitation":current.get("precipitation", 0),
            "windspeed":    current.get("windspeed_10m", "N/A"),
            "description":  WEATHER_DESC.get(code, "Unknown"),
        }
    except Exception as e:
        return {"error": str(e)}


# ─── 7-DAY FORECAST ──────────────────────────────────────────
def get_forecast(lat, lon):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"weathercode,windspeed_10m_max"
            f"&timezone=auto&forecast_days=7"
        )
        r = requests.get(url, timeout=8)
        data  = r.json()
        daily = data.get("daily", {})
        dates    = daily.get("time", [])
        temp_max = daily.get("temperature_2m_max", [])
        temp_min = daily.get("temperature_2m_min", [])
        precip   = daily.get("precipitation_sum", [])
        codes    = daily.get("weathercode", [])
        wind     = daily.get("windspeed_10m_max", [])
        forecast = []
        for i in range(len(dates)):
            code = codes[i] if i < len(codes) else 0
            forecast.append({
                "date":     dates[i],
                "temp_max": temp_max[i] if i < len(temp_max) else "N/A",
                "temp_min": temp_min[i] if i < len(temp_min) else "N/A",
                "precip":   precip[i]   if i < len(precip)   else 0,
                "wind":     wind[i]     if i < len(wind)      else "N/A",
                "desc":     WEATHER_DESC.get(code, "Unknown"),
                "code":     code,
            })
        return forecast
    except Exception:
        return []


# ─── REDDIT ──────────────────────────────────────────────────
def get_reddit_posts(country_subs, keywords, limit=12):
    try:
        reddit = praw.Reddit(
            client_id=get_secret("REDDIT_CLIENT_ID"),
            client_secret=get_secret("REDDIT_CLIENT_SECRET"),
            user_agent="AgriApp/1.0",
        )
        all_subs = list(set(AGRI_SUBREDDITS + country_subs))
        query    = "crop OR farm OR harvest OR yield OR soil OR irrigation OR fertilizer OR drought OR pest OR cultivation"
        posts    = []
        for sub in all_subs[:7]:
            try:
                subreddit = reddit.subreddit(sub)
                for post in subreddit.search(query, limit=limit, sort="new", time_filter="month"):
                    title_lower = (post.title + " " + (post.selftext[:300] or "")).lower()
                    if not any(kw in title_lower for kw in AGRI_KEYWORDS):
                        continue
                    sentiment = analyzer.polarity_scores(post.title + " " + (post.selftext[:200] or ""))
                    label = "Positive 🟢" if sentiment["compound"] >= 0.05 else \
                            "Negative 🔴" if sentiment["compound"] <= -0.05 else "Neutral 🟡"
                    posts.append({
                        "title":     post.title,
                        "score":     post.score,
                        "url":       f"https://reddit.com{post.permalink}",
                        "sentiment": label,
                        "compound":  sentiment["compound"],
                        "subreddit": sub,
                        "created":   post.created_utc,
                    })
            except Exception:
                continue
        return sorted(posts, key=lambda x: x["created"], reverse=True)[:15]
    except Exception:
        return []


# ─── NEWS ────────────────────────────────────────────────────
def get_news(query, api_key=None):
    key = api_key or get_secret("NEWS_API_KEY")
    if not key or key == "your_newsapi_key_here":
        return []
    try:
        agri_query = f"({query}) AND (agriculture OR farming OR crop OR harvest OR yield)"
        url = (
            f"https://newsapi.org/v2/everything"
            f"?q={requests.utils.quote(agri_query)}"
            f"&language=en&sortBy=publishedAt&pageSize=10"
            f"&apiKey={key}"
        )
        r        = requests.get(url, timeout=8)
        articles = r.json().get("articles", [])
        result   = []
        for a in articles:
            text = (a.get("title") or "") + " " + (a.get("description") or "")
            if not any(kw in text.lower() for kw in AGRI_KEYWORDS):
                continue
            sentiment = analyzer.polarity_scores(text)
            label = "Positive 🟢" if sentiment["compound"] >= 0.05 else \
                    "Negative 🔴" if sentiment["compound"] <= -0.05 else "Neutral 🟡"
            result.append({
                "title":       a.get("title", ""),
                "description": a.get("description", ""),
                "url":         a.get("url", ""),
                "source":      a.get("source", {}).get("name", ""),
                "sentiment":   label,
                "compound":    sentiment["compound"],
                "publishedAt": a.get("publishedAt", ""),
            })
        return result
    except Exception:
        return []


# ─── RISK SCORE ──────────────────────────────────────────────
def calculate_risk_score(reddit_posts, news_articles, weather):
    scores = []
    for p in reddit_posts:  scores.append(p["compound"])
    for n in news_articles: scores.append(n["compound"])
    weather_risk = 0
    if isinstance(weather, dict) and "error" not in weather:
        precip = weather.get("precipitation", 0) or 0
        temp   = weather.get("temperature", 20)  or 20
        if precip > 20:                 weather_risk = -0.4
        elif precip == 0 and temp > 38: weather_risk = -0.3
        elif precip > 5:                weather_risk =  0.1
        scores.append(weather_risk)
    if not scores:
        return 50, "⚪ No Data"
    avg  = sum(scores) / len(scores)
    risk = int((1 - ((avg + 1) / 2)) * 100)
    risk = max(0, min(100, risk))
    label = "🟢 Low Risk" if risk <= 33 else "🟡 Moderate Risk" if risk <= 66 else "🔴 High Risk"
    return risk, label


# ─── CROP DISEASE DETECTION ──────────────────────────────────
def detect_crop_disease(image_bytes, crop_name=""):
    try:
        import google.generativeai as genai
        from PIL import Image
        import io
        api_key = get_secret("GEMINI_API_KEY")
        if not api_key:
            return {"error": "Please add Gemini API key in secrets.toml"}
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3-flash-preview")

        # Convert bytes to PIL Image — most reliable method
        image = Image.open(io.BytesIO(image_bytes))

        prompt = f"""You are an expert plant pathologist. Analyze this crop image carefully.
{"The crop is: " + crop_name if crop_name else ""}

Please provide:
1. **Disease Name** (or "Healthy" if no disease found)
2. **Confidence Level** (High / Medium / Low)
3. **Symptoms Observed** (what you see in the image)
4. **Cause** (fungal / bacterial / viral / nutrient deficiency / pest / environmental)
5. **Severity** (Mild / Moderate / Severe)
6. **Immediate Action** (what to do right now)
7. **Treatment** (specific fungicide/pesticide/remedy with dosage if applicable)
8. **Prevention** (how to prevent this in future)

Be specific and practical. If the image is not a crop or plant, say so clearly."""

        response = model.generate_content([prompt, image])
        return {"result": response.text, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
# ─── CROP PRICES ─────────────────────────────────────────────
# Simulated mandi prices (India) — realistic ranges in INR/quintal
import random
from datetime import datetime, timedelta

MANDI_BASE_PRICES = {
    "Wheat":     {"min": 2100, "max": 2400, "unit": "INR/quintal"},
    "Rice":      {"min": 2000, "max": 2500, "unit": "INR/quintal"},
    "Maize":     {"min": 1700, "max": 2100, "unit": "INR/quintal"},
    "Cotton":    {"min": 6200, "max": 7500, "unit": "INR/quintal"},
    "Sugarcane": {"min": 305,  "max": 340,  "unit": "INR/quintal"},
    "Soybean":   {"min": 3800, "max": 4600, "unit": "INR/quintal"},
    "Barley":    {"min": 1700, "max": 2000, "unit": "INR/quintal"},
    "Potato":    {"min": 800,  "max": 1500, "unit": "INR/quintal"},
    "Tomato":    {"min": 400,  "max": 2500, "unit": "INR/quintal"},
    "Carrot":    {"min": 600,  "max": 1400, "unit": "INR/quintal"},
    "Onion":     {"min": 500,  "max": 3000, "unit": "INR/quintal"},
    "Mustard":   {"min": 4800, "max": 5600, "unit": "INR/quintal"},
    "Groundnut": {"min": 4500, "max": 5500, "unit": "INR/quintal"},
    "Chickpea":  {"min": 4800, "max": 5800, "unit": "INR/quintal"},
}

def get_mandi_prices(crop, days=30):
    """Generate realistic mandi price trend for last N days"""
    if crop not in MANDI_BASE_PRICES:
        return None
    base  = MANDI_BASE_PRICES[crop]
    mid   = (base["min"] + base["max"]) / 2
    dates = [(datetime.now() - timedelta(days=days-i)).strftime("%d %b") for i in range(days)]
    random.seed(hash(crop) % 100)
    prices = []
    price  = mid
    for _ in range(days):
        change = random.uniform(-0.02, 0.02)
        price  = max(base["min"], min(base["max"], price * (1 + change)))
        prices.append(round(price))
    return {
        "dates":   dates,
        "prices":  prices,
        "current": prices[-1],
        "high":    max(prices),
        "low":     min(prices),
        "unit":    base["unit"],
        "change":  round(((prices[-1] - prices[0]) / prices[0]) * 100, 2),
    }

def get_all_mandi_crops():
    return list(MANDI_BASE_PRICES.keys())


# ─── GEMINI CHATBOT ──────────────────────────────────────────
def ask_gemini(question, context=""):
    try:
        import google.generativeai as genai
        api_key = get_secret("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            return "⚠️ Please add your Gemini API key in secrets.toml to use the chatbot."
        genai.configure(api_key=api_key)
        model  = genai.GenerativeModel("gemini-3-flash-preview")
        prompt = f"""You are an expert agriculture assistant. Help farmers and researchers understand 
crop yield, farming practices, weather impacts, soil types, and agricultural trends worldwide.
Answer simply and practically. Only answer agriculture-related questions.
If not agriculture-related say: "I can only help with agriculture-related questions!"

Context: {context}
Question: {question}
Keep answer to 3-5 sentences max."""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Chatbot error: {str(e)}"
