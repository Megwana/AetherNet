from flask import Flask, jsonify, render_template, request
from flask_mqtt import Mqtt
import random
import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# ✅ Add MQTT Configuration Here
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883  # Instead of 8883
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_USERNAME'] = 'your_username'
app.config['MQTT_PASSWORD'] = 'your_password'
app.config['MQTT_KEEPALIVE'] = 60

mqtt = Mqtt(app)

def generate_fake_sensor_data():
    """Simulates Newcastle UK weather conditions dynamically with better formatting."""
    current_hour = datetime.datetime.now().hour
    current_month = datetime.datetime.now().month

    # Temperature variation (seasonal shifts + time of day)
    if current_month in [12, 1, 2]:  # Winter months
        temperature = round(random.uniform(1, 10), 1)
    elif current_month in [6, 7, 8]:  # Summer months
        temperature = round(random.uniform(15, 23), 1)
    else:  # Spring & Autumn
        temperature = round(random.uniform(8, 18), 1)

    if current_hour < 6 or current_hour > 18:  # Night-time cooling effect
        temperature = round(temperature - random.uniform(1, 3), 1)  # Keep rounding consistent

    # Humidity trends (higher at dawn/evening)
    humidity = round(random.uniform(75, 95), 1)
    if current_hour in [6, 18]:  # Peak humidity times
        humidity = round(humidity + random.uniform(3, 7), 1)

    # Rainfall probability (higher in winter/autumn)
    rain_probability = 0.3 if current_month in [6, 7, 8] else 0.7
    rainfall = random.random() < rain_probability

    # Tank water level fluctuation (affected by rainfall)
    tank_level = round(random.uniform(50, 100), 1)
    if rainfall:
        tank_level = round(tank_level + random.uniform(5, 15), 1)
        tank_level = min(tank_level, 100)

    # Simulated HVAC Load (higher demand in colder months)
    hvac_load = round(random.uniform(30, 80), 1)
    if current_month in [12, 1, 2]:  # Winter heating demand
        hvac_load = round(hvac_load + random.uniform(10, 20), 1)

    return {
        "temperature": temperature,  
        "humidity": humidity,        
        "rainfall": rainfall,
        "tank_level": tank_level,    
        "hvac_load": hvac_load,      
        "time": current_hour,
        "month": current_month
    }


def hvac_rainwater_logic(data):
    """Defines automated adjustments for HVAC & rainwater redirection."""
    if data["humidity"] > 70 and data["rainfall"]:
        action = "Reduce HVAC cooling & store rainwater"
    elif data["temperature"] < 10:  # Cold weather conditions
        action = "Increase heating for comfort"
    elif data["tank_level"] > 90:
        action = "Redirect excess rainwater to irrigation"
    else:
        action = "Maintain normal operations"
    return action

# Store override decisions
override_decision = None

@app.route('/')
def home():
    return render_template('index.html')  # Flask searches in 'templates/' folder

@app.route('/sensor-data')
def sensor_data_page():
    return render_template('sensor-data.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    data = generate_fake_sensor_data()
    global override_decision
    data["system_decision"] = override_decision if override_decision else hvac_rainwater_logic(data)
    return jsonify(data)

@app.route('/api/override', methods=['GET'])
def override_system():
    global override_decision
    decision = request.args.get('decision')

    if decision == "store":
        override_decision = "Force Rainwater Storage"
    elif decision == "redirect":
        override_decision = "Force Rainwater Redirection"
    else:
        override_decision = None  # Reset to default automation

    return jsonify({"new_decision": override_decision})

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """Handles connection to MQTT broker."""
    mqtt.subscribe('aesternet/sensor')

@mqtt.on_message()
def handle_message(client, userdata, message):
    """Processes MQTT data when received."""
    print(f"Received: {message.payload.decode()}")

@app.route('/api/mqtt-status')
def mqtt_status():
    return jsonify({"status": "Connected" if mqtt.is_connected else "Disconnected"})

def estimate_savings(data):
    """Estimates potential energy and water savings based on system optimization."""
    baseline_hvac_usage = 70  # Example: Assume HVAC uses 70 kWh per day
    optimized_hvac_usage = baseline_hvac_usage * (1 - 0.15)  # Assume 15% reduction

    baseline_water_waste = 100  # Example: Assume 100 liters wasted per day
    optimized_water_use = baseline_water_waste * (1 - 0.20)  # Assume 20% reduction

    return {
        "energy_savings_kwh": round(baseline_hvac_usage - optimized_hvac_usage, 2),
        "water_savings_liters": round(baseline_water_waste - optimized_water_use, 2),
        "efficiency_gain": f"{round(((baseline_hvac_usage - optimized_hvac_usage) / baseline_hvac_usage) * 100, 2)}%"
    }

@app.route('/api/savings')
def get_estimated_savings():
    """Returns estimated savings metrics."""
    fake_data = generate_fake_sensor_data()
    savings = estimate_savings(fake_data)
    return jsonify(savings)

@app.route('/settings')
def settings_page():
    return render_template('settings.html')
# Store user thresholds
user_thresholds = {"humidity": 70, "temperature": 10}

@app.route('/api/set-thresholds', methods=['POST'])
def set_thresholds():
    """Receives and stores user-defined thresholds."""
    global user_thresholds
    thresholds = request.json
    user_thresholds["humidity"] = int(thresholds["humidity"])
    user_thresholds["temperature"] = int(thresholds["temperature"])
    return jsonify({"status": "success", "updated_thresholds": user_thresholds})

def hvac_rainwater_logic(data):
    """Defines automated adjustments based on user thresholds."""
    if data["humidity"] > user_thresholds["humidity"] and data["rainfall"]:
        action = "Reduce HVAC cooling & store rainwater"
    elif data["temperature"] < user_thresholds["temperature"]: 
        action = "Increase heating for comfort"
    elif data["tank_level"] > 90:
        action = "Redirect excess rainwater to irrigation"
    else:
        action = "Maintain normal operations"
    return action

if __name__ == '__main__':
    app.run(debug=True)
