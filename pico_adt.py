from adt import adt, Case
from typing import Any

# pretty_print = False
statement_end_symbol = ";"


def print_instructions(instructions: list[Any], pretty_print, separator: str) -> str:
    return separator.join(i.print(pretty_print) for i in instructions)

@adt
class PicoC:
    INSTS: Case[list["Inst"]]

    def __init__(self, pretty_print=True):
        self.pretty_print = pretty_print

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.print(self.pretty_print)

    def print(self, pretty_print=True):
        self.pretty_print = pretty_print
        return self.match(
            insts=lambda instructions: ("" if self.pretty_print else "PICOC (\n") + print_instructions(instructions, pretty_print, " ") + ("" if self.pretty_print else "\n)")
        )


@adt
class Bloco:
    INSTS: Case[list["Inst"]]

    def __init__(self, pretty_print=True):
        self.pretty_print = pretty_print

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.print(self.pretty_print)

    def print(self, pretty_print=True):
        self.pretty_print = pretty_print
        return self.match(
            insts=lambda instructions: ("" if self.pretty_print else "BLOCO (") + print_instructions(instructions, pretty_print, " ") + ("" if self.pretty_print else ")")
        )

@adt
class Inst:
    DECL: Case[str, str]
    ATRIB: Case[str, str, "Exp"]
    WHILE_LOOP: Case["Cond", "Bloco"]
    ITE: Case["Cond", "Bloco", "Bloco"]
    RETURNS: Case["Exp"]
    EMPTY: Case
    PRINT: Case[str]

    def __init__(self, pretty_print=True):
        self.pretty_print = pretty_print

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.print(self.pretty_print)

    def print(self, pretty_print=True):
        self.pretty_print = pretty_print
        return self.match(
            decl=lambda t, s: f"{t} {s}{statement_end_symbol}" if self.pretty_print else "DECL (" + t + ", " + s + ")",
            atrib=lambda t, s,
                         e: f"{t + ' ' if t else ''}{s} = {e.print(pretty_print)}{statement_end_symbol}" if self.pretty_print else "ATRIB (" + t + ", " + s + ", " + e.print(
                pretty_print) + ")",
            while_loop=lambda c,
                              b: f"while ({c.print(pretty_print)}) then {b.print(pretty_print)} end" if self.pretty_print else "WHILE (" + c.print(
                pretty_print) + ", " + b.print(pretty_print) + ")",
            ite=lambda c, b1,
                       b2: f"if ({c.print(pretty_print)}) then {b1.print(pretty_print)} {' else ' + b2.print(pretty_print) if b2 != Inst.EMPTY() else ''} end" if self.pretty_print else "ITE (" + c.print(
                pretty_print) + ", " + b1.print(pretty_print) + ", " + b2.print(pretty_print) + ")",
            returns=lambda
                e: f"return {e.print(pretty_print)}{statement_end_symbol}" if self.pretty_print else "RETURNS (" + e.print(
                pretty_print) + ")",
            empty=lambda: "" if self.pretty_print else "EMPTY",
            print=lambda x: f'print({x[1:len(x)-1]}){statement_end_symbol}' if self.pretty_print else "PRINT(" + x + ")"

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

    def __init__(self, pretty_print=True):
        self.pretty_print = pretty_print

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.print(self.pretty_print)

    def print(self, pretty_print=True):
        self.pretty_print = pretty_print
        return self.match(
            add=lambda x, y: x.print(pretty_print) + ' + ' + y.print(
                pretty_print) if self.pretty_print else "ADD (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            sub=lambda x, y: x.print(pretty_print) + ' - ' + y.print(
                pretty_print) if self.pretty_print else "SUB (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            mul=lambda x, y: x.print(pretty_print) + ' * ' + y.print(
                pretty_print) if self.pretty_print else "MUL (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            div=lambda x, y: x.print(pretty_print) + ' / ' + y.print(
                pretty_print) if self.pretty_print else "DIV (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            neg=lambda x: '-' + x.print(pretty_print) if self.pretty_print else "NEG (" + x.print(pretty_print) + ")",
            group=lambda e: f"({e.print(pretty_print)})" if self.pretty_print else "GROUP (" + e.print(
                pretty_print) + ")",
            var=lambda x: x if self.pretty_print else "VAR (" + x + ")",
            const=lambda x: str(x) if self.pretty_print else "CONS (" + str(x) + ")",
            bool=lambda x: str(x) if self.pretty_print else "BOOL (" + str(x) + ")"
        )


@adt
class Cond:
    EQUAL: Case["Exp", "Exp"]
    NOT_EQUAL: Case["Exp", "Exp"]
    GREATER: Case["Exp", "Exp"]
    GREATER_EQUAL: Case["Exp", "Exp"]
    LESS: Case["Exp", "Exp"]
    LESS_EQUAL: Case["Exp", "Exp"]

    def __init__(self, pretty_print=True):
        self.pretty_print = pretty_print

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.print(self.pretty_print)

    def print(self, pretty_print=True):
        self.pretty_print = pretty_print
        return self.match(
            equal=lambda x, y: x.print(pretty_print) + ' == ' + y.print(
                pretty_print) if self.pretty_print else "EQUAL (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            not_equal=lambda x, y: x.print(pretty_print) + ' != ' + y.print(
                pretty_print) if self.pretty_print else "NOT_EQUAL (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            greater=lambda x, y: x.print(pretty_print) + ' > ' + y.print(
                pretty_print) if self.pretty_print else "GREATER (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            greater_equal=lambda x, y: x.print(pretty_print) + ' >= ' + y.print(
                pretty_print) if self.pretty_print else "GREATER_EQUAL (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            less=lambda x, y: x.print(pretty_print) + ' < ' + y.print(
                pretty_print) if self.pretty_print else "LESS (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
            less_equal=lambda x, y: x.print(pretty_print) + ' <= ' + y.print(
                pretty_print) if self.pretty_print else "LESS_EQUAL (" + x.print(pretty_print) + ", " + y.print(
                pretty_print) + ")",
        )
    
def instrumentation(program):
    def instrument_instructions(instructions):
        instrumented_instructions = []
        for instr in instructions:
            instrumented_instructions.append(Inst.PRINT(f"Executing: {instr.print()}"))
            instrumented_instructions.append(instr)
        return instrumented_instructions

    return program.match(
        insts=lambda instructions: PicoC.INSTS(instrument_instructions(instructions))
    )


def picoc_to_code(ast: PicoC) -> str:
    return str(ast.print(True))
