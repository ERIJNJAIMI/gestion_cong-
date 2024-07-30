import os

class Config:
    # Utilise la variable d'environnement DATABASE_URL si elle est définie, sinon utilise SQLite par défaut
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///gestionconge.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
