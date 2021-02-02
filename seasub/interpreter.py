"""
The interpreter of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import symbol_table as st


class Intepreter(ast.NodeVisitor):
    def __init__(self):
        self.symbol_table = st.SymbolTable()

    def visit_Assignment(self, node):
        self.symbol_table[node.identifier.name] = self.visit(node.value)

    def visit_BinaryOperator(self, node):
        operators = {'+': lambda a, b: a + b,
                     '-': lambda a, b: a - b,
                     '*': lambda a, b: a * b,
                     '/': lambda a, b: a / b}
        a = self.visit(node.a)
        b = self.visit(node.b)
        return operators[node.operator](a, b)

    def visit_UnaryOperator(self, node):
        operators = {'+': lambda a: +a,
                     '-': lambda a: -a}
        a = self.visit(node.a)
        return operators[node.operator](a)

    def visit_Identifier(self, node):
        return self.symbol_table[node.name]

    def visit_Number(self, node):
        return node.value
