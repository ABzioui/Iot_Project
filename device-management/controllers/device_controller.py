from flask import Blueprint, request, jsonify
from business.device_service import DeviceService

device_blueprint = Blueprint("device", __name__)

### 📌 GESTION DES APPAREILS
@device_blueprint.route("/devices", methods=["GET"])
def list_devices():
    try:
        devices = DeviceService.list_devices()
        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@device_blueprint.route("/devices", methods=["POST"])
def register_device():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        result, status_code = DeviceService.register_device(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@device_blueprint.route("/devices/<device_id>", methods=["GET", "PUT", "DELETE"])
def manage_device(device_id):
    try:
        if request.method == "GET":
            device = DeviceService.get_device(device_id)
            return jsonify(device) if device else ({"error": "Device not found"}, 404)
        
        elif request.method == "PUT":
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON data"}), 400
            result, status_code = DeviceService.update_device(device_id, data)
            return jsonify(result), status_code
        
        elif request.method == "DELETE":
            result = DeviceService.delete_device(device_id)
            return jsonify(result), result[1] if isinstance(result, tuple) else 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500

### 📌 GESTION DES APPAREILS IoT
@device_blueprint.route("/iot/devices", methods=["GET", "POST"])
def manage_iot_devices():
    try:
        if request.method == "GET":
            devices = DeviceService.list_iot_devices()
            return jsonify(devices), 200
        
        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            result, status_code = DeviceService.register_iot_device(data)
            return jsonify(result), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@device_blueprint.route("/iot/devices/<device_id>", methods=["GET", "PUT", "DELETE"])
def manage_iot_device(device_id):
    try:
        if request.method == "GET":
            device = DeviceService.get_iot_device(device_id)
            return jsonify(device) if device else ({"error": "IoT Device not found"}, 404)

        elif request.method == "PUT":
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON data"}), 400
            result, status_code = DeviceService.update_iot_device(device_id, data)
            return jsonify(result), status_code

        elif request.method == "DELETE":
            result = DeviceService.delete_iot_device(device_id)
            return jsonify(result), result[1] if isinstance(result, tuple) else 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500

### 📌 GESTION DES DONNÉES IoT
@device_blueprint.route("/iot/devices/data/<device_id>", methods=["POST", "GET"])
def manage_iot_data(device_id):
    try:
        if request.method == "POST":
            # Get the incoming JSON data from the request body
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Call the service method to save IoT data
            result, status_code = DeviceService.save_iot_data(device_id, data)
            return jsonify(result), status_code

        elif request.method == "GET":
            # Retrieve IoT data for the specific device
            data, status_code = DeviceService.list_iot_data(device_id)
            return jsonify(data), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@device_blueprint.route("/iot/devices/data/<device_id>/latest", methods=["GET"])
def get_latest_iot_data(device_id):
    try:
        data, status_code = DeviceService.get_latest_iot_data(device_id)
        return jsonify(data), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

### 📌 GESTION DES END DEVICES
@device_blueprint.route("/end_device/devices", methods=["GET", "POST"])
def manage_end_device():
    try:
        if request.method == "GET":
            devices = DeviceService.list_end_devices()  # Fetch all end devices
            return jsonify(devices), 200

        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            result, status_code = DeviceService.register_end_device(data)  # Register new device
            return jsonify(result), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@device_blueprint.route("/end_device/devices/<device_id>", methods=["GET", "PUT", "DELETE"])
def manage_end_device_by_id(device_id):
    try:
        if request.method == "GET":
            device = DeviceService.get_end_device(device_id)
            return jsonify(device) if device else ({"error": "End Device not found"}, 404)

        elif request.method == "PUT":
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON data"}), 400
            result, status_code = DeviceService.update_end_device(device_id, data)  # Update device details
            return jsonify(result), status_code

        elif request.method == "DELETE":
            result = DeviceService.delete_end_device(device_id)  # Delete the device
            return jsonify(result), result[1] if isinstance(result, tuple) else 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@device_blueprint.route("/end_device/devices/data/<device_id>", methods=["POST", "GET"])
def manage_end_device_data(device_id):
    try:
        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            result, status_code = DeviceService.save_end_device_data(device_id, data)  # Save device data
            return jsonify(result), status_code

        elif request.method == "GET":
            data, status_code = DeviceService.list_end_device_data(device_id)  # Fetch data for a specific device
            return jsonify(data), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@device_blueprint.route("/api/devices", methods=["GET", "POST"])
def manage_api_devices():
    try:
        if request.method == "GET":
            devices = DeviceService.list_api_devices()  # Fetch all API devices
            return jsonify(devices), 200

        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            result, status_code = DeviceService.register_api_device(data)  # Register new API device
            return jsonify(result), status_code

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@device_blueprint.route("/api/devices/<device_id>", methods=["GET", "PUT", "DELETE"])
def manage_api_device_by_id(device_id):
    try:
        if request.method == "GET":
            device = DeviceService.get_api_device(device_id)
            if device:
                return jsonify(device), 200
            return jsonify({"error": "API Device not found"}), 404

        elif request.method == "PUT":
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON data"}), 400
            result, status_code = DeviceService.update_api_device(device_id, data)  # Update API device details
            return jsonify(result), status_code

        elif request.method == "DELETE":
            result = DeviceService.delete_api_device(device_id)  # Delete the API device
            # If result contains a tuple (message, status_code), return that, else default to 204
            return jsonify(result), result[1] if isinstance(result, tuple) else 204

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@device_blueprint.route("/api/devices/data/<device_id>", methods=["POST", "GET"])
def manage_api_data(device_id):
    try:
        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            result, status_code = DeviceService.save_api_data(device_id, data)  # Save API data
            return jsonify(result), status_code

        elif request.method == "GET":
            data, status_code = DeviceService.list_api_data(device_id)  # Fetch data for the API device
            return jsonify(data), status_code

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@device_blueprint.route("/api/devices/data/<device_id>/latest", methods=["GET"])
def get_latest_api_data(device_id):
    try:
        data, status_code = DeviceService.get_latest_api_data(device_id)
        return jsonify(data), status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500