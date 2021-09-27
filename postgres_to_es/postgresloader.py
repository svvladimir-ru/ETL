from psycopg2.extensions import connection as _connection
import psycopg2
import time
from psycopg2.extras import DictCursor
from psycopg2 import sql
import pprint

pp = pprint.PrettyPrinter(indent=4)


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.counter = 0

    def loader(self):

        load_person = f'''SELECT id
                            FROM content.person
                            ORDER BY updated_at
                            LIMIT 100'''


        load_film = f'''SELECT fw.id
                            FROM content.film_work as fw
                            LEFT JOIN content.person_film_work as pfw ON pfw.film_work_id = fw.id
                            WHERE pfw.person_id IN ({load_person})
                            ORDER BY fw.updated_at
                            LIMIT 100'''

        self.cursor.execute(f'''SELECT fw.id, fw.title, fw.description, fw.rating, fw.type, fw.created_at,
                                      fw.updated_at, pfw.role, p.id, p.full_name, g.name
                                        FROM content.film_work as fw
                                        LEFT JOIN content.person_film_work as pfw ON pfw.film_work_id = fw.id
                                        LEFT JOIN content.person as p ON p.id = pfw.person_id
                                        LEFT JOIN content.genre_film_work as gfw ON gfw.film_work_id = fw.id
                                        LEFT JOIN content.genre as g ON g.id = gfw.genre_id
                                        WHERE fw.id IN ({load_film});''')

        data = self.cursor.fetchall()
        return data



dsl = {
    'dbname': 'movies',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432,
}

if __name__ == '__main__':

    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        pp.pprint(PostgresSaver(pg_conn).loader())

    pg_conn.close()
