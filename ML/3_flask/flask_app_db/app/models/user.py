# импортируем SQLAlchemy
from app import db


# определение модели User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    # возвращает строковое представление объекта
    def __repr__(self):
        return f'<User {self.name}>'
