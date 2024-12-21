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
    fitness_threshold=0.5,
    egg_count=50,
    carrying_capacity=1000
):
    mutation_rate = 5.97e-9
    num_generations = num_decades * 10  # 10 generations per decade
    environment = Environment(num_patches=num_patches, preset=Environment.cave_presets(preset_name))
    population = [Organism() for _ in range(initial_population_size)]

    # Data collection
    population_sizes = []
    average_fitness = []
    trait_averages = {
        "pigmentation": [],
        "eye_size": [],
        "metabolic_rate": [],
        "lateral_line": [],
        "olfactory_bulb": []
    }

    for generation in range(1, num_generations + 1):
        # Change environmental conditions
        environment.change_conditions()
        for patch in environment.patches:
            update_optimal_traits(patch)

        # Move organisms to patches and calculate fitness
        for organism in population:
            organism.move_to_patch(environment)
            organism.calculate_fitness(organism.environment_patch)

        # Filter viable population based on fitness threshold
        viable_population = [org for org in population if org.fitness >= fitness_threshold]
        if not viable_population:
            print(f"Generation {generation}: Population extinct!")
            break

        # Reproduction and mutation
        offspring_population = []
        for organism in viable_population:
            num_offspring = int(organism.fitness * ((egg_count+organism.environment_patch.get('food_availability'))**2/egg_count))
            for _ in range(num_offspring):
                if len(offspring_population) < carrying_capacity:
                    parent = random.choice(viable_population)
                    offspring = Organism.reproduce(parent, organism)
                    offspring.mutate(mutation_rate)
                    offspring_population.append(offspring)

        # Update population
        population = offspring_population
        print(len(population)

        # Collect data
        population_sizes.append(len(population))
        if population:
            avg_fitness = np.mean([org.fitness for org in population])
            average_fitness.append(avg_fitness)
            # Debugging: Print fitness stats for the generation
            print(f"  Average Fitness: {avg_fitness:.4f}")

        for trait in trait_averages:
            avg_trait = (
                np.mean([org.genetics[trait] for org in population]) if population else 0
            )
            trait_averages[trait].append(avg_trait)

        # Print debugging information
        print(f"Generation {generation}:")
        print(f"  Population Size: {len(population)}")
        print(f"  Average Fitness: {average_fitness[-1]:.4f}")
        print(f"  Trait Averages: {', '.join(f'{trait}: {trait_averages[trait][-1]:.4f}' for trait in trait_averages)}")

    # Plot population size over generations
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(population_sizes)), population_sizes, label="Population Size", color="blue", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Population Size")
    plt.title("Population Dynamics Over Time")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot average fitness over generations
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(average_fitness)), average_fitness, label="Average Fitness", color="green", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    plt.title("Fitness Trends Over Generations")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot trait evolution over generations
    plt.figure(figsize=(12, 6))
    for trait, averages in trait_averages.items():
        plt.plot(range(len(averages)), averages, label=f"Average {trait.capitalize()}", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Trait Value")
    plt.title("Trait Evolution Over Generations")
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
