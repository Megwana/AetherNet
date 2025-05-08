from flask import Flask, jsonify, render_template
import random
import datetime

app = Flask(__name__)

def generate_fake_sensor_data():
    """Simulates Newcastle UK weather conditions dynamically."""
    current_hour = datetime.datetime.now().hour
    current_month = datetime.datetime.now().month

    # Temperature variation (seasonal shifts + time of day)
    if current_month in [12, 1, 2]:  # Winter months
        temperature = round(random.uniform(1, 10), 2)
    elif current_month in [6, 7, 8]:  # Summer months
        temperature = round(random.uniform(15, 23), 2)
    else:  # Spring & Autumn
        temperature = round(random.uniform(8, 18), 2)

    if current_hour < 6 or current_hour > 18:  # Night-time cooling effect
        temperature -= random.uniform(1, 3)

    # Humidity trends (higher at dawn/evening)
    humidity = round(random.uniform(75, 95), 2)
    if current_hour in [6, 18]:  # Peak humidity times
        humidity += random.uniform(3, 7)

    # Rainfall probability (higher in winter/autumn)
    rain_probability = 0.3 if current_month in [6, 7, 8] else 0.7  # Less rain in summer
    rainfall = random.random() < rain_probability  # Simulated rain occurrence

    # Tank water level fluctuation (affected by rainfall)
    tank_level = round(random.uniform(50, 100), 2)
    if rainfall:
        tank_level += random.uniform(5, 15)  # Rainwater collection effect
        tank_level = min(tank_level, 100)  # Prevent overflow

    # Simulated HVAC Load (higher demand in colder months)
    hvac_load = round(random.uniform(30, 80), 2)
    if current_month in [12, 1, 2]:  # Winter heating demand
        hvac_load += random.uniform(10, 20)

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
    if data["humidity"] > 70 and data["rainfall"]:
        action = "Reduce HVAC cooling & store rainwater"
    elif data["temperature"] < 10:  # Cold weather conditions
        action = "Increase heating for comfort"
    elif data["tank_level"] > 90:
        action = "Redirect excess rainwater to irrigation"
    else:
        action = "Maintain normal operations"
    return action

rainfall_history = []

def predict_tank_overflow(data):
    global rainfall_history
    rainfall_history.append(data["rainfall"])

    # Simple prediction: If consecutive rain days exceed 3, assume overflow risk
    if sum(rainfall_history[-3:]) > 2 and data["tank_level"] > 85:
        return "High risk of overflow! Redirect rainwater preemptively."
    return "Normal water storage operation."

@app.route('/')
def home():
    return render_template('index.html')  # Flask searches in 'templates/' folder

@app.route('/sensor-data')
def get_sensor_data():
    """Returns dynamically generated Newcastle weather-based sensor data."""
    data = generate_fake_sensor_data()
    data["system_decision"] = hvac_rainwater_logic(data)  # Apply automation logic
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
