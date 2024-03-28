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
                 | whileLoop
                 | atrib
                 | nr"""
    p[0] = p[1]

def p_atrib(p):
    """atrib : int var ';'
             | string var ';'
             | int var '=' exp ';'
             | string var '=' str ';'"""
    if len(p) == 4:
        p[0] = 'Atrib "' + p[2] + '"'
    else:
        p[0] = 'Atrib "' + p[2] + '" (Const ' + str(p[4]) + ')'

def p_error(p):
    print("Syntax error in input!")

def p_ifStatment(p):
    """ ifStatment : if '(' cond ')' then Instrucao end
                   | if '(' cond ')' then Instrucao else Instrucao end
    """
    if len(p) == 8:
        p[0] = 'If (' + p[3] + ') then ' + p[6] + ' end'
    else:
        p[0] = 'If (' + p[3] + ') then ' + p[6] + ' else ' + p[8] + ' end'

def p_cond(p):
    """ cond : exp '>' exp
             | exp '<' exp
             | exp isEqual exp
             | exp isNotEqual exp
             | exp isEqualOrGreater exp
             | exp isEqualOrLess exp
             | exp
    """
    if (p[2] == '>'):
        p[0] = str(p[1]) + ' isGreaterThan ' + str(p[3])
    elif (p[2] == '<'):
        p[0] = str(p[1]) + ' isLessThan ' + str(p[3])
    elif (p[2] == '=='):
        p[0] = str(p[1]) + ' isEqual ' + str(p[3])
    elif (p[2] == '!='):
        p[0] = str(p[1]) + ' isNotEqual ' + str(p[3])
    elif (p[2] == '>='):
        p[0] = str(p[1]) + ' isEqualOrGreater ' + str(p[3])
    elif (p[2] == '<='):
        p[0] = str(p[1]) + ' isEqualOrLess ' + str(p[3])

def p_exp(p):
    """exp : exp '+' exp
           | exp '-' exp
           | exp '*' exp
           | exp '/' exp
           | '(' exp ')'
           | '-' exp %prec UMINUS
           | nr
           | var
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = -p[2]
    elif p[1] == '(':
        p[0] = str(p[2])
    else:
        p[0] = eval(str(p[1]) + p[2] + str(p[3]))

def p_whileLoop(p):
    """whileLoop : while '(' cond ')' then Instrucao end"""
    p[0] = 'While (' + p[3] + ') then ' + p[6] + ' end'

# https://www.dabeaz.com/ply/ply.html#ply_nn1
# his declaration specifies that PLUS/MINUS have the same precedence level and are left-associative
# and that TIMES/DIVIDE have the same precedence and are left-associative.
# Within the precedence declaration, tokens are ordered from lowest to highest precedence.
# Thus, this declaration specifies that TIMES/DIVIDE have higher precedence than PLUS/MINUS
# (since they appear later in the precedence specification).
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),            # Unary minus operator
)

parser = yacc.yacc()

data = """ 
    int x = 3 * 4 + 5;
    int y = 3 + 4 * -5;
    
    if(1 == 0) then 
        int x = 1 + 1;
    else 
        int x = 2;
    end

    if(x > (2+2*2)) then
        int a = 1;
    else
        int b = 2;
    end

    while(x > 2) then
        int c = 3;
    end
"""

result = parser.parse(data)
print(result)
