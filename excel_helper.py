# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:09:51 2019

@author: PuchkovaKS
"""

import pandas as pd
import logging
import datetime as dt
import xlrd
import os

def get_type(value) -> type:
    for converter_type, converter in TYPE_CONVERTERS.items():
        try:
            converter(value)
            return converter_type
        except Exception:
            pass
    return str

def key_types_of_plain_dict(d: dict) -> dict:
    result = {}
    for key, value in d.items():
        result[key] = get_type(value)
    return result


def __get_cols_indecies_to_skip(df: pd.DataFrame) -> list:
    (_, row_values) = next(df.iterrows())
    for cols_number_to_skip, value in enumerate(row_values):
        if value is not None:
            break
    if cols_number_to_skip == len(row_values):
        logging.error('Cannot handle file. Probably, it is empty')
        exit(1)
    return list(range(0, cols_number_to_skip))


def __read_excel(file_path: str) -> dict:
    # read file without marking first row as header
    df = pd.read_excel(file_path, header=None)
    df = df.dropna(how='all')
    # replace empty value of cells by None instead of NaN
    df = df.where(pd.notnull(df), None)
    # shift table if data are not placed in the first row/column
    cols_indecies_to_skip = __get_cols_indecies_to_skip(df)
    df = df.drop(df.columns[cols_indecies_to_skip], axis=1)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
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


def get_excel_files_in_dir(path: str, exclude: list) -> list:
    def only_excel_file(file_path):
        return is_excel_file(file_path) and \
                os.path.basename(file_path) not in exclude
    return list(filter(only_excel_file, os.listdir(path)))


TYPE_CONVERTERS = {
    int: int,
    float: float,
    dt.time: lambda value: dt.datetime.strptime(value, '%H:%M:%S').time(),
    dt.date: lambda value: dt.datetime.strptime(value, '%d.%m.%Y').date(),
    dt.datetime: lambda value: dt.datetime.strptime(value, '%d.%m.%Y %H:%M:%S'),
    str: str,
}
