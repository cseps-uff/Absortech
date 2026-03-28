import os

mqtt_broker_configs = {
    'HOST': os.getenv('MQTT_HOST', 'localhost'),
    'PORT': int(os.getenv('MQTT_PORT', 1883)),
    'CLIENT_NAME': "absortech-broker",
    'KEEPALIVE': 60,
    'TOPIC': "SENSOR/ULTRASSOM"
}
