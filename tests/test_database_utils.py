from uploader.database_utils import null_or_format_str


def test_single_quote_escape():
    assert null_or_format_str("it's quite late", "'{}'") == "'it''s quite late'"