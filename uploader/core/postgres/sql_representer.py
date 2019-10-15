from uploader.base import IData
from uploader.base.irepresenter import IRepresenter


class SqlRepresenter(IRepresenter):
    def __init__(self, data: IData):
        self._table: str = None
        self._values: str = None
        self._data = data

    def scheme(self) -> dict:
        d = {'create': '', 'drop': 'mapping'}
        return d

    def data(self) -> dict:
        pass
