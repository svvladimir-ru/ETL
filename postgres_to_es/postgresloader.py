from datetime import datetime
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from state import JsonFileStorage, State
from big_awful_request import big_request
from schemas import FilmWorkWithoutField


class PostgresLoader:
    """Класс для выгрузки данных из postgres"""
    def __init__(self, pg_conn: _connection, state_key='my_key'):
        self.conn = pg_conn
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.batch_size = 100
        self.key = state_key
        self.state_key = State(JsonFileStorage('PostgresData.txt')).get_state(state_key)
        self.data = []

    def load_person_id(self) -> str:
        """Вложенный запрос на получение id персон, думаю функция тут лишняя """
        load_person_id = f'''SELECT DISTINCT id
                            FROM content.person
                            GROUP BY id
                            '''
        return load_person_id

    def load_film_work_id(self) -> str:
        """Вложенный запрос на получение id фильмворков"""
        load_film_id = f'''SELECT DISTINCT fw.id
                            FROM content.film_work as fw
                            LEFT JOIN content.person_film_work as pfw ON pfw.film_work_id = fw.id
                            WHERE pfw.person_id IN ({self.load_person_id()})
                            GROUP BY fw.id
                            '''
        if self.state_key is None:
            return load_film_id
        inx = load_film_id.rfind(f'WHERE pfw.person_id IN ({self.load_person_id()})')
        return f"{load_film_id[:inx]} AND updated_at > '{self.state_key}' {load_film_id[inx:]}"


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
                                    GROUP BY fw.id
                                    ORDER BY fw.updated_at;'''
        self.cursor.execute(full_load)

        while True:
            rows = self.cursor.fetchmany(self.batch_size)
            if not rows:
                break

            for row in rows:
                d = FilmWorkWithoutField(
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
                self.data.append(d.dict())
        State(JsonFileStorage('PostgresData.txt')).set_state(str(self.key), value=str(datetime.now()))

        return self.data
