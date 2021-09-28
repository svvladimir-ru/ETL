import json
from datetime import datetime
from elasticsearch import Elasticsearch


class EsSaver:
    def __init__(self, host: list, query: list):
        self.client = Elasticsearch(host)
        self.query = query
        self.movies_list = []

    def create_index(self, file_path):
        with open(file_path, 'r') as file:
            f = json.load(file)
            self.client.index(f)

    def load(self):
        while self.query:
            rows = iter(self.query)
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
                self.movies_list.extend(row)
                if len(self.movies_list) == 50:
                    self.es.bulk(body='\n'.join(self.movies_list) + '\n', index='movies')
                    self.movies_list().clear()

        return self.movies_list
