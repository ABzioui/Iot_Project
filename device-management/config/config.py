import os

class Config:
    # PostgreSQL configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:Yahya12%4012@localhost/device_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # RabbitMQ configuration
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
    RABBITMQ_QUEUE = "device_events"

    # Meteo API configuration
    METEO_API_URL = "https://api.open-meteo.com/v1/forecast"
    METEO_API_PARAMS = {
        "latitude": 48.8566,  # Example: Paris latitude
        "longitude": 2.3522,  # Example: Paris longitude
        "hourly": "temperature_2m,relativehumidity_2m",
    }