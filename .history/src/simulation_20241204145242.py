from organism import Organism
from environment import Environment
import random

def run_simulation(num_generations, initial_population_size, mutation_rate):
    
    environment = Environment()
    population = []
    for i in range(initial_population_size):
        print(f"\nInitializing Organism {i+1}:")
        organism = Organism(input_mode='user')
        organism.calculate_fitness(environment)
        population.append(organism)
    
            
    
