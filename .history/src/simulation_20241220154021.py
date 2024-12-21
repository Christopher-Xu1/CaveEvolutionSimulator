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
    num_patches,
    fitness_threshold,
    egg_count,
    carrying_capacity
):
    mutation_rate = 0.0026
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
        
        for trait, values in trait_averages.items():
            avg_trait = (
                np.mean([org.genetics[trait] for org in population]) if population else 0
            )
            values.append(avg_trait)

        # Print information
        print(f"Generation {generation}:")
        print(f"  Population Size: {len(population)}")
        print(f"  Average Fitness: {avg_fit:.4f}")
        print("  Trait Averages:")
        for trait, values in trait_averages.items():
            print(f"    {trait}: {values[-1]:.4f}")

        #calculate surviving probablities
        surviving_population = [org for org in population if random.uniform(0,fitness_threshold) < org.fitness]

        if not surviving_population:
            print(f"Generation {generation}: Population extinct!")
            break

        # Reproduction and mutation
        offspring_population = []
        offspring_counts = []
        total_potential_offspring = 0

        # Calculate potential offspring counts
        for organism in surviving_population:
            # Ensure that food_availability is obtained correctly
            food_availability = organism.environment_patch.get('food_availability', 0)
            reproductive_capability= (organism.fitness**2 *2) * ((egg_count)*((1+food_availability)** 2) / egg_count)
            count = int(random.gauss(reproductive_capability, 1))
            offspring_counts.append(count)
            total_potential_offspring += count

        # Adjust counts if total exceeds carrying capacity
        if total_potential_offspring > carrying_capacity:
            scaling_factor = carrying_capacity / total_potential_offspring
            offspring_counts = [int(count * scaling_factor) for count in offspring_counts]
            total_potential_offspring = sum(offspring_counts)

        # Initialize a set to track organisms that have already reproduced
        reproduced_set = set()

        # Create offspring using adjusted counts
        for organism, num_offspring in zip(surviving_population, offspring_counts):
            if organism in reproduced_set:
                continue  # Skip if already reproduced
            for _ in range(num_offspring):
                # Select a parent who has not yet reproduced and is not the current organism
                eligible_parents = [p for p in surviving_population if p not in reproduced_set and p != organism]
                if eligible_parents:
                    parent = random.choice(eligible_parents)
                else:
                    parent = organism  # If no eligible parents, reproduce with self
                # Reproduce to create an offspring
                offspring = organism.reproduce(organism, parent)
                # Apply mutation
                offspring.mutate(mutation_rate)
                # Add offspring to the new population
                offspring_population.append(offspring)
            # Mark the organism as having reproduced
            reproduced_set.add(organism)


        # Update population
        population = offspring_population

        # Initialize a dictionary to count organisms per patch
patch_population = {patch: 0 for patch in environment.patches}

for org in population:
    patch = org.environment_patch
    patch_population[patch] += 1

        
        population_sizes.append(len(population))
        

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
    # try:
    #     num_decades = int(input("Enter simulation runtime in decades: "))
    #     initial_population_size = int(input("Enter initial population size: "))
    #     preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
    #     fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
    #     num_patches=int(input("Enter number of cave patches (1-5): "))
    #     egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus, 50 for mammoth cave fish): "))
    #     carrying_capacity = int(input("Enter carrying capacity (usually 500-5000): "))
    # except ValueError as e:
    #     print(f"Invalid input: {e}")
    #     exit(1)

    run_simulation(
        num_decades=10,
        initial_population_size=500,
        preset_name="default_cave",
        num_patches=1,
        fitness_threshold=0.5,
        egg_count=50,
        carrying_capacity=1000
    )
    # run_simulation(
    #     num_decades=num_decades,
    #     initial_population_size=initial_population_size,
    #     preset_name=preset_name,
    #     num_patches=num_patches,
    #     fitness_threshold=fitness_threshold,
    #     egg_count=egg_count,
    #     carrying_capacity=carrying_capacity
    # )
