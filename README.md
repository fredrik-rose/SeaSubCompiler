# Sea Sub Compiler

A compiler for a small subset (sub) of the C (sea) programming language.

## Usage

Stand in the root if the SeaSubCompiler directory and run:
```
python main.py
```

Currently only runs a toy example.

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

### Lexer

The lexical analyzer (also known as scanner or tokenizer). This is the first step of the compiler that takes the raw
sea sub source code as input and outputs tokens (e.g. numbers, brackets, operators, etc.). It performs the first part
of the syntax check as it only accepts tokens that are part of the sea sub language.

### Parser

The second step of the compiler takes tokens from the lexer as input and outputs an abstract syntax tree. It performs
the second part of the syntax check by verifying that the stream of tokens fulfills the grammar of the sea sub
language. It is this part of the compiler that implements the grammar as a recursive descent parser.

### Semantic Analyzer
Verifies the semantic correctness of the program. This includes checking type correctness and that variables are
declared.

### Error Handler

This component is responsible for the error handling and is used by all parts of the compiler.

### Symbol Table

This component is responsible to manage all kinds of symbols in the language, for built-in types, variables and
functions.
