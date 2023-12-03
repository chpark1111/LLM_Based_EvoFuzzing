import random
import warnings
warnings.filterwarnings("ignore")

from evollmfuzz.oracle import OracleResult
from evollmfuzz.evollmfuzz_class import EvoLLMFuzz
from parse import *
from exception import *
from coverage_parse import *

if __name__ == "__main__":
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

    num_init_inputs = 20
    input_data_dir = "./data/input.txt"
    initial_inputs = []
    with open(input_data_dir, "r") as f:
        nw = f.readline().strip("\n").strip()
        while nw:
            initial_inputs.append(nw)
            nw = f.readline().strip("\n").strip()
            
    random.shuffle(initial_inputs)
    initial_inputs = initial_inputs[:num_init_inputs]
    # initial_inputs = ["tan(1272)", "cos(-125)", "1 + 3 - sin(34)"]

    print("Initailize Fuzzer")
    elf = EvoLLMFuzz(oracle=oracle,
        inputs=initial_inputs,
        iterations=30,
        num_individuals=80)

    print("Start Fuzzer")
    found_inputs = elf.fuzz()
    elf.evaluate_population(found_inputs)