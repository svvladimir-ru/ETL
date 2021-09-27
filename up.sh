#!/bin/bash
echo "Запуск postgres"
docker-compose up --build -d ma_postgres
sleep 5
echo "Начало загрузки данных в postgres"
cp .env.sample sqlite_to_postgres/.env
cp .env.sample movies_admin/.env
cd sqlite_to_postgres/ || exit
../venv/bin/python load_data.py
cd ..
echo "Старт Админки"
docker-compose up --build -d ma_web
docker exec -it ma_web bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput"
echo "Запуск Nginx"
docker-compose up --build ma_nginx