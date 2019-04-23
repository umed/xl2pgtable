# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:09:51 2019

@author: PuchkovaKS
"""

import psycopg2 as pg
import logging
from database_settings import DatabaseSettings
import datetime as dt


def __str_or_NULL(value):
    if value is not None:
        return str(value)
    else:
        return 'NULL'


PG_SQL_TYPES_TO_PYTHON_TYPES = {
    int: {
        'type': 'integer',
        'converter': lambda value: __str_or_NULL(value)
    },
    float: {
        'type': 'real',
        'converter': lambda value: __str_or_NULL(value)
    },
    str: {
        'type': 'varchar',
        'converter': lambda value: "'{}'".format(__str_or_NULL(value))
    },
    dt.time: {
        'type': 'time',
        'converter': lambda value: "'{}'".format(__str_or_NULL(value))
    },
    dt.datetime: {
        'type': 'timestamp',
        'converter': lambda value: "to_timestamp('{}', 'dd.mm.yyyy hh24:mi:ss')".format(value)
    },
    dt.date: {
        'type': 'date',
        'converter': lambda value: "to_date('{}', 'dd.mm.yyyy')".format(value)
    }
}

class DatabaseHelper(object):
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings

    def execute(self, command: str):
        try:
            connection = pg.connect(**dict(self._settings))
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            logging.error("Something goes wrong during SQL script execution: {}".format(str(e)))
            exit(1)

    @staticmethod
    def __to_pg_str(value_type, value) -> str:
        return PG_SQL_TYPES_TO_PYTHON_TYPES[value_type]['converter'](value)

    @staticmethod
    def __pg_type(t: type) -> str:
        return PG_SQL_TYPES_TO_PYTHON_TYPES[t]['type']

    @staticmethod
    def __row_to_insert_str(columns: dict, row: dict) -> str:
        values = ', '.join([DatabaseHelper.__to_pg_str(columns[key], value) for key, value in row.items()])
        return '({})'.format(values)

    @staticmethod
    def __rows_to_insert_str(columns: dict, rows: list) -> str:
        return ', '.join([DatabaseHelper.__row_to_insert_str(columns, row) for row in rows])

    @staticmethod
    def __create_insert_query(table_name: str, columns: dict, data: list) -> str:
        return 'insert into {} values {}'.format(table_name, DatabaseHelper.__rows_to_insert_str(columns, data))

    def __create_table(self, name, columns: dict):
        columns_definition_list = []
        for column_name, column_type in columns.items():
            column_definition = '{} {}'.format(column_name, DatabaseHelper.__pg_type(column_type))
            columns_definition_list.append(column_definition)
        columns_definition = ', '.join(columns_definition_list)
        command = 'create table {} ({})'.format(name, columns_definition)
        self.execute(command)

    def __insert_rows(self, name: str, columns: dict, data: list):
        insert_query = DatabaseHelper.__create_insert_query(name, columns, data)
        self.execute(insert_query)

    def create_table(self, name: str, columns: dict, data: list):
        self.__create_table(name, columns)
        self.__insert_rows(name, columns, data)

    def rewrite_data(self, table_name: str,  data: list):
        pass
        # self.execute('trancate {}'.format(table_name))
        # self.__create_insert_query()
