import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import time

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['VM_DB']
collection = db['Test_Data']

# MQTT broker details
mqtt_broker = 'localhost'
mqtt_port = 1883
mqtt_topic = 'fbs_vierplus'

# Connect to MQTT broker
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, mqtt_port)

# Function to fetch new data from MongoDB and publish to MQTT
def fetch_and_publish():
    last_id = None
    
    while True:
        query = {}
        if last_id:
            query = {'_id': {'$gt': last_id}}  # Query for documents with an ID greater than the last processed ID
        
        documents = collection.find(query).sort('_id')
        for document in documents:
            data_to_publish = json.dumps(document)  # Convert MongoDB document to JSON
            mqtt_client.publish(mqtt_topic, data_to_publish)
            last_id = document['_id']  # Update last_id to the ID of the current document
        
        time.sleep(10)  # Wait for a specified time before checking for new data again

# Start fetching and publishing data
fetch_and_publish()

mqtt_client.disconnect()
