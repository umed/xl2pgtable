from uploader.database.database import Database
from uploader.excel_helper import column_types, excel_to_list_of_dicts
from typing import List

from uploader.utils import create_column_name


class FileUploader:
    def __init__(self, db: Database):
        self._db = db

    def upload(self, file_path: str, table_name: str, mappings: List[dict] = None):
        rows = excel_to_list_of_dicts(file_path)
        columns = column_types(rows)
        for key, value in columns.items():
            d = {
                'type': value,
                'name': create_column_name(key)
            }
            for mapping in mappings:
                if key != mapping['Original name']:
                    continue
                d.update({
                    'mapping': {
                        'name': mapping['Code'],
                        'type': mapping['Data type'],
                        'comment': mapping['Comment']
                    }
                })
            columns[key] = d
        self._db.rewrite_data(table_name, columns, rows)


TABLE_NAME = 'table_name'
COLUMNS_INFO = 'columns_info'
ROWS = 'rows'
