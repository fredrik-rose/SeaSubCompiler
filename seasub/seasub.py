"""
The sea sub compiler.
"""
from seasub import abstract_syntax_tree as ast
from seasub import interpreter
from seasub import lexer
from seasub import parser
from seasub import semantic_analyzer as sa
from seasub import symbol_table as st

def run():
    statements = '''
    int main(int x)
    {
        int a;
        int b;
        int d;

        a = -3 +
        -(4 + +-9)
        * 5;

        ;;

        b = -3 + -(4 + +-9);

        {
            int c;

            c = b + 6 - 7;
        }

        {
            int e;

            e = 8;

            return 10;
        }

        {

        }

        d = 1 + 2;

        return d + 11;
    }

    double add(double a, double b)
    {
        double z;

        z = a + b;

        return z;
    }
    '''
    print(f"Statements: {statements}")
    token_stream = lexer.tokenize(statements)
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
