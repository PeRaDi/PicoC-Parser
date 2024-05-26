import copy
import random

import pico_adt as pa
import zipper as zp
import strategy as st
import pico_parser as p
import pico_opt as po

def mutations(exp: pa.Exp):
    try:
        r = exp.match(
            # add=lambda x, y: pa.Exp.SUB(x, y),
            # sub=lambda x, y: pa.Exp.ADD(x, y),
            # mul=lambda x, y: pa.Exp.ADD(x, y),
            # div=lambda x, y: pa.Exp.SUB(x, y),
            # neg=lambda x: pa.Exp.NEG(x.neg()),
            # group=lambda x: st.StrategicError,
            # bool=lambda x: pa.Exp.BOOL(not x),
            # var=lambda x: st.StrategicError,
            const=lambda x: pa.Exp.CONST(x + 1),
        )
        if r is st.StrategicError:
            st.failTP(r)
        else:
            return st.idTP(r)
        return st.idTP(r)
    except Exception as e:
        #st.failTP(e)
        st.idTP(exp)

def step_mutations(x, on_fail=st.idTP):
    # print(f"Step: {x}")
    val = st.adhocTP(on_fail, mutations, x)
    # print(f"Val: {val}")
    return val

# Function to gather all nodes in the AST
def gather_nodes(ast):
    node_list = []
    def gather(n):
        # if ((not (x is None))
        #     and type(x.node()) == pa.Exp
        #     and (lambda y: x != pa.Exp.VAR())
        #     and (lambda y: x != pa.Exp.GROUP())
        #     and (lambda y: x != pa.Exp.NEG())):
        #     node_list.append(x)
        try:
            if n is None:
                return st.idTP(n)
            node = n.node()
            node_type = type(node)

            if not node_type is pa.Exp:
                return st.idTP(n)

            node_list.append(n)
            return st.idTP(n)
        except Exception as e:
            return st.idTP(n)

    st.full_tdTP(gather, ast)
    return node_list

def apply_mutation(ast, node):
    print(f"Apply to node {type(node.node())} => {node.node()} => {ast.node()}")
    def apply(x):
        if x == node:
            return step_mutations(x)
        else:
            return st.idTP(x)

    return st.full_tdTP(apply, ast)

def insert_mutations(ast: pa.PicoC) -> list[pa.PicoC]:
    # Para evitar o erro de list is not iterable com o zipper
    ast_to_zip = copy.deepcopy(ast)
    ast_to_zip.insts().append(pa.Inst.EMPTY())
    z = zp.obj(ast_to_zip.insts())

    node_list = gather_nodes(z)
    # Select a random node to mutate
    random_node = random.choice(node_list)
    # print(node_list)
    # print(random_node)
    # Apply mutation to the selected node
    mutated = apply_mutation(z, random_node)

    # mutated = st.full_tdTP(lambda x: step_mutations(x), z)
    opt_z = mutated
    # print(mutated.node())
    # opt_z = st.innermost(lambda x: po.step_instruction(x, lambda y: po.step_cond(y, po.step_expr)), mutated)
    result = opt_z.node()

    result.pop()

    return pa.PicoC.INSTS(result)


if __name__ == '__main__':
    data = """
        int x = 1 + 1;
        int y = 2 - 1;
        int z = 2 * 1;
        int w = 2 / 1;
        int a = -3;
        t = true;
        f = false;
        return x;
    """
    ast = p.parse(data)
    print(f"AST: {ast}")
    mutated = insert_mutations(ast)
    print(f"Mut: {mutated}")