import datetime
from pytz import lazy
from fakepinterest import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(id_usuario)

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    nome = database.Column(database.String(50), nullable=False)
    usuario = database.Column(database.String(50), nullable=False)
    senha = database.Column(database.String(50), nullable=False)
    email = database.Column(database.String(50), nullable=False, unique=True)
    fotos = database.relationship('Foto', backref='usuario', lazy=True)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.datetime.now())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)