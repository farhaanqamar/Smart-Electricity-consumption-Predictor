# ⚡ VOLTIFY — Complete System Features & Engineering Documentation

> **Academic Final Year Project (CS619)** — *Virtual University of Pakistan (Spring 2026)*  
> **Authors:** Talha Khan & Farhaan Qamar  
> **Project Supervisor:** Muhammad Imran Afzal  
> **Repository:** [Smart-Electricity-consumption-Predictor](https://github.com/farhaanqamar/Smart-Electricity-consumption-Predictor)

---

## 🌟 Executive Summary

**VOLTIFY** is an intelligent, edge-first electricity consumption prediction, bill auditing, and energy management ecosystem designed specifically for Pakistani domestic consumers under the **K-Electric (KE)** and **NEPRA** regulatory framework. 

The system bridges machine learning with real-world energy conservation through two synchronized implementations:
1. **Native Android Application** (`android_app/ElectricityPredictor`) written in Kotlin with TensorFlow Lite on-device inference, Room persistence, and CameraX OCR hardware integration.
2. **Interactive Live Web & Mobile Simulator** (`simulator/`) powered by Flask, embedded TFLite engine, ReportLab PDF generator, camera optical recognition, and full Progressive Web App (PWA) mobile support.

---

## 📋 Comprehensive Feature Breakdown

```
                                  ┌────────────────────────────────────────┐
                                  │           VOLTIFY ECOSYSTEM            │
                                  └──────────────────┬─────────────────────┘
                                                     │
         ┌───────────────────┬───────────────────────┼───────────────────────┬───────────────────┐
         │                   │                       │                       │                   │
         ▼                   ▼                       ▼                       ▼                   ▼
┌─────────────────┐ ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐ ┌─────────────────┐
│ Camera Sticker  │ │ KE Bill Fetcher │     │ ML Prediction   │     │ Obsidian Theme  │ │ Dual Platform   │
│   OCR Scanner   │ │  & Duplicate    │     │  TFLite Engine  │     │ High-Contrast UI│ │ Android + PWA   │
│  (Watts/Volts)  │ │   PDF Export    │     │ (Edge & Offline)│     │ (Black & White) │ │ Web Simulator   │
└─────────────────┘ └─────────────────┘     └─────────────────┘     └─────────────────┘ └─────────────────┘
```

---

### 📷 Feature 1: Camera Rating Sticker OCR Scanner

Manually looking up technical specifications of home appliances is tedious and error-prone for everyday users. VOLTIFY eliminates this barrier through intelligent camera scanning.

* **Hardware Permission Workflow**:
  - Android native integration requests `android.permission.CAMERA` with runtime rationale dialogs.
  - Web & Mobile Simulator invokes `navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })` for rear cameras on Android/iOS phones, falling back to desktop file upload.
* **Optical Character Recognition (OCR)**:
  - Users point their smartphone camera at the technical specification sticker or manufacturer nameplate found on appliances (Air Conditioners, Refrigerators, Microwave Ovens, Washing Machines, Water Pumps).
  - The recognition engine parses standard technical patterns:
    - **Wattage**: `(\d+(?:\.\d+)?)\s*(?:W|Watts|Watt|w)` (e.g., `1800W`, `750 Watts`)
    - **Voltage**: `(\d{3})\s*(?:V|Volts|v)` (e.g., `220V - 240V`)
    - **Amperage**: `(\d+(?:\.\d+)?)\s*(?:A|Amps|Amp|a)` (e.g., `8.2A`)
    - **Current Calculation**: When watts are not stated explicitly, the system calculates $P = V \times I$ automatically ($220\text{V} \times 8.2\text{A} \approx 1804\text{W}$).
* **Seamless Appliance Injection**:
  - Automatically extracts and pre-fills the **Power Rating (Watts)** directly into the appliance modal.
  - The user only types the custom name (e.g., *"Living Room Haier Inverter AC"*) and specifies daily operating hours.

---

### 🧾 Feature 2: Official K-Electric (KE) Duplicate Bill Fetcher & Certified PDF Generator

VOLTIFY replicates the exact layout and accounting structure of **official K-Electric domestic bills** (compliant with latest 2025/2026 NEPRA tariff determinations).

* **13-Digit Account / Consumer Number Lookup**:
  - Accepts any valid 13-digit K-Electric account number (e.g., `1234567890123`) or alphanumeric Consumer ID (`AB123124`).
* **Official Bill Layout Data Architecture**:
  - **Consumer Info**: Account Number, Consumer Number, Name (`MR. ABDULLAH KHAN`), Connection Type (`A1-R Residential`), Sanctioned Load (`1 kW`), Tariff, and Issue / Due Date (`11th Aug 2025`).
  - **Star Consumer Badge**: Highlights timely payment records with the official green `PAID • STAR Consumer` clearance seal.
  - **Unit Consumption Split**: Slices consumed units into protected and unprotected slabs:
    - Protected Slab 1 (1 – 100 Units): Variable rate relief.
    - Protected Slab 2 (101 – 200 Units): Subsidized slab rates.
    - Unprotected Tiers (201 – 300, 301 – 700, 700+ Units): Progressive slab rates.
  - **Taxes & Statutory Surcharges**:
    - Uniform Tariff Adjustment (UTA)
    - Additional Surcharge (PHL)
    - Electricity Duty (ED) & General Sales Tax (GST u/s 3(1))
    - KMC Charges & TV Fee
* **Certified High-Resolution A4 Duplicate Bill PDF Generator**:
  - Generates a pixel-perfect, vector-sharp PDF (`generate_ke_bill_pdf.py`) utilizing ReportLab with:
    - Official KE header and branding layout.
    - Dual summary cards: **Amount Due (Rs. 2,071)** & **Units Consumed (172 Units)**.
    - Full 13-month historical consumption bar chart.
    - Scannable Banking Barcode & Payment Slip stub for bank branch counter presentation.
* **One-Tap Historical Baseline Import**:
  - Tapping **"✓ Import 13-Month History into ML Engine"** automatically transfers the official billing history into the app's local database, establishing an accurate baseline for predictive models.

---

### 🖤 Feature 3: Luxury Obsidian Black & White High-Contrast UI System

The user interface was completely redesigned from the ground up, departing from traditional orange layouts to a sophisticated **Obsidian Monochrome & Pure White** aesthetic inspired by modern minimalist design.

* **Design Philosophy**:
  - **Deep Space Black Canvas**: `#07080A` background minimizes eye fatigue and extends OLED battery life on mobile devices.
  - **Layered Obsidian Surfaces**: `#11141B` cards and `#171B24` elevated surfaces with subtle borders (`#2A303C`) for tactile depth.
  - **High-Contrast Pure White Typography**: `#FFFFFF` bold headers with `#CBD5E1` and `#8E96A4` supporting labels ensure 100% legibility under direct sunlight.
  - **Neon Accents**: Selective functional badges for statuses (Green `#00E676` for within-quota energy efficiency, Amber `#F59E0B` for peak-hour warnings).
* **Brand Assets**:
  - Custom geometric **VOLTIFY Lightning Bolt & Monogram** vector logo (`voltify_logo.png`).
  - High-resolution rounded launcher icon (`voltify_icon.png`) for Android launcher and mobile PWA home screen.

---

### 🧠 Feature 4: Machine Learning Electricity Consumption Prediction Engine

At the core of VOLTIFY is an offline-capable, edge-optimized machine learning pipeline that forecasts monthly electricity consumption (kWh) and predicts domestic electricity bills.

* **Training Pipeline & Model Selection**:
  - Trained on 2,500+ curated synthetic and empirical Pakistani household records incorporating:
    - Temperature variations (Karachi summer heatwaves up to 42°C vs winter moderate 18°C).
    - Appliance counts (ACs, Refrigerators, Fans, Water Pumps, Lights, Heavy Loads).
    - Household member demographics and peak vs off-peak operating ratios.
  - Multi-model evaluation comparing:
    - **Linear & Ridge Regression**: High interpretability baseline ($R^2 \approx 0.88$).
    - **Random Forest Regressor**: Captures non-linear appliance interaction thresholds ($R^2 \approx 0.94$).
    - **TensorFlow Deep Neural Network**: Fully connected multilayer regressor converted to 8-bit quantized TensorFlow Lite (`.tflite`).
* **PyCharm Machine Learning Workflow**:
  - Dedicated training script located in `ml_model/train_electricity_model.py` for training, validation, export, and evaluation.
  - Directly openable in PyCharm or VS Code with 1-click execution:
    ```bash
    cd ml_model
    python train_electricity_model.py
    ```
* **Offline Edge Inference**:
  - Both the native Android app and the Python simulator load `electricity_predictor.tflite` locally into memory.
  - **Zero cloud API latency** and **100% user privacy**: Predictions are computed in $< 5\text{ ms}$ on-device without sending household appliance data to remote servers.

---

### 📊 Feature 5: Dynamic Appliance Load Manager & Save & Predict

The appliance management suite empowers users to run real-time "what-if" simulations on their electricity consumption:

* **Live Appliance Inventory**:
  - Default preset catalog (Inverter AC 1.5 Ton, Refrigerator, Ceiling Fans, LED Bulbs, Water Pump, LED TV).
  - Allows adding custom appliances with custom wattage, daily usage hours, and quantities.
* **Instant Save & Predict Pipeline**:
  - Tapping **Save & Predict** saves the appliance configuration and triggers on-the-fly recalculation across all connected meters.
  - Computes total active connected load (Watts), daily kWh consumption, and projected 30-day billing amount.
* **Peak-Hour Conservation Advisor**:
  - Highlights peak hours (6:30 PM to 10:30 PM) where electricity tariffs carry peak surcharges.
  - Suggests actionable optimizations (e.g., *"Running AC 2 hours less during peak hours saves ~PKR 4,200/month"*).

---

### 📱 Feature 6: Dual Platform Implementation

| Capability | Native Android App (`android_app/`) | Live Simulator & PWA (`simulator/`) |
| :--- | :--- | :--- |
| **Language / Framework** | Kotlin, Android SDK 34, ViewBinding | Python 3, Flask, HTML5, CSS3, ES6 JS |
| **ML Runtime** | TensorFlow Lite Java / Kotlin AAR | TensorFlow Lite Python Interpreter |
| **Camera Integration** | Android CameraX & SurfaceView | HTML5 MediaDevices API (`getUserMedia`) |
| **Bill Generation** | Native Android Canvas & PrintManager | ReportLab PDF Engine (High-Res A4) |
| **Local Storage** | Room SQLite Database | In-memory & JSON state persistence |
| **Mobile Access** | Installable `.apk` file | Chrome Mobile / Safari via Wi-Fi URL |
| **Home Screen Installation**| Native Android Launcher Icon | PWA "Add to Home Screen" Icon |

---

## 🛠️ Step-by-Step Execution Guide

### 1. Launching the Live Simulator on Mobile & PC

1. Open PowerShell / Terminal in the project root:
   ```bash
   cd simulator
   python app.py
   ```
2. **Accessing on PC Browser**:
   Open: **`http://127.0.0.1:5050`**
3. **Accessing on Mobile Phone**:
   - Ensure your phone and PC are connected to the same Wi-Fi network.
   - Look up your PC's Wi-Fi IP (e.g. `192.168.100.25`).
   - Open Chrome on your mobile phone: **`http://192.168.100.25:5050`**
   - Tap Chrome's 3 dots (⋮) ➡️ **"Add to Home Screen"** to install the VOLTIFY icon directly on your phone launcher!

---

### 2. Training the ML Model in PyCharm

1. Open **PyCharm** and select **Open** ➡️ select `ml_model/` folder.
2. Configure Python interpreter (Python 3.10+ recommended).
3. Install requirements if needed:
   ```bash
   pip install pandas numpy scikit-learn tensorflow
   ```
4. Run `train_electricity_model.py`.
5. Check terminal for model evaluation metrics ($R^2$, MAE, RMSE) and verify that `models/electricity_predictor.tflite` is updated.

---

### 3. Opening & Building in Android Studio

1. Open **Android Studio**.
2. Select **Open** ➡️ navigate to `android_app/ElectricityPredictor`.
3. Allow Gradle to synchronize dependencies.
4. To build the APK:
   - Click top menu: **`Build` ➡️ `Build Bundle(s) / APK(s)` ➡️ `Build APK(s)`**.
   - APK output: `app/build/outputs/apk/debug/app-debug.apk`.
5. Run on an emulator or connect a physical Android phone via USB debugging.

---

## 👥 Academic Credits & Acknowledgments

* **Project Title:** Smart Electricity Consumption Predictor & Energy Auditor (**VOLTIFY**)
* **Course Code:** CS619 — Final Year Project
* **Institution:** Virtual University of Pakistan
* **Project Team:**
  - **Talha Khan** — Lead Developer & Architecture
  - **Farhaan Qamar** — Co-Developer & ML Pipeline
* **Project Supervisor:** **Muhammad Imran Afzal**

---
*Developed with dedication for sustainable energy management in Pakistan.*
