import paho.mqtt.client as mqtt
import random
import time
import requests
from datetime import datetime

# Configuration
DEVICE_ID = "device999"  # Assurez-vous que cet ID est valide dans le système
API_URL_REGISTER_DEVICE = "http://localhost:5001/iot/devices"  # Endpoint pour enregistrer un appareil IoT
API_URL_SEND_DATA = f"http://localhost:5001/iot/devices/data/{DEVICE_ID}"  # Endpoint pour envoyer les données IoT

# Callback de connexion MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connexion réussie au broker MQTT.")
    else:
        print(f"❌ Échec de connexion. Code : {rc}")

# Initialisation du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.connect("localhost", 1883, 60)
client.loop_start()

# Fonction pour enregistrer un appareil IoT
def register_device():
    payload = {
        "device_id": DEVICE_ID,
        "type": "iot",  # Type d'appareil défini dans le service
        "status": "active"
    }
    
    try:
        response = requests.post(API_URL_REGISTER_DEVICE, json=payload)
        if response.status_code == 201:
            print(f"✅ Appareil IoT enregistré : {payload}")
        elif response.status_code == 409:
            print(f"⚠️ L'appareil existe déjà : {payload}")
        else:
            print(f"⚠️ Erreur lors de l'enregistrement : {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Erreur de connexion à l'API : {e}")

# Simulation des données IoT
def send_iot_data():
    while True:
        temperature = round(random.uniform(20, 30), 2)  # Température aléatoire entre 20 et 30°C
        humidity = round(random.uniform(40, 60), 2)  # Humidité entre 40 et 60%

        # Construction du payload conforme à votre API
        payload = {
            "temperature": temperature,  
            "humidity": humidity,
            "timestamp": datetime.utcnow().isoformat()  # Timestamp au format ISO 8601
        }

        try:
            # Envoi des données à l'API
            response = requests.post(API_URL_SEND_DATA, json=payload)
            if response.status_code == 201:
                print(f"📡 Données envoyées : {payload}")
            else:
                print(f"⚠️ Erreur lors de l'envoi des données : {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"🚨 Erreur de connexion à l'API : {e}")

        time.sleep(5)  # Attente de 5 secondes avant d'envoyer une nouvelle mesure

# Exécution du script
register_device()
send_iot_data()
