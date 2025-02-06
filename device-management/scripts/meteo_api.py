import requests
import time

DEVICE_ID = "api_device_7"  # Example device ID
API_URL = f"http://localhost:5001/api/devices/data/{DEVICE_ID}"
LATITUDE = 48.8566  # Paris
LONGITUDE = 2.3522  # Paris

def fetch_meteo_data():
    """
    Récupère les données météo depuis Open-Meteo.
    """
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "hourly": "temperature_2m,precipitation,relativehumidity_2m",
        })
        response.raise_for_status()
        data = response.json()

        # Extraction des valeurs pour l'heure actuelle
        current_hour = 0
        temperature = data["hourly"]["temperature_2m"][current_hour]
        precipitation = data["hourly"]["precipitation"][current_hour]
        humidity = data["hourly"]["relativehumidity_2m"][current_hour]

        # Retourne un dictionnaire avec les valeurs météo
        return {
            "temperature": temperature,
            "precipitation": precipitation,
            "humidity": humidity,
            "location_lat": LATITUDE,
            "location_lon": LONGITUDE
        }
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur API Météo : {e}")
        return None

def send_meteo_data():
    """
    Envoie les données météorologiques avec latitude & longitude.
    """
    while True:
        meteo_data = fetch_meteo_data()
        if meteo_data:
            payload = {
                "device_id": DEVICE_ID,
                "status": "active",  # You can set the status here (if needed)
                "location_lat": meteo_data["location_lat"],
                "location_lon": meteo_data["location_lon"],
                "monitored_params": ["temperature", "humidity", "precipitation"],  # Optional params to monitor
                "temperature": meteo_data["temperature"],
                "precipitation": meteo_data["precipitation"],
                "humidity": meteo_data["humidity"]
            }
            
            # Send data to the API
            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                print(f"📡 Données météo envoyées pour le dispositif {DEVICE_ID}: {payload}")
            except requests.exceptions.RequestException as e:
                print(f"🚨 Erreur d'envoi des données : {e}")
        else:
            print("❌ Impossible de récupérer les données météo.")

        time.sleep(10)  # Rafraîchissement toutes les 10 secondes

if __name__ == "__main__":
    send_meteo_data()
