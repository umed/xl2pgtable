import psycopg2 as pg
from uploader.database.database_settings import DatabaseSettings
import logging


class Database(object):
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings

    def settings(self) -> DatabaseSettings:
        return self._settings

    def execute(self, command: str):
        try:
            connection = pg.connect(**dict(self._settings))
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            logging.error(
                "Something goes wrong during SQL script execution: {}".format(str(e)))
            exit(1)
