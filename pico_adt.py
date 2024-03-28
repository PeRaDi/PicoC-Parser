
from adt import adt, Case

@adt
class PicoC:
    INST: Case["Inst"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            inst=lambda i: "INST (" + str(i) + ")"
            #inst=lambda i: str(i)
        )


@adt
class Bloco:
    INST: Case["Inst"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            inst=lambda i: "INST (" + str(i) + ")"
            #inst=lambda i: str(i)
        )


@adt
class Inst:
    ATRIB: Case[str, "Exp"]
    WHILE_LOOP: Case["Exp", "Bloco"]
    ITE: Case["Exp", "Bloco", "Bloco"]
    EMPTY: Case

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            atrib=lambda s, e: "ATRIB (" + s + ", " + str(e) + ")",
            while_loop=lambda e, b: "WHILE (" + str(e) + ", " + str(b) + ")",
            ite=lambda e, b1, b2: "ITE (" + str(e) + ", " + str(b1) + ", " + str(b2) + ")",
            empty=lambda: "EMPTY"
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
            add=lambda x, y: "ADD (" + str(x) + ", " + str(y) + ")",
            sub=lambda x, y: "SUB (" + str(x) + ", " + str(y) + ")",
            mul=lambda x, y: "MUL (" + str(x) + ", " + str(y) + ")",
            div=lambda x, y: "DIV (" + str(x) + ", " + str(y) + ")",
            neg=lambda x: "NEG (" + str(x) + ")",
            var=lambda x: "VAR (" + x + ")",
            const=lambda x: "CONS (" + str(x) + ")",
        )


@adt
class Cond:
    EQUAL: Case["Exp", "Exp"]
    NOT_EQUAL: Case["Exp", "Exp"]
    GREATER: Case["Exp", "Exp"]
    GREATER_EQUAL: Case["Exp", "Exp"]
    LESS: Case["Exp", "Exp"]
    LESS_EQUAL: Case["Exp", "Exp"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            equal=lambda x, y: "EQUAL (" + str(x) + ", " + str(y) + ")",
            not_equal=lambda x, y: "NOT_EQUAL (" + str(x) + ", " + str(y) + ")",
            greater=lambda x, y: "GREATER (" + str(x) + ", " + str(y) + ")",
            greater_equal=lambda x, y: "GREATER_EQUAL (" + str(x) + ", " + str(y) + ")",
            less=lambda x, y: "LESS (" + str(x) + ", " + str(y) + ")",
            less_equal=lambda x, y: "LESS_EQUAL (" + str(x) + ", " + str(y) + ")",
        )

