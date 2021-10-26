"""
The sea sub compiler.
"""
from seasub import interpreter
from seasub import lexer
from seasub import parser
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
    '''
    print(f"Statements: {statements}")
    token_stream = lexer.tokenize(statements)
    tree = parser.parse(token_stream)[0]  # TODO: Remove [0]
    print(f"Parse tree:\n{repr(tree)}\n")
    print(f"Statement(s):\n{tree}\n")
    interp = interpreter.Intepreter()
    interp.visit(tree)
    print(f"Result: {interp.environment}")
    symbol_table = st.attach_symbol_table(tree)
    print(symbol_table)
