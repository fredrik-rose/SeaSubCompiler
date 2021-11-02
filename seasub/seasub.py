"""
The sea sub compiler.
"""
import sys

from seasub import abstract_syntax_tree as ast
from seasub import error_handler as err
from seasub import interpreter
from seasub import lexer
from seasub import parser
from seasub import semantic_analyzer as sa
from seasub import symbol_table as st


def run(file_path, ast_graph_path=None, symbol_table_graph_path=None):
    with open(file_path, 'r') as file:
        source_code = file.read()
    try:
        token_stream = lexer.tokenize(source_code)
        abstract_syntax_tree = parser.parse(token_stream)
        symbol_table = st.attach_symbol_table(abstract_syntax_tree)
        sa.analyze_semantics(abstract_syntax_tree)
    except (err.SeaSubLexicalError, err.SeaSubSyntaxError, err.SeaSubSemanticError) as error:
        sys.exit(f"Error: {error}")
    if ast_graph_path:
        ast.save_graph(abstract_syntax_tree, ast_graph_path)
    if symbol_table_graph_path:
        st.save_graph(symbol_table, symbol_table_graph_path)
    interp = interpreter.Intepreter()
    interp.visit(abstract_syntax_tree)
    print(f"Result: {interp.environment}")
