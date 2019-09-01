# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:09:51 2019

@author: PuchkovaKS
"""

import datetime as dt
import logging
import os

import pandas as pd
import xlrd

from uploader.utils import create_adopted_columns_names, NULL


def get_type(value) -> type:
    for converter_type, converter in TYPE_CONVERTERS.items():
        try:
            converter(value)
            return converter_type
        except Exception:
            continue
    return str


def rows_item_types(rows: list) -> dict:
    if len(rows) == 0:
        return {}
    item_types = {}
    for key in rows[0].keys():
        for row in rows:
            value = row[key]
            if value != NULL:
                item_types[key] = get_type(value)
                break
    return item_types


def __get_cols_indexes_to_skip(df: pd.DataFrame) -> list:
    (_, row_values) = next(df.iterrows())
    cols_number_to_skip = 0
    for cols_number_to_skip, value in enumerate(row_values):
        if not pd.isna(value):
            break
    if cols_number_to_skip == len(row_values):
        error_message = 'Cannot handle file. Probably, it is empty'
        logging.error(error_message)
        raise ValueError(error_message)
    return list(range(0, cols_number_to_skip))


def __read_excel(file_path: str) -> list:
    df = pd.read_excel(file_path, header=None)
    df.dropna(how='all', inplace=True)
    # shift table if data are not placed in the first row/column
    cols_indexes_to_skip = __get_cols_indexes_to_skip(df)
    df.drop(df.columns[cols_indexes_to_skip], axis=1, inplace=True)
    # first row as columns names
    df.fillna(NULL, inplace=True)
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(df.index[0], inplace=True)
    df.columns = create_adopted_columns_names(df.columns)
    return df.to_dict('records')


def read_excel(file_path: str) -> tuple:
    sheet_data = __read_excel(file_path)
    return rows_item_types(sheet_data), sheet_data


def is_excel_file(file_path: str) -> bool:
    try:
        xlrd.open_workbook(file_path).release_resources()
        return True
    except Exception:
        return False


def get_excel_files_in_dir(dir_path: str, exclude: list) -> list:
    def is_acceptable_file(file_path):
        return is_excel_file(file_path) and \
               os.path.basename(file_path) not in exclude

    files = [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)]
    return [f for f in files if is_acceptable_file(f)]


TYPE_CONVERTERS = {
    int: int,
    float: float,
    dt.time: lambda value: value if type(value) == dt.time else dt.datetime.strptime(value, '%H:%M:%S').time(),
    dt.date: lambda value: value if type(value) == dt.date else dt.datetime.strptime(value, '%d.%m.%Y').date(),
    dt.datetime: lambda value: value if type(value) == dt.datetime else dt.datetime.strptime(value,
                                                                                             '%d.%m.%Y %H:%M:%S'),
    str: str,
}
