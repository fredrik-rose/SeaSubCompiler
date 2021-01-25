# Sea Sub Compiler

A compiler for a small subset (sub) of the C (sea) programming language.

## Architecture

This section describes the architecture of the sea sub compiler.

### Lexer

The lexical analyzer (also known as scanner or tokenizer). This is the first step of the compiler that takes the raw
sea sub source code as input and outputs tokens (e.g. numbers, brackets, operators, etc.). It performs the first part
of the syntax check as it only accepts tokens that are part of the sea sub language.

### Error Handler

This component is responsible for the error handling and is used by all parts of the compiler.
