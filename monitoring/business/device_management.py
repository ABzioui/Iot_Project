from models.device_model import Device
from models.iot_data_model import IoTData
import pika
import json
from datetime import datetime
from pymongo import MongoClient



class DeviceManager:
    def __init__(self):
        # Use the MONGO_URI from config.py
        self.client = MongoClient("mongodb://root:example@localhost:27017/iot_database")
        # Specify the database name here
        self.db = self.client.get_database("iot_database")  # <-- Add your database name here
        self.devices_collection = self.db.devices
        self.iot_data_collection = self.db.iot_data
        
        # RabbitMQ setup here (no changes needed for MongoDB connection)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='device_events')
        self.channel.basic_consume(queue='device_events', on_message_callback=self.process_message, auto_ack=True)

    def process_message(self, ch, method, properties, body):
        message = json.loads(body.decode())
        action = message.get('action')
        device_id = message.get('device_id')
        data = message.get('data')
        
        if action == 'save_data':
            self.handle_device_data(device_id, data)

    def handle_device_data(self, device_id, data):
        device = self.devices_collection.find_one({"device_id": device_id})
        
        if not device:
            self.register_device(device_id, data)
        else:
            self.store_iot_data(device_id, data)
    
    def register_device(self, device_id, data):
        device_info = {
            "device_id": device_id,
            "status": "active",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "latest_data": data
        }
        self.devices_collection.insert_one(device_info)
        print(f"New device registered: {device_id}")
        self.store_iot_data(device_id, data)

    def store_iot_data(self, device_id, data):
        iot_data_entry = {
            "device_id": device_id,
            "temperature": data['temperature'],
            "humidity": data['humidity'],
            "timestamp": datetime.fromisoformat(data['timestamp'])
        }
        self.iot_data_collection.insert_one(iot_data_entry)
        print(f"Data saved for device: {device_id} at {data['timestamp']}")

    def start_consuming(self):
        print("Waiting for messages...")
        self.channel.start_consuming()
