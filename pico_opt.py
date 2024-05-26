import copy

import pico_adt as pa
import zipper as zp
import strategy as st


def optAdd(x: pa.Exp, y: pa.Exp):
    if (x == pa.Exp.CONST(0)):
        return y
    elif (y == pa.Exp.CONST(0)):
        return x
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() + y.const())
    else:
        return st.StrategicError


def optSub(x: pa.Exp, y: pa.Exp):
    if (x == pa.Exp.CONST(0)):
        return y.neg()
    elif (y == pa.Exp.CONST(0)):
        return x
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() - y.const())
    else:
        return st.StrategicError


def optNeg(x: pa.Exp):
    if (lambda a: x == pa.Exp.NEG()):
        # print(f"Neg: {str(x)}")
        val = x.neg()
        # print(f"N: {str(x)} -> {str(val)}")
        return val
    elif (lambda b: x == pa.Exp.CONST()):
        val = pa.Exp.CONST(-x.const())
        # print(f"NC: {str(x)} -> {str(val)}")
        return val
    # if (lambda b: x == pa.Exp.CONST()):
    #     val = pa.Exp.CONST(-x.const())
    #     print(f"NC: {str(val)}")
    #     return val
    # elif (lambda a: x == pa.Exp.NEG()):
    #     val = x.neg()
    #     print(f"N: {str(val)}")
    #     return val
    else:
        # print(f"O: {str(x)}")
        return st.StrategicError


def optMul(x: pa.Exp, y: pa.Exp):
    if (x == pa.Exp.CONST(0) or y == pa.Exp.CONST(0)):
        return pa.Exp.CONST(0)
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() * y.const())
    elif (lambda a, b: x == pa.Exp() and y == pa.Exp()):
        return pa.Exp.MUL(expr(x), expr(y))
    else:
        return st.StrategicError


def optDiv(x: pa.Exp, y: pa.Exp):
    if (x == pa.Exp.CONST(0)):
        return pa.Exp.CONST(0)
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() / y.const())
    else:
        return st.StrategicError


def instruction(inst: pa.Inst):
    x = inst.match(
        decl=lambda t, s: st.StrategicError,
        atrib=lambda t, s, e: expr(e),
        while_loop=lambda e, b: st.StrategicError,
        ite=lambda e, b1, b2: st.StrategicError,
        returns=lambda e: expr(e),
        empty=lambda: st.StrategicError
    )
    if x is st.StrategicError:
        raise x
    else:
        # print(f"INST: {inst}, val: {x}")
        return x


def expr(exp: pa.Exp):
    x = exp.match(
        add=lambda x, y: optAdd(x, y),
        sub=lambda x, y: optSub(x, y),
        mul=lambda x, y: optMul(x, y),
        div=lambda x, y: optDiv(x, y),
        neg=lambda x: optNeg(x),
        group=lambda x: st.StrategicError,
        bool=lambda x: st.StrategicError,
        var=lambda x: st.StrategicError,
        const=lambda x: st.StrategicError,
        # returns=lambda x: expr(x),
    )
    if x is st.StrategicError:
        raise x
    else:
        # print(f"EXP: {exp}, val: {x}")
        return x


def optEqual(x: pa.Cond, y: pa.Cond):
    # print(f"x: {str(x)} and y: {str(y)}")
    if y == pa.Exp.BOOL(True):
        return x
    else:
        return st.StrategicError


def conditional(cond: pa.Cond):
    x = cond.match(
        equal=lambda x, y: optEqual(x, y),
        not_equal=lambda x, y: st.StrategicError,
        greater=lambda x, y: st.StrategicError,
        greater_equal=lambda x, y: st.StrategicError,
        less=lambda x, y: st.StrategicError,
        less_equal=lambda x, y: st.StrategicError,
    )
    if x is st.StrategicError:
        raise x
    else:
        # print(f"COND: {cond}, val: {x}")
        return x

def step_expr(x, on_fail=st.failTP):
    # print("step_expr: " + str(x))
    val = st.adhocTP(on_fail, expr, x)
    # print(f"STEP_EXPR: {val}")
    return val


def step_cond(x, on_fail=st.failTP):
    val = st.adhocTP(on_fail, conditional, x)
    # print(f"STEP_COND: {val}")
    return val


def step_instruction(x, on_fail=st.failTP):
    val = st.adhocTP(on_fail, instruction, x)
    # print(f"STEP_INST: {val}")
    return val

def optimize(ast: pa.PicoC) -> pa.PicoC:
    # Para evitar o erro de list is not iterable com o zipper
    ast_to_zip = copy.deepcopy(ast)
    ast_to_zip.insts().append(pa.Inst.EMPTY())
    # print(ast_to_zip.print(False))
    z = zp.obj(ast_to_zip.insts())
    # z = zp.obj(ast.insts())

    # Todas essas implementações estão a funcionar
    # result = st.innermost(lambda x: st.adhocTP(lambda y: st.adhocTP(st.failTP, conditional, y), expr, x), z).node()
    # result = st.innermost(lambda x: st.adhocTP(lambda y: step_cond(y), expr, x), z).node()
    # result = st.innermost(lambda x: step_expr(x, on_fail=lambda y: step_cond(y)), z).node()
    # result = st.innermost(lambda x: step_expr(x, step_cond), z).node()
    # result = st.innermost(lambda x: step_expr(x, lambda y: step_cond(y, step_instruction)), z).node()
    result = st.innermost(lambda x: step_instruction(x, lambda y: step_cond(y, step_expr)), z).node()
    # result = st.innermost(lambda x:
    #                       step_instruction(x, lambda i:
    #                       step_bloco(i, lambda b:
    #                       step_expr(b, step_cond))),
    #                       z).node()

    # result.insts().pop()
    result.pop()

    # return result
    return pa.PicoC.INSTS(result)
