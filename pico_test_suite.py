import pico_parser as p
import pico_adt as pa
import pico_evaluate as pe
import pico_mutation_2 as pm
import pico_instrumentation as pi
import copy

class TestResult:
    def __init__(self, passed: bool, trace: list[tuple[int, str]]):
        self.passed = passed
        self.trace = trace
    def __repr__(self):
        return f'Passed: {self.passed}, Trace: {self.trace}'

class JaccardSimilaryCoefficient:
    def __init__(self, id: int, label: str, score: float):
        self.id = id
        self.label = label
        self.score = score

    def __repr__(self):
        return f'Instruction: {self.id}, Label: {self.label}, Score: {self.score}'

def runTest(ast: pa.PicoC, args: tuple[dict[str, int], int]) -> bool:
    result = pe.evaluate(ast, args[0])
    expected = args[1]
    return result == expected

def runTestSuite(ast: pa.PicoC, test_cases: list[tuple[dict[str, int], int]]) -> bool:
    for test_case in test_cases:
        args = copy.deepcopy(test_case)
        result = runTest(ast, args)
        if not result:
            # print(ast, "\n", test_case, "\n", args, "\n", result)
            return False
    return True

def instrumentedTestSuite(ast: pa.PicoC, test_cases: list[tuple[dict[str, int], int]]) -> bool:
    test_results = []
    for test_case in test_cases:
        print(f"\nTestCase: {test_case}")
        args = copy.deepcopy(test_case)
        execution_trace = []
        def trace(inst_id, inst):
            print(f"Instruction {inst_id}: {inst}")
            execution_trace.append((inst_id, inst))
        instrumented = pi.instrumentation(ast, trace)
        result = runTest(instrumented, args)
        test_results.append(TestResult(result, execution_trace))
        # if not result:
        #     # print(ast, "\n", test_case, "\n", args, "\n", result)
        #     return False
    scores = calculate_jaccard(test_results)
    print(f"\nJaccard Similarity Coefficient")
    for s in scores:
        print(s)
    # for s in list(scores.values()):
    #     print(f"{s[0]} => {s[1]}")
    return len([r for r in test_results if r.passed ]) == len(test_results)

def calculate_jaccard(test_results: list[TestResult]) -> list[JaccardSimilaryCoefficient]:
    suspiciousness = {}
    total_passed = sum(1 for result in test_results if result.passed)
    total_failed = sum(1 for result in test_results if not result.passed)
    aux = {}

    for result in test_results:
        for inst_id, inst in result.trace:
            if inst_id not in aux:
                aux[inst_id] = inst

            if inst_id not in suspiciousness:
                suspiciousness[inst_id] = [0, 0]  # [executed in passed, executed in failed]
            if result.passed:
                suspiciousness[inst_id][0] += 1
            else:
                suspiciousness[inst_id][1] += 1

    for inst_id, (passed, failed) in suspiciousness.items():
        total_executed = passed + failed
        if total_executed > 0:
            jaccard_score = failed / total_executed
            suspiciousness[inst_id] = jaccard_score
        else:
            suspiciousness[inst_id] = 0.0

    scores = []
    for inst_id, score in suspiciousness.items():
        # scores[inst_id] = (aux[inst_id], score)
        scores.append(JaccardSimilaryCoefficient(inst_id, aux[inst_id], score))
    return scores

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

def run_suite(code: str, test_cases: list[tuple[dict[str, int], int]], mutate: bool = False):
    ast = p.parse(code)
    if mutate:
        # print(f"AST: {ast}")
        ast = pm.insert_mutations(ast)
        # print(f"Mutations: {ast}")
    result = runTestSuite(ast, test_cases)
    print(result)

def run_instrumented_suite(code: str, test_cases: list[tuple[dict[str, int], int]], mutate: bool = False):
    ast = p.parse(code)
    if mutate:
        # print(f"AST: {ast}")
        ast = pm.insert_mutations(ast)
        # print(f"Mutations: {ast}")
    result = instrumentedTestSuite(ast, test_cases)
    print(f"\nAll tests passed: {result}")
    print()

