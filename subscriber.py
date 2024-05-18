import paho.mqtt.client as mqtt

# MQTT broker details
mqtt_broker = '100.108.16.72'  # Tailsacle IP address from VM
mqtt_port = 1883
mqtt_topic = 'fbs_vierplus'

# Callback function when a message is received
def on_message(client, userdata, message):
    print('Received message:', str(message.payload.decode('utf-8')))

# Connect to MQTT broker and subscribe to topic
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_client.subscribe(mqtt_topic)

# Keep the client running to receive messages
mqtt_client.loop_forever()
