import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import time

# MongoDB connection
mongo_uri = "mongodb://vierplus:4plus@localhost:27017/"
client_mongo = MongoClient(mongo_uri)
db = client_mongo["VM_DB"]
collection = db["Test_Data"]

# MQTT broker connection
mqtt_broker_uri = "localhost"
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker_uri)

# List to store IDs of documents that have been sent
sent_document_ids = []

# Initial publication of stored data
for document in collection.find():
    document['_id'] = str(document['_id'])
    payload = json.dumps(document)
    mqtt_client.publish("fbs_vierplus", payload, retain=True)
    sent_document_ids.append(document["_id"])

# Main loop to continuously publish new data
while True:
    # Fetch and publish new data from MongoDB to MQTT broker
    for document in collection.find():
        document_id = str(document['_id'])
        if document_id not in sent_document_ids:
            document['_id'] = document_id
            payload = json.dumps(document)
            mqtt_client.publish("fbs_vierplus", payload, retain=True)
            sent_document_ids.append(document_id)

    # Sleep for some time before fetching new data
    time.sleep(10)
