import random
import numpy as np
class Organism:
    def __init__(self, genetics=None):
        if genetics is not None:
            self.genetics = genetics
        else:
            self.genetics = {
                'pigmentation': max(0,random.gauss(0.5, 0.181)),  # Regressive trait
                'eye_size': max(0, random.gauss(0.5, 0.181)),      # Regressive trait
                'metabolic_rate': genetics['pigmentation']+genetics['eye_size'] + genetics['lateral_line'] 
                'lateral_line': max(0,random.gauss(0.5, 0.181)),  # Adaptive trait
                'olfactory_bulb': max(0,random.gauss(0.5, 0.181)) # Adaptive trait
            }
        self.fitness = 0
        self.environment_patch = None

    def mutate(self, mutation_rate):
        for trait in self.genetics:
            if random.random() < mutation_rate:
                mutation_amount = random.gauss(0, 0.1)
                self.genetics[trait] = max(0, min(1, self.genetics[trait] + mutation_amount))

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
        if environment_patch is None or 'optimal_traits' not in environment_patch:
            raise ValueError("Invalid environment patch. Cannot calculate fitness.")

        optimal_traits = environment_patch['optimal_traits']

        # Contribution from regressive traits (energy savings)
        W_r = (
            0.2 * (1 - self.genetics['pigmentation']) + 
            0.3 * (1 - self.genetics['eye_size'])
        )

        # Contribution from adaptive traits (sensory enhancements)
        W_a = (
            0.25 * (1 - abs(self.genetics['lateral_line'] - optimal_traits.get('lateral_line'))) + 
            0.25 * (1 - abs(self.genetics['olfactory_bulb'] - optimal_traits.get('olfactory_bulb')))
        )

        # Energy cost (metabolic rate and maintenance)
        C = 0.4 * self.genetics['metabolic_rate']

        # Fitness calculation
        self.fitness = max(0, W_r + W_a - C)

        # Debugging: Print organism's traits and calculated fitness
        # print(f"Traits: {self.genetics}, Fitness: {self.fitness:.4f}")

    def move_to_patch(self, environment):
        self.environment_patch = environment.get_patch()
