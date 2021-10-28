"""
The semantic analyzer of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import error_handler as err


def analyze_semantics(abstract_syntax_tree):
    _SemanticAnalyzerDeclaredIdentifiers().visit(abstract_syntax_tree)


class _SemanticAnalyzerDeclaredIdentifiers(ast.NodeVisitor):
    def _visit_Assignment(self, node):
        self._verify_identifier_declared(node.identifier, node.symbol_table)
        self._generic_visit(node)

    def _visit_Identifier(self, node):
        self._verify_identifier_declared(node.name, node.symbol_table)
        self._generic_visit(node)

    @staticmethod
    def _verify_identifier_declared(identifier, symbol_table):
        try:
            symbol_table[identifier]
        except KeyError as key_error:
            raise err.SeaSubSemanticError(f"{identifier} is not declared") from key_error
