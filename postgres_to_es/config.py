import os

from dotenv import load_dotenv

load_dotenv()

dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.environ.get('PG_HOST'),
    'port': os.environ.get('POSTGRES_PORT'),
}

es_conf = [{
    'host': os.getenv('ES_HOST'),
    'port': os.getenv('ES_PORT'),
}]
