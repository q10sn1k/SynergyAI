import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Order

load_dotenv()

app = create_app()
app.app_context().push()


def random_string(length=5):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for _ in range(length))


def fill_database():
    db.create_all()

    # Добавляем пользователей
    users = []
    for _ in range(100):
        user = User(
            name=f'{random_string()} {random_string()}',
            email=f'{random_string()}@example.com',
            age=random.randint(18, 80),
            country=random_string().capitalize(),
            balance=random.uniform(0, 10000)
        )
        users.append(user)
        db.session.add(user)

    db.session.commit()

    # Добавляем заказы
    for _ in range(100):
        order = Order(
            user_id=random.choice(users).id,
            product_name=f'Товар-{random_string(3)}',
            price=random.uniform(10, 1000),
            quantity=random.randint(1, 10),
            order_date=datetime.utcnow() - timedelta(days=random.randint(0, 365))
        )
        db.session.add(order)

    db.session.commit()


if __name__ == '__main__':
    fill_database()
