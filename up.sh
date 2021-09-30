#!/bin/bash
echo "Запуск postgres"
docker-compose up --build -d ma_postgres
sleep 5
echo "Начало загрузки данных в postgres"
cp .env.sample sqlite_to_postgres/.env
cp .env.sample movies_admin/.env
cp .env.sample postgres_to_es/.env
cd sqlite_to_postgres/ || exit
../venv/bin/python load_data.py
cd ..
echo "Старт Админки"
docker-compose up --build -d ma_web
docker exec -it ma_web bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput"
echo "Запуск Nginx"
docker-compose up --build -d ma_nginx
echo "Запуск ETL"
mkdir postgres_to_es/volumes
mkdir ./elasticdb
touch postgres_to_es/volumes/etl.log
docker-compose up --build -d ma_es01
docker-compose up --build -d ma_etl