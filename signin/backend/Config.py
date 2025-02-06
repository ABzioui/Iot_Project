import os

class Config:
    """Configuration de base pour l'application Flask."""
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Yahya12%4012@localhost:5432/user_service'
    REDIS_URL = 'redis://localhost:6379/0'
