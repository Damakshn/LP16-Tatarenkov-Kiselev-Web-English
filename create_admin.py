from getpass import getpass
import sys
from config import DevConfig
from web_english import create_app, db
from web_english.models import User

app = create_app(DevConfig)

with app.app_context():
    username = input("Введите имя: ")
    if User.query.filter(User.username == username).count():
        print("Пользователь с таким именем уже есть.")
        sys.exit(0)
    password = getpass("Введите пароль: ")
    password2 = getpass("Повторите пароль: ")
    if password != password2:
        print("Пароль повторён неверно.")
        sys.exit(0)
    email = input("Введите e-mail: ")
    if User.query.filter(User.email == email).count():
        print("Этот e-mail уже используется.")
        sys.exit(0)
    new_user = User(username=username, password=password, email=email, role=User.USER_ROLE_ADMIN)
    db.session.add(new_user)
    db.session.commit()
    print(f"Создан новый пользователь {new_user.username} id={new_user.id}")
