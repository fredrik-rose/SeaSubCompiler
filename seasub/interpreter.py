"""
The interpreter of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast


class Intepreter(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.environment = {}

    def _visit_FunctionCall(self, node):
        # TODO: Implement!
        return 0

    def _visit_Assignment(self, node):
        self.environment[node.identifier] = self.visit(node.value)

    def _visit_BinaryOperator(self, node):
        operators = {'+': lambda a, b: a + b,
                     '-': lambda a, b: a - b,
                     '*': lambda a, b: a * b,
                     '/': lambda a, b: a / b}
        a = self.visit(node.a)
        b = self.visit(node.b)
        return operators[node.operator](a, b)

    def _visit_UnaryOperator(self, node):
        operators = {'+': lambda a: +a,
                     '-': lambda a: -a}
        a = self.visit(node.a)
        return operators[node.operator](a)

    def _visit_Identifier(self, node):
        return self.environment[node.name]

    def _visit_IntegerConstant(self, node):
        return node.value

    def _visit_RealConstant(self, node):
        return node.value
