from flask import Blueprint, request, jsonify, render_template, url_for
from app.models import db, User
from app.models import db, SensorData, OverrideDecision
from app.utils import load_json, save_json

routes = Blueprint('routes', __name__)

@routes.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    data = load_json("thresholds.json")
    return jsonify(data)

@routes.route('/api/override', methods=['GET'])
def override_system():
    decision = request.args.get('decision')
    override = OverrideDecision.query.first()
    override.decision = decision
    db.session.commit()
    return jsonify({"new_decision": decision})

@routes.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@routes.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({"message": "Login successful", "user": user.username}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@routes.route('/')
def home():
    return render_template("index.html", base_url="/static")

@routes.route('/login')
def login_page():
    return render_template("login.html")
