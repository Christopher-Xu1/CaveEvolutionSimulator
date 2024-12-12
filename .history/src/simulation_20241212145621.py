import matplotlib.pyplot as plt
import en

def run_simulation(num_decades, initial_population_size, mutation_rate, preset_name, num_patches=1):
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
        reproduction_probabilities = [org.fitness / total_fitness for org in population]

        new_population = []
        for _ in range(len(population)):
            parents = random.choices(population, weights=reproduction_probabilities, k=2)
            offspring = Organism.reproduce(parents[0], parents[1])
            offspring.mutate(mutation_rate)
            offspring.move_to_patch(environment)
            offspring.calculate_fitness(offspring.environment_patch)
            new_population.append(offspring)

        population = new_population
        population_sizes.append(len(population))

        for trait in trait_averages:
            avg_trait = sum(org.genetics[trait] for org in population) / len(population)
            trait_averages[trait].append(avg_trait)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(range(num_generations), population_sizes, label="Population Size")
    plt.xlabel("Generation")
    plt.ylabel("Population Size")
    plt.title("Population Size Over Time")
    plt.legend()
    plt.show()

    for trait, averages in trait_averages.items():
        plt.figure(figsize=(10, 6))
        plt.plot(range(num_generations), averages, label=f"{trait.capitalize()} Average")
        plt.xlabel("Generation")
        plt.ylabel("Trait Value")
        plt.title(f"Evolution of {trait.capitalize()} Over Time")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    num_decades = int(input("Enter simulation runtime in decades: "))
    initial_population_size = int(input("Enter initial population size: "))
    mutation_rate = float(input("Enter mutation rate (e.g., 0.05 for 5%): "))
    preset_name = input("Enter cave preset (default_cave, rich_cave, harsh_cave): ")
    run_simulation(num_decades, initial_population_size, mutation_rate, preset_name)
