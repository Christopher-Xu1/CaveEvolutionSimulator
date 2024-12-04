from organism import Organism
from environment import Environment
import random

def run_simulation(num_generations, initial_population_size, mutation_rate):
    
    environment = Environment()
    population = []
