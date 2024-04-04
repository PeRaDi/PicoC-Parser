
import pico_adt as pa
import pico_parser as p
import pico_opt as op

def main():
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * -5;
        int z = 0;
        
        if(z <= (x + 2 * y)) then 
             z = (1 + 3) * y;
        end
        
        if (w == true) then
            x = y;
        end
        
        if (g == false) then
            k = y;
        end
        
        if(1 == 0) then 
            int x = 1 + 3;
        else 
            int x = 2;
        end
    
        if(x > (2+2*4)) then
            int a = 1;
        else
            int b = 2;
        end
    
        while(x > 2) then
            int c = 3;
        end
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

    data = """
        int x = 2 + 3 * 5;
        if(1 == 0) then
            int x = 1 + 3;
        end
        z = 3;
    """

    pa.pretty_print = True
    ast = p.parse(data)
    print(f"AST: {ast}")

    opt = op.optimize(ast)
    print(f"OPT: {opt}")

    print("\n")

    code = pa.picoc_to_code(ast)
    print(f"CODE: \n{code}\n")

    ast2 = p.parse(code)
    print(f"AST2: {ast2}")
    print(f"OPT2: {op.optimize(ast2)}")

    print(ast == ast2)

if __name__ == "__main__":
    main()