def suite_test_example():
    print("Test Suite")
    code = """
        int x;
        int y;
        int z;
        int ans = x + y * z;
        return ans;
    """
    run_suite(code, [
        ({"x": 3 * 4 + 5, "y": 3 + 4 * 5, "z": 2}, 63),
        ({"x": 10, "y": 1, "z": -2}, 8),
        ({"x": 10, "y": 20, "z": -2}, -30),
        ({"x": 10, "y": 20, "z": 1/2}, 20),
    ])

    code = """
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
    run_suite(code, [
        ({"x": 1, "y": 3, "z": 2}, 3),
        ({"x": 1, "y": 1, "z": 2}, 2),
        ({"x": 3, "y": 5, "z": 2}, 15),
        ({"x": 2, "y": 4, "z": 10}, 16),
    ])

    code = """
        int x;
        int z;
        int count = 0;

        while ( x < z) then
            x = x + 1;
            count = count + 1;
        end

        return count;
    """
    run_suite(code, [
        ({"x": 1, "z": 3}, 19),
        ({"x": 10, "z": 15}, 5),
    ])


def suite_test_mutation_example():
    print("Test Suite with Mutations")
    code = """
        int x;
        int y;
        int z;
        int ans = x + y * z;
        return ans;
    """
    run_suite(code, [
        ({"x": 3 * 4 + 5, "y": 3 + 4 * 5, "z": 2}, 63),
        ({"x": 10, "y": 1, "z": -2}, 8),
        ({"x": 10, "y": 20, "z": -2}, -30),
        ({"x": 10, "y": 20, "z": 1/2}, 20),
    ], True)

    code = """
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
    run_suite(code, [
        ({"x": 1, "y": 3, "z": 2}, 3),
        ({"x": 1, "y": 1, "z": 2}, 2),
        ({"x": 3, "y": 5, "z": 2}, 15),
        ({"x": 2, "y": 4, "z": 10}, 16),
    ], True)

    code = """
        int x;
        int z;
        int count = 0;

        while ( x < z) then
            x = x + 1;
            count = count - 1; // alterou-se + para -
        end

        return count;
    """
    run_suite(code, [
        ({"x": 1, "z": 20}, 19),
        ({"x": 10, "z": 15}, 5),
    ], False) # Fazemos mutação manual para evitar ciclo infinito


def instrumentation_suite_example():
    print("Instrumented Test Suite")
    code = """
        int x;
        int y;
        int z;
        int ans = x + y * z;
        return ans;
    """
    run_instrumented_suite(code, [
        ({"x": 3 * 4 + 5, "y": 3 + 4 * 5, "z": 2}, 63),
        ({"x": 10, "y": 1, "z": -2}, 8),
        ({"x": 10, "y": 20, "z": -2}, -30),
        ({"x": 10, "y": 20, "z": 1/2}, 20),
    ])

    code = """
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
    run_instrumented_suite(code, [
        ({"x": 1, "y": 3, "z": 2}, 3),
        ({"x": 1, "y": 1, "z": 2}, 2),
        ({"x": 3, "y": 5, "z": 2}, 15),
        ({"x": 2, "y": 4, "z": 10}, 16),
    ])

    code = """
        int x;
        int z;
        int count = 0;

        while ( x < z) then
            x = x + 1;
            count = count + 1; // alterou-se + para -
        end

        return count;
    """
    run_instrumented_suite(code, [
        ({"x": 1, "z": 3}, 2),
        ({"x": 10, "z": 13}, 3),
    ]) # Fazemos mutação manual para evitar ciclo infinito

    code = """
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
    """
    run_instrumented_suite(code, [
        ({"a": 1, "b": 2, "c": 3}, 3),
        ({"a": 1, "b": 4, "c": 2}, 4),
        ({"a": 2, "b": 1, "c": 1}, 2),
        ({"a": 2, "b": 1, "c": 3}, 3),
    ]) # Fazemos mutação manual para evitar ciclo infinito

if __name__ == '__main__':
    # simple_test_example()
    # suite_test_example()
    # suite_test_mutation_example()
    instrumentation_suite_example()