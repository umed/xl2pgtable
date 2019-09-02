from uploader.database_utils import null_or_format_str, py_value_to_pg_value
from uploader.utils import NULL


def test_single_quote_escape():
    assert null_or_format_str("it's quite late", "'{}'") == "'it''s quite late'"

def test_single_space_int():
    assert py_value_to_pg_value(int, ' ') == NULL