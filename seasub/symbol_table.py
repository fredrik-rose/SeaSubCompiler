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
        self.name = name
        self._symbols = {}
        self._outer = outer
        self._inner = []
        if outer is not None:
            self.level = outer.level + 1
            outer._inner.append(self)
        else:
            self.level = 0

    @property
    def symbols(self):
        return self._symbols

    @property
    def outer(self):
        return self._outer

    @property
    def inner(self):
        return self._inner

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
        output = f"{self.name}L{self.level}: {symbols}\n{children}"
        return output


class Symbol:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Symbol({self.name})'

    def __str__(self):
        return f'Symbol<{self.name}>'


class BuiltinType(Symbol):
    def __repr__(self):
        return f'BuiltinType({self.name})'

    def __str__(self):
        return f'BuiltinType<{self.name}>'


class Function(Symbol):
    def __init__(self, name, return_type, parameters):
        super().__init__(name)
        self.type = return_type
        self.parameters = parameters

    def __repr__(self):
        return f"Function({self.name}, {self.type}, {self.parameters})"

    def __str__(self):
        return f"Function<{self.name}({', '.join(str(param) for param in self.parameters)}): {self.type}>"


class Parameter(Symbol):
    def __init__(self, name, parameter_type):
        super().__init__(name)
        self.type = parameter_type

    def __repr__(self):
        return f"Parameter({self.name}, {self.type})"

    def __str__(self):
        return f"Parameter<{self.name}: {self.type}>"


class Variable(Symbol):
    def __init__(self, name, symbol_type):
        super().__init__(name)
        self.type = symbol_type

    def __repr__(self):
        return f"Variable({self.name}, {self.type})"

    def __str__(self):
        return f"Variable<{self.name}: {self.type}>"


class _SymbolTableVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.current_scope = None

    def attach(self, tree, global_scope):
        self.current_scope = global_scope
        self.visit(tree)
        assert self.current_scope == global_scope

    def _visit_NoOperation(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_TranslationUnit(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_Function(self, node):
        self.current_scope = SymbolTable(node.identifier, self.current_scope)
        self._generic_visit(node)
        self._add_symbol_table(node)
        parameters = [self.current_scope[param.identifier] for param in node.parameters]
        self.current_scope = self.current_scope.outer
        self.current_scope[node.identifier] = Function(node.identifier, node.type_specifier, parameters)

    def _visit_Parameter(self, node):
        self.current_scope[node.identifier] = Parameter(node.identifier, node.type_specifier)
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_ReturnStatement(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_CompoundStatement(self, node):
        self.current_scope = SymbolTable(self.current_scope.name, self.current_scope)
        self._generic_visit(node)
        self._add_symbol_table(node)
        self.current_scope = self.current_scope.outer

    def _visit_Declaration(self, node):
        self.current_scope[node.identifier] = Variable(node.identifier, node.type_specifier)
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_Assignment(self, node):
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
        node.symbol_table = self.current_scope
