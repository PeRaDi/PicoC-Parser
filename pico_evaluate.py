import pico_parser as p
import pico_adt as pa


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
    # print(f"eval_cond: {cond}")
    val = cond.match(
        equal=lambda x, y: eval_exp(x, args) == eval_exp(y, args),
        not_equal=lambda x, y: eval_exp(x, args) != eval_exp(y, args),
        greater=lambda x, y: eval_exp(x, args) > eval_exp(y, args),
        greater_equal=lambda x, y: eval_exp(x, args) >= eval_exp(y, args),
        less=lambda x, y: eval_exp(x, args) < eval_exp(y, args),
        less_equal=lambda x, y: eval_exp(x, args) <= eval_exp(y, args),
    )
    # print(f"eval_cond result: {val}")
    return val


def eval_while(cond: pa.Cond, bloco: pa.Bloco, args: dict[str, int] = {}):
    while eval_cond(cond, args):
        eval_bloco(bloco, args)


def eval_ite(cond: pa.Exp, b1: pa.Bloco, b2: pa.Bloco, args: dict[str, int] = {}):
    if eval_cond(cond, args):
        eval_bloco(b1, args)
    else:
        eval_bloco(b2, args)


def eval_bloco(bloco: pa.Bloco, args: dict[str, int] = {}):
    if bloco == pa.Inst.EMPTY():
        return
    for i in bloco.insts():
        eval_inst(i, args)


def eval_inst(inst: pa.Inst, args: dict[str, int] = {}):
    # print(f"eval_inst: {inst}, type: {type(inst)}")
    val = inst.match(
        decl=lambda t, s: None,
        atrib=lambda t, s, e: eval_atrib(t, s, e, args),
        while_loop=lambda e, b: eval_while(e, b, args),
        ite=lambda e, b1, b2: eval_ite(e, b1, b2, args),
        returns=lambda e: eval_return(e, args),
        empty=lambda: None
    )
    return val


def evaluate(ast: pa.PicoC, args: dict[str, int] = {}) -> int:
    if ast == None:
        return None

    for i in ast.insts():
        eval_inst(i, args)

    return args.get("return")


if __name__ == "__main__":
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 2;
        z = 1;
        
        int ans = x + y * z;
        
        return ans;
    """

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

    data = """
        int x = 1;
        int y = 3;
        int z = 2;
    
        if (z <= y * x) then
            x = 4;
        end
    
        return x;
    """
    vars = {}
    ast = p.parse(data)
    result = evaluate(ast, vars)
    print(ast)
    print(vars)
    print(result)