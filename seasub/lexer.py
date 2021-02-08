"""
The lexical analyzer (also known as scanner or tokenizer) of the sea sub compiler.
"""
import re

from seasub import error_handler as err


def tokenize(text):
    token_specification = [
        ('LEFT_CURLY_BRACKET', r'\{'),  # Left curly bracket.
        ('RIGHT_CURLY_BRACKET', r'\}'),  # Right curly bracket.
        ('TYPE_SPECIFIER', r'int|double'),  # Type specifier.
        ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number.
        ('IDENTIFIER', r'[_a-zA-Z][_a-zA-Z0-9]{0,30}'),  # Variable or function name.
        ('ASSIGNMENT', r'='),  # Assignment operator.
        ('ARITHMETIC_OPERATOR', r'[+\-*/]'),  # Arithmetic operators.
        ('LEFT_PARENTHESIS', r'\('),  # Left parenthesis.
        ('RIGHT_PARENTHESIS', r'\)'),  # Right parenthesis.
        ('SEMICOLON', r';'),  # Semicolon.
        ('COMMA', r','),  # Comma.
        ('NEWLINE', r'\n'),  # Line ending.
        ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs.
        ('MISMATCH', r'.'),  # Any other character.
    ]
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    line = 1
    line_start = 0
    for match in re.finditer(token_regex, text):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start + 1
        if kind == 'NUMBER':
            if '.' in value:
                kind = 'DOUBLE_CONSTANT'
                value = float(value)
            else:
                kind = 'INTEGER_CONSTANT'
                value = int(value)
        elif kind == 'NEWLINE':
            line_start = match.end()
            line += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise err.SeaSubLexicalError(f"Unexpected {value!r} on line {line}:{column}")
        yield Token(kind, value, line, column)
    yield Token('EOF', None, line, 0)


class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.column})"

    def __str__(self):
        return "<{}, {}>".format(self.type, self.value)
