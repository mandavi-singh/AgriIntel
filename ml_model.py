import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pickle
import os

# ─── Paths ───────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_PATH   = os.path.join(BASE_DIR, "crop_yield.csv")
MODEL_PATH  = os.path.join(BASE_DIR, "model_real.pkl")
ENC_PATH    = os.path.join(BASE_DIR, "encoders_real.pkl")
META_PATH   = os.path.join(BASE_DIR, "model_meta.pkl")

FEATURES = ['Crop', 'Season', 'State', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
CAT_COLS = ['Crop', 'Season', 'State']
TARGET   = 'Yield'


# ─── Load & Clean Data ───────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Season'] = df['Season'].str.strip()
    df['Crop']   = df['Crop'].str.strip()
    df['State']  = df['State'].str.strip()
    # Remove outliers
    q99 = df['Yield'].quantile(0.99)
    df  = df[(df['Yield'] <= q99) & (df['Yield'] > 0)]
    df  = df[FEATURES + [TARGET]].dropna()
    return df


# ─── Train & Cache Model ─────────────────────────────────────
def get_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(ENC_PATH):
        with open(MODEL_PATH, "rb") as f: model    = pickle.load(f)
        with open(ENC_PATH,   "rb") as f: encoders = pickle.load(f)
        with open(META_PATH,  "rb") as f: meta     = pickle.load(f)
        return model, encoders, meta

    df = load_data()

    # Encode categoricals
    encoders = {}
    for col in CAT_COLS:
        le      = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    meta   = {
        "r2":        round(r2_score(y_test, y_pred), 4),
        "mae":       round(mean_absolute_error(y_test, y_pred), 4),
        "rmse":      round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        "mape":      round(np.mean(np.abs((y_test - y_pred) / y_test)) * 100, 2),
        "train_size":len(X_train),
        "test_size": len(X_test),
        "features":  FEATURES,
        "crops":     list(encoders['Crop'].classes_),
        "seasons":   list(encoders['Season'].classes_),
        "states":    list(encoders['State'].classes_),
    }

    with open(MODEL_PATH, "wb") as f: pickle.dump(model,    f)
    with open(ENC_PATH,   "wb") as f: pickle.dump(encoders, f)
    with open(META_PATH,  "wb") as f: pickle.dump(meta,     f)

    return model, encoders, meta


# ─── Predict ─────────────────────────────────────────────────
def predict_yield(crop, season, state, area, rainfall, fertilizer, pesticide):
    model, encoders, meta = get_model()
    try:
        # Handle unseen labels
        def safe_encode(le, val):
            if val in le.classes_:
                return le.transform([val])[0]
            return le.transform([le.classes_[0]])[0]

        row = pd.DataFrame([[
            safe_encode(encoders['Crop'],   crop),
            safe_encode(encoders['Season'], season),
            safe_encode(encoders['State'],  state),
            float(area),
            float(rainfall),
            float(fertilizer),
            float(pesticide),
        ]], columns=FEATURES)

        return round(float(model.predict(row)[0]), 3)
    except Exception as e:
        return None


# ─── Averages for comparison ─────────────────────────────────
def get_averages():
    df = load_data()
    crop_avg   = df.groupby('Crop')['Yield'].mean().to_dict()
    season_avg = df.groupby('Season')['Yield'].mean().to_dict()
    state_avg  = df.groupby('State')['Yield'].mean().to_dict()
    return crop_avg, season_avg, state_avg


# ─── Get options for dropdowns ───────────────────────────────
def get_options():
    _, encoders, meta = get_model()
    return {
        "crops":   sorted(meta['crops']),
        "seasons": sorted(meta['seasons']),
        "states":  sorted(meta['states']),
    }


# ─── Model metrics ───────────────────────────────────────────
def get_metrics():
    _, _, meta = get_model()
    return meta


# ─── EDA data ────────────────────────────────────────────────
def get_eda_data():
    # Load raw data without encoding — directly for display
    df = pd.read_csv(DATA_PATH)
    df['Season'] = df['Season'].str.strip()
    df['Crop']   = df['Crop'].str.strip()
    df['State']  = df['State'].str.strip()
    q99 = df['Yield'].quantile(0.99)
    df  = df[(df['Yield'] <= q99) & (df['Yield'] > 0)]
    df  = df[FEATURES + [TARGET]].dropna()
    return df


# ─── Model Performance Data for Plots ────────────────────────
def get_performance_data():
    """Returns actual vs predicted values and residuals for plotting"""
    model, encoders, meta = get_model()
    df = load_data()

    for col in CAT_COLS:
        df[col] = encoders[col].transform(df[col])

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    y_pred     = model.predict(X_test)
    residuals  = y_test.values - y_pred

    # Feature importance
    feat_imp = pd.Series(
        model.feature_importances_,
        index=FEATURES
    ).sort_values(ascending=True)

    # Cross validation
    from sklearn.model_selection import cross_val_score
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')

    return {
        "y_test":     y_test.values[:500],   # limit for performance
        "y_pred":     y_pred[:500],
        "residuals":  residuals[:500],
        "feat_imp":   feat_imp,
        "cv_scores":  cv_scores,
        "cv_mean":    round(cv_scores.mean(), 4),
        "cv_std":     round(cv_scores.std(), 4),
    }
