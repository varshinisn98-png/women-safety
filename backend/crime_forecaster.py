# -*- coding: utf-8 -*-
"""
Crime Forecaster Module -- Abhaya Safety Platform
Provides multi-method future crime prediction:
  1. Linear Trend Extrapolation  (always available, fast)
  2. ARIMA-style autoregressive model (statsmodels, if available)
  3. LSTM deep learning forecast  (tensorflow, if models trained)

All methods return a unified ForecastResult dict so the API and UI
can consume them interchangeably.
"""

import os
import sys
import json
import pickle
import warnings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

warnings.filterwarnings("ignore")

# -----------------------------------------------------------------
# Path setup so this module works when called from backend/ or root
# -----------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "data"))

# -----------------------------------------------------------------
# Real NCRB dataset import
# -----------------------------------------------------------------
try:
    from real_datasets import (
        STATE_RATE_HISTORY,
        STATE_CASES_2023,
        NATIONAL_YEARLY_TOTALS,
        CRIME_CATEGORY_BREAKDOWN_2023,
        build_ncrb_timeseries_df,
        get_state_trend_summary,
    )
    REAL_DATA_AVAILABLE = True
except ImportError:
    REAL_DATA_AVAILABLE = False
    STATE_RATE_HISTORY = {}
    STATE_CASES_2023 = {}
    NATIONAL_YEARLY_TOTALS = {}
    CRIME_CATEGORY_BREAKDOWN_2023 = {}


# ===================================================================
# HELPER: load monthly CSV (merged real + synthetic)
# ===================================================================

def _load_monthly_df() -> Optional[pd.DataFrame]:
    paths = [
        os.path.join(_ROOT, "data", "monthly_crimes.csv"),
        os.path.join(_HERE, "..", "data", "monthly_crimes.csv"),
        "data/monthly_crimes.csv",
    ]
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            df["date"] = pd.to_datetime(df["date"])
            return df
    return None


# ===================================================================
# METHOD 1 -- Linear + Polynomial Trend Extrapolation
# ===================================================================

def forecast_linear(
    state: str,
    horizon_months: int = 36,
    poly_degree: int = 2,
) -> Dict:
    """
    Fits a polynomial trend to historical NCRB annual rates then
    extrapolates forward horizon_months months.
    Returns dates, historical series, and forecast series.
    """
    yr_map = STATE_RATE_HISTORY.get(state)
    if not yr_map:
        return {"error": f"No NCRB data for state: {state}"}

    years = sorted(yr_map.keys())
    rates = [yr_map[y] for y in years]

    # Fit polynomial to annual data
    x = np.array(years, dtype=float)
    y = np.array(rates, dtype=float)
    coeffs = np.polyfit(x - x[0], y, poly_degree)
    poly = np.poly1d(coeffs)

    # Build historical monthly series (2001-2023)
    hist_dates = pd.date_range(start="2001-01-01", end="2023-12-01", freq="MS")
    hist_vals = []
    for dt in hist_dates:
        yr_f = dt.year + (dt.month - 1) / 12.0
        base = float(poly(yr_f - years[0]))
        # Seasonality
        seasonality = np.sin(2 * np.pi * (dt.month - 1) / 12.0) * 3.0
        # COVID adjustment
        covid = 0.0
        if dt.year == 2020 and dt.month in [4, 5, 6, 7]:
            covid = -8.0
        elif dt.year == 2021 and dt.month in [4, 5]:
            covid = -4.0
        val = max(2.0, base + seasonality + covid)
        hist_vals.append(round(val, 2))

    # Build forecast monthly series
    last_year = years[-1]
    last_rate = rates[-1]

    # Detect recent trend (last 5 years)
    recent_years = years[-5:]
    recent_rates = [yr_map[y] for y in recent_years]
    recent_slope = (recent_rates[-1] - recent_rates[0]) / max(1, len(recent_rates) - 1)

    forecast_start = pd.Timestamp("2024-01-01")
    forecast_dates = pd.date_range(start=forecast_start, periods=horizon_months, freq="MS")
    forecast_vals = []

    for i, dt in enumerate(forecast_dates):
        months_ahead = i + 1
        # Linear extrapolation based on recent slope (annualised ? monthly)
        monthly_trend = recent_slope / 12.0
        base = last_rate + monthly_trend * months_ahead

        # Diminishing returns / regression-to-mean: cap growth at 3% per year
        max_cap = last_rate * (1 + 0.03) ** (months_ahead / 12.0)
        min_floor = last_rate * (1 - 0.02) ** (months_ahead / 12.0)
        base = min(base, max_cap)
        base = max(base, min_floor)

        # Seasonality
        seasonality = np.sin(2 * np.pi * (dt.month - 1) / 12.0) * 3.0
        val = max(2.0, base + seasonality)
        forecast_vals.append(round(val, 2))

    # Confidence intervals (?1.5? from mean residual)
    residuals_std = float(np.std(np.array(hist_vals[-24:]) - np.mean(hist_vals[-24:])))
    ci_lower = [round(v - 1.5 * residuals_std, 2) for v in forecast_vals]
    ci_upper = [round(v + 1.5 * residuals_std, 2) for v in forecast_vals]

    # Yearly aggregated forecast
    yearly_forecast = {}
    for i, dt in enumerate(forecast_dates):
        yr = dt.year
        if yr not in yearly_forecast:
            yearly_forecast[yr] = []
        yearly_forecast[yr].append(forecast_vals[i])
    yearly_avg = {yr: round(float(np.mean(vals)), 2) for yr, vals in yearly_forecast.items()}

    return {
        "state": state,
        "method": "Polynomial Trend Extrapolation",
        "historical_dates": [d.strftime("%Y-%m-%d") for d in hist_dates],
        "historical_values": hist_vals,
        "forecast_dates": [d.strftime("%Y-%m-%d") for d in forecast_dates],
        "forecast_values": forecast_vals,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "yearly_avg_forecast": yearly_avg,
        "last_known_rate": float(last_rate),
        "recent_annual_slope": round(float(recent_slope), 3),
        "trend_direction": "Rising" if recent_slope > 0.5 else ("Declining" if recent_slope < -0.5 else "Stable"),
        "horizon_months": horizon_months,
        "confidence_band": f"?{round(1.5 * residuals_std, 1)} per lakh",
    }


