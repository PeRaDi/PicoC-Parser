import pico_parser as parser
import pico_adt as pa

def test_instrumentation():
    data = """
        int x = 3 * 4 + 5;
        int y = 3 + 4 * 5;
        int z = 2;
        z = 1;
        
        int ans = x + y * z;
        
        return ans;
    """
    
    ast = parser.parse(data)
    
    intrumentated = pa.instrumentation(ast)
    
    print(intrumentated)

if __name__ == "__main__":
    test_instrumentation()
