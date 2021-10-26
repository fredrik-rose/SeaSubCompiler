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


class SymbolTable:
    def __init__(self, outer=None):
        self._symbols = {}
        self._outer = outer
        self._inner = []
        if outer is not None:
            outer._inner.append(self)

    @property
    def outer(self):
        return self._outer

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
        return 'SymbolTable()'

    def __str__(self):
        if self._outer is not None:
            return str(self._outer)
        return f'----- SYMBOL TABLE -----\n{self._str()}'

    def _str(self, level=0):
        symbols = ', '.join(str(symbol) for symbol in self._symbols.values())
        children = ''.join(child._str(level + 1) for child in self._inner)
        output = f'L{level}: {symbols}\n{children}'
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

    def _visit_ReturnStatement(self, node):
        self._generic_visit(node)
        self._add_symbol_table(node)

    def _visit_CompoundStatement(self, node):
        self.current_scope = SymbolTable(self.current_scope)
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
