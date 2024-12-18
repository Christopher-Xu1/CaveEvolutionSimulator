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
    egg_count=50,
    carrying_capacity=1000
):
    mutation_rate = 5.97e-9
    num_generations = num_decades * 10  # 10 generations per decade
    environment = Environment(num_patches=num_patches, preset=Environment.cave_presets(preset_name))
    population = [Organism() for _ in range(initial_population_size)]

    population_sizes = []
    trait_averages = {"pigmentation": [], "eye_size": [], "metabolic_rate": []}

    for _ in range(1, num_generations + 1):
        environment.change_conditions()
        for patch in environment.patches:
            update_optimal_traits(patch)

        for organism in population:
            organism.move_to_patch(environment)

        for organism in population:
            organism.calculate_fitness(organism.environment_patch)

        # Filter viable population based on fitness
        viable_population = [org for org in population if org.fitness >= fitness_threshold]

        if not viable_population:
            print("Population extinct!")
            break

        # Calculate density-dependent survival rate with a minimum threshold
        survival_rate = max(0.1, 1 - (len(population) / carrying_capacity))

        # Generate offspring based on fitness and survival rate
        offspring_population = []
        for organism in viable_population:
            num_offspring = max(0, int((organism.fitness * egg_count * survival_rate)))
            for _ in range(num_offspring):
                if len(offspring_population) < carrying_capacity:
                    parents = random.choices(
                        viable_population,
                        weights=[org.fitness for org in viable_population],
                        k=2
                    )
                    offspring = Organism.reproduce(parents[0], parents[1])
                    offspring.mutate(mutation_rate)
                    offspring.move_to_patch(environment)
                    offspring.calculate_fitness(offspring.environment_patch)
                    offspring_population.append(offspring)

        population = offspring_population
        # Debugging Output for Current Generation
        print(f"Generation {_}:")
        print(f"- Population Size: {len(population)}")
        print(f"- Average Fitness: {np.mean([org.fitness for org in population]) if population else 0:.4f}")
        print(f"- Survival Rate: {survival_rate:.4f}")
        print(f"- Average Traits:")
        for trait in trait_averages:
            avg_trait = np.mean([org.genetics[trait] for org in population]) if population else 0
            print(f"  - {trait.capitalize()}: {avg_trait:.4f}")
        population_sizes.append(len(population))

        for trait, value in trait_averages.items():
            avg_trait = (
                np.mean([org.genetics[trait] for org in population]) if population else 0
            )
            value.append(avg_trait)

    # Plot population size
    plt.figure(figsize=(12, 6))
    generations = range(len(population_sizes))
    plt.plot(generations, population_sizes, label="Population Size", color="blue", linewidth=2)
    _extracted_from_run_simulation_70(
        "Population Size", "Population Size Over Time"
    )
    # Plot trait averages with relative scaling
    plt.figure(figsize=(12, 6))
    for trait, averages in trait_averages.items():
        if any(averages):  # Check if there are non-zero averages
            scaled_averages = [
                avg / max(averages) if max(averages) > 0 else 0 for avg in averages
            ]
            plt.plot(
                generations,
                scaled_averages,
                label=f"Relative {trait.capitalize()}",
                linewidth=2
            )
    _extracted_from_run_simulation_70(
        "Relative Trait Value", "Relative Trait Evolution Over Time"
    )


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
