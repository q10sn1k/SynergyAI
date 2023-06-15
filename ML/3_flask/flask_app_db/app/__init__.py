from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # загружаем конфигурацию
    app.config.from_object('app.config.Config')

    # инициализируем расширения
    db.init_app(app)

    # регистрируем маршруты
    from .routes import bp as main_routes
    app.register_blueprint(main_routes)

    from .routes import user_routes
    app.register_blueprint(user_routes.bp)

    from .routes import order_routes
    app.register_blueprint(order_routes.bp)

    return app
