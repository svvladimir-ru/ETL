from psycopg2.extensions import connection as _connection
import psycopg2
from datetime import datetime
import time
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, Json
from config import dsl, es_conf
from state import JsonFileStorage, State
from uuid import uuid4
from big_awful_request import big_request
import pprint
from schemas import FilmWorkWithoutField
import json


pp = pprint.PrettyPrinter(indent=4)


class PostgresLoader:
    def __init__(self, pg_conn: _connection, state_bd=False):
        self.conn = pg_conn
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.batch_size = 100
        self.state_bd = state_bd
        # self.time =

    def load_person_id(self) -> str:
        """Вложенный запрос на получение id персон, думаю функция тут лишняя """
        load_person_id = f'''SELECT DISTINCT id
                            FROM content.person
                            GROUP BY id
                            '''
        if self.state_bd:
            return load_person_id
        inx = load_person_id.find('ORDER')
        return f'{load_person_id[inx:]} WHERE updated_at > {time}\n {load_person_id[:inx]}'

    def load_film_work_id(self) -> str:
        """Вложенный запрос на получение id фильмворков"""
        load_film_id = f'''SELECT DISTINCT fw.id
                            FROM content.film_work as fw
                            LEFT JOIN content.person_film_work as pfw ON pfw.film_work_id = fw.id
                            WHERE pfw.person_id IN ({self.load_person_id()})
                            GROUP BY fw.id
                            '''
        if self.state_bd:
            return load_film_id

        inx = load_film_id.find('ORDER')
        return f'{load_film_id[inx:]} AND updated_at > {time}\n {load_film_id[:inx]}'

    def loader(self) -> list:
        """Запрос на получение всех данных"""
        full_load = f'''SELECT DISTINCT fw.id, fw.title, fw.description, fw.rating, fw.type,
                                  fw.updated_at, {big_request}
                                    FROM content.film_work as fw
                                    LEFT JOIN content.person_film_work as pfw ON pfw.film_work_id = fw.id
                                    LEFT JOIN content.person as p ON p.id = pfw.person_id
                                    LEFT JOIN content.genre_film_work as gfw ON gfw.film_work_id = fw.id
                                    LEFT JOIN content.genre as g ON g.id = gfw.genre_id
                                    WHERE fw.id IN ({self.load_film_work_id()})
                                    GROUP BY fw.id, fw.title, fw.description, fw.rating, fw.type,
                                             fw.updated_at, pfw.role, p.id, p.full_name, g.name
                                    ORDER BY fw.updated_at;'''
        if self.state_bd:
            self.cursor.execute(full_load)
        else:
            inx = full_load.rfind('IN')
            self.cursor.execute(f'{full_load[inx + 1:]} (updated_at > {time}) AND {full_load[:inx]}')

        while True:
            rows = self.cursor.fetchmany()
            if not rows:
                break

            for row in rows:
                # print(dict(row))
                # try:
                # a = {}
                #
                # a[f"{str(datetime.now()).replace(' ', '')}"]= dict(row)
                # pp.pprint(a)
                c = FilmWorkWithoutField(
                    id              = dict(row).get('id'),
                    imdb_rating     = dict(row).get('rating'),
                    title           = dict(row).get('title'),
                    description     = dict(row).get('description'),
                    actors_names    = dict(row).get('actors_names'),
                    writers_names   = dict(row).get('writers_names'),
                    directors_names = dict(row).get('directors_names'),
                    genres_names    = dict(row).get('genre'),
                    actors          = dict(row).get('actors'),
                    writers         = dict(row).get('writers'),
                    directors       = dict(row).get('directors'),
                )
                a = {}
                a[f"{str(datetime.now()).replace(' ', '')}"] = c.dict()

                print(json.dumps(a))
                # State(JsonFileStorage(file_path='PostgresData.json')).set_state(
                #     key=f"{str(datetime.now()).replace(' ', '')}", value=c.dict())
                # except:
                #     with open('error.txt' 'w') as file:
                #         file.writelines(row)
            # i = {}
            # i[f"{str(datetime.now()).replace(' ', '')}"] = rows
            # pp.pprint(i)
            # count = 0
            # if count == 2:
            #     break
            # count += 1
            break
            # State(JsonFileStorage(file_path='PostgresData.json')).set_state(
            #     key=f"{str(datetime.now()).replace(' ', '')}", value=rows)

