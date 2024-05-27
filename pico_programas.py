import pico_parser as pp
import pico_adt as pa
import pico_evaluate as pe
import pico_mutation as pm
import pico_instrumentation as pi
import pico_test_suite as pt


programa1 = pp.parse("""
        int x;
        int y;
        int z;

        if (z <= y * x) then
            z = y * x;
        else
            z = (x * y) * 2;
        end

        return z;
    """)

testSuitePrograma1 = [
        ({"x": 1, "y": 3, "z": 2}, 3),
        ({"x": 1, "y": 1, "z": 2}, 2),
        ({"x": 3, "y": 5, "z": 2}, 15),
        ({"x": 2, "y": 4, "z": 10}, 16),
    ]

programa2 = pp.parse("""
        int x;
        int z;
        int count = 0;

        if (x < z) then
            while ( x < z) then
                x = x + 1;
                count = count + 1;
            end 
        else
            while ( x > z) then
                x = x - 1;
                count = count - 1;
            end 
        end

        return count;
    """)

# Foi criado essa mutação manual porque o nosso insert_mutations pode gerar loop infinito
programa2mutated = pp.parse("""
        int x;
        int z;
        int count = 0;

        if (x < z) then
            while ( x < z) then
                x = x + 1;
                count = count + 1;
            end 
        else
            while ( x > z) then
                x = x - 1;
                count = count + 1;
            end 
        end

        return count;
    """)

testSuitePrograma2 = [
        ({"x": 1, "z": 3}, 2),
        ({"x": 10, "z": 13}, 3),
        ({"x": 3, "z": 1}, -2),
        ({"x": 13, "z": 10}, -3),
    ]

programa3 = pp.parse("""
        int a;
        int b;
        int c;
        int m;
        
        if (a > b) then
            if (a > c) then
                m = a;
            else
                m = b;
            end
        else 
            if (b > c) then
                m = b;
            else
                m = c;
            end
        end
        
        return m;
    """)

# Foi criado essa mutação manual porque o nosso insert_mutations está a gerar loop infinito 
# no memento de criação da mutação
programa3mutated = pp.parse("""
        int a;
        int b;
        int c;
        int m;
        
        if (a > b) then
            if (a > c) then
                m = -a;
            else
                m = b;
            end
        else 
            if (b > c) then
                m = b;
            else
                m = c;
            end
        end
        
        return m;
    """)

testSuitePrograma3 = [
        ({"a": 1, "b": 2, "c": 3}, 3),
        ({"a": 1, "b": 4, "c": 2}, 4),
        ({"a": 2, "b": 1, "c": 1}, 2),
    ]

def ponto_4():
    print(pt.runTestSuite(programa1, testSuitePrograma1))
    print(pt.runTestSuite(programa2, testSuitePrograma2))
    print(pt.runTestSuite(programa3, testSuitePrograma3))

def ponto_6():
    print(pt.runTestSuite(pm.insert_mutations(programa1), testSuitePrograma1))
    print(pt.runTestSuite(programa2mutated, testSuitePrograma2))
    print(pt.runTestSuite(programa3mutated, testSuitePrograma3))

def ponto_7():
    programa = pp.parse('print "teste para o terminal"; return 0;')
    print(pe.evaluate(programa, {}))

def ponto_10():
    pt.instrumentedTestSuite(pm.insert_mutations(programa1), testSuitePrograma1)
    pt.instrumentedTestSuite(programa2mutated, testSuitePrograma2)
    pt.instrumentedTestSuite(programa3mutated, testSuitePrograma3 + [({"a": 2, "b": 1, "c": 3}, 3),])
    

if __name__ == "__main__":
    #ponto_4()
    #ponto_6()
    #ponto_7()
    ponto_10()
