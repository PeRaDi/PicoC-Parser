from adt import adt, Case

pretty_print = False
statement_end_symbol = ";"


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
    DECL: Case[str, str]
    ATRIB: Case[str, str, "Exp"]
    WHILE_LOOP: Case["Exp", "Bloco"]
    ITE: Case["Exp", "Bloco", "Bloco"]
    RETURNS: Case["Exp"]
    EMPTY: Case

    def __repr__(self):
        return str(self) if pretty_print else "INST (" + str(self) + ")"

    def __str__(self):
        return self.match(
            decl=lambda t, s: f"{t} {s}{statement_end_symbol}" if pretty_print else "DECL (" + t + ", " + s + ")",
            atrib=lambda t, s,
                         e: f"{t + ' ' if t else ''}{s} = {str(e)}{statement_end_symbol}" if pretty_print else "ATRIB (" + t + ", " + s + ", " + str(
                e) + ")",
            while_loop=lambda e, b: f"while ({str(e)}) then {str(b)} end" if pretty_print else "WHILE (" + str(
                e) + ", " + str(b) + ")",
            ite=lambda e, b1,
                       b2: f"if ({str(e)}) then {str(b1)} {' else ' + str(b2) if b2 != Inst.EMPTY() else ''} end" if pretty_print else "ITE (" + str(
                e) + ", " + str(b1) + ", " + str(b2) + ")",
            returns=lambda e: f"return {str(e)}{statement_end_symbol}" if pretty_print else "RETURNS (" + str(e) + ")",
            empty=lambda: "" if pretty_print else "EMPTY",
        )

    def is_attrib(self):
        return self.match(
            decl=lambda t, s: False,
            atrib=lambda t, s, e: True,
            while_loop=lambda e, b: False,
            ite=lambda e, b1, b2: False,
            returns=lambda e: False,
            empty=lambda: False
        )


@adt
class Exp:
    ADD: Case["Exp", "Exp"]
    SUB: Case["Exp", "Exp"]
    MUL: Case["Exp", "Exp"]
    DIV: Case["Exp", "Exp"]
    NEG: Case["Exp"]
    GROUP: Case["Exp"]
    VAR: Case[str]
    CONST: Case[int]
    BOOL: Case[bool]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.match(
            add=lambda x, y: str(x) + ' + ' + str(y) if pretty_print else "ADD (" + str(x) + ", " + str(y) + ")",
            sub=lambda x, y: str(x) + ' - ' + str(y) if pretty_print else "SUB (" + str(x) + ", " + str(y) + ")",
            mul=lambda x, y: str(x) + ' * ' + str(y) if pretty_print else "MUL (" + str(x) + ", " + str(y) + ")",
            div=lambda x, y: str(x) + ' / ' + str(y) if pretty_print else "DIV (" + str(x) + ", " + str(y) + ")",
            neg=lambda x: '-' + str(x) if pretty_print else "NEG (" + str(x) + ")",
            group=lambda e: f"({str(e)})" if pretty_print else "GROUP (" + str(e) + ")",
            var=lambda x: x if pretty_print else "VAR (" + x + ")",
            const=lambda x: str(x) if pretty_print else "CONS (" + str(x) + ")",
            bool=lambda x: str(x) if pretty_print else "BOOL (" + str(x) + ")"
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
            not_equal=lambda x, y: str(x) + ' != ' + str(y) if pretty_print else "NOT_EQUAL (" + str(x) + ", " + str(
                y) + ")",
            greater=lambda x, y: str(x) + ' > ' + str(y) if pretty_print else "GREATER (" + str(x) + ", " + str(
                y) + ")",
            greater_equal=lambda x, y: str(x) + ' >= ' + str(y) if pretty_print else "GREATER_EQUAL (" + str(
                x) + ", " + str(y) + ")",
            less=lambda x, y: str(x) + ' < ' + str(y) if pretty_print else "LESS (" + str(x) + ", " + str(y) + ")",
            less_equal=lambda x, y: str(x) + ' <= ' + str(y) if pretty_print else "LESS_EQUAL (" + str(x) + ", " + str(
                y) + ")",
        )


def picoc_to_code(ast: list[Inst]) -> str:
    return "\n".join(str(c) for c in ast if c)
