import random
import numpy as np
class Organism:
    def __init__(self, genetics=None):
        if genetics is not None:
            self.genetics = genetics
        else:
            self.genetics = {
                'pigmentation': random.uniform(0, 1),
                'eye_size': random.uniform(0, 1),
                'antennae_length': random.uniform(0, 1),
                'metabolic_rate': random.uniform(0, 1),
            }
        self.fitness = 0
        self.environment_patch = None  # For spatial structure

    def mutate(self, mutation_rate):
        for trait in self.genetics:
            if random.random() < mutation_rate:
                mutation_amount = random.gauss(0, 0.001)
                self.genetics[trait] += mutation_amount
                self.genetics[trait] = max(0, min(1, self.genetics[trait]))

    @staticmethod
    def reproduce(parent1, parent2):
        child_genetics = {
            trait: random.choice(
                [parent1.genetics[trait], parent2.genetics[trait]]
            )
            for trait in parent1.genetics
        }
        return Organism(genetics=child_genetics)

    def calculate_fitness(self, environment_patch):
        """
        Calculate fitness based on the organism's traits and the environment's optimal traits.
        """
        if environment_patch is None or 'optimal_traits' not in environment_patch:
            raise ValueError("Invalid environment patch. Cannot calculate fitness.")

        optimal_traits = environment_patch['optimal_traits']
        fitness = 0
        for trait, value in self.genetics.items():
            optimal = optimal_traits.get(trait, 0.5)  # Default optimal trait value is 0.5
            fitness += (1 - (abs(value - optimal)))  # Fitness inversely proportional to deviation
        self.fitness = fitness / len(self.genetics)  # Normalize fitness to [0, 1]

    def move_to_patch(self, environment):
        self.environment_patch = environment.get_patch()
