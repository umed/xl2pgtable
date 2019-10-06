import abc
from typing import List
from .itype_recognizer import ITypeRecognizer

NULL = 'NULL'


class IData(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def to_dict(self) -> List[dict]:
        pass

    @abc.abstractmethod
    def columns(self) -> list:
        pass

    @abc.abstractmethod
    def set_type_recognizer(self, type_recognizer: ITypeRecognizer):
        pass

    @abc.abstractmethod
    def types(self) -> dict:
        pass

    @abc.abstractmethod
    def rows(self) -> List[list]:
        pass
