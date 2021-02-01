"""
The sea sub compiler.
"""
from seasub import interpreter
from seasub import parser


def run():
    statements = '''
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

        }

        d = 1 + 2;
    }
    '''
    print(f"Statements: {statements}")
    tree = parser.parse(statements)
    print(f"Parse tree:\n{repr(tree)}\n")
    print(f"Statement(s):\n{tree}\n")
    interp = interpreter.Intepreter()
    interp.visit(tree)
    print(f"Result: {interp.symbol_table}")
