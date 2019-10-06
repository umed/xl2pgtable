import logging
import psycopg2 as pg
import sys
from typing import List

from uploader.database.database_settings import DatabaseSettings


class SqlExecutor:
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings

    def execute(self, command: str) -> List[tuple]:
        connection = None
        cursor = None
        try:
            connection = pg.connect(**dict(self._settings))
            cursor = connection.cursor()
            cursor.execute(command)
            data = []
            if cursor.statusmessage.startswith('SELECT '):
                data = cursor.fetchall()
            connection.commit()
            return data
        except Exception as e:
            logging.error(
                "Something goes wrong during SQL script execution: {}".format(str(e)))
            sys.exit(1)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
