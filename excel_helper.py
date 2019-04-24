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

import utils


def get_type(value) -> type:
    for converter_type, converter in TYPE_CONVERTERS.items():
        try:
            converter(value)
            return converter_type
        except Exception:
            continue
    return str


def key_types_of_plain_dict(d: dict) -> dict:
    result = {}
    for key, value in d.items():
        result[key] = get_type(value)
    return result


def __get_cols_indexes_to_skip(df: pd.DataFrame) -> list:
    (_, row_values) = next(df.iterrows())
    for cols_number_to_skip, value in enumerate(row_values):
        if not pd.isna(value):
            break
    if cols_number_to_skip == len(row_values):
        logging.error('Cannot handle file. Probably, it is empty')
        exit(1)
    return list(range(0, cols_number_to_skip))


def __read_excel(file_path: str) -> dict:
    df = pd.read_excel(file_path, header=None)
    df.dropna(how='all', inplace=True)
    # shift table if data are not placed in the first row/column
    cols_indexes_to_skip = __get_cols_indexes_to_skip(df)
    df.drop(df.columns[cols_indexes_to_skip], axis=1, inplace=True)
    # first row as columns names
    df.fillna('NULL', inplace=True)
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(df.index[0], inplace=True)
    df.columns = utils.create_adopted_columns_names(df.columns)
    return df.to_dict('records')


def read_excel(file_path: str) -> tuple:
    sheet_data = __read_excel(file_path)
    if len(sheet_data) > 0:
        result = (key_types_of_plain_dict(sheet_data[0]), sheet_data)
    else:
        result = (dict(), sheet_data)
    return result


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
