from pymongo import MongoClient

class Device:
    def __init__(self, device_id, status, created_at, updated_at, latest_data):
        self.device_id = device_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.latest_data = latest_data
