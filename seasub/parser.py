"""
The parser of the sea sub compiler.
"""
from seasub import lexer as seasublex


class BinaryOperator:
    def __init__(self, operator, a, b):
        self.operator = operator.value
        self.a = a
        self.b = b

    def __repr__(self):
        return f"BinaryOperator({repr(self.operator)}, {repr(self.a)}, {repr(self.b)})"

    def __str__(self):
        return f"({self.a} {self.operator} {self.b})"


class UnaryOperator:
    def __init__(self, operator, a):
        self.operator = operator.value
        self.a = a

    def __repr__(self):
        return f"UnaryOperator({repr(self.operator)}, {repr(self.a)})"

    def __str__(self):
        return f"({self.operator}{self.a})"


class Number:
    def __init__(self, value):
        self.value = value.value

    def __repr__(self):
        return f"Number({repr(self.value)})"

    def __str__(self):
        return str(self.value)


def parse(text):
    def program(lexer):
        node = additive_expression(lexer)
        lexer.eat('EOF')
        return node

    def additive_expression(lexer):
        node = multiplicative_expression(lexer)
        while lexer.peek().type == 'ARITHMETIC_OPERATOR' and lexer.peek().value in ('+', '-'):
            operator = lexer.eat('ARITHMETIC_OPERATOR')
            operand = multiplicative_expression(lexer)
            node = BinaryOperator(operator, node, operand)
        return node

    def multiplicative_expression(lexer):
        node = unary_expression(lexer)
        while lexer.peek().type == 'ARITHMETIC_OPERATOR' and lexer.peek().value in ('*', '/'):
            operator = lexer.eat('ARITHMETIC_OPERATOR')
            operand = unary_expression(lexer)
            node = BinaryOperator(operator, node, operand)
        return node

    def unary_expression(lexer):
        if lexer.peek().type == 'ARITHMETIC_OPERATOR' and lexer.peek().value in ('+', '-'):
            operator = lexer.eat('ARITHMETIC_OPERATOR')
            operand = unary_expression(lexer)
            node = UnaryOperator(operator, operand)
        else:
            node = primary_expression(lexer)
        return node

    def primary_expression(lexer):
        if lexer.peek().type == 'LEFT_PARENTHESIS':
            lexer.eat('LEFT_PARENTHESIS')
            node = additive_expression(lexer)
            lexer.eat('RIGHT_PARENTHESI')
        else:
            number = lexer.eat('NUMBER')
            node = Number(number)
        return node

    return program(seasublex.Lexer(text))
