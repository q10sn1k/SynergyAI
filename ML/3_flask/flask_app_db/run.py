# импортируем объект приложения
from app import create_app

app = create_app()

# запускаем сервер
if __name__ == '__main__':
    app.run()
