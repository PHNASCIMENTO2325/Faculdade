from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.String(255), nullable=False)
    opcao_a = db.Column(db.String(255), nullable=False)
    opcao_b = db.Column(db.String(255), nullable=False)
    opcao_c = db.Column(db.String(255), nullable=False)
    opcao_d = db.Column(db.String(255), nullable=False)
    correta = db.Column(db.String(1), nullable=False)
