"""
The sea sub compiler.
"""
from seasub import interpreter
from seasub import parser


def run():
    statements = '''
    {
        a = -3 +
        -(4 + +-9)
        * 5;

        ;;

        b = -3 + -(4 + +-9);

        {
            c = 5 + 6 - 7;
        }

        {

        }

        int a = 1 + 2;
    }
    '''
    print(f"Statements: {statements}")
    tree = parser.parse(statements)
    print(f"Parse tree:\n{repr(tree)}\n")
    print(f"Statement(s):\n{tree}\n")
    result = interpreter.Intepreter().visit(tree)
    print(f"Result: {result}")
