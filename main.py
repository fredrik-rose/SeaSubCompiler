"""
The sea sub compiler entry point.
"""
import argparse
import pathlib

from seasub import seasub

_DEFAULT_OPTIMIZATION_LEVEL = 1


def main():
    optimization_levels = {0: "No optimization", 1: "Constant folding"}
    optimization_level_help = "\n".join(f"\t{level}: {description}"
                                        for level, description in optimization_levels.items())
    parser = argparse.ArgumentParser(description="A compiler for the Sea Sub (C subset) language.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input', type=pathlib.Path, help="the c source file to be compiled")
    parser.add_argument('-o',
                        help=f"optimization level (default {_DEFAULT_OPTIMIZATION_LEVEL})\n{optimization_level_help}",
                        dest='optimization_level', type=int, metavar='N', default=_DEFAULT_OPTIMIZATION_LEVEL)
    parser.add_argument('--ast', type=pathlib.Path, metavar='ast.dot',
                        help=".dot file to store the abstract syntax tree")
    parser.add_argument('--symbol-table', type=pathlib.Path, metavar='symbol-table.dot',
                        help=".dot file to store the symbol table")
    args = parser.parse_args()
    seasub.run(args.input, args.optimization_level, ast_graph_path=args.ast, symbol_table_graph_path=args.symbol_table)


if __name__ == "__main__":
    main()
