import math
import string
from evogfuzz.evogfuzz_class import EvoGFuzz
from evogfuzz.oracle import OracleResult
from parse import *
from exception import *
from coverage_parse import *


def oracle(inp: str):
    try:
        arith_eval(inp)
        return (OracleResult.NO_BUG, "nobug")
    except testError as e:
        return (OracleResult.BUG, e)
    except ValueError as e:
        return (OracleResult.BUG, e)
    except ZeroDivisionError as e:
        return (OracleResult.BUG, e)

def arith_eval(inp) -> float: 
    p = Parser(str(inp), {a:ord(a) for a in string.ascii_lowercase if a != 'e'})
    return p.getValue()


grammar = {
    "<start>": ["<complex_arith_expr>"],

    "<number>": ["<maybe_minus><onenine><maybe_digits>", "<digit>"],
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
    iterations=30
)

found_exception_inputs = epp.fuzz()
number_of_inp = 0
overflow_count = 0
underflow_count = 0
zero_collision_error = 0
valueerror_count = 0
divisionzero_count = 0
nobug_count = 0 

with open('coverage.txt', 'w') as f:
    f.write("Trial      \t max\tmedian\ttotal \n")
    coverage_value_max = coverage_func(list(found_exception_inputs), "max")
    coverage_value_median = coverage_func(list(found_exception_inputs), "median")
    coverage_value_total = coverage_func(list(found_exception_inputs), "total")

    coverage_value_max = (224 * coverage_value_max - 1 ) / 176
    coverage_value_median = (224 * coverage_value_median - 1) / 176
    coverage_value_total = (277 * coverage_value_total - 3) / 176
    f.write("Coverage")
    f.write("\t")
    f.write(str(format(coverage_value_max,".2f")))
    f.write("\t")
    f.write(str(format(coverage_value_median, ".2f")))
    f.write("\t")
    f.write(str(format(coverage_value_total, ".2f")))


    for inp in list(found_exception_inputs):

        number_of_inp += 1
        exception_type = oracle(str(inp))[1]
        if exception_type == "nobug":
            nobug_count += 1
        if isinstance(exception_type, testError):
            if exception_type.value == "overflow":
                overflow_count += 1
            elif exception_type.value == "underflow":
                underflow_count += 1
            elif exception_type.value == "zero_collision_error":
                zero_collision_error += 1
            else:
                raise ValueError("No such error")
        elif isinstance(exception_type,ValueError):
            valueerror_count += 1
        elif isinstance(exception_type, ZeroDivisionError):
            divisionzero_count += 1

        if len(found_exception_inputs) - number_of_inp < 200:
            print(str(inp).ljust(30), oracle(str(inp)))


    print("number_of_inp: ", number_of_inp)
    print("Nobug: ", nobug_count / number_of_inp * 100)
    print("ValueError: ", valueerror_count / number_of_inp * 100)
    print("OverflowError: ", overflow_count / number_of_inp * 100)
    print("UnderflowError: ", underflow_count / number_of_inp * 100)
    print("ZerocollisionError: ", zero_collision_error / number_of_inp * 100)
    print("DivisionError: ", divisionzero_count / number_of_inp * 100)

    sum_count = valueerror_count + overflow_count + underflow_count + zero_collision_error + divisionzero_count
    distinct_count = 0
    distinct_count += 1 if overflow_count else 0
    distinct_count += 1 if valueerror_count else 0
    distinct_count += 1 if underflow_count else 0
    distinct_count += 1 if zero_collision_error else 0
    distinct_count += 1 if divisionzero_count else 0

    print("Distinct bug: ", distinct_count ," / ", 5)
    f.write('\n')
    f.write("Distinct bug: " + str(distinct_count) + " / " + "5")
    print("Bug Ratio: ", sum_count , " / ", number_of_inp)
    f.write('\n')
    f.write("Bug ratio: " + str(sum_count) + " / " + str(number_of_inp))
    f.close()