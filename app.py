from flask import Flask
from flask_migrate import Migrate
from models.models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)

    return app