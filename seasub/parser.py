"""
The parser of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import error_handler as err


def parse(token_stream):
    def translation_unit(lexer):
        node = function_definition_list(lexer)
        lexer.eat('EOF')
        return node

    def function_definition_list(lexer):
        function_definitions = [function_definition(lexer)]
        while lexer.peek().type == 'TYPE_SPECIFIER':
            function_definitions.append(function_definition(lexer))
        return function_definitions

    def function_definition(lexer):
        type_specifier = lexer.eat('TYPE_SPECIFIER').value
        name = identifier(lexer).name
        lexer.eat('LEFT_PARENTHESIS')
        parameters = parameter_list(lexer)
        lexer.eat('RIGHT_PARENTHESIS')
        body = compound_statement(lexer)
        node = ast.Function(type_specifier, name, parameters, body)
        return node

    def parameter_list(lexer):
        parameters = [parameter_declaration(lexer)]
        while lexer.peek().type == 'COMMA':
            lexer.eat('COMMA')
            parameters.append(parameter_declaration(lexer))
        return parameters

    def parameter_declaration(lexer):
        type_specifier = lexer.eat('TYPE_SPECIFIER').value
        name = identifier(lexer).name
        return ast.Parameter(type_specifier, name)

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
        type_specifier = lexer.eat('TYPE_SPECIFIER').value
        variable = identifier(lexer).name
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
            variable = identifier(lexer).name
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
            operator = lexer.eat('ARITHMETIC_OPERATOR').value
            operand = multiplicative_expression(lexer)
            node = ast.BinaryOperator(operator, node, operand)
        return node

    def multiplicative_expression(lexer):
        node = unary_expression(lexer)
        while lexer.peek().type == 'ARITHMETIC_OPERATOR' and lexer.peek().value in ('*', '/'):
            operator = lexer.eat('ARITHMETIC_OPERATOR').value
            operand = unary_expression(lexer)
            node = ast.BinaryOperator(operator, node, operand)
        return node

    def unary_expression(lexer):
        if lexer.peek().type == 'ARITHMETIC_OPERATOR' and lexer.peek().value in ('+', '-'):
            operator = lexer.eat('ARITHMETIC_OPERATOR').value
            operand = unary_expression(lexer)
            node = ast.UnaryOperator(operator, operand)
        else:
            node = primary_expression(lexer)
        return node

    def primary_expression(lexer):
        if lexer.peek().type == 'LEFT_PARENTHESIS':
            lexer.eat('LEFT_PARENTHESIS')
            node = additive_expression(lexer)
            lexer.eat('RIGHT_PARENTHESIS')
        elif lexer.peek().type == 'IDENTIFIER':
            node = identifier(lexer)
        else:
            node = constant(lexer)
        return node

    def identifier(lexer):
        name = lexer.eat('IDENTIFIER').value
        node = ast.Identifier(name)
        return node

    def constant(lexer):
        if lexer.peek().type == 'INTEGER_CONSTANT':
            number = lexer.eat('INTEGER_CONSTANT').value
            node = ast.IntegerConstant(number)
        else:
            number = lexer.eat('DOUBLE_CONSTANT').value
            node = ast.RealConstant(number)
        return node

    return translation_unit(_Lexer(token_stream))


class _Lexer:
    def __init__(self, token_stream):
        self._token_stream = token_stream
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
            self._current = next(self._token_stream)
        except StopIteration:
            self._current = None
