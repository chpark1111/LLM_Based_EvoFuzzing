import math
import string
from evogfuzz.evogfuzz_class import EvoGFuzz
from evogfuzz.oracle import OracleResult

def oracle(inp: str) -> OracleResult:
    try:
        arith_eval(inp)
        return OracleResult.NO_BUG
    except ValueError:
        return OracleResult.BUG


def arith_eval(inp) -> float:
    return eval(
        str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log}
    )

grammar = {
    "<start>": ["<complex_arith_expr>"],

    "<number>": ["<maybe_minus><onenine><maybe_digits>"],
    "<maybe_minus>": ["", "-"],
    "<onenine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],

    "<complex_arith_expr>": ["<number>", "<function>(<complex_arith_expr>)", "<function>(<number>)", "(<complex_arith_expr> <binary_operation> <complex_arith_expr>)"],
    "<function>": ["sqrt", "sin", "cos", "tan", "log"],
    
    "<binary_operation>": ["+", "-", "/", "*"],
}

initial_inputs = ['cos(10)', 'sqrt(28367)', 'tan(-12)', 'sqrt(3)']

epp = EvoGFuzz(
    grammar=grammar,
    oracle=oracle,
    inputs=initial_inputs,
    iterations=10
)

found_exception_inputs = epp.fuzz()
for inp in list(found_exception_inputs)[:20]:
    print(str(inp).ljust(30), inp.oracle)