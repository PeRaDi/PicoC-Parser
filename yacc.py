import ply.yacc as yacc
from lex import tokens
from lex import literals

def p_Rec0(p) :
    "Rec : Instrucao"
    p[0] = [p[1]]

def p_Rec1(p) :
    "Rec : Rec Instrucao"
    p[0] = p[1]
    p[0].append(p[2])

def p_Instrucao(p) :
    """Instrucao : ifStatment
                 | while
                 | atrib
                 | nr"""
    p[0] = p[1]

def p_atrib(p):
    """atrib : int var ';'
             | string var ';'
             | int var '=' nr ';'
             | string var '=' str ';'"""
    if len(p) == 4:
        p[0] = 'Atrib "' + p[2] + '"'
    else:
        p[0] = 'Atrib "' + p[2] + '" (Const ' + str(p[4]) + ')'

def p_error(p):
    print("Syntax error in input!")

def p_ifStatment(p):
    "ifStatment : if '(' cond ')' then Instrucao end"
    p[0] = 'If (' + p[3] + ') then ' + p[6] + ' end'

def p_cond(p):
    """ cond : exp '>' exp
             | exp '<' exp
             | exp '==' exp
             | exp '!=' exp
             | exp '>=' exp
             | exp '<=' exp
             | exp
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ' ' + p[2] + ' ' + p[3]

def p_exp(p):
    """exp : exp '+' exp
           | exp '-' exp
           | exp '*' exp
           | exp '/' exp
           | '(' exp ')'
           | nr
           | var
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = '(' + p[2] + ')'
    else:
        p[0] = p[1] + ' ' + p[2] + ' ' + p[3]


parser = yacc.yacc()

data = """
if(x > 0) then
    x = 1+1;
end
"""
result = parser.parse(data)
print(result)
