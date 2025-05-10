import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecurekey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MQTT_BROKER_URL = 'broker.hivemq.com'
    MQTT_BROKER_PORT = 1883
    MQTT_TLS_ENABLED = False
