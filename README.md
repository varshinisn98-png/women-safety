# Women Safety Intelligence System (WSIS) - Indian Cities

An advanced analytics and forecasting system designed to evaluate and predict women's safety levels in Indian cities. The system utilizes machine learning (Artificial Neural Networks and Long Short-Term Memory networks), geospatial mapping, and crowd-sourced reporting to identify crime-prone locations and recommend policy improvements.

---

## Key Features

1. **Multi-Task Learning ANN Safety Classifier**:
   - Classifies any custom latitude/longitude coordinate in real-time into safety levels: **Safe**, **Moderate Risk**, or **High Risk**.
   - Outputs a continuous **Safety Score (0–100%)** based on features like streetlight density, police patrol frequency, population density, historical local crime rate, and time of day.
   - Leverages **cyclical time transformations** (sine/cosine representations for hours and weekdays) to capture time-of-day dynamics.

2. **Temporal LSTM Crime Trend Forecaster**:
   - Takes a 12-month historical sequence of monthly crime indices for a target city.
   - Forecasts the expected crime index monthly for the upcoming **12 months** using a multi-layered LSTM (RNN) model.
   - Highlights trend deviations (e.g. rising or falling risk levels) to support proactive policing.

3. **Interactive Geospatial Safety Heatmap (Folium)**:
   - High-fidelity visual heatmap overlay highlighting high-risk/low-light zones in red and safe zones in green.
   - Supports double-clicking coordinates on the map to trigger immediate ANN risk evaluations for that exact location.
   - Displays real-time citizen-submitted hazard reports on the map as warnings.

4. **Crowdsourced Hazard Center & Database (SQLite)**:
   - Safe citizen portal where authenticated users can pin hazards (e.g., broken streetlights, desolate spots, stalking zones) directly onto the map.
   - Stores and updates reports dynamically in a local SQLite database (`data/safety.db`).
   - Integrated role management (**Citizen**, **Law Enforcement**, **Administrator**) allowing police and admins to review and resolve reports directly from the dashboard.

5. **SOS Emergency Hub**:
   - An animated, pulsating SOS button simulation that broadcasts distress signals with current coordinates to police logs and emergency contacts.
   - Instant portal with key helpline hotlines in India (112, 1091, 181, 100).

6. **Model Diagnostics & Metrics Dashboard**:
   - Full deep learning breakdown showing loss curves, mean absolute error (MAE) points, and classification validation accuracy for the neural networks.

---

## File Structure

```
ws/
│
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation
│
├── venv/                       # Local Python virtual environment
│
├── src/
│   ├── app.py                  # Main Streamlit dashboard & router
│   ├── auth.py                 # Streamlit login/signup panel
│   ├── database.py             # SQLite interface & user seeding
│   ├── data_manager.py         # Geospatial & time-series data generators
│   ├── models.py               # ANN & LSTM architecture configurations
│   ├── train_models.py         # Train-validation loop for models
│   └── styles.py               # Custom CSS for dark glassmorphism styling
│
├── data/                       # Local SQLite DB & generated CSV files
│   ├── safety.db               # SQLite database file
│   ├── city_neighborhoods.csv  # Geographic neighborhood points
│   ├── crime_incidents.csv     # Individual training incidents
│   └── monthly_crimes.csv      # Time-series datasets
│
└── models/                     # Saved model binaries & features scalers
    ├── ann_safety_model.h5     # Trained ANN model
    ├── lstm_trend_model.h5     # Trained LSTM model
    ├── scaler_ann.pkl          # Scaler for ANN features
    ├── scaler_lstm.pkl         # Scaler for LSTM features
    └── model_metrics.json      # Model performance statistics
```

---

## Quick Start

### 1. Set Up Virtual Environment (Done)
```bash
python -m venv venv
```

### 2. Activate Virtual Environment & Install Dependencies (In-Progress)
* **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  .\venv\Scripts\pip install -r requirements.txt
  ```
* **Windows (CMD)**:
  ```cmd
  .\venv\Scripts\activate.bat
  pip install -r requirements.txt
  ```

### 3. Generate Datasets & Train Models
You can compile the datasets and train the deep learning models by running the training pipeline:
```bash
.\venv\Scripts\python src/train_models.py
```
*(Alternatively, you can click the "Generate Datasets" button directly from the Home Dashboard interface on first startup.)*

### 4. Run the Streamlit Application
Start the interactive portal:
```bash
.\venv\Scripts\streamlit run src/app.py
```
The application will launch in your default web browser at `http://localhost:8501`.

---

## Default Accounts for Testing
- **Citizen User**: `citizen` / `citizen123`
- **Law Enforcement Officer**: `police` / `police123`
- **Administrator**: `admin` / `admin123`
- **Alternative Account**: `varsha` / `varsha123`
