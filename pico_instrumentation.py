import pico_adt as pa
import pico_evaluate as pe
import pico_parser as p


def instrumentation(ast: pa.PicoC) -> pa.PicoC:
    def instrument_inst(inst: pa.Inst) -> pa.Inst:
        # print(f"INST: {inst}")
        return inst.match(
            decl=lambda t, s: [
                pa.Inst.DECL(t, s),
                pa.Inst.PRINT(f'Variable {t} {s} declared')
            ],
            atrib=lambda t, s, e: [
                pa.Inst.ATRIB(t, s, e),
                pa.Inst.PRINT(f'Variable {t} {s} assigned value {e}')
                # pa.Inst.PRINT(f'Variable {s} assigned value: {{eval_exp(e, args)}}')
            ],
            while_loop=lambda c, b: [
                # pa.Inst.PRINT(f'Entering while with condition: {{eval_cond(c, args)}}'),
                pa.Inst.PRINT(f'Entering while with condition {c}'),
                pa.Inst.WHILE_LOOP(
                    c,
                    instrument_bloco(b),
                ),
                # pa.Inst.PRINT(f'Exiting while with condition: {{eval_cond(c, args)}}')
                pa.Inst.PRINT(f'Exiting while with condition {c}')
            ],
            ite=lambda c, b1, b2: instrument_ite(c, b1, b2),
            returns=lambda e: [
                # pa.Inst.PRINT(f'Returning value: {{eval_exp(e, args)}}'),
                pa.Inst.PRINT(f'Returning value {e}'),
                pa.Inst.RETURNS(e)
            ],
            empty=lambda: [pa.Inst.EMPTY()],
            print=lambda s: [pa.Inst.PRINT(s)]
        )

    def instrument_ite(c, b1, b2):
        return [
            # pa.Inst.PRINT(f'Entering if with condition: {{eval_cond(c, args)}}'),
            pa.Inst.PRINT(f'Entering if with condition {c}'),
            pa.Inst.ITE(c, instrument_ite_b1(b1), instrument_ite_b2(b2)),
            # pa.Inst.PRINT(f'Exiting if with condition: {{eval_cond(c, args)}}')
            pa.Inst.PRINT(f'Exiting if with condition {c}')
        ]

    def instrument_ite_b1(b):
        instrumented_insts = [pa.Inst.PRINT(f'Entering If branch')]
        for inst in b.insts():
            for i in instrument_inst(inst):
                instrumented_insts.append(i)
        return pa.Bloco.INSTS(instrumented_insts)

    def instrument_ite_b2(b):
        instrumented_insts = [pa.Inst.PRINT(f'Entering Else branch')]
        for inst in b.insts():
            for i in instrument_inst(inst):
                instrumented_insts.append(i)
        return pa.Bloco.INSTS(instrumented_insts)

    def instrument_bloco(bloco: pa.Bloco) -> pa.Bloco:
        # instrumented_insts = [instrument_inst(inst) for inst in bloco.insts()]
        instrumented_insts = []
        for inst in bloco.insts():
            for i in instrument_inst(inst):
                instrumented_insts.append(i)
        return pa.Bloco.INSTS(instrumented_insts)

    def instrument_picoc(picoc: pa.PicoC) -> pa.PicoC:
        # instrumented_insts = [instrument_inst(inst) for inst in picoc.insts()]
        instrumented_insts = []
        for inst in picoc.insts():
            for i in instrument_inst(inst):
                instrumented_insts.append(i)
        return pa.PicoC.INSTS(instrumented_insts)

    return instrument_picoc(ast)


# Exemplo de uso:
if __name__ == "__main__":
    data = """
        int x;
        int y;
        int z;
        int ans = x + y * z;
        return ans;
    """
    vars = {"x": 1, "y": 2, "z": 3}

    data = """
        int x;
        int z;
        int count = 0;

        while ( x <= z) then
            x = x + 1;
            count = count + 1;
        end

        return count;
    """
    vars = {"x": 1, "z": 3}

    data = """
        int x;
        int y;
        int z;

        if (z <= y * x) then
            z = y * x;
        else
            z = (x * y) * 2;
        end

        return z;
    """
    vars = { "x": 1, "y": 20, "z": 3}

    ast = p.parse(data)
    print(f"AST: {ast}")
    instrumented_ast = instrumentation(ast)
    print(f"INS: {instrumented_ast}")
    result = pe.evaluate(instrumented_ast, vars)
    # print(vars)
    print(result)
