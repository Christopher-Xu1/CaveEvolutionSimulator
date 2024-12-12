from environment import Environment
from organism import Organism
from evolution import update_optimal_traits
import random
import matplotlib.pyplot as plt

def run_simulation(num_decades, initial_population_size, mutation_rate, preset_name, num_patches=1, fitness_threshold=0.2, egg_count=3000):
    num_generations = num_decades * 10  # 10 generations per decade
    environment = Environment(num_patches=num_patches, preset=Environment.cave_presets(preset_name))
    population = [Organism() for _ in range(initial_population_size)]

    population_sizes = []
    trait_averages = {"pigmentation": [], "eye_size": [], "metabolic_rate": []}

    for generation in range(1, num_generations + 1):
        environment.change_conditions()
        for patch in environment.patches:
            update_optimal_traits(patch)

        for organism in population:
            organism.move_to_patch(environment)

        for organism in population:
            organism.calculate_fitness(organism.environment_patch)

        total_fitness = sum(org.fitness for org in population)
        reproduction_probabilities = [org.fitness / total_fitness if org.fitness >= fitness_threshold else 0 for org in population]

        new_population = []
        for organism in population:
            if organism.fitness >= fitness_threshold:
                # Egg laying and survival
                eggs = egg_count
                survival_rate = 1 / (eggs / 50)  # Example proportional survival
                surviving_offspring = int(eggs * survival_rate)

                # Generate offspring
                for _ in range(surviving_offspring):
                    parents = random.choices(population, weights=reproduction_probabilities, k=2)
                    offspring = Organism.reproduce(parents[0], parents[1])
                    offspring.mutate(mutation_rate)
                    offspring.move_to_patch(environment)
                    offspring.calculate_fitness(offspring.environment_patch)
                    new_population.append(offspring)

        population = new_population
        population_sizes.append(len(population))

        for trait in trait_averages:
            avg_trait = sum(org.genetics[trait] for org in population) / len(population) if population else 0
            trait_averages[trait].append(avg_trait)

    # Unified plot
    plt.figure(figsize=(12, 8))
    generations = range(num_generations)

    # Plot population size
    plt.plot(generations, population_sizes, label="Population Size", color="blue", linewidth=2)

    # Plot trait averages
    for trait, averages in trait_averages.items():
        plt.plot(generations, averages, label=f"Average {trait.capitalize()}", linewidth=2)

    plt.xlabel("Generation")
    plt.ylabel("Values")
    plt.title("Population Growth and Trait Evolution")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    num_decades = int(input("Enter simulation runtime in decades: "))
    initial_population_size = int(input("Enter initial population size: "))
# The line `mutation_rate = float(input("Enter mutation rate (e.g., 0.05 for 5%): "))` is prompting
# the user to enter a mutation rate for the simulation.
    mutation_rate = float(input("Enter mutation rate (e.g., 0.05 for 5%): "))
    preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
    fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
    egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus): "))
    run_simulation(num_decades, initial_population_size, mutation_rate, preset_name, fitness_threshold=fitness_threshold, egg_count=egg_count)
