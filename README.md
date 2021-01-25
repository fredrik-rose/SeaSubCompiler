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
program ->
    additive_expression EOF

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
    NUMBER |
    '(' additive_expression ')'
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

### Error Handler

This component is responsible for the error handling and is used by all parts of the compiler.
