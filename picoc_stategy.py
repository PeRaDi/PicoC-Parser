
import pico_parser as p

def main():
    data = """ 
        int x = 3 * 4 + 5;
        int y = 3 + 4 * -5;
        
        if(1 == 0) then 
            int x = 1 + 1;
        else 
            int x = 2;
        end
    
        if(x > (2+2*2)) then
            int a = 1;
        else
            int b = 2;
        end
    
        while(x > 2) then
            int c = 3;
        end
    """
    ast = p.parse(data)
    print(ast)

if __name__ == "__main__":
    main()
