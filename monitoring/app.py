import pika
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import threading

# Connexion à MongoDB
MONGO_URI = 'mongodb+srv://anas:tSUrDdvOGGhzKE2J@cluster0.tpi9ehl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)

# Sélection des bases de données et collections
db = client["iot_database"]
iot_collection = db["iot_data"]
end_device_collection = db["end_device_data"]
api_meteo_collection = db["api_meteo_data"]
devices_collection = db["devices"]  # Collection des appareils

# Connexion à RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Déclarer la queue
queue_name = "device_events"
channel.queue_declare(queue=queue_name)

# Enable CORS for all routes
app = Flask(__name__)
CORS(app)

# Fonction de traitement des messages "save_data"
def process_and_store_data(message):
    data = message.get("data", {})
    device_id = message.get("device_id")
    msg = data.get("message")

    if msg == "End device data saved successfully":
        collection = end_device_collection
        category = "End Device Data"
    elif "location_lat" in data:
        collection = api_meteo_collection
        category = "API Meteo Data"
        data["device_id"] = device_id
    else:
        collection = iot_collection
        category = "IoT Data"
    
    collection.insert_one(data)
    print(f"✅ {category} sauvegardé : {data}")

# Fonction pour enregistrer un nouvel appareil
def register_device(message):
    data = message.get("data", {})
    msg = data.get("message", "").lower()

    device = data.get("device", {})
    type = device.get("type", "")

    if "iot device registered successfully" in msg:
        device_type = "iot"
    elif (type == "end_device") or ("end device registered successfully") in msg:
        device_type = "end_device"
    elif "api device registered successfully" in msg:
        device_type = "api"
    else:
        print("⚠️ Type d'appareil inconnu, enregistrement ignoré.")
        return

    if type == "end_device":
        device_info = {
        "device_id": device.get("device_id"),
        "type": device_type,
        "status": device.get("status", "unknown"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        }
    else :
        device_info = {
            "device_id": data.get("device_id"),
            "type": device_type,
            "status": data.get("status", "unknown"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
        }

    devices_collection.insert_one(device_info)
    print(f"✅ Appareil enregistré : {device_info}")

# Fonction pour mettre à jour un appareil
def update_device_status(message):
    data = message.get("data", {})
    device_id = data.get("device_id")
    new_status = data.get("status")

    if not device_id or not new_status:
        print("⚠️ Données invalides pour la mise à jour.")
        return

    result = devices_collection.update_one(
        {"device_id": device_id}, 
        {"$set": {"status": new_status, "updated_at": data.get("updated_at")} }
    )

    if result.matched_count > 0:
        print(f"✅ Statut du device {device_id} mis à jour : {new_status}")
    else:
        print(f"⚠️ Aucun device trouvé avec l'ID {device_id}, mise à jour ignorée.")

# Fonction pour supprimer un appareil et ses données associées
def delete_device(message):
    data = message.get("data", {})
    device_id = message.get("device_id")

    if not device_id:
        print("⚠️ Aucun device_id fourni pour la suppression.")
        return

    result_device = devices_collection.delete_many({"device_id": device_id})
    result_iot = iot_collection.delete_many({"device_id": device_id})
    result_end_device = end_device_collection.delete_many({"device_id": device_id})
    result_api_meteo = api_meteo_collection.delete_many({"device_id": device_id})

    if result_device.deleted_count > 0:
        print(f"✅ Appareil {device_id} supprimé de 'devices'.")
    else:
        print(f"⚠️ Aucun appareil trouvé avec l'ID {device_id} dans 'devices'.")
    print(f"📉 Données supprimées : IoT({result_iot.deleted_count}), End Device({result_end_device.deleted_count}), API Meteo({result_api_meteo.deleted_count})")

# Ajout du cas delete dans le callback
def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
        action = message.get("action")

        if action == "save_data":
            process_and_store_data(message)
        elif action == "register":
            register_device(message)
        elif action == "update":
            update_device_status(message)
        elif action == "delete":
            delete_device(message)
        else:
            print(f"⚠️ Action non prise en charge : {action}")
    except json.JSONDecodeError:
        print("❌ Erreur de décodage JSON.")

# Consommateur RabbitMQ
def start_rabbitmq_consumer():
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# New Routes for Device IDs and Temperature Data
@app.route('/get-device-ids', methods=['GET'])
def get_device_ids():
    device_ids = db.iot_data.distinct('device_id')
    return jsonify(device_ids)

@app.route('/get-temperature-data', methods=['GET'])
def get_temperature_data():
    device_id = request.args.get('device_id')
    data = list(db.iot_data.find({'device_id': device_id}, {'_id': 0, 'temperature': 1, 'humidity': 1,'timestamp': 1}))
    return jsonify(data)

@app.route('/get-enddevice-ip', methods=['GET'])
def get_enddevice_ip():
    ip_addresses = db.end_device_data.distinct('ip_address')  # Fetch unique ip_address from end_device_data collection
    return jsonify(ip_addresses)

@app.route('/get-enddevice-data', methods=['GET'])
def get_enddevice_data():
    ip_address = request.args.get('ip_address')  # Get the ip_address from query parameters
    data = list(db.end_device_data.find({'ip_address': ip_address}, {'_id': 0, 'cpu_load': 1, 'disk_usage': 1, 'memory_usage': 1, 'timestamp': 1}))
    return jsonify(data)

if __name__ == '__main__':
    # Start RabbitMQ listener in a separate thread
    rabbitmq_thread = threading.Thread(target=start_rabbitmq_consumer)
    rabbitmq_thread.daemon = True  # Ensure it exits when the main program exits
    rabbitmq_thread.start()

    # Start Flask app
    app.run(debug=True, port=5010)
