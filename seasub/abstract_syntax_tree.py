"""
The abstract syntax tree of the sea sub compiler.
"""
import abc


class NodeVisitor:
    def visit(self, node):
        visitor = getattr(self, f'visit_{type(node).__name__}', self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
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
