import os
import logging

from dotenv import load_dotenv

load_dotenv()

# Logging settings
logging.basicConfig(filename='etl.log', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT'),
}

es_conf = [{
    'host': os.getenv('ES_HOST'),
    'port': os.getenv('ES_PORT'),
}]
