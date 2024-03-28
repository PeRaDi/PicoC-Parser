
import pico_parser as p
import pico_opt as op

def main():
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * -5;
        
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
    #     int x = 1 + 0;
    # """
    ast = p.parse(data)
    print(ast)
    opt = op.optimize(ast)
    print(opt)

if __name__ == "__main__":
    main()
