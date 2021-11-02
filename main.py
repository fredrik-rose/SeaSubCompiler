"""
The sea sub compiler entry point.
"""
import argparse

from seasub import seasub


def main():
    parser = argparse.ArgumentParser("A compiler for the Sea Sub (C subset) language.")
    parser.parse_args()
    seasub.run('demo.c', 'abstract-syntax-tree.dot', 'symbol-table.dot')


if __name__ == "__main__":
    main()
