import paho.mqtt.client as mqtt
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['VM']
collection = db['Test_Data']

# MQTT broker details
mqtt_broker = 'localhost'  # or specify the IP address of your VM
mqtt_port = 1883
mqtt_topic = 'fbs_vierplus'

# Connect to MQTT broker
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, mqtt_port)

# Publish data from MongoDB to MQTT topic
for document in collection.find():
    data_to_publish = str(document)  # Modify as needed
    mqtt_client.publish(mqtt_topic, data_to_publish)

mqtt_client.disconnect()
