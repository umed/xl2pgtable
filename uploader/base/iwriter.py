import abc
from uploader.base.idata import IData


class IWriter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, data: IData, mapping, append: bool):
        pass
