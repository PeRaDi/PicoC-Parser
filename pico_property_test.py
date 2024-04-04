
from hypothesis import given, event, example, strategies as st

@given(st.integers())
def test_integers(i):
    pass

@given(st.integers().filter(lambda x: x % 2 == 0))
def test_even_integers(i):
    event(f"i mod 3 = {i % 3}")