from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt
from flask_cors import CORS
from app.config import Config
from app.models import db
from app.routes import routes

# Explicitly set static and template folders
app = Flask(__name__, static_folder='static', template_folder='templates')
# Load app config
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

# Register the routes blueprint
app.register_blueprint(routes)

# Initialize MQTT
mqtt = Mqtt(app)

# Create database tables
with app.app_context():
    db.create_all()
