"""
The intermediate code generator of the sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import symbol_table as symtab


def generate_intermediate_code(abstract_syntax_tree):
    return Generator().generate(abstract_syntax_tree)


def save_code(code, file_path):
    with open(file_path, 'w') as file:
        for name, function in code.items():
            file.write(f"{name}:\n")
            file.writelines("\n".join(f"\t{instruction}" for instruction in function))
            file.write("\n")


class Quadruple:
    def __init__(self, operator, operand_1, operand_2, result):
        self._operator = operator
        self._operand_1 = operand_1
        self._operand_2 = operand_2
        self._result = result

    def __str__(self):
        def column(field):
            value = "-" if field is None else str(field)
            return f"{value}{' ' * (10 - len(value))}"
        return "".join(column(e) for e in (self._operator, self._operand_1, self._operand_2, self._result))


class Generator(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self._functions = None
        self._code = None
        self._temp_counter = None
        self._label_counter = None
        self._current_label = None
        self._current_function = None

    def generate(self, abstract_syntax_tree):
        self._temp_counter = 0
        self._label_counter = 0
        self.visit(abstract_syntax_tree)
        return self._functions

    def _visit_TranslationUnit(self, node):
        self._functions = {}
        self._generic_visit(node)

    def _visit_FunctionDefinition(self, node):
        self._verify_type(node)
        self._current_function = node.symbol_table[node.identifier]
        self._current_label = self._generate_label()
        self._code = []
        self._functions[node.identifier] = self._code
        self._generic_visit(node)
        self._code.append(Quadruple('q_label', self._current_label, None, None))
        self._code = None
        self._current_label = None

    def _visit_Parameter(self, node):
        self._verify_type(node)
        self._generic_visit(node)

    def _visit_FunctionCall(self, node):
        arguments = [self.visit(arg) for arg in node.arguments]
        for arg in arguments:
            self._code.append(Quadruple('q_param', arg, None, None))
        temp = self._generate_temp(node)
        self._code.append(Quadruple('q_call', node.identifier.name, len(arguments), temp))
        return temp

    def _visit_ReturnStatement(self, node):
        value = self.visit(node.value)
        self._code.append(Quadruple('q_return', self._current_label, value, None))

    def _visit_Declaration(self, node):
        self._verify_type(node)
        self._generic_visit(node)

    def _visit_Assignment(self, node):
        value = self.visit(node.value)
        self._code.append(Quadruple('q_assign', value, None, node.identifier))

    def _visit_BinaryOperator(self, node):
        operators = {'+': 'q_plus', '-': 'q_minus', '*': 'q_mult', '/': 'q_div'}
        a = self.visit(node.a)
        b = self.visit(node.b)
        temp = self._generate_temp(node)
        self._code.append(Quadruple(operators[node.operator], a, b, temp))
        return temp

    def _visit_UnaryOperator(self, node):
        operators = {'+': 'q_uplus', '-': 'q_uminus'}
        a = self.visit(node.a)
        temp = self._generate_temp(node)
        self._code.append(Quadruple(operators[node.operator], a, None, temp))
        return temp

    def _visit_Identifier(self, node):
        return node.name

    def _visit_IntegerConstant(self, node):
        temp = self._generate_temp(node)
        self._code.append(Quadruple('q_load', node.value, None, temp))
        return temp

    def _visit_RealConstant(self, node):
        raise NotImplementedError("The intermediate code generator does not support real values")

    @staticmethod
    def _verify_type(node):
        if node.type_specifier != 'int':
            raise NotImplementedError("The intermediate code generator only support integers")

    def _generate_temp(self, node):
        temp = f'${self._temp_counter}'
        self._temp_counter += 1
        variable = symtab.Variable(temp, 'int')
        self._current_function.add_variable(variable)
        node.symbol_table[temp] = variable
        return temp

    def _generate_label(self):
        label = f'label{self._label_counter}'
        self._label_counter += 1
        return label
