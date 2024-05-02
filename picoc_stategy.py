
import pico_adt as pa
import pico_parser as p
import pico_opt as op

def main():
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 0;
        
        int ans = x + y * z;
        
        return 3 + 4 * 5;
        
    """

    # data = """
    #     x = y * ((2 + 4) / 2);
    # """
    #
    # data = """
    #     if (x == true) then
    #         x = 1;
    #     end
    # """
    #
    # data = """
    #     if(1 == 0) then
    #         int x = 1 + 3;
    #     else
    #         int x = 2;
    #     end
    #
    #     if (z <= (x + 2 * y)) then
    #         z = (1 + 3) * y;
    #     end
    #
    #     if (w == true) then
    #         x = y;
    #     else
    #         x = y;
    #     end
    # """

    # data = """
    #     int x = 2 + 3 * 5;
    #     if(1 == 0) then
    #         int x = 1 + 3;
    #     end
    #     z = 3;
    # """

    pa.pretty_print = True
    ast = p.parse(data)
    code = pa.picoc_to_code(ast)
    opt = op.optimize(ast)
    ast2 = p.parse(code)
    opt2 = op.optimize(ast2)

    pa.pretty_print = False
    print(f"AST: {ast}")
    print(f"OPT: {opt}")
    print("\n")
    print(f"AST2: {ast2}")
    print(f"OPT2: {opt2}")
    print("\n")
    print(ast == ast2)
    print(opt == opt2)
    print(f"CODE: \n{code}\n")

if __name__ == "__main__":
    main()
