# Simple-Pascal-Interpreter
This is a simple pascal interpreter built with python to translate 
a source program of some high-levl program into another form.

calc1.py:
    2 classes, Token and Interpreter
    Token:
    - Type
    - Value

    Interpreter:
    - text
    - pos
    - current_token
    Breaks down an input into either integer, plus, or EOF tokens.
    Uses the created tokens to evaluate an expression based on the operation token
    which is only addition for now.

calc2.py:
    calc2 buils on calc1 by adding functionaly for subtract and whitespace handling.
    Token:
    - Type
    - Value

    Interpreter:
    - text
    - pos
    - current_token
    - current_char