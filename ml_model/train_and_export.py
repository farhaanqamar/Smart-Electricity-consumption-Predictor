import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

np.random.seed(42)
tf.random.set_seed(42)

BASE_DIR = r"G:\farhan_fyp\ml_model"
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

print("="*60)
print("STEP 1: Generating Comprehensive Household Electricity Dataset")
print("="*60)

# 10,000 realistic household consumption patterns
N = 10000

# Input Features:
# 1. total_connected_watts: Total appliance load (Fans, ACs, Refrigerator, LED lights, Motors, etc.)
# 2. avg_daily_active_hours: Average hours appliances run per day (2 to 18 hours)
# 3. past_month_units: Last month billing units in kWh
# 4. past_3month_avg_units: Average of past 3 months in kWh
# 5. season_factor: 1 = Winter (Nov-Feb), 2 = Moderate (Mar-Apr, Oct), 3 = Peak Summer (May-Sep)
# 6. household_members: Number of residents (1 to 12)

total_connected_watts = np.random.uniform(600, 12000, N)
avg_daily_active_hours = np.random.uniform(2.5, 16.0, N)
household_members = np.random.randint(1, 11, N)
season_factor = np.random.choice([1, 2, 3], size=N, p=[0.25, 0.35, 0.40])

# Realistic physics-based diversity factor + seasonal impact
diversity_factor = np.random.uniform(0.35, 0.48, N)
calculated_daily_kwh = (total_connected_watts * avg_daily_active_hours * diversity_factor) / 1000.0
calculated_monthly_kwh = calculated_daily_kwh * 30.0

# Trend history with noise
past_3month_avg_units = calculated_monthly_kwh * np.random.uniform(0.85, 1.15, N)
past_month_units = past_3month_avg_units * np.random.uniform(0.90, 1.10, N)

# Seasonal multiplier (Summer AC peak usage vs Winter drop)
season_mult = np.where(season_factor == 3, 1.40, np.where(season_factor == 1, 0.78, 1.05))

# Target: Next Month Predicted Units (kWh)
next_month_units = (
    0.42 * calculated_monthly_kwh * season_mult +
    0.36 * past_month_units +
    0.22 * past_3month_avg_units +
    (household_members * 7.5) +
    np.random.normal(0, 10.0, N)
)
next_month_units = np.clip(next_month_units, 25.0, 2500.0)

df = pd.DataFrame({
    'total_connected_watts': np.round(total_connected_watts, 1),
    'avg_daily_active_hours': np.round(avg_daily_active_hours, 1),
    'past_month_units': np.round(past_month_units, 1),
    'past_3month_avg_units': np.round(past_3month_avg_units, 1),
    'season_factor': season_factor,
    'household_members': household_members,
    'next_month_units': np.round(next_month_units, 1)
})

csv_file = os.path.join(DATASET_DIR, "household_energy_consumption.csv")
df.to_csv(csv_file, index=False)
print(f"Dataset successfully created and saved to Google Drive: {csv_file}")
print(df.head(5))

print("\n" + "="*60)
print("STEP 2: Model Training & Comparison (Linear Regression vs Random Forest vs Neural Net)")
print("="*60)

feature_cols = ['total_connected_watts', 'avg_daily_active_hours', 'past_month_units', 
                'past_3month_avg_units', 'season_factor', 'household_members']
X = df[feature_cols].values
y = df['next_month_units'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# 1. Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
print(f"[Linear Regression]  R2: {r2_score(y_test, lr_pred)*100:.2f}% | MAE: {mean_absolute_error(y_test, lr_pred):.2f} kWh")

# 2. Random Forest Regressor
rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
print(f"[Random Forest]      R2: {r2_score(y_test, rf_pred)*100:.2f}% | MAE: {mean_absolute_error(y_test, rf_pred):.2f} kWh")

# 3. Keras Neural Regressor (For direct native Android TFLite deployment)
mean_X = np.mean(X_train, axis=0)
std_X = np.std(X_train, axis=0)

X_train_scaled = (X_train - mean_X) / std_X
X_test_scaled = (X_test - mean_X) / std_X

nn_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(6,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)
])

nn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.008), loss='mse', metrics=['mae'])
nn_model.fit(X_train_scaled, y_train, epochs=45, batch_size=32, verbose=0)

nn_pred = nn_model.predict(X_test_scaled, verbose=0).flatten()
print(f"[Neural Network]     R2: {r2_score(y_test, nn_pred)*100:.2f}% | MAE: {mean_absolute_error(y_test, nn_pred):.2f} kWh")

print("\n" + "="*60)
print("STEP 3: Exporting End-to-End TFLite Model (No External Scaling Required in Android)")
print("="*60)

class EmbeddedPredictor(tf.Module):
    def __init__(self, model, mean, std):
        super(EmbeddedPredictor, self).__init__()
        self.model = model
        self.mean = tf.constant(mean, dtype=tf.float32)
        self.std = tf.constant(std, dtype=tf.float32)

    @tf.function(input_signature=[tf.TensorSpec(shape=[None, 6], dtype=tf.float32)])
    def __call__(self, raw_input):
        normalized = (raw_input - self.mean) / self.std
        return self.model(normalized)

serving_mod = EmbeddedPredictor(nn_model, mean_X, std_X)
converter = tf.lite.TFLiteConverter.from_concrete_functions([serving_mod.__call__.get_concrete_function()])
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_bytes = converter.convert()

tflite_path = os.path.join(MODELS_DIR, "electricity_predictor.tflite")
with open(tflite_path, "wb") as f:
    f.write(tflite_bytes)

print(f"TensorFlow Lite file created: {tflite_path}")
print(f"Model Size: {os.path.getsize(tflite_path)/1024:.2f} KB (Optimized for Android!)")

# Verification inside TFLite
interpreter = tf.lite.Interpreter(model_path=tflite_path)
interpreter.allocate_tensors()
in_idx = interpreter.get_input_details()[0]['index']
out_idx = interpreter.get_output_details()[0]['index']

# Sample household test case:
# 4500 Watts (1 Inverter AC + Fridge + 4 Fans + Lights), 8 hours/day, 350 past month units, 340 past 3m avg, Summer (3), 5 members
test_case = np.array([[4500.0, 8.0, 350.0, 340.0, 3.0, 5.0]], dtype=np.float32)
interpreter.set_tensor(in_idx, test_case)
interpreter.invoke()
pred = interpreter.get_tensor(out_idx)[0][0]

print("\n" + "="*60)
print(f"VERIFICATION TEST RESULT:")
print(f"Household Profile: 4500W load, 8h/day run time, 350 kWh last month, Season: Summer, 5 People")
print(f"Predicted Next Month Consumption: {pred:.1f} kWh / Units")
print("="*60)

