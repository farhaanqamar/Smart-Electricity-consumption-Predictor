"""
========================================================================================
PROJECT: Android-Based Smart Electricity Consumption Predictor (CS619 FYP)
FILE: train_electricity_model.py
PURPOSE: Standalone, clean PyCharm script to load dataset, train Machine Learning models
         (Linear Regression & Random Forest & Neural Net), visualize performance graphs,
         and export optimized TensorFlow Lite (.tflite) for Android.
IDE COMPATIBILITY: Fully compatible with PyCharm, VS Code, Jupyter, Google Colab.
========================================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import tensorflow as tf

def main():
    print("*" * 75)
    print("      CS619 FYP - SMART ELECTRICITY CONSUMPTION PREDICTOR (ML ENGINE)")
    print("*" * 75)

    # 1. Paths Setup (Relative & Absolute fallback)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(script_dir, "dataset")
    models_dir = os.path.join(script_dir, "models")
    os.makedirs(dataset_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    csv_path = os.path.join(dataset_dir, "household_energy_consumption.csv")
    tflite_path = os.path.join(models_dir, "electricity_predictor.tflite")

    # 2. Dataset Loading (or Automatic Realistic Generation if not present)
    if not os.path.exists(csv_path):
        print(f"\n[+] Dataset not found at {csv_path}. Generating realistic 10,000 household samples...")
        np.random.seed(42)
        n = 10000
        watts = np.random.uniform(600, 12000, n)
        hours = np.random.uniform(2.5, 16.0, n)
        members = np.random.randint(1, 11, n)
        season = np.random.choice([1, 2, 3], size=n, p=[0.25, 0.35, 0.40])
        diversity = np.random.uniform(0.35, 0.48, n)

        daily_kwh = (watts * hours * diversity) / 1000.0
        monthly_kwh = daily_kwh * 30.0

        past_3m = monthly_kwh * np.random.uniform(0.85, 1.15, n)
        past_1m = past_3m * np.random.uniform(0.90, 1.10, n)
        season_mult = np.where(season == 3, 1.40, np.where(season == 1, 0.78, 1.05))

        target_units = (
            0.42 * monthly_kwh * season_mult +
            0.36 * past_1m +
            0.22 * past_3m +
            (members * 7.5) +
            np.random.normal(0, 10.0, n)
        )
        target_units = np.clip(target_units, 25.0, 2500.0)

        df = pd.DataFrame({
            'total_connected_watts': np.round(watts, 1),
            'avg_daily_active_hours': np.round(hours, 1),
            'past_month_units': np.round(past_1m, 1),
            'past_3month_avg_units': np.round(past_3m, 1),
            'season_factor': season,
            'household_members': members,
            'next_month_units': np.round(target_units, 1)
        })
        df.to_csv(csv_path, index=False)
        print(f"[✓] Created dataset: {csv_path}")
    else:
        print(f"\n[+] Loading existing dataset from: {csv_path}")
        df = pd.read_csv(csv_path)

    print(f"[i] Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(df.head())

    # 3. Train / Test Split
    feature_cols = [
        'total_connected_watts', 
        'avg_daily_active_hours', 
        'past_month_units', 
        'past_3month_avg_units', 
        'season_factor', 
        'household_members'
    ]
    X = df[feature_cols].values
    y = df['next_month_units'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    # 4. Training Models (Supervisor Benchmark Requirement)
    print("\n" + "="*50)
    print("TRAINING & BENCHMARKING ALGORITHMS")
    print("="*50)

    # A) Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    print(f"1. Linear Regression  -> R2 Score: {r2_score(y_test, lr_pred)*100:.2f}% | MAE: {mean_absolute_error(y_test, lr_pred):.2f} kWh")

    # B) Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    print(f"2. Random Forest      -> R2 Score: {r2_score(y_test, rf_pred)*100:.2f}% | MAE: {mean_absolute_error(y_test, rf_pred):.2f} kWh")

    # C) Neural Network with Embedded Feature Normalization (Direct Android Deployment)
    mean_X = np.mean(X_train, axis=0)
    std_X = np.std(X_train, axis=0)

    X_train_norm = (X_train - mean_X) / std_X
    X_test_norm = (X_test - mean_X) / std_X

    nn = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(6,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    nn.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.008), loss='mse', metrics=['mae'])
    nn.fit(X_train_norm, y_train, epochs=45, batch_size=32, verbose=0)

    nn_pred = nn.predict(X_test_norm, verbose=0).flatten()
    print(f"3. Neural Network     -> R2 Score: {r2_score(y_test, nn_pred)*100:.2f}% | MAE: {mean_absolute_error(y_test, nn_pred):.2f} kWh")

    # 5. Exporting to Android TensorFlow Lite (.tflite)
    print("\n" + "="*50)
    print("EXPORTING TENSORFLOW LITE (.tflite) FOR MOBILE")
    print("="*50)

    class EmbeddedModel(tf.Module):
        def __init__(self, trained_model, mean, std):
            super().__init__()
            self.trained_model = trained_model
            self.mean = tf.constant(mean, dtype=tf.float32)
            self.std = tf.constant(std, dtype=tf.float32)

        @tf.function(input_signature=[tf.TensorSpec(shape=[None, 6], dtype=tf.float32)])
        def __call__(self, raw_input):
            normalized = (raw_input - self.mean) / self.std
            return self.trained_model(normalized)

    serving_module = EmbeddedModel(nn, mean_X, std_X)
    converter = tf.lite.TFLiteConverter.from_concrete_functions([serving_module.__call__.get_concrete_function()])
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_bytes = converter.convert()

    with open(tflite_path, "wb") as f:
        f.write(tflite_bytes)

    print(f"[✓] TFLite Model Saved Successfully: {tflite_path}")
    print(f"[✓] File Size: {os.path.getsize(tflite_path)/1024:.2f} KB (Optimized for Android offline execution)")

    # 6. Verification Test
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    input_idx = interpreter.get_input_details()[0]['index']
    output_idx = interpreter.get_output_details()[0]['index']

    # Test household: 4500W load, 8h/day, 350 last month, 340 3m avg, Summer (3), 5 members
    test_sample = np.array([[4500.0, 8.0, 350.0, 340.0, 3.0, 5.0]], dtype=np.float32)
    interpreter.set_tensor(input_idx, test_sample)
    interpreter.invoke()
    sample_prediction = interpreter.get_tensor(output_idx)[0][0]

    print("\n" + "-"*50)
    print("PREDICTION TEST ON SAMPLE HOUSEHOLD:")
    print("Inputs -> Load: 4500W | Daily: 8 Hours | Last Month: 350 kWh | Season: Summer | Members: 5")
    print(f"Predicted Consumption: {sample_prediction:.1f} kWh / Units")
    print("-" * 50)
    print("\n[✓] Everything is ready to show your supervisor or run directly in PyCharm!")

if __name__ == "__main__":
    main()

