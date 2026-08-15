import os
import pickle
import json
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Suppress TensorFlow logs for clean output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_manager import generate_national_datasets
from models import build_ann_safety_model, build_lstm_trend_model

# Ensure directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

def train_ann():
    print("\n--- Training ANN Safety Classifier Model ---")
    
    # 1. Load or Generate Dataset
    csv_path = "data/crime_incidents.csv"
    if not os.path.exists(csv_path):
        generate_national_datasets()
    df = pd.read_csv(csv_path)
        
    # 2. Feature Engineering: Cyclical features for Time (Hour) and Day of Week
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7.0)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7.0)
    
    # Input features list
    feature_cols = [
        'latitude', 'longitude', 'streetlights', 'population_density', 
        'patrol_frequency', 'base_crime_rate', 'hour_sin', 'hour_cos', 
        'day_sin', 'day_cos'
    ]
    
    X = df[feature_cols].values
    y_score = df['safety_score'].values
    y_level = df['safety_level'].values
    
    # Train-test split
    X_train, X_test, y_score_train, y_score_test, y_level_train, y_level_test = train_test_split(
        X, y_score, y_level, test_size=0.2, random_state=42
    )
    
    # Scale Features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler
    with open("models/scaler_ann.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("Saved ANN feature scaler to models/scaler_ann.pkl")
    
    # 3. Build & Compile Model
    model = build_ann_safety_model(input_dim=len(feature_cols))
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss={
            "safety_score": "mae", 
            "safety_level": "sparse_categorical_crossentropy"
        },
        loss_weights={
            "safety_score": 1.0, 
            "safety_level": 5.0
        },
        metrics={
            "safety_score": "mse", 
            "safety_level": "accuracy"
        }
    )
    
    # 4. Train Model
    history = model.fit(
        X_train_scaled, 
        {"safety_score": y_score_train, "safety_level": y_level_train},
        validation_data=(X_test_scaled, {"safety_score": y_score_test, "safety_level": y_level_test}),
        epochs=30,
        batch_size=64,
        verbose=1
    )
    
    # 5. Evaluate Baseline Random Forest vs ANN
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
    
    print("Training Baseline Random Forest Regressor & Classifier...")
    rf_reg = RandomForestRegressor(n_estimators=30, random_state=42)
    rf_reg.fit(X_train_scaled, y_score_train)
    rf_score_pred = rf_reg.predict(X_test_scaled)
    
    rf_clf = RandomForestClassifier(n_estimators=30, random_state=42)
    rf_clf.fit(X_train_scaled, y_level_train)
    rf_level_pred = rf_clf.predict(X_test_scaled)
    
    # Deep learning predictions
    ann_preds = model.predict(X_test_scaled, verbose=0)
    ann_score_pred = ann_preds[0].flatten()
    ann_level_pred = np.argmax(ann_preds[1], axis=1)
    
    metrics = {
        "baseline_rf": {
            "score_mae": float(mean_absolute_error(y_score_test, rf_score_pred)),
            "score_mse": float(mean_squared_error(y_score_test, rf_score_pred)),
            "score_rmse": float(np.sqrt(mean_squared_error(y_score_test, rf_score_pred))),
            "score_r2": float(r2_score(y_score_test, rf_score_pred)),
            "level_accuracy": float(accuracy_score(y_level_test, rf_level_pred)),
            "level_precision": float(precision_score(y_level_test, rf_level_pred, average="weighted")),
            "level_recall": float(recall_score(y_level_test, rf_level_pred, average="weighted")),
            "level_f1": float(f1_score(y_level_test, rf_level_pred, average="weighted"))
        },
        "ann_dl": {
            "score_mae": float(mean_absolute_error(y_score_test, ann_score_pred)),
            "score_mse": float(mean_squared_error(y_score_test, ann_score_pred)),
            "score_rmse": float(np.sqrt(mean_squared_error(y_score_test, ann_score_pred))),
            "score_r2": float(r2_score(y_score_test, ann_score_pred)),
            "level_accuracy": float(accuracy_score(y_level_test, ann_level_pred)),
            "level_precision": float(precision_score(y_level_test, ann_level_pred, average="weighted")),
            "level_recall": float(recall_score(y_level_test, ann_level_pred, average="weighted")),
            "level_f1": float(f1_score(y_level_test, ann_level_pred, average="weighted"))
        },
        "ann_history": {
            "loss": [float(x) for x in history.history["loss"]],
            "val_loss": [float(x) for x in history.history["val_loss"]],
            "safety_score_loss": [float(x) for x in history.history["safety_score_loss"]],
            "val_safety_score_loss": [float(x) for x in history.history["val_safety_score_loss"]],
            "safety_level_accuracy": [float(x) for x in history.history["safety_level_accuracy"]],
            "val_safety_level_accuracy": [float(x) for x in history.history["val_safety_level_accuracy"]]
        }
    }
    
    # Save RF models to models folder
    with open("models/baseline_rf_regressor.pkl", "wb") as f:
        pickle.dump(rf_reg, f)
    with open("models/baseline_rf_classifier.pkl", "wb") as f:
        pickle.dump(rf_clf, f)
        
    model.save("models/ann_safety_model.h5")
    print("Saved trained ANN model to models/ann_safety_model.h5")
    return metrics

