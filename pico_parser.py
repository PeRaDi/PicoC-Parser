import ply.yacc as yacc
from lex import tokens
from lex import literals

import pico_adt as pa

def p_error(p):
    print("Syntax error in input!")


def p_Rec0(p):
    "Rec : PicoC"
    p[0] = [p[1]]


def p_Rec1(p):
    "Rec : Rec PicoC"
    p[0] = p[1]
    p[0].append(p[2])


def p_PicoC(p):
    "PicoC : Instrucao"
    p[0] = pa.PicoC.INST(p[1])


# def p_Rec0(p) :
#     "Rec : Instrucao"
#     p[0] = [p[1]]
#
# def p_Rec1(p) :
#     "Rec : Rec Instrucao"
#     p[0] = p[1]
#     p[0].append(p[2])
#
def p_Instrucao(p):
    """Instrucao : ifStatement
                | whileLoop
                | atrib
                | nr
    """
    p[0] = p[1]


def p_atrib(p):
    """atrib : int var ';'
             | string var ';'
             | int var '=' exp ';'
             | string var '=' str ';'"""
    if len(p) == 4:
        p[0] = pa.Inst.ATRIB(p[2])
    else:
        p[0] = pa.Inst.ATRIB(p[2], p[4])


def p_exp_var(p):
    """exp : var"""
    p[0] = pa.Exp.VAR(p[1])


def p_exp_const(p):
    """exp : nr"""
    p[0] = pa.Exp.CONST(p[1])


def p_exp_binary_operation(p):
    """exp : exp '+' exp
           | exp '-' exp
           | exp '*' exp
           | exp '/' exp
    """
    if p[2] == '+':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = pa.Exp.ADD(p[1], p[3])
    elif p[2] == '-':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = pa.Exp.SUB(p[1], p[3])
    elif p[2] == '*':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = pa.Exp.MUL(p[1], p[3])
    elif p[2] == '/':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = pa.Exp.DIV(p[1], p[3])


def p_exp_unary_minus(p):
    """exp : '-' exp %prec UMINUS
    """
    p[0] = pa.Exp.NEG(p[2])


def p_exp_group(p):
    """exp : '(' exp ')'
    """
    p[0] = p[2]


def p_ifThen(p):
    """ifStatement : if '(' cond ')' then Instrucao end
    """
    p[0] = pa.Inst.ITE(p[3], p[6], pa.Inst.EMPTY())


def p_ifThenElse(p):
    """ifStatement : if '(' cond ')' then Instrucao else Instrucao end
    """
    p[0] = pa.Inst.ITE(p[3], p[6], p[8])


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
        p[0] = pa.Cond.GREATER(p[1], p[3])
    elif (p[2] == '<'):
        p[0] = pa.Cond.LESS(p[1], p[3])
    elif (p[2] == '=='):
        p[0] = pa.Cond.EQUAL(p[1], p[3])
    elif (p[2] == '!='):
        p[0] = pa.Cond.NOT_EQUAL(p[1], p[3])
    elif (p[2] == '>='):
        p[0] = pa.Cond.GREATER_EQUAL(p[1], p[3])
    elif (p[2] == '<='):
        p[0] = pa.Cond.LESS_EQUAL(p[1], p[3])

def p_whileLoop(p):
    """whileLoop : while '(' cond ')' then Instrucao end"""
    p[0] = pa.Inst.WHILE_LOOP(p[3], p[6])

# https://www.dabeaz.com/ply/ply.html#ply_nn1
# his declaration specifies that PLUS/MINUS have the same precedence level and are left-associative
# and that TIMES/DIVIDE have the same precedence and are left-associative.
# Within the precedence declaration, tokens are ordered from lowest to highest precedence.
# Thus, this declaration specifies that TIMES/DIVIDE have higher precedence than PLUS/MINUS
# (since they appear later in the precedence specification).
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),  # Unary minus operator
)

def parse(data):
    parser = yacc.yacc()
    ast = parser.parse(data)
    return ast


