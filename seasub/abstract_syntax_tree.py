"""
The abstract syntax tree of the sea sub compiler.
"""
import abc


def save_graph(symbol_table, file_path):
    _Graph().save(symbol_table, file_path)


def _get_nodes():
    return (NoOperation, TranslationUnit, FunctionDefinition, Parameter, FunctionCall,
            ReturnStatement, CompoundStatement, Declaration, Assignment, IfStatement,
            BinaryOperator, UnaryOperator, Identifier, IntegerConstant, RealConstant)


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
    def __init__(self, token):
        self._token = token
        self._symbol_table = None

    @property
    def token(self):
        return self._token

    @property
    def symbol_table(self):
        return self._symbol_table

    @symbol_table.setter
    def symbol_table(self, value):
        self._symbol_table = value

    @abc.abstractmethod
    def get_children(self):
        ...


class NoOperation(AbstractSyntaxTreeNode):
    def __init__(self, token):
        super().__init__(token)

    def __repr__(self):
        return "NoOperation()"

    def __str__(self):
        return "NoOperation"

    def get_children(self):
        return []


class TranslationUnit(AbstractSyntaxTreeNode):
    def __init__(self, token, functions):
        super().__init__(token)
        self._functions = functions

    def __repr__(self):
        return f"TranslationUnit({self._functions})"

    def __str__(self):
        return "\n".join(f"{str(func)}" for func in self._functions)

    def get_children(self):
        return self._functions


class FunctionDefinition(AbstractSyntaxTreeNode):
    def __init__(self, token, type_specifier, identifier, parameters, body):
        super().__init__(token)
        self._type_specifier = type_specifier
        self._identifier = identifier
        self._parameters = parameters
        self._body = body

    @property
    def type_specifier(self):
        return self._type_specifier

    @property
    def identifier(self):
        return self._identifier

    @property
    def parameters(self):
        return self._parameters

    def __repr__(self):
        return f"FunctionDefinition({self._type_specifier}, {self._identifier}, {self._parameters}, <body>)"

    def __str__(self):
        return f"{self._type_specifier} {self._identifier} ({self._parameters})\n{self._body}"

    def get_children(self):
        return self._parameters + [self._body]


class Parameter(AbstractSyntaxTreeNode):
    def __init__(self, token, type_specifier, identifier):
        super().__init__(token)
        self._type_specifier = type_specifier
        self._identifier = identifier

    @property
    def type_specifier(self):
        return self._type_specifier

    @property
    def identifier(self):
        return self._identifier

    def __repr__(self):
        return f"Parameter({self._type_specifier}, {self._identifier})"

    def __str__(self):
        return f"{str(self._type_specifier)} {str(self._identifier)}"

    def get_children(self):
        return []


class FunctionCall(AbstractSyntaxTreeNode):
    def __init__(self, token, identifier, arguments):
        super().__init__(token)
        self._identifier = identifier
        self._arguments = arguments

    @property
    def identifier(self):
        return self._identifier

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value

    def __repr__(self):
        return f"FunctionCall({self._identifier}, {self._arguments})"

    def __str__(self):
        return f"{str(self._identifier)} ({self._arguments})"

    def get_children(self):
        return [self._identifier] + self._arguments


class ReturnStatement(AbstractSyntaxTreeNode):
    def __init__(self, token, value):
        super().__init__(token)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f"Return({repr(self._value)})"

    def __str__(self):
        return f"return {self._value}"

    def get_children(self):
        return [self._value]


class CompoundStatement(AbstractSyntaxTreeNode):
    def __init__(self, token, declarations, statements):
        super().__init__(token)
        self._declarations = declarations
        self._statements = statements

    def __repr__(self):
        return f"CompoundStatement({self._declarations}, {self._statements})"

    def __str__(self):
        return "\n".join(f"{str(item)}" for item in self._declarations + self._statements)

    def get_children(self):
        return self._declarations + self._statements


class Declaration(AbstractSyntaxTreeNode):
    def __init__(self, token, type_specifier, identifier):
        super().__init__(token)
        self._type_specifier = type_specifier
        self._identifier = identifier

    @property
    def type_specifier(self):
        return self._type_specifier

    @property
    def identifier(self):
        return self._identifier

    def __repr__(self):
        return f"Declaration({self._type_specifier}, {self._identifier})"

    def __str__(self):
        return f"{str(self._type_specifier)} {str(self._identifier)}"

    def get_children(self):
        return []


class Assignment(AbstractSyntaxTreeNode):
    def __init__(self, token, identifier, value):
        super().__init__(token)
        self._identifier = identifier
        self._value = value

    @property
    def identifier(self):
        return self._identifier

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f"Assignment({repr(self._identifier)}, {repr(self._value)})"

    def __str__(self):
        return f"{self._identifier} = {self._value}"

    def get_children(self):
        return [self._value]


