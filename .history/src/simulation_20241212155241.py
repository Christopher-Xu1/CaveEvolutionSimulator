import numpy as np
import random
from environment import Environment
from organism import Organism
from evolution import update_optimal_traits
import matplotlib.pyplot as plt

def run_simulation(
    num_decades,
    initial_population_size,
    preset_name,
    num_patches=1,
    fitness_threshold=0.2,
    egg_count=3000,
    carrying_capacity=1000
):
    mutation_rate = 5.97e-9
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
            organism.move_to_patch(environment)  # Assign a valid patch

        for organism in population:
            organism.calculate_fitness(organism.environment_patch)  # Calculate fitness

        viable_population = [org for org in population if org.fitness >= fitness_threshold]

        if not viable_population:
            print("Population extinct!")
            break

        # Adjust survival rate based on egg count
        survival_rate = min(1, 1 / (egg_count / 10))
        total_offspring = sum(int(egg_count * survival_rate) for _ in viable_population)

        # Create offspring population
        parents = random.choices(
            viable_population,
            weights=[org.fitness for org in viable_population],
            k=min(total_offspring * 2, len(viable_population) * 2)
        )
        new_population = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                offspring = Organism.reproduce(parents[i], parents[i + 1])
                offspring.mutate(mutation_rate)
                offspring.move_to_patch(environment)
                offspring.calculate_fitness(offspring.environment_patch)
                new_population.append(offspring)

        # Enforce carrying capacity
        if len(new_population) > carrying_capacity:
            new_population = random.sample(new_population, carrying_capacity)

        population = new_population
        population_sizes.append(len(population))

        for trait in trait_averages:
            avg_trait = (
                np.mean([org.genetics[trait] for org in population]) if population else 0
            )
            trait_averages[trait].append(avg_trait)

    plt.figure(figsize=(12, 8))
    generations = range(len(population_sizes))
    plt.plot(generations, population_sizes, label="Population Size", color="blue", linewidth=2)

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
    preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
    fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
    egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus, 50 for mammoth cave fish): "))
    carrying_capacity = int(input("Enter carrying capacity (e.g., 1000): "))
    run_simulation(
        num_decades,
        initial_population_size,
        preset_name,
        fitness_threshold=fitness_threshold,
        egg_count=egg_count,
        carrying_capacity=carrying_capacity,
    )
