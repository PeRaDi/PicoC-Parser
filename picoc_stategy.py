import ply.yacc as yacc
from lex import tokens
from lex import literals
import zipper as zp
import strategy as st
from adt import adt, Case


@adt
class PicoC:
    INST: Case["Inst"]

    def __repr__(self):
        return  str(self)

    def __str__(self):
        return self.match(
            inst=lambda i: "INST (" + str(i) + ")"
        )


@adt
class Inst:
    ATRIB: Case[str, "Exp"]
    # WHILE: Case["Exp", "Inst"]
    # ITE: Case["Exp", "Inst", "Inst"]
    # NUMBER: Case["Number"]
    EMPTY: Case

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            #atrib=lambda s, e: s + " = " + str(e),
            atrib=lambda s, e: "ATRIB (" + s + ", " + str(e) + ")",
            empty=lambda: ""
        )

@adt
class Exp:
    ADD: Case["Exp", "Exp"]
    SUB: Case["Exp", "Exp"]
    MUL: Case["Exp", "Exp"]
    DIV: Case["Exp", "Exp"]
    NEG: Case["Exp"]
    VAR: Case[str]
    CONST: Case[int]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            # add=lambda x, y: str(x) + " + " + str(y),
            # sub=lambda x, y: str(x) + " - " + str(y),
            # mul=lambda x, y: str(x) + " * " + str(y),
            # div=lambda x, y:  str(x) + " / " + str(y),
            add=lambda x, y: "ADD (" + str(x) + ", " + str(y) + ")",
            sub=lambda x, y: "SUB (" + str(x) + ", " + str(y) + ")",
            mul=lambda x, y: "MUL (" + str(x) + ", " + str(y) + ")",
            div=lambda x, y: "DIV (" + str(x) + ", " + str(y) + ")",
            neg=lambda x: "NEG (" + str(x) + ")",
            var=lambda x: "VAR (" + x + ")",
            const=lambda x: "CONS (" + str(x) + ")",
        )


def p_error(p):
    print("Syntax error in input!")

def p_Rec0(p) :
    "Rec : PicoC"
    p[0] = [p[1]]

def p_Rec1(p) :
    "Rec : Rec PicoC"
    p[0] = p[1]
    p[0].append(p[2])

def p_PicoC(p):
    "PicoC : Instrucao"
    p[0] = PicoC.INST(p[1])

# def p_Rec0(p) :
#     "Rec : Instrucao"
#     p[0] = [p[1]]
#
# def p_Rec1(p) :
#     "Rec : Rec Instrucao"
#     p[0] = p[1]
#     p[0].append(p[2])
#
def p_Instrucao(p) :
    """Instrucao : atrib
                | nr
    """
    p[0] = p[1]

def p_atrib(p):
    """atrib : int var ';'
             | string var ';'
             | int var '=' exp ';'
             | string var '=' str ';'"""
    if len(p) == 4:
        p[0] = Inst.ATRIB(p[2])
    else:
        p[0] = Inst.ATRIB(p[2], p[4])

def p_exp_var(p):
    """exp : var"""
    p[0] = Exp.VAR(p[1])

def p_exp_const(p):
    """exp : nr"""
    p[0] = Exp.CONST(p[1])

def p_exp_binary_operation(p):
    """exp : exp '+' exp
           | exp '-' exp
           | exp '*' exp
           | exp '/' exp
    """
    if p[2] == '+':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = Exp.ADD(p[1], p[3])
    elif p[2] == '-':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = Exp.SUB(p[1], p[3])
    elif p[2] == '*':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = Exp.MUL(p[1], p[3])
    elif p[2] == '/':
        # print(str(p[1]) + " '" + p[2] + "' " + str(p[3]))
        p[0] = Exp.DIV(p[1], p[3])

def p_exp_unary_minus(p):
    """exp : '-' exp %prec UMINUS
    """
    p[0] = Exp.NEG(p[2])

def p_exp_group(p):
    """exp : '(' exp ')'
    """
    p[0] = p[2]

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

def main():
    #p = PicoC.INST(Inst.ATRIB("x", Exp.VAR("b")))
    #print(p)
    data = """
        int x = 3 * 4 + 5;
        int y = 3 + 4 * -5;
    """
    ast = parser.parse(data)
    print(ast)

if __name__ == "__main__":
    main()
