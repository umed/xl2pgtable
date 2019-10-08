import logging
import sys
from typing import List

import psycopg2 as pg

from uploader.database.database_settings import DatabaseSettings
from uploader.database.database_utils import py_type_to_pg_type, py_value_to_pg_value


class Database(object):
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

    @staticmethod
    def __row_to_insert_str(columns: dict, row: dict) -> str:
        values = ', '.join([py_value_to_pg_value(columns[key], value) for key, value in row.items()])
        return '({})'.format(values)

    @staticmethod
    def __rows_to_insert_str(columns: dict, rows: list) -> str:
        rows_to_insert_list = [Database.__row_to_insert_str(columns, row) for row in rows]
        return ', '.join(rows_to_insert_list)

    def __create_insert_query(self, table_name: str, columns: dict, data: list) -> str:
        rows_to_insert_str = Database.__rows_to_insert_str(columns, data)
        return 'insert into {}.{} values {}'.format(self._settings.schema, table_name, rows_to_insert_str)

    def __create_table(self, name, columns: dict):
        columns_definition_list = []
        for column_key, column_value in columns.items():
            column_mapping = column_value.get('mapping', None)
            column_name = column_mapping['name'] if column_mapping and column_mapping['name'] else column_value['name']
            column_type = column_mapping['type'] if column_mapping and column_mapping['type'] else py_type_to_pg_type(
                column_value['type'])
            column_definition = '{} {}'.format(column_name, column_type)
            columns_definition_list.append(column_definition)
        columns_definition = ', '.join(columns_definition_list)
        command = 'create table {}.{} ({})'.format(self._settings.schema, name, columns_definition)
        print(command)
        self.execute(command)
        print('Table "{}" was created/updated'.format(name))

    def __insert_rows(self, name: str, columns: dict, data: list):
        insert_query = self.__create_insert_query(name, columns, data)
        self.execute(insert_query)
        print('Rows inserted to table {}'.format(name))

    def create_table(self, name: str, columns: dict, data: list):
        self.__create_table(name, columns)
        self.__insert_rows(name, columns, data)

    def rewrite_data(self, table_name: str, columns: dict, data: list, drop_if_exists: bool = False):
        if drop_if_exists:
            command_to_drop_table = 'DROP TABLE IF EXISTS {}.{};'.format(self._settings.schema, table_name)
            self.execute(command_to_drop_table)
            self.create_table(table_name, columns, data)
        else:
            command = "SELECT exists(SELECT 1 FROM information_schema.tables WHERE " \
                      "table_schema = '{}' AND table_name = '{}')".format(self._settings.schema, table_name)
            result = self.execute(command)
            if len(result) > 0 and len(result[0]) > 0 and result[0][0]:
                self.execute('TRUNCATE {}.{}'.format(self._settings.schema, table_name))
                self.__insert_rows(table_name, columns, data)
            else:
                self.create_table(table_name, columns, data)
