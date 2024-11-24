from flask import Flask
from flask_migrate import Migrate
from config import Config
from models.models import db
from extensions import db
from routes.userRoute import user_bp
from routes.gameRoute import game_bp
from routes.levelRoute import level_bp
from routes.monsterRoute import monster_bp
from routes.categoryRoute import category_bp
from routes.questionRoute import question_bp
from routes.answerRoute import answer_bp
from routes.gameHasMonsters import gameHasMonsters_bp
from routes.gameHasLevels import gameHasLevels_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(user_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(level_bp)
    app.register_blueprint(monster_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(answer_bp)
    app.register_blueprint(gameHasMonsters_bp)
    app.register_blueprint(gameHasLevels_bp)

    return app