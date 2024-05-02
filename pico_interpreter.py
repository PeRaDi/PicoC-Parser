import pico_parser as p
import pico_adt as pa

commands = {

}

data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * -5;
        int z = 0;
                
        int ans = x + y * z;
        
        return 3 + 4 * 5;
    """



def evaluate_inst(inst: pa.Inst, args = None):
    print(inst)
    if inst.is_attrib():
        print("Atrib")


def evaluate_ast(ast: list[pa.Inst], args = None):
    if ast == None:
        return None

    for a in ast:
        print("A")
        print(a)
        evaluate_inst(a, args)
        print("---A---")

    # if inst.is_attrib():
    #     print("Atrib")
    # elif type(inst) == list:
    #     for x in inst:
    #         if (type(x) == pa.Inst):
    #             print(x == pa.Inst.ATRIB())
    #             #v = evaluate(x, args)
    #             #args[symbol] = v
    #
    #         #evaluate(x, args)
    # else:
    #     raise Exception("Invalid command")

vars = {}
ast = p.parse(data)

evaluate_ast(ast, vars)