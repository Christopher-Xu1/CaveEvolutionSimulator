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
        print(f"Debug: Viable Population Size = {len(viable_population)}, Threshold = {fitness_threshold}")

        if not viable_population:
            print(f"Generation {generation}: Population extinct!")
            break

        # Reproduction and mutation
        offspring_population = []
        # Calculate potential offspring counts
        offspring_counts = []
        total_potential_offspring = 0
        for organism in viable_population:
            count = int((organism.fitness**2) * ((egg_count+organism.environment_patch.get('food_availability'))**2/egg_count))
            offspring_counts.append(count)
            total_potential_offspring += count
            
        # Adjust counts if total exceeds carrying capacity
        if total_potential_offspring > carrying_capacity:
            scale_factor = carrying_capacity / total_potential_offspring
            offspring_counts = carring_capacity
            
        # Create offspring using adjusted counts
        for organism, num_offspring in zip(viable_population, offspring_counts):
            for _ in range(num_offspring):
                parent = random.choice(viable_population)
                offspring = Organism.reproduce(parent, organism)
                offspring.mutate(mutation_rate)
                offspring_population.append(offspring)

        # Update population
        population = offspring_population
        # Collect data
        population_sizes.append(len(population))
        fitness_values = [org.fitness for org in population]
        print(f"Debug: Fitness Values = {fitness_values}")
        average_fitness.append(np.mean(fitness_values) if fitness_values else 0)

        for trait, value in trait_averages.items():
            avg_trait = (
                np.mean([org.genetics[trait] for org in population]) if population else 0
            )
            value.append(avg_trait)

        # Print debugging information
        print(f"Generation {generation}:")
        print(f"  Population Size: {len(population)}")
        print(f"  Average Fitness: {average_fitness[-1]:.4f}")
        print(f"  Trait Averages: {', '.join(f'{trait}: {trait_averages[trait][-1]:.4f}' for trait in trait_averages)}")

    # Plot population size over generations
    plt.figure(figsize=(12, 6))
    _extracted_from_run_simulation_78(
        population_sizes,
        "Population Size",
        "blue",
        "Population Dynamics Over Time",
    )
    _extracted_from_run_simulation_78(
        average_fitness,
        "Average Fitness",
        "green",
        "Fitness Trends Over Generations",
    )
    for trait, averages in trait_averages.items():
        plt.plot(range(len(averages)), averages, label=f"Average {trait.capitalize()}", linewidth=2)
    _extracted_from_run_simulation_79(
        "Trait Value", "Trait Evolution Over Generations"
    )


# TODO Rename this here and in `run_simulation`
def _extracted_from_run_simulation_78(arg0, label, color, arg3):
    plt.plot(range(len(arg0)), arg0, label=label, color=color, linewidth=2)
    _extracted_from_run_simulation_79(label, arg3)
    # Plot average fitness over generations
    plt.figure(figsize=(12, 6))


# TODO Rename this here and in `run_simulation`
def _extracted_from_run_simulation_79(arg0, arg1):
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
