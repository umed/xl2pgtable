import logging

from uploader.excel_helper import is_excel_file, excel_to_list_of_dicts
from uploader.utils import create_table_name
from uploader import utils
from typing import List
import os

COLUMNS_LIST = ["Link", "Table name", "Department name"]


def __absolute_path(base: str, file_path: str):
    if os.path.isabs(file_path):
        return file_path
    return os.path.join(base, file_path)


def read_config(file_path: str) -> list:
    configs = __read_excel(file_path, COLUMNS_LIST)
    file_dir = os.path.dirname(file_path)
    result_configs = []
    for config in configs:
        if 'Upload' in config and config['Upload'] != 1:
            continue
        table_name = config.get('Table name', None)
        config['Link'] = __absolute_path(file_dir, config['Link'])
        if not table_name or table_name == utils.NULL:
            config['Table name'] = create_table_name(config['Link'], config['Department name'])
        result_configs.append(config)
    return result_configs


def __read_excel(file_path, columns_names_to_check: list) -> List[dict]:
    if not is_excel_file(file_path):
        raise FileExistsError('"{}" is not excel file'.format(file_path))
    configs = excel_to_list_of_dicts(file_path)
    if not configs or len(configs) == 0:
        raise ValueError('Config file is empty or could not parse it')
    if not all(item in configs[0] for item in columns_names_to_check):
        raise ValueError('File format is invalid')
    return configs


def __get_table_columns(column_mappings: List[dict], table_name: str):
    table_mappings = []
    for mapping in column_mappings:
        if mapping.get('Table name', None) == table_name:
            table_mappings.append(mapping)
    if len(table_mappings) == 0:
        logging.error('There is no columns mapping of {} table'.format(table_name))
    return table_mappings


def apply_column_mappings(file_path: str, configs: List[dict]):
    column_mappings = __read_excel(file_path, [])
    #print(column_mappings)
    #print(configs)
    for config in configs:
        table_name = config.get('Table name', None)
        if table_name:
            config['mappings'] = __get_table_columns(column_mappings, table_name)
