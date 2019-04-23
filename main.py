# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:09:51 2019

@author: PuchkovaKS
"""

import logging
from excel_helper import read_excel, get_excel_files_in_dir
from database_helper import DatabaseHelper
from database_settings import DatabaseSettings
import os

TABLE_NAME = 'table_name'
COLUMNS_INFO = 'columns_info'
ROWS = 'rows'

def transliterate(text: str) -> str:
    """Transliterate given text"""
    return text


def extract_allowed_symbols(text: str) -> str:
    result = ''.join([s for s in text if s.isalpha()
                      or s == ' ' or s.isdigit()])
    return result.replace(' ', '_')


def create_column_name(text: str) -> str:
    return extract_allowed_symbols(text)


def create_table_name(file_path: str) -> str:
    file_name_with_ext = os.path.basename(file_path)
    file_name = os.path.splitext(file_name_with_ext)[0]
    return transliterate(extract_allowed_symbols(file_name))


def create_file_info(file_path: str) -> dict:
    columns_info, rows = read_excel('file_path')
    new_columns_info = {}
    for key, value in columns_info.items():
        new_columns_info[create_column_name(key)] = value
    return {
        TABLE_NAME: create_table_name(file_path),
        COLUMNS_INFO: new_columns_info,
        ROWS: rows
    }


def create_files_info(dirname: str, exclude: list = None) -> list:
    if not os.path.exists(dirname):
        logging.error('"{}" does not exist'.format(dirname))
        exit(1)
    if not exclude:
        exclude = []
    files_info = []
    files = get_excel_files_in_dir(dirname, exclude)
    for file_path in files:
        files_info.append(create_file_info(file_path))
    return files_info


def main():
    # cols, data = read_excel('/home/umed/Desktop/test.xlsx')
    # print(read_excel('C:\\Users\\puchkovaks\\Desktop\\test2.xlsx'))
    files_info = create_files_info('/home/umed/Desktop/test_dir/')
    settings = DatabaseSettings()
    db = DatabaseHelper(settings)
    for info in files_info:
        db.create_table(info[TABLE_NAME], info[COLUMNS_INFO], info[ROWS])
    exit(0)


if __name__ == "__main__":
    main()
# conn = psycopg2.connect(**dict(settings))
# cur = conn.cursor()
# cur.execute("select * from tsob_sandbox.datasource where type_db='O2C'")
