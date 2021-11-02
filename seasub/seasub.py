"""
The sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import interpreter
from seasub import lexer
from seasub import parser
from seasub import semantic_analyzer as sa
from seasub import symbol_table as st

def compile(file_path):
    with open(file_path) as file:
        source_code = file.read()
    print(f"Source code: {source_code}")
    token_stream = lexer.tokenize(source_code)
    tree = parser.parse(token_stream)
    print(f"Parse tree:\n{repr(tree)}\n")
    print(f"Statement(s):\n{tree}\n")
    symbol_table = st.attach_symbol_table(tree)
    st.save_graph(symbol_table, 'symbol-table.dot')
    sa.analyze_semantics(tree)
    ast.save_graph(tree, 'abstract-syntax-tree.dot')
    interp = interpreter.Intepreter()
    interp.visit(tree)
    print(f"Result: {interp.environment}")
