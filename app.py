import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime

from country_data  import COUNTRY_DATA
from utils         import (get_weather, get_forecast, get_reddit_posts, get_news,
                            calculate_risk_score, ask_gemini,
                            detect_crop_disease, get_mandi_prices, get_all_mandi_crops)
from ml_model      import predict_yield, get_averages, get_options, get_metrics, get_eda_data, get_performance_data
from crop_calendar import get_calendar, get_available_crops, get_available_seasons
from india_states  import INDIA_STATES
from yield_history import get_yield_history, get_available_crops_history

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(page_title="🌾 AgriIntel", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main{background:#f8fdf4}
    .stTabs [data-baseweb="tab-list"]{gap:6px}
    .stTabs [data-baseweb="tab"]{background:#e8f5e9;border-radius:8px 8px 0 0;padding:6px 14px;font-weight:600;font-size:0.85em}
    .stTabs [aria-selected="true"]{background-color:#2e7d32 !important;color:white !important}
    .metric-card{background:white;border-radius:12px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,0.08);border-left:4px solid #2e7d32;margin-bottom:10px}
    .forecast-card{background:white;border-radius:12px;padding:12px 8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;margin-bottom:8px;border-top:4px solid #4caf50}
    .forecast-card.rain{border-top-color:#1565c0}
    .forecast-card.hot{border-top-color:#e53935}
    .calendar-card{background:white;border-radius:10px;padding:14px;box-shadow:0 2px 6px rgba(0,0,0,0.07);margin-bottom:10px;border-left:4px solid #4caf50}
    .disease-result{background:#f1f8e9;border-radius:12px;padding:20px;border-left:4px solid #2e7d32;margin-top:10px}
    .chat-msg-user{background:#e3f2fd;border-radius:12px 12px 2px 12px;padding:10px 16px;margin:6px 0;text-align:right}
    .chat-msg-bot{background:#f1f8e9;border-radius:12px 12px 12px 2px;padding:10px 16px;margin:6px 0;border-left:3px solid #4caf50}
    .price-up{color:#e53935;font-weight:bold}
    .price-down{color:#4caf50;font-weight:bold}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/wheat.png", width=55)
    st.title("🌾 AgriIntel")
    st.markdown("**Global Agriculture Intelligence**")
    st.divider()
    selected_country = st.selectbox("📍 Select Country", list(COUNTRY_DATA.keys()), index=0)
    country = COUNTRY_DATA[selected_country]
    st.divider()
    st.markdown(f"**{country['flag']} {selected_country}**")
    st.markdown(f"📍 {country['lat']}, {country['lon']}")
    st.divider()
    st.caption("Built by Mandavi Singh | IIT Guwahati")

# ─── TABS ────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🗺️ World Map",
    "📊 Intelligence",
    "🌤️ Forecast",
    "🌾 Yield Predict",
    "📸 Disease AI",
    "📅 Crop Calendar",
    "💰 Mandi Prices",
    "🗺️ India Map",
    "🤖 AgriBot"
])

# ════════════════════════════════════════════════════════════
# TAB 1 — WORLD MAP
# ════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## 🗺️ Global Agriculture Map")
    st.caption("Click any marker to explore that country's agriculture profile.")
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")
    for name, data in COUNTRY_DATA.items():
        html = f"""<div style='font-family:Arial;min-width:200px'>
            <h4 style='color:#2e7d32;margin:0'>{data['flag']} {name}</h4><hr style='margin:5px 0'>
            <b>🌱 Crops:</b> {', '.join(data['famous_crops'][:4])}<br>
            <b>📅 Seasons:</b> {', '.join(data['seasons'][:2])}<br>
            <b>🏞️ Regions:</b> {', '.join(data['major_states'][:3])}</div>"""
        folium.Marker([data['lat'], data['lon']],
            popup=folium.Popup(html, max_width=250),
            tooltip=f"{data['flag']} {name}",
            icon=folium.Icon(color="green", icon="leaf", prefix="fa")
        ).add_to(m)
    st_folium(m, width="100%", height=480)
    st.markdown("---")
    st.markdown("### 🌍 All Countries")
    cols = st.columns(4)
    for i, (name, data) in enumerate(COUNTRY_DATA.items()):
        with cols[i % 4]:
            st.markdown(f"<div class='metric-card'><b>{data['flag']} {name}</b><br><small style='color:#666'>Top: {data['famous_crops'][0]}</small></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 2 — COUNTRY INTELLIGENCE
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"## {country['flag']} {selected_country} — Agriculture Intelligence")
    with st.spinner("Fetching live data..."):
        weather       = get_weather(country['lat'], country['lon'])
        reddit_posts  = get_reddit_posts(country['reddit_subs'], [], limit=8)
        
        st.write(f"Debug: {len(news_articles)} articles")
    risk_score, risk_label = calculate_risk_score(reddit_posts, [], weather)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, label, val, unit in [
        (c1,"🌡️ Temp", weather.get('temperature','N/A'), "°C"),
        (c2,"💧 Humidity", weather.get('humidity','N/A'), "%"),
        (c3,"🌧️ Precip", weather.get('precipitation','N/A'), "mm"),
        (c4,"💨 Wind", weather.get('windspeed','N/A'), "km/h"),
    ]:
        col.markdown(f"<div class='metric-card'><small>{label}</small><br><b style='font-size:1.3em'>{val}{unit}</b></div>", unsafe_allow_html=True)
    color = "#4caf50" if risk_score<=33 else "#ff9800" if risk_score<=66 else "#f44336"
    c5.markdown(f"<div class='metric-card' style='border-left-color:{color}'><small>⚠️ Risk</small><br><b style='font-size:1.3em;color:{color}'>{risk_score}/100</b><br><small>{risk_label}</small></div>", unsafe_allow_html=True)
    st.caption(f"🌤 {weather.get('description','N/A')}")
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🌱 Famous Crops")
        crop_df = pd.DataFrame({"Crop": country['famous_crops'], "Rank": range(1, len(country['famous_crops'])+1)})
        fig = px.bar(crop_df, x="Crop", y="Rank", color="Crop", color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"), height=280, margin=dict(t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown("### 🏔️ Soil Types")
        soil_df = pd.DataFrame({"Soil": country['soil_types'], "Value": [1]*len(country['soil_types'])})
        fig2 = px.pie(soil_df, names="Soil", values="Value", color_discrete_sequence=px.colors.sequential.Greens_r)
        fig2.update_layout(height=280, margin=dict(t=10,b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.markdown("### 📡 Live Social & News Signals")
    col_r, col_n = st.columns(2)
    with col_r:
        st.markdown("#### 💬 Reddit")
        if reddit_posts:
            for p in reddit_posts[:5]:
                clr = "#4caf50" if "🟢" in p['sentiment'] else "#f44336" if "🔴" in p['sentiment'] else "#ff9800"
                st.markdown(f"<div style='background:white;border-radius:8px;padding:9px;border-left:3px solid {clr};margin-bottom:7px'><small>r/{p['subreddit']} • {p['sentiment']}</small><br><a href='{p['url']}' target='_blank' style='color:#1b5e20;text-decoration:none'>{p['title'][:90]}...</a></div>", unsafe_allow_html=True)
        else:
            st.info("Add Reddit API keys in secrets.toml")
    
# ════════════════════════════════════════════════════════════
# TAB 3 — WEATHER FORECAST
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"## 🌤️ 7-Day Forecast — {country['flag']} {selected_country}")
    with st.spinner("Fetching forecast..."):
        forecast = get_forecast(country['lat'], country['lon'])
    if forecast:
        cols = st.columns(7)
        for i, day in enumerate(forecast):
            with cols[i]:
                d         = datetime.strptime(day['date'], "%Y-%m-%d")
                precip    = day['precip'] or 0
                card_cls  = "forecast-card rain" if precip>5 else "forecast-card hot" if day['temp_max']>38 else "forecast-card"
                emoji     = day['desc'].split()[1] if len(day['desc'].split())>1 else "🌡️"
                st.markdown(f"<div class='{card_cls}'><b style='color:#1b5e20'>{d.strftime('%a')}</b><br><small style='color:#888'>{d.strftime('%d %b')}</small><br><div style='font-size:1.4em'>{emoji}</div><br><span style='color:#e53935;font-weight:700'>{day['temp_max']}°</span><span style='color:#888;font-size:0.85em'>/{day['temp_min']}°</span><br><small style='color:#1565c0'>🌧 {precip}mm</small><br><small>💨{day['wind']}km/h</small></div>", unsafe_allow_html=True)
        st.divider()
        df_fc       = pd.DataFrame(forecast)
        df_fc['day']= pd.to_datetime(df_fc['date']).dt.strftime("%a %d")
        col_t, col_r2 = st.columns(2)
        with col_t:
            st.markdown("#### 🌡️ Temperature")
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(x=df_fc['day'],y=df_fc['temp_max'],name="Max",line=dict(color="#e53935",width=2),mode='lines+markers'))
            fig_t.add_trace(go.Scatter(x=df_fc['day'],y=df_fc['temp_min'],name="Min",line=dict(color="#1565c0",width=2),fill='tonexty',fillcolor='rgba(100,181,246,0.12)',mode='lines+markers'))
            fig_t.update_layout(height=260,margin=dict(t=10,b=10),yaxis_title="°C",plot_bgcolor='white',paper_bgcolor='white',legend=dict(orientation="h",y=1.1))
            st.plotly_chart(fig_t, use_container_width=True)
        with col_r2:
            st.markdown("#### 🌧️ Precipitation")
            fig_r = px.bar(df_fc, x='day', y='precip', color='precip', color_continuous_scale=["#e3f2fd","#1565c0"])
            fig_r.update_layout(height=260,margin=dict(t=10,b=10),showlegend=False,plot_bgcolor='white',paper_bgcolor='white')
            st.plotly_chart(fig_r, use_container_width=True)

        st.divider()
        st.markdown("### 🌾 Farming Tips")
        total_rain = sum(d['precip'] or 0 for d in forecast)
        max_temp   = max(d['temp_max'] for d in forecast)
        rainy_days = sum(1 for d in forecast if (d['precip'] or 0)>5)
        tips = []
        if total_rain>50:   tips.append("🌧️ Heavy rain expected — ensure drainage, avoid sowing")
        elif total_rain<5:  tips.append("☀️ Dry week — schedule irrigation, monitor soil moisture")
        else:               tips.append("🌱 Good moisture — suitable for sowing and transplanting")
        if max_temp>40:     tips.append("🔥 Extreme heat — water early morning/evening, use mulching")
        elif max_temp<10:   tips.append("❄️ Cold week — protect sensitive crops from frost")
        else:               tips.append("✅ Temperature suitable for most crops this week")
        if rainy_days>=4:   tips.append("🍄 High humidity — watch for fungal diseases, use fungicide")
        for tip in tips:    st.markdown(f"- {tip}")

# ════════════════════════════════════════════════════════════
# TAB 4 — YIELD PREDICTION
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 🌾 Crop Yield Prediction")
    st.caption("Trained on real India crop yield data (19,380 records) — R² = 94.45%")

    # Load options and metrics
    with st.spinner("Loading model..."):
        options = get_options()
        metrics = get_metrics()

    # Model metrics bar
    m1,m2,m3,m4 = st.columns(4)
    m1.markdown(f"<div class='metric-card'><small>🎯 R² Score</small><br><b style='font-size:1.3em;color:#2e7d32'>{metrics['r2']*100:.1f}%</b></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><small>📉 MAE</small><br><b style='font-size:1.3em'>{metrics['mae']} t/ha</b></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-card'><small>📊 RMSE</small><br><b style='font-size:1.3em'>{metrics['rmse']} t/ha</b></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='metric-card'><small>🗃️ Training Data</small><br><b style='font-size:1.3em'>{metrics['train_size']:,}</b></div>", unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### 📋 Farm Details")
        crop       = st.selectbox("🌱 Crop", options['crops'])
        season     = st.selectbox("📅 Season", options['seasons'])
        state      = st.selectbox("📍 State", options['states'])
        area       = st.number_input("🌍 Farm Area (hectares)", 0.5, 50000000.0, 1000.0, 100.0)
        rainfall   = st.number_input("🌧️ Annual Rainfall (mm)", 0.0, 5000.0, 800.0, 50.0)
        fertilizer = st.number_input("🧪 Fertilizer Used (tons)", 0.0, 10000000.0, 5000.0, 100.0)
        pesticide  = st.number_input("🐛 Pesticide Used (kg)", 0.0, 1000000.0, 500.0, 50.0)
        predict_btn = st.button("🔍 Predict Yield", use_container_width=True, type="primary")

    with col2:
        st.markdown("### 📈 Results")
        if predict_btn:
            with st.spinner("Predicting..."):
                predicted = predict_yield(crop, season, state, area, rainfall, fertilizer, pesticide)
                crop_avg, season_avg, state_avg = get_averages()
            if predicted:
                color = "#2e7d32" if predicted >= crop_avg.get(crop, 0) else "#e53935"
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#1b5e20,#4caf50);color:white;
                            border-radius:14px;padding:20px;text-align:center;margin-bottom:14px'>
                    <div style='font-size:0.9em;opacity:0.9'>Predicted Yield</div>
                    <div style='font-size:2.8em;font-weight:bold'>{predicted}</div>
                    <div style='font-size:0.9em;opacity:0.9'>tons / hectare</div>
                </div>""", unsafe_allow_html=True)

                comp = pd.DataFrame({
                    "Category": ["Your Prediction", f"{crop} Avg", f"{season} Avg", f"{state} Avg"],
                    "Yield":    [predicted,
                                 round(crop_avg.get(crop, 0), 3),
                                 round(season_avg.get(season, 0), 3),
                                 round(state_avg.get(state, 0), 3)]
                })
                fig = px.bar(comp, x="Category", y="Yield", color="Category",
                             color_discrete_sequence=["#2e7d32","#81c784","#a5d6a7","#c8e6c9"],
                             text="Yield")
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                fig.update_layout(showlegend=False, height=290, margin=dict(t=10,b=10),
                                  yaxis_title="Yield (tons/ha)", plot_bgcolor='white', paper_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)

                # Recommendations
                st.markdown("### 💡 Recommendations")
                recs = []
                if predicted < crop_avg.get(crop, 0):
                    recs.append("📌 Below crop average — consider high-yield varieties")
                if rainfall < 500:
                    recs.append("🌧️ Low rainfall area — ensure proper irrigation")
                if fertilizer < 1000:
                    recs.append("🧪 Low fertilizer — balanced NPK can improve yield")
                if predicted > crop_avg.get(crop, 0):
                    recs.append("✅ Above average yield expected — maintain current practices")
                if not recs:
                    recs.append("✅ Inputs look well-optimized!")
                for r in recs:
                    st.markdown(f"- {r}")
            else:
                st.error("Could not predict. Please check inputs.")
        else:
            st.markdown("""
            <div style='text-align:center;padding:50px 20px;color:#888'>
                <div style='font-size:2.5em'>🌾</div>
                <div>Fill in farm details and click <b>Predict Yield</b></div>
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📊 Dataset Overview")
    df_eda = get_eda_data()
    view   = st.radio("View by:", ["Crop","Season","State"], horizontal=True, key="eda_view")
    avg_df = df_eda.groupby(view)['Yield'].mean().reset_index().sort_values('Yield', ascending=False).head(15)
    avg_df.columns = [view, "Avg Yield (t/ha)"]
    fig_eda = px.bar(avg_df, x=view, y="Avg Yield (t/ha)", color=view,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    fig_eda.update_layout(showlegend=False, height=320, margin=dict(t=10,b=10),
                          plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig_eda, use_container_width=True)

    st.divider()
    st.markdown("### 📈 Historical Yield Trends")
    hist_crops = get_available_crops_history(selected_country)
    if hist_crops:
        col_h1, col_h2 = st.columns([1,3])
        with col_h1:
            selected_hist_crop = st.selectbox("Select crop", hist_crops, key="hist_crop")
            compare_crops      = st.multiselect("Compare crops", hist_crops, default=hist_crops[:2], key="compare")
        with col_h2:
            if selected_hist_crop:
                df_hist = get_yield_history(selected_country, selected_hist_crop)
                if df_hist is not None:
                    fig_h = px.line(df_hist, x="Year", y="Yield", markers=True,
                        title=f"{selected_hist_crop} — {selected_country} (2015–2024)",
                        color_discrete_sequence=["#2e7d32"])
                    fig_h.update_layout(height=260, margin=dict(t=30,b=10),
                                        yaxis_title="Yield (t/ha)", plot_bgcolor='white', paper_bgcolor='white')
                    st.plotly_chart(fig_h, use_container_width=True)
            if len(compare_crops) >= 2:
                fig_c = go.Figure()
                for c in compare_crops:
                    df_c = get_yield_history(selected_country, c)
                    if df_c is not None:
                        fig_c.add_trace(go.Scatter(x=df_c['Year'], y=df_c['Yield'], name=c, mode='lines+markers'))
                fig_c.update_layout(height=260, title=f"Crop Comparison — {selected_country}",
                                    margin=dict(t=30,b=10), yaxis_title="Yield (t/ha)",
                                    plot_bgcolor='white', paper_bgcolor='white')
                st.plotly_chart(fig_c, use_container_width=True)
    else:
        st.info(f"Historical data not available for {selected_country} yet.")

    st.divider()
    with st.expander("🔬 Model Performance & Analysis", expanded=False):
        st.markdown("### 🤖 Random Forest — Model Evaluation")
        st.caption("Trained on 19,380 real India crop yield records")

        with st.spinner("Loading performance data..."):
            perf    = get_performance_data()
            metrics = get_metrics()

        c1,c2,c3,c4,c5 = st.columns(5)
        c1.markdown(f"<div class='metric-card'><small>🎯 R² Score</small><br><b style='font-size:1.4em;color:#2e7d32'>{metrics['r2']*100:.2f}%</b></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><small>📉 MAE</small><br><b style='font-size:1.4em'>{metrics['mae']}</b><br><small>t/ha</small></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><small>📊 RMSE</small><br><b style='font-size:1.4em'>{metrics['rmse']}</b><br><small>t/ha</small></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='metric-card'><small>📐 MAPE</small><br><b style='font-size:1.4em'>{metrics['mape']}%</b></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='metric-card'><small>🔁 CV R²</small><br><b style='font-size:1.4em'>{perf['cv_mean']*100:.2f}%</b><br><small>±{perf['cv_std']*100:.2f}%</small></div>", unsafe_allow_html=True)

        st.divider()
        col_p1, col_p2 = st.columns(2)

        with col_p1:
            st.markdown("#### 📍 Actual vs Predicted")
            fig_ap = go.Figure()
            fig_ap.add_trace(go.Scatter(x=perf['y_test'], y=perf['y_pred'],
                mode='markers', marker=dict(color='#2e7d32', opacity=0.5, size=5), name='Predictions'))
            max_val = float(max(perf['y_test'].max(), perf['y_pred'].max()))
            fig_ap.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val],
                mode='lines', line=dict(color='#e53935', dash='dash', width=2), name='Perfect'))
            fig_ap.update_layout(height=320, margin=dict(t=10,b=10),
                xaxis_title="Actual Yield (t/ha)", yaxis_title="Predicted Yield (t/ha)",
                plot_bgcolor='white', paper_bgcolor='white', legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig_ap, use_container_width=True)
            st.caption("Points closer to red line = better predictions")

        with col_p2:
            st.markdown("#### 📊 Residual Distribution")
            fig_res = go.Figure()
            fig_res.add_trace(go.Histogram(x=perf['residuals'], nbinsx=40,
                marker_color='#4caf50', opacity=0.75))
            fig_res.add_vline(x=0, line_dash="dash", line_color="#e53935", line_width=2)
            fig_res.update_layout(height=320, margin=dict(t=10,b=10),
                xaxis_title="Residual (Actual - Predicted)", yaxis_title="Count",
                plot_bgcolor='white', paper_bgcolor='white', showlegend=False)
            st.plotly_chart(fig_res, use_container_width=True)
            st.caption("Good model = residuals centered around 0")

        st.divider()
        col_p3, col_p4 = st.columns(2)

        with col_p3:
            st.markdown("#### 🏆 Feature Importance")
            feat_df = perf['feat_imp'].reset_index()
            feat_df.columns = ['Feature', 'Importance']
            feat_df['Pct'] = (feat_df['Importance'] * 100).round(2)
            fig_fi = px.bar(feat_df, x='Importance', y='Feature', orientation='h',
                color='Importance', color_continuous_scale=["#c8e6c9","#2e7d32"], text='Pct')
            fig_fi.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_fi.update_layout(height=300, margin=dict(t=10,b=10),
                showlegend=False, coloraxis_showscale=False,
                plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig_fi, use_container_width=True)

        with col_p4:
            st.markdown("#### 🔁 Cross-Validation R² (5-Fold)")
            cv_df = pd.DataFrame({
                'Fold': [f'Fold {i+1}' for i in range(len(perf['cv_scores']))],
                'R2':   [round(s, 4) for s in perf['cv_scores']],
                'Pct':  [round(s*100, 2) for s in perf['cv_scores']]
            })
            fig_cv = px.bar(cv_df, x='Fold', y='R2', color='R2',
                color_continuous_scale=["#a5d6a7","#1b5e20"], text='Pct')
            fig_cv.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_cv.add_hline(y=perf['cv_mean'], line_dash="dash", line_color="#e53935",
                annotation_text=f"Mean: {perf['cv_mean']*100:.1f}%")
            fig_cv.update_layout(height=300, margin=dict(t=10,b=10),
                coloraxis_showscale=False, plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig_cv, use_container_width=True)

        st.divider()
        st.markdown("#### 📈 Residuals vs Predicted")
        fig_rv = go.Figure()
        fig_rv.add_trace(go.Scatter(x=perf['y_pred'], y=perf['residuals'],
            mode='markers', marker=dict(color='#1565c0', opacity=0.4, size=4)))
        fig_rv.add_hline(y=0, line_dash="dash", line_color="#e53935", line_width=2)
        fig_rv.update_layout(height=260, margin=dict(t=10,b=10),
            xaxis_title="Predicted Yield (t/ha)", yaxis_title="Residual",
            plot_bgcolor='white', paper_bgcolor='white', showlegend=False)
        st.plotly_chart(fig_rv, use_container_width=True)
        st.caption("Good model = points randomly scattered around 0")

        st.divider()
        st.markdown("#### Model Details")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"- **Algorithm:** Random Forest Regressor")
            st.markdown(f"- **Trees:** 150 estimators")
            st.markdown(f"- **Split:** 80% train / 20% test")
            st.markdown(f"- **Train records:** {metrics['train_size']:,}")
        with col_d2:
            st.markdown(f"- **Test records:** {metrics['test_size']:,}")
            st.markdown(f"- **Dataset:** India Crop Yield (real)")
            st.markdown(f"- **Target:** Yield (tons/hectare)")
            st.markdown(f"- **Features:** Crop, Season, State, Area, Rainfall, Fertilizer, Pesticide")


# ════════════════════════════════════════════════════════════
# TAB 5 — CROP DISEASE DETECTION
# ════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## 📸 Crop Disease Detection — AI")
    st.markdown("Upload a photo of your crop leaf/plant and AI will diagnose the disease instantly.")

    col_u, col_r3 = st.columns([1,1])
    with col_u:
        st.markdown("### 📤 Upload Image")
        crop_name  = st.selectbox("Crop type (optional)", ["","Rice","Wheat","Maize","Cotton","Tomato","Potato","Soybean","Barley","Sugarcane","Other"], key="disease_crop")
        uploaded   = st.file_uploader("Upload crop photo (JPG/PNG)", type=["jpg","jpeg","png"])
        analyze_btn = st.button("🔬 Analyze Disease", use_container_width=True, type="primary", disabled=uploaded is None)

        if uploaded:
            st.image(uploaded, caption="Uploaded image", use_column_width=True)

        st.divider()
        st.markdown("#### 💡 Tips for best results:")
        st.markdown("""
- 📷 Take close-up photo of affected leaf
- ☀️ Good lighting — avoid shadows
- 🎯 Focus on the diseased area
- 📐 Single leaf works better than whole plant
        """)

    with col_r3:
        st.markdown("### 🔬 AI Diagnosis")
        if analyze_btn and uploaded:
            with st.spinner("AI is analyzing your crop image..."):
                img_bytes = uploaded.read()
                result    = detect_crop_disease(img_bytes, crop_name)
            if result["error"]:
                st.error(f"Error: {result['error']}")
            else:
                st.markdown(f"<div class='disease-result'>{result['result']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align:center;padding:60px 20px;color:#888;border:2px dashed #c8e6c9;border-radius:12px'>
                <div style='font-size:3em'>🌿</div>
                <div>Upload a crop image and click<br><b>Analyze Disease</b></div>
            </div>""", unsafe_allow_html=True)
            st.divider()
            st.markdown("#### 🦠 Common Crop Diseases:")
            diseases = [
                ("🌾 Wheat","Rust, Smut, Powdery Mildew, Blight"),
                ("🍚 Rice","Blast, Brown Spot, Sheath Blight, BLB"),
                ("🍅 Tomato","Early Blight, Late Blight, Leaf Curl"),
                ("🌽 Maize","Grey Leaf Spot, Northern Blight, Rust"),
                ("🫘 Soybean","Frogeye Spot, Sudden Death, Rust"),
            ]
            for crop_n, dis in diseases:
                st.markdown(f"**{crop_n}:** {dis}")

# ════════════════════════════════════════════════════════════
# TAB 6 — CROP CALENDAR
# ════════════════════════════════════════════════════════════
with tab6:
    st.markdown("## 📅 Crop Calendar")
    st.markdown("Select your country and crop to get complete farming schedule.")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        cal_country = st.selectbox("🌍 Country", ["India","USA","Brazil","Australia","China"], key="cal_country")
    with col_c2:
        available_crops = get_available_crops(cal_country)
        cal_crop = st.selectbox("🌱 Crop", available_crops if available_crops else ["No data"], key="cal_crop")
    with col_c3:
        available_seasons = get_available_seasons(cal_country, cal_crop)
        cal_season = st.selectbox("📅 Season", available_seasons if available_seasons else ["N/A"], key="cal_season")

    if available_crops and cal_crop != "No data":
        calendar = get_calendar(cal_country, cal_crop)
        if calendar and cal_season in calendar:
            season_data = calendar[cal_season]
            st.markdown(f"### 🗓️ {cal_crop} — {cal_season} Season Calendar ({cal_country})")

            # Timeline visual
            stages = [
                ("🌱 Sowing",      "sowing",      "#4caf50"),
                ("🧪 Fertilizing", "fertilizing", "#ff9800"),
                ("💧 Irrigation",  "irrigation",  "#2196f3"),
                ("🌾 Harvesting",  "harvesting",  "#795548"),
            ]

            for icon_label, key, color in stages:
                if key in season_data:
                    info = season_data[key]
                    st.markdown(f"""
                    <div class='calendar-card' style='border-left-color:{color}'>
                        <div style='display:flex;justify-content:space-between;align-items:center'>
                            <h4 style='margin:0;color:{color}'>{icon_label}</h4>
                            <span style='background:{color};color:white;padding:3px 10px;border-radius:20px;font-size:0.85em'>📅 {info['months']}</span>
                        </div>
                        <p style='margin:8px 0 0 0;color:#444;font-size:0.95em'>💡 {info['tip']}</p>
                    </div>""", unsafe_allow_html=True)

            # Show all seasons if multiple
            if len(calendar) > 1:
                st.divider()
                st.markdown(f"#### Other seasons for {cal_crop} in {cal_country}:")
                other = [s for s in calendar.keys() if s != cal_season]
                for s in other:
                    st.markdown(f"- **{s}** season also available — select from dropdown above")
        else:
            st.info("Calendar data not available for this combination. Select another crop or season.")
    else:
        st.info(f"Calendar data not available for {cal_country}. Available: India, USA, Brazil, Australia, China")

# ════════════════════════════════════════════════════════════
# TAB 7 — MANDI PRICES
# ════════════════════════════════════════════════════════════
with tab7:
    st.markdown("## 💰 Crop Price Tracker — Indian Mandi")
    st.markdown("Live-simulated mandi prices with 30-day trend charts.")

    all_crops   = get_all_mandi_crops()
    col_p1, col_p2 = st.columns([1,2])

    with col_p1:
        price_crop  = st.selectbox("🌱 Select Crop", all_crops, key="price_crop")
        price_days  = st.slider("📅 Days to show", 7, 60, 30)
        st.divider()
        price_data  = get_mandi_prices(price_crop, price_days)
        if price_data:
            chg_color = "price-up" if price_data['change']>0 else "price-down"
            chg_arrow = "▲" if price_data['change']>0 else "▼"
            st.markdown(f"""
            <div class='metric-card'>
                <small>Current Price</small><br>
                <b style='font-size:1.8em'>₹{price_data['current']}</b><br>
                <small>{price_data['unit']}</small>
            </div>
            <div class='metric-card'>
                <small>30-Day Change</small><br>
                <b class='{chg_color}' style='font-size:1.4em'>{chg_arrow} {abs(price_data['change'])}%</b>
            </div>
            <div class='metric-card'>
                <small>Range (30 days)</small><br>
                <b>₹{price_data['low']} – ₹{price_data['high']}</b>
            </div>""", unsafe_allow_html=True)

    with col_p2:
        if price_data:
            df_price = pd.DataFrame({"Date": price_data['dates'], "Price": price_data['prices']})
            fig_p    = go.Figure()
            fig_p.add_trace(go.Scatter(
                x=df_price['Date'], y=df_price['Price'],
                fill='tozeroy', fillcolor='rgba(76,175,80,0.1)',
                line=dict(color="#2e7d32", width=2),
                mode='lines', name="Price"
            ))
            fig_p.update_layout(
                title=f"{price_crop} — Mandi Price Trend (INR/quintal)",
                height=380, margin=dict(t=40,b=20),
                yaxis_title="Price (INR/quintal)",
                xaxis_tickangle=45,
                plot_bgcolor='white', paper_bgcolor='white'
            )
            st.plotly_chart(fig_p, use_container_width=True)

    st.divider()
    st.markdown("### 📊 All Crops — Current Prices")
    all_price_data = []
    for c in all_crops:
        pd_  = get_mandi_prices(c, 7)
        if pd_:
            all_price_data.append({"Crop": c, "Current Price (₹/qtl)": pd_['current'],
                "7-Day High": pd_['high'], "7-Day Low": pd_['low'], "Change %": pd_['change']})
    if all_price_data:
        df_all = pd.DataFrame(all_price_data)
        st.dataframe(df_all, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════
# TAB 8 — INDIA STATE MAP
# ════════════════════════════════════════════════════════════
with tab8:
    st.markdown("## 🗺️ India — State-wise Agriculture Map")
    st.markdown("Click any state marker to see crops, soil, yield and agriculture facts.")

    col_m1, col_m2 = st.columns([2,1])
    with col_m1:
        india_map = folium.Map(location=[22, 80], zoom_start=5, tiles="CartoDB positron")
        for state, data in INDIA_STATES.items():
            popup_html = f"""
            <div style='font-family:Arial;min-width:220px'>
                <h4 style='color:#2e7d32;margin:0'>📍 {state}</h4><hr style='margin:5px 0'>
                <b>🌱 Top Crop:</b> {data['top_crop']}<br>
                <b>🌾 All Crops:</b> {', '.join(data['famous_crops'])}<br>
                <b>🏔️ Soil:</b> {data['soil']}<br>
                <b>💧 Irrigation:</b> {data['irrigation']}<br>
                <b>📊 Avg Yield:</b> {data['annual_yield']} t/ha<br><br>
                <i style='color:#555;font-size:0.9em'>{data['fact']}</i>
            </div>"""
            folium.CircleMarker(
                location=[data['lat'], data['lon']],
                radius=10,
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"📍 {state} — Top: {data['top_crop']}",
                color=data['color'],
                fill=True,
                fill_color=data['color'],
                fill_opacity=0.7
            ).add_to(india_map)
            folium.Marker(
                location=[data['lat'], data['lon']],
                tooltip=f"📍 {state}",
                icon=folium.DivIcon(html=f"<div style='font-size:9px;color:#1b5e20;font-weight:bold;white-space:nowrap'>{state}</div>")
            ).add_to(india_map)
        st_folium(india_map, width="100%", height=500)

    with col_m2:
        st.markdown("### 📋 State Details")
        sel_state = st.selectbox("Select State", list(INDIA_STATES.keys()))
        sd        = INDIA_STATES[sel_state]
        st.markdown(f"""
        <div class='metric-card' style='border-left-color:{sd['color']}'>
            <h4 style='margin:0;color:{sd['color']}'>📍 {sel_state}</h4>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"**🌱 Top Crop:** {sd['top_crop']}")
        st.markdown(f"**📊 Avg Yield:** {sd['annual_yield']} t/ha")
        st.markdown(f"**🏔️ Soil:** {sd['soil']}")
        st.markdown(f"**💧 Irrigation:** {sd['irrigation']}")
        st.markdown("**🌾 All Crops:**")
        for c in sd['famous_crops']: st.markdown(f"  • {c}")
        st.divider()
        st.markdown(f"**💡 Fact:** _{sd['fact']}_")

    st.divider()
    st.markdown("### 📊 State Comparison")
    comp_states = st.multiselect("Select states to compare", list(INDIA_STATES.keys()), default=list(INDIA_STATES.keys())[:5])
    if comp_states:
        comp_df = pd.DataFrame([{"State": s, "Avg Yield (t/ha)": INDIA_STATES[s]['annual_yield'],
            "Top Crop": INDIA_STATES[s]['top_crop']} for s in comp_states])
        fig_s = px.bar(comp_df, x="State", y="Avg Yield (t/ha)", color="Top Crop",
            color_discrete_sequence=px.colors.qualitative.Set2, text="Avg Yield (t/ha)")
        fig_s.update_traces(texttemplate='%{text}', textposition='outside')
        fig_s.update_layout(height=320, margin=dict(t=10,b=10), showlegend=True, plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig_s, use_container_width=True)

# ════════════════════════════════════════════════════════════
# TAB 9 — CHATBOT
# ════════════════════════════════════════════════════════════
with tab9:
    st.markdown("## 🤖 AgriBot — Your Agriculture Assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role":"bot","text":f"👋 Hi! I'm AgriBot. You're exploring **{selected_country}**. Ask me anything about agriculture!"}
        ]
    suggestions = [
        f"What crops grow best in {selected_country}?",
        "What is the best irrigation method for rice?",
        "How does soil type affect yield?",
        "What are signs of pest attack in wheat?"
    ]
    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        if cols[i%2].button(s, key=f"sug_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role":"user","text":s})
            ctx = f"User exploring {selected_country}. Crops: {', '.join(country['famous_crops'][:4])}."
            st.session_state.chat_history.append({"role":"bot","text":ask_gemini(s,ctx)})
    st.divider()
    for msg in st.session_state.chat_history:
        if msg["role"]=="user":
            st.markdown(f"<div class='chat-msg-user'><b>You:</b> {msg['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-msg-bot'>🌾 <b>AgriBot:</b> {msg['text']}</div>", unsafe_allow_html=True)
    st.divider()
    col_i, col_b2 = st.columns([4,1])
    with col_i:
        user_input = st.text_input("Ask anything...", key="chat_input", placeholder="e.g. Best crop for clay soil in India?", label_visibility="collapsed")
    with col_b2:
        send = st.button("Send 🚀", use_container_width=True, type="primary")
    if send and user_input.strip():
        st.session_state.chat_history.append({"role":"user","text":user_input})
        ctx = f"User exploring {selected_country}. Crops: {', '.join(country['famous_crops'][:4])}."
        with st.spinner("Thinking..."):
            resp = ask_gemini(user_input, ctx)
        st.session_state.chat_history.append({"role":"bot","text":resp})
        st.rerun()
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = [{"role":"bot","text":"Chat cleared! Ask me anything 🌾"}]
        st.rerun()
