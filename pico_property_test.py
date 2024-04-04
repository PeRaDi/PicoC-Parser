import pico_adt as pa
import pico_parser as p
import pico_opt as op

from hypothesis import given, event, example, strategies as st

def test_manual_parse_of_unparsed_ast():
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

    pa.pretty_print = True
    ast = p.parse(data)
    code = pa.picoc_to_code(ast)
    ast2 = p.parse(code)

    assert ast == ast2

# @given(st.integers())
# def test_integers(i):
#     pass
#
# @given(st.integers().filter(lambda x: x % 2 == 0))
# def test_even_integers(i):
#     event(f"i mod 3 = {i % 3}")