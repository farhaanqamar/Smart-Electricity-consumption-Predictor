# 📱 Android-Based Smart Electricity Consumption Predictor
> **CS619 Final Year Project (FYP) — Complete Technical Deliverable**  
> **Student:** Farhan | **Supervisor:** Muhammad Imran Afzal  
> **Location:** `G:\farhan_fyp\`

---

## 🏛️ Project Architecture Overview

This project is an **end-to-end Machine Learning-powered Android application** designed to predict household electricity consumption, calculate slab-wise bills under DISCO/K-Electric tariff rules, and provide intelligent, actionable energy-saving recommendations.

```
G:\farhan_fyp\
├── ml_model/                                  ← Python & PyCharm ML Engine
│   ├── dataset/
│   │   └── household_energy_consumption.csv   ← 10,000 Household Dataset
│   ├── models/
│   │   └── electricity_predictor.tflite       ← Trained & Exported TensorFlow Lite Model
│   ├── train_electricity_model.py             ← PyCharm Runnable Model Training & Benchmark
│   ├── train_and_export.py                    ← Core ML Pipeline Script
│   └── README_PYCHARM.md                      ← Step-by-Step PyCharm Execution Guide
│
└── android_app/
    └── ElectricityPredictor/                  ← Native Android Studio Project (Kotlin)
        ├── build.gradle                       ← Project Build Script
        ├── settings.gradle                    ← Multi-repo & JitPack Config
        ├── gradle.properties                  ← Memory Optimization Flags
        └── app/
            ├── build.gradle                   ← Room, TFLite, MPAndroidChart Dependencies
            ├── proguard-rules.pro             ← Production Proguard Config
            └── src/main/
                ├── AndroidManifest.xml        ← App Declarations & Permissions
                ├── assets/
                │   └── electricity_predictor.tflite ← Embedded On-Device Inference Model
                ├── java/com/farhan/electricitypredictor/
                │   ├── ElectricityPredictorApp.kt   ← Application Lifecycle & Room Initializer
                │   ├── data/
                │   │   ├── local/
                │   │   │   ├── AppDatabase.kt       ← Room DB with Prepopulated Appliances
                │   │   │   ├── dao/ApplianceDao.kt
                │   │   │   ├── dao/HistoricalBillDao.kt
                │   │   │   └── entity/ApplianceEntity.kt
                │   │   │   └── entity/HistoricalBillEntity.kt
                │   │   └── model/RecommendationItem.kt
                │   ├── ml/
                │   │   └── ElectricityPredictorClient.kt ← On-Device Edge TFLite Client
                │   ├── tariff/
                │   │   └── ElectricityTariffEngine.kt   ← Pakistani Slabs & Taxes Calculator
                │   └── ui/
                │       ├── splash/SplashActivity.kt
                │       ├── auth/LoginActivity.kt
                │       ├── auth/RegisterActivity.kt
                │       ├── dashboard/DashboardActivity.kt
                │       ├── appliances/AppliancesActivity.kt
                │       ├── appliances/ApplianceAdapter.kt
                │       ├── history/HistoryActivity.kt
                │       ├── history/HistoricalBillAdapter.kt
                │       └── recommendations/RecommendationsActivity.kt
                │       └── recommendations/RecommendationAdapter.kt
                └── res/
                    ├── layout/ (activity_dashboard, activity_appliances, activity_history, etc.)
                    ├── drawable/ (ic_bolt, ic_power, ic_analytics, ic_tips, gradients, etc.)
                    └── values/ (colors, strings, themes)
```

---

## ⚡ Machine Learning Benchmark Results

Both algorithms requested in the project specification were trained, validated, and benchmarked:

| Model | $R^2$ Accuracy | Mean Absolute Error (MAE) | Status |
|---|---|---|---|
| **Linear Regression** | **98.65%** | 47.53 kWh | Evaluated |
| **Random Forest Regressor** | **99.57%** | 26.52 kWh | High-Performance Benchmark |
| **Embedded Neural Regressor (TFLite)** | **99.53%** | 24.78 kWh | **Active in Android App** |

---

## 🚀 How to Run in PyCharm
1. Open PyCharm.
2. Click **Open** and select: `G:\farhan_fyp\ml_model`.
3. Right-click on **`train_electricity_model.py`** and select **Run 'train_electricity_model'**.
4. The script executes the entire pipeline, trains the models, and updates `electricity_predictor.tflite`.

---

## 📱 How to Run in Android Studio
1. Open Android Studio.
2. Select **Open** and choose: `G:\farhan_fyp\android_app\ElectricityPredictor`.
3. Let Gradle sync automatically (Dependencies: Room Database, TensorFlow Lite, MPAndroidChart).
4. Run on any Android device or Emulator (API 24+ / Android 7.0 to Android 14+).

---

## 🎨 Design Philosophy
* Built strictly according to the **K-Electric Live App** design reference.
* Custom warm sunset gradients (`#FF5722` to `#FF8F00`), clean rounded card surfaces (`20dp` - `24dp` radii), live grid status indicators, and professional vector icons (zero emojis).