def train_lstm(lookback=12):
    print("\n--- Training LSTM Crime Trend Forecasting Model ---")
    
    # 1. Load or Generate Dataset
    csv_path = "data/monthly_crimes.csv"
    if not os.path.exists(csv_path):
        generate_national_datasets()
    df = pd.read_csv(csv_path)
        
    # 2. Prepare Sequences for LSTM
    # We train a unified LSTM model on historical segments of all cities
    cities = df['city'].unique()
    
    # We will scale the crime index values between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    # Fit scaler on all crime index values
    df['crime_index_scaled'] = scaler.fit_transform(df[['crime_index']])
    
    with open("models/scaler_lstm.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("Saved LSTM index scaler to models/scaler_lstm.pkl")
    
    X_seq, y_val = [], []
    
    for city in cities:
        city_df = df[df['city'] == city].sort_values('date')
        scaled_values = city_df['crime_index_scaled'].values
        
        # Create sliding windows
        for i in range(len(scaled_values) - lookback):
            X_seq.append(scaled_values[i : i + lookback])
            y_val.append(scaled_values[i + lookback])
            
    X_seq = np.array(X_seq)
    y_val = np.array(y_val)
    
    # Reshape input to [samples, time steps, features] for LSTM
    X_seq = np.reshape(X_seq, (X_seq.shape[0], X_seq.shape[1], 1))
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_seq, y_val, test_size=0.15, random_state=42)
    
    # 3. Build & Compile Model
    model = build_lstm_trend_model(lookback)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.002),
        loss="mse",
        metrics=["mae"]
    )
    
    # 4. Train Model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=35,
        batch_size=16,
        verbose=1
    )
    
    # 5. Evaluate and Save Model
    eval_results = model.evaluate(X_test, y_test, verbose=0)
    
    # Convert loss/mae back to real index units for validation reporting
    # RMSE in scaled units
    scaled_rmse = np.sqrt(eval_results[0])
    
    # Dummy inverse transform for scaling back errors roughly (range is index max - index min)
    min_val = float(scaler.data_min_[0])
    max_val = float(scaler.data_max_[0])
    range_val = max_val - min_val
    
    metrics = {
        "lstm_scaled_mse": float(eval_results[0]),
        "lstm_scaled_mae": float(eval_results[1]),
        "lstm_index_mae": float(eval_results[1] * range_val),
        "lstm_index_rmse": float(scaled_rmse * range_val)
    }
    
    model.save("models/lstm_trend_model.h5")
    print("Saved trained LSTM model to models/lstm_trend_model.h5")
    return metrics

def main():
    # Force CPU usage if GPU issues occur, ensuring stability
    try:
        tf.config.set_visible_devices([], 'GPU')
    except Exception:
        pass
        
    ann_metrics = train_ann()
    lstm_metrics = train_lstm()
    
    # Combine and save report metrics
    summary = {
        "ann": ann_metrics,
        "lstm": lstm_metrics,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open("models/model_metrics.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    print("\n--- Training Complete! ---")
    print(json.dumps(summary, indent=4))

if __name__ == "__main__":
    main()
