import json

import paho.mqtt.client as mqtt

payload = {
    'dispenser_id': 1,
    'distancia_cm': 10.5
}

mqtt_client = mqtt.Client(
    client_id='absortech_publisher',
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
mqtt_client.connect(host="localhost", port=1883)
mqtt_client.publish("SENSOR/ULTRASSOM", json.dumps(payload))
mqtt_client.disconnect()
