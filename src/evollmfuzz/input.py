from typing import Generator, Optional, Dict

from .oracle import OracleResult

class Input:
    """
    Class describing a test input.
    """

    def __init__(self, value: str, oracle: OracleResult = None, fitness: float = 0):
        assert isinstance(value, str)
        self._value: str = value
        self._oracle: Optional[OracleResult] = oracle
        self._fitness: float = float()

    @property
    def value(self) -> str:
        return self._tree

    @property
    def oracle(self) -> OracleResult:
        return self._oracle

    @property
    def fitness(self) -> float:
        return self._fitness

    @oracle.setter
    def oracle(self, oracle_: OracleResult):
        self._oracle = oracle_

    @fitness.setter
    def fitness(self, fitness_: float):
        self._fitness = fitness_

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other):
        if not isinstance(other, Input):
            return False
        return self._value == other._value

    # def __iter__(self) -> Generator[DerivationTree | OracleResult | None, None, None]:
    #     """
    #     Allows tuple unpacking: tree, oracle = input

    #     :return: An iterator of two elements: The derivation tree and the execution oracle.
    #     """
    #     yield self.tree
    #     yield self.oracle

    # def __getitem__(self, item: int) -> Optional[DerivationTree] | OracleResult:
    #     """
    #     Allows accessing the input's derivation tree using index 0 and the oracle using index 1.

    #     param item: The index of the item to get (0 -> tree, 1 -> oracle)
    #     :return: The input's tree or oracle.
    #     """
    #     assert isinstance(item, int)
    #     assert 0 <= item <= 1, "Can only access element 0 (tree) or 1 (oracle)"
    #     if item == 0:
    #         return self.tree
    #     else:
    #         return self.oracle