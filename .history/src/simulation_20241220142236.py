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
            
        avg_fit = np.mean([org.fitness() for org in population]) if population else 0
        average_fitness.append(avg_fit)
        print(f"Debug: Average Fitness = {avg_fit:.4f}")
        # Filter viable population based on fitness threshold
        viable_population = [org for org in population if org.fitness >= fitness_threshold]
        print(f"Debug: Viable Population Size = {len(viable_population)}, Threshold = {fitness_threshold}")

        if not viable_population:
            print(f"Generation {generation}: Population extinct!")
            break

        # Reproduction and mutation
        offspring_population = []
        offspring_counts = []
        total_potential_offspring = 0

        # Calculate potential offspring counts
        for organism in viable_population:
            # Ensure that food_availability is obtained correctly
            food_availability = organism.environment_patch.get('food_availability', 0)
            count = int(
                (organism.fitness ** 2) *
                ((egg_count + food_availability) ** 2 / egg_count)
            )
            offspring_counts.append(count)
            total_potential_offspring += count

        # Adjust counts if total exceeds carrying capacity
        if total_potential_offspring > carrying_capacity:
            scaling_factor = carrying_capacity / total_potential_offspring
            offspring_counts = [int(count * scaling_factor) for count in offspring_counts]
            total_potential_offspring = sum(offspring_counts)
            print(f"Adjusted offspring counts to fit carrying capacity: {total_potential_offspring}")

        # Create offspring using adjusted counts
        for organism, num_offspring in zip(viable_population, offspring_counts):
            for _ in range(num_offspring):
                parent = random.choice(viable_population)
                offspring = organism.reproduce(organism, parent)
                offspring.mutate(mutation_rate)
                offspring_population.append(offspring)

        # Update population
        population = offspring_population

        # Collect data
        population_sizes.append(len(population))

        avg_fit = np.mean([org.calculate_fitness() for org in population]) if population else 0
        average_fitness.append(avg_fit)
        print(f"Debug: Average Fitness = {avg_fit:.4f}")

        for trait, values in trait_averages.items():
            avg_trait = (
                np.mean([org.genetics[trait] for org in population]) if population else 0
            )
            values.append(avg_trait)

        # Print debugging information
        print(f"Generation {generation}:")
        print(f"  Population Size: {len(population)}")
        print(f"  Average Fitness: {avg_fit:.4f}")
        print("  Trait Averages:")
        for trait, values in trait_averages.items():
            print(f"    {trait}: {values[-1]:.4f}")

    # Plotting Results
    plot_results(population_sizes, average_fitness, trait_averages)


def plot_results(population_sizes, average_fitness, trait_averages):
    plt.figure(figsize=(12, 6))

    # Plot Population Size
    plt.plot(range(1, len(population_sizes) + 1), population_sizes, label="Population Size", color="blue", linewidth=2)
    
    # Plot Average Fitness
    plt.plot(range(1, len(average_fitness) + 1), average_fitness, label="Average Fitness", color="green", linewidth=2)

    # Plot Trait Averages
    for trait, averages in trait_averages.items():
        plt.plot(range(1, len(averages) + 1), averages, label=f"Average {trait.capitalize()}", linewidth=2)

    # Configure Plot
    plt.xlabel("Generation")
    plt.ylabel("Value")
    plt.title("Simulation Results Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # try:
    #     num_decades = int(input("Enter simulation runtime in decades: "))
    #     initial_population_size = int(input("Enter initial population size: "))
    #     preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
    #     fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
    #     egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus, 50 for mammoth cave fish): "))
    #     carrying_capacity = int(input("Enter carrying capacity (e.g., 1000): "))
    # except ValueError as e:
    #     print(f"Invalid input: {e}")
    #     exit(1)

    run_simulation(
        num_decades=10,
        initial_population_size=500,
        preset_name="default_cave",
        num_patches=1,
        fitness_threshold=0.5,
        egg_count=500,
        carrying_capacity=2000
    )
