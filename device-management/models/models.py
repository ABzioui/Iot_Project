from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

db = SQLAlchemy()

# Enum for device types
device_type_enum = db.Enum('iot', 'end_device', 'api', name='device_type')

class Device(db.Model):
    """Main table to store devices"""
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(device_type_enum, nullable=False)
    status = db.Column(db.String(20), default="active")
    monitored_params = db.Column(JSONB, nullable=True)  # Optional monitored parameters
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    def to_dict(self):
        return {
            'device_id': self.device_id,
            'type': self.type,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class IoTData(db.Model):
    """Stores IoT device data"""
    __tablename__ = "iot_data"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), db.ForeignKey('devices.device_id'), nullable=False)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)

class EndDeviceData(db.Model):
    """Stores end device (PC) data"""
    __tablename__ = "end_device_data"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), db.ForeignKey('devices.device_id'), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)  # IP address
    cpu_load = db.Column(db.Float, nullable=True)  # CPU load (%)
    memory_usage = db.Column(db.Float, nullable=True)  # Memory usage (%)
    disk_usage = db.Column(db.Float, nullable=True)  # Disk usage (%)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    def to_dict(self):
        return {
            'device_id': self.device_id,
            'ip_address': self.ip_address,
            'cpu_load': self.cpu_load,
            'memory_usage': self.memory_usage,
            'disk_usage': self.disk_usage,
            'timestamp': self.timestamp
        }

class APIData(db.Model):
    """Stores API data (e.g., weather data)"""
    __tablename__ = "api_data"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), db.ForeignKey('devices.device_id'), nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    location_lat = db.Column(db.Float, nullable=False)  # Latitude
    location_lon = db.Column(db.Float, nullable=False)  # Longitude
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
