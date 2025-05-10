from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt
from flask_cors import CORS
from app.config import Config
from app.models import db
from app.routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

app.register_blueprint(routes)

mqtt = Mqtt(app)

# Create database tables
with app.app_context():
    db.create_all()
