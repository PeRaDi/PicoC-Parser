import pico_adt as pa
import zipper as zp
import strategy as st

def optAdd(x, y):
    if (x == pa.Exp.CONST(0)):
        return y
    elif (y == pa.Exp.CONST(0)):
        return x
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() + y.const())
    else:
        return st.StrategicError

def optSub(x, y):
    if (x == pa.Exp.CONST(0)):
        return y.neg()
    elif (y == pa.Exp.CONST(0)):
        return x
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() - y.const())
    else:
        return st.StrategicError

def optNeg(x):
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

def optMul(x, y):
    if (x == pa.Exp.CONST(0) or y == pa.Exp.CONST(0)):
        return pa.Exp.CONST(0)
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() * y.const())
    elif (lambda a, b: x == pa.Exp() and y == pa.Exp()):
        return pa.Exp.MUL(expr(x), expr(y))
    else:
        return st.StrategicError

def optDiv(x, y):
    if (x == pa.Exp.CONST(0)):
        return pa.Exp.CONST(0)
    elif (lambda a, b: x == pa.Exp.CONST() and y == pa.Exp.CONST()):
        return pa.Exp.CONST(x.const() / y.const())
    else:
        return st.StrategicError

def expr(exp):
    # print(f"EXP: {exp}")
    x = exp.match(
        add=lambda x, y: optAdd(x, y),
        sub=lambda x, y: optSub(x, y),
        mul=lambda x, y: optMul(x, y),
        div=lambda x, y: optDiv(x, y),
        neg=lambda x: optNeg(x),
        bool=lambda x: st.StrategicError,
        var=lambda x: st.StrategicError,
        const=lambda x: st.StrategicError,
    )
    if x is st.StrategicError:
        raise x
    else:
        # print(f"X: {x}")
        return x

def optEqual(x, y):
    # print(f"x: {str(x)} and y: {str(y)}")
    if y == pa.Exp.BOOL("true"):
        return x
    else:
        return st.StrategicError

def conditional(cond):
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
        return x

def step_expr(x):
    return st.adhocTP(st.failTP, expr, x)

def step_cond(x):
    return st.adhocTP(st.failTP, conditional, x)

def optimize(ast):
    empty_added = False

    if len(ast) == 1:
        # Esta condicional é porque gera erro de list is not iterable com o zipper
        ast.append(pa.Inst.EMPTY())
        empty_added = True

    z = zp.obj(ast)
    #return st.innermost(lambda x: st.adhocTP(st.failTP, expr, conditional(x)), z).node()
    #return st.innermost(lambda x: st.adhocTP(st.failTP, lambda y: st.adhocTP(conditional, expr, y), x), z).node()
    result = st.innermost(lambda x: step_expr(x), z).node()
    #result = st.innermost(lambda x: step_cond(x), z).node() # funciona se tiver var == true mas não para exp == true

    # Pelo que percebi na aula o inner most tratava desses casos sem preocupar com a ordem (pelo menos em haskell?, confirmar isso com o professor)
    #result = st.innermost(lambda x: step_cond(step_expr(x)), z).node()
    # funciona se tiver exp == true mas não para var == true
    #result = st.innermost(lambda x: step_expr(step_cond(x)), z).node()

    if empty_added:
        result.pop()

    return result
