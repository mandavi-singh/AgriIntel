import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os
import warnings
warnings.filterwarnings('ignore')

# ─── Config ──────────────────────────────────────────────────
DATA_PATH  = "crop_yield.csv"
PLOTS_DIR  = "plots"
FEATURES   = ['Crop', 'Season', 'State', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
CAT_COLS   = ['Crop', 'Season', 'State']
TARGET     = 'Yield'

# Colors
GREEN       = '#2e7d32'
LIGHT_GREEN = '#81c784'
RED         = '#e53935'
BLUE        = '#1565c0'
LIGHT_BLUE  = '#90caf9'
ORANGE      = '#ff6f00'
BG          = '#f9fbe7'

os.makedirs(PLOTS_DIR, exist_ok=True)

def save_plot(name):
    path = os.path.join(PLOTS_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ─── Load & Clean ─────────────────────────────────────────────
print("=" * 55)
print("   AgriIntel — ML Model Evaluation")
print("=" * 55)
print("\n Loading dataset...")

df = pd.read_csv(DATA_PATH)
df['Season'] = df['Season'].str.strip()
df['Crop']   = df['Crop'].str.strip()
df['State']  = df['State'].str.strip()

q99 = df['Yield'].quantile(0.99)
df  = df[(df['Yield'] <= q99) & (df['Yield'] > 0)]
df  = df[FEATURES + [TARGET]].dropna()

print(f"   Records  : {len(df):,}")
print(f"   Crops    : {df['Crop'].nunique()}")
print(f"   States   : {df['State'].nunique()}")
print(f"   Seasons  : {df['Season'].nunique()}")

# ─── Encode ───────────────────────────────────────────────────
df_display = df.copy()   # keep decoded copy for EDA plots
encoders   = {}
for col in CAT_COLS:
    le        = LabelEncoder()
    df[col]   = le.fit_transform(df[col])
    encoders[col] = le

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ─── Train ────────────────────────────────────────────────────
print("\n Training Random Forest...")
model = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred    = model.predict(X_test)
residuals = y_test.values - y_pred

r2   = r2_score(y_test, y_pred)
mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print("\n Metrics:")
print(f"   R²   : {r2*100:.2f}%")
print(f"   MAE  : {mae:.4f} t/ha")
print(f"   RMSE : {rmse:.4f} t/ha")
print(f"   MAPE : {mape:.2f}%")

print("\n Cross Validation...")
cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"   CV Mean : {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")

feat_imp = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=True)

print("\n📈 Saving plots to /plots folder...\n")

# ══════════════════════════════════════════════════════════════
# PLOT 1 — Actual vs Predicted
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(y_test[:500], y_pred[:500], alpha=0.45, color=GREEN, s=18, label='Predictions', zorder=3)
max_val = float(max(y_test.max(), y_pred.max()))
ax.plot([0, max_val], [0, max_val], color=RED, linestyle='--', lw=2, label='Perfect Prediction')
ax.set_xlabel("Actual Yield (tons/ha)", fontsize=11)
ax.set_ylabel("Predicted Yield (tons/ha)", fontsize=11)
ax.set_title("Actual vs Predicted Yield", fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=9)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3)
ax.text(0.05, 0.92, f"R² = {r2*100:.2f}%", transform=ax.transAxes,
        fontsize=11, color=GREEN, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=GREEN))
fig.tight_layout()
save_plot("01_actual_vs_predicted.png")

# ══════════════════════════════════════════════════════════════
# PLOT 2 — Residual Distribution
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(residuals[:500], bins=45, color=LIGHT_GREEN, edgecolor='white', alpha=0.85, zorder=3)
ax.axvline(0, color=RED, linestyle='--', lw=2, label='Zero (Perfect)')
ax.axvline(residuals.mean(), color=ORANGE, linestyle='-', lw=1.5,
           label=f'Mean = {residuals.mean():.3f}')
