# organism.py

import random

class Organism:

    def __init__(self, genetics=None):
        """
        Initialize an organism with genetic traits.
        :param genetics: A dictionary representing genetic traits. If None, initialize with random traits.
        """
        if genetics is not None:
            self.genetics = genetics
        else:
            # Initialize with random genetics
            self.genetics = {
                'pigmentation': random.uniform(0, 1),     # 0 = no pigmentation, 1 = full pigmentation
                'eye_size': random.uniform(0, 1),         # 0 = blind, 1 = full eyesight
                'antennae_length': random.uniform(0, 1),  # 0 = short antennae, 1 = long antennae
                'metabolic_rate': random.uniform(0, 1),   # 0 = low, 1 = high
                # Add other traits as needed
            }
        self.fitness = 0

    def mutate(self, mutation_rate):
        """
        Apply mutation to the organism's genetic traits.

        :param mutation_rate: Probability of mutation for each trait.
        """
        for trait in self.genetics:
            if random.random() < mutation_rate:
                # Apply mutation by adding a small random value
                mutation_amount = random.gauss(0, 0.1)  # Mean 0, standard deviation 0.1
                self.genetics[trait] += mutation_amount
                # Ensure trait values stay within [0, 1]
                self.genetics[trait] = max(0, min(1, self.genetics[trait]))

    @staticmethod
    def reproduce(parent1, parent2):
        """
        Create a new organism by combining genetics of two parents.

        :param parent1: First parent organism.
        :param parent2: Second parent organism.
        :return: A new Organism instance representing the offspring.
        """
        child_genetics = {}
        for trait in parent1.genetics:
            # Child inherits each trait from one of the parents
            if random.random() < 0.5:
                child_genetics[trait] = parent1.genetics[trait]
            else:
                child_genetics[trait] = parent2.genetics[trait]
        return Organism(genetics=child_genetics)

    def calculate_fitness(self, environment):
        """
        Calculate the fitness of the organism based on its genetics and the environment.

        :param environment: An instance of the Environment class.
        """
        # Example fitness function
        # Fitness increases as the organism's traits match the environment's optimal traits
        fitness = 0
        for trait in self.genetics:
            optimal = environment.optimal_traits.get(trait, 0.5)  # Default optimal trait value is 0.5
            fitness += (1 - abs(self.genetics[trait] - optimal))
        self.fitness = fitness / len(self.genetics)  # Normalize fitness to be between 0 and 1

    def __repr__(self):
        return f"Organism(genetics={self.genetics}, fitness={self.fitness})"
