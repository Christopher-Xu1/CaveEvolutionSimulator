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
    fitness_threshold,  # Deprecated in this implementation
    egg_count=50,
    carrying_capacity=1000
):
    # Fixed mutation rate
    mutation_rate = 5.97e-9  # Fixed mutation rate
    
    # Calculate the total number of generations
    num_generations = num_decades * 10  # 10 generations per decade
    
    # Initialize the environment
    environment = Environment(num_patches=num_patches, preset=Environment.cave_presets(preset_name))
    
    # Initialize the population
    population = [Organism() for _ in range(initial_population_size)]

    # Data collection structures
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
        
        # Calculate average fitness for the current population
        avg_fit = np.mean([org.fitness for org in population]) if population else 0
        average_fitness.append(avg_fit)
        
        # Calculate total fitness
        total_fitness = sum(org.fitness for org in population)
        
        # Assign survival probabilities
        for organism in population:
            organism.survival_probability = organism.fitness / total_fitness if total_fitness > 0 else 0
        
        # Determine survivors
        surviving_population = []
        for organism in population:
            if random.random() < organism.survival_probability:
                surviving_population.append(organism)
        
        # Calculate total fitness for reproduction
        total_fitness_repro = sum(org.fitness for org in surviving_population)
        
        # Assign reproduction probabilities
        for organism in surviving_population:
            organism.reproduction_probability = organism.fitness / total_fitness_repro if total_fitness_repro > 0 else 0
        
        # Initialize offspring population list and reproduced set
        offspring_population = []
        reproduced_set = set()
        
        # Create offspring using reproduction probabilities
        for organism in surviving_population:
            if organism in reproduced_set:
                continue  # Skip if already reproduced
            if random.random() < organism.reproduction_probability:
                # Reproduce
                offspring = organism.reproduce()
                # Apply mutation
                offspring.mutate(mutation_rate)
                # Add offspring to the new population
                offspring_population.append(offspring)
                # Mark the organism as having reproduced
                reproduced_set.add(organism)
        
        # Adjust offspring counts if total exceeds carrying capacity
        if len(offspring_population) > carrying_capacity:
            offspring_population = random.sample(offspring_population, carrying_capacity)
            print(f"Generation {generation}: Offspring limited to carrying capacity of {carrying_capacity}.")
        
        # Update population
        population = offspring_population

        # Collect population size data
        population_sizes.append(len(population))
        
        # Collect trait averages
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
    # Uncomment the following block to enable user inputs
    """
    try:
        num_decades = int(input("Enter simulation runtime in decades: "))
        initial_population_size = int(input("Enter initial population size: "))
        preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
        fitness_threshold = float(input("Enter minimum fitness threshold (e.g., 0.2): "))
        num_patches = int(input("Enter number of cave patches (1-5): "))
        egg_count = int(input("Enter egg count per reproduction event (e.g., 3000 for Astyanax mexicanus, 50 for mammoth cave fish): "))
        carrying_capacity = int(input("Enter carrying capacity (usually 500-5000): "))
    except ValueError as e:
        print(f"Invalid input: {e}")
        exit(1)
    """
    
    # Example run with predefined parameters
    run_simulation(
        num_decades=10,
        initial_population_size=500,
        preset_name="default_cave",
        num_patches=1,
        fitness_threshold=0.5,  # Deprecated but kept for compatibility
        egg_count=50,
        carrying_capacity=1000
    )
    # To use user inputs, comment out the above run_simulation call and uncomment the block above.
