from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    idUser = Column(Integer, primary_key=True, autoincrement=True)
    idCard = Column(Integer, unique=True, nullable=False)
    names = Column(String(50), nullable=False)
    surnames = Column(String(50), nullable=False)
    email = Column(String(75), nullable=False)
    password = Column(String(255), nullable=False)
    score = Column(Integer, nullable=False)

    games = relationship("Game", back_populates="user")
    game_has_monsters = relationship("GameHasMonsters", back_populates="user")
    game_has_levels = relationship("GameHasLevel", back_populates="user")

class Game(db.Model):
    __tablename__ = "game"
    idGame = Column(Integer, primary_key=True, autoincrement=True)
    idUser = Column(Integer, ForeignKey("users.idUser"), nullable=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    finalScore = Column(Integer, nullable=False)

    user = relationship("User", back_populates="games")
    game_has_monsters = relationship("GameHasMonsters", back_populates="game")
    game_has_levels = relationship("GameHasLevel", back_populates="game")

class Level(db.Model):
    __tablename__ = "level"
    idLevel = Column(Integer, primary_key=True, autoincrement=True)
    difficulty = Column(String(20), nullable=False)

    monsters = relationship("Monsters", back_populates="level")
    game_has_levels = relationship("GameHasLevel", back_populates="level")

class Monsters(db.Model):
    __tablename__ = "monsters"
    idMonsters = Column(Integer, primary_key=True, autoincrement=True)
    idLevel = Column(Integer, ForeignKey("level.idLevel"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)

    level = relationship("Level", back_populates="monsters")
    categories = relationship("Category", back_populates="monster")
    game_has_monsters = relationship("GameHasMonsters", back_populates="monster")

class Category(db.Model):
    __tablename__ = "categories"
    idCategory = Column(Integer, primary_key=True, autoincrement=True)
    idMonsters = Column(Integer, ForeignKey("monsters.idMonsters"), nullable=False)
    category = Column(String(65), nullable=False)

    monster = relationship("Monsters", back_populates="categories")
    questions = relationship("Question", back_populates="category")

class Question(db.Model):
    __tablename__ = "questions"
    idQuestion = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200), nullable=False)

    category = relationship("Category", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(db.Model):
    __tablename__ = "answers"
    idAnswer = Column(Integer, primary_key=True, autoincrement=True)
    idQuestion = Column(Integer, ForeignKey("questions.idQuestion"), nullable=False)
    answer = Column(String(170), nullable=False)
    isCorrect = Column(Boolean, nullable=False)

    question = relationship("Question", back_populates="answers")

class GameHasMonsters(db.Model):
    __tablename__ = "game_has_monsters"
    idGameHasMonsters = Column(Integer, primary_key=True, autoincrement=True)
    idGame = Column(Integer, ForeignKey("game.idGame"), nullable=False)
    idUser = Column(Integer, ForeignKey("users.idUser"), nullable=False)
    idMonsters = Column(Integer, ForeignKey("monsters.idMonsters"), nullable=False)
    idLevel = Column(Integer, ForeignKey("level.idLevel"), nullable=False)

    game = relationship("Game", back_populates="game_has_monsters")
    user = relationship("User", back_populates="game_has_monsters")
    monster = relationship("Monsters", back_populates="game_has_monsters")

class GameHasLevel(db.Model):
    __tablename__ = "game_has_level"
    idGameHasLevel = Column(Integer, primary_key=True, autoincrement=True)
    idGame = Column(Integer, ForeignKey("game.idGame"), nullable=False)
    idUser = Column(Integer, ForeignKey("users.idUser"), nullable=False)
    idLevel = Column(Integer, ForeignKey("level.idLevel"), nullable=False)

    game = relationship("Game", back_populates="game_has_levels")
    user = relationship("User", back_populates="game_has_levels")
    level = relationship("Level", back_populates="game_has_levels")