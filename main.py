"""
The sea sub compiler entry point.
"""
import argparse
import pathlib

from seasub import seasub


def main():
    parser = argparse.ArgumentParser(description="A compiler for the Sea Sub (C subset) language.")
    parser.add_argument('input', type=pathlib.Path, help="the c source file to be compiled")
    parser.add_argument('--ast', type=pathlib.Path, metavar='ast.dot',
                        help=".dot file to store the abstract syntax tree")
    parser.add_argument('--symbol-table', type=pathlib.Path, metavar='symbol-table.dot',
                        help=".dot file to store the symbol table")
    args = parser.parse_args()
    seasub.run(args.input, ast_graph_path=args.ast, symbol_table_graph_path=args.symbol_table)


if __name__ == "__main__":
    main()
