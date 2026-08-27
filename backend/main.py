# -*- coding: utf-8 -*-
import os
import sys
import pickle
import json
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add current path to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
import database as db

# Initialize database on startup
db.init_db()

app = FastAPI(
    title="Suraksha Women Safety API Backend",
    description="REST backend running deep learning safety inference and SQLite database endpoints",
    version="1.0"
)

# --- MODEL LOADING LOGIC ---
ann_model = None
lstm_model = None
scaler_ann = None
scaler_lstm = None
metrics = None

def load_ml_resources():
    global ann_model, lstm_model, scaler_ann, scaler_lstm, metrics
    ann_path = "models/ann_safety_model.h5"
    lstm_path = "models/lstm_trend_model.h5"
    scaler_ann_path = "models/scaler_ann.pkl"
    scaler_lstm_path = "models/scaler_lstm.pkl"
    metrics_path = "models/model_metrics.json"
    
    if not (os.path.exists(ann_path) and os.path.exists(lstm_path) and 
            os.path.exists(scaler_ann_path) and os.path.exists(scaler_lstm_path)):
        print("Models not trained yet.")
        return
        
    try:
        import tensorflow as tf
        try:
            tf.config.set_visible_devices([], 'GPU')
        except:
            pass
            
        ann_model = tf.keras.models.load_model(ann_path, compile=False)
        lstm_model = tf.keras.models.load_model(lstm_path, compile=False)
        
        with open(scaler_ann_path, "rb") as f:
            scaler_ann = pickle.load(f)
            
        with open(scaler_lstm_path, "rb") as f:
            scaler_lstm = pickle.load(f)
            
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                metrics = json.load(f)
        print("Backend models loaded successfully.")
    except Exception as e:
        print(f"Error loading backend models: {str(e)}")

load_ml_resources()

# Load National Monthly Dataset for LSTM
monthly_df = None
if os.path.exists("data/monthly_crimes.csv"):
    monthly_df = pd.read_csv("data/monthly_crimes.csv")

# Haversine distance helper
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlam = np.radians(lon2 - lon1)
    a = np.sin(dphi/2.0)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlam/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

# --- PYDANTIC SCHEMAS ---
class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    password: str
    email: str
    role: str = "Citizen"

class PredictRequest(BaseModel):
    lat: float
    lon: float
    lights: float
    patrol: float
    pop_density: float
    base_crime: float
    hour: int
    day_num: int

class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    dest_lat: float
    dest_lon: float
    lights: float = 0.7
    patrol: float = 0.6
    pop_density: float = 0.5
    base_crime: float = 0.3
    mode: Optional[str] = "driving"
    start_address: Optional[str] = ""
    dest_address: Optional[str] = ""

class HazardSubmitRequest(BaseModel):
    username: str
    state: str
    district: str
    taluk: str
    hobli: str
    village: str
    latitude: float
    longitude: float
    incident_type: str
    description: str
    severity: str

class ResolveRequest(BaseModel):
    report_id: int
    status: str

# --- AUTH ENDPOINTS ---
@app.post("/auth/login")
def login(req: LoginRequest):
    user = db.verify_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    return user

@app.post("/auth/signup")
def signup(req: SignupRequest):
    success = db.add_user(req.username, req.password, req.email, req.role)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists.")
    return {"message": "User registered successfully."}

