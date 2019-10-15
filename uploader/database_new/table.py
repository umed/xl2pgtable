from uploader.database.database_utils import py_type_to_pg_type
from uploader.database import Database


class Table(object):
    def __init__(self, db: Database, name: str, columns: dict):
        self._columns = columns
        self._name = name
        self._db = db

    def to_sql(self):
        columns_definition_list = []
        for column_name, column_type in self._columns.items():
            column_definition = '{} {}'.format(
                column_name, py_type_to_pg_type(column_type))
            columns_definition_list.append(column_definition)
        columns_definition = ', '.join(columns_definition_list)
        command = 'create table {}.{} ({})'.format(
            self._db._settings.schema, self._name, columns_definition)
        return command
