import datetime as dt

from uploader.base import ITypeRecognizer

TYPE_CONVERTERS = {
    int: int,
    float: float,
    dt.time: lambda value: value if type(value) == dt.time else dt.datetime.strptime(value, '%H:%M:%S').time(),
    dt.date: lambda value: value if type(value) == dt.date else dt.datetime.strptime(value, '%d.%m.%Y').date(),
    dt.datetime: lambda value: value if type(value) == dt.datetime else dt.datetime.strptime(value,
                                                                                             '%d.%m.%Y %H:%M:%S'),
    str: str,
}


class TypeRecognizer(ITypeRecognizer):
    def type(self, value) -> type:
        global TYPE_CONVERTERS
        for converter_type, converter in TYPE_CONVERTERS.items():
            try:
                converter(value)
                return converter_type
            except Exception:
                continue
        return self.default_type()

    def default_type(self):
        return str

    def convert(self, value):
        global TYPE_CONVERTERS
        for _, converter in TYPE_CONVERTERS.items():
            try:
                return converter(value)
            except Exception:
                continue
        return self.default_type()(value)
