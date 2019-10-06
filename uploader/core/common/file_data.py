from typing import List, Type

from uploader.base import IData, NULL, ITypeRecognizer


class FileData(IData):
    def __init__(self, data: List[dict]):
        self._data = data
        self._items = []
        self._columns = []
        self._types = {}
        self._type_recognizer: ITypeRecognizer = None

    def to_dict(self) -> List[dict]:
        return self._data

    def columns(self) -> list:
        if len(self._data) > 0 and len(self._columns) != len(self._data[0].keys()):
            self._columns = list(self._data[0].keys())
        return self._columns

    def set_type_recognizer(self, type_recognizer: ITypeRecognizer):
        self._type_recognizer = type_recognizer

    def types(self) -> dict:
        if not self._type_recognizer:
            raise ReferenceError("type recognizer is not set")
        if not bool(self._types) and len(self._data) != 0:
            for key in self.columns():
                for row in self._data:
                    value = row[key]
                    if value != NULL:
                        self._types[key] = self._type_recognizer.type(value)
                        break
                if key not in self._types:
                    self._types[key] = self._type_recognizer.default_type()
        return self._types

    def rows(self) -> List[list]:
        if len(self._items) != len(self._data):
            for row in self._data:
                self._items.append(list(row.values()))
        return self._items
