from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from extensions import db

class User(db.Model):
    __tablename__ = "users"
    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCard = db.Column(db.Integer, unique=True, nullable=False)
    names = db.Column(String(50), nullable=False)
    surnames = db.Column(String(50), nullable=False)
    email = db.Column(String(75), nullable=False)
    password = db.Column(String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    games = relationship("Game", back_populates="user")
    game_has_monsters = relationship("GameHasMonsters", back_populates="user")
    game_has_levels = relationship("GameHasLevel", back_populates="user")

class Game(db.Model):
    __tablename__ = "game"
    idGame = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, ForeignKey("users.idUser"), nullable=False)
    startDate = db.Column(Date, nullable=False)
    endDate = db.Column(Date, nullable=False)
    finalScore = db.Column(db.Integer, nullable=False)

    user = relationship("User", back_populates="games")
    game_has_monsters = relationship("GameHasMonsters", back_populates="game")
    game_has_levels = relationship("GameHasLevel", back_populates="game")

class Level(db.Model):
    __tablename__ = "level"
    idLevel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    difficulty = db.Column(String(20), nullable=False)

    monsters = relationship("Monsters", back_populates="level")
    game_has_levels = relationship("GameHasLevel", back_populates="level")

class Monsters(db.Model):
    __tablename__ = "monsters"
    idMonsters = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idLevel = db.Column(db.Integer, ForeignKey("level.idLevel"), nullable=False)
    name = db.Column(String(50), nullable=False)
    description = db.Column(String(100), nullable=False)

    level = relationship("Level", back_populates="monsters")
    categories = relationship("Category", back_populates="monster")
    game_has_monsters = relationship("GameHasMonsters", back_populates="monster")

class Category(db.Model):
    __tablename__ = "categories"
    idCategory = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMonsters = db.Column(db.Integer, ForeignKey("monsters.idMonsters"), nullable=False)
    category = db.Column(String(65), nullable=False)

    monster = relationship("Monsters", back_populates="categories")
    questions = relationship("Question", back_populates="category")

class Question(db.Model):
    __tablename__ = "questions"
    idQuestion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCategory = db.Column(db.Integer, ForeignKey("categories.idCategory"), nullable=False)  # Agregar clave foránea
    content = db.Column(String(200), nullable=False)

    category = relationship("Category", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(db.Model):
    __tablename__ = "answers"
    idAnswer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idQuestion = db.Column(db.Integer, ForeignKey("questions.idQuestion"), nullable=False)
    answer = db.Column(String(170), nullable=False)
    isCorrect = db.Column(Boolean, nullable=False)

    question = relationship("Question", back_populates="answers")

class GameHasMonsters(db.Model):
    __tablename__ = "game_has_monsters"
    idGameHasMonsters = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idGame = db.Column(db.Integer, ForeignKey("game.idGame"), nullable=False)
    idUser = db.Column(db.Integer, ForeignKey("users.idUser"), nullable=False)
    idMonsters = db.Column(db.Integer, ForeignKey("monsters.idMonsters"), nullable=False)
    idLevel = db.Column(db.Integer, ForeignKey("level.idLevel"), nullable=False)

    game = relationship("Game", back_populates="game_has_monsters")
    user = relationship("User", back_populates="game_has_monsters")
    monster = relationship("Monsters", back_populates="game_has_monsters")

class GameHasLevel(db.Model):
    __tablename__ = "game_has_level"
    idGameHasLevel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idGame = db.Column(db.Integer, ForeignKey("game.idGame"), nullable=False)
    idUser = db.Column(db.Integer, ForeignKey("users.idUser"), nullable=False)
    idLevel = db.Column(db.Integer, ForeignKey("level.idLevel"), nullable=False)

    game = relationship("Game", back_populates="game_has_levels")
    user = relationship("User", back_populates="game_has_levels")
    level = relationship("Level", back_populates="game_has_levels")