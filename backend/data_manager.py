# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Create data and models directories if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Allow import of real_datasets from data/ directory
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "data"))

# Complete mapping of 28 States and 8 Union Territories in India with their Capitals and Capital Coordinates
STATES_AND_UT = {
    # Northern Region
    "Delhi": {
        "capital": "New Delhi", "lat": 28.6139, "lon": 77.2090, "base_crime": 0.65, "streetlights": 0.85,
        "districts": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi", "South West Delhi", "North West Delhi", "Shahdara"]
    },
    "Uttar Pradesh": {
        "capital": "Lucknow", "lat": 26.8467, "lon": 80.9462, "base_crime": 0.58, "streetlights": 0.60,
        "districts": ["Lucknow", "Kanpur", "Gautam Buddha Nagar (Noida)", "Varanasi", "Agra", "Prayagraj (Allahabad)", "Meerut", "Ghaziabad", "Bareilly", "Gorakhpur", "Aligarh", "Mathura"]
    },
    "Punjab": {
        "capital": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "base_crime": 0.38, "streetlights": 0.70,
        "districts": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Hoshiarpur", "Pathankot"]
    },
    "Haryana": {
        "capital": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "base_crime": 0.52, "streetlights": 0.68,
        "districts": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Panchkula", "Rohtak", "Karnal", "Sonipat"]
    },
    "Himachal Pradesh": {
        "capital": "Shimla", "lat": 31.1048, "lon": 77.1734, "base_crime": 0.28, "streetlights": 0.55,
        "districts": ["Shimla", "Kangra", "Mandi", "Solan", "Kullu", "Chamba", "Hamirpur", "Una"]
    },
    "Uttarakhand": {
        "capital": "Dehradun", "lat": 30.3165, "lon": 78.0322, "base_crime": 0.35, "streetlights": 0.58,
        "districts": ["Dehradun", "Haridwar", "Nainital", "Udham Singh Nagar", "Rishikesh", "Pithoragarh", "Almora"]
    },
    "Jammu and Kashmir": {
        "capital": "Srinagar", "lat": 34.0837, "lon": 74.7973, "base_crime": 0.45, "streetlights": 0.50,
        "districts": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Kathua", "Udhampur", "Pulwama", "Kupwara"]
    },
    "Ladakh": {
        "capital": "Leh", "lat": 34.1526, "lon": 77.5771, "base_crime": 0.15, "streetlights": 0.40,
        "districts": ["Leh", "Kargil"]
    },
    "Chandigarh": {
        "capital": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "base_crime": 0.32, "streetlights": 0.82,
        "districts": ["Chandigarh District"]
    },
    # Western & Central Region
    "Maharashtra": {
        "capital": "Mumbai", "lat": 19.0760, "lon": 72.8777, "base_crime": 0.46, "streetlights": 0.80,
        "districts": ["Mumbai City", "Mumbai Suburban", "Pune", "Thane", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Amravati", "Kolhapur", "Navi Mumbai"]
    },
    "Gujarat": {
        "capital": "Gandhinagar", "lat": 23.2156, "lon": 72.6369, "base_crime": 0.34, "streetlights": 0.72,
        "districts": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar", "Bhavnagar", "Jamnagar", "Anand"]
    },
    "Rajasthan": {
        "capital": "Jaipur", "lat": 26.9124, "lon": 75.7873, "base_crime": 0.60, "streetlights": 0.58,
        "districts": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Sikar", "Bhilwara", "Jaisalmer"]
    },
    "Madhya Pradesh": {
        "capital": "Bhopal", "lat": 23.2599, "lon": 77.4126, "base_crime": 0.55, "streetlights": 0.55,
        "districts": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Rewa", "Satna"]
    },
    "Chhattisgarh": {
        "capital": "Raipur", "lat": 21.2514, "lon": 81.6296, "base_crime": 0.44, "streetlights": 0.52,
        "districts": ["Raipur", "Durg", "Bilaspur", "Korba", "Rajnandgaon", "Jagdalpur"]
    },
    "Goa": {
        "capital": "Panaji", "lat": 15.4909, "lon": 73.8278, "base_crime": 0.28, "streetlights": 0.75,
        "districts": ["North Goa", "South Goa"]
    },
    "Dadra and Nagar Haveli and Daman and Diu": {
        "capital": "Daman", "lat": 20.3974, "lon": 72.8328, "base_crime": 0.24, "streetlights": 0.65,
        "districts": ["Daman", "Diu", "Dadra and Nagar Haveli"]
    },
    # Southern Region
    "Karnataka": {
        "capital": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "base_crime": 0.36, "streetlights": 0.78,
        "districts": ["Bengaluru Urban", "Bengaluru Rural", "Mysuru", "Dharwad (Hubli)", "Mangaluru (Dakshina Kannada)", "Belagavi", "Kalaburagi", "Udupi", "Davangere", "Tumakuru"]
    },
    "Telangana": {
        "capital": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "base_crime": 0.48, "streetlights": 0.76,
        "districts": ["Hyderabad", "Medchal-Malkajgiri", "Rangareddy", "Warangal", "Nizamabad", "Karimnagar", "Khammam"]
    },
    "Andhra Pradesh": {
        "capital": "Amaravati", "lat": 16.5748, "lon": 80.3736, "base_crime": 0.46, "streetlights": 0.62,
        "districts": ["Visakhapatnam", "Vijayawada (NTR)", "Guntur", "Nellore", "Kurnool", "Tirupati", "Anantapur", "Kadapa", "Kakinada"]
    },
    "Tamil Nadu": {
        "capital": "Chennai", "lat": 13.0827, "lon": 80.2707, "base_crime": 0.32, "streetlights": 0.78,
        "districts": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Vellore", "Kancheepuram", "Thanjavur"]
    },
    "Kerala": {
        "capital": "Thiruvananthapuram", "lat": 8.5241, "lon": 76.9366, "base_crime": 0.34, "streetlights": 0.70,
        "districts": ["Thiruvananthapuram", "Ernakulam (Kochi)", "Kozhikode", "Thrissur", "Kollam", "Kannur", "Kottayam", "Alappuzha", "Palakkad", "Malappuram"]
    },
    "Puducherry": {
        "capital": "Puducherry", "lat": 11.9416, "lon": 79.8083, "base_crime": 0.30, "streetlights": 0.75,
        "districts": ["Puducherry", "Karaikal", "Mahe", "Yanam"]
    },
    "Lakshadweep": {
        "capital": "Kavaratti", "lat": 10.5667, "lon": 72.6417, "base_crime": 0.08, "streetlights": 0.45,
        "districts": ["Lakshadweep District"]
    },
    "Andaman and Nicobar Islands": {
        "capital": "Port Blair", "lat": 11.6234, "lon": 92.7265, "base_crime": 0.22, "streetlights": 0.60,
        "districts": ["South Andaman", "North and Middle Andaman", "Nicobar"]
    },
    # Eastern Region
    "West Bengal": {
        "capital": "Kolkata", "lat": 22.5726, "lon": 88.3639, "base_crime": 0.56, "streetlights": 0.65,
        "districts": ["Kolkata", "North 24 Parganas", "South 24 Parganas", "Howrah", "Hooghly", "Darjeeling", "Paschim Medinipur", "Purba Medinipur", "Murshidabad", "Asansol-Durgapur"]
    },
    "Bihar": {
        "capital": "Patna", "lat": 25.5941, "lon": 85.1376, "base_crime": 0.54, "streetlights": 0.48,
        "districts": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga", "Purnia", "Begusarai", "Arrah", "Nalanda"]
    },
    "Jharkhand": {
        "capital": "Ranchi", "lat": 23.3441, "lon": 85.3090, "base_crime": 0.45, "streetlights": 0.50,
        "districts": ["Ranchi", "East Singhbhum (Jamshedpur)", "Dhanbad", "Bokaro", "Hazaribagh", "Deoghar"]
    },
    "Odisha": {
        "capital": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245, "base_crime": 0.48, "streetlights": 0.55,
        "districts": ["Khordha (Bhubaneswar)", "Cuttack", "Ganjam", "Sundargarh (Rourkela)", "Sambalpur", "Puri", "Balasore"]
    },
    # North-Eastern Region
    "Assam": {
        "capital": "Dispur", "lat": 26.1433, "lon": 91.7898, "base_crime": 0.62, "streetlights": 0.48,
        "districts": ["Kamrup Metropolitan (Guwahati)", "Kamrup", "Dibrugarh", "Silchar (Cachar)", "Jorhat", "Nagaon", "Tezpur (Sonitpur)", "Tinsukia"]
    },
    "Sikkim": {
        "capital": "Gangtok", "lat": 27.3314, "lon": 88.6138, "base_crime": 0.20, "streetlights": 0.62,
        "districts": ["Gangtok", "Gyalshing", "Namchi", "Mangan"]
    },
    "Arunachal Pradesh": {
        "capital": "Itanagar", "lat": 27.0844, "lon": 93.6053, "base_crime": 0.32, "streetlights": 0.42,
        "districts": ["Papum Pare (Itanagar)", "East Siang", "Tawang", "West Kameng", "Changlang", "Lohit"]
    },
    "Nagaland": {
        "capital": "Kohima", "lat": 25.6751, "lon": 94.1086, "base_crime": 0.22, "streetlights": 0.40,
        "districts": ["Kohima", "Dimapur", "Mokokchung", "Wokha", "Tuensang"]
    },
    "Manipur": {
        "capital": "Imphal", "lat": 24.8170, "lon": 93.9368, "base_crime": 0.36, "streetlights": 0.40,
        "districts": ["Imphal West", "Imphal East", "Thoubal", "Churachandpur", "Ukhrul", "Senapati"]
    },
    "Mizoram": {
        "capital": "Aizawl", "lat": 23.7307, "lon": 92.7173, "base_crime": 0.24, "streetlights": 0.48,
        "districts": ["Aizawl", "Lunglei", "Champhai", "Kolasib", "Serchhip"]
    },
    "Tripura": {
        "capital": "Agartala", "lat": 23.8315, "lon": 91.2868, "base_crime": 0.40, "streetlights": 0.52,
        "districts": ["West Tripura (Agartala)", "South Tripura", "North Tripura", "Dhalai"]
    },
    "Meghalaya": {
        "capital": "Shillong", "lat": 25.5788, "lon": 91.8833, "base_crime": 0.30, "streetlights": 0.50,
        "districts": ["East Khasi Hills (Shillong)", "West Garo Hills (Tura)", "West Jaintia Hills", "Ri-Bhoi"]
    }
}

def calculate_safety_index(row):
    """
    Formulates a mathematical safety score (0-100) based on location features.
    This serves as the underlying target generator for the national ANN model.
    """
    score = 100.0
    
    # Streetlight impact (Weight: 30%)
    streetlights = row['streetlights']
    score -= (1.0 - streetlights) * 30.0
    
    # Police Patrol frequency impact (Weight: 20%)
    patrol = row['patrol_frequency']
    score -= (1.0 - patrol) * 20.0
    
    # Base local crime rate impact (Weight: 25%)
    crime_rate = row['base_crime_rate']
    score -= crime_rate * 25.0
    
    # Time of Day impact (Weight: 15%)
    hour = row['hour']
    is_night = (hour >= 22) or (hour <= 5)
    is_late_evening = (hour >= 18) and (hour < 22)
    
    if is_night:
        night_penalty = 15.0 + (1.0 - streetlights) * 10.0
        score -= night_penalty
    elif is_late_evening:
        score -= 8.0 + (1.0 - streetlights) * 5.0
        
    # Population Density / Desolation impact (Weight: 10%)
    pop_density = row['population_density']
    if is_night and pop_density < 0.4:
        score -= 10.0
    elif is_night and pop_density > 0.8:
        score -= 2.0
    
    # Add minor noise to represent real-life variability
    np.random.seed(int(row.get('seed', 42)))
    noise = np.random.normal(0, 1.0)
    score += noise
    
    # Clip between 0 and 100
    score = max(0.0, min(100.0, score))
    return round(score, 2)

def generate_national_datasets(samples_per_taluk=15):
    """
    Generates a national dataset covering all States/UTs, major districts, and sub-districts.
    Compiles:
      - data/national_taluks.csv
      - data/crime_incidents.csv (approx 50,000+ records)
      - data/monthly_crimes.csv (aggregated time series)
    """
    print("Generating National Spatial and Environmental Database...")
    
    taluks_records = []
    incidents_records = []
    
    # Seed control
    seed_idx = 0
    
    for state_name, state_info in STATES_AND_UT.items():
        state_lat = state_info["lat"]
        state_lon = state_info["lon"]
        state_crime_base = state_info["base_crime"]
        state_light_base = state_info["streetlights"]
        districts = state_info["districts"]
        
        # Select scale based on state size to keep coordinates highly realistic and localized
        std_scale = 0.04 if state_name in ["Delhi", "Chandigarh", "Puducherry", "Goa", "Lakshadweep"] else 0.18
        np.random.seed(len(districts) + int(state_lat * 10))
        dist_lats = state_lat + np.random.normal(0, std_scale, size=len(districts))
        dist_lons = state_lon + np.random.normal(0, std_scale, size=len(districts))
        
        for d_idx, dist_name in enumerate(districts):
            d_lat = dist_lats[d_idx]
            d_lon = dist_lons[d_idx]
            
            # Programmatically define 3 sub-districts (taluks) per district
            # e.g., District West, District East, District Center
            taluk_suffixes = ["Central", "West", "East"]
            
            # Distribute taluks in a tight radius around the district center
            np.random.seed(d_idx + int(d_lat * 100))
            taluk_lats = d_lat + np.random.normal(0, 0.08, size=3)
            taluk_lons = d_lon + np.random.normal(0, 0.08, size=3)
            
            for t_idx, suffix in enumerate(taluk_suffixes):
                t_name = f"{dist_name} {suffix}"
                t_lat = taluk_lats[t_idx]
                t_lon = taluk_lons[t_idx]
                
                # Assign environment metrics with slight variance per taluk
                # Capitals and "Central" taluks have better lighting/patrol, "West/East" (suburbs/rural) have less
                lights = max(0.1, min(1.0, state_light_base + (0.05 if suffix == "Central" else -0.1) + np.random.normal(0, 0.05)))
                patrol = max(0.1, min(1.0, 0.6 + (0.1 if suffix == "Central" else -0.15) + np.random.normal(0, 0.05)))
                pop_dens = max(0.1, min(1.0, 0.6 + (0.2 if suffix == "Central" else -0.2) + np.random.normal(0, 0.05)))
                
                # Taluk crime rate fluctuates from state baseline
                t_crime_base = max(0.05, min(0.95, state_crime_base + np.random.normal(0, 0.08)))
                
                # Append taluk details
                taluk_row = {
                    "state": state_name,
                    "district": dist_name,
                    "taluk": t_name,
                    "latitude": round(t_lat, 5),
                    "longitude": round(t_lon, 5),
                    "streetlights": round(lights, 2),
                    "population_density": round(pop_dens, 2),
                    "patrol_frequency": round(patrol, 2),
                    "base_crime_rate": round(t_crime_base, 2)
                }
                taluks_records.append(taluk_row)
                
                # Generate sample incidents in this taluk to build the large 50,000+ dataset
                for _ in range(samples_per_taluk):
                    # Random temporal values
                    hour = np.random.randint(0, 24)
                    day_of_week = np.random.randint(0, 7)
                    
                    # Localized coordinate variance inside the taluk boundary
                    inc_lat = t_lat + np.random.normal(0, 0.008)
                    inc_lon = t_lon + np.random.normal(0, 0.008)
                    
                    # Custom audit variations for the incident spot
                    spot_lights = max(0.05, min(1.0, lights + np.random.normal(0, 0.08)))
                    spot_patrol = max(0.05, min(1.0, patrol + np.random.normal(0, 0.08)))
                    
                    row = {
                        "state": state_name,
                        "district": dist_name,
                        "taluk": t_name,
                        "latitude": round(inc_lat, 5),
                        "longitude": round(inc_lon, 5),
                        "streetlights": round(spot_lights, 2),
                        "population_density": round(pop_dens, 2),
                        "patrol_frequency": round(spot_patrol, 2),
                        "base_crime_rate": round(t_crime_base, 2),
                        "hour": hour,
                        "day_of_week": day_of_week,
                        "seed": seed_idx
                    }
                    
                    seed_idx += 1
                    score = calculate_safety_index(row)
                    
                    # Classify Safety Levels: 0=Unsafe, 1=Moderate, 2=Safe
                    if score >= 75.0:
                        safety_level = 2
                    elif score >= 50.0:
                        safety_level = 1
                    else:
                        safety_level = 0
                        
                    row["safety_score"] = score
                    row["safety_level"] = safety_level
                    
                    # Add incident type details
                    has_crime = 0
                    crime_type = "None"
                    if score < 45.0 and np.random.rand() > 0.3:
                        has_crime = 1
                        crime_type = np.random.choice(["Harassment", "Stalking", "Eve Teasing", "Assault", "Pickpocketing"])
                    elif score < 70.0 and np.random.rand() > 0.7:
                        has_crime = 1
                        crime_type = np.random.choice(["Eve Teasing", "Stalking", "Pickpocketing"])
                        
                    row["incident_occurred"] = has_crime
                    row["crime_type"] = crime_type
                    
                    incidents_records.append(row)
                    
    # Save Spatial Taluks List
    df_taluks = pd.DataFrame(taluks_records)
    df_taluks.to_csv("data/city_neighborhoods.csv", index=False) # Overwrite existing neighborhoods file to simplify loading
    df_taluks.to_csv("data/national_taluks.csv", index=False)
    
    # Save Incidents Logs (Large dataset)
    df_incidents = pd.DataFrame(incidents_records)
    df_incidents.to_csv("data/crime_incidents.csv", index=False)
    
    print(f"Generated {len(df_taluks)} Taluks/Areas.")
    print(f"Generated {len(df_incidents)} detailed crime incidents records (National Scale).")
    
    # 3. Generate aggregated monthly crime trends for each State/UT for LSTM training
    generate_national_timeseries()

def generate_national_timeseries():
    """Generates monthly aggregated crime index rates (Jan 2020 - Aug 2026) for each State/UT."""
    print("Generating State-level Time-Series Aggregates (2020-2026)...")
    months = pd.date_range(start="2020-01-01", end="2026-08-01", freq="MS")
    records = []
    
    for state_name, state_info in STATES_AND_UT.items():
        base_crime_val = state_info["base_crime"]
        # Map baseline score to an index between 15 and 90
        base_index = 15.0 + (base_crime_val * 70.0)
        
        # Assign random linear trends
        np.random.seed(int(state_info["lat"] * 10))
        trend = np.random.uniform(-0.06, 0.08)
        
        for idx, month in enumerate(months):
            crime_index = base_index
            
            # Trend component
            crime_index += idx * trend
            
            # Seasonality (Peaks in Nov-Jan due to early sunset)
            month_num = month.month
            seasonality = np.sin(2 * np.pi * (month_num - 1) / 12.0) * 5.0
            crime_index += seasonality
            
            # Lockdown effects (2020 and 2021 drop)
            covid_effect = 0.0
            if month.year == 2020 and month_num in [4, 5, 6, 7]:
                covid_effect = -25.0
            elif month.year == 2021 and month_num in [4, 5]:
                covid_effect = -12.0
            crime_index += covid_effect
            
            # Random fluctuations
            noise = np.random.normal(0, 2.0)
            crime_index += noise
            
            crime_index = max(5.0, min(100.0, crime_index))
            
            records.append({
                "city": state_name, # Maintain "city" column name to prevent breaking LSTM loader
                "date": month.strftime("%Y-%m-%d"),
                "crime_index": round(crime_index, 2)
            })
            
    df_ts = pd.DataFrame(records)
    df_ts.to_csv("data/monthly_crimes.csv", index=False)
    print(f"Generated {len(df_ts)} synthetic monthly time-series records.")

    # -- Merge in REAL NCRB data (2001-2023) ------------------------------
    merge_real_ncrb_data()


def merge_real_ncrb_data():
    """
    Loads real NCRB state-wise crime-rate history (2001-2023) from
    data/real_datasets.py, converts it to the monthly_crimes.csv format,
    and blends it with any existing synthetic records using a weighted merge.

    Real data takes precedence where it overlaps (2001-2023).
    Synthetic data fills in states not covered by real data.
    The merged file then extends to 2026 with synthetic continuation.
    """
    csv_path = "data/monthly_crimes.csv"
    try:
        from real_datasets import build_ncrb_timeseries_df, STATE_RATE_HISTORY
        REAL_DATA_AVAILABLE = True
    except ImportError:
        print("  [data_manager] real_datasets.py not found - skipping NCRB merge.")
        return

    # Load existing synthetic CSV
    if os.path.exists(csv_path):
        df_synth = pd.read_csv(csv_path)
        df_synth["date"] = pd.to_datetime(df_synth["date"])
    else:
        df_synth = pd.DataFrame(columns=["city", "date", "crime_index"])

    # Build real monthly data
    df_real = build_ncrb_timeseries_df()
    # Rename to match existing schema
    df_real = df_real.rename(columns={"city": "city"})
    df_real["source"] = "NCRB_REAL"

    real_states = set(df_real["city"].unique())

    # Drop synthetic rows for states that now have real data (2001-2023 window)
    if "source" not in df_synth.columns:
        df_synth["source"] = "SYNTHETIC"

    df_synth_keep = df_synth[
        ~(
            df_synth["city"].isin(real_states) &
            (df_synth["date"] >= pd.Timestamp("2001-01-01")) &
            (df_synth["date"] <= pd.Timestamp("2023-12-31"))
        )
    ].copy()

    # Extend real data 2024-2026 with synthetic continuation
    extension_records = []
    for state_name, state_info in STATES_AND_UT.items():
        if state_name not in real_states:
            continue
        # Last known real value for this state
        state_real = df_real[df_real["city"] == state_name].sort_values("date")
        if len(state_real) == 0:
            continue
        last_val = float(state_real["crime_index"].iloc[-1])
        last_date = state_real["date"].iloc[-1]

        np.random.seed(int(abs(hash(state_name))) % (2**31))
        trend = np.random.uniform(-0.04, 0.06)

        ext_months = pd.date_range(
            start=last_date + pd.offsets.MonthBegin(1),
            end=pd.Timestamp("2026-12-01"),
            freq="MS"
        )
        for idx, month in enumerate(ext_months):
            crime_index = last_val + idx * trend
            seasonality = np.sin(2 * np.pi * (month.month - 1) / 12.0) * 5.0
            noise = np.random.normal(0, 1.5)
            crime_index = max(5.0, min(160.0, crime_index + seasonality + noise))
            extension_records.append({
                "city": state_name,
                "date": month,
                "crime_index": round(crime_index, 2),
                "source": "SYNTHETIC_EXT"
            })

    df_ext = pd.DataFrame(extension_records)

    # Merge all three: real (2001-2023) + synthetic remainder + extension (2024-2026)
    df_merged = pd.concat([df_synth_keep, df_real, df_ext], ignore_index=True)
    df_merged = df_merged.drop_duplicates(subset=["city", "date"]).sort_values(["city", "date"])

    # Keep only columns the LSTM expects
    df_out = df_merged[["city", "date", "crime_index"]].copy()
    df_out["date"] = df_out["date"].dt.strftime("%Y-%m-%d")

    df_out.to_csv(csv_path, index=False)
    real_count = len(df_real)
    total_count = len(df_out)
    print(f"  Merged {real_count} real NCRB records + synthetic into {total_count} total monthly records (2001-2026).")
    print(f"  States with real data: {len(real_states)}")


if __name__ == "__main__":
    # Generate large scale dataset
    # We use 20 samples per taluk across ~750 taluks, generating ~15,000 taluk checkpoints,
    # or let's use 50 samples per taluk to hit 36 States * 8 districts * 3 taluks * 50 = ~43,200 records (very large dataset!)
    generate_national_datasets(samples_per_taluk=50)
