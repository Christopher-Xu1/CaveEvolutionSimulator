# simulation.py

from organism import Organism
from environment import Environment
import random

def run_simulation(num_generations, initial_population_size, mutation_rate):

    # Initialize environment
    environment = Environment()
    
    # Initialize population with user inputs
    population = []
    for i in range(initial_population_size):
        print(f"\nInitializing Organism {i+1}:")
        organism = Organism()
        organism.calculate_fitness(environment)
        population.append(organism)

    for generation in range(1, num_generations + 1):
        print(f"\n--- Generation {generation} ---")
        
        # Calculate fitness for all organisms
        for organism in population:
            organism.calculate_fitness(environment)

        # Check if all organisms have zero fitness
        total_fitness = sum(org.fitness for org in population)
        if total_fitness == 0:
            print("All organisms have zero fitness. Simulation ends.")
            break

        # Selection probabilities based on fitness
        reproduction_probabilities = [org.fitness / total_fitness for org in population]

        # Reproduction phase
        new_population = []
        for _ in range(len(population)):
            # Select two parents based on fitness
            parents = random.choices(
                population,
                weights=reproduction_probabilities,
                k=2
            )
            # Reproduce to create an offspring
            offspring = Organism.reproduce(parents[0], parents[1])
            # Mutate offspring
            offspring.mutate(mutation_rate)
            # Calculate offspring fitness
            offspring.calculate_fitness(environment)
            new_population.append(offspring)

        # Parents die after reproduction
        population = new_population

        # Display population details
        print(f"\nPopulation at Generation {generation}:")
        for i, org in enumerate(population, 1):
            print(f"Organism {i}: {org}")

    print("\nSimulation completed.")

if __name__ == "__main__":
    try:
        num_generations = int(input("Enter the number of generations to simulate: "))
        initial_population_size = int(input("Enter the initial population size: "))
        mutation_rate = float(input("Enter the mutation rate (e.g., 0.05 for 5%): "))
        run_simulation(num_generations, initial_population_size, mutation_rate)
    except ValueError:
        print("Invalid input. Please enter numeric values.")
