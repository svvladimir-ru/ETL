Для запуска сервиса выполнить следующие шаги:

### Авто запуск
1. Клонируем репозиторий
2. Создаем виртуальное окружение python -m venv venv
3. Выполняем команду ```pip install -r requirements.txt```
4. В консоле запускаем ./up.sh (Файл должен быть исполняемым chmod +x ./up.sh)
5. Пользуемся и радуемся)

### Ручной запуск
1. Клонируем репозиторий
2. Создаем виртуальное окружение python -m venv venv
 
Далее выполняем компанды:
```
- source venv/bin/activate
- pip install -r requirements.txt
- cp .env.sample sqlite_to_postgres/.env
- cp .env.sample movies_admin/.env
- docker-compose up --build -d ma_postgres
- python ./sqlite_to_postgres/load_data.py
- docker-compose up --build -d ma_web
- docker-compose up --build ma_nginx
```
