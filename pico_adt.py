from adt import adt, Case

pretty_print = False


@adt
class PicoC:
    INST: Case["Inst"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            inst=lambda i: str(i) if pretty_print else "INST (" + str(i) + ")"
        )


@adt
class Bloco:
    INST: Case["Inst"]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            inst=lambda i: str(i) if pretty_print else "INST (" + str(i) + ")"
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
            atrib=lambda s, e: s + ' = ' + str(e) if pretty_print else "ATRIB (" + s + ", " + str(e) + ")",
            while_loop=lambda e, b: 'while (' + str(e) + ') { ' + str(b) + ' }' if pretty_print else "WHILE (" + str(e) + ", " + str(b) + ")",
            ite=lambda e, b1, b2:  'if (' + str(e) + ') { ' + str(b1) + ' } else { ' + str(b2) + ' }' if pretty_print else "ITE (" + str(e) + ", " + str(b1) + ", " + str(b2) + ")",
            empty=lambda: "" if pretty_print else "EMPTY"
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
            add=lambda x, y: str(x) + ' + ' + str(y) if pretty_print else "ADD (" + str(x) + ", " + str(y) + ")",
            sub=lambda x, y: str(x) + ' - ' + str(y) if pretty_print else "SUB (" + str(x) + ", " + str(y) + ")",
            mul=lambda x, y: str(x) + ' * ' + str(y) if pretty_print else "MUL (" + str(x) + ", " + str(y) + ")",
            div=lambda x, y: str(x) + ' / ' + str(y) if pretty_print else "DIV (" + str(x) + ", " + str(y) + ")",
            neg=lambda x: '-' + str(x) if pretty_print else "NEG (" + str(x) + ")",
            var=lambda x: x if pretty_print else "VAR (" + x + ")",
            const=lambda x: str(x) if pretty_print else "CONS (" + str(x) + ")",
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
            equal=lambda x, y: str(x) + ' == ' + str(y) if pretty_print else "EQUAL (" + str(x) + ", " + str(y) + ")",
            not_equal=lambda x, y: str(x) + ' != ' + str(y) if pretty_print else "NOT_EQUAL (" + str(x) + ", " + str(y) + ")",
            greater=lambda x, y: str(x) + ' > ' + str(y) if pretty_print else "GREATER (" + str(x) + ", " + str(y) + ")",
            greater_equal=lambda x, y: str(x) + ' >= ' + str(y) if pretty_print else "GREATER_EQUAL (" + str(x) + ", " + str(y) + ")",
            less=lambda x, y: str(x) + ' < ' + str(y) if pretty_print else "LESS (" + str(x) + ", " + str(y) + ")",
            less_equal=lambda x, y: str(x) + ' <= ' + str(y) if pretty_print else "LESS_EQUAL (" + str(x) + ", " + str(y) + ")",
        )
