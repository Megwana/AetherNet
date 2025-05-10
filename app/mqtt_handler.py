from flask_mqtt import Mqtt

mqtt = Mqtt()

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('aesternet/sensor')
    print("[MQTT] Connected and subscribed.")

@mqtt.on_message()
def handle_message(client, userdata, message):
    print("[MQTT] Received:", message.payload.decode())