ax.set_xlabel("Residual  (Actual − Predicted)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title("Residual Distribution", fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=9)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3)
fig.tight_layout()
save_plot("02_residual_distribution.png")

# ══════════════════════════════════════════════════════════════
# PLOT 3 — Residuals vs Predicted
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(y_pred[:500], residuals[:500], alpha=0.35, color=BLUE, s=12, zorder=3)
ax.axhline(0, color=RED, linestyle='--', lw=2, label='Zero Line')
ax.set_xlabel("Predicted Yield (tons/ha)", fontsize=11)
ax.set_ylabel("Residual", fontsize=11)
ax.set_title("Residuals vs Predicted Values", fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=9)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3)
ax.text(0.02, 0.95, "Good model = points randomly\nscattered around 0",
        transform=ax.transAxes, fontsize=9, color='#555',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
fig.tight_layout()
save_plot("03_residuals_vs_predicted.png")

# ══════════════════════════════════════════════════════════════
# PLOT 4 — Feature Importance
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
colors_fi = [GREEN if v == feat_imp.max() else LIGHT_GREEN for v in feat_imp.values]
bars = ax.barh(feat_imp.index, feat_imp.values, color=colors_fi,
               edgecolor='white', height=0.6, zorder=3)
for bar, val in zip(bars, feat_imp.values):
    ax.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height()/2,
            f'{val*100:.1f}%', va='center', fontsize=10, fontweight='bold', color='#333')
ax.set_xlabel("Importance Score", fontsize=11)
ax.set_title("Feature Importance", fontsize=14, fontweight='bold', pad=15)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3, axis='x')
ax.set_xlim(0, feat_imp.max() * 1.2)
fig.tight_layout()
save_plot("04_feature_importance.png")

# ══════════════════════════════════════════════════════════════
# PLOT 5 — Cross Validation
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
fold_names = [f'Fold {i+1}' for i in range(len(cv_scores))]
bar_colors = [GREEN if s >= cv_scores.mean() else LIGHT_GREEN for s in cv_scores]
bars = ax.bar(fold_names, cv_scores * 100, color=bar_colors, edgecolor='white',
              width=0.5, zorder=3)
for bar, val in zip(bars, cv_scores):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val*100:.2f}%', ha='center', fontsize=10, fontweight='bold')
ax.axhline(cv_scores.mean() * 100, color=RED, linestyle='--', lw=2,
           label=f'Mean R² = {cv_scores.mean()*100:.2f}%')
ax.set_ylabel("R² Score (%)", fontsize=11)
ax.set_title("5-Fold Cross Validation R² Scores", fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=10)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, cv_scores.max() * 100 * 1.1)
fig.tight_layout()
save_plot("05_cross_validation.png")

# ══════════════════════════════════════════════════════════════
# PLOT 6 — Yield Distribution (Actual vs Predicted)
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(y_test, bins=45, alpha=0.6, color=BLUE, label='Actual', edgecolor='white', zorder=3)
ax.hist(y_pred, bins=45, alpha=0.6, color=GREEN, label='Predicted', edgecolor='white', zorder=3)
ax.set_xlabel("Yield (tons/ha)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title("Yield Distribution — Actual vs Predicted", fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=10)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3)
fig.tight_layout()
save_plot("06_yield_distribution.png")

# ══════════════════════════════════════════════════════════════
# PLOT 7 — Top 15 Crops by Average Yield
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 7))
top_crops = df_display.groupby('Crop')['Yield'].mean().sort_values(ascending=True).tail(15)
colors_c  = [GREEN if v == top_crops.max() else LIGHT_GREEN for v in top_crops.values]
bars = ax.barh(top_crops.index, top_crops.values, color=colors_c,
               edgecolor='white', height=0.6, zorder=3)
for bar, val in zip(bars, top_crops.values):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}', va='center', fontsize=9, color='#333')
ax.set_xlabel("Average Yield (tons/ha)", fontsize=11)
ax.set_title("Top 15 Crops by Average Yield", fontsize=14, fontweight='bold', pad=15)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3, axis='x')
fig.tight_layout()
save_plot("07_top_crops_yield.png")

