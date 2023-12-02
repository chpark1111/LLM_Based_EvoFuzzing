from evollmfuzz.oracle import OracleResult
from evollmfuzz.evollmfuzz_class import EvoLLMFuzz

if __name__ == "__init__":
    def oracle(inp: str) -> (OracleResult, str):
        e = "nobug"
        return (OracleResult.NO_BUG, e)
    
    initial_inputs = ["tan(1272)", "cos(-125)", "1 + 3 - sin(34)"] # TODO fill

    elf = EvoLLMFuzz()

    found_inputs = elf.fuzz(
        oracle=oracle,
        inputs=initial_inputs,
        iterations=10
    )