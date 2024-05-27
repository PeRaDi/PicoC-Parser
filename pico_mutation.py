import copy
import random

import pico_adt as pa
import zipper as zp
import strategy as st
import pico_parser as p
import pico_opt as po

mutation_applied = False  # Flag to ensure only one mutation is applied

def mutations(node: pa.Exp):
    global mutation_applied
    if mutation_applied or random.uniform(0.0, 1.0) < 0.5:
        st.failTP(node)  # Skip mutation if one has already been applied

    try:
        t = type(node)
        if node is None or t in [list, str, int, pa.Inst, pa.Bloco, pa.Cond]:
            st.failTP(node)
        #print(t, node, node.type_str(), node.can_be_mutated())
        if not node.can_be_mutated():
            st.failTP(node)

        r = node.match(
            add=lambda x, y: pa.Exp.SUB(x, y),
            sub=lambda x, y: pa.Exp.ADD(x, y),
            mul=lambda x, y: pa.Exp.ADD(x, y),
            div=lambda x, y: pa.Exp.SUB(x, y),
            neg=lambda x: st.StrategicError, #pa.Exp.NEG(x.neg()),
            group=lambda x: st.StrategicError,
            bool=lambda x: pa.Exp.BOOL(not x),
            var=lambda x: st.StrategicError,
            const=lambda x: pa.Exp.CONST(x + 1),
        )

        if r is st.StrategicError:
            st.failTP(r)
        else:
            mutation_applied = True
            # print(f"Mutation applied: {node} ==> {r} => {r.print(False)}")
            return st.idTP(r)
    except Exception as e:
        # print(f"Erro: {e}")
        st.failTP(e)

def step_mutations(x, on_fail=st.idTP):
    return st.adhocTP(on_fail, mutations, x)

def insert_mutations(ast: pa.PicoC) -> pa.PicoC:
    global mutation_applied

    # print(ast)
    # Para evitar o erro de list is not iterable com o zipper
    ast_to_zip = copy.deepcopy(ast)
    ast_to_zip.insts().append(pa.Inst.EMPTY())
    z = zp.obj(ast_to_zip.insts())

    # mutated = st.full_tdTP(lambda x: step_mutations(x), z)
    mutated = False
    while not mutated:
        mutation_applied = False  # Reset the mutation flag
        # Algumas mutações estão a causar error no zipper por isso
        # tenta aplicar mutação até conseguir um que não causa erro
        try:
            mutated_z = st.full_tdTP(lambda x: step_mutations(x), copy.deepcopy(z))
            opt_z = mutated_z
            mutated = mutation_applied
        except Exception as e:
            mutated = False

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