import pico_adt as pa
import pico_parser as p
import pico_opt as op

from hypothesis import given, event, example, strategies as st

def test_manual_parse_of_unparsed_ast():
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 0;
        
        int ans = x + y * z;
        
        return 3 + 4 * 5;
    """


    # data = """
    #     int x = 0;
    #     while ( x < 10) then
    #         x = x + 1;
    #     end
    #     return x;
    # """

    # data = """
    #     int x = 0;
    #     int y = 0;
    #     while ( x < 10) then
    #         x = x + 1;
    #         y = y + 1;
    #     end
    #     return x;
    # """

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