# ===================================================================
# METHOD 2 -- ARIMA Autoregressive Model (statsmodels)
# ===================================================================

def forecast_arima(
    state: str,
    horizon_months: int = 36,
) -> Dict:
    """
    Fits ARIMA(2,1,2) to the monthly crime-rate time series and
    returns a horizon_months forecast with 95% confidence interval.
    Falls back to linear forecast if statsmodels is not installed.
    """
    try:
        from statsmodels.tsa.arima.model import ARIMA
        from statsmodels.tsa.statespace.sarimax import SARIMAX
    except ImportError:
        result = forecast_linear(state, horizon_months)
        result["method"] = "Linear Trend (ARIMA unavailable -- install statsmodels)"
        return result

    yr_map = STATE_RATE_HISTORY.get(state)
    if not yr_map:
        return {"error": f"No NCRB data for state: {state}"}

    # Build monthly series from annual data (linear monthly interpolation)
    years = sorted(yr_map.keys())
    monthly_series = []
    monthly_dates = []

    for i, yr in enumerate(years):
        r_start = yr_map[yr]
        r_end = yr_map[years[i + 1]] if i + 1 < len(years) else r_start
        for m in range(1, 13):
            frac = (m - 1) / 12.0
            val = r_start + frac * (r_end - r_start)
            # COVID adjustment
            covid = 0.0
            if yr == 2020 and m in [4, 5, 6, 7]:
                covid = -8.0
            elif yr == 2021 and m in [4, 5]:
                covid = -4.0
            seasonality = np.sin(2 * np.pi * (m - 1) / 12.0) * 3.0
            np.random.seed(hash(f"{state}{yr}{m}") % (2**31))
            noise = float(np.random.normal(0, 0.8))
            v = max(2.0, val + seasonality + covid + noise)
            monthly_series.append(round(v, 2))
            monthly_dates.append(pd.Timestamp(f"{yr}-{m:02d}-01"))

    ts = pd.Series(monthly_series, index=monthly_dates)

    try:
        # SARIMA(1,1,1)(1,0,1,12) captures seasonal pattern
        model = SARIMAX(ts, order=(1, 1, 1), seasonal_order=(1, 0, 1, 12),
                        enforce_stationarity=False, enforce_invertibility=False)
        fitted = model.fit(disp=False, maxiter=200)

        forecast_result = fitted.get_forecast(steps=horizon_months)
        forecast_mean = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int(alpha=0.05)

        forecast_dates = [d.strftime("%Y-%m-%d") for d in forecast_mean.index]
        forecast_vals = [round(max(2.0, float(v)), 2) for v in forecast_mean.values]
        ci_lower = [round(max(2.0, float(v)), 2) for v in conf_int.iloc[:, 0].values]
        ci_upper = [round(max(2.0, float(v)), 2) for v in conf_int.iloc[:, 1].values]

        # Yearly aggregates
        yearly_forecast = {}
        for i, dt in enumerate(forecast_mean.index):
            yr = dt.year
            if yr not in yearly_forecast:
                yearly_forecast[yr] = []
            yearly_forecast[yr].append(forecast_vals[i])
        yearly_avg = {yr: round(float(np.mean(v)), 2) for yr, v in yearly_forecast.items()}

        last_rate = yr_map[years[-1]]
        recent_slope = (yr_map[years[-1]] - yr_map[years[-5]]) / max(1, 4)
        trend_dir = "Rising" if recent_slope > 0.5 else ("Declining" if recent_slope < -0.5 else "Stable")

        return {
            "state": state,
            "method": "SARIMA(1,1,1)(1,0,1,12) Seasonal Autoregressive",
            "historical_dates": [d.strftime("%Y-%m-%d") for d in monthly_dates],
            "historical_values": monthly_series,
            "forecast_dates": forecast_dates,
            "forecast_values": forecast_vals,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "yearly_avg_forecast": yearly_avg,
            "last_known_rate": float(last_rate),
            "recent_annual_slope": round(float(recent_slope), 3),
            "trend_direction": trend_dir,
            "horizon_months": horizon_months,
            "aic": round(float(fitted.aic), 2),
            "bic": round(float(fitted.bic), 2),
        }
    except Exception as e:
        result = forecast_linear(state, horizon_months)
        result["method"] = f"Linear Trend (SARIMA failed: {str(e)[:60]})"
        return result


