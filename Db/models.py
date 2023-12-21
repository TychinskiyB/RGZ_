from . import db
from flask_login import UserMixin

#Таблица пользователи 
class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(102), nullable=False)
    admin_on_off = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, admin_on_off:{self.admin_on_off}"

#Таблица книги
class book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_book = db.Column(db.String(100), nullable=False)
    photo_link = db.Column(db.String, nullable=True)
    avtor = db.Column(db.String, nullable=False)
    izdatelstvo = db.Column(db.String, nullable=False)
    ks= db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"id:{self.id}, name_book:{self.name_book}, photo_link:{self.photo_link}, avtor:{self.avtor}, izdatelstvo:{self.izdatelstvo}, ks:{self.ks}"