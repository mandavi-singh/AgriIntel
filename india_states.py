# ─── India State-wise Agriculture Data ───────────────────────

INDIA_STATES = {
    "Punjab": {
        "lat": 31.1471, "lon": 75.3412,
        "famous_crops": ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"],
        "top_crop": "Wheat",
        "soil": "Alluvial",
        "annual_yield": 4.8,
        "irrigation": "Canal + Tube well",
        "color": "#2e7d32",
        "fact": "Wheat bowl of India — contributes ~35% of India's wheat production"
    },
    "Haryana": {
        "lat": 29.0588, "lon": 76.0856,
        "famous_crops": ["Wheat", "Rice", "Bajra", "Cotton", "Sugarcane"],
        "top_crop": "Wheat",
        "soil": "Alluvial",
        "annual_yield": 4.2,
        "irrigation": "Canal + Tube well",
        "color": "#388e3c",
        "fact": "Second largest wheat producer — advanced mechanized farming"
    },
    "Uttar Pradesh": {
        "lat": 26.8467, "lon": 80.9462,
        "famous_crops": ["Sugarcane", "Wheat", "Rice", "Potato", "Pulses"],
        "top_crop": "Sugarcane",
        "soil": "Alluvial",
        "annual_yield": 3.9,
        "irrigation": "Canal + Tube well",
        "color": "#43a047",
        "fact": "Largest sugarcane producer — also top potato & wheat state"
    },
    "Maharashtra": {
        "lat": 19.7515, "lon": 75.7139,
        "famous_crops": ["Cotton", "Sugarcane", "Soybean", "Onion", "Grapes"],
        "top_crop": "Cotton",
        "soil": "Black (Regur)",
        "annual_yield": 2.1,
        "irrigation": "Rainfed + Drip",
        "color": "#4caf50",
        "fact": "Largest cotton grower — Vidarbha region is India's cotton heartland"
    },
    "Madhya Pradesh": {
        "lat": 22.9734, "lon": 78.6569,
        "famous_crops": ["Soybean", "Wheat", "Chickpea", "Cotton", "Maize"],
        "top_crop": "Soybean",
        "soil": "Black + Red",
        "annual_yield": 2.4,
        "irrigation": "Rainfed",
        "color": "#66bb6a",
        "fact": "Soybean capital of India — also top chickpea & wheat producer"
    },
    "Rajasthan": {
        "lat": 27.0238, "lon": 74.2179,
        "famous_crops": ["Bajra", "Wheat", "Mustard", "Guar", "Jowar"],
        "top_crop": "Bajra",
        "soil": "Sandy + Loamy",
        "annual_yield": 1.8,
        "irrigation": "Canal + Drip",
        "color": "#81c784",
        "fact": "Largest mustard producer — drip irrigation revolution in Rajasthan"
    },
    "Gujarat": {
        "lat": 22.2587, "lon": 71.1924,
        "famous_crops": ["Cotton", "Groundnut", "Wheat", "Castor", "Tobacco"],
        "top_crop": "Cotton",
        "soil": "Black + Alluvial",
        "annual_yield": 2.6,
        "irrigation": "Canal + Drip",
        "color": "#a5d6a7",
        "fact": "Bt cotton revolution started here — highest cotton yield per acre"
    },
    "Andhra Pradesh": {
        "lat": 15.9129, "lon": 79.7400,
        "famous_crops": ["Rice", "Cotton", "Chilli", "Tobacco", "Maize"],
        "top_crop": "Rice",
        "soil": "Alluvial + Red",
        "annual_yield": 3.1,
        "irrigation": "Canal",
        "color": "#1b5e20",
        "fact": "Largest chilli producer — Krishna-Godavari delta is rice bowl of south"
    },
    "Tamil Nadu": {
        "lat": 11.1271, "lon": 78.6569,
        "famous_crops": ["Rice", "Banana", "Sugarcane", "Coconut", "Groundnut"],
        "top_crop": "Rice",
        "soil": "Alluvial + Red",
        "annual_yield": 2.9,
        "irrigation": "Tank + Canal",
        "color": "#2e7d32",
        "fact": "Famous for Samba rice variety — traditional tank irrigation system"
    },
    "West Bengal": {
        "lat": 22.9868, "lon": 87.8550,
        "famous_crops": ["Rice", "Jute", "Potato", "Tea", "Vegetables"],
        "top_crop": "Rice",
        "soil": "Alluvial",
        "annual_yield": 2.7,
        "irrigation": "Canal + Pump",
        "color": "#388e3c",
        "fact": "Largest jute producer — produces 3 rice crops/year in some areas"
    },
    "Karnataka": {
        "lat": 15.3173, "lon": 75.7139,
        "famous_crops": ["Coffee", "Ragi", "Rice", "Sunflower", "Coconut"],
        "top_crop": "Coffee",
        "soil": "Red + Laterite",
        "annual_yield": 1.9,
        "irrigation": "Rainfed + Drip",
        "color": "#43a047",
        "fact": "Largest coffee producer — Coorg produces world-class Arabica coffee"
    },
    "Kerala": {
        "lat": 10.8505, "lon": 76.2711,
        "famous_crops": ["Coconut", "Rubber", "Tea", "Spices", "Rice"],
        "top_crop": "Coconut",
        "soil": "Laterite + Alluvial",
        "annual_yield": 2.2,
        "irrigation": "Rainfed",
        "color": "#4caf50",
        "fact": "Coconut land — largest rubber & spice producer in India"
    },
    "Assam": {
        "lat": 26.2006, "lon": 92.9376,
        "famous_crops": ["Tea", "Rice", "Jute", "Mustard", "Banana"],
        "top_crop": "Tea",
        "soil": "Alluvial + Laterite",
        "annual_yield": 1.7,
        "irrigation": "Rainfed",
        "color": "#66bb6a",
        "fact": "Largest tea producer — Assam tea is famous worldwide"
    },
    "Odisha": {
        "lat": 20.9517, "lon": 85.0985,
        "famous_crops": ["Rice", "Pulses", "Oilseeds", "Sugarcane", "Coconut"],
        "top_crop": "Rice",
        "soil": "Red + Alluvial",
        "annual_yield": 1.8,
        "irrigation": "Canal + Rainfed",
        "color": "#81c784",
        "fact": "Rice is main food crop — traditional Parboiled rice popular here"
    },
    "Bihar": {
        "lat": 25.0961, "lon": 85.3131,
        "famous_crops": ["Rice", "Wheat", "Maize", "Vegetables", "Litchi"],
        "top_crop": "Rice",
        "soil": "Alluvial",
        "annual_yield": 2.1,
        "irrigation": "Tube well + Canal",
        "color": "#a5d6a7",
        "fact": "Largest litchi producer — Mithila Makhana (fox nuts) famous globally"
    },
}

def get_state_info(state_name):
    return INDIA_STATES.get(state_name, None)

def get_all_states():
    return list(INDIA_STATES.keys())
