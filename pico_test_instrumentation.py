import pico_parser as parser
import pico_adt as pa

def instrumentation(program):
    def instrument_instructions(instructions):
        instrumented_instructions = []
        for instr in instructions:
            instrumented_instructions.append(pa.Inst.PRINT(f"Executing: {instr.print()}"))
            instrumented_instructions.append(instr)
        return instrumented_instructions

    return program.match(
        insts=lambda instructions: pa.PicoC.INSTS(instrument_instructions(instructions))
    )

def test_instrumentation():
    data = """
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 2;
        z = 1;
        
        int ans = x + y * z;
        
        return ans;
    """
    
    ast = parser.parse(data)
    
    instrumented = instrumentation(ast)
    
    print(instrumented)

if __name__ == "__main__":
    test_instrumentation()
