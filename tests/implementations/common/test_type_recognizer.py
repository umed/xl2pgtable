import pytest
import datetime as dt
from uploader.core.common.type_recognizer import TypeRecognizer


@pytest.mark.parametrize("test_input, expected", [(123, int), ("cool text here", str), ("12.04.2018", dt.date)])
def test_type(test_input, expected):
    recognizer = TypeRecognizer()
    assert recognizer.type(test_input) == expected


@pytest.mark.parametrize("test_input, expected",
                         [(123, 123), ("cool text here", "cool text here"), ("12.04.2018", dt.date(2018, 4, 12))])
def test_convert(test_input, expected):
    recognizer = TypeRecognizer()
    assert recognizer.convert(test_input) == expected
