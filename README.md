# Sea Sub Compiler

<img src="img/seasub.png" width="300"/>

A compiler for a small subset (sub) of the C (sea) programming language.

## Usage

Stand in the root if the SeaSubCompiler directory and run:
```
python main.py -o 1 --ast abstract-syntax-tree.dot --symbol-table symbol-table.dot demo.c
```

Currently only runs a toy example.

### Visualization

The Sea sub compiler can generate .dot graph files containing the abstract syntax tree and the symbol table. These can
be visualized by using e.g. Graphvis:
```
dot -Tpng -o abstract-syntax-tree.png abstract-syntax-tree.dot
dot -Tpng -o symbol-table.png symbol-table.dot
```

## Grammar

This section defines the grammar of the sea sub language.

```
translation_unit ->
    function_definition_list EOF

function_definition_list ->
    function_definition |
    function_definition function_definition_list

function_definition ->
    type_specifier identifier '(' parameter_list ')' compound_statement

parameter_list ->
    parameter_declaration |
    parameter_declaration ',' parameter_list

parameter_declaration ->
    type_specifier identifier

compound_statement ->
    '{' '}' |
    '{' statement_list '}' |
    '{' declaration_list statement_list '}'

declaration_list ->
    declaration |
    declaration declaration_list

declaration ->
    type_specifier identifier ';'

statement_list ->
    statement |
    statement statement_list

statement ->
    compound_statement |
    expression_statement |
    jump_statement

jump_statement ->
    'return' expression ';'

expression_statement ->
    ';' |
    identifier '=' expression ';'

expression ->
    additive_expression

additive_expression ->
    multiplicative_expression |
    additive_expression '+' multiplicative_expression |
    additive_expression '-' multiplicative_expression
=> / remove left recursion / =>
additive_expression ->
    multiplicative_expression ('+'|'-' multiplicative_expression)*

multiplicative_expression ->
    unary_expression |
    multiplicative_expression '*' unary_expression |
    multiplicative_expression '/' unary_expression
=> / remove left recursion / =>
multiplicative_expression ->
    unary_expression ('*'|'/' unary_expression)*

unary_expression ->
    primary_expression |
    '+' unary_expression |
    '-' unary_expression

primary_expression ->
    constant |
    identifier |
    '(' expression ')'

type_specifier ->
    'int' |
    'double'

identifier ->
    IDENTIFIER

constant ->
    INTEGER_CONSTANT |
    DOUBLE_CONSTANT
```

## Architecture

This section describes the architecture of the sea sub compiler.

<img src="img/architecture.png" width="1000"/>

### Lexer

The lexical analyzer (also known as scanner or tokenizer). This is the first step of the compiler that takes the raw
sea sub source code as input and outputs tokens (e.g. numbers, brackets, operators, etc.). It performs the first part
of the syntax check as it only accepts tokens that are part of the sea sub language.

### Parser

The second step of the compiler takes tokens from the lexer as input and outputs an abstract syntax tree. It performs
the second part of the syntax check by verifying that the stream of tokens fulfills the grammar of the sea sub
language. It is this part of the compiler that implements the grammar as a recursive descent parser.

A core part of the compiler is the node visitor. It provides functionality to traverse an abstract syntax tree by
implementing the *visitor* design pattern. The sub classes of the node visitor provides a visitor function for
each relevant node in the abstract syntax tree. The default visitor will be used for nodes that do not have a visitor.
The Sea sub compiler uses the node visitor heavily, for example:

* Semantic analysis
* Symbol table creation
* Visualization

### Semantic Analyzer

The third step of the compiler verifies the semantic correctness of the program. The abstract syntax tree created by
the parser is the input and the output is a verified abstract syntax tree. The semantic verification includes type
correctness and declaration of variables before use.

### Optimizer

The fourth step of the compiler performs optimizations on the abstract syntax tree. The output is a modified abstract
syntax tree. Currently only constant folding is implemented. Optimization is probably the most important part of a
compiler and it can be performed in several of the compilation stages.

### Symbol Table

This component is responsible to manage all kinds of symbols in the language, for built-in types, variables and
functions. To support lexical scopes it is implemented as a tree data structure, were each node corresponds to a scope
level.

The symbol table is attached to the abstract syntax tree by adding a *symbol table* member to each of the node in the
abstract syntax tree, referring to the corresponding lexical scope in the symbol table.

### Error Handler

This component is responsible for the error handling and is used by all parts of the compiler.

