from pymongo import MongoClient

class IoTData:
    def __init__(self, device_id, temperature, humidity, timestamp):
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp
