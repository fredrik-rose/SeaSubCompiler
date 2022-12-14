"""
The symbol table of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast


def attach_symbol_table(abstract_syntax_tree):
    symbol_table = SymbolTable()
    add_builtins(symbol_table)
    _SymbolTableVisitor().attach(abstract_syntax_tree, symbol_table)
    return symbol_table


def add_builtins(symbol_table):
    symbol_table['int'] = BuiltinType('int')
    symbol_table['double'] = BuiltinType('double')


def save_graph(symbol_table, file_path):
    def level(node, connections=[]):
        name = f"===== {node.name} L{node.level} ====="
        symbols = "\\n".join(f'{key}: {str(value)}' for key, value in node.symbols.items())
        label = f"{name}\\n{symbols}"
        connections.append(f'node{id(node)} [label="{label}", shape=box]')
        for child in node.inner:
            level(child, connections)
            connections.append(f"node{id(node)} -> node{id(child)};")
        return connections

    connections = level(symbol_table)
    internal = "\n".join(connections)
    graph = f"digraph symboltable {{\n{internal}\n}}"
    with open(file_path, 'w') as file:
        file.write(graph)


class SymbolTable:
    def __init__(self, name='global', outer=None):
        self._name = name
        self._symbols = {}
        self._outer = outer
        self._inner = []
        if outer is not None:
            self.level = outer.level + 1
            outer._inner.append(self)
        else:
            self.level = 0

    def __setitem__(self, identifier, symbol):
        self._symbols[identifier] = symbol

    def __getitem__(self, identifier):
        if identifier in self._symbols:
            return self._symbols[identifier]
        elif self.outer:
            return self.outer[identifier]
        else:
            raise KeyError(f"Identifier '{identifier}' not found in symbol table")

    def __repr__(self):
        return "SymbolTable()"

    def __str__(self):
        symbols = ", ".join(str(symbol) for symbol in self._symbols.values())
        children = "".join(str(child) for child in self.inner) if self.inner else ""
        output = f"{self._name}L{self.level}: {symbols}\n{children}"
        return output

    @property
    def name(self):
        return self._name

    @property
    def symbols(self):
        return self._symbols

    @property
    def outer(self):
        return self._outer

    @property
    def inner(self):
        return self._inner


class Symbol:
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return f'Symbol({self._name})'

    def __str__(self):
        return f'Symbol<{self._name}>'

    @property
    def name(self):
        return self._name


class BuiltinType(Symbol):
    def __repr__(self):
        return f'BuiltinType({self.name})'

    def __str__(self):
        return f'BuiltinType<{self.name}>'


class Function(Symbol):
    def __init__(self, name, return_type):
        super().__init__(name)
        self._type = return_type
        self._parameters = []
        self._variables = []

    def __repr__(self):
        return f"Function({self.name}, {self._type}, {self._parameters})"

    def __str__(self):
        return f"Function<{self.name}({', '.join(str(param) for param in self._parameters)}): {self._type}>"

    @property
    def type(self):
        return self._type

    @property
    def parameters(self):
        return self._parameters

    @property
    def variables(self):
        return self._variables

    def add_parameter(self, parameter):
        parameter.index = len(self._parameters)
        self._parameters.append(parameter)

    def add_variable(self, variable):
        variable.index = len(self._variables)
        self._variables.append(variable)


class Parameter(Symbol):
    def __init__(self, name, parameter_type):
        super().__init__(name)
        self._type = parameter_type
        self._index = None

    def __repr__(self):
        return f"Parameter({self.name}, {self._type})"

    def __str__(self):
        return f"Parameter<{self.name}: {self._type} @ {self._index}>"

    @property
    def type(self):
        return self._type

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value


class Variable(Symbol):
    def __init__(self, name, symbol_type):
        super().__init__(name)
        self._type = symbol_type
        self._index = None

    def __repr__(self):
        return f"Variable({self.name}, {self._type})"

    def __str__(self):
        return f"Variable<{self.name}: {self._type} @ {self._index}>"

    @property
    def type(self):
        return self._type

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value


class _SymbolTableVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self._current_scope = None
        self._current_function = None

    def attach(self, tree, global_scope):
        self._current_scope = global_scope
        self.visit(tree)
        assert self._current_scope == global_scope

    def _visit_NoOperation(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_TranslationUnit(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_FunctionDefinition(self, node):
        self._current_function = Function(node.identifier, node.type_specifier)
        self._current_scope[node.identifier] = self._current_function
        self._current_scope = SymbolTable(node.identifier, self._current_scope)
        self._generic_visit(node)
        self._add_symbol_table(node)
        self._current_scope = self._current_scope.outer
        self._current_function = None

    def _visit_Parameter(self, node):
        parameter = Parameter(node.identifier, node.type_specifier)
        self._current_function.add_parameter(parameter)
        self._current_scope[node.identifier] = parameter
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_FunctionCall(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_ReturnStatement(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_CompoundStatement(self, node):
        self._current_scope = SymbolTable(self._current_scope.name, self._current_scope)
        self._generic_visit(node)
        self._add_symbol_table(node)
        self._current_scope = self._current_scope.outer

    def _visit_Declaration(self, node):
        variable = Variable(node.identifier, node.type_specifier)
        self._current_function.add_variable(variable)
        self._current_scope[node.identifier] = variable
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_Assignment(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_IfStatement(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_BinaryOperator(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_UnaryOperator(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_Identifier(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_IntegerConstant(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_RealConstant(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _add_symbol_table(self, node):
        node.symbol_table = self._current_scope
