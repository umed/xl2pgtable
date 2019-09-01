# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:09:51 2019

@author: PuchkovaKS
"""

import logging
import os
import sys

from uploader.database import Database
from uploader.database_settings import DatabaseSettings
from uploader.excel_helper import get_excel_files_in_dir, read_excel

from uploader.utils import create_table_name

# REPLACE PATH BY YOUR PATH TO EXCEL FILES
# use double slashes on windows
PATH_TO_FOLDER_WITH_EXCEL_FILES = '/home/umed/Documents'


TABLE_NAME = 'table_name'
COLUMNS_INFO = 'columns_info'
ROWS = 'rows'


def create_file_info(file_path: str) -> dict:
    columns_info, rows = read_excel(file_path)
    new_columns_info = {}
    for key, value in columns_info.items():
        new_columns_info[key] = value
    return {
        TABLE_NAME: create_table_name(file_path),
        COLUMNS_INFO: new_columns_info,
        ROWS: rows
    }


def create_files_info(dir_name: str, exclude: list = None) -> list:
    if not os.path.exists(dir_name):
        logging.error('"{}" does not exist'.format(dir_name))
        exit(1)
    if not exclude:
        exclude = []
    files_info = []
    files = get_excel_files_in_dir(dir_name, exclude)
    for file_path in files:
        try:
            files_info.append(create_file_info(file_path))
        except ValueError:
            print("Error happened during '{}' reading. Will be skipped.".format(file_path))
    return files_info


def main():
    if len(sys.argv) > 1:
        files_path = sys.argv[1]
    else:
        files_path = PATH_TO_FOLDER_WITH_EXCEL_FILES
    files_info = create_files_info(files_path)
    settings = DatabaseSettings()
    db = Database(settings)
    for info in files_info:
        db.rewrite_data(info[TABLE_NAME], info[COLUMNS_INFO], info[ROWS])
    exit(0)


if __name__ == "__main__":
    main()
