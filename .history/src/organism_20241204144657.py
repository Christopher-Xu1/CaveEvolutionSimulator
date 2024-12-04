# organism.py

class Organism:
    """
    A class representing a troglobite organism with genetic traits.
    """

    def __init__(self, genetics=None, input_mode='user'):
        """
        Initialize an organism with genetic traits.

        :param genetics: A dictionary representing genetic traits. If None, initialize based on input_mode.
        :param input_mode: Mode of input ('user' for user input, 'random' for random initialization).
        """
        if genetics is not None:
            self.genetics = genetics
        elif input_mode == 'user':
            # Initialize with user-inputted genetics
            self.genetics = self.get_user_input_genetics()
        elif input_mode == 'random':
            # Initialize with random genetics
            self.genetics = self.get_random_genetics()
        else:
            raise ValueError("Invalid input_mode. Choose 'user' or 'random'.")
        self.fitness = 0

    @staticmethod
    def get_user_input_genetics():
        """
        Collect genetic trait values from the user.

        :return: A dictionary of genetic traits.
        """
        genetics = {}
        print("Please input values for the following traits (between 0 and 1):")

        traits = ['pigmentation', 'eye_size', 'antennae_length', 'metabolic_rate']
        for trait in traits:
            while True:
                try:
                    value = float(input(f"{trait.replace('_', ' ').title()}: "))
                    if 0 <= value <= 1:
                        genetics[trait] = value
                        break
                    else:
                        print("Please enter a value between 0 and 1.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value between 0 and 1.")
        return genetics

    @staticmethod
    def get_random_genetics():
        """
        Generate random genetic trait values.

        :return: A dictionary of genetic traits.
        """
        import random
        genetics = {
            'pigmentation': random.uniform(0, 1),
            'eye_size': random.uniform(0, 1),
            'antennae_length': random.uniform(0, 1),
            'metabolic_rate': random.uniform(0, 1),
        }
        return genetics

    def mutate(self, mutation_rate):
        """
        Apply mutation to the organism's genetic traits.

        :param mutation_rate: Probability of mutation for each trait.
        """
        import random
        for trait in self.genetics:
            if random.random() < mutation_rate:
                mutation_amount = random.gauss(0, 0.1)  # Mean 0, standard deviation 0.1
                self.genetics[trait] += mutation_amount
                self.genetics[trait] = max(0, min(1, self.genetics[trait]))

    @staticmethod
    def reproduce(parent1, parent2):
        """
        Create a new organism by combining genetics of two parents.

        :param parent1: First parent organism.
        :param parent2: Second parent organism.
        :return: A new Organism instance representing the offspring.
        """
        import random
        child_genetics = {}
        for trait in parent1.genetics:
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
        fitness = 0
        for trait in self.genetics:
            optimal = environment.optimal_traits.get(trait, 0.5)
            fitness += (1 - abs(self.genetics[trait] - optimal))
        self.fitness = fitness / len(self.genetics)

    def __repr__(self):
        return f"Organism(genetics={self.genetics}, fitness={self.fitness})"
