"""
The semantic analyzer of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import error_handler as err


def analyze_semantics(abstract_syntax_tree):
    _SemanticAnalyzerDeclaredIdentifiers().visit(abstract_syntax_tree)
    _SemanticAnalyzerTypes().visit(abstract_syntax_tree)


class _SemanticAnalyzerDeclaredIdentifiers(ast.NodeVisitor):
    def _visit_Assignment(self, node):
        self._verify_identifier_declared(node.identifier, node.symbol_table, node.token.line, node.token.column)
        self._generic_visit(node)

    def _visit_Identifier(self, node):
        self._verify_identifier_declared(node.name, node.symbol_table, node.token.line, node.token.column)
        self._generic_visit(node)

    @staticmethod
    def _verify_identifier_declared(identifier, symbol_table, line, column):
        try:
            symbol_table[identifier]
        except KeyError as error:
            raise err.SeaSubSemanticError(f"Undeclared identifier '{identifier}' on line {line}:{column}") from error


class _SemanticAnalyzerTypes(ast.NodeVisitor):
    def _visit_Assignment(self, node):
        identifier_type = node.symbol_table[node.identifier].type
        value_type = self.visit(node.value)
        if identifier_type != value_type:
            raise err.SeaSubSemanticError((f"Assigning value of type '{value_type}'' to variable of type "
                                           f"'{identifier_type}' on line {node.token.line}:{node.token.column}"))

    def _visit_BinaryOperator(self, node):
        a_type = self.visit(node.a)
        b_type = self.visit(node.b)
        if a_type != b_type:
            raise err.SeaSubSemanticError((f"Applying binary operator '{node.operator}' with incompatible types "
                                           f"'{a_type}' and '{b_type}' on line {node.token.line}:{node.token.column}"))
        return a_type

    def _visit_UnaryOperator(self, node):
        return self.visit(node.a)

    def _visit_Identifier(self, node):
        return node.symbol_table[node.name].type

    def _visit_IntegerConstant(self, node):
        return 'int'

    def _visit_RealConstant(self, node):
        return 'double'
