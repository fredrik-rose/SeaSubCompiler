"""
The interpreter of the sea sub compiler.
"""
from seasub import symbol_table as st


class NodeVisitor:
    def visit(self, node):
        visitor = getattr(self, self._visitor_name(node), self.visit_Undefined)
        return visitor(node)

    def visit_Undefined(self, node):
        raise AttributeError(f"Visitor {self._visitor_name(node)}() not implemented for type {type(self).__name__}")

    @staticmethod
    def _visitor_name(node):
        return f'visit_{type(node).__name__}'


class Intepreter(NodeVisitor):
    def __init__(self):
        self.symbol_table = st.SymbolTable()

    def visit_NoOperation(self, node):
        pass

    def visit_CompoundStatement(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        for statement in node.statements:
            self.visit(statement)

    def visit_Declaration(self, node):
        pass

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
