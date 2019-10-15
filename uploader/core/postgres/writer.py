from uploader.core.common.type_recognizer import TypeRecognizer
from uploader.base import IWriter, IData, ITypeRecognizer
from uploader.core.postgres.sql_executor import SqlExecutor
from uploader.core.postgres.sql_representer import SqlRepresenter


class Writer(IWriter):
    def __init__(self, settings=None, type_recognizer: ITypeRecognizer = TypeRecognizer()):
        # FIXME: inject type recognizer
        self._type_recognizer = type_recognizer
        self._executor = SqlExecutor(settings)

    def write(self, data: IData, mapping: dict, append: bool = False, drop_if_exists: bool = False):
        data.set_type_recognizer(self._type_recognizer)
        representer = SqlRepresenter(data)
        self._executor.execute(representer.scheme()['create'])
        self._executor.execute(representer.data()['query'])

    def dd(self, drop_if_exists: bool = False):
        if drop_if_exists:
            command_to_drop_table = 'DROP TABLE IF EXISTS {}.{};'.format(self._settings.schema, table_name)
            self.execute(command_to_drop_table)
            self.create_table(table_name, columns, data)
        else:
            command = "SELECT exists(SELECT 1 FROM information_schema.tables WHERE " \
                      "table_schema = '{}' AND table_name = '{}')".format(self._settings.schema, table_name)
            result = self.execute(command)
            print(table_name, result)
            if len(result) > 0 and len(result[0]) > 0 and result[0][0]:
                self.execute('TRUNCATE {}.{}'.format(self._settings.schema, table_name))
                self.__insert_rows(table_name, columns, data)
            else:
                self.create_table(table_name, columns, data)