import numpy as np
import random
from environment import Environment
from organism import Organism
from evolution import update_optimal_traits
import matplotlib.pyplot as plt

def run_simulation(num_decades, initial_population_size, preset_name, num_patches=1, fitness_threshold=0.5, egg_count=50, carrying_capacity=1000):
    mutation_rate = 5.97e-9
    num_generations = num_decades * 10
    environment = Environment(num_patches=num_patches, preset=Environment.cave_presets(preset_name))
    population = [Organism() for _ in range(initial_population_size)]

    for generation in range(1, num_generations + 1):
        environment.change_conditions()
        for patch in environment.patches:
            update_optimal_traits(patch)

        for organism in population:
            organism.move_to_patch(environment)

        for organism in population:
            organism.calculate_fitness(organism.environment_patch)

        viable_population = [org for org in population if org.fitness >= fitness_threshold]
        if not viable_population:
            print("Population extinct!")
            break

        offspring_population = []
        for organism in viable_population:
            num_offspring = int(organism.fitness * egg_count)
            for _ in range(num_offspring):
                if len(offspring_population) < carrying_capacity:
                    parent = random.choice(viable_population)
                    offspring = Organism.reproduce(parent, organism)
                    offspring.mutate(mutation_rate)
                    offspring_population.append(offspring)

        population = offspring_population



# TODO Rename this here and in `run_simulation`
def _extracted_from_run_simulation_70(arg0, arg1):
    plt.xlabel("Generation")
    plt.ylabel(arg0)
    plt.title(arg1)
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    num_decades = int(input("Enter simulation runtime in decades: "))
    initial_population_size = int(input("Enter initial population size: "))
    preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
    fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
    egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus, 50 for mammoth cave fish): "))
    carrying_capacity = int(input("Enter carrying capacity (e.g., 1000): "))
    run_simulation(
        num_decades,
        initial_population_size,
        preset_name,
        num_patches=1,
        fitness_threshold=fitness_threshold,
        egg_count=egg_count,
        carrying_capacity=carrying_capacity
    )
