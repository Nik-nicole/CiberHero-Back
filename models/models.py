from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from extensions import db

class User(db.Model):
    __tablename__ = "users"
    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCard = db.Column(db.Integer, unique=True, nullable=False)
    names = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    games = relationship("Game", back_populates="user", cascade="all, delete-orphan")
   
class Game(db.Model):
    __tablename__ = "game"
    idGame = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, ForeignKey("users.idUser", ondelete="CASCADE"), nullable=False)
    idMonsters = db.Column(db.Integer, ForeignKey("monsters.idMonsters", ondelete="CASCADE"))
    idLevel = db.Column(db.Integer, ForeignKey("level.idLevel", ondelete="CASCADE"))
    startDate = db.Column(Date, nullable=False)
    endDate = db.Column(Date, nullable=False)
    finalScore = db.Column(db.Integer, nullable=False)

    user = relationship("User", back_populates="games")

class Level(db.Model):
    __tablename__ = "level"
    idLevel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    difficulty = db.Column(db.String(20), nullable=False)

    monsters = relationship("Monsters", back_populates="level")

class Monsters(db.Model):
    __tablename__ = "monsters"
    idMonsters = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idLevel = db.Column(db.Integer, ForeignKey("level.idLevel", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    level = relationship("Level", back_populates="monsters")
    categories = relationship("Category", back_populates="monster")

class Category(db.Model):
    __tablename__ = "categories"
    idCategory = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMonsters = db.Column(db.Integer, ForeignKey("monsters.idMonsters", ondelete="CASCADE"), nullable=False)
    category = db.Column(db.String(65), nullable=False)

    monster = relationship("Monsters", back_populates="categories")
    questions = relationship("Question", back_populates="category")

class Question(db.Model):
    __tablename__ = "questions"
    idQuestion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCategory = db.Column(db.Integer, ForeignKey("categories.idCategory", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    category = relationship("Category", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(db.Model):
    __tablename__ = "answers"
    idAnswer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idQuestion = db.Column(db.Integer, ForeignKey("questions.idQuestion", ondelete="CASCADE"), nullable=False)
    answer = db.Column(db.String(170), nullable=False)
    isCorrect = db.Column(Boolean, nullable=False)

    question = relationship("Question", back_populates="answers")