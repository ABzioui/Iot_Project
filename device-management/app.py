from flask import Flask
from flask_cors import CORS  # Ajout de Flask-CORS
from controllers.device_controller import device_blueprint
from config.config import Config
from models.models import db

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

app.config.from_object(Config)  # Chargement de la configuration

# Initialisation de la base de données
db.init_app(app)
with app.app_context():
    db.create_all()

# Enregistrement du blueprint des devices
app.register_blueprint(device_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
