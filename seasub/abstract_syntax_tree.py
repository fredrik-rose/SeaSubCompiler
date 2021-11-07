"""
The abstract syntax tree of the sea sub compiler.
"""
import abc


def save_graph(symbol_table, file_path):
    _Graph().save(symbol_table, file_path)


def _get_nodes():
    return (NoOperation, TranslationUnit, FunctionDefinition, Parameter, FunctionCall,
            ReturnStatement, CompoundStatement, Declaration, Assignment, BinaryOperator,
            UnaryOperator, Identifier, IntegerConstant, RealConstant)


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
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "NoOperation()"

    def __str__(self):
        return "NoOperation"

    def get_children(self):
        return []


class TranslationUnit(AbstractSyntaxTreeNode):
    def __init__(self, token, functions):
        self.token = token
        self.functions = functions

    def __repr__(self):
        return f"TranslationUnit({self.functions})"

    def __str__(self):
        return "\n".join(f"{str(func)}" for func in self.functions)

    def get_children(self):
        return self.functions


class FunctionDefinition(AbstractSyntaxTreeNode):
    def __init__(self, token, type_specifier, identifier, parameters, body):
        self.token = token
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionDefinition({self.type_specifier}, {self.identifier}, {self.parameters}, <body>)"

    def __str__(self):
        return f"{self.type_specifier} {self.identifier} ({self.parameters})\n{self.body}"

    def get_children(self):
        return self.parameters + [self.body]


class Parameter(AbstractSyntaxTreeNode):
    def __init__(self, token, type_specifier, identifier):
        self.token = token
        self.type_specifier = type_specifier
        self.identifier = identifier

    def __repr__(self):
        return f"Parameter({self.type_specifier}, {self.identifier})"

    def __str__(self):
        return f"{str(self.type_specifier)} {str(self.identifier)}"

    def get_children(self):
        return []


class FunctionCall(AbstractSyntaxTreeNode):
    def __init__(self, token, identifier, arguments):
        self.token = token
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall({self.identifier}, {self.arguments})"

    def __str__(self):
        return f"{str(self.identifier)} ({self.arguments})"

    def get_children(self):
        return [self.identifier] + self.arguments


class ReturnStatement(AbstractSyntaxTreeNode):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __repr__(self):
        return f"Return({repr(self.value)})"

    def __str__(self):
        return f"return {self.value}"

    def get_children(self):
        return [self.value]


class CompoundStatement(AbstractSyntaxTreeNode):
    def __init__(self, token, declarations, statements):
        self.token = token
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"CompoundStatement({self.declarations}, {self.statements})"

    def __str__(self):
        return "\n".join(f"{str(item)}" for item in self.declarations + self.statements)

    def get_children(self):
        return self.declarations + self.statements


class Declaration(AbstractSyntaxTreeNode):
    def __init__(self, token, type_specifier, identifier):
        self.token = token
        self.type_specifier = type_specifier
        self.identifier = identifier

    def __repr__(self):
        return f"Declaration({self.type_specifier}, {self.identifier})"

    def __str__(self):
        return f"{str(self.type_specifier)} {str(self.identifier)}"

    def get_children(self):
        return []


class Assignment(AbstractSyntaxTreeNode):
    def __init__(self, token, identifier, value):
        self.token = token
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"Assignment({repr(self.identifier)}, {repr(self.value)})"

    def __str__(self):
        return f"{self.identifier} = {self.value}"

    def get_children(self):
        return [self.value]


class BinaryOperator(AbstractSyntaxTreeNode):
    def __init__(self, token, operator, a, b):
        self.token = token
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
    def __init__(self, token, operator, a):
        self.token = token
        self.operator = operator
        self.a = a

    def __repr__(self):
        return f"UnaryOperator({repr(self.operator)}, {repr(self.a)})"

    def __str__(self):
        return f"({self.operator}{self.a})"

    def get_children(self):
        return [self.a]


class Identifier(AbstractSyntaxTreeNode):
    def __init__(self, token, name):
        self.token = token
        self.name = name

    def __repr__(self):
        return f"Identifier({repr(self.name)})"

    def __str__(self):
        return f"{self.name}"

    def get_children(self):
        return []


class IntegerConstant(AbstractSyntaxTreeNode):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __repr__(self):
        return f"IntegerConstant({repr(self.value)})"

    def __str__(self):
        return str(self.value)

    def get_children(self):
        return []


class RealConstant(AbstractSyntaxTreeNode):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __repr__(self):
        return f"RealConstant({repr(self.value)})"

    def __str__(self):
        return str(self.value)

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
