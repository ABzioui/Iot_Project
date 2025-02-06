import requests
import psutil
import time
import socket

DEVICE_ID = "pc_device_1012"
API_URL = f"http://localhost:5001/end_device/devices/data/{DEVICE_ID}"  # Updated URL to match your controller
API_URL_REGISTER_DEVICE = "http://localhost:5001/end_device/devices"  # Endpoint pour enregistrer un appareil IoT

def get_system_data():
    """Récupère les statistiques système (CPU, RAM, Disque)"""
    return {
        "ip_address": socket.gethostbyname(socket.gethostname()),  # ✅ Adresse IP
        "cpu_load": psutil.cpu_percent(interval=1),  # ✅ Charge CPU (%)
        "memory_usage": psutil.virtual_memory().percent,  # ✅ Mémoire utilisée (%)
        "disk_usage": psutil.disk_usage('/').percent  # ✅ Espace disque utilisé (%)
    }

def send_system_data():
    """Envoie les données système au serveur toutes les minutes."""
    while True:
        system_data = get_system_data()
        payload = {
            "ip_address": system_data["ip_address"],
            "cpu_load": system_data["cpu_load"],
            "memory_usage": system_data["memory_usage"],
            "disk_usage": system_data["disk_usage"],
            "status": "active",  # Assuming the device status is active by default
            # Optional: monitored_params could be added here if necessary
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            print(f"📡 Données système envoyées : {payload}")
        except requests.exceptions.RequestException as e:
            print(f"🚨 Erreur d'envoi des données : {e}")
        
        time.sleep(10)  # Envoi toutes les 60 secondes

def register_device():
    payload = {
        "device_id": DEVICE_ID,
        "type": "end_device",  # Type d'appareil défini dans le service
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

if __name__ == "__main__":
    register_device()
    send_system_data()
