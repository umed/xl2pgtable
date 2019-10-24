import datetime as dt
from uploader.utils import NULL
from typing import List

__ESCAPE_SYMBOLS_MAPPING = {"'": r"''"}


def __value_empty(value) -> bool:
    return value == NULL or value is None or not value or (isinstance(value, str) and value.isspace())


def __escaped_symbols() -> dict:
    if not hasattr(__escaped_symbols, 'translation'):
        __escaped_symbols.translation = str.maketrans(__ESCAPE_SYMBOLS_MAPPING)
    return __escaped_symbols.translation


def time_delta_to_str(value: dt.datetime):
    excel_start_date = dt.datetime(1899, 12, 31, 0, 0, 0)
    delta = value - excel_start_date
    hours = delta.days * 24 + int(delta.seconds / 3600)
    minutes = int(delta.seconds % 3600 / 60)
    seconds = delta.seconds % 3600 % 60
    result = '{}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return result


def convert_datetime_to_str(value, to_format: str, formater_type: str) -> str:
    if __value_empty(value):
        return NULL
    if formater_type == 'timedelta':
        return time_delta_to_str(value)
    if type(value) == str:
        formater = FORMATERS[formater_type]
        for format in formater['formats']:
            try:
                dt_value = dt.datetime.strptime(value, format)
            except:
                continue
            value = formater['converter'](dt_value)
    return value.strftime(to_format)


# def convert_datetime_to_str(value, dt_format: str) -> str:
#     if type(value) == str:
#         return value
#     else:
#         return value.strftime(dt_format)


def null_or_format_str(value, str_format: str):
    if __value_empty(value):
        return NULL
    else:
        return str_format.format(str(value).translate(__escaped_symbols()))


def py_type_to_pg_type(py_type):
    return PYTHON_TYPES_TO_PG_SQL_TYPES[py_type]['type']


def py_value_to_pg_value(value_type, value) -> str:
    if type(value_type) is dict:
        if 'mapping' in value_type and 'type' in value_type['mapping'] and value_type['mapping']['type'] is not None:
            current_type = pg_type_to_py(value_type['mapping']['type'], value_type['type'])
        else:
            current_type = value_type['type']
    else:
        current_type = value_type
    return PYTHON_TYPES_TO_PG_SQL_TYPES[current_type]['converter'](value)


# def datetime_to_null_or_str_format(value, dt_format, str_format):
#     result = convert_datetime_to_str(value, dt_format)
#     result = null_or_format_str(result, str_format)
#     return result

PG_TYPE_TO_PYTHON_TYPE = {
    'numer': int,
    'integ': int,
    'real': float,
    'times': dt.datetime,
    'time': dt.time,
    'date': dt.date,
    'inter': dt.timedelta,
    'varch': str,
    'text': str

}


def pg_type_to_py(pg_type: str, default_type: type) -> type:
    pg_type = pg_type.lower()[0:5]
    if pg_type in PG_TYPE_TO_PYTHON_TYPE:
        return PG_TYPE_TO_PYTHON_TYPE[pg_type]
    return default_type


FORMATERS = {
    'date': {
        'formats': [
            '%d.%m.%Y',
            '%Y-%m-%d'
        ],
        'converter': lambda value: value.date()
    },
    'time': {
        'formats': [
            '%H:%M:%S',
        ],
        'converter': lambda value: value.time()
    },
    'timestamp': {
        'formats': [
            '%d.%m.%Y %H:%M:%S',
            '%Y-%m-%d %H:%M:%S'
        ],
        'converter': lambda value: value
    }
}

PYTHON_TYPES_TO_PG_SQL_TYPES = {
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
        'converter': lambda value: null_or_format_str(convert_datetime_to_str(value,
                                                                              '%H:%M:%S',
                                                                              'time'),
                                                      "'{}'")
    },
    dt.datetime: {
        'type': 'timestamp',
        'converter': lambda value: null_or_format_str(convert_datetime_to_str(value,
                                                                              '%d.%m.%Y %H:%M:%S',
                                                                              'timestamp'),
                                                      "to_timestamp('{}', 'dd.mm.yyyy hh24:mi:ss')")
    },
    dt.date: {
        'type': 'date',
        'converter': lambda value: null_or_format_str(convert_datetime_to_str(value,
                                                                              '%d.%m.%Y',
                                                                              'date'),
                                                      "to_date('{}', 'dd.mm.yyyy')")
    },
    dt.timedelta: {
        'type': 'interval',
        'converter': lambda value: null_or_format_str(convert_datetime_to_str(value,
                                                                              '%d.%m.%Y %H:%M:%S',
                                                                              'timedelta'),
                                                      "'{}'")
    }
}
