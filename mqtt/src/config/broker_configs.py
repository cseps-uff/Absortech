import os

mqtt_broker_configs = {
    'HOST': os.getenv('MQTT_HOST', 'localhost'),
    'PORT': int(os.getenv('MQTT_PORT', 1883)),
    'USERNAME': os.getenv('MQTT_USER', ''),
    'PASSWORD': os.getenv('MQTT_PASS', ''),
    'USE_TLS': os.getenv('MQTT_TLS', 'false').lower() in ('1', 'true', 'yes'),
    'CLIENT_NAME': "absortech-broker",
    'KEEPALIVE': 60,
    'TOPIC': "SENSOR/ULTRASSOM"
}