# ===================================================================
# METHOD 3 -- LSTM Deep Learning Forecast (existing model)
# ===================================================================

def forecast_lstm(
    state: str,
    horizon_months: int = 36,
    models_dir: str = None,
) -> Dict:
    """
    Uses the trained LSTM model (if available) to forecast.
    Falls back to ARIMA if model files are missing.
    """
    if models_dir is None:
        models_dir = os.path.join(_ROOT, "models")

    lstm_path = os.path.join(models_dir, "lstm_trend_model.h5")
    scaler_path = os.path.join(models_dir, "scaler_lstm.pkl")

    if not (os.path.exists(lstm_path) and os.path.exists(scaler_path)):
        return forecast_arima(state, horizon_months)

    try:
        import tensorflow as tf
        try:
            tf.config.set_visible_devices([], "GPU")
        except Exception:
            pass

        lstm_model = tf.keras.models.load_model(lstm_path, compile=False)
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)

        monthly_df = _load_monthly_df()
        if monthly_df is None:
            raise ValueError("monthly_crimes.csv not found")

        state_df = monthly_df[monthly_df["city"] == state].sort_values("date")
        if len(state_df) < 12:
            raise ValueError("Insufficient history")

        scaled = scaler.transform(state_df[["crime_index"]].values)
        lookback = 12
        history = list(scaled.flatten())
        forecasted_scaled = []

        for _ in range(horizon_months):
            seq = np.array(history[-lookback:]).reshape(1, lookback, 1)
            pred = float(lstm_model.predict(seq, verbose=0)[0][0])
            forecasted_scaled.append(pred)
            history.append(pred)

        forecasted_vals = scaler.inverse_transform(
            np.array(forecasted_scaled).reshape(-1, 1)
        ).flatten()

        last_date = state_df["date"].iloc[-1]
        forecast_dates = pd.date_range(
            start=last_date + pd.offsets.MonthBegin(1),
            periods=horizon_months,
            freq="MS"
        )
        forecast_vals = [round(max(2.0, float(v)), 2) for v in forecasted_vals]

        # CI: use residual std from last 24 historical months
        hist_vals = list(state_df["crime_index"].values)
        residual_std = float(np.std(hist_vals[-24:]))
        ci_lower = [round(max(2.0, v - 1.5 * residual_std), 2) for v in forecast_vals]
        ci_upper = [round(v + 1.5 * residual_std, 2) for v in forecast_vals]

        yearly_forecast: Dict[int, list] = {}
        for i, dt in enumerate(forecast_dates):
            yearly_forecast.setdefault(dt.year, []).append(forecast_vals[i])
        yearly_avg = {yr: round(float(np.mean(v)), 2) for yr, v in yearly_forecast.items()}

        last_rate = float(hist_vals[-1])
        recent_slope = (float(hist_vals[-1]) - float(hist_vals[-13])) / 12.0 * 12
        trend_dir = "Rising" if recent_slope > 0.5 else ("Declining" if recent_slope < -0.5 else "Stable")

        return {
            "state": state,
            "method": "LSTM Recurrent Neural Network (Deep Learning)",
            "historical_dates": [d.strftime("%Y-%m-%d") for d in state_df["date"]],
            "historical_values": [round(float(v), 2) for v in hist_vals],
            "forecast_dates": [d.strftime("%Y-%m-%d") for d in forecast_dates],
            "forecast_values": forecast_vals,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "yearly_avg_forecast": yearly_avg,
            "last_known_rate": last_rate,
            "recent_annual_slope": round(float(recent_slope), 3),
            "trend_direction": trend_dir,
            "horizon_months": horizon_months,
        }

    except Exception as e:
        result = forecast_arima(state, horizon_months)
        result["method"] += f" | LSTM fallback ({str(e)[:50]})"
        return result


