import time
from psycopg2.extensions import connection as _connection


class PostgresLoader:
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.batch_size = 100

    def load_person_id(self, time=None) -> str:
        load_person_id = f'''SELECT id
                            FROM content.person
                            ORDER BY updated_at
                            '''
        return load_person_id

    def load_film_work_id(self) -> str:
        load_film_id = f'''SELECT fw.id
                            FROM content.film_work as fw
                            LEFT JOIN content.person_film_work as pfw ON pfw.film_work_id = fw.id
                            WHERE pfw.person_id IN ({self.load_person_id()})
                            ORDER BY fw.updated_at
                            '''
        return load_film_id

    def loader(self) -> list:
        self.cursor.execute(f'''SELECT fw.id, fw.title, fw.description, fw.rating, fw.type, fw.created_at,
                                      fw.updated_at, pfw.role, p.id, p.full_name, g.name
                                        FROM content.film_work as fw
                                        LEFT JOIN content.person_film_work as pfw ON pfw.film_work_id = fw.id
                                        LEFT JOIN content.person as p ON p.id = pfw.person_id
                                        LEFT JOIN content.genre_film_work as gfw ON gfw.film_work_id = fw.id
                                        LEFT JOIN content.genre as g ON g.id = gfw.genre_id
                                        WHERE fw.id IN ({self.load_film_work_id()});''')

        data = []
        while True:
            rows = self.cursor.fetchmany(self.batch_size)
            data.append(rows)
            if not rows:
                break

        return data
