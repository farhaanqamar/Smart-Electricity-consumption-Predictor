import os
import json
import re
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
import tensorflow as tf
from generate_ke_bill_pdf import generate_ke_bill_pdf

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

BASE_DIR = r"G:\farhan_fyp"
TFLITE_MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "models", "electricity_predictor.tflite")

# Load TFLite Model
interpreter = None
try:
    interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("[✓] TFLite Model loaded successfully into VOLTIFY Simulator!")
except Exception as e:
    print(f"[!] Warning: TFLite model load error: {e}")

# In-Memory State initialized with pre-populated realistic data
appliances = [
    {"id": 1, "name": "1.5 Ton Inverter AC", "watts": 1800.0, "hours": 8.0, "qty": 1, "category": "Cooling"},
    {"id": 2, "name": "Refrigerator (Medium)", "watts": 300.0, "hours": 24.0, "qty": 1, "category": "Kitchen"},
    {"id": 3, "name": "Ceiling Fans", "watts": 80.0, "hours": 12.0, "qty": 4, "category": "General"},
    {"id": 4, "name": "LED Energy Saver Lights", "watts": 18.0, "hours": 7.0, "qty": 8, "category": "Lighting"},
    {"id": 5, "name": "Water Pump / Motor (1 HP)", "watts": 750.0, "hours": 1.5, "qty": 1, "category": "Heavy Load"},
    {"id": 6, "name": "Electric Iron", "watts": 1000.0, "hours": 0.8, "qty": 1, "category": "General"},
    {"id": 7, "name": "Smart LED TV (50-inch)", "watts": 120.0, "hours": 5.0, "qty": 1, "category": "Entertainment"},
    {"id": 8, "name": "Washing Machine", "watts": 500.0, "hours": 1.0, "qty": 1, "category": "General"}
]

historical_bills = [
    {"id": 1, "month": "July 2025", "units": 172.0, "bill": 2071.0},
    {"id": 2, "month": "June 2025", "units": 173.0, "bill": 2150.0},
    {"id": 3, "month": "May 2025", "units": 195.0, "bill": 2680.0},
    {"id": 4, "month": "April 2025", "units": 195.0, "bill": 2680.0},
    {"id": 5, "month": "March 2025", "units": 162.0, "bill": 1890.0},
    {"id": 6, "month": "February 2025", "units": 94.0, "bill": 1150.0},
    {"id": 7, "month": "January 2025", "units": 48.0, "bill": 720.0},
    {"id": 8, "month": "December 2024", "units": 83.0, "bill": 980.0},
    {"id": 9, "month": "November 2024", "units": 159.0, "bill": 1820.0},
    {"id": 10, "month": "October 2024", "units": 175.0, "bill": 2100.0},
    {"id": 11, "month": "September 2024", "units": 184.0, "bill": 2340.0},
    {"id": 12, "month": "August 2024", "units": 190.0, "bill": 2450.0},
    {"id": 13, "month": "July 2024", "units": 187.0, "bill": 2390.0}
]

ke_consumer_data = {
    "account_no": "1234567890123",
    "consumer_no": "AB123124",
    "customer_name": "MR. ABDULLAH KHAN",
    "tariff": "A1-R Residential",
    "status": "PAID • STAR Consumer",
    "bill_month": "Jul-25",
    "issue_date": "28-Jul-2025",
    "due_date": "11-Aug-2025",
    "current_units": 172.0,
    "amount_due": 2071.0,
    "amount_after_due": 2157.0,
    "variable_charges": 1093.56,
    "additional_surcharge": 58.82,
    "electricity_duty": 25.69,
    "sales_tax": 73.96
}

