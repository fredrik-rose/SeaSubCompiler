"""
The sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import interpreter
from seasub import lexer
from seasub import parser
from seasub import semantic_analyzer as sa
from seasub import symbol_table as st


def run(file_path, ast_graph_path=None, symbol_table_graph_path=None):
    with open(file_path) as file:
        source_code = file.read()
    token_stream = lexer.tokenize(source_code)
    abstract_syntax_tree = parser.parse(token_stream)
    symbol_table = st.attach_symbol_table(abstract_syntax_tree)
    sa.analyze_semantics(abstract_syntax_tree)
    if ast_graph_path:
        ast.save_graph(abstract_syntax_tree, ast_graph_path)
    if symbol_table_graph_path:
        st.save_graph(symbol_table, symbol_table_graph_path)
    interp = interpreter.Intepreter()
    interp.visit(abstract_syntax_tree)
    print(f"Result: {interp.environment}")
