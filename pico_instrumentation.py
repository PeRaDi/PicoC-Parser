from typing import Callable

import pico_adt as pa
import pico_evaluate as pe
import pico_parser as p


def instrumentation(ast: pa.PicoC, trace: Callable[[int, pa.Inst], None]) -> pa.PicoC:
    def instrument_inst(inst: pa.Inst, inst_id: int) -> pa.Inst:
        # print(f"INST: {inst}")
        return inst.match(
            decl=lambda t, s: [
                pa.Inst.DECL(t, s),
                # pa.Inst.PRINT(f'Instruction {inst_id}: Declare {t} {s}'),
                pa.Inst.INSTRUMENT(inst_id, pa.Inst.DECL(t, s), trace)
            ],
            atrib=lambda t, s, e: [
                pa.Inst.ATRIB(t, s, e),
                # pa.Inst.PRINT(f'Instruction {inst_id}: Assign {t} {s} = {e}'),
                pa.Inst.INSTRUMENT(inst_id, pa.Inst.ATRIB(t, s, e), trace)
                # pa.Inst.PRINT(f'Variable {s} assigned value: {{eval_exp(e, args)}}')
            ],
            while_loop=lambda c, b: [
                # pa.Inst.PRINT(f'Entering while with condition: {{eval_cond(c, args)}}'),
                # pa.Inst.PRINT(f'Instruction {inst_id}: Entering while with condition {c}'),
                pa.Inst.INSTRUMENT(inst_id, f'Entering while with condition {c}', trace),
                pa.Inst.WHILE_LOOP(c, instrument_bloco(b, inst_id)),
                # pa.Inst.PRINT(f'Exiting while with condition: {{eval_cond(c, args)}}')
                # pa.Inst.PRINT(f'Instruction {inst_id}: Exiting while with condition {c}')
                # pa.Inst.PRINT(inst_id, f'Exited while with condition {c}', trace)
            ],
            ite=lambda c, b1, b2: instrument_ite(inst_id, c, b1, b2),
            returns=lambda e: [
                # pa.Inst.PRINT(f'Returning value: {{eval_exp(e, args)}}'),
                # pa.Inst.PRINT(f'Instruction {inst_id}: Returning value {e}'),
                pa.Inst.INSTRUMENT(inst_id, pa.Inst.RETURNS(e), trace),
                pa.Inst.RETURNS(e)
            ],
            empty=lambda: [pa.Inst.EMPTY()],
            print=lambda s: [pa.Inst.PRINT(s)],
            instrument=lambda id, f: [pa.Inst.INSTRUMENT(id, f)]
        )

    def instrument_ite(inst_id: int, c, b1, b2):
        return [
            # pa.Inst.PRINT(f'Entering if with condition: {{eval_cond(c, args)}}'),
            # pa.Inst.PRINT(f'Instruction {inst_id}: Entering if with condition {c}'),
            pa.Inst.INSTRUMENT(inst_id, f'Checkin if with condition {c}', trace),
            pa.Inst.ITE(c,
                        # instrument_bloco(b1, inst_id, pa.Inst.PRINT(f'Instruction {inst_id}: Entering If branch'), 0),
                        # instrument_bloco(b2, inst_id, pa.Inst.PRINT(f'Instruction {inst_id}: Entering Else branch'), 50)
                        instrument_bloco(b1, inst_id, pa.Inst.INSTRUMENT(inst_id, f"Entering if branch of {c}", trace),0),
                        instrument_bloco(b2, inst_id, pa.Inst.INSTRUMENT(inst_id, f"Entering else branch of {c}", trace), 50),
                        # instrument_bloco(b1, inst_id, None,0),
                        # instrument_bloco(b2, inst_id, None, 50),
                        ),
            # pa.Inst.PRINT(f'Exiting if with condition: {{eval_cond(c, args)}}')
            # pa.Inst.PRINT(f'Instruction {inst_id}: Exiting if with condition {c}')
            # pa.Inst.INSTRUMENT(inst_id, f'Exited if with condition {c}', trace),
        ]

    def instrument_bloco(bloco: pa.Bloco, parent_id: int, log=None, offset=0) -> pa.Bloco:
        instrumented_insts = []
        if not log is None:
            instrumented_insts.append(log)
        for id, inst in enumerate(bloco.insts()):
            inst_id = parent_id * 100 + offset + id
            instrumented_insts = instrumented_insts + instrument_inst(inst, inst_id)
        return pa.Bloco.INSTS(instrumented_insts)

    def instrument_picoc(picoc: pa.PicoC) -> pa.PicoC:
        instrumented_insts = []
        for id, inst in enumerate(picoc.insts()):
            instrumented_insts = instrumented_insts + instrument_inst(inst, id)
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

    # data = """
    #     int x;
    #     int y;
    #     int z;
    #
    #     if (z <= y * x) then
    #         z = y * x;
    #     else
    #         z = (x * y) * 2;
    #     end
    #
    #     return z;
    # """
    # vars = { "x": 1, "y": 20, "z": 3}

    data = """
        int a;
        int b;
        int c;
        int m;
        
        if (a > b) then
            if (a > c) then
                m = a;
            else
                m = b;
            end
        else 
            if (b > c) then
                m = b;
            else
                m = c;
            end
        end
        
        return m;
    """
    vars = {"a": 1, "b": 2, "c": 3}

    ast = p.parse(data)
    print(f"AST: {ast}")
    execution_trace = []
    def trace(inst_id, inst):
        print(f"Instruction {inst_id}: {inst}")
        execution_trace.append(inst_id)

    instrumented_ast = instrumentation(ast, trace)
    print(f"INS: {instrumented_ast}")
    result = pe.evaluate(instrumented_ast, vars)
    print(vars)
    print(result)
    print(execution_trace)
