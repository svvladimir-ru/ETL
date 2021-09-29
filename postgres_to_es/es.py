import json
import time
from elasticsearch import Elasticsearch
from utils import backoff


class EsSaver:
    def __init__(self, host: list):
        self.client = Elasticsearch(host)
        self.movies_list = []

    def create_index(self, file_path):
        with open(file_path, 'r') as file:
            f = json.load(file)
        self.client.index(index='movies', body=f)

    @backoff()
    def load_data(self):
        self.client.bulk(body='\n'.join(self.movies_list) + '\n', index='movies')

    def load(self, query):
        while query :
            rows = iter(query)
            for row in rows:
                self.movies_list.extend(
                    [
                        json.dumps(
                            {
                                'index': {
                                    '_index': 'movies',
                                    '_id': row['id']
                                }
                            }
                        ),
                        json.dumps(row),
                    ]
                )
                if len(self.movies_list) == 50:
                    self.load_data()
                    self.movies_list.clear()
            self.load_data()
            break
