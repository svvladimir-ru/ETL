import psycopg2
import time
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config import dsl
from postgresloader import PostgresLoader
from utils import backoff
import pprint

pp = pprint.PrettyPrinter(indent=4)


def load_from_postgres(pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresLoader(pg_conn)
    pp.pprint(postgres_saver.loader())

    # data = sqlite_loader.load_movies()
    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    @backoff()
    def query_postgres():
        with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_postgres(pg_conn)

        pg_conn.close()


    query_postgres()
