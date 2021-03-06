import os

from transliterate import translit

NULL = 'NULL'


def transliterate(text: str) -> str:
    """Transliterate given text"""
    return translit(text, 'ru', reversed=True)


def to_allowed_symbols(text: str) -> str:
    result = ''.join([s for s in text if s.isalpha() or s in [' ', '_'] or s.isdigit()])
    result = ' '.join(result.split())
    return result.replace(' ', '_')


def create_column_name(text: str) -> str:
    return to_allowed_symbols(text)


def create_table_name(file_path: str, department: str = None) -> str:
    department_adopted = department + '_' if department else ''
    file_name_with_ext = os.path.basename(file_path)
    file_name = department_adopted + os.path.splitext(file_name_with_ext)[0]
    return transliterate(to_allowed_symbols(file_name))


def create_adopted_columns_names(columns) -> list:
    return [create_column_name(column) for column in columns]
