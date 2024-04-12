import pico_parser as p

commands = {
    
}

data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * -5;
        int z = 0;
        
        return x + y + z;
    """

def evaluate(ast, args = None):
    if ast == None:
        return None
    elif type(ast) == list:
        for x in ast:
            evaluate(x, args)
    elif ast 
    else:
        raise Exception("Invalid command")
vars = {}
evaluate(p.parse(data))