# ===================================================================
# ENSEMBLE -- combine all 3 methods for best estimate
# ===================================================================

def forecast_ensemble(
    state: str,
    horizon_months: int = 36,
) -> Dict:
    """
    Runs all three methods and returns a weighted ensemble average.
    Weights: LSTM=0.50, ARIMA=0.35, Linear=0.15 when available.
    Falls back gracefully if LSTM or ARIMA are unavailable.
    """
    linear = forecast_linear(state, horizon_months)
    arima  = forecast_arima(state, horizon_months)
    lstm   = forecast_lstm(state, horizon_months)

    has_lstm  = "error" not in lstm  and lstm.get("method", "").startswith("LSTM")
    has_arima = "error" not in arima and "ARIMA" in arima.get("method", "SARIMA")

    if has_lstm and has_arima:
        w_lstm, w_arima, w_linear = 0.50, 0.35, 0.15
    elif has_arima:
        w_lstm, w_arima, w_linear = 0.00, 0.70, 0.30
    else:
        w_lstm, w_arima, w_linear = 0.00, 0.00, 1.00

    n = horizon_months
    lin_v  = linear.get("forecast_values", [0] * n)
    arm_v  = arima.get("forecast_values",  [0] * n)
    lst_v  = lstm.get("forecast_values",   [0] * n)

    lin_lo = linear.get("ci_lower", lin_v)
    lin_hi = linear.get("ci_upper", lin_v)
    arm_lo = arima.get("ci_lower",  arm_v)
    arm_hi = arima.get("ci_upper",  arm_v)
    lst_lo = lstm.get("ci_lower",   lst_v)
    lst_hi = lstm.get("ci_upper",   lst_v)

    ensemble_vals = []
    ci_lower = []
    ci_upper = []
    for i in range(min(n, len(lin_v), len(arm_v), len(lst_v))):
        ev = round(
            w_linear * lin_v[i] + w_arima * arm_v[i] + w_lstm * lst_v[i], 2
        )
        lo = round(
            w_linear * lin_lo[i] + w_arima * arm_lo[i] + w_lstm * lst_lo[i], 2
        )
        hi = round(
            w_linear * lin_hi[i] + w_arima * arm_hi[i] + w_lstm * lst_hi[i], 2
        )
        ensemble_vals.append(ev)
        ci_lower.append(lo)
        ci_upper.append(hi)

    forecast_dates = linear.get("forecast_dates", [])
    yearly_forecast: Dict[int, list] = {}
    for i, d_str in enumerate(forecast_dates[:len(ensemble_vals)]):
        yr = int(d_str[:4])
        yearly_forecast.setdefault(yr, []).append(ensemble_vals[i])
    yearly_avg = {yr: round(float(np.mean(v)), 2) for yr, v in yearly_forecast.items()}

    return {
        "state": state,
        "method": "Ensemble (LSTM + SARIMA + Trend)",
        "weights": {"lstm": w_lstm, "arima": w_arima, "linear": w_linear},
        "historical_dates":  linear.get("historical_dates", []),
        "historical_values": linear.get("historical_values", []),
        "forecast_dates":  forecast_dates,
        "forecast_values": ensemble_vals,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "yearly_avg_forecast": yearly_avg,
        "last_known_rate": linear.get("last_known_rate", 0.0),
        "recent_annual_slope": linear.get("recent_annual_slope", 0.0),
        "trend_direction": linear.get("trend_direction", "Unknown"),
        "horizon_months": horizon_months,
        # Component breakdowns
        "component_linear": lin_v[:n],
        "component_arima":  arm_v[:n],
        "component_lstm":   lst_v[:n],
    }


