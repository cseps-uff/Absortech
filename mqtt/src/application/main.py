import sys
import os

from time import sleep

import django

# Django setup - must be done before importing models
sys.path.insert(0, '/app/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAbsortech.settings')
django.setup()

from src.config.broker_configs import mqtt_broker_configs
from src.application.client.mqtt_client_connection import MQTTClientConnection


# Gets broker info, configures client and starts connection
def start():
    mqtt_client_connection = MQTTClientConnection(
        mqtt_broker_configs["HOST"],
        mqtt_broker_configs["PORT"],
        mqtt_broker_configs["CLIENT_NAME"],
        mqtt_broker_configs["KEEPALIVE"]
    )
    
    mqtt_client_connection.start_connection()

    while True: sleep(0.001)
