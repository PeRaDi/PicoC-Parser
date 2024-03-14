from ply import lex, yacc

literals = ['+', '-', '*', '/', '(', ')', '{', '}', ';', '=', '>', '<', '!', '"']

tokens = ['nr', 'string', 'str', 'if', 'else', 'while', 'var', 'int', 'then', 'end', 'isEqual', 'isNotEqual', 'isEqualOrGreater', 'isEqualOrLess']

def t_int(t):
    r"int"
    return t

def t_string(t):
    r"string"
    return t

def t_if(t):
    r"if"
    return t

def t_else(t):
    r"else"
    return t

def t_while(t):
    r"while"
    return t

def t_then(t):
    r"then"
    return t

def t_end(t):
    r"end"
    return t

def t_var(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    return t

def t_nr(t):
    r"[0-9]+(\.[0-9]+)?"
    t.value = int(t.value)
    return t

def t_str(t):
    r'"[^"]*"'
    return t

def t_isEqual(t):
    r"=="
    return t

def t_isNotEqual(t):
    r"!="
    return t

def t_isEqualOrGreater(t):
    r">="
    return t

def t_isEqualOrLess(t):
    r"<="
    return t


def t_error(t):
    print("Error: " + str(t))
    t.lexer.skip(1)

t_ignore = " \t\n"

lexer = lex.lex()

# int x = 0;

# if (x == 0) {
#     x = 1+1;
# } else {
#     x = 2;
# }

# while(x == 2) {
#     x = 3;
# }
    