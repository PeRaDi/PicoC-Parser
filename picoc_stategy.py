
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

    # data = """
    #     int x = 0;
    #     while ( x < 10) then
    #         x = x + 1;
    #     end
    #     return x;
    # """
    #
    # data = """
    #     int x = 0;
    #     int y = 0;
    #     while ( x < 10) then
    #         x = x + 1;
    #         y = y + 1;
    #     end
    #     return x;
    # """

    data = """
        // bool w = false;
        w = false;
        if(1 == 1) then
            int x = 1 + 3;
            int z = 1 + 5;
        else
            int y = 2;
        end
        return z;
    """

    ast = p.parse(data)
    code = pa.picoc_to_code(ast)

    opt = op.optimize(ast)
    ast2 = p.parse(code)
    opt2 = op.optimize(ast2)

    print(f"AST:\n{ast.print()}\n")
    print(f"OPT:\n{opt.print()}\n")
    print(f"AST2:\n{ast2}\n")
    print(f"OPT2:\n{opt2}\n")
    print(f"CODE:\n{code}\n")

if __name__ == "__main__":
    main()
