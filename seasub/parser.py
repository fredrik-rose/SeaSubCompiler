"""
The parser of the sea sub compiler.
"""
from seasub import lexer as seasublex


class NoOperation:
    def __repr__(self):
        return "NoOperation()"

    def __str__(self):
        return "NoOperation"


class CompoundStatement:
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"CompoundStatement({self.declarations}, {self.statements})"

    def __str__(self):
        return "\n".join(f"{str(item)}" for item in self.declarations + self.statements)


class Declaration:
    def __init__(self, type_specifier, identifier):
        self.type_specifier = type_specifier.value
        self.identifier = identifier

    def __repr__(self):
        return f"Declaration({self.type_specifier}, {self.identifier})"

    def __str__(self):
        return f"{str(self.type_specifier)} {str(self.identifier)}"


class Assignment:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"Assignment({repr(self.identifier)}, {repr(self.value)})"

    def __str__(self):
        return f"{self.identifier} = {self.value}"


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


class Identifier:
    def __init__(self, name):
        self.name = name.value

    def __repr__(self):
        return f"Identifier({repr(self.name)})"

    def __str__(self):
        return f"{self.name}"


class Number:
    def __init__(self, value):
        self.value = value.value

    def __repr__(self):
        return f"Number({repr(self.value)})"

    def __str__(self):
        return str(self.value)


def parse(text):
    def translation_unit(lexer):
        node = compound_statement(lexer)
        lexer.eat('EOF')
        return node

    def compound_statement(lexer):
        lexer.eat('LEFT_CURLY_BRACKET')
        if lexer.peek().type == 'RIGHT_CURLY_BRACKET':
            node = NoOperation()
        else:
            declarations = []
            if lexer.peek().type == 'TYPE_SPECIFIER':
                declarations = declaration_list(lexer)
            statements = statement_list(lexer)
            node = CompoundStatement(declarations, statements)
        lexer.eat('RIGHT_CURLY_BRACKET')
        return node

    def declaration_list(lexer):
        declarations = [declaration(lexer)]
        while lexer.peek().type == 'TYPE_SPECIFIER':
            declarations.append(declaration(lexer))
        return declarations

    def declaration(lexer):
        type_specifier = lexer.eat('TYPE_SPECIFIER')
        variable = identifier(lexer)
        lexer.eat('SEMICOLON')
        node = Declaration(type_specifier, variable)
        return node

    def statement_list(lexer):
        statements = [statement(lexer)]
        while lexer.peek().type != 'RIGHT_CURLY_BRACKET':
            statements.append(statement(lexer))
        return statements

    def statement(lexer):
        if lexer.peek().type == 'LEFT_CURLY_BRACKET':
            node = compound_statement(lexer)
        else:
            node = expression_statement(lexer)
        return node

    def expression_statement(lexer):
        if lexer.peek().type == 'SEMICOLON':
            node = NoOperation()
        else:
            variable = identifier(lexer)
            lexer.eat('ASSIGNMENT')
            value = expression(lexer)
            node = Assignment(variable, value)
        lexer.eat('SEMICOLON')
        return node

    def expression(lexer):
        node = additive_expression(lexer)
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
        elif lexer.peek().type == 'IDENTIFIER':
            node = identifier(lexer)
        else:
            number = lexer.eat('NUMBER')
            node = Number(number)
        return node

    def identifier(lexer):
        name = lexer.eat('IDENTIFIER')
        node = Identifier(name)
        return node

    return translation_unit(seasublex.Lexer(text))
