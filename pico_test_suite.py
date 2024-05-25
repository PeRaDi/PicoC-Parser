import pico_parser as p
import pico_adt as pa
import pico_evaluate as pe

def runTest(ast: pa.PicoC, args: tuple[dict[str, int], int]) -> bool:
    result = pe.evaluate(ast, args[0])
    expected = args[1]
    return result == expected


if __name__ == '__main__':
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