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
                mutation_amount = random.gauss(0, 0.1)
                self.genetics[trait] += mutation_amount
                self.genetics[trait] = max(0, min(1, self.genetics[trait]))

    @staticmethod
    def reproduce(parent1, parent2):
        child_genetics = {}
        for trait in parent1.genetics:
            child_genetics[trait] = random.choice([parent1.genetics[trait], parent2.genetics[trait]])
        return Organism(genetics=child_genetics)

    def calculate_fitness(self, environment):
        optimal_traits = environment['optimal_traits']
        fitness = 0
        for trait in self.genetics:
            optimal = optimal_traits.get(trait, 0.5)
            fitness += (1 - abs(self.genetics[trait] - optimal))
        self.fitness = fitness / len(self.genetics)

    def move_to_patch(self, environment):
        self.environment_patch = environment.get_patch()
