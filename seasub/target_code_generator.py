"""
The target code generator of the sea sub compiler.

Generates code for the x86-64 architecture.
"""
import functools as ft

from seasub import symbol_table as symtab


_SIZE_OF_INT = 4


def generate(intermediate_code, symbol_table, file_name):
    output = []
    output.append(f'.file "{file_name}"')
    output.append(r'.text')
    for function, body in intermediate_code.items():
        function_symbol = symbol_table[function]
        output.append(f'.globl {function_symbol.name}')
        output.append(f'.type {function_symbol.name}, @function')
        output.append(f'{function_symbol.name}:')
        _emit_function(function_symbol, body, output)
        output.append(f'.size {function_symbol.name}, .-{function_symbol.name}')
    return output


def save_code(code, file_path):
    with open(file_path, 'w') as file:
        file.writelines("\n".join(line if ':' in line else f'\t{line}' for line in code))
        file.write("\n")


def _emit_function(function, body, output):
    def prologue():
        local_variables_size = _get_next_multiple(len(function.variables) * _SIZE_OF_INT, 8)  # 8 bytes aligned.
        output.append(r'pushq %rbp')  # Save the previous frame pointer.
        output.append(r'movq %rsp, %rbp')  # Set the frame pointer to the current frame (i.e. current stack pointer).
        output.append(f'subq ${local_variables_size}, %rsp')  # Allocate local variables on the stack.

    def epilogue():
        output.append(r'movq %rbp, %rsp')  # Restore the stack pointer.
        output.append(r'popq %rbp')  # Restore the frame pointer.
        output.append(r'ret')  # Pops the return address from the stack and jumps to it.

    prologue()
    for instruction in body:
        globals()[instruction.operator](instruction, output)  # Calls the q_xxx functions below.
    epilogue()


def q_param(quad, output):
    value = _get_address(quad.symbol_table[quad.operand_1])
    output.append(f'movl {value}, %eax')
    output.append(r'pushq %rax')  # Push the parameter on the stack.
    # The lower 32 bits of rax is eax, the reason for doing like this is to keep the stack pointer aligned to 8 bytes.


def q_call(quad, output):
    function = quad.symbol_table[quad.operand_1]
    result = _get_address(quad.symbol_table[quad.result])
    output.append(f'call {quad.operand_1}')  # Pushes the return address on the stack.
    output.append(f'addq ${len(function.parameters) * _SIZE_OF_INT * 2}, %rsp')  # Remove the parameters from the stack.
    # Multiply by 2 since each parameter is 8 byte aligned.
    output.append(f'movl %eax, {result}')  # Store the returned value (which will be located in eax).


def q_load(quad, output):
    result = _get_address(quad.symbol_table[quad.result])
    output.append(f'movl ${quad.operand_1}, {result}')


def q_uplus(quad, output):
    pass  # Unary plus doesn't do anything.


def q_uminus(quad, output):
    operand = _get_address(quad.symbol_table[quad.operand_1])
    result = _get_address(quad.symbol_table[quad.result])
    output.append(f'movl {operand}, %eax')
    output.append(r'negl %eax')
    output.append(f'movl %eax, {result}')


def q_plus(quad, output):
    _binary_operator('addl', quad, output)


def q_minus(quad, output):
    _binary_operator('subl', quad, output)


def q_mult(quad, output):
    _binary_operator('imull', quad, output)


def q_div(quad, output):
    operand_1 = _get_address(quad.symbol_table[quad.operand_1])
    operand_2 = _get_address(quad.symbol_table[quad.operand_2])
    result = _get_address(quad.symbol_table[quad.result])
    output.append(f'movl {operand_1}, %eax')
    output.append(r'cltd')  # Alias for cdq, sign-extends eax into edx:eax.
    output.append(f'movl {operand_2}, %ecx')
    output.append(r'idivl %ecx')  # Divides to content of edx:eax with ecx, result is eax: quotient, edx: remainder.
    output.append(f'movl %eax, {result}')


def _binary_operator(operator, quad, output):
    operand_1 = _get_address(quad.symbol_table[quad.operand_1])
    operand_2 = _get_address(quad.symbol_table[quad.operand_2])
    result = _get_address(quad.symbol_table[quad.result])
    output.append(f'movl {operand_2}, %edx')
    output.append(f'movl {operand_1}, %eax')
    output.append(f'{operator} %edx, %eax')
    output.append(f'movl %eax, {result}')


def q_assign(quad, output):
    value = _get_address(quad.symbol_table[quad.operand_1])
    variable = _get_address(quad.symbol_table[quad.result])
    output.append(f'movl {value}, %eax')
    output.append(f'movl %eax, {variable}')


def q_label(quad, output):
    output.append(f'{quad.operand_1}:')


def q_return(quad, output):
    value = _get_address(quad.symbol_table[quad.operand_2])
    output.append(f'movl {value}, %eax')  # Move the return value to the return register (eax).
    output.append(f'jmp {quad.operand_1}')  # Jump to the end of the function (epilogue).


@ft.singledispatch
def _get_address(symbol):
    raise NotImplementedError()


@_get_address.register(symtab.Parameter)
def _(symbol):
    # %rbp + 0: Previous stack frame pointer (i.e. rbp) [8 bytes].
    # %rbp + 8: Return address [8 bytes].
    # %rbp + 16: First parameter [4 bytes].
    # %rbp + 20: Alignment padding [4 bytes].
    # %rbp + 24: Second parameter [4 bytes].
    # %rbp + 28: Alignment padding [4 bytes].
    offset = (symbol.index * _SIZE_OF_INT * 2) + 16  # Multiply by 2 since each parameter is 8 byte aligned.
    return f'{offset}(%rbp)'


@_get_address.register(symtab.Variable)
def _(symbol):
    # %rbp - 0: Previous stack frame pointer (i.e. rbp) [8 bytes].
    # %rbp - 4: First local variable [4 bytes].
    # %rbp - 8: Second local variable [4 bytes].
    offset = (symbol.index + 1) * _SIZE_OF_INT
    return f'-{offset}(%rbp)'


def _get_next_multiple(number, multiple):
    return (number + (multiple - 1)) // multiple * multiple
