import psycopg2
import time
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config import dsl, es_conf
from postgresloader import PostgresLoader
from utils import backoff
from es import EsSaver
import pprint

pp = pprint.PrettyPrinter(indent=4)


def load_from_postgres(pg_conn: _connection) -> list:
    """Основной метод загрузки данных из Postgres"""
    postgres_saver = PostgresLoader(pg_conn)
    data = postgres_saver.loader()
    return data


if __name__ == '__main__':
    @backoff()
    def query_postgres():
        with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_pq = load_from_postgres(pg_conn)
        pg_conn.close()
        return load_pq

    @backoff()
    def save_elastic():
        # EsSaver(es_conf).create_index('schemas.json')
        EsSaver(es_conf).load(query_postgres())

    save_elastic()
