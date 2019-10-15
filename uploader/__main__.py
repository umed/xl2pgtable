from uploader.utils import create_table_name
import logging
import os
import sys

from uploader.database.database import Database
from uploader.database.database_settings import DatabaseSettings
from uploader.excel_helper import get_excel_files_in_dir
from uploader.file_uploader import FileUploader
from uploader.config_reader import read_config, apply_column_mappings
import argparse

# REPLACE PATH BY YOUR PATH TO EXCEL FILES
# use double slashes on windows
PATH_TO_FOLDER_WITH_EXCEL_FILES = 'C:\\Users\\uabdumum\\Desktop\\projects\\test_data'


# def create_files_info(dir_name: str, exclude: list = None) -> list:
#     if not os.path.exists(dir_name):
#         logging.error('"{}" does not exist'.format(dir_name))
#         exit(1)
#     if not exclude:
#         exclude = []
#     files_info = []
#     files = get_excel_files_in_dir(dir_name, exclude)
#     for file_path in files:
#         try:
#             files_info.append(create_file_info(file_path))
#         except ValueError:
#             print("Error happened during '{}' reading. Will be skipped.".format(file_path))
#     return files_info


# def create_argparse():
#     argparse.


def main():
    if len(sys.argv) == 2:
        files_path = sys.argv[1]
        tables = [{'Link': f, 'Table name': create_table_name(f), 'mappings': None}
                  for f in get_excel_files_in_dir(files_path, [])]
    elif len(sys.argv) == 3:
        files_config_path = sys.argv[1]
        mappings_path = sys.argv[2]
        tables = read_config(files_config_path)
        apply_column_mappings(mappings_path, tables)
    else:
        files_path = PATH_TO_FOLDER_WITH_EXCEL_FILES
        tables = [{'Link': f, 'Table name': create_table_name(f), 'mappings': None}
                  for f in get_excel_files_in_dir(files_path, [])]

    settings = DatabaseSettings()
    db = Database(settings)
    file_uploader = FileUploader(db)
    for table in tables:
        file_uploader.upload(table['Link'], table['Table name'], table['mappings'])
    sys.exit(0)


# for info in files_info:
#     postgres.rewrite_data(info[TABLE_NAME], info[COLUMNS_INFO], info[ROWS])
# exit(0)


if __name__ == "__main__":
    main()
