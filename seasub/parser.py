"""
The parser of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import error_handler as err
from seasub import lexer as seasublex


def parse(text):
    def translation_unit(lexer):
        node = compound_statement(lexer)
        lexer.eat('EOF')
        return node

    def compound_statement(lexer):
        lexer.eat('LEFT_CURLY_BRACKET')
        if lexer.peek().type == 'RIGHT_CURLY_BRACKET':
            node = ast.NoOperation()
        else:
            declarations = []
            if lexer.peek().type == 'TYPE_SPECIFIER':
                declarations = declaration_list(lexer)
            statements = statement_list(lexer)
            node = ast.CompoundStatement(declarations, statements)
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
        node = ast.Declaration(type_specifier, variable)
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
            node = ast.NoOperation()
        else:
            variable = identifier(lexer)
            lexer.eat('ASSIGNMENT')
            value = expression(lexer)
            node = ast.Assignment(variable, value)
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
            node = ast.BinaryOperator(operator, node, operand)
        return node

    def multiplicative_expression(lexer):
        node = unary_expression(lexer)
        while lexer.peek().type == 'ARITHMETIC_OPERATOR' and lexer.peek().value in ('*', '/'):
            operator = lexer.eat('ARITHMETIC_OPERATOR')
            operand = unary_expression(lexer)
            node = ast.BinaryOperator(operator, node, operand)
        return node

    def unary_expression(lexer):
        if lexer.peek().type == 'ARITHMETIC_OPERATOR' and lexer.peek().value in ('+', '-'):
            operator = lexer.eat('ARITHMETIC_OPERATOR')
            operand = unary_expression(lexer)
            node = ast.UnaryOperator(operator, operand)
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
            node = ast.Number(number)
        return node

    def identifier(lexer):
        name = lexer.eat('IDENTIFIER')
        node = ast.Identifier(name)
        return node

    return translation_unit(_Lexer(text))


class _Lexer:
    def __init__(self, text):
        self._tokenizer = seasublex.tokenize(text)
        self._advance()

    def peek(self):
        return self._current

    def eat(self, token_type):
        current = self._current
        if current.type != token_type:
            raise err.SeaSubSyntaxError(f"Unexpected {current.value!r} on line {current.line}:{current.column}")
        self._advance()
        return current

    def _advance(self):
        try:
            self._current = next(self._tokenizer)
        except StopIteration:
            self._current = None
