import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client('absortech_publisher')
mqtt_client.connect(host="localhost", port=1883)
