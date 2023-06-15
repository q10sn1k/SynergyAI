# импортируем SQLAlchemy
from app import db


# определение модели Order
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, nullable=False)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    # возвращает строковое представление объекта
    def __repr__(self):
        return f'<Order {self.product_name}>'
