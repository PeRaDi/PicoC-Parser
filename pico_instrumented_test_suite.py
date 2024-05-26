import pico_evaluate as pe
from pico_adt import instrumentation
import pico_parser as parser

def instrumented_evaluate(ast, args):
    from collections import defaultdict
    executed_instructions = defaultdict(int)

    def instrumented_eval_inst(inst, args):
        executed_instructions[str(inst)] += 1
        return eval_inst(inst, args)

    def eval_inst(inst, args):
        val = inst.match(
            decl=lambda t, s: None,
            atrib=lambda t, s, e: pe.eval_atrib(t, s, e, args),
            while_loop=lambda e, b: instrumented_eval_while(e, b, args),
            ite=lambda e, b1, b2: instrumented_eval_ite(e, b1, b2, args),
            returns=lambda e: pe.eval_return(e, args),
            empty=lambda: None,
            print=lambda s: print(s[1:len(s) - 1].replace("\\n", "\n"))
        )
        return val

    def instrumented_eval_while(cond, bloco, args):
        while pe.eval_cond(cond, args):
            for inst in bloco.insts():
                instrumented_eval_inst(inst, args)

    def instrumented_eval_ite(cond, b1, b2, args):
        if pe.eval_cond(cond, args):
            for inst in b1.insts():
                instrumented_eval_inst(inst, args)
        else:
            for inst in b2.insts():
                instrumented_eval_inst(inst, args)

    if ast is None:
        return None

    for i in ast.insts():
        instrumented_eval_inst(i, args)

    return args.get("return"), executed_instructions

def instrumentedTestSuite(program, test_suite):
    instrumented_program = instrumentation(program)
    all_tests_pass = True
    for inputs, expected in test_suite:
        result, executed_instructions = instrumented_evaluate(instrumented_program, inputs)
        if result != expected:
            all_tests_pass = False
        print("Executed Instructions:")
        for inst, count in executed_instructions.items():
            print(f"{inst}: {count} time(s)")
    return all_tests_pass

# Example usage
if __name__ == "__main__":
    # Define um programa PicoC e sua suíte de testes
    data = """
        int x = 1;
        int z = 10;
        int count = 0;
        
        while ( x <= z) then
            x = x + 1;
            count = count + 1;
        end
    
        return count;
    """
    program = parser.parse(data)
    test_suite = [({}, 10)]  # Suíte de testes exemplo com entradas e resultado esperado
    
    # Executa a suíte de testes instrumentada
    all_tests_pass = instrumentedTestSuite(program, test_suite)
    print(f"All tests pass: {all_tests_pass}")
