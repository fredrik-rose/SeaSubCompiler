"""
The optimizer of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast

def optimize(abstract_syntax_tree):
    _ConstantFolding().visit(abstract_syntax_tree)


class _ConstantFolding(ast.NodeVisitor):
    def _visit_FunctionCall(self, node):
        assert len(node.get_children()) == 1 + len(node.arguments)
        self.visit(node.identifier)
        node.arguments = [self.visit(arg) for arg in node.arguments]
        return node

    def _visit_ReturnStatement(self, node):
        assert len(node.get_children()) == 1
        node.value = self.visit(node.value)

    def _visit_Assignment(self, node):
        assert len(node.get_children()) == 1
        node.value = self.visit(node.value)

    def _visit_BinaryOperator(self, node):
        assert len(node.get_children()) == 2
        a = self.visit(node.a)
        b = self.visit(node.b)
        if isinstance(a, ast.IntegerConstant) and isinstance(b, ast.IntegerConstant):
            operators = {'+': lambda a, b: a + b,
                         '-': lambda a, b: a - b,
                         '*': lambda a, b: a * b,
                         '/': lambda a, b: a // b}
            value = operators[node.operator](a.value, b.value)
            new_node = ast.IntegerConstant(node.token, value)
            new_node.symbol_table = node.symbol_table
            return new_node
        if isinstance(a, ast.RealConstant) and isinstance(b, ast.RealConstant):
            operators = {'+': lambda a, b: a + b,
                         '-': lambda a, b: a - b,
                         '*': lambda a, b: a * b,
                         '/': lambda a, b: a / b}
            value = operators[node.operator](a.value, b.value)
            new_node = ast.RealConstant(node.token, value)
            new_node.symbol_table = node.symbol_table
            return new_node
        return node

    def _visit_UnaryOperator(self, node):
        assert len(node.get_children()) == 1
        a = self.visit(node.a)
        if isinstance(a, (ast.IntegerConstant, ast.RealConstant)):
            operators = {'+': lambda a: a,
                         '-': lambda a: -a}
            a.value = operators[node.operator](a.value)
            return a
        return node

    def _visit_Identifier(self, node):
        assert len(node.get_children()) == 0
        return node

    def _visit_IntegerConstant(self, node):
        assert len(node.get_children()) == 0
        return node

    def _visit_RealConstant(self, node):
        assert len(node.get_children()) == 0
        return node