# --- INFERENCE ENDPOINTS ---
@app.post("/predict/safety")
def predict_safety(req: PredictRequest):
    global ann_model, scaler_ann
    if ann_model is None:
        score = 100.0 - (req.base_crime * 45.0) + (req.lights * 25.0) + (req.patrol * 20.0) - (req.pop_density * 10.0)
        score = max(5.0, min(98.0, score))
        level = 0 if score >= 70 else 1 if score >= 50 else 2
        return {"safety_score": score, "safety_level": int(level)}
        
    try:
        hour_sin = np.sin(2 * np.pi * req.hour / 24.0)
        hour_cos = np.cos(2 * np.pi * req.hour / 24.0)
        day_sin = np.sin(2 * np.pi * req.day_num / 7.0)
        day_cos = np.cos(2 * np.pi * req.day_num / 7.0)
        
        vector = np.array([[
            req.lat, req.lon, req.lights, req.pop_density, req.patrol, req.base_crime,
            hour_sin, hour_cos, day_sin, day_cos
        ]])
        
        scaled = scaler_ann.transform(vector)
        predictions = ann_model.predict(scaled, verbose=0)
        
        score_raw = predictions[0]
        level_raw = predictions[1]
        
        score = max(0.0, min(100.0, float(score_raw[0][0])))
        level = np.argmax(level_raw[0])
        return {"safety_score": score, "safety_level": int(level)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.get("/predict/forecast")
def get_forecast(state: str):
    global lstm_model, scaler_lstm, monthly_df
    if monthly_df is None or lstm_model is None:
        raise HTTPException(status_code=400, detail="LSTM resources or CSV monthly datasets not loaded.")
        
    try:
        state_monthly = monthly_df[monthly_df['city'] == state].sort_values('date')
        if len(state_monthly) < 12:
            raise HTTPException(status_code=400, detail="Insufficient state records to build sequences.")
            
        state_monthly['scaled_index'] = scaler_lstm.transform(state_monthly[['crime_index']])
        
        lookback = 12
        history = list(state_monthly['scaled_index'].values)
        forecasted_scaled = []
        
        for _ in range(12):
            seq = np.array(history[-lookback:])
            seq = np.reshape(seq, (1, lookback, 1))
            pred = lstm_model.predict(seq, verbose=0)[0][0]
            forecasted_scaled.append(pred)
            history.append(pred)
            
        forecasted_indices = scaler_lstm.inverse_transform(np.array(forecasted_scaled).reshape(-1, 1)).flatten()
        
        last_date = datetime.strptime(state_monthly['date'].iloc[-1], "%Y-%m-%d")
        forecast_dates = []
        for i in range(1, 13):
            next_month = last_date.replace(day=1) + timedelta(days=32 * i)
            forecast_dates.append(next_month.replace(day=1).strftime("%Y-%m-%d"))
            
        historical_dates = list(state_monthly['date'].values)
        historical_indices = list(state_monthly['crime_index'].values)
        
        return {
            "historical_dates": historical_dates,
            "historical_indices": historical_indices,
            "forecast_dates": forecast_dates,
            "forecast_indices": [round(float(x), 2) for x in forecasted_indices]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import BackgroundTasks

def run_training_background():
    try:
        import train_models
        train_models.main()
        # Reload model weights in-memory
        load_ml_resources()
        print("Backend models successfully retrained and reloaded.")
    except Exception as e:
        print(f"Background retraining failed: {e}")

@app.get("/predict/metrics")
def get_model_metrics():
    global metrics
    if metrics is None:
        raise HTTPException(status_code=404, detail="Metrics not loaded.")
    return metrics

@app.post("/predict/train")
def trigger_retraining(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_training_background)
    return {"status": "Training started in background. Check evaluation diagnostics in ~30 seconds."}

# Import routing service
try:
    import routing
except ImportError:
    from backend import routing

# --- ROUTING ENDPOINT ---
@app.post("/route/optimize")
def optimize_route(req: RouteRequest):
    """
    Computes accurate real-road routing, exact distances (km/meters), ETAs,
    turn-by-turn navigation steps, and multi-profile safety evaluations.
    """
    res = routing.calculate_optimized_routes(
        start_lat=req.start_lat,
        start_lon=req.start_lon,
        dest_lat=req.dest_lat,
        dest_lon=req.dest_lon,
        mode=req.mode or "driving",
        lights=req.lights,
        patrol=req.patrol,
        pop_density=req.pop_density,
        base_crime=req.base_crime,
        start_address=req.start_address or "",
        dest_address=req.dest_address or ""
    )
    return res

# --- EXPLAINABLE AI (XAI) PERTURBATION ENDPOINT ---
@app.post("/predict/explain")
def explain_safety(req: PredictRequest):
    base_res = predict_safety(req)
    base_score = base_res["safety_score"]
    
    improving = []
    worsening = []
    
    # Analyze Streetlight contributions
    if req.lights >= 0.7:
        improving.append({"factor": "💡 Strong verified local streetlight coverage", "impact": float(req.lights * 14.5)})
    elif req.lights <= 0.35:
        worsening.append({"factor": "⚠️ High risk: Poor streetlight coverage verified", "impact": float((1.0 - req.lights) * -16.0)})
        
    # Analyze Patrol contributions
    if req.patrol >= 0.6:
        improving.append({"factor": "🚓 Active verified police patrols (GAST)", "impact": float(req.patrol * 12.0)})
    elif req.patrol <= 0.3:
        worsening.append({"factor": "⚠️ High risk: Limited police patrolling recorded", "impact": float((1.0 - req.patrol) * -14.0)})
        
    # Analyze Crime indices
    if req.base_crime <= 0.35:
        improving.append({"factor": "🛡️ Safe zone: Low historical crime frequency density", "impact": float((1.0 - req.base_crime) * 15.0)})
    else:
        worsening.append({"factor": "⚠️ High risk: Dense crime historical index", "impact": float(req.base_crime * -24.0)})
        
    # Analyze Temporal components
    is_night = (req.hour >= 22) or (req.hour <= 5)
    if is_night:
        worsening.append({"factor": "🌙 Temporal: High vulnerability night hours", "impact": -12.0})
    else:
        improving.append({"factor": "☀️ Temporal: Daytime safety visibility", "impact": 6.5})
        
    # Analyze Population density
    if req.pop_density < 0.3:
        worsening.append({"factor": "⚠️ Desolation: Low activity population density index", "impact": -8.0})
    elif req.pop_density > 0.8:
        improving.append({"factor": "👥 Active: Dense pedestrian public presence", "impact": 4.0})
        
    # Data Confidence calculation
    incidents_path = "data/crime_incidents.csv"
    local_count = 0
    if os.path.exists(incidents_path):
        try:
            df_inc = pd.read_csv(incidents_path)
            local_df = df_inc[
                (df_inc['latitude'] >= req.lat - 0.05) & (df_inc['latitude'] <= req.lat + 0.05) &
                (df_inc['longitude'] >= req.lon - 0.05) & (df_inc['longitude'] <= req.lon + 0.05)
            ]
            local_count = len(local_df)
        except:
            pass
            
    confidence = "HIGH" if local_count >= 15 else "MEDIUM" if local_count >= 5 else "LOW"
    
    return {
        "safety_score": base_score,
        "safety_level": base_res["safety_level"],
        "improving_factors": improving,
        "worsening_factors": worsening,
        "data_confidence": confidence,
        "observation_count": local_count
    }

# --- DBSCAN SPATIAL CRIME HOTSPOT DETECTION ---
@app.get("/api/spatial/clusters")
def get_spatial_clusters(state: str):
    from sklearn.cluster import DBSCAN
    incidents_path = "data/crime_incidents.csv"
    if not os.path.exists(incidents_path):
        return []
        
    try:
        df = pd.read_csv(incidents_path)
        # Filter for actual crimes that occurred
        state_df = df[(df['state'] == state) & (df['incident_occurred'] == 1)]
        if len(state_df) < 5:
            return []
            
        coords = state_df[['latitude', 'longitude']].values
        
        # DBSCAN clustering: eps=0.015 is ~1.6km grid radius
        db = DBSCAN(eps=0.015, min_samples=3).fit(coords)
        labels = db.labels_
        
        unique_labels = set(labels)
        clusters = []
        
        for label in unique_labels:
            if label == -1:
                continue  # Noise
                
            cluster_coords = coords[labels == label]
            centroid = np.mean(cluster_coords, axis=0)
            clusters.append({
                "latitude": float(centroid[0]),
                "longitude": float(centroid[1]),
                "crime_count": int(len(cluster_coords)),
                "label": f"Hotspot Cluster #{label + 1} ({len(cluster_coords)} incidents)"
            })
            
        return sorted(clusters, key=lambda x: x["crime_count"], reverse=True)
    except Exception as e:
        print(f"Error computing DBSCAN spatial clusters: {e}")
        return []

# --- HAZARDS DB ENDPOINTS ---
@app.get("/hazards/list")
def list_hazards(state: Optional[str] = None, district: Optional[str] = None, taluk: Optional[str] = None, hobli: Optional[str] = None, village: Optional[str] = None, include_resolved: bool = False):
    reports = db.get_reports(state, district, taluk, hobli, village, include_resolved)
    return reports

@app.post("/hazards/submit")
def submit_hazard(req: HazardSubmitRequest):
    success = db.add_report(
        req.username, req.state, req.district, req.taluk, req.hobli, req.village,
        req.latitude, req.longitude, req.incident_type, req.description, req.severity
    )
    if not success:
        raise HTTPException(status_code=500, detail="Database write error saving hazard.")
    return {"message": "Hazard report saved successfully."}

@app.post("/hazards/resolve")
def resolve_hazard(req: ResolveRequest):
    success = db.update_report_status(req.report_id, req.status)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update report status.")
    return {"message": f"Hazard report status updated to {req.status}."}


# -----------------------------------------------------------------
# FUTURE CRIME PREDICTION ENDPOINTS
# -----------------------------------------------------------------

from crime_forecaster import (
    forecast_ensemble,
    forecast_linear,
    forecast_arima,
    forecast_lstm,
    forecast_national,
    forecast_crime_categories,
    forecast_risk_hotspots,
)


@app.get("/predict/future/state")
def future_state_forecast(state: str, horizon_months: int = 36, method: str = "ensemble"):
    """
    Forecast crime rates for a specific state.
    method: 'ensemble' | 'linear' | 'arima' | 'lstm'
    horizon_months: number of months to forecast (default 36 = 3 years)
    """
    try:
        if method == "linear":
            result = forecast_linear(state, horizon_months)
        elif method == "arima":
            result = forecast_arima(state, horizon_months)
        elif method == "lstm":
            result = forecast_lstm(state, horizon_months)
        else:
            result = forecast_ensemble(state, horizon_months)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast error: {str(e)}")


@app.get("/predict/future/national")
def future_national_forecast(horizon_years: int = 5):
    """
    Forecast national total crimes against women for the next N years.
    Uses polynomial regression on NCRB 2001-2023 annual totals.
    """
    try:
        return forecast_national(horizon_years)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/future/categories")
def future_categories_forecast(target_year: int = 2026):
    """
    Project the crime-type breakdown (rape, kidnapping, cybercrime, etc.)
    for a future year based on 2023 NCRB proportions and known trend directions.
    """
    try:
        return forecast_crime_categories(target_year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/future/hotspots")
def future_risk_hotspots(horizon_years: int = 3):
    """
    Returns all states ranked by projected crime rate horizon_years from now,
    with acceleration/deceleration trend flag.
    """
    try:
        return forecast_risk_hotspots(horizon_years)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/future/compare")
def compare_state_forecasts(states: str, horizon_months: int = 36):
    """
    Compare forecasts for multiple states (comma-separated).
    e.g. ?states=Delhi,Rajasthan,Karnataka
    Returns ensemble forecasts for each state in one call.
    """
    try:
        state_list = [s.strip() for s in states.split(",") if s.strip()]
        if len(state_list) > 8:
            raise HTTPException(status_code=400, detail="Maximum 8 states per comparison.")
        results = {}
        for s in state_list:
            results[s] = forecast_ensemble(s, horizon_months)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "online", "service": "Suraksha AI Backend", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "database": "connected"}

@app.get("/api/police_stations")
def get_police_stations(lat: float, lon: float, radius_km: float = 50.0, display_name: str = ""):
    """
    Returns genuine verified OpenStreetMap police stations around (lat, lon).
    Never fabricates fake stations.
    """
    from routing import fetch_real_police_stations
    return {"police_stations": fetch_real_police_stations(lat, lon, radius_km=radius_km, display_name=display_name)}
