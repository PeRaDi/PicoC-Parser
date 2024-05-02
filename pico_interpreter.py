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


data = """
    int x = 0;
    int z = 10;
    
    while ( x < z) then
        x = x + 3;
    end
    
    return x;
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
    # print("get_var_value")
    return args.get(var_name)

def eval_exp(exp: pa.Exp, args: dict[str, int] = {}):
    # print("eval_exp")
    # print(exp)
    # print("eval_exp_")
    val = exp.match(
        add=lambda x, y: eval_exp(x, args) + eval_exp(y, args),
        sub=lambda x, y: eval_exp(x, args) - eval_exp(y, args),
        mul=lambda x, y: eval_exp(x, args) * eval_exp(y, args),
        div=lambda x, y: eval_exp(x, args) / eval_exp(y, args),
        neg=lambda x: -eval_exp(x, args),
        group=lambda x: eval_exp(x, args),
        bool=lambda x: x,
        var=lambda x: get_var_value(x, args),
        const=lambda x: x,
    )
    return val

def eval_atrib(type_name, var_name, exp: pa.Exp, args: dict[str, int] = {}):
    # print("eval_atrib")
    args[var_name] = eval_exp(exp, args)
    return args[var_name]

def eval_return(exp: pa.Exp, args: dict[str, int] = {}):
    # print("eval_return")
    args["return"] = eval_exp(exp, args)
    return args["return"]

def eval_cond(cond: pa.Cond, args: dict[str, int] = {}):
    val = cond.match(
        equal=lambda x, y: eval_exp(x, args) == eval_exp(y, args),
        not_equal=lambda x, y: eval_exp(x, args) != eval_exp(y, args),
        greater=lambda x, y: eval_exp(x, args) > eval_exp(y, args),
        greater_equal=lambda x, y: eval_exp(x, args) >= eval_exp(y, args),
        less=lambda x, y: eval_exp(x, args) < eval_exp(y, args),
        less_equal=lambda x, y: eval_exp(x, args) <= eval_exp(y, args),
    )
    return val

def eval_while(cond: pa.Cond, inst: pa.Inst, args: dict[str, int] = {}):
    print("eval_while")
    print(cond)
    print(inst)
    print(args)
    print("eval_while_")

    while eval_cond(cond, args):
        eval_inst(inst, args)

def eval_ite(condition: pa.Exp, b1: pa.Bloco, b2: pa.Bloco, args: dict[str, int] = {}):
    # if evaluate_exp(condition, args):
        # eva
    print(condition)
    print(b1)
    print(b2)

def eval_inst(inst: pa.Inst, args: dict[str, int] = {}):
    val = inst.match(
        decl=lambda t, s: None,
        atrib=lambda t, s, e: eval_atrib(t, s, e, args),
        while_loop=lambda e, b: eval_while(e, b, args),
        ite=lambda e, b1, b2: eval_ite(e, b1, b2, args),
        returns=lambda e: eval_return(e, args),
        empty=lambda: None
    )
    return val


def evaluate_ast(ast: list[pa.Inst], args: dict[str, int] = {}):
    if ast == None:
        return None

    for a in ast:
        eval_inst(a, args)

    return args.get("return")

vars = {}

ast = p.parse(data)

result = evaluate_ast(ast, vars)

print(vars)
print(result)