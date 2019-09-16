import datetime as dt
from uploader.utils import NULL

__ESCAPE_SYMBOLS_MAPPING = {"'": r"''"}


def __value_empty(value) -> bool:
    return value == NULL or value is None or not value or (isinstance(value, str) and value.isspace())


def __escaped_symbols() -> dict:
    if not hasattr(__escaped_symbols, 'translation'):
        __escaped_symbols.translation = str.maketrans(__ESCAPE_SYMBOLS_MAPPING)
    return __escaped_symbols.translation


def convert_datetime_to_str(value, dt_format: str) -> str:
    if type(value) == str:
        return value
    else:
        return value.strftime(dt_format)


def null_or_format_str(value, str_format: str):
    if __value_empty(value):
        return NULL
    else:
        return str_format.format(str(value).translate(__escaped_symbols()))


def py_type_to_pg_type(py_type):
    return PG_SQL_TYPES_TO_PYTHON_TYPES[py_type]['type']


def py_value_to_pg_value(value_type, value) -> str:
    current_type = value_type['type'] if type(value_type) is dict else value_type
    return PG_SQL_TYPES_TO_PYTHON_TYPES[current_type]['converter'](value)


# def datetime_to_null_or_str_format(value, dt_format, str_format):
#     result = convert_datetime_to_str(value, dt_format)
#     result = null_or_format_str(result, str_format)
#     return result


PG_SQL_TYPES_TO_PYTHON_TYPES = {
    int: {
        'type': 'numeric',
        'converter': lambda value: null_or_format_str(value, '{}')
    },
    float: {
        'type': 'real',
        'converter': lambda value: null_or_format_str(value, '{}')
    },
    str: {
        'type': 'varchar',
        'converter': lambda value: null_or_format_str(value, "'{}'")
    },
    dt.time: {
        'type': 'time',
        'converter': lambda value: null_or_format_str(convert_datetime_to_str(value, '%H:%M:%S'),
                                                      "'{}'")
    },
    dt.datetime: {
        'type': 'timestamp',
        'converter': lambda value: null_or_format_str(convert_datetime_to_str(value, '%d.%m.%Y %H:%M:%S'),
                                                      "to_timestamp('{}', 'dd.mm.yyyy hh24:mi:ss')")
    },
    dt.date: {
        'type': 'date',
        'converter': lambda value: null_or_format_str(convert_datetime_to_str(value, '%d.%m.%Y'),
                                                      "to_date('{}', 'dd.mm.yyyy')")
    }
}