def calculate_pakistan_bill(units):
    if units <= 100:
        slab = "Lifeline / Protected (0 - 100 Units)"
        base_cost = units * 16.50
    elif units <= 200:
        slab = "Protected (101 - 200 Units)"
        base_cost = (100 * 16.50) + ((units - 100) * 22.95)
    elif units <= 300:
        slab = "Non-Protected (201 - 300 Units)"
        base_cost = (100 * 16.50) + (100 * 22.95) + ((units - 200) * 34.25)
    elif units <= 700:
        slab = "Medium Load (301 - 700 Units)"
        base_cost = (100 * 16.50) + (100 * 22.95) + (100 * 34.25) + ((units - 300) * 42.80)
    else:
        slab = "High Consumption (> 700 Units)"
        base_cost = (100 * 16.50) + (100 * 22.95) + (100 * 34.25) + (400 * 42.80) + ((units - 700) * 48.50)

    fpa = units * 4.50
    taxes = (base_cost + fpa) * 0.18
    total = base_cost + fpa + taxes

    return {
        "units": round(units, 1),
        "base_cost": round(base_cost, 0),
        "fpa": round(fpa, 0),
        "taxes": round(taxes, 0),
        "total_bill": round(total, 0),
        "slab_name": slab
    }

def run_prediction(total_watts, avg_hours, last_units, past_3m_avg):
    if interpreter is not None:
        try:
            inp = np.array([[float(total_watts), float(avg_hours), float(last_units), float(past_3m_avg), 3.0, 5.0]], dtype=np.float32)
            interpreter.set_tensor(input_details[0]['index'], inp)
            interpreter.invoke()
            pred = float(interpreter.get_tensor(output_details[0]['index'])[0][0])
            if pred > 0:
                return round(pred, 1)
        except Exception as e:
            print(f"Prediction error: {e}")

    calc = (total_watts * avg_hours * 0.40 * 30.0) / 1000.0
    return round((calc * 0.55) + (last_units * 0.45), 1)

def get_current_metrics():
    total_watts = sum(a['watts'] * a['qty'] for a in appliances)
    total_weighted_hours = sum(a['hours'] * (a['watts'] * a['qty']) for a in appliances)
    avg_hours = (total_weighted_hours / total_watts) if total_watts > 0 else 6.0
    total_items = sum(a['qty'] for a in appliances)

    last_month_units = historical_bills[0]['units'] if historical_bills else 172.0
    past_3m_avg = sum(b['units'] for b in historical_bills[:3]) / len(historical_bills[:3]) if historical_bills else 180.0

    predicted_units = run_prediction(total_watts, avg_hours, last_month_units, past_3m_avg)
    breakdown = calculate_pakistan_bill(predicted_units)

    return {
        "total_watts": total_watts,
        "avg_hours": round(avg_hours, 1),
        "total_items": total_items,
        "last_month_units": last_month_units,
        "past_3m_avg": round(past_3m_avg, 1),
        "predicted_units": predicted_units,
        "breakdown": breakdown,
        "consumer": ke_consumer_data
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({
        "metrics": get_current_metrics(),
        "appliances": appliances,
        "historical_bills": historical_bills,
        "consumer": ke_consumer_data
    })

@app.route("/api/ke/fetch-bill", methods=["POST"])
def fetch_ke_bill():
    data = request.json or {}
    account_no = data.get("account_no", "1234567890123").strip()
    global ke_consumer_data
    ke_consumer_data["account_no"] = account_no if len(account_no) >= 10 else "1234567890123"
    return jsonify({
        "success": True,
        "bill": ke_consumer_data,
        "history_13_months": historical_bills,
        "metrics": get_current_metrics()
    })

@app.route("/api/ke/download-bill-pdf", methods=["GET"])
def download_bill_pdf():
    """Generates and serves printable K-Electric Bill PDF"""
    pdf_path = os.path.join(app.static_folder, "ke_official_bill.pdf")
    generate_ke_bill_pdf(pdf_path, ke_consumer_data)
    return send_file(pdf_path, as_attachment=True, download_name="K_Electric_Official_Bill.pdf")

@app.route("/api/ocr/scan-sticker", methods=["POST"])
def scan_sticker():
    data = request.json or {}
    sample_type = data.get("preset", "ac").lower()
    raw_text = data.get("raw_text", "")

    watts = None
    volts = 220.0
    amps = None

    if raw_text:
        w_match = re.search(r'(\d+)\s*(?:W|Watts|Watt)', raw_text, re.IGNORECASE)
        v_match = re.search(r'(\d+)\s*(?:V|Volts|Volt)', raw_text, re.IGNORECASE)
        a_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:A|Amps|Amp)', raw_text, re.IGNORECASE)

        if w_match: watts = float(w_match.group(1))
        if v_match: volts = float(v_match.group(1))
        if a_match: amps = float(a_match.group(1))

        if watts is None and amps is not None and volts is not None:
            watts = round(volts * amps, 0)

    presets = {
        "ac": {"name": "Inverter Split AC 1.5 Ton", "watts": 1850.0, "volts": 220.0, "amps": 8.4, "category": "Cooling"},
        "refrigerator": {"name": "Dawlance Inverter Refrigerator", "watts": 280.0, "volts": 230.0, "amps": 1.2, "category": "Kitchen"},
        "microwave": {"name": "Microwave Oven with Grill", "watts": 1200.0, "volts": 230.0, "amps": 5.2, "category": "Kitchen"},
        "pump": {"name": "Water Pump / Motor (1 HP)", "watts": 750.0, "volts": 220.0, "amps": 3.5, "category": "Heavy Load"},
        "iron": {"name": "Automatic Electric Iron", "watts": 1000.0, "volts": 220.0, "amps": 4.5, "category": "General"}
    }

    result = presets.get(sample_type, presets["ac"])
    if watts is not None:
        result["watts"] = watts
        if volts: result["volts"] = volts

    return jsonify({
        "success": True,
        "detected_name": result["name"],
        "detected_watts": result["watts"],
        "detected_volts": result["volts"],
        "category": result["category"],
        "confidence": "98.4%",
        "sticker_snippet": f"VOLTAGE: {result['volts']}V • RATED POWER: {result['watts']}W"
    })

