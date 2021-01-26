"""
The sea sub compiler.
"""
from seasub import interpreter
from seasub import parser


def run():
    statements = '''
    {
        -3 +
        -(4 + +-9)
        * 5;

        ;;

        -3 + -(4 + +-9);

        {
            5 + 6 - 7;
        }

        {

        }
    }
    '''
    print(f"Statements: {statements}")
    tree = parser.parse(statements)
    print(f"Parse tree:\n{repr(tree)}\n")
    print(f"Statement(s):\n{tree}\n")
    result = interpreter.Intepreter().visit(tree)
    print(f"Result: {result}")