# ===================================================================
# NATIONAL FORECAST -- aggregate over all states
# ===================================================================

def forecast_national(horizon_years: int = 5) -> Dict:
    """
    Forecasts national total crimes against women for next N years.
    Uses NCRB annual totals 2001-2023 + polynomial regression.
    """
    years = sorted(NATIONAL_YEARLY_TOTALS.keys())
    totals = [NATIONAL_YEARLY_TOTALS[y] for y in years]

    x = np.array(years, dtype=float)
    y = np.array(totals, dtype=float)

    # Fit degree-2 polynomial to national totals
    coeffs = np.polyfit(x - x[0], y, 2)
    poly = np.poly1d(coeffs)

    # Detect recent slope (last 5 years, excluding COVID dip)
    recent = {yr: NATIONAL_YEARLY_TOTALS[yr] for yr in [2018, 2019, 2021, 2022, 2023]}
    recent_yrs = sorted(recent.keys())
    recent_vals = [recent[yr] for yr in recent_yrs]
    recent_slope = (recent_vals[-1] - recent_vals[0]) / (recent_yrs[-1] - recent_yrs[0])

    forecast_years = list(range(2024, 2024 + horizon_years))
    forecast_totals = []
    for yr in forecast_years:
        base = NATIONAL_YEARLY_TOTALS[2023] + recent_slope * (yr - 2023)
        # Cap at 2% annual growth max
        cap = NATIONAL_YEARLY_TOTALS[2023] * (1.02 ** (yr - 2023))
        val = int(min(base, cap))
        forecast_totals.append(val)

    # Optimistic / pessimistic bands (?8%)
    ci_lower = [int(v * 0.92) for v in forecast_totals]
    ci_upper = [int(v * 1.08) for v in forecast_totals]

    return {
        "method": "National Trend Extrapolation (NCRB 2001-2023)",
        "historical_years": years,
        "historical_totals": totals,
        "forecast_years": forecast_years,
        "forecast_totals": forecast_totals,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "annual_change_rate_pct": round(float(recent_slope / NATIONAL_YEARLY_TOTALS[2023] * 100), 2),
        "last_known_year": 2023,
        "last_known_total": NATIONAL_YEARLY_TOTALS[2023],
    }


# ===================================================================
# CRIME-TYPE BREAKDOWN FORECAST
# ===================================================================

def forecast_crime_categories(target_year: int = 2026) -> Dict:
    """
    Projects crime category breakdown for a future year based on
    2023 NCRB proportions and known trend directions.
    """
    # Known trend adjustments per category (annual % change observed 2019-2023)
    category_trends = {
        "Cruelty by Husband/Relatives":       -0.5,
        "Kidnapping & Abduction":             +1.2,
        "Assault on Women":                   +0.8,
        "Rape":                               -0.3,
        "Stalking":                           +2.5,
        "Eve Teasing (Insult to Modesty)":    -1.0,
        "Dowry Deaths":                       -1.5,
        "Trafficking":                        -0.8,
        "Cybercrime (against women)":        +31.2,  # NCRB 2023: 31.2% surge
        "Other IPC Crimes against Women":    +1.0,
    }

    years_ahead = target_year - 2023
    national_2023 = NATIONAL_YEARLY_TOTALS.get(2023, 448211)

    projected = {}
    for cat, pct in CRIME_CATEGORY_BREAKDOWN_2023.items():
        trend = category_trends.get(cat, 0.0)
        future_pct = pct * ((1 + trend / 100) ** years_ahead)
        projected[cat] = round(future_pct, 2)

    # Normalise to 100%
    total_pct = sum(projected.values())
    projected = {k: round(v / total_pct * 100, 2) for k, v in projected.items()}

    # Estimate national total for target year
    nat_total_2023 = national_2023
    recent_slope = (448211 - 405326) / 4  # 2019-2023 avg
    nat_target = int(nat_total_2023 + recent_slope * years_ahead)

    return {
        "target_year": target_year,
        "baseline_year": 2023,
        "baseline_total_cases": national_2023,
        "projected_total_cases": nat_target,
        "projected_breakdown_pct": projected,
        "projected_absolute": {
            cat: int(nat_target * pct / 100) for cat, pct in projected.items()
        },
        "note": "Cybercrime category growing fastest (+31.2%/yr per NCRB 2023 data)"
    }


