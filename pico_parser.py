import ply.yacc as yacc
from lex import tokens
from lex import literals

import pico_adt as pa

def p_Rec0(p):
    "Rec : PicoC"
    p[0] = p[1]

def p_PicoC(p):
    "PicoC : Instrucoes"
    p[0] = pa.PicoC.INSTS(p[1])

def p_Bloco(p):
    """Bloco : Instrucoes
    """
    p[0] = pa.Bloco.INSTS(p[1])

def p_Instrucoes(p):
    """Instrucoes : Instrucoes Instrucao
                  | Instrucao
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# def p_Rec0(p) :
#     "Rec : Instrucao"
#     p[0] = [p[1]]

# def p_Rec1(p) :
#     "Rec : Rec Instrucao"
#     p[0] = p[1]
#     p[0].append(p[2])

def p_Instrucao(p):
    """Instrucao : ifStatement
                 | whileLoop
                 | atrib
                 | nr
                 | returnStatement
                 | printStatement
    """
    p[0] = p[1]

def p_printStatement(p):
    """printStatement : print str ';'
    """
    p[0] = pa.Inst.PRINT(p[2])

def p_returnStatement(p):
    """returnStatement : return exp ';'
    """
    p[0] = pa.Inst.RETURNS(p[2])

def p_declare(p):
    """atrib : int var ';'
             | string var ';'
             | bool var ';'
     """
    p[0] = pa.Inst.DECL(p[1], p[2])

def p_declare_atrib(p):
    """atrib : int var '=' exp ';'
             | string var '=' str ';'
             | bool var '=' exp ';'
     """
    p[0] = pa.Inst.ATRIB(p[1], p[2], p[4])

def p_atrib(p):
    """atrib : var '=' exp ';' """
    p[0] = pa.Inst.ATRIB("", p[1], p[3])

def p_exp_var(p):
    """exp : var"""
    p[0] = pa.Exp.VAR(p[1])

def p_exp_const(p):
    """exp : nr"""
    p[0] = pa.Exp.CONST(p[1])

def p_exp_bool(p):
    """exp : true
            | false
    """
    p[0] = pa.Exp.BOOL(p[1] == "true")


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
    p[0] = pa.Exp.GROUP(p[2])


def p_ifThen(p):
    """ifStatement : if '(' cond ')' then Bloco end
    """
    p[0] = pa.Inst.ITE(p[3], p[6], pa.Inst.EMPTY())


def p_ifThenElse(p):
    """ifStatement : if '(' cond ')' then Bloco else Bloco end
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
    """whileLoop : while '(' cond ')' then Bloco end"""
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

def parse(data) -> pa.PicoC:
    parser = yacc.yacc()
    ast = parser.parse(data)
    return ast


if __name__ == '__main__':
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * -5;
        int z = 0;
        
        if(z <= (x + 2 * y)) then 
             z = (1 + 3) * y;
        end
        
        if (w == true) then
            x = y;
        else (w == false) then
            x = y;
        end        
        
        if(1 == 0) then 
            int x = 1 + 3;
        else 
            int x = 2;
        end
    
        if(x > (2+2*4)) then
            int a = 1;
        else
            int b = 2;
        end
    
        while(x > 2) then
            int c = 3;
        end
    """

    # data = """
    #     int x = 0;
    #     int y = 0;
    #     while ( x < 10) then
    #         x = x + 1;
    #         y = y + 1;
    #     end
    #     return x;
    # """

    data = """
        if(x == 1) then
            y = 2;
            w = x;
        else
            z = 3;
            w = 2;
        end
        return x;
    """
    data = """ 
        print "ola";
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 0;
        bool w = false;
        
        int ans = x + y * z;
        
        return 3 + 4 * 5;
    """

    ast = parse(data)
    print(ast)
    # print(ast.print())