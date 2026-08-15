import tensorflow as tf
from tensorflow.keras import layers, Model

def build_ann_safety_model(input_dim):
    """
    Builds a Multi-Task Learning Artificial Neural Network (ANN).
    Inputs: Geographic coordinates, temporal sine/cos values, lighting, and police patrols.
    Outputs: 
      - safety_score (Regression target, 0-100 range)
      - safety_level (Classification target, 3 classes: Unsafe, Moderate, Safe)
    """
    inputs = layers.Input(shape=(input_dim,), name="input_features")
    
    # Shared Dense Layers
    x = layers.Dense(256, activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.1)(x)
    
    x = layers.Dense(128, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.1)(x)
    
    x = layers.Dense(64, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    
    # Regression branch for safety score
    # We can use sigmoid scaled to 0-100 or standard linear. Let's use linear with bounding.
    score_out = layers.Dense(1, activation='linear', name='safety_score')(x)
    
    # Classification branch for safety level (0, 1, 2)
    level_out = layers.Dense(3, activation='softmax', name='safety_level')(x)
    
    model = Model(inputs=inputs, outputs=[score_out, level_out], name="ANN_Safety_Classifier")
    return model

def build_lstm_trend_model(lookback):
    """
    Builds an LSTM Recurrent Neural Network for time-series forecasting.
    Inputs: Sequence of historical monthly crime indices (lookback window size)
    Outputs: Predicted crime index for the next month
    """
    inputs = layers.Input(shape=(lookback, 1), name="historical_crime_series")
    
    # LSTM Layers
    x = layers.LSTM(64, return_sequences=True)(inputs)
    x = layers.Dropout(0.2)(x)
    
    x = layers.LSTM(32, return_sequences=False)(x)
    x = layers.Dropout(0.2)(x)
    
    # Dense layer mapping to the single step output
    outputs = layers.Dense(1, activation='linear', name='predicted_crime_index')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name="LSTM_Crime_Forecaster")
    return model

if __name__ == "__main__":
    # Test compilation
    ann = build_ann_safety_model(10)
    ann.summary()
    
    lstm = build_lstm_trend_model(12)
    lstm.summary()