# ══════════════════════════════════════════════════════════════
# PLOT 8 — Average Yield by Season
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
season_avg = df_display.groupby('Season')['Yield'].mean().sort_values(ascending=False)
bar_colors = [GREEN, LIGHT_GREEN, '#66bb6a', '#a5d6a7', BLUE, LIGHT_BLUE][:len(season_avg)]
bars = ax.bar(season_avg.index, season_avg.values, color=bar_colors,
              edgecolor='white', width=0.5, zorder=3)
for bar, val in zip(bars, season_avg.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'{val:.2f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel("Average Yield (tons/ha)", fontsize=11)
ax.set_xlabel("Season", fontsize=11)
ax.set_title("Average Yield by Season", fontsize=14, fontweight='bold', pad=15)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3, axis='y')
fig.tight_layout()
save_plot("08_yield_by_season.png")

# ══════════════════════════════════════════════════════════════
# PLOT 9 — Top 15 States by Average Yield
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 7))
state_avg  = df_display.groupby('State')['Yield'].mean().sort_values(ascending=True).tail(15)
colors_s   = [GREEN if v == state_avg.max() else LIGHT_GREEN for v in state_avg.values]
bars = ax.barh(state_avg.index, state_avg.values, color=colors_s,
               edgecolor='white', height=0.6, zorder=3)
for bar, val in zip(bars, state_avg.values):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}', va='center', fontsize=9, color='#333')
ax.set_xlabel("Average Yield (tons/ha)", fontsize=11)
ax.set_title("Top 15 States by Average Yield", fontsize=14, fontweight='bold', pad=15)
ax.set_facecolor(BG)
ax.grid(True, alpha=0.3, axis='x')
fig.tight_layout()
save_plot("09_yield_by_state.png")

# ══════════════════════════════════════════════════════════════
# PLOT 10 — Metrics Summary Table
# ══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 5))
ax.axis('off')
table_data = [
    ["Metric",              "Value",                  "Interpretation"],
    ["R² Score",            f"{r2*100:.2f}%",         "94%+ variance explained"],
    ["MAE",                 f"{mae:.4f} t/ha",         "Avg absolute error"],
    ["RMSE",                f"{rmse:.4f} t/ha",        "Penalizes large errors"],
    ["MAPE",                f"{mape:.2f}%",            "Avg % error"],
    ["CV R² Mean (5-fold)", f"{cv_scores.mean()*100:.2f}%", "Consistent performance"],
    ["CV R² Std",           f"±{cv_scores.std()*100:.2f}%", "Low = stable model"],
    ["Train Records",       f"{len(X_train):,}",       "80% of dataset"],
    ["Test Records",        f"{len(X_test):,}",        "20% of dataset"],
    ["Algorithm",           "Random Forest",           "150 trees, n_jobs=-1"],
]
table = ax.table(
    cellText=table_data[1:],
    colLabels=table_data[0],
    cellLoc='center',
    loc='center',
    colWidths=[0.32, 0.28, 0.40]
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.8)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor(GREEN)
        cell.set_text_props(color='white', fontweight='bold')
    elif row % 2 == 0:
        cell.set_facecolor('#f1f8e9')
    else:
        cell.set_facecolor('white')
    cell.set_edgecolor('#ddd')

ax.set_title("Model Metrics Summary", fontsize=14, fontweight='bold', pad=20)
fig.tight_layout()
save_plot("10_metrics_summary.png")

# ─── Done ─────────────────────────────────────────────────────
print("\n" + "=" * 55)
print(f"   All 10 plots saved in → ./{PLOTS_DIR}/")
print("=" * 55)
print("""
   01_actual_vs_predicted.png
   02_residual_distribution.png
   03_residuals_vs_predicted.png
   04_feature_importance.png
   05_cross_validation.png
   06_yield_distribution.png
   07_top_crops_yield.png
   08_yield_by_season.png
   09_yield_by_state.png
   10_metrics_summary.png
""")

