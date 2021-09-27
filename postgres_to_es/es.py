import json
from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch([
    {
        'host': '127.0.0.1',
        'port': 9200
    }
])

with open('schemas.json', 'r') as file:
    f = json.load(file)

es.index(f)
