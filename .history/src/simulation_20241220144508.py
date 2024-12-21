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
    mutation_rate = random.gauss(5.97e-9,1e-7)
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
            
        avg_fit = np.mean([org.fitness for org in population]) if population else 0
        average_fitness.append(avg_fit)
        # Filter viable population based on fitness threshold
        viable_population = [org for org in population if org.fitness+random.gauss(0,0.1) >= fitness_threshold]

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
            repoductive_capability= max(1,(organism.fitness * 2) * ((egg_count)*(1+food_availability)** 3 / egg_count))
            count = random.randint(repoductive_capability-1, repoductive_capability+1)
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
    plot_results_separate(population_sizes, average_fitness, trait_averages)


def plot_results_separate(population_sizes, average_fitness, trait_averages):
    generations = range(1, len(population_sizes) + 1)

    # Plot Population Size
    plt.figure(figsize=(10, 6))
    plt.plot(generations, population_sizes, label="Population Size", color="blue", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Population Size")
    plt.title("Population Dynamics Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Average Fitness
    plt.figure(figsize=(10, 6))
    plt.plot(generations, average_fitness, label="Average Fitness", color="green", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    plt.title("Fitness Trends Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Trait Averages Together
    plt.figure(figsize=(10, 6))
    for trait, averages in trait_averages.items():
        plt.plot(generations, averages, label=f"Average {trait.capitalize()}", linewidth=2)
    plt.xlabel("Generation")
    plt.ylabel("Average Trait Value")
    plt.title("Trait Evolution Over Generations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    try:
        num_decades = int(input("Enter simulation runtime in decades: "))
        initial_population_size = int(input("Enter initial population size: "))
        preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
        fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
        num_patches=int(input("Enter number of cave patches (1-5): "))
        egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus, 50 for mammoth cave fish): "))
        carrying_capacity = int(input("Enter carrying capacity (usually 500-5000): "))
    except ValueError as e:
        print(f"Invalid input: {e}")
        exit(1)

    run_simulation(
        num_decades10,
        initial_population_size=initial_population_size,
        preset_name=preset_name,
        num_patches=num_patches,
        fitness_threshold=fitness_threshold,
        egg_count=egg_count,
        carrying_capacity=carrying_capacity
    )
    run_simulation(
        num_decades=num_decades,
        initial_population_size=initial_population_size,
        preset_name=preset_name,
        num_patches=num_patches,
        fitness_threshold=fitness_threshold,
        egg_count=egg_count,
        carrying_capacity=carrying_capacity
    )
