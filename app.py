import os
import json
import random
import datetime
from flask import Flask, jsonify, render_template, request
from flask_mqtt import Mqtt
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)
CORS(app)

# MQTT Configuration (secure)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME')
app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD')
app.config['MQTT_KEEPALIVE'] = 60

mqtt = Mqtt(app)

# Data Storage Paths
THRESHOLD_FILE = 'thresholds.json'
OVERRIDE_FILE = 'override.json'

# Ensure files exist
for f, default in [(THRESHOLD_FILE, {"humidity": 70, "temperature": 10}),
                   (OVERRIDE_FILE, {"decision": None})]:
    if not os.path.exists(f):
        with open(f, 'w') as file:
            json.dump(default, file)

# ------------------ Utility Functions ------------------

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def get_thresholds():
    return load_json(THRESHOLD_FILE)

def get_override():
    return load_json(OVERRIDE_FILE).get("decision")

def set_override(value):
    save_json(OVERRIDE_FILE, {"decision": value})

def generate_fake_sensor_data():
    """Simulates realistic weather data for testing purposes."""
    now = datetime.datetime.now()
    hour, month = now.hour, now.month

    temperature = round(random.uniform(1, 10), 1) if month in [12, 1, 2] else \
                  round(random.uniform(15, 23), 1) if month in [6, 7, 8] else \
                  round(random.uniform(8, 18), 1)
    if hour < 6 or hour > 18:
        temperature -= round(random.uniform(1, 3), 1)

    humidity = round(random.uniform(75, 95), 1)
    if hour in [6, 18]:
        humidity += round(random.uniform(3, 7), 1)

    rainfall = random.random() < (0.3 if month in [6, 7, 8] else 0.7)
    tank_level = round(random.uniform(50, 100), 1)
    if rainfall:
        tank_level = min(tank_level + round(random.uniform(5, 15), 1), 100)

    hvac_load = round(random.uniform(30, 80), 1)
    if month in [12, 1, 2]:
        hvac_load += round(random.uniform(10, 20), 1)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "tank_level": tank_level,
        "hvac_load": hvac_load,
        "time": hour,
        "month": month
    }

def evaluate_logic(data):
    thresholds = get_thresholds()
    if data["humidity"] > thresholds["humidity"] and data["rainfall"]:
        return "Reduce HVAC cooling & store rainwater"
    elif data["temperature"] < thresholds["temperature"]:
        return "Increase heating for comfort"
    elif data["tank_level"] > 90:
        return "Redirect excess rainwater to irrigation"
    return "Maintain normal operations"

def estimate_savings(data):
    """Estimates potential HVAC/water savings."""
    baseline_hvac = 70
    optimized_hvac = baseline_hvac * 0.85
    baseline_water = 100
    optimized_water = baseline_water * 0.8

    return {
        "energy_savings_kwh": round(baseline_hvac - optimized_hvac, 2),
        "water_savings_liters": round(baseline_water - optimized_water, 2),
        "efficiency_gain": f"{round((1 - (optimized_hvac / baseline_hvac)) * 100, 2)}%"
    }

# ------------------ MQTT ------------------

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('aesternet/sensor')
    print("[MQTT] Connected and subscribed to topic.")

@mqtt.on_message()
def handle_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        print("[MQTT] Received:", payload)
        # Future: You could validate/store/process this MQTT data here
    except Exception as e:
        print("[MQTT] Failed to parse payload:", e)

# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sensor-data')
def sensor_data_page():
    return render_template('sensor-data.html')

@app.route('/settings')
def settings_page():
    return render_template('settings.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    try:
        data = generate_fake_sensor_data()
        override = get_override()
        data["system_decision"] = override or evaluate_logic(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Failed to generate data", "details": str(e)}), 500

@app.route('/api/override', methods=['GET'])
def override_system():
    decision = request.args.get('decision')
    decision_map = {
        "store": "Force Rainwater Storage",
        "redirect": "Force Rainwater Redirection",
        "clear": None
    }

    if decision not in decision_map:
        return jsonify({"error": "Invalid override option"}), 400

    set_override(decision_map[decision])
    return jsonify({"new_decision": decision_map[decision]})

@app.route('/api/set-thresholds', methods=['POST'])
def set_thresholds():
    try:
        data = request.json
        humidity = int(data.get("humidity"))
        temperature = int(data.get("temperature"))
        save_json(THRESHOLD_FILE, {"humidity": humidity, "temperature": temperature})
        return jsonify({"status": "success", "updated_thresholds": get_thresholds()})
    except Exception as e:
        return jsonify({"error": "Invalid input", "details": str(e)}), 400

@app.route('/api/savings')
def get_savings():
    try:
        data = generate_fake_sensor_data()
        return jsonify(estimate_savings(data))
    except Exception as e:
        return jsonify({"error": "Could not calculate savings", "details": str(e)}), 500

@app.route('/api/mqtt-status')
def mqtt_status():
    return jsonify({"status": "Connected" if mqtt.is_connected else "Disconnected"})

# ------------------ Entry ------------------

if __name__ == '__main__':
    app.run(debug=True)
