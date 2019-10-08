import datetime as dt

from uploader.database.database_utils import null_or_format_str, py_value_to_pg_value
from uploader.utils import NULL


def test_single_quote_escape():
    assert null_or_format_str("it's quite late", "'{}'") == "'it''s quite late'"


def test_single_space_int():
    assert py_value_to_pg_value(int, ' ') == NULL


def test_mapping():
    value_type = {
        'mapping': {
            'type': 'interval'
        }
    }

    value_str = '12.12.2014 13:53:03'
    value_format = '%d.%m.%Y %H:%M:%S'
    value = dt.datetime.strptime(value_str, value_format)
    assert py_value_to_pg_value(value_type, value) == "to_timestamp('{}', 'dd.mm.yyyy hh24:mi:ss')".format(value_str)