class IfStatement(AbstractSyntaxTreeNode):
    def __init__(self, token, predicate, consequent, alternative):
        super().__init__(token)
        self._predicate = predicate
        self._consequent = consequent
        self._alternative = alternative

    @property
    def predicate(self):
        return self._predicate

    @predicate.setter
    def predicate(self, value):
        self._predicate = value

    @property
    def consequent(self):
        return self._consequent

    @property
    def alternative(self):
        return self._alternative

    def __repr__(self):
        return f"IfStatement({repr(self._predicate)}, {repr(self._consequent)}, {repr(self._alternative)})"

    def __str__(self):
        return f"if ({self._predicate})\nthen\n{self._consequent}\nelse\n{self._alternative}"

    def get_children(self):
        return [self._predicate, self._consequent, self._alternative]


class BinaryOperator(AbstractSyntaxTreeNode):
    def __init__(self, token, operator, a, b):
        super().__init__(token)
        self._operator = operator
        self._a = a
        self._b = b

    @property
    def operator(self):
        return self._operator

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def __repr__(self):
        return f"BinaryOperator({repr(self._operator)}, {repr(self._a)}, {repr(self._b)})"

    def __str__(self):
        return f"({self._a} {self._operator} {self._b})"

    def get_children(self):
        return [self._a, self._b]


class UnaryOperator(AbstractSyntaxTreeNode):
    def __init__(self, token, operator, a):
        super().__init__(token)
        self._operator = operator
        self._a = a

    @property
    def operator(self):
        return self._operator

    @property
    def a(self):
        return self._a

    def __repr__(self):
        return f"UnaryOperator({repr(self._operator)}, {repr(self._a)})"

    def __str__(self):
        return f"({self._operator}{self._a})"

    def get_children(self):
        return [self._a]


class Identifier(AbstractSyntaxTreeNode):
    def __init__(self, token, name):
        super().__init__(token)
        self._name = name

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return f"Identifier({repr(self._name)})"

    def __str__(self):
        return f"{self._name}"

    def get_children(self):
        return []


class IntegerConstant(AbstractSyntaxTreeNode):
    def __init__(self, token, value):
        super().__init__(token)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f"IntegerConstant({repr(self._value)})"

    def __str__(self):
        return str(self._value)

    def get_children(self):
        return []


class RealConstant(AbstractSyntaxTreeNode):
    def __init__(self, token, value):
        super().__init__(token)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return f"RealConstant({repr(self._value)})"

    def __str__(self):
        return str(self._value)

    def get_children(self):
        return []


class _Graph(NodeVisitor):
    def __init__(self):
        super().__init__()
        self._connections = None

    def save(self, abstract_syntax_tree, file_path):
        self._connections = []
        self.visit(abstract_syntax_tree)
        internal = "\n".join(self._connections)
        graph = f"digraph abstractsyntaxtree {{ {internal} }}"
        with open(file_path, 'w') as file:
            file.write(graph)

    def _visit_NoOperation(self, node):
        self._add_connections(node, "NOP")

    def _visit_TranslationUnit(self, node):
        self._add_connections(node, "Translation unit")

    def _visit_FunctionDefinition(self, node):
        self._add_connections(node, f"{node.identifier}()")

    def _visit_Parameter(self, node):
        self._add_connections(node, f"{node.type_specifier} {node.identifier}")

    def _visit_FunctionCall(self, node):
        self._add_connections(node, "( )")

    def _visit_ReturnStatement(self, node):
        self._add_connections(node, "return")

    def _visit_CompoundStatement(self, node):
        self._add_connections(node, "{ }")

    def _visit_Declaration(self, node):
        self._add_connections(node, f"{node.type_specifier} {node.identifier}")

    def _visit_Assignment(self, node):
        self._add_connections(node, f"{node.identifier} = ")

    def _visit_IfStatement(self, node):
        self._add_connections(node, "if")

    def _visit_BinaryOperator(self, node):
        self._add_connections(node, f"{node.operator}")

    def _visit_UnaryOperator(self, node):
        self._add_connections(node, f"{node.operator}")

    def _visit_Identifier(self, node):
        self._add_connections(node, f"{node.name}")

    def _visit_IntegerConstant(self, node):
        self._add_connections(node, f"{node.value}")

    def _visit_RealConstant(self, node):
        self._add_connections(node, f"{node.value}")

    def _add_connections(self, node, label):
        self._connections.append(f'node{id(node)} [label="{label}"]')
        self._generic_visit(node)
        for child in node.get_children():
            self._connections.append(f"node{id(node)} -> node{id(child)};")
