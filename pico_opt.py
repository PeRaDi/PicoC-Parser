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
    if (lambda b: x == pa.Exp.CONST()):
        return pa.Exp.CONST(-x.const())
    elif (lambda a: x == pa.Exp.NEG()):
        return x.neg()
    else:
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

def optBool(x):
    if (x == pa.Exp.BOOL()):
        return x.bool()
    else:
        return st.StrategicError

def expr(exp):
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
        return x

def optEqual(x, y):
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

def optimize(ast):
    z = zp.obj(ast)
    return st.innermost(lambda x: st.adhocTP(st.failTP, expr, x), z).node()
