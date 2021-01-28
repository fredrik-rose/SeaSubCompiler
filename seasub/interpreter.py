"""
The interpreter of the sea sub compiler.
"""


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
    def visit_NoOperation(self, node):
        return None

    def visit_CompoundStatement(self, node):
        return [self.visit(statement) for statement in node.statements]

    def visit_Definition(self, node):
        return (node.type_specifier, self.visit(node.identifier), self.visit(node.value))

    def visit_Assignment(self, node):
        return (self.visit(node.identifier), self.visit(node.value))

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
        return node.name

    def visit_Number(self, node):
        return node.value
