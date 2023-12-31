import logging
import random
import tqdm
import math
import copy

from typing import Callable, List, Union, Set, Tuple, Optional, Sequence
from .oracle import OracleResult
from .input import Input
from .llm.intelchat import mutatate_input_with_llm
from .evaluate import evaluate


class EvoLLMFuzz:
    def __init__(
        self,
        oracle: Callable[[Union[Input, str]], Union[OracleResult, Sequence]],
        inputs: List[str],
        iterations: int = 10,
        num_individuals : int = 100
    ):
        self._oracle: Callable[[Input], Union[OracleResult, Sequence]] = oracle
        self._max_iterations: int = iterations
        self._number_individuals: int = num_individuals
        self._elitism_rate: int = 5
        self._tournament_size: int = 4
        self._all_inputs = set()

        self._bug_counts = {}

        self.inputs = set()
        for inp in inputs:
            self.inputs.add(
                Input(
                    value=inp,
                )
            )

    def _update_fitness(self, input):
        """
        Updates the fitness of an individual by running oracle
        """
        bug_type = self._oracle(input)[1] # bug type (oracle returns tuple)
        
        if bug_type == 'nobug':
            fitness = 0
        elif bug_type not in self._bug_counts:
            fitness = 1
        else:
            fitness = 1 / self._bug_counts[bug_type]

        input._fitness = fitness

        return bug_type

    def _fitness_pop(self, population):
        """
        Calculates the fitness for the entire population
        Stores bug counts for later fitness
        """
        new_bug_counts = {}
        for inp in population:
            bug_type = self._update_fitness(inp)
            if bug_type in new_bug_counts:
                new_bug_counts[bug_type] += 1
            else:
                new_bug_counts[bug_type] = 0

        self._bug_counts = new_bug_counts # update bug counts

        return

    def _initialize_population(self):
        initial_strings = copy.deepcopy(list(self.inputs))

        gen_per_string = math.ceil(self._number_individuals / len(self.inputs)) - 1
        input_list = list(self.inputs)
        print("Generating Populations")
        for i in tqdm.tqdm(range(len(input_list))):
            initial_strings.extend(
                mutatate_input_with_llm(input_list[i], gen_per_string) # create new individuals
            )
        initial_strings = initial_strings[:self._number_individuals]

        initial_population = []
        for string in initial_strings:
            initial_population.append(
                Input(value=str(string))
            )

        return initial_population
    
    def _select(self, population):
        """
        selects a individual among population using tournament selection
        """
        k = self._tournament_size
        participants = random.sample(population, k)

        return max(participants, key=lambda x: x.fitness)
    
    def _mutation(self, individual):
        """
        Use LLM to create multiple mutated individuals from 1 individual
        """
        mutated_strings = mutatate_input_with_llm(individual.value, num_gen=self._number_individuals / len(self.inputs))
        
        mutated_individuals = []
        for string in mutated_strings:
            mutated = Input(
                value = string,
            )
            self._update_fitness(mutated)
            mutated_individuals.append(mutated)

        return mutated_individuals
    
    def fuzz(self):
        population = self._initialize_population()
        self._fitness_pop(population)

        count = 0
        while count < self._max_iterations:
            next_gen = []
            print("Mutating Next Generation")
            pbar = tqdm.tqdm(total = self._max_iterations)
            while len(next_gen) < self._number_individuals:
                parent = self._select(population)

                offspring = self._mutation(parent)
                next_gen.extend(offspring)
                pbar.update(len(offspring))

            population.extend(next_gen)
            population = sorted(population, key=lambda x: x.fitness, reverse=True)
            population = population[:self._number_individuals]

            self._fitness_pop(population)
            count += 1
            
            print(count, population[0])
            self.evaluate_population(population)
            
        return population
    
    def evaluate_population(self, population):
        evaluate(population, "LEAF")

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

    evaluate(found_inputs, "LEAF")