@app.route("/api/appliances", methods=["POST"])
def add_appliance():
    data = request.json
    new_id = max([a['id'] for a in appliances], default=0) + 1
    new_app = {
        "id": new_id,
        "name": data.get("name", "New Appliance"),
        "watts": float(data.get("watts", 100)),
        "hours": float(data.get("hours", 4)),
        "qty": int(data.get("qty", 1)),
        "category": data.get("category", "General")
    }
    appliances.append(new_app)
    return jsonify({"success": True, "appliance": new_app, "metrics": get_current_metrics()})

@app.route("/api/appliances/<int:item_id>", methods=["DELETE"])
def delete_appliance(item_id):
    global appliances
    appliances = [a for a in appliances if a['id'] != item_id]
    return jsonify({"success": True, "metrics": get_current_metrics()})

@app.route("/api/history", methods=["POST"])
def add_history():
    data = request.json
    new_id = max([b['id'] for b in historical_bills], default=0) + 1
    new_bill = {
        "id": new_id,
        "month": data.get("month", "Month 2026"),
        "units": float(data.get("units", 300)),
        "bill": float(data.get("bill", 15000))
    }
    historical_bills.insert(0, new_bill)
    return jsonify({"success": True, "bill": new_bill, "metrics": get_current_metrics()})

@app.route("/api/history/<int:bill_id>", methods=["DELETE"])
def delete_history(bill_id):
    global historical_bills
    historical_bills = [b for b in historical_bills if b['id'] != bill_id]
    return jsonify({"success": True, "metrics": get_current_metrics()})

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 VOLTIFY Live Simulator running on:")
    print("👉 http://127.0.0.1:5050")
    print("="*60 + "\n")
    app.run(host="127.0.0.1", port=5050, debug=False)