# ===================================================================
# RISK HOTSPOT FORECAST -- states likely to worsen
# ===================================================================

def forecast_risk_hotspots(horizon_years: int = 3) -> List[Dict]:
    """
    Returns a ranked list of states by projected 2026 crime rate,
    highlighting those with accelerating trends.
    """
    results = []
    for state, yr_map in STATE_RATE_HISTORY.items():
        years = sorted(yr_map.keys())
        if len(years) < 5:
            continue

        r2019 = yr_map.get(2019, yr_map[years[-1]])
        r2023 = yr_map.get(2023, yr_map[years[-1]])

        # Avg annual change 2019-2023
        slope = (r2023 - r2019) / 4.0

        # Project to 2026
        projected_rate = r2023 + slope * horizon_years
        projected_rate = max(2.0, projected_rate)

        # Acceleration check: compare 2017-2019 slope vs 2021-2023 slope
        r2017 = yr_map.get(2017, r2019)
        r2021 = yr_map.get(2021, r2023)
        slope_early = (r2019 - r2017) / 2.0
        slope_late  = (r2023 - r2021) / 2.0
        acceleration = slope_late - slope_early

        if projected_rate >= 100:
            risk_level = "Critical"
        elif projected_rate >= 70:
            risk_level = "High"
        elif projected_rate >= 40:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        results.append({
            "state": state,
            "rate_2023": r2023,
            "projected_rate_2026": round(projected_rate, 1),
            "annual_slope": round(slope, 2),
            "acceleration": round(acceleration, 2),
            "trend": "Accelerating" if acceleration > 0.5 else ("Decelerating" if acceleration < -0.5 else "Steady"),
            "risk_level": risk_level,
            "cases_2023": STATE_CASES_2023.get(state, 0),
        })

    results.sort(key=lambda x: x["projected_rate_2026"], reverse=True)
    return results


# ===================================================================
# CACHE: save/load forecast results to disk
# ===================================================================

_CACHE_DIR = os.path.join(_ROOT, "data", "forecast_cache")

def save_forecast_cache(state: str, method: str, data: Dict):
    os.makedirs(_CACHE_DIR, exist_ok=True)
    fname = f"{state.replace(' ', '_')}_{method}.json"
    with open(os.path.join(_CACHE_DIR, fname), "w") as f:
        json.dump(data, f)


def load_forecast_cache(state: str, method: str) -> Optional[Dict]:
    fname = f"{state.replace(' ', '_')}_{method}.json"
    path = os.path.join(_CACHE_DIR, fname)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


# ===================================================================
# MAIN -- CLI test
# ===================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing crime_forecaster.py")
    print("=" * 60)

    # Test linear forecast
    res = forecast_linear("Delhi", horizon_months=36)
    print(f"\n[Linear] Delhi 2024-2026 yearly avg:")
    for yr, avg in res.get("yearly_avg_forecast", {}).items():
        print(f"  {yr}: {avg:.1f} per lakh female population")
    print(f"  Trend: {res.get('trend_direction')}")

    # Test ARIMA
    res2 = forecast_arima("Rajasthan", horizon_months=36)
    print(f"\n[{res2['method'][:30]}] Rajasthan 2024-2026:")
    for yr, avg in res2.get("yearly_avg_forecast", {}).items():
        print(f"  {yr}: {avg:.1f}")

    # Test national forecast
    nat = forecast_national(5)
    print(f"\n[National Forecast] 2024-2028:")
    for yr, tot in zip(nat["forecast_years"], nat["forecast_totals"]):
        print(f"  {yr}: {tot:,} total CAW cases")

    # Test hotspots
    hotspots = forecast_risk_hotspots(3)
    print(f"\n[Risk Hotspots 2026] Top 5:")
    for h in hotspots[:5]:
        print(f"  {h['state']}: {h['projected_rate_2026']} ({h['risk_level']}, {h['trend']})")

    # Test category forecast
    cats = forecast_crime_categories(2026)
    print(f"\n[Category Forecast 2026] Cybercrime: {cats['projected_breakdown_pct'].get('Cybercrime (against women)', 0):.1f}%")
