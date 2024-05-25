import pico_parser as p
import pico_adt as pa
import pico_evaluate as pe
import copy

def runTest(ast: pa.PicoC, args: tuple[dict[str, int], int]) -> bool:
    result = pe.evaluate(ast, args[0])
    expected = args[1]
    return result == expected

def runTestSuite(ast: pa.PicoC, test_cases: list[tuple[dict[str, int], int]]) -> bool:
    for test_case in test_cases:
        args = copy.deepcopy(test_case)
        result = runTest(ast, args)
        if not result:
            print(ast, "\n", test_case, "\n", args, "\n", result)
            return False
    return True

def simple_test_example():
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 2;
        z = 1;
        
        int ans = x + y * z;
        
        return ans;
    """
    print(runTest(p.parse(data), args=({}, 40)))

    data = """
        int x = 1;
        int z = 10;
        int count = 0;
        
        while ( x <= z) then
            x = x + 1;
            count = count + 1;
        end
    
        return count;
    """
    print(runTest(p.parse(data), args=({}, 10)))

    data = """
        int x = 1;
        int y = 3;
        int z = 2;
    
        if (z <= y * x) then
            x = 4;
        end
    
        return x;
    """
    print(runTest(p.parse(data), args=({}, 4)))

def suite_test_example():
    data = """
        int x;
        int y;
        int z;
        int ans = x + y * z;
        return ans;
    """
    print(runTestSuite(p.parse(data), [
        ({"x": 3 * 4 + 5, "y": 3 + 4 * 5, "z": 2}, 63),
        ({"x": 10, "y": 1, "z": -2}, 8),
        ({"x": 10, "y": 20, "z": -2}, -30),
        ({"x": 10, "y": 20, "z": 1/2}, 20),
    ]))

    data = """
        int x;
        int y;
        int z;
    
        if (z <= y * x) then
            z = y * x;
        else
            z = (x * y) * 2;
        end
    
        return z;
    """
    print(runTestSuite(p.parse(data), [
        ({"x": 1, "y": 3, "z": 2}, 3),
        ({"x": 1, "y": 1, "z": 2}, 2),
        ({"x": 3, "y": 5, "z": 2}, 15),
        ({"x": 2, "y": 4, "z": 10}, 16),
    ]))

    data = """
        int x;
        int z;
        int count = 0;

        while ( x < z) then
            x = x + 1;
            count = count + 1;
        end

        return count;
    """
    print(runTestSuite(p.parse(data), [
        ({"x": 1, "z": 20}, 19),
        ({"x": 10, "z": 15}, 5),
    ]))

if __name__ == '__main__':
    # simple_test_example()
    suite_test_example()