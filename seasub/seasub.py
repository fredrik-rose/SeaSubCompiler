"""
The sea sub compiler.
"""
import sys

from seasub import abstract_syntax_tree as ast
from seasub import error_handler as err
from seasub import intermediate_code_generator as icg
from seasub import lexer
from seasub import optimizer as opt
from seasub import parser
from seasub import semantic_analyzer as sa
from seasub import symbol_table as symtab
from seasub import target_code_generator as tcg


def run(input_file_path, output_file_path, optimization_level,
        ast_graph_path=None, symbol_table_graph_path=None, intermediate_code_path=None):
    with open(input_file_path, 'r') as file:
        source_code = file.read()
    try:
        token_stream = lexer.tokenize(source_code)
        abstract_syntax_tree = parser.parse(token_stream)
        symbol_table = symtab.attach_symbol_table(abstract_syntax_tree)
        sa.analyze_semantics(abstract_syntax_tree)
    except (err.SeaSubLexicalError, err.SeaSubSyntaxError, err.SeaSubSemanticError) as error:
        sys.exit(f"Error: {error}")
    if optimization_level > 0:
        opt.optimize(abstract_syntax_tree)
    intermediate_code = icg.generate_intermediate_code(abstract_syntax_tree)
    target_code = tcg.generate(intermediate_code, symbol_table, input_file_path.name)
    tcg.save_code(target_code, output_file_path)
    if ast_graph_path:
        ast.save_graph(abstract_syntax_tree, ast_graph_path)
    if symbol_table_graph_path:
        symtab.save_graph(symbol_table, symbol_table_graph_path)
    if intermediate_code_path:
        icg.save_code(intermediate_code, intermediate_code_path)
