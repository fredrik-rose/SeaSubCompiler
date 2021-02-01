"""
The abstract syntax tree of the sea sub compiler.
"""


class NoOperation:
    def __repr__(self):
        return "NoOperation()"

    def __str__(self):
        return "NoOperation"


class CompoundStatement:
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"CompoundStatement({self.declarations}, {self.statements})"

    def __str__(self):
        return "\n".join(f"{str(item)}" for item in self.declarations + self.statements)


class Declaration:
    def __init__(self, type_specifier, identifier):
        self.type_specifier = type_specifier.value
        self.identifier = identifier

    def __repr__(self):
        return f"Declaration({self.type_specifier}, {self.identifier})"

    def __str__(self):
        return f"{str(self.type_specifier)} {str(self.identifier)}"


class Assignment:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"Assignment({repr(self.identifier)}, {repr(self.value)})"

    def __str__(self):
        return f"{self.identifier} = {self.value}"


class BinaryOperator:
    def __init__(self, operator, a, b):
        self.operator = operator.value
        self.a = a
        self.b = b

    def __repr__(self):
        return f"BinaryOperator({repr(self.operator)}, {repr(self.a)}, {repr(self.b)})"

    def __str__(self):
        return f"({self.a} {self.operator} {self.b})"


class UnaryOperator:
    def __init__(self, operator, a):
        self.operator = operator.value
        self.a = a

    def __repr__(self):
        return f"UnaryOperator({repr(self.operator)}, {repr(self.a)})"

    def __str__(self):
        return f"({self.operator}{self.a})"


class Identifier:
    def __init__(self, name):
        self.name = name.value

    def __repr__(self):
        return f"Identifier({repr(self.name)})"

    def __str__(self):
        return f"{self.name}"


class Number:
    def __init__(self, value):
        self.value = value.value

    def __repr__(self):
        return f"Number({repr(self.value)})"

    def __str__(self):
        return str(self.value)
