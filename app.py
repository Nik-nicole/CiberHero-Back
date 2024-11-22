from flask import Flask
from flask_migrate import Migrate
from config import Config
from models.models import db
from routes.userRoute import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(user_bp)

    return app