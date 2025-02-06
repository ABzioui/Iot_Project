import json
from datetime import datetime
from models.models import db, Device, IoTData, EndDeviceData, APIData
import pika
from sqlalchemy.exc import SQLAlchemyError
import uuid


class DeviceService:

    @staticmethod
    def publish_to_rabbitmq(action, device_id, data):
        """Publie un message dans RabbitMQ"""
        from config.config import Config
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT))
        channel = connection.channel()
        channel.queue_declare(queue=Config.RABBITMQ_QUEUE)

        message = {
            "action": action,
            "device_id": device_id,
            "data": data
        }

        channel.basic_publish(exchange="", routing_key=Config.RABBITMQ_QUEUE, body=json.dumps(message))
        connection.close()

    @staticmethod
    def register_device(data):
        """Enregistre un nouvel appareil"""
        if not data.get('device_id') or not data.get('type'):
            return {"error": "Device ID and type are required"}, 400

        existing_device = Device.query.filter_by(device_id=data['device_id']).first()
        if existing_device:
            return {"error": "Device ID already exists"}, 409

        if data['type'] not in ['iot', 'end_device', 'api']:
            return {"error": "Invalid device type"}, 400

        try:
            new_device = Device(
                device_id=data['device_id'],
                type=data['type'],
                status=data.get('status', 'active'),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            if data['type'] == 'api':
                if not data.get('location_lat') or not data.get('location_lon'):
                    return {"error": "Location coordinates required for API devices"}, 400
                
                new_device.location_lat = data['location_lat']
                new_device.location_lon = data['location_lon']
                new_device.monitored_params = data.get('monitored_params', [])

            db.session.add(new_device)
            db.session.commit()

            response_data = {
                "message": "Device registered successfully",
                "device": {
                    "device_id": new_device.device_id,
                    "type": new_device.type,
                    "status": new_device.status,
                    "created_at": new_device.created_at.isoformat()
                }
            }

            if new_device.type == 'api':
                response_data["device"].update({
                    "location_lat": new_device.location_lat,
                    "location_lon": new_device.location_lon,
                    "monitored_params": new_device.monitored_params
                })

            DeviceService.publish_to_rabbitmq("register", new_device.device_id, response_data)

            return response_data, 201

        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to register device: {str(e)}"}, 500

    @staticmethod
    def get_device(device_id):
        """Récupère un appareil avec ses dernières données"""
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return None

        result = {
            "device_id": device.device_id,
            "type": device.type,
            "status": device.status,
            "monitored_params": device.monitored_params,
            "latest_data": None
        }

        if device.type == "iot":
            latest = IoTData.query.filter_by(device_id=device_id).order_by(IoTData.timestamp.desc()).first()
            if latest:
                result["latest_data"] = {"temperature": latest.temperature, "humidity": latest.humidity, "timestamp": latest.timestamp}
        elif device.type == "end_device":
            latest = EndDeviceData.query.filter_by(device_id=device_id).order_by(EndDeviceData.timestamp.desc()).first()
            if latest:
                result["latest_data"] = {"ip_address": latest.ip_address, "cpu_load": latest.cpu_load, "memory_usage": latest.memory_usage, "disk_usage": latest.disk_usage, "timestamp": latest.timestamp}
        elif device.type == "api":
            latest = APIData.query.filter_by(device_id=device_id).order_by(APIData.timestamp.desc()).first()
            if latest:
                result["latest_data"] = {"temperature": latest.temperature, "precipitation": latest.precipitation, "humidity": latest.humidity, "location_lat": latest.location_lat, "location_lon": latest.location_lon, "timestamp": latest.timestamp}

        return result

    @staticmethod
    def list_devices():
        """Récupère tous les appareils enregistrés"""
        devices = Device.query.all()
        return [DeviceService.get_device(device.device_id) for device in devices]

    @staticmethod
    def update_device(device_id, data):
        """Met à jour un appareil"""
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return {"error": "Device not found"}, 404

        allowed_fields = ["status"]
        if device.type == "api":
            allowed_fields += ["location_lat", "location_lon", "monitored_params"]

        for field in allowed_fields:
            if field in data and data[field] is not None:
                setattr(device, field, data[field])

        device.updated_at = datetime.utcnow()
        db.session.commit()

        DeviceService.publish_to_rabbitmq("update", device_id, data)

        return {"message": "Device updated successfully", "device": DeviceService.get_device(device_id)}, 200

    @staticmethod
    def delete_device(device_id):
        """Supprime un appareil et ses données associées"""
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return {"error": "Device not found"}, 404

        if device.type == "iot":
            IoTData.query.filter_by(device_id=device_id).delete()
        elif device.type == "end_device":
            EndDeviceData.query.filter_by(device_id=device_id).delete()
        elif device.type == "api":
            APIData.query.filter_by(device_id=device_id).delete()

        db.session.delete(device)
        db.session.commit()

        DeviceService.publish_to_rabbitmq("delete", device_id, {})
        return {"message": "Device deleted successfully"}, 200

    @staticmethod
    def register_iot_device(data):
        """Enregistre un nouvel appareil IoT et initialise ses données si nécessaire."""
        if not data or not data.get('device_id'):
            return {"error": "Device ID is required"}, 400

        existing_device = Device.query.filter_by(device_id=data['device_id'], type='iot').first()
        if existing_device:
            return {"error": "Device ID already exists"}, 409

        try:
            new_device = Device(
                device_id=data['device_id'],
                type='iot',
                status=data.get('status', 'active'),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.session.add(new_device)
            db.session.commit()

            # ✅ Initialiser une première entrée dans iot_data
            initial_data = IoTData(
                device_id=new_device.device_id,
                temperature=None,
                humidity=None,
                timestamp=datetime.utcnow()
            )
            db.session.add(initial_data)
            db.session.commit()

            # Publier à RabbitMQ après l'enregistrement
            response_data = {
                "message": "IoT Device registered successfully",
                "device_id": new_device.device_id,
                "status": new_device.status,
                "created_at": new_device.created_at.isoformat(),
                "updated_at": new_device.updated_at.isoformat(),
                "latest_data": {
                    "temperature": initial_data.temperature,
                    "humidity": initial_data.humidity,
                    "timestamp": initial_data.timestamp.isoformat()
                }
            }
            # Publier sur RabbitMQ pour signaler l'enregistrement du device IoT
            DeviceService.publish_to_rabbitmq("register", new_device.device_id, response_data)

            return response_data, 201

        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to register IoT device: {str(e)}"}, 500

    @staticmethod
    def update_iot_device(device_id, data):
        """Met à jour un appareil IoT"""
        device = Device.query.filter_by(device_id=device_id, type="iot").first()
        if not device:
            return {"error": "IoT Device not found"}, 404

        if "status" in data:
            device.status = data["status"]
        device.updated_at = datetime.utcnow()

        db.session.commit()

        # Publier à RabbitMQ après la mise à jour
        response_data = {
            "message": "IoT Device updated successfully",
            "device_id": device.device_id,
            "status": device.status,
            "updated_at": device.updated_at.isoformat()
        }
        # Publier sur RabbitMQ pour signaler la mise à jour du device IoT
        DeviceService.publish_to_rabbitmq("update", device.device_id, response_data)

        return {"message": "IoT Device updated successfully", "device_id": device.device_id}, 200

    @staticmethod
    def delete_iot_device(device_id):
        """Supprime un appareil IoT et ses données associées"""
        device = Device.query.filter_by(device_id=device_id, type="iot").first()
        if not device:
            return {"error": "IoT Device not found"}, 404

        # Supprime les données associées
        IoTData.query.filter_by(device_id=device_id).delete()

        db.session.delete(device)
        db.session.commit()

        # Publier à RabbitMQ après la suppression
        DeviceService.publish_to_rabbitmq("delete", device_id, {})

        return {"message": "IoT Device deleted successfully"}, 204
            
    @staticmethod
    def save_iot_data(device_id, data):
        """Enregistre les données IoT pour un appareil, crée l'appareil si inexistant"""
        # Vérifier si le device existe déjà dans la base
        device = Device.query.filter_by(device_id=device_id, type="iot").first()
        
        # Si le device n'existe pas, on le crée
        if not device:
            try:
                # Créer un nouvel appareil IoT avec le type 'iot' et le statut 'active'
                device = Device(device_id=device_id, type="iot", status="active")
                db.session.add(device)
                db.session.commit()
            except Exception as e:
                db.session.rollback()  # Annuler en cas d'erreur
                return {"error": f"Error registering device: {str(e)}"}, 500
        
        # Vérification des données reçues
        if not data or "temperature" not in data or "humidity" not in data:
            return {"error": "Invalid data format"}, 400

        try:
            # Créer un enregistrement IoTData
            new_data = IoTData(
                device_id=device_id,
                temperature=data["temperature"],
                humidity=data["humidity"],
                timestamp=datetime.utcnow()
            )
            db.session.add(new_data)
            db.session.commit()

            # Convertir la date en chaîne (format ISO 8601)
            timestamp_str = datetime.utcnow().isoformat()

            # Publier les données sur RabbitMQ
            response_data = {
                "device_id": device_id,
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "timestamp": timestamp_str  # Utiliser la chaîne ISO 8601 pour la date
            }
            
            # Publication sur RabbitMQ
            DeviceService.publish_to_rabbitmq("save_data", device.device_id, response_data)

            return {"message": "IoT Data saved and published successfully", "device_id": device_id}, 201

        except Exception as e:
            db.session.rollback()  # Annuler en cas d'erreur
            return {"error": str(e)}, 500

    @staticmethod
    def list_iot_devices():
        """Liste tous les appareils IoT"""
        devices = Device.query.filter_by(type="iot").all()
        return [{"device_id": device.device_id, "status": device.status} for device in devices], 200

    @staticmethod
    def get_iot_device(device_id):
        """Récupère un appareil IoT spécifique"""
        device = Device.query.filter_by(device_id=device_id, type="iot").first()
        if not device:
            return {"error": "IoT Device not found"}, 404

        return {
            "device_id": device.device_id,
            "status": device.status,
            "created_at": device.created_at.isoformat(),
            "updated_at": device.updated_at.isoformat()
        }, 200


    @staticmethod
    def list_iot_data(device_id):
        """Récupère les données IoT d'un appareil"""
        device = Device.query.filter_by(device_id=device_id, type="iot").first()
        if not device:
            return {"error": "IoT Device not found"}, 404

        iot_data = IoTData.query.filter_by(device_id=device_id).order_by(IoTData.timestamp.desc()).all()
        return [{
            "temperature": data.temperature,
            "humidity": data.humidity,
            "timestamp": data.timestamp.isoformat()
        } for data in iot_data], 200

    @staticmethod
    def get_latest_iot_data(device_id):
        """Récupère les dernières données IoT d'un appareil"""
        latest_data = IoTData.query.filter_by(device_id=device_id).order_by(IoTData.timestamp.desc()).first()
        if not latest_data:
            return {"error": "No IoT Data found for this device"}, 404

        return {
            "temperature": latest_data.temperature,
            "humidity": latest_data.humidity,
            "timestamp": latest_data.timestamp.isoformat()
        }, 200

    @staticmethod
    def register_end_device(data):
        """Registers a new end device."""
        device_id = data.get('device_id')
        if Device.query.filter_by(device_id=device_id).first():
            return {"error": "Device already exists"}, 400
        
        device = Device(device_id=device_id, type='end_device', status='active')
        db.session.add(device)
        db.session.commit()

        # Publish to RabbitMQ
        response_data = {
            "message": "End device registered successfully",
            "device_id": device.device_id,
            "status": device.status,
            "created_at": device.created_at.isoformat(),
            "updated_at": device.updated_at.isoformat()
        }
        DeviceService.publish_to_rabbitmq("register", device.device_id, response_data)

        return {"message": "End device registered successfully", "device_id": device.device_id}, 201

    @staticmethod
    def update_end_device(device_id, data):
        """Update an existing end device."""
        device = Device.query.filter_by(device_id=device_id, type='end_device').first()
        if not device:
            return {"error": "End device not found"}, 404
        
        device.status = data.get('status', device.status)
        db.session.commit()

        # Publish to RabbitMQ
        response_data = {
            "message": "End device updated successfully",
            "device_id": device.device_id,
            "status": device.status,
            "updated_at": device.updated_at.isoformat()
        }
        DeviceService.publish_to_rabbitmq("update", device.device_id, response_data)

        return {"message": "Device updated successfully"}, 200

    @staticmethod
    def delete_end_device(device_id):
        """Delete an end device."""
        device = Device.query.filter_by(device_id=device_id, type='end_device').first()
        if not device:
            return {"error": "End device not found"}, 404
        
        db.session.delete(device)
        db.session.commit()

        # Publish to RabbitMQ
        DeviceService.publish_to_rabbitmq("delete", device_id, {})

        return {"message": "Device deleted successfully"}, 204

    @staticmethod
    def save_end_device_data(device_id, data):
        """Save data for a specific end device."""
        device = Device.query.filter_by(device_id=device_id, type='end_device').first()
        if not device:
            return {"error": "End device not found"}, 404
        
        end_device_data = EndDeviceData(
            device_id=device_id,
            ip_address=data.get('ip_address'),
            cpu_load=data.get('cpu_load'),
            memory_usage=data.get('memory_usage'),
            disk_usage=data.get('disk_usage'),
            timestamp=datetime.utcnow()
        )
        db.session.add(end_device_data)
        db.session.commit()

        # Publish to RabbitMQ
        response_data = {
            "message": "End device data saved successfully",
            "device_id": device.device_id,
            "ip_address": end_device_data.ip_address,
            "cpu_load": end_device_data.cpu_load,
            "memory_usage": end_device_data.memory_usage,
            "disk_usage": end_device_data.disk_usage,
            "timestamp": end_device_data.timestamp.isoformat()
        }
        DeviceService.publish_to_rabbitmq("save_data", device.device_id, response_data)

        return {"message": "End device data saved successfully"}, 201

    @staticmethod
    def list_end_device_data(device_id):
        """Fetch data for a specific end device."""
        data = EndDeviceData.query.filter_by(device_id=device_id).all()
        return [d.to_dict() for d in data], 200

    @staticmethod
    def list_end_devices():
        """Returns a list of all end devices."""
        devices = Device.query.filter_by(type='end_device').all()
        return [device.to_dict() for device in devices]

    @staticmethod
    def get_end_device(device_id):
        """Fetch a single end device by ID."""
        device = Device.query.filter_by(device_id=device_id, type='end_device').first()
        return device.to_dict() if device else None

    @staticmethod
    def list_end_device_data(device_id):
        """Fetch data for a specific end device."""
        data = EndDeviceData.query.filter_by(device_id=device_id).all()
        return [d.to_dict() for d in data], 200

    # CRUD Operations for API Devices
    @staticmethod
    def register_api_device(data):
        """Registers a new API device."""
        if not data or not data.get('device_id'):
            return {"error": "Device ID is required"}, 400

        # Check if the device already exists
        existing_device = Device.query.filter_by(device_id=data['device_id'], type='api').first()
        if existing_device:
            return {"error": "Device ID already exists"}, 409

        try:
            # Create the device without location data
            new_device = Device(
                device_id=data['device_id'],
                type='api',
                status=data.get('status', 'active'),
                monitored_params=data.get('monitored_params', [])
            )

            # Add the device to the database
            db.session.add(new_device)
            db.session.commit()

            # If location data is provided, save it in the APIData model
            if 'location_lat' in data and 'location_lon' in data:
                new_api_data = APIData(
                    device_id=data['device_id'],
                    location_lat=data['location_lat'],
                    location_lon=data['location_lon']
                )
                db.session.add(new_api_data)
                db.session.commit()

            return {
                "message": "API Device registered successfully",
                "device_id": new_device.device_id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to register API device: {str(e)}"}, 500

    @staticmethod
    def list_api_devices():
        """Lists all API devices."""
        devices = Device.query.filter_by(type="api").all()
        return [{"device_id": device.device_id, "status": device.status} for device in devices], 200

    @staticmethod
    def get_api_device(device_id):
        """Fetches a specific API device."""
        device = Device.query.filter_by(device_id=device_id, type="api").first()
        if not device:
            return {"error": "API Device not found"}, 404

        return {
            "device_id": device.device_id,
            "status": device.status,
            "location_lat": device.location_lat,
            "location_lon": device.location_lon,
            "monitored_params": device.monitored_params,
            "created_at": device.created_at.isoformat(),
            "updated_at": device.updated_at.isoformat()
        }, 200

    @staticmethod
    def update_api_device(device_id, data):
        """Updates an API device."""
        device = Device.query.filter_by(device_id=device_id, type="api").first()
        if not device:
            return {"error": "API Device not found"}, 404

        # Allowed fields to update
        allowed_fields = ["status", "location_lat", "location_lon", "monitored_params"]
        for field in allowed_fields:
            if field in data and data[field] is not None:
                setattr(device, field, data[field])

        device.updated_at = datetime.utcnow()
        db.session.commit()

        # Publish update event to RabbitMQ
        response_data = {
            "message": "API Device updated successfully",
            "device_id": device.device_id,
            "status": device.status,
            "updated_at": device.updated_at.isoformat()
        }
        DeviceService.publish_to_rabbitmq("update", device.device_id, response_data)

        return {"message": "API Device updated successfully", "device_id": device.device_id}, 200

    @staticmethod
    def delete_api_device(device_id):
        """Deletes an API device and its associated data."""
        device = Device.query.filter_by(device_id=device_id, type="api").first()
        if not device:
            return {"error": "API Device not found"}, 404

        # Delete associated data
        APIData.query.filter_by(device_id=device_id).delete()

        db.session.delete(device)
        db.session.commit()

        # Publish delete event to RabbitMQ
        DeviceService.publish_to_rabbitmq("delete", device_id, {})

        return {"message": "API Device deleted successfully"}, 204

    @staticmethod
    def save_api_data(device_id, data):
        """Save API data for a device. If the device doesn't exist, create it."""
        # Check if the device exists
        device = Device.query.filter_by(device_id=device_id, type="api").first()

        if not device:
            # If the device doesn't exist, create it
            try:
                new_device = Device(
                    device_id=device_id,
                    type='api',
                    status=data.get('status', 'active'),
                    monitored_params=data.get('monitored_params', [])
                )
                db.session.add(new_device)
                db.session.commit()

                # After creating the device, we can proceed to add the data
                device = new_device
            except Exception as e:
                db.session.rollback()
                return {"error": f"Failed to register API device: {str(e)}"}, 500

        # Now that we have the device, add the API data
        if 'location_lat' in data and 'location_lon' in data:
            try:
                # Add the API data for this device
                new_data = APIData(
                    device_id=device_id,
                    temperature=data.get("temperature"),
                    humidity=data.get("humidity"),
                    precipitation=data.get("precipitation"),
                    location_lat=data["location_lat"],
                    location_lon=data["location_lon"],
                    timestamp=datetime.utcnow()
                )
                db.session.add(new_data)
                db.session.commit()

                # Prepare message data for RabbitMQ
                message_data = {
                    "temperature": new_data.temperature,
                    "precipitation": new_data.precipitation,
                    "humidity": new_data.humidity,
                    "location_lat": new_data.location_lat,
                    "location_lon": new_data.location_lon,
                    "timestamp": new_data.timestamp.isoformat()
                }

                # Publish data to RabbitMQ
                DeviceService.publish_to_rabbitmq("save_data", device.device_id, message_data)

                return {"message": "API Data saved successfully"}, 201
            except Exception as e:
                db.session.rollback()
                return {"error": f"Failed to save API data: {str(e)}"}, 500

        return {"error": "Location data required"}, 400

    @staticmethod
    def get_latest_api_data(device_id):
        """Fetches the latest API data for a device."""
        latest_data = APIData.query.filter_by(device_id=device_id).order_by(APIData.timestamp.desc()).first()
        if not latest_data:
            return {"error": "No API Data found for this device"}, 404

        return {
            "temperature": latest_data.temperature,
            "precipitation": latest_data.precipitation,
            "humidity": latest_data.humidity,
            "location_lat": latest_data.location_lat,
            "location_lon": latest_data.location_lon,
            "timestamp": latest_data.timestamp.isoformat()
        }, 200