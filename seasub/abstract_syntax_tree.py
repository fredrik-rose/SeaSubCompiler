"""
The abstract syntax tree of the sea sub compiler.
"""
import abc


def _get_nodes():
    return (NoOperation, Function, Parameter, ReturnStatement, CompoundStatement, Declaration,
            Assignment, BinaryOperator, UnaryOperator, Identifier, IntegerConstant, RealConstant)


class NodeVisitor:
    def __init__(self):
        visitors = set(self._node_visitor(node) for node in _get_nodes())
        for element in dir(self):
            if element.startswith('_visit_') and element not in visitors:
                raise AttributeError(f'{element} is not a valid visitor as the node does not exist')

    @staticmethod
    def _node_visitor(node_class):
        return f'_visit_{node_class.__name__}'

    def visit(self, node):
        visitor = getattr(self, self._node_visitor(type(node)), self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        for child in node.get_children():
            self.visit(child)


class AbstractSyntaxTreeNode(abc.ABC):
    @abc.abstractmethod
    def get_children(self):
        ...


class NoOperation(AbstractSyntaxTreeNode):
    def __repr__(self):
        return "NoOperation()"

    def __str__(self):
        return "NoOperation"

    def get_children(self):
        return []


class Function(AbstractSyntaxTreeNode):
    def __init__(self, type_specifier, identifier, parameters, body):
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"Function({self.type_specifier}, {self.identifier}, {self.parameters}, <body>)"

    def __str__(self):
        return f"{self.type_specifier} {self.identifier} ({self.parameters})\n{self.body}"

    def get_children(self):
        return self.parameters + [self.body]


class Parameter(AbstractSyntaxTreeNode):
    def __init__(self, type_specifier, identifier):
        self.type_specifier = type_specifier
        self.identifier = identifier

    def __repr__(self):
        return f"Parameter({self.type_specifier}, {self.identifier})"

    def __str__(self):
        return f"{str(self.type_specifier)} {str(self.identifier)}"

    def get_children(self):
        return []


class ReturnStatement(AbstractSyntaxTreeNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({repr(self.value)})"

    def __str__(self):
        return f"return {self.value}"

    def get_children(self):
        return [self.value]


class CompoundStatement(AbstractSyntaxTreeNode):
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"CompoundStatement({self.declarations}, {self.statements})"

    def __str__(self):
        return "\n".join(f"{str(item)}" for item in self.declarations + self.statements)

    def get_children(self):
        return self.declarations + self.statements


class Declaration(AbstractSyntaxTreeNode):
    def __init__(self, type_specifier, identifier):
        self.type_specifier = type_specifier
        self.identifier = identifier

    def __repr__(self):
        return f"Declaration({self.type_specifier}, {self.identifier})"

    def __str__(self):
        return f"{str(self.type_specifier)} {str(self.identifier)}"

    def get_children(self):
        return []


class Assignment(AbstractSyntaxTreeNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"Assignment({repr(self.identifier)}, {repr(self.value)})"

    def __str__(self):
        return f"{self.identifier} = {self.value}"

    def get_children(self):
        return [self.value]


class BinaryOperator(AbstractSyntaxTreeNode):
    def __init__(self, operator, a, b):
        self.operator = operator
        self.a = a
        self.b = b

    def __repr__(self):
        return f"BinaryOperator({repr(self.operator)}, {repr(self.a)}, {repr(self.b)})"

    def __str__(self):
        return f"({self.a} {self.operator} {self.b})"

    def get_children(self):
        return [self.a, self.b]


class UnaryOperator(AbstractSyntaxTreeNode):
    def __init__(self, operator, a):
        self.operator = operator
        self.a = a

    def __repr__(self):
        return f"UnaryOperator({repr(self.operator)}, {repr(self.a)})"

    def __str__(self):
        return f"({self.operator}{self.a})"

    def get_children(self):
        return [self.a]


class Identifier(AbstractSyntaxTreeNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({repr(self.name)})"

    def __str__(self):
        return f"{self.name}"

    def get_children(self):
        return []


class IntegerConstant(AbstractSyntaxTreeNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IntegerConstant({repr(self.value)})"

    def __str__(self):
        return str(self.value)

    def get_children(self):
        return []


class RealConstant(AbstractSyntaxTreeNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"RealConstant({repr(self.value)})"

    def __str__(self):
        return str(self.value)

    def get_children(self):
        return []
