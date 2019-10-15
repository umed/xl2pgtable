import abc

from uploader.base import IData


class IReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self, path: str, top_offset: int, bottom_offset: int, left_offset: int,
             right_offset: int) -> IData:
        pass
