import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# ─── Generate synthetic training data ────────────────────────
def generate_data(n=2000):
    np.random.seed(42)
    crops = ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane",
             "Barley", "Soybean", "Tomato", "Potato", "Carrot"]
    irrigations = ["Drip", "Sprinkler", "Flood", "Rain-fed", "Manual"]
    soils = ["Loamy", "Clay", "Sandy", "Silty", "Peaty", "Chalky"]
    seasons = ["Kharif", "Rabi", "Zaid"]

    base_yield = {
        "Rice": 28, "Wheat": 25, "Maize": 22, "Cotton": 20,
        "Sugarcane": 33, "Barley": 24, "Soybean": 23,
        "Tomato": 34, "Potato": 31, "Carrot": 36
    }
    irr_mult = {"Drip": 1.15, "Sprinkler": 1.10, "Flood": 0.95, "Rain-fed": 0.90, "Manual": 1.0}
    soil_mult = {"Loamy": 1.10, "Clay": 1.05, "Sandy": 0.88, "Silty": 1.08, "Peaty": 1.12, "Chalky": 0.92}
    season_mult = {"Kharif": 1.05, "Rabi": 1.08, "Zaid": 0.97}

    rows = []
    for _ in range(n):
        crop = np.random.choice(crops)
        irr = np.random.choice(irrigations)
        soil = np.random.choice(soils)
        season = np.random.choice(seasons)
        area = np.random.uniform(1, 500)
        fertilizer = np.random.uniform(1, 20)
        pesticide = np.random.uniform(0.1, 10)
        water = np.random.uniform(5000, 100000)

        yield_val = (base_yield[crop]
                     * irr_mult[irr]
                     * soil_mult[soil]
                     * season_mult[season]
                     * (1 + 0.01 * fertilizer)
                     * (1 + 0.005 * pesticide)
                     * np.random.uniform(0.85, 1.15))

        rows.append([crop, irr, soil, season, area, fertilizer, pesticide, water, round(yield_val, 2)])

    return pd.DataFrame(rows, columns=[
        "Crop_Type", "Irrigation_Type", "Soil_Type", "Season",
        "Farm_Area", "Fertilizer_Used", "Pesticide_Used", "Water_Usage", "Yield"
    ])


# ─── Train & cache model ─────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
ENCODERS_PATH = os.path.join(os.path.dirname(__file__), "encoders.pkl")

def get_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(ENCODERS_PATH, "rb") as f:
            encoders = pickle.load(f)
        return model, encoders

    df = generate_data(2000)
    cat_cols = ["Crop_Type", "Irrigation_Type", "Soil_Type", "Season"]
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df.drop("Yield", axis=1)
    y = df["Yield"]

    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(ENCODERS_PATH, "wb") as f:
        pickle.dump(encoders, f)

    return model, encoders


def predict_yield(crop, irrigation, soil, season, area, fertilizer, pesticide, water):
    model, encoders = get_model()
    try:
        row = pd.DataFrame([[crop, irrigation, soil, season, area, fertilizer, pesticide, water]],
                           columns=["Crop_Type", "Irrigation_Type", "Soil_Type", "Season",
                                    "Farm_Area", "Fertilizer_Used", "Pesticide_Used", "Water_Usage"])
        cat_cols = ["Crop_Type", "Irrigation_Type", "Soil_Type", "Season"]
        for col in cat_cols:
            row[col] = encoders[col].transform(row[col])
        return round(float(model.predict(row)[0]), 2)
    except Exception as e:
        return None


def get_averages():
    df = generate_data(2000)
    crop_avg = df.groupby("Crop_Type")["Yield"].mean().to_dict()
    irr_avg = df.groupby("Irrigation_Type")["Yield"].mean().to_dict()
    season_avg = df.groupby("Season")["Yield"].mean().to_dict()
    return crop_avg, irr_avg, season_avg
