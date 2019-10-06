import logging

import pandas as pd
import xlrd

from typing import List

from xlrd import XLRDError

from uploader.base import IReader, IData, NULL
from uploader.core.common.file_data import FileData


class ExcelReader(IReader):
    def read(self, path: str, top_offset: int = 0, bottom_offset: int = 0, left_offset: int = 0,
             right_offset: int = 0) -> IData:
        if not self.is_excel_file(path):
            # TODO: log it, raise exception
            pass
        return FileData(self.__excel_to_list_of_dicts(path))

    @staticmethod
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

    def __excel_to_data_frame(self, file_path) -> pd.DataFrame:
        df = pd.read_excel(file_path, header=None)
        df.dropna(how='all', inplace=True)
        # shift table if data are not placed in the first row/column
        cols_indexes_to_skip = self.__get_cols_indexes_to_skip(df)
        df.drop(df.columns[cols_indexes_to_skip], axis=1, inplace=True)
        # first row as columns names
        df.fillna(NULL, inplace=True)
        df.rename(columns=df.iloc[0], inplace=True)
        df.drop(df.index[0], inplace=True)
        return df

    @staticmethod
    def is_excel_file(file_path: str) -> bool:
        try:
            xlrd.open_workbook(file_path).release_resources()
            return True
        except XLRDError:
            return False
        except Exception:
            return False

    def __excel_to_list_of_dicts(self, file_path: str) -> List[dict]:
        return self.__excel_to_data_frame(file_path).to_dict('records')
