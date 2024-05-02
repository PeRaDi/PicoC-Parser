import pico_parser as p
import pico_adt as pa

commands = {

}

data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 2;
        z = 1;
        
        int ans = x + y * z;
        
        return ans;
    """

# data = """
#         int x = 3 * 4 + 5;
#         int y = 3 + 4 * 5;
#         int z = 2;
#
#         if (z <= (x + y)) then
#             z = (x + y) * 2;
#         end
#
#         return z;
#     """

def get_var_value(var_name: str, args: dict[str, int] = {}):
    return args.get(var_name)

def evaluate_exp(exp: pa.Exp, args: dict[str, int] = {}):
    val = exp.match(
        add=lambda x, y: evaluate_exp(x, args) + evaluate_exp(y, args),
        sub=lambda x, y: evaluate_exp(x, args) - evaluate_exp(y, args),
        mul=lambda x, y: evaluate_exp(x, args) * evaluate_exp(y, args),
        div=lambda x, y: evaluate_exp(x, args) / evaluate_exp(y, args),
        neg=lambda x: -evaluate_exp(x, args),
        group=lambda x: x,
        bool=lambda x: x,
        var=lambda x: get_var_value(x, args),
        const=lambda x: x,
    )
    return val

def eval_atrib(type_name, var_name, exp: pa.Exp, args: dict[str, int] = {}):
    args[var_name] = evaluate_exp(exp, args)
    return args[var_name]

def eval_return(exp: pa.Exp, args: dict[str, int] = {}):
    args["return"] = evaluate_exp(exp, args)
    return args["return"]

def eval_while(exp: pa.Exp, block: pa.Bloco, args: dict[str, int] = {}):
    pass

def eval_ite(condition: pa.Exp, b1: pa.Bloco, b2: pa.Bloco, args: dict[str, int] = {}):
    # if evaluate_exp(condition, args):
        # eva
    print(condition)
    print(b1)
    print(b2)

def evaluate_inst(inst: pa.Inst, args: dict[str, int] = {}):
    val = inst.match(
        decl=lambda t, s: None,
        atrib=lambda t, s, e: eval_atrib(t, s, e, args),
        while_loop=lambda e, b: None,
        ite=lambda e, b1, b2: eval_ite(e, b1, b2, args),
        returns=lambda e: eval_return(e, args),
        empty=lambda: None
    )
    return val


def evaluate_ast(ast: list[pa.Inst], args: dict[str, int] = {}):
    if ast == None:
        return None

    for a in ast:
        evaluate_inst(a, args)

    return args["return"]

vars = {}
ast = p.parse(data)

result = evaluate_ast(ast, vars)

print(vars)
print(